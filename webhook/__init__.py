import json
from webhook.globals import __service__,__version__
import webhook.integrations.jira
from fastapi import FastAPI, Request


API = FastAPI(docs_url=None, redoc_url=None, default_response_class=HTMLResponse)