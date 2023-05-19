# Wizards Bot
*A Discord Bot for the McTyeire wizgang Discord server*

### Current Feature Set
* **About** - Displays the about page for the bot
* **Birthday** - Allows users to set their birthday and receive a birthday message on their birthday.
* **Help** - Displays the help page for the bot with command descriptions
* **Ping** - Allows users to ping the bot and receive the bot's latency in milliseconds.
* **Snipe** - Allows users to snipe messages that have been deleted.

### Changelog
* **0.3.0** (*19MAY 4:00pm*)
  * Built counting bot functionality! Use `/register_counter` to register the counter to a specified channel.  Messages in other channels will not be interpreted for the count.
  * Modified `/register_birthday` to warn users of registering multiple birthdays.  A `/forget_birthday` command was added to allow someone to forget their birthday. *A future implementation might do better at combining these, but I want to add more features before improving on current ones.*
* **0.3.0** (*17MAY 5:00pm*)
  * Added **snipe** command
* **0.2.0** (*16MAY 6:30am*)
  * Added **help** command
  * Added **about** command
  * Storing Changelog in `storage/changelog.json` to avoid updating every file every time we update the version
  * Built *update_log.py*, which updates the changelog with the new version and date.  **Use: `python3 update_log.py 0.3.0 2023-05-16`**.
* **0.1.0** (*16MAY 5:45am*)
  * Initial Commit to GitHub
  * This commit contains the shell of the bot, plus working **birthday** and **ping** commands. 
  * Unlike previous editions, this bot has been abstracted into Cogs rather than maintaining all the code in a single file.  Hopefully, this helps us to debug easier and maintain solid readability.