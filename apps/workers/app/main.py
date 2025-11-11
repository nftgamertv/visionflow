from arq import create_pool
from arq.connections import RedisSettings
from .core.config import get_settings
from .tasks.augmentation import generate_version_task, export_dataset_task

settings = get_settings()


async def startup(ctx):
    """Startup hook for ARQ worker."""
    print("ARQ Worker starting...")


async def shutdown(ctx):
    """Shutdown hook for ARQ worker."""
    print("ARQ Worker shutting down...")


class WorkerSettings:
    """
    ARQ worker settings.
    This configures the async task queue for long-running jobs.
    """

    functions = [generate_version_task, export_dataset_task]

    redis_settings = RedisSettings.from_dsn(settings.redis_url)

    on_startup = startup
    on_shutdown = shutdown

    # Worker configuration
    max_jobs = 10
    job_timeout = 3600  # 1 hour
    keep_result = 3600  # Keep results for 1 hour
