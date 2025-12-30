#Without Celery: user clicks “Export”, request hangs 10 seconds → client waits → server can’t handle other requests efficiently.
#With Celery: the export job runs in the background, and the client immediately gets a “job accepted” response.

from celery import Celery

celery_app = Celery(
    "worker", #name of Celery app
    broker="redis://localhost:6379/0",      # Redis broker URL - stores tasks until workers pick them up
    backend="redis://localhost:6379/0",     # Redis result backend - where Celery stores the results of finished tasks
    include=["app.tasks.email_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True
)