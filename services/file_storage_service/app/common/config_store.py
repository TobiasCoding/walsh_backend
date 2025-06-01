# services/file_storage_service/app/common/config_store.py

class Config:
    """
    Objeto vacío al que iremos añadiendo atributos
    según el payload que publique el Admin Panel.
    """

    pass


# Instancia global que usaremos en todo el servicio
settings = Config()
