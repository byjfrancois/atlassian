import asyncio
from dataclasses import Field, field
from datetime import datetime
from logging import raiseExceptions
from signal import pause
from tokenize import group
from webhook.applications.atlassian import Jira
import time
from typing import Dict, Optional



class User:
    """jira user class"""

    def __init__(self, data: Dict) -> None:
        """constructor"""
        self._user = data
        self.name = self._user["displayName"]
        # self.email = self._user["emailAddress"]
        self.display_name = self._user["displayName"]
        self.timezone = self._user["timeZone"]

    def __repr__(self) -> str:
        """repl representation"""
        return f"<JiraUser: [{self.name}]>"


class Issue:
    """jira issue class"""

    def _exists(self, key: str, data: Dict) -> bool:
        """return if the key is in the data and the value of that key is not falsey"""
        return (key in data) and bool(data[key])

    def _user(self, key: str, data: Dict) -> Optional[User]:
        """attempt to parse a user"""
        return User(data[key]) if self._exists(key, data) else None

    def __init__(self, data: Dict) -> None:
        """constructor"""
        self._issue = data
        self._id = self._issue["id"]
        self.id = self._issue["key"]
        self.api_url = self._issue["self"]

        self._fields = self._issue["fields"]
        self._sofware = self._fields["customfield_10034"]
        self.software = self._sofware["value"]
        self.reporter = self._user("reporter", self._fields)
        self.creator = self._user("creator", self._fields)
        self.assignee = self._user("assignee", self._fields)
        self._priority = self._fields["priority"]
        self.priority_level = self._priority["id"]
        self.priority = self._priority["name"]

        self.summary = self._fields["summary"]
        self.created_at = datetime.fromisoformat(self._fields["created"][:-5])
        self.updated_at = datetime.fromisoformat(self._fields["updated"][:-5])

        self._status = self._fields["status"]
        self.description = self._status["description"]

        self._status_category = self._status["statusCategory"]
        self.status_id = self._status_category["id"]
        self.status_key = self._status_category["key"]
        self.status = self._status_category["name"]


class Event:
    """jira webhook event class"""

    class Type:
        """event type enum"""

        CREATED = "issue_created"

    def __init__(self, data: Dict) -> None:
        """constructor"""
        self._data = data
        self._timestamp = self._data["timestamp"]
        self.timestamp = datetime.utcfromtimestamp(self._timestamp / 1000)
        self.issue = Issue(self._data["issue"])       
        self.event_type = self._data["issue_event_type_name"]
        self.user = User(self._data["user"])

    def __repr__(self) -> str:
        """repl representation"""
        return f"<JiraEvent({self.event_type}): [{self.issue.id}]> {self.timestamp}"

