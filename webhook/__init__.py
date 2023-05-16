"""
jira specific routes
"""

from dataclasses import fields
import json
from anybadge import Badge
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from webhook.globals import __service__ , __version__ 
from webhook.integrations.jira import Event,User,Issue



API = FastAPI(docs_url=None, redoc_url=None, default_response_class=HTMLResponse)


@API.get("/")
async def api_root() -> str:
    """blank root so that our web server doesn't yell at us"""
    return ""


@API.get("/healthz")
async def api_healthz() -> str:
    """health check endpoint"""
    return ""


@API.get("/version", response_class=JSONResponse)
async def api_version() -> JSONResponse:
    """version endpoint"""
    return JSONResponse(content=dict(version=__version__, service=__service__))

@API.post("/jira/webhook")
async def api_jira_webhook(request: Request) -> str:
    data = await request.json()
    # json_object = json.dumps(data, indent=4)
    # with open("event.json","w") as outfile:
    #     outfile.write(json_object)
    event = Event(data)
    print(event.issue.software)
    print("got it")
    



