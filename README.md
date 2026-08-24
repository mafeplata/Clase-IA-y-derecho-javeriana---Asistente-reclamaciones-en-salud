# ⚖️🤖 Proyecto Final — Derecho e Inteligencia Artificial

**Pontificia Universidad Javeriana · 2026-II · Docente: Pedro Ardila**

> **Estudiante:** Maria Fernanda Plata Silva
> **Nombre del proyecto:** Asistente de reclamaciones de salud
> **Fecha de inicio:** 2026-08-18

---

Bienvenido/a a tu repositorio de proyecto. **Este archivo es tu tablero de mando**: aquí describes tu proyecto, planificas su desarrollo y dejas evidencia del avance. Lo vas a completar por partes, siguiendo el curso.

📌 Si ya habías escrito una descripción de tu proyecto cuando creaste el repo, la encuentras intacta en `README-ORIGINAL.md`. Úsala como punto de partida para la Parte 1 — no empieces de cero.

**No necesitas saber programar.** Todo el código lo construirás con asistencia de IA (*vibe coding*). Tu valor como estudiante de derecho está en el problema que eliges, las fuentes que alimentas, las instrucciones que diseñas y el juicio crítico con el que evalúas el resultado.

---

## 📋 Parte 1 — Descripción del proyecto

> Completa cada sección con 3–10 frases. Sé concreto/a: esta descripción es la que tu IA usará como contexto y la que el docente usará para realimentarte.

### 1.1 El problema jurídico
¿Qué problema **real del derecho colombiano** resuelve tu herramienta? ¿Quién lo sufre hoy y cómo lo resuelve sin tu herramienta?

En Colombia, muchos usuarios del sistema de salud encuentran dificultades para acceder a los servicios que necesitan, como medicamentos, citas médicas, exámenes, procedimientos, tratamientos y atención especializada. Estas dificultades pueden consistir en negativas, demoras injustificadas, interrupciones del servicio, barreras administrativas o ausencia de una respuesta clara por parte de la EPS.

Muchas personas no saben cómo presentar una reclamación, qué información deben incluir, qué deben solicitar ni cuáles normas pueden respaldar su petición. Actualmente, los usuarios deben buscar modelos generales en internet, acudir presencialmente a diferentes entidades o solicitar ayuda profesional, lo que puede generar confusión y retrasar la solución del problema.

El proyecto busca facilitar la elaboración de una reclamación inicial mediante una entrevista guiada. La herramienta organizará los hechos, identificará información faltante y generará un borrador dirigido a la EPS, sustentado en un corpus jurídico previamente seleccionado. También explicará posibles pasos posteriores cuando la EPS no responda o la situación requiera la intervención de otra entidad.

La herramienta no determinará de manera definitiva que exista una vulneración de derechos, no garantizará un resultado favorable y no sustituirá la asesoría de un abogado ni la atención de un profesional de la salud.

---

### 1.2 Usuarios
¿Quién va a usarla? Describe a tu usuario ideal en una frase (ej. *"un arrendatario bogotano que le subieron el canon de arrendamiento más del límite legal"*). Recuerda que al final necesitas **al menos un usuario real** que la pruebe.

La herramienta está dirigida a personas afiliadas a una EPS en Colombia que enfrentan dificultades para acceder a medicamentos, citas, exámenes, procedimientos, tratamientos u otros servicios de salud.

Su usuario ideal es una persona que recibió una negativa, experimenta una demora o encuentra una barrera administrativa, pero no sabe cómo presentar una reclamación clara ante su EPS. No necesita tener conocimientos jurídicos ni experiencia redactando documentos legales.

La herramienta utilizará preguntas sencillas para ayudar al usuario a organizar los hechos y expresar concretamente sus solicitudes. También podrá ser utilizada por familiares o cuidadores que ayuden al paciente, siempre que estén autorizados para actuar en su nombre cuando sea necesario.

Durante la etapa académica, las pruebas se realizarán con situaciones ficticias y datos inventados para evitar el tratamiento de información personal o médica real.

**Usuario ideal en una frase:**

> Una persona afiliada a una EPS en Colombia que enfrenta una barrera de acceso a un servicio de salud y necesita ayuda para redactar una reclamación inicial.

---

### 1.3 Qué hace y qué NO hace (alcance)
| ✅ Sí hace | ❌ No hace |
| --- | --- |
| Realiza preguntas para conocer el problema del usuario con su EPS. | No proporciona diagnósticos médicos. |
| Identifica si el caso se relaciona con una demora, negativa, interrupción o barrera administrativa. | No recomienda medicamentos, tratamientos ni procedimientos médicos. |
| Organiza cronológicamente los hechos relatados por el usuario. | No inventa hechos que el usuario no haya proporcionado. |
| Señala qué información importante hace falta. | No determina definitivamente que la EPS vulneró un derecho. |
| Genera un borrador de reclamación inicial dirigido a la EPS. | No garantiza que la reclamación sea aceptada. |
| Propone solicitudes concretas para incluir en la reclamación. | No presenta ni radica automáticamente la reclamación. |
| Explica en lenguaje sencillo las normas encontradas en su corpus. | No actúa en representación del usuario. |
| Cita las fuentes jurídicas utilizadas en la respuesta. | No inventa normas, artículos, sentencias, autoridades ni plazos. |
| Sugiere documentos que podrían anexarse a la reclamación. | No verifica la autenticidad o validez de los documentos. |
| Informa sobre posibles pasos posteriores, como acudir a la Supersalud o buscar orientación profesional. | No elabora automáticamente demandas ni acciones de tutela. |
| Muestra una alerta cuando el relato indica una posible urgencia. | No sustituye los servicios de urgencias, un médico o un abogado. |
| Permite copiar o descargar el borrador generado. | No almacena historias clínicas ni datos sensibles en la versión académica. |
| Reconoce cuando el corpus no contiene información suficiente. | No responde jurídicamente asuntos que estén fuera de su corpus. |

**Advertencia obligatoria:**

> Esta herramienta es un ejercicio académico. No constituye asesoría legal, no ofrece orientación médica y no sustituye la consulta con un abogado, un profesional de la salud o las autoridades competentes. En una emergencia médica, comuníquese con los servicios de emergencia o acuda inmediatamente al centro asistencial más cercano.

**Regla principal del asistente:**

> La herramienta ayuda a organizar los hechos y redactar una reclamación inicial, pero no decide el caso, no realiza diagnósticos y no promete resultados.

---

*Consejo de abogado: un alcance pequeño y perfecto vale más que uno grande y roto.*

### 1.4 Marco jurídico y fuentes
¿Qué normas alimentan tu herramienta? Lista tu corpus normativo (leyes, decretos, sentencias — debe ser **pequeño y público**):
La herramienta se fundamentará en normas colombianas relacionadas con el derecho fundamental a la salud, el acceso a servicios sanitarios, los derechos de los afiliados y la presentación de reclamaciones.

Para reducir errores, la primera versión utilizará un corpus pequeño compuesto por fuentes públicas y oficiales. El asistente solo podrá formular afirmaciones jurídicas respaldadas por estas fuentes y deberá citar la norma, artículo o sentencia correspondiente.

Si el corpus no contiene información suficiente para responder un caso, la herramienta deberá reconocer esa limitación en lugar de inventar una respuesta.

#### Corpus principal

- [ ] **Constitución Política de Colombia — artículos 23, 48 y 49.**  
  El artículo 23 reconoce el derecho de petición; el artículo 48 regula la seguridad social; y el artículo 49 garantiza el acceso a los servicios de promoción, protección y recuperación de la salud.  
  [Consultar en SUIN-Juriscol](https://www.suin-juriscol.gov.co/viewDocument.asp?id=1687988)

- [ ] **Ley Estatutaria 1751 de 2015 — derecho fundamental a la salud.**  
  Será la fuente principal para explicar principios como oportunidad, continuidad, accesibilidad, calidad e integralidad. También contiene derechos y deberes relacionados con la prestación de servicios de salud.  
  [Consultar en el Ministerio de Salud](https://minsalud.gov.co/Normatividad_Nuevo/Ley%201751%20de%202015.pdf)

- [ ] **Ley 1755 de 2015 — derecho de petición.**  
  Define para qué sirve una petición, su contenido mínimo y los términos generales de respuesta. Será utilizada para construir la estructura formal de las reclamaciones.  
  [Consultar en Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma_pdf.php?i=65334)

- [ ] **Resolución 229 de 2020 — Carta de derechos y deberes del afiliado y del paciente.**  
  Contiene los derechos de las personas afiliadas y las obligaciones informativas de las EPS.  
  [Consultar en el Ministerio de Salud](https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-229-de-2020.pdf)

- [ ] **Circular Externa 2023151000000010-5 de 2023 — Superintendencia Nacional de Salud.**  
  Contiene instrucciones sobre la recepción y gestión de peticiones, quejas y reclamos en salud. También clasifica los reclamos según su riesgo y establece términos diferenciados para su gestión.  
  [Consultar en la Superintendencia Nacional de Salud](https://docs.supersalud.gov.co/PortalWeb/Juridica/CircularesExterna/Circular%20Externa%20No.%202023151000000010-5%20de%202023.pdf)

- [ ] **Sentencia T-760 de 2008 — Corte Constitucional.**  
  Reúne reglas importantes sobre el acceso efectivo a los servicios de salud, las barreras administrativas, la continuidad y la obligación de prestar los servicios de manera oportuna, eficiente y con calidad.  
  [Consultar en la Corte Constitucional](https://www.corteconstitucional.gov.co/relatoria/2008/t-760-08.htm)

#### Fuentes complementarias

Estas fuentes podrán incorporarse después de probar correctamente el corpus principal:

- [ ] **Decreto 780 de 2016 — Decreto Único Reglamentario del Sector Salud.**  
  Debido a su extensión y modificaciones, solamente se seleccionarán los artículos directamente relacionados con el alcance del proyecto.  
  [Consultar en el Ministerio de Salud](https://minsalud.gov.co/Normativa/paginas/decreto-unico-minsalud-780-de-2016.aspx)

- [ ] **Sentencia SU-508 de 2020 — Corte Constitucional.**  
  Puede utilizarse para estudiar el acceso a servicios y tecnologías en salud y los mecanismos de protección disponibles.  
  [Consultar en la Corte Constitucional](https://www.corteconstitucional.gov.co/relatoria/2020/su508-20.htm)

- [ ] **Canales oficiales de PQRD de la Superintendencia Nacional de Salud.**  
  Se utilizarán para informar al usuario dónde puede presentar o consultar una reclamación.  
  [Consultar en la Superintendencia Nacional de Salud](https://www.supersalud.gov.co/es-co/Paginas/Protecci%C3%B3n%20al%20Usuario/atencion-al-ciudadano.html)

#### Protección de datos

- [ ] **Ley 1581 de 2012 — protección de datos personales.**  
  Los datos relacionados con la salud son datos sensibles. Por esta razón, el prototipo académico no almacenará historias clínicas, diagnósticos, documentos de identidad ni anexos reales. Las pruebas se realizarán con información ficticia.  
  [Consultar en Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?country=76&i=49981&offset=0)

---

### 1.5 Nombre y lema
Un nombre corto para tu herramienta y una frase que explique qué hace (la usarás en la demo del día de presentaciones).
**Nombre:** ReclamaSalud

**Lema:** Organiza tu caso y crea una reclamación clara para tu EPS.

**Descripción:**

ReclamaSalud es un asistente académico que ayuda a las personas afiliadas a una EPS en Colombia a organizar un problema de acceso a servicios de salud y generar un borrador de reclamación basado en fuentes jurídicas verificables.

La herramienta no sustituye la asesoría legal ni la atención de un profesional de la salud.
---

## 🗺️ Parte 2 — Plan de desarrollo

Marca cada hito cuando lo termines. Los hitos siguen las sesiones del curso.

- [ ] **M0 — Descripción y plan** *(con Sesión 1)*: Partes 1 y 2 de este README completas.
- [ ] **M1 — Asistente con instrucciones v1** *(Sesión 1–2)*: redactaste las instrucciones (prompt de sistema) de tu asistente y funcionan en una herramienta gratuita de chat.
- [ ] **M2 — Casos de prueba documentados** *(Sesión 2)*: tienes al menos 5 casos de prueba (donde antes fallaba) con resultados guardados en `docs/casos-de-prueba.md`.
- [ ] **M3 — Corpus conectado (RAG)** *(Sesión 3)*: tu asistente **cita la fuente** normativa que usa y no inventa. Corpus cargado en `corpus/`.
- [ ] **M4 — Interfaz web desplegada** *(Sesión 4)*: tu herramienta tiene **URL pública** (ver Parte 4) y tu primer usuario real la probó con evidencia.
- [ ] **M5 — Análisis crítico y demo** *(Sesión 5)*: Parte 7 completada + presentación de 5 minutos.

### Bitácora de avance semanal
- [x] **M0 — Descripción y plan** *(Sesión 1)*  
  Se completaron las Partes 1 y 2 del README. Se definieron el problema jurídico, los usuarios, el alcance, las fuentes jurídicas iniciales, el nombre del proyecto y el plan de desarrollo.

- [ ] **M1 — Asistente con instrucciones v1** *(Sesiones 1 y 2)*  
  Redactar y probar el prompt de sistema de ReclamaSalud. El asistente deberá organizar los hechos, solicitar información faltante, utilizar únicamente las fuentes suministradas y reconocer cuando no pueda responder.

- [ ] **M2 — Casos de prueba documentados** *(Sesión 2)*  
  Diseñar al menos cinco casos ficticios para evaluar el asistente. Los casos deberán incluir situaciones correctas, información incompleta, consultas fuera del alcance y solicitudes que puedan provocar respuestas inventadas.

- [ ] **M3 — Corpus conectado mediante RAG** *(Sesión 3)*  
  Descargar, organizar y conectar las fuentes jurídicas seleccionadas. El asistente deberá recuperar los fragmentos pertinentes y citar la norma, el artículo o la sentencia utilizada en cada respuesta.

- [ ] **M4 — Interfaz web desplegada** *(Sesión 4)*  
  Crear una interfaz sencilla donde el usuario pueda responder preguntas, revisar la información de su caso y generar un borrador de reclamación. La herramienta deberá tener una advertencia visible y una URL pública.

- [ ] **M5 — Análisis crítico y presentación** *(Sesión 5)*  
  Probar la herramienta con al menos un usuario, documentar sus resultados, identificar limitaciones y preparar una presentación de cinco minutos.

---

### Actividades previstas por hito

#### M0 — Descripción y plan

- [x] Definir el problema jurídico.
- [x] Identificar a los usuarios.
- [x] Establecer qué hace y qué no hace la herramienta.
- [x] Seleccionar las fuentes jurídicas iniciales.
- [x] Escoger el nombre y el lema.
- [x] Elaborar el plan de desarrollo.

#### M1 — Instrucciones del asistente

- [ ] Redactar la primera versión del prompt de sistema.
- [ ] Definir las preguntas que realizará al usuario.
- [ ] Establecer la estructura de las respuestas.
- [ ] Incluir reglas contra la invención de normas y hechos.
- [ ] Incluir la advertencia académica, jurídica y médica.
- [ ] Probar el prompt en una herramienta de chat.

#### M2 — Casos de prueba

- [ ] Crear casos ficticios de demoras y negativas de servicios.
- [ ] Crear un caso con información incompleta.
- [ ] Crear un caso que se encuentre fuera del alcance.
- [ ] Crear un caso con una posible urgencia médica.
- [ ] Crear un caso que intente hacer que el modelo invente una norma.
- [ ] Documentar los resultados en `docs/casos-de-prueba.md`.
- [ ] Corregir las instrucciones según los errores encontrados.

#### M3 — Corpus y RAG

- [ ] Descargar las fuentes desde sitios oficiales.
- [ ] Seleccionar los artículos y fragmentos pertinentes.
- [ ] Guardar los documentos en la carpeta `corpus/`.
- [ ] Registrar el nombre, autoridad, fecha y enlace de cada fuente.
- [ ] Dividir los documentos en fragmentos utilizables.
- [ ] Conectar el corpus mediante RAG.
- [ ] Verificar que las citas correspondan con las fuentes.
- [ ] Probar que el asistente se niegue a inventar respuestas.

#### M4 — Interfaz y despliegue

- [ ] Crear el formulario de entrevista.
- [ ] Mostrar un resumen de los hechos.
- [ ] Generar el borrador de reclamación.
- [ ] Permitir copiar o descargar el documento.
- [ ] Mostrar las fuentes jurídicas utilizadas.
- [ ] Mostrar la advertencia obligatoria.
- [ ] Evitar el almacenamiento de datos sensibles.
- [ ] Publicar la herramienta en una URL accesible.

#### M5 — Evaluación y presentación

- [ ] Realizar una prueba con un usuario.
- [ ] Utilizar únicamente casos ficticios o datos inventados.
- [ ] Guardar evidencia de la prueba.
- [ ] Registrar los comentarios del usuario.
- [ ] Identificar por lo menos dos limitaciones.
- [ ] Completar el análisis crítico de la Parte 7.
- [ ] Preparar la demostración de cinco minutos.

---

### Bitácora de avance semanal

| Semana | Qué hice | Evidencia | Dudas para la clase |
| --- | --- | --- | --- |
| 1-3 | Definí el problema jurídico, los usuarios, el alcance, las fuentes iniciales, el nombre y el lema de ReclamaSalud. También elaboré el plan de desarrollo. | Partes 1 y 2 del README. | ¿El corpus inicial es adecuado y suficientemente delimitado para el proyecto? |
| 4-7 | Pendiente: redactar y probar el prompt de sistema. | Pendiente. | Pendiente. |
| 7-10| Pendiente: crear casos de prueba y organizar el corpus. | Pendiente. | Pendiente. |
| 11-13 | Pendiente: conectar el sistema RAG y construir la interfaz. | Pendiente. | Pendiente. |
| 14-16| Pendiente: desplegar, probar con un usuario y preparar la presentación. | Pendiente. | Pendiente. |

---

### Estado actual del proyecto

**Hito actual:** M0 — Descripción y plan.

**Estado:** Completado.

**Próximo hito:** M1 — Asistente con instrucciones v1.

En esta etapa todavía no se ha escrito código, no se ha conectado un modelo de lenguaje, no se ha construido el sistema RAG y no existe una interfaz pública. Estas actividades se realizarán en los siguientes hitos.
---

## 🛠️ Parte 3 — Stack técnico recomendado

Todo es **gratuito y no exige tarjeta de crédito**. Tu proyecto final debería verse así:

```
[Usuario] → [Interfaz web] → [Orquestación (LangChain)] → [Modelo (OpenRouter)]
                                   ↕
                          [Tu corpus normativo (RAG)]
```

| Pieza | Herramienta recomendada | Para qué sirve (en cristiano) |
| --- | --- | --- |
| **Interfaz web** | **v0.dev** (genera una app Next.js) o **Streamlit** (si tu agente trabaja en Python) | Lo que el usuario ve: cajas de texto, botones. Se la describes a la IA y ella la construye. |
| **Orquestación** | **LangChain / LangGraph** | El "cerebro intermedio": toma la pregunta del usuario, busca en tus normas, arma el prompt y llama al modelo. |
| **Modelo (LLM)** | **OpenRouter** — modelos con etiqueta `:free` | El "cerebro" que redacta. OpenRouter te da acceso a modelos gratuitos con una sola cuenta y una sola API key. |
| **Memoria de fuentes (RAG)** | LangChain + almacén de vectores (**Chroma** o **FAISS** en local; **Supabase** si necesitas base de datos en la nube) | La técnica para que el modelo responda **con tus normas** y no con lo que "recuerda" (que puede ser una alucinación jurídica). |
| **Trazabilidad** *(opcional)* | **LangSmith** (plan gratuito) | Ver qué le pasó a cada respuesta por dentro. Útil para depurar. |

> 🔑 **Regla de oro:** tu `OPENROUTER_API_KEY` va en una **variable de entorno**, jamás pegada en el código ni en el chat. Si una clave se filtra en GitHub, revócala de inmediato en openrouter.ai → Keys.

Pídele a tu agente de IA que te explique esta arquitectura con tu proyecto concreto antes de escribir una línea de código.

---

## 🚀 Parte 4 — Ruta de despliegue

Tu meta: **una URL pública** que cualquiera pueda abrir. Elige una ruta:

### Opción A — Vercel ⭐ (recomendada, la del curso)
1. Sube tu código a este repo de GitHub (ya lo tienes ✅).
2. Crea cuenta gratis en [vercel.com](https://vercel.com) con tu GitHub.
3. "Add New Project" → importa tu repo → Deploy.
4. Cada `git push` re-despliega solo.
- ✅ Ideal para Next.js/Streamlit (Streamlit via [streamlit.io/community-cloud](https://streamlit.io)) · gratis · sin servidor.

### Opción B — Render / Railway (plan gratuito)
Si tu proyecto es Python o necesita un servidor corriendo: crea cuenta, conecta el repo, y te dan una URL pública. Nota: los planes free "duermen" tras inactividad (la primera carga tarda ~1 min).

### Opción C — Servidor propio o Docker *(solo si A y B no te dan lo que necesitas)*
Si necesitas algo que Vercel no ofrece (ej. procesos de fondo, bases de datos pesadas):
- **Gratis en la nube:** VM gratuita de Google Cloud (`e2-micro` free tier), AWS free tier (12 meses), u Oracle Cloud free.
- **Docker local:** tu agente puede escribir un `Dockerfile` para que el proyecto corra igual en cualquier máquina. Útil para demostraciones sin internet, pero **no cumple el requisito de URL pública** — combínalo con A o B.

### Checklist de despliegue ✅
- [ ] URL pública funciona en el navegador de otra persona (pídele a alguien que la abra)
- [ ] La advertencia de la Parte 7 es **visible** en la interfaz
- [ ] No hay API keys ni secretos en el código (verifica con una búsqueda de `sk-` en el repo)
- [ ] Anota la URL aquí: **`[tu-url-publica]`**

> El dominio propio (.com, .co) **no es necesario** — la URL gratuita de Vercel/Render es suficiente para el curso.

---

## 🧠 Parte 5 — Guía de prompting para *vibe coding*

Tu competencia más transferible a la práctica profesional: **instruir bien a la IA**. Reglas:

1. **Un hito a la vez.** No le pidas "hazme todo el proyecto". Pide: "vamos por M1".
2. **Da contexto jurídico, recibe código.** Pega tu Parte 1 y dile: "eres mi ingeniero, yo soy el abogado del proyecto".
3. **Pide explicaciones.** "Explícame como a alguien que no sabe programar qué acabas de hacer."
4. **Commits frecuentes.** Cada vez que algo funcione: `git add . && git commit -m "M1: instrucciones del asistente"` y push. Si rompes algo, siempre puedes volver atrás.
5. **Nunca pegues datos personales reales** de usuarios en el chat ni en el código (Ley 1581).
6. **Verifica como abogado.** Toda respuesta legal que dé la herramienta, contrástala con la norma. Tú respondes por lo que publicas.

### Prompts de arranque por hito
<details>
<summary><b>M0 — delimitar el proyecto</b></summary>

> "Soy estudiante de derecho primer semestre. Mi idea de proyecto es [idea]. Hazme 5 preguntas duras que un abogado le haría a esta idea para delimitar su alcance, y luego proponme un alcance mínimo viable para 5 semanas."
</details>

<details>
<summary><b>M1 — instrucciones del asistente</b></summary>

> "Escribe el prompt de sistema de mi asistente jurídico. Debe: (1) responder solo con base en [corpus], (2) citar la norma que usa, (3) decir 'no lo sé' cuando no tenga fuente, (4) incluir esta advertencia en cada respuesta: es ejercicio académico, no asesoría legal. Proponme 3 versiones y explícame las diferencias."
</details>

<details>
<summary><b>M3 — RAG con mis normas</b></summary>

> "Tengo [ley X] en archivos de texto en /corpus. Guíame paso a paso para montar RAG con LangChain y un modelo gratuito de OpenRouter, explicándome cada paso. Al final, el asistente debe citar artículo y norma en cada respuesta."
</details>

<details>
<summary><b>M4 — interfaz y despliegue</b></summary>

> "Crea una interfaz web simple para mi asistente: un recuadro para escribir la consulta, el espacio de respuesta, la advertencia legal visible arriba, y el logo/nombre. Luego guíame para desplegarla gratis en Vercel con mi repo de GitHub. No sé programar: dime exactamente qué archivo tocar y qué copiar."
</details>

---

## ⚖️ Parte 6 — Ética, datos y responsabilidad

Estas salvaguardas son **obligatorias** y hacen parte de la evaluación:

- **Advertencia visible obligatoria.** Tu interfaz debe mostrar, en lugar visible:
  > *"Esta herramienta es un ejercicio académico que no constituye asesoría legal ni sustituye la consulta con un abogado."*
  - [ ] Implementada y visible en la interfaz
- **Protección de datos (Ley 1581 de 2012).** Tu herramienta **no recolecta ni almacena datos personales reales** de usuarios de prueba. Los usuarios de prueba usan situaciones ficticias o datos inventados.
  - [ ] Verificado: no guardo datos personales
- **Corpus público.** Solo fuentes públicas: leyes, decretos, jurisprudencia publicada.
  - [ ] Verificado
- **Anti-alucinaciones.** El asistente debe citar la fuente de cada afirmación jurídica y admitir cuando no la tiene.
  - [ ] Casos de prueba donde la herramienta se niega a inventar

---

## 🔍 Parte 7 — Análisis crítico (insumo de tu sustentación final)

Responde con total honestidad — aquí es donde demuestras tu criterio jurídico:

1. **¿Dónde falla tu herramienta?** Describe 2 situaciones donde se equivoca o se queda corta.
2. **¿Qué datos procesa?** Qué entra, qué se guarda, qué sale.
3. **¿Por qué no reemplaza al abogado?** Argumenta en 5–8 frases.

---

## ✅ Parte 8 — Entregables finales (Definition of Done)

Requisitos de entrega del curso — todos deben estar ✅:

- [ ] 🔗 **Solución funcionando**: resuelve el problema jurídico y está desplegada con URL pública.
- [ ] 👤 **Usuario real**: al menos una persona externa al curso la usó, con evidencia (video corto o testimonio). Guarda la evidencia en `docs/evidencia-usuario.md`.
- [ ] 📦 **Repositorio con historial**: este repo muestra tus avances semanales (commits + bitácora).
- [ ] 🧠 **Análisis crítico**: Parte 7 completada.
- [ ] 📋 Partes 1–7 de este README completas y al día.

---

*Construido con asistencia de IA — como se enseña en este curso.* 🧑‍⚖️🤖
