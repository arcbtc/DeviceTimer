import asyncio
from typing import List

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_zoosats")

zoosats_ext: APIRouter = APIRouter(prefix="/zoosats", tags=["zoosats"])

scheduled_tasks: List[asyncio.Task] = []

zoosats_static_files = [
    {
        "path": "/zoosats/static",
        "app": StaticFiles(directory="lnbits/extensions/zoosats/static"),
        "name": "zoosats_static",
    }
]


def zoosats_renderer():
    return template_renderer(["lnbits/extensions/zoosats/templates"])


from .lnurl import *  # noqa: F401,F403
from .tasks import wait_for_paid_invoices
from .views import *  # noqa: F401,F403
from .views_api import *  # noqa: F401,F403


def zoosats_start():
    loop = asyncio.get_event_loop()
    task = loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
    scheduled_tasks.append(task)