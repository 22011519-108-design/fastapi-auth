from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

from app.core.config import DATABASE_URL
from app.core.database import Base

# Import models so Alembic can detect tables
from app.modules.chat import models
from app.modules.auth import models as auth_models


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic will use this metadata to detect database tables
target_metadata = Base.metadata


def run_migrations_offline() -> None:

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()