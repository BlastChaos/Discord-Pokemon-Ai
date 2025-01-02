# What is it?

This is a bot for discord. His puropose is to create a real life pokedex entry based on the photos you provided

![Demo](demo.mp4)

# Getting Started

This project is built in python. **You** also need docker to test the application

1. Clone the repos
2. Rename **docker-compose.template.yml** to **docker-compose.yml** and change these environnemnts variables
   - DISCORD_TOKEN: Your discord token. You need this to use this bot in discord. For more info about how to create a discord token, you can see [this article.](https://www.writebots.com/discord-bot-token/).
   - GOOGLE_API_KEY: Your google gemini api key. You need this to generate the entry based on your photo. For more info about how to create a gemini api key, you can see [this article.](https://ai.google.dev/gemini-api/docs/api-key#windows)
