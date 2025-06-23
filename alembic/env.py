import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# .env dosyalarını yüklemek için python-dotenv
from dotenv import load_dotenv
from app.core.config import settings
from app.db.base import Base  # tüm modellerinizin metadata'sı burada

# ENV_FILE ile hangi .env yüklenecek?
load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env.dev"))

# Alembic Config objesi
config = context.config

# Logging konfigürasyonu
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy URL’i Pydantic ayarlarından al ve Alembic'e söyle
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Autogenerate için metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline modda (DB bağlantısı olmadan) migration."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online modda (DB bağlantılı) migration."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # sütun tipi değişimlerini de takip eder
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
