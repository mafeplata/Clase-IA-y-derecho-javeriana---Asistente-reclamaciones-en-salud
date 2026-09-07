"""
Motor RAG (Retrieval-Augmented Generation) para ReclamaSalud.
Proyecto Final: Derecho e Inteligencia Artificial - Pontificia Universidad Javeriana.
Estudiante: Maria Fernanda Plata Silva.
Docente: Pedro Ardila.

Este módulo carga el corpus normativo oficial ubicado en 'corpus/', divide los textos
en fragmentos estructurados con metadatos y recupera los artículos y jurisprudencia
más pertinentes para fundamentar reclamaciones de salud sin inventar normas.
"""

import os
import re
from typing import List, Dict, Any

class CorpusRAG:
    """Motor de indexación y recuperación documental sobre el corpus jurídico colombiano."""

    def __init__(self, corpus_dir: str = None):
        if corpus_dir is None:
            # Localizar la carpeta corpus/ relativa a la raíz del repositorio
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.corpus_dir = os.path.join(base_dir, "corpus")
        else:
            self.corpus_dir = corpus_dir

        self.documents: List[Dict[str, Any]] = []
        self._load_and_chunk_corpus()

    def _load_and_chunk_corpus(self):
        """Carga y segmenta los documentos del corpus por artículos y subreglas."""
        if not os.path.exists(self.corpus_dir):
            print(f"Advertencia: Directorio de corpus no encontrado en {self.corpus_dir}")
            return

        for filename in sorted(os.listdir(self.corpus_dir)):
            if not filename.endswith(".txt"):
                continue

            filepath = os.path.join(self.corpus_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Extraer metadatos de encabezado
            lines = content.split("\n")
            header_title = lines[0].replace("#", "").strip() if lines else filename
            
            # Segmentar por artículos o numerales
            # Patrón para dividir por "ARTÍCULO X." o "NUMERAL X." o "1. PRINCIPIO..."
            chunks = re.split(r"\n(?=(?:ARTÍCULO\s+\d+|[0-9]+\.\s+[A-ZÁÉÍÓÚÑ]))", content)

            for idx, chunk in enumerate(chunks):
                chunk_clean = chunk.strip()
                if not chunk_clean or chunk_clean.startswith("#"):
                    continue

                # Extraer título del artículo o subregla
                first_line = chunk_clean.split("\n")[0]
                section_title = first_line.replace("#", "").strip()

                self.documents.append({
                    "id": f"{filename}_{idx}",
                    "source_file": filename,
                    "source_title": header_title,
                    "section": section_title,
                    "text": chunk_clean
                })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Búsqueda de relevancia en el corpus normativo.
        Calcula puntajes de coincidencia léxico-semántica basados en palabras clave jurídicas.
        """
        if not self.documents:
            return []

        # Palabras clave y tokenización normalizada
        query_terms = set(re.findall(r"\b\w{4,}\b", query.lower()))
        
        # Ponderación de términos jurídicos clave
        legal_boosts = {
            "medicamento": ["medicamento", "fórmula", "farmacia", "desabastecimiento", "pendiente", "suministro"],
            "cita": ["cita", "especialista", "médico", "agenda", "oportunidad", "demora"],
            "urgencia": ["urgencia", "vital", "inmediato", "emergencia", "riesgo"],
            "peticion": ["peticion", "término", "15 días", "resolución", "derecho de petición"],
            "cargas": ["trámite", "barrera", "administrativa", "carga", "traslado"],
            "continuidad": ["continuidad", "interrupción", "suspensión", "tratamiento"],
            "integralidad": ["integral", "integralidad", "completo", "prestación"]
        }

        scored_docs = []
        for doc in self.documents:
            doc_text_lower = doc["text"].lower() + " " + doc["section"].lower()
            score = 0

            # Coincidencias de términos directos
            for term in query_terms:
                if term in doc_text_lower:
                    score += doc_text_lower.count(term)

            # Coincidencias temáticas ponderadas
            for concept, keywords in legal_boosts.items():
                if any(k in query.lower() for k in keywords):
                    for k in keywords:
                        if k in doc_text_lower:
                            score += 2

            if score > 0:
                scored_docs.append((score, doc))

        # Ordenar por puntaje descendente
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]

    def get_formatted_context(self, query: str, top_k: int = 3) -> str:
        """Formatea los fragmentos recuperados para inyectarlos en el prompt del LLM."""
        results = self.search(query, top_k=top_k)
        if not results:
            return "No se encontraron normas específicas directamente aplicables en el corpus."

        context_parts = []
        for i, doc in enumerate(results, 1):
            context_parts.append(
                f"[FUENTE {i}]: {doc['source_title']}\n"
                f"APARTE: {doc['section']}\n"
                f"CONTENIDO:\n{doc['text']}\n"
            )

        return "\n----------------------------------------\n".join(context_parts)

# Instancia reutilizable por defecto
corpus_rag = CorpusRAG()

if __name__ == "__main__":
    print(f"Total de fragmentos jurídicos cargados: {len(corpus_rag.documents)}")
    query_test = "La EPS no me entrega el medicamento para la presión porque dicen que está agotado"
    print(f"\n--- Prueba de consulta: '{query_test}' ---")
    retrieved = corpus_rag.search(query_test, top_k=2)
    for doc in retrieved:
        print(f"-> {doc['source_title']} | {doc['section']}")
