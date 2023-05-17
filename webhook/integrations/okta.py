from typing import Dict
from webhook.applications.okta_config import okta
from webhook.applications.atlassian import jira


class Okta_Event:
    """Okta webhook event class"""

    def __init__(self, data: Dict) -> None:
        """constructor"""
        self._data = data
        self.source = data["source"]
        self._realdata = self._data["data"]
        self._event = self._realdata["events"]
        self.event = self._event[0]
        self.uuid = self.event["uuid"]
        self.eventType = self.event["eventType"]
        self.displayMessage = self.event["displayMessage"]
        self.severity = self.event["severity"]
        self._actor = self.event["actor"]
        self.actorEmail = self._actor["alternateId"]
        self._outcome = self.event["outcome"]
        self.results = self._outcome["result"]
        self._target = self.event["target"]
        # need to figureout if we deactive more than on user at a time if so i might want ot create another class just to handle users  // Tested via okta you can deactive multi users and one json file is sent at a time
        self.target = self._target[0]
        self.userid = self.target["id"]
        self.email = self.target["alternateId"]
        self.displayName = self.target["displayName"]
        # self.eventTime = datetime.fromisoformat(self._realdata["eventTime"])

    def __repr__(self) -> str:
        """repl representation"""
        return f"<OktaEvent({self.email}):"

    # need to find a way to handle errors / confirm that there is a user with the same email id

    def deactiveUser(self):
        # try:
        #     if jira.is_active_user(self.email) is not False:
        jira.user_deactivate(self.email)
        # except urllib.request.HTTPError as err:
        #     print(err.code)

    def createJiraIssue(self) -> None:

        fields = {
            "project": {"key": "TEST"},
            "issuetype": {"name": "Task"},
            "summary": "{message} - {user}".format(
                user=self.email, message=self.displayMessage
            ),
        }
        jira.create_issue(fields)



async def main():
    users, resp, err = await okta.list_users()
    for user in users:
        print(user.profile.first_name, user.profile.last_name)

loop = asyncio.get_event_loop()
loop.run_untill_complelte(main())