"""
Directorio Oficial de Canales de Radicación de EPS y Superintendencia Nacional de Salud.
ReclamaSalud — Pontificia Universidad Javeriana.
"""

DIRECTORIO_EPS = {
    "EPS Sanitas": {
        "nombre_completo": "Entidad Promotora de Salud Sanitas S.A.S.",
        "portal_web": "https://www.epssanitas.com",
        "portal_pqrs": "https://www.epssanitas.com",
        "telefono_nacional": "01 8000 919 100",
        "telefono_bogota": "(601) 375 9000",
        "canal_virtual": "Portal Web EPS Sanitas / Oficina Virtual",
        "consejo_radicacion": "Ingresa al portal web oficial de EPS Sanitas con tu tipo y número de documento en la sección 'Oficina Virtual' para radicar en línea, o acude presencialmente a tu centro de atención exigiendo copia sellada con fecha y número de radicado."
    },
    "Nueva EPS": {
        "nombre_completo": "Nueva EPS S.A.",
        "portal_web": "https://www.nuevaeps.com.co",
        "portal_pqrs": "https://www.nuevaeps.com.co",
        "telefono_nacional": "01 8000 954 400 (Contributivo) / 01 8000 952 000 (Subsidiado)",
        "telefono_bogota": "(601) 307 7022",
        "canal_virtual": "Portal Web Nueva EPS / Canales de Atención",
        "consejo_radicacion": "Ingresa al portal web oficial de Nueva EPS e inicia sesión en 'Oficina Virtual' para tramitar tu solicitud, o radica por escrito en la Oficina de Atención al Afiliado más cercana."
    },
    "Sura EPS": {
        "nombre_completo": "EPS y Medicina Prepagada Suramericana S.A.",
        "portal_web": "https://www.epssura.com",
        "portal_pqrs": "https://www.epssura.com",
        "telefono_nacional": "01 8000 519 519",
        "telefono_bogota": "(601) 489 7941",
        "canal_virtual": "Portal Oficial EPS Sura / Servicios en Línea",
        "consejo_radicacion": "Accede a www.epssura.com e inicia sesión en 'Servicios en Línea' con tu usuario para radicar y hacer seguimiento a tu reclamo, o llama a su línea nacional de atención."
    },
    "Salud Total EPS": {
        "nombre_completo": "Salud Total Entidad Promotora de Salud del Régimen Contributivo S.A.",
        "portal_web": "https://saludtotal.com.co",
        "portal_pqrs": "https://saludtotal.com.co",
        "telefono_nacional": "01 8000 1 14524",
        "telefono_bogota": "(601) 485 4555",
        "canal_virtual": "Punto de Atención al Usuario (PAU) Virtual",
        "consejo_radicacion": "Ingresa a saludtotal.com.co e identifícate en el 'Punto de Atención al Usuario (PAU) Virtual' con tu cédula y contraseña para registrar tu PQRD con constancia inmediata."
    },
    "Famisanar EPS": {
        "nombre_completo": "EPS Famisanar SAS",
        "portal_web": "https://www.famisanar.com.co",
        "portal_pqrs": "https://www.famisanar.com.co",
        "telefono_nacional": "01 8000 116 662 (Contributivo) / 01 8000 914 202 (Subsidiado)",
        "telefono_bogota": "(601) 307 8069",
        "canal_virtual": "Oficina Virtual Famisanar",
        "consejo_radicacion": "Ingresa al portal oficial de Famisanar en 'Oficina Virtual' para radicar en línea, o acude a los Centros de Atención al Usuario (CAU) con copia física del documento."
    },
    "Compensar EPS": {
        "nombre_completo": "Compensar Entidad Promotora de Salud",
        "portal_web": "https://www.compensar.com",
        "portal_pqrs": "https://www.compensar.com",
        "telefono_nacional": "01 8000 915 202",
        "telefono_bogota": "(601) 444 1234",
        "canal_virtual": "Portal Web Compensar / Transacciones en Línea",
        "consejo_radicacion": "Ingresa a compensar.com en el módulo de Salud y accede con tus credenciales a 'Transacciones en Línea' para registrar tu queja o reclamo."
    },
    "Savia Salud EPS": {
        "nombre_completo": "Alianza Medellín Antioquia EPS S.A.S. - Savia Salud",
        "portal_web": "https://www.saviasaludeps.com",
        "portal_pqrs": "https://www.saviasaludeps.com",
        "telefono_nacional": "01 8000 423 683",
        "telefono_bogota": "Línea Medellín: (604) 448 1747",
        "canal_virtual": "Página web oficial de Savia Salud",
        "consejo_radicacion": "Ingresa a saviasaludeps.com en la sección 'Atención al Ciudadano' o radica en la oficina de atención municipal más cercana."
    }
}

CANAL_SUPERSALUD = {
    "entidad": "Superintendencia Nacional de Salud (Supersalud)",
    "portal_web": "https://www.supersalud.gov.co",
    "portal_pqrs": "https://www.supersalud.gov.co",
    "linea_gratuita_nacional": "01 8000 513 700",
    "telefono_bogota": "(601) 744 2000",
    "correo": "correoinstitucional@supersalud.gov.co",
    "cuando_acudir": "Acude a la Supersalud si la EPS no responde dentro de los términos legales, niega injustificadamente el servicio prescrito o suspende un tratamiento continuo."
}

def get_eps_info(nombre_eps: str) -> dict:
    """Retorna la ficha de contacto y radicación de la EPS seleccionada."""
    for key, data in DIRECTORIO_EPS.items():
        if key.lower() in nombre_eps.lower():
            return data
    # Información genérica si es 'Otra EPS'
    return {
        "nombre_completo": nombre_eps,
        "portal_web": "https://www.supersalud.gov.co",
        "portal_pqrs": "https://www.supersalud.gov.co",
        "telefono_nacional": "Línea de atención de la entidad",
        "telefono_bogota": "Verificar en la página web oficial de la EPS",
        "canal_virtual": "Portal web de la entidad o ventanilla presencial",
        "consejo_radicacion": "Radica en la oficina de atención al usuario de la EPS o a través de su página web oficial exigiendo constancia de recibido."
    }
