# Wizards Bot
*A Discord Bot for the McTyeire wizgang Discord server*

### Current Feature Set
* **Birthday** - Allows users to set their birthday and receive a birthday message on their birthday.
* **Ping** - Allows users to ping the bot and receive the bot's latency in milliseconds.

### Changelog
* **0.2.0** (*16MAY 6:30am*)
  * Added **help** command
  * Added **about** command
  * Storing Changelog in `storage/changelog.json` to avoid updating every file every time we update the version
  * Built *update_log.py*, which updates the changelog with the new version and date.  **Use: `python3 update_log.py 0.3.0 2023-05-16`**.
* **0.1.0** (*16MAY 5:45am*)
  * Initial Commit to GitHub
  * This commit contains the shell of the bot, plus working **birthday** and **ping** commands. 
  * Unlike previous editions, this bot has been abstracted into Cogs rather than maintaining all the code in a single file.  Hopefully, this helps us to debug easier and maintain solid readability.