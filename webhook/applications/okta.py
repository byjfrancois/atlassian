from atlassian import Jira
from webhook.globals import OKTA_URL
from dotenv import load_dotenv
import os


token = os.getenv("OKTA_TOKEN","")

config = {
    "orgUrl": OKTA_URL;
    "token": token
}

okta_client = OktaClient(config)