"""
Directorio Oficial de Canales de Radicación de EPS y Superintendencia Nacional de Salud.
ReclamaSalud — Pontificia Universidad Javeriana.
"""

DIRECTORIO_EPS = {
    "EPS Sanitas": {
        "nombre_completo": "Entidad Promotora de Salud Sanitas S.A.S.",
        "portal_pqrs": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/pqrs",
        "telefono_nacional": "01 8000 919 100",
        "telefono_bogota": "(601) 375 9000",
        "canal_virtual": "Portal Web EPS Sanitas / App Móvil",
        "consejo_radicacion": "Radica por el portal web oficial en la opción 'Radicar PQRS' o de forma presencial en tu punto de atención primaria, exigiendo copia con sello y número de radicado."
    },
    "Nueva EPS": {
        "nombre_completo": "Nueva EPS S.A.",
        "portal_pqrs": "https://www.nuevaeps.com.co/canales-atencion/pqrd",
        "telefono_nacional": "01 8000 954 400 (Contributivo) / 01 8000 952 000 (Subsidiado)",
        "telefono_bogota": "(601) 307 7022",
        "canal_virtual": "Portal Transaccional Nueva EPS / Oficina Virtual",
        "consejo_radicacion": "Ingresa al portal de PQRD de Nueva EPS con tu usuario o radica por escrito en la Oficina de Atención al Afiliado más cercana."
    },
    "Sura EPS": {
        "nombre_completo": "EPS y Medicina Prepagada Suramericana S.A.",
        "portal_pqrs": "https://www.epssura.com/servicios-en-linea/pqrs",
        "telefono_nacional": "01 8000 519 519",
        "telefono_bogota": "(601) 489 7941",
        "canal_virtual": "Servicios en Línea EPS Sura / App Seguros SURA",
        "consejo_radicacion": "Radica a través de la sección 'Radicar Solicitudes y Reclamos' en www.epssura.com o por su línea de atención telefónica."
    },
    "Salud Total EPS": {
        "nombre_completo": "Salud Total Entidad Promotora de Salud del Régimen Contributivo S.A.",
        "portal_pqrs": "https://saludtotal.com.co/peticiones-quejas-y-reclamos/",
        "telefono_nacional": "01 8000 1 14524",
        "telefono_bogota": "(601) 485 4555",
        "canal_virtual": "Punto de Atención al Usuario (PAU) Virtual",
        "consejo_radicacion": "Utiliza el formulario PQRD en la página oficial de Salud Total para obtener un número de radicado virtual inmediato con seguimiento en línea."
    },
    "Famisanar EPS": {
        "nombre_completo": "EPS Famisanar SAS",
        "portal_pqrs": "https://www.famisanar.com.co/canales-de-atencion/pqrd/",
        "telefono_nacional": "01 8000 116 662 (Contributivo) / 01 8000 914 202 (Subsidiado)",
        "telefono_bogota": "(601) 307 8069",
        "canal_virtual": "Oficina Virtual Famisanar",
        "consejo_radicacion": "Radica por el formulario PQRD de Famisanar o presencialmente en los Centros de Atención al Usuario (CAU)."
    },
    "Compensar EPS": {
        "nombre_completo": "Compensar Entidad Promotora de Salud",
        "portal_pqrs": "https://www.compensar.com/salud/pqrs",
        "telefono_nacional": "01 8000 915 202",
        "telefono_bogota": "(601) 444 1234",
        "canal_virtual": "Portal Transaccional Compensar Salud",
        "consejo_radicacion": "Radica en el formulario digital de felicitaciones, quejas o reclamos en compensar.com/salud o en la sede de atención ambulatoria."
    },
    "Savia Salud EPS": {
        "nombre_completo": "Alianza Medellín Antioquia EPS S.A.S. - Savia Salud",
        "portal_pqrs": "https://www.saviasaludeps.com/servicios-en-linea/pqrd",
        "telefono_nacional": "01 8000 423 683",
        "telefono_bogota": "Línea Medellín: (604) 448 1747",
        "canal_virtual": "Página web oficial de Savia Salud",
        "consejo_radicacion": "Radica a través del formulario PQRD en www.saviasaludeps.com o en los puntos de atención municipal de Antioquia."
    }
}

CANAL_SUPERSALUD = {
    "entidad": "Superintendencia Nacional de Salud (Supersalud)",
    "portal_pqrs": "https://www.supersalud.gov.co/es-co/Paginas/Protecci%C3%B3n%20al%20Usuario/atencion-al-ciudadano.html",
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
        "portal_pqrs": "https://www.supersalud.gov.co",
        "telefono_nacional": "Línea de atención de la entidad",
        "telefono_bogota": "Verificar en la página web oficial de la EPS",
        "canal_virtual": "Portal web de la entidad o ventanilla presencial",
        "consejo_radicacion": "Radica en la oficina de atención al usuario de la EPS o a través de su página web oficial exigiendo constancia de recibido."
    }
