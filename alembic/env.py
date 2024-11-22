from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.schemas.models import Base  # Import the Base from models.py
from app.schemas.models import User  # Import the User model or any other models you have

# This will allow Alembic to reflect on your models for migrations
target_metadata = Base.metadata

# Reading the Alembic configuration
config = context.config

# Set up loggers if necessary (optional)
fileConfig(config.config_file_name)

def run_migrations_online():
    # Set up the database connection
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    # Connect to the database and run migrations
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        # Run the migrations in a transaction
        with context.begin_transaction():
            context.run_migrations()

# If you want to support offline migrations (when not connected to the database), you can use this method
def run_migrations_offline():
    # Generate a database URL for offline migrations
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Decide whether to run migrations online or offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
