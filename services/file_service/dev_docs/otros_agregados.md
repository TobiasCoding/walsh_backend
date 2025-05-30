Mejorar el esquema del evento Kafka file_stored: podría definir explícitamente el modelo FileStoredEvent también para serializar a JSON (hoy lo arma como un diccionario).
Agregar limitador de tamaño de archivo (MAX_UPLOAD_MB) en el middleware.


Mi recomendación pragmática:

### 1. Soporte S3/NFS

* **Código listo, pero backend local por defecto.**

  * Define desde el inicio una interfaz `StorageBackend` con dos métodos (`save_file`, `get_file`).
  * Implementá la versión **LocalFSBackend** ahora mismo.
  * Dejá stubs vacíos o un módulo `s3_backend.py` / `nfs_backend.py` con TODO-comments; así el patrón ya existe y la migración futura sólo será agregar la implementación y ajustar una variable de entorno (`STORAGE_BACKEND=s3`).
  * Ventaja: mantenés el servicio liviano y sin dependencias pesadas (boto3, fsspec) en la beta, pero la arquitectura ya contempla el intercambio de backend sin refactor.

### 2. Cliente de Kafka

* **Producción** → `confluent-kafka` (enlaza librdkafka en C).

  * \~10× más throughput que `kafka-python`, menor latencia y mejor compresión.
  * Mantenimiento activo por Confluent, preparación para features nuevos (idempotent producer, transactions).
* **Desarrollo local** → podés empezar también con `confluent-kafka`; hoy está en PyPI y la instalación vía wheels pre-compilados suele ser trivial en Ubuntu.

  * Si alguna vez el build se complica (p.ej. en Windows sin librdkafka), `kafka-python` sirve como fallback sin cambios de API mayores.

**En resumen:**

* Arrancá con backend local implementado, pero con interfaz pluggable y flag para futuro S3/NFS.
* Usa `confluent-kafka` como cliente principal; te ahorra dolores de rendimiento cuando escales y no agrega complejidad significativa durante el desarrollo.

