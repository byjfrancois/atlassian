from atlassian import Jira
from webhook.globals import JIRA_URL
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("ATLASSIAN_TOKEN","")


jira=Jira(
url = JIRA_URL,
token = password
)

