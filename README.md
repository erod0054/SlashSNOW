# slashsnow

Use Slack to open a ticket in Service-Now.

The slash commands available in Slack allow Slack to post a payload to a designated URL, this Flask application listens for an incoming POST from Slack and parses the Slack user ID into the Service-Now user name (SSO).  It then posts a mostly boiler-plated payload to the Service-Now incident import table, and returns an incident ID and link to Slack.

Included with the response is an advisory to go update the urgency and provide aplifying information at the link provided, so hopefully we don't get "computer broken" too many times.

Currently running this with gunicorn behind nginx, as Slack requires a proper SSL connection.  The authenticity token generated when building your Slack Slash command must be added to the app route to prevent calls not originating from your integration from being processed.

The /test URL will return the form values of the payload sent to Slack using the `/snowtest` command in Slack.
