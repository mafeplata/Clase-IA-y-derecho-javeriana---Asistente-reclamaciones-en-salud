# 🚀 Guía de Despliegue en Streamlit Community Cloud — Hito M4

> **Proyecto:** ReclamaSalud — Asistente de reclamaciones de salud  
> **Curso:** Derecho e Inteligencia Artificial · Pontificia Universidad Javeriana  
> **Docente:** Pedro Ardila  
> **Estudiante:** Maria Fernanda Plata Silva  
> **Hito:** M4 — Interfaz web desplegada con URL pública  
> **Servicio:** [Streamlit Community Cloud](https://streamlit.io/community-cloud) (100% gratuito y sin tarjeta de crédito)

---

## 🎯 Objetivo de este hito

El objetivo del **Hito M4** es publicar **ReclamaSalud** en una **URL pública en internet** para que cualquier persona (el docente, compañeros o un usuario de prueba) pueda acceder desde su navegador o teléfono celular sin necesidad de instalar nada en su computador.

---

## 📋 Requisitos previos

1. Tu repositorio de GitHub al día con los archivos del proyecto:
   - `app.py` (aplicación web principal)
   - `requirements.txt` (lista de paquetes necesarios)
   - `corpus/` (textos normativos)
   - `src/rag_engine.py` (motor de búsqueda)
   - `README.md` (tablero de mando)

---

## 🛠️ Pasos para desplegar en 3 minutos

### Paso 1: Iniciar sesión en Streamlit Cloud
1. Entra a [share.streamlit.io](https://share.streamlit.io/).
2. Haz clic en **"Sign in with GitHub"** (inicia sesión con tu misma cuenta de GitHub donde tienes este repositorio).
3. Autoriza a Streamlit el acceso de lectura a tus repositorios.

---

### Paso 2: Crear la aplicación
1. En tu panel de control de Streamlit, haz clic en el botón azul superior: **"Create app"** (o *"New app"*).
2. Selecciona la opción **"I already have an app"**.
3. Diligencia los siguientes tres campos:
   - **Repository:** Selecciona tu repositorio (ejemplo: `tu-usuario/Clase-IA-y-derecho-javeriana---Asistente-reclamaciones-en-salud-main`).
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (opcional):** Puedes personalizar el subdominio si está disponible (por ejemplo: `reclamasalud.streamlit.app`).

---

### Paso 3: Configurar Secretos (Opcional para OpenRouter)
Si deseas que la aplicación utilice un modelo de OpenRouter automáticamente sin que el usuario deba escribir su clave:
1. Haz clic en **"Advanced settings"** (o entra a los ajustes de la app una vez creada $\rightarrow$ *Settings* $\rightarrow$ *Secrets*).
2. En el recuadro de texto escribe:
   ```toml
   OPENROUTER_API_KEY = "tu_clave_de_openrouter_aqui"
   ```
3. Haz clic en **"Save"**.
*(Nota: Si no configuras ninguna clave, la aplicación funcionará de todas formas de manera autónoma utilizando el motor RAG y la plantilla formal canónica).*

---

### Paso 4: Desplegar (*Deploy*)
1. Haz clic en el botón **"Deploy!"**.
2. Streamlit comenzará a construir el entorno en la nube instalando las dependencias de `requirements.txt`.
3. En aproximadamente 1 a 2 minutos, tu aplicación se abrirá en pantalla con una URL pública funcional (ejemplo: `https://reclamasalud.streamlit.app`).

---

## ✅ Checklist de Verificación de Despliegue (Parte 4 del README)

Una vez que la aplicación esté en línea, verifica los siguientes puntos:

- [ ] La **URL pública** abre correctamente en el navegador de otra persona o en tu celular.
- [ ] La **advertencia obligatoria** (ejercicio académico / no asesoría legal ni médica) es visible arriba.
- [ ] El **protocolo de triage ético** (alerta médica de urgencias) funciona al marcar la casilla de alarma.
- [ ] El formulario genera el **Derecho de Petición con citas exactas** del corpus normativo.
- [ ] El botón de **descarga de documento (`.txt`)** funciona correctamente.
- [ ] No existen claves de API escritas directamente en el código de GitHub (todas van en secrets).
- [ ] Copia y pega tu URL pública en la **Parte 4 del `README.md`**.
