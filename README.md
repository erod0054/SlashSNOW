# slashsnow

Use Slack to open a ticket in Service-Now.

The slash commands available in Slack allow Slack to post a payload to a designated URL, this Flask application listens for an incoming POST from Slack and parses the Slack user ID into the Service-Now user name (SSO).  It then posts a mostly boiler-plated payload to the Service-Now incident import table, and returns an incident ID and link to Slack.

To use it in a Slack channel, just type `/ticket my computer is broken`.  Actually, don't do that, because that drops it in the Racker Experience queue as I bogarted that slash command in Slack.  Type `/asops my computer is broken` and it will go bother Raj.

This code is intended to be taken and personalized to use your team's queue and service account information, as well as your own defined slash command in Slack.  It can be run on any server accessible to Slack.  

Included with the response is an advisory to go update the urgency and provide amplifying information at the link provided, so hopefully we don't get "my computer is broken" too many times.  I'm working on a check in Service-Now that will return a link to any existing incident already opened for the short description, currently only logging the INC number, user, and description to cut down on static.

Currently running this with gunicorn behind nginx, as Slack requires a proper SSL connection.  The authenticity token generated when building your Slack Slash command must be added to the app route to prevent calls not originating from your integration from being processed.

The /test URL will return the form values of the payload sent to Slack using the `/snowtest` command in Slack.
