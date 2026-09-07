# 📚 Catálogo y Trazabilidad del Corpus Jurídico — ReclamaSalud

> **Proyecto:** ReclamaSalud — Asistente de reclamaciones de salud  
> **Curso:** Derecho e Inteligencia Artificial · Pontificia Universidad Javeriana (2026-II)  
> **Docente:** Pedro Ardila  
> **Estudiante:** Maria Fernanda Plata Silva  
> **Hito:** M3 — Corpus conectado (RAG)  
> **Ubicación:** `corpus/`  

Este directorio contiene los documentos oficiales que conforman el **corpus normativo cerrado y público** de **ReclamaSalud**. La herramienta utiliza este corpus como base para la generación de fragmentos jurídicos mediante RAG (*Retrieval-Augmented Generation*), garantizando que toda cita jurídica en los borradores de reclamación provenga de fuentes verificables y prohibiendo la invención de normas.

---

## 🏛️ Tabla de Trazabilidad de Fuentes Normativas

| Archivo | Norma / Fuente | Autoridad Emisora | Fecha Oficial | Enlace Oficial de Consulta | Principales Artículos y Materias |
| :--- | :--- | :--- | :---: | :---: | :--- |
| [`01_constitucion_politica_colombia.txt`](./01_constitucion_politica_colombia.txt) | Constitución Política de Colombia | Asamblea Nacional Constituyente | 07/07/1991 | [SUIN-Juriscol](https://www.suin-juriscol.gov.co/viewDocument.asp?id=1687988) | **Art. 23** (Derecho de petición), **Art. 48** (Seguridad Social) y **Art. 49** (Atención a la salud). |
| [`02_ley_estatutaria_1751_de_2015.txt`](./02_ley_estatutaria_1751_de_2015.txt) | Ley Estatutaria 1751 de 2015 | Congreso de la República de Colombia | 16/02/2015 | [MinSalud](https://minsalud.gov.co/Normatividad_Nuevo/Ley%201751%20de%202015.pdf) | **Art. 2** (Derecho fundamental autónomo), **Art. 6** (Principios: oportunidad, continuidad, integralidad), **Art. 8** (Integralidad), **Art. 10** (Derechos del paciente), **Art. 11** (Sujetos de especial protección) y **Art. 14** (Urgencias obligatorias sin copago). |
| [`03_ley_1755_de_2015_derecho_peticion.txt`](./03_ley_1755_de_2015_derecho_peticion.txt) | Ley 1755 de 2015 (Regulación CPACA) | Congreso de la República de Colombia | 30/06/2015 | [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma_pdf.php?i=65334) | **Art. 13** (Objeto y modalidades), **Art. 14** (Término legal general de 15 días hábiles), **Art. 16** (Contenido mínimo) y **Art. 32** (Peticiones ante EPS y particulares prestadores de servicios públicos). |
| [`04_resolucion_229_de_2020_minsalud.txt`](./04_resolucion_229_de_2020_minsalud.txt) | Resolución 229 de 2020 | Ministerio de Salud y Protección Social | 14/02/2020 | [MinSalud (RIDE)](https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-229-de-2020.pdf) | Carta de Derechos del Paciente: derecho a entrega completa de medicamentos (48 horas si queda pendiente), citas sin dilaciones y canales de PQRS. |
| [`05_circular_externa_2023151000000010_5_supersalud.txt`](./05_circular_externa_2023151000000010_5_supersalud.txt) | Circular Externa 2023151000000010-5 | Superintendencia Nacional de Salud | 22/11/2023 | [SuperSalud](https://docs.supersalud.gov.co/PortalWeb/Juridica/CircularesExterna/Circular%20Externa%20No.%202023151000000010-5%20de%202023.pdf) | Instrucciones PQRD en salud: clasificación por nivel de riesgo (Vital: < 24 horas; Priorizado: 48–72 horas; Ordinario: 15 días) y prohibición de barreras farmacéuticas. |
| [`06_sentencia_t760_de_2008_corte_constitucional.txt`](./06_sentencia_t760_de_2008_corte_constitucional.txt) | Sentencia T-760 de 2008 | Corte Constitucional de Colombia | 31/07/2008 | [Corte Constitucional](https://www.corteconstitucional.gov.co/relatoria/2008/t-760-08.htm) | Subreglas vinculantes: principio de continuidad del tratamiento médico, prohibición de trasladar trámites y barreras burocráticas al usuario, y valor prevalente de la orden del médico tratante. |

---

## ⚙️ Estrategia de Curaduría y Segmentación (Chunking)

1. **Delimitación sustantiva:** La Sentencia T-760/08 y los decretos reglamentarios generales superan miles de páginas. Para maximizar la relevancia en el sistema RAG, se seleccionaron los núcleos dogmáticos y las reglas decisionales directamente asociadas a la presentación de reclamaciones iniciales y derechos de petición ante EPS.
2. **Encabezados semánticos:** Cada archivo de texto cuenta con encabezados `#` y etiquetas normativas claras (`ARTÍCULO X`, `PRINCIPIO DE...`). Esto permite que el segmentador (*RecursiveCharacterTextSplitter*) conserve la unidad de sentido de cada artículo y mantenga la cita exacta de la fuente en los metadatos.
3. **Control anti-alucinación:** Si el sistema de búsqueda vectorial no encuentra similitud relevante con ninguna de estas fuentes para una consulta determinada, el asistente activa la regla de denegación: *"No cuento con información jurídica suficiente en mi corpus normativo para responder a este punto específico."*
