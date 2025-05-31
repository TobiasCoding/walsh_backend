🛡️ Medidas de seguridad que se pueden agregar
Escaneo antivirus (opcional, vía ClamAV sidecar)

Detecta malware en archivos binarios.

Puede montarse como contenedor auxiliar o usarse vía subprocess.

Verificación MIME y contenido real

Validar que un .pdf sea realmente PDF y no un .exe renombrado.

Puede hacerse con magic o python-magic.

Lista blanca de extensiones permitidas

Rechazar tipos peligrosos (ej.: .exe, .sh, .bat, .js).

Firmado opcional o checksum desde el cliente

Comparar hash SHA-256 con uno provisto para validar integridad.

Protección de rutas públicas (firma o token)

Si file_service expone archivos públicamente, se puede exigir una firma temporaria para acceder a GET /files/{key}.

