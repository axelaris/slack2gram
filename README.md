# Slack2gram

Slack2gram is an application to forward chat messages from Slack to Telegram channels. Is supports message routing, so one single bot could be used to do forwarding for many channels. Slack2gram was developed for those, who using Slack as a primary corporate or team communication solution, but does not want to have Slack installed on their mobile devices. Using Slack2gram they can recieve Slack chat messages in Telegram channels.

# How to prepare

## Slack bot

- [Create a new app](https://api.slack.com/apps/new)
- Use "**From an app manifest**" feature and [example manifest](manifest.yml)
- Click "**Install to Workspace**"
- On **Basic Information** blade, scroll down to **App-Level Tokens** section and click on **Generate Tokens and Scopes**
- Type any Token Name and select "**connections:write**" scope
- Click "**Generate**" and write down **xapp** token
- Go to "**OAuth & Permissions**" blade, and write down **xoxb** token
- Go to "**Install App**" blade and click "**Reinstall to Workspace**"
- Open Slack application and invite the Bot user to every channel where you want to make forward from. The Bot will unable to forward messages from any channels where it's not a member.

## Telegram bot

- Open Telegram, find **@BotFather**, type `/start`
- Type `/newbot` to create a bot and follow instructions
- Write down API key
- Open Telegram application and add the Bot user to every channel where you want to make forward to. The Bot will unable to forward messages to any channels where it's not a member. While adding bot, you can only select a **Post Messages** permission.

## Routing rules

Create a file `routing.conf` with message routing rules in following form:
```
<slack channel name #1>: <telegram channel id #1>
<slack channel name #2>: <telegram channel id #2>
```
To find an Id for telegram channel open in browser the following URL: `https://api.telegram.org/bot<api_token>/getUpdates`. If you can't see the channel you are looking for - just send a new message there.

# How to run

## From source code

- Create and activate a new Python virtual env:
```
python3 -m venv .venv
source .venv/bin/activate
```

- Export following environment variables:

  ```
  export SLACK_BOT_TOKEN=<xoxb-...>
  export SLACK_APP_TOKEN=<xapp-...>
  export TG_BOT_TOKEN=<0123456789:AA..>
  ```

- Install Python dependencies: `pip install -r requirements.txt`

- Run the code: `python3 main.py`

## Using docker image

- Export following environment variables:
```
  export SLACK_BOT_TOKEN=<xoxb-...>
  export SLACK_APP_TOKEN=<xapp-...>
  export TG_BOT_TOKEN=<0123456789:AA..>
```
- Run the docker container:
```
docker run -d -v $(pwd)/routing.conf:/app/routing.conf -e SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} -e SLACK_APP_TOKEN=${SLACK_APP_TOKEN} -e TG_BOT_TOKEN=${TG_BOT_TOKEN} slack2gram:latest
```