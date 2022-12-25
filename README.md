# Kian_dailyBot
A robot for reporting users and managing reports
## How to run
To run Kian_dailyBot in development mode; Just use steps below:

1. Create new Slack app with the following steps:
    1. Open slack API console. (https://api.slack.com/).
    2. Click on “Your apps”.
    3. Click on “Create New App”.
    4. Click on “From scratch”.
    5. Now give your app name and select workspace then click on the “Create App” button.
    6. Click on the “App Home” button and click on “Review Scopes to Add”.
    7. After clicking on the “Review Scope to Add” button, scroll down and find the Scope section. Then click on the “Add an OAuth Scopes” Button and add `chat: write`, `channels:read`,`groups:read`, `im:write`, `users:read`
    8. Now click on “Install to Workspace” and press on “Allow” to generate an OAuth token.
2. Install `Docker`, `Docker-Compose` in your system.
3. Clone the project https://github.com/DataCoLabltd/Kian_dailyBot.git
4. update .env file based on the Slack tokens prepared in the previous steps
5. Make development environment ready using commands below;

  ```bash
  git clone https://github.com/DataCoLabltd/Kian_dailyBot.git && cd Kian_dailyBot/daily_bot/
  sudo docker-compose up --build
  sudo docker exec -it daily_bot_postgres_db_1 /bin/bash
        psql -U postgres
        CREATE USER daily_bot WITH SUPERUSER PASSWORD '1234';
        CREATE DATABASE daily_bot;
  sudo docker exec -it daily_bot_django_1 /bin/bash
        python manage.py createsuperuser
```
You can access the admin panel through the following address. In the management panel, you can see information about users, channels, etc., and also prepare reports for each user.

 http://localhost:8040/admin

Note that to use the bot, you must add it to the channel and direct message
