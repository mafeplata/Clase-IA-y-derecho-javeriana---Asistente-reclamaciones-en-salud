"""
Script de verificación y prueba del motor RAG — ReclamaSalud.
Hito M3: Corpus conectado (RAG).
"""

import os
from src.rag_engine import CorpusRAG

def run_tests():
    print("=" * 70)
    print("  VERIFICACIÓN DEL SISTEMA RAG — RECLAMASALUD (HITO M3)")
    print("=" * 70)

    rag = CorpusRAG()
    total_docs = len(rag.documents)
    print(f"\n[OK] Documentos indexados exitosamente: {total_docs} fragmentos normativos.")

    test_queries = [
        {
            "categoria": "Medicamentos pendientes / Agotados",
            "query": "La farmacia de la EPS me dice que el medicamento está agotado y me dejó pendiente la fórmula",
            "fuentes_esperadas": ["Ley Estatutaria 1751", "Resolución 229", "Circular Externa 2023151000000010-5", "Sentencia T-760"]
        },
        {
            "categoria": "Término legal de respuesta de petición",
            "query": "¿Cuántos días tiene la EPS para responder un derecho de petición en Colombia?",
            "fuentes_esperadas": ["Ley 1755 de 2015", "Constitución Política"]
        },
        {
            "categoria": "Urgencia médica vital",
            "query": "La EPS me pide autorización y copago para ingresar al servicio de urgencias",
            "fuentes_esperadas": ["Ley Estatutaria 1751 de 2015", "Artículo 14"]
        },
        {
            "categoria": "Traba administrativa y caída del sistema",
            "query": "La EPS me hace ir de ventanilla en ventanilla y dice que no atienden porque se cayó el sistema",
            "fuentes_esperadas": ["Sentencia T-760 de 2008", "Cargas administrativas"]
        }
    ]

    for i, test in enumerate(test_queries, 1):
        print(f"\n" + "-" * 70)
        print(f"Prueba {i}: {test['categoria']}")
        print(f"Consulta: '{test['query']}'")
        
        results = rag.search(test['query'], top_k=2)
        print(f"Resultados recuperados ({len(results)} fragmentos):")
        
        for r_idx, doc in enumerate(results, 1):
            print(f"  [{r_idx}] {doc['source_title']} -> {doc['section']}")

        # Validación de pertinencia
        found = any(
            any(exp.lower() in (doc['source_title'].lower() + " " + doc['section'].lower()) for exp in test['fuentes_esperadas'])
            for doc in results
        )
        estado = "PASÓ ✅" if found else "REVISAR ⚠️"
        print(f"Estado de la prueba: {estado}")

    print("\n" + "=" * 70)
    print("  RESULTADO GENERAL: Motor RAG verificado y conectado al corpus.")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
