"""
Generador de Documentos Jurídicos en formato PDF para ReclamaSalud.
Utiliza fpdf2 (puro Python, liviano, sin dependencias de C).
ReclamaSalud — Pontificia Universidad Javeriana.
"""

from fpdf import FPDF
import re

class ReclamaSaludPDF(FPDF):
    """Clase personalizada para maquetar el Derecho de Petición con formato judicial."""

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 110, 120)
        self.cell(0, 5, "RECLAMASALUD — ASISTENTE ACADÉMICO DE SALUD | PONTIFICIA UNIVERSIDAD JAVERIANA", 0, 1, "C")
        self.set_draw_color(180, 190, 200)
        self.line(20, 14, 190, 14)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}} · Documento para radicación ciudadana ante la EPS (Ley 1755 de 2015)", 0, 0, "C")


def sanitize_text_for_pdf(text: str) -> str:
    """
    Limpia y normaliza caracteres Unicode complejos para que fpdf2
    los renderice sin error en la tipografía estándar Helvetica (latin-1).
    """
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "*",
        "⚖️": "",
        "🚨": "",
        "📋": "",
        "✅": "",
        "⚠️": "",
        "💡": "",
        "🏥": "",
        "📄": "",
        "🔍": "",
        "📌": "",
        "📥": ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Reemplazar cualquier caracter no representable en latin-1
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_petition_pdf(petition_text: str) -> bytes:
    """
    Convierte el texto completo del Derecho de Petición en un archivo PDF formal.
    Retorna los bytes listos para descarga en Streamlit.
    """
    clean_text = sanitize_text_for_pdf(petition_text)

    pdf = ReclamaSaludPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.alias_nb_pages()
    pdf.add_page()

    lines = clean_text.split("\n")
    for line in lines:
        stripped = line.strip()
        
        # Separadores decorativos
        if stripped.startswith("====") or stripped.startswith("----"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(3)
            continue

        # Títulos de sección (I. HECHOS, II. PETICIONES, etc.)
        if re.match(r"^(I|II|III|IV|V)\.\s+[A-ZÁÉÍÓÚÑ\s]+", stripped) or stripped.startswith("ASUNTO:"):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 30, 60)
            pdf.multi_cell(0, 5, stripped)
            pdf.ln(1)
        # Encabezado (Señores EPS, Ciudad, etc.)
        elif stripped.startswith("Señores:") or stripped.startswith("Peticionario") or stripped.startswith("Atentamente,"):
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(30, 40, 50)
            pdf.multi_cell(0, 5, stripped)
            pdf.ln(1)
        # Advertencia final
        elif "ADVERTENCIA:" in stripped:
            pdf.ln(2)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(120, 30, 30)
            pdf.multi_cell(0, 4, stripped)
        # Texto general de párrafos
        else:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(20, 25, 30)
            if stripped:
                pdf.multi_cell(0, 5, stripped)
            else:
                pdf.ln(2)

    return bytes(pdf.output())
