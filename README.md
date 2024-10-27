# prs_scheduler_bot

This repository provides a discord bot that uses [prs_scheduler_api](https://github.com/jmusone/prs_scheduler_api). It contains near-similar functionality, outlined in the commands listed below.

This github repository does not include the .env file, which holds global variables including the very secret DISCORD_TOKEN. The .env file also includes the endpoints for the prs_scheduler_api, but those can be found in it's own repository (listed above).

## Commands:
### League Commands:
- $teams: Returns all teams
- $add: Adds a new team
```
$add https://pittsburghsportsleague.leaguetab.com/team/<team_id>/<team_name>
```
- $teaminfo: Retrieves all information for a team based on the given id
```
$teaminfo <team_id>
```
- $edit: Edit a previously added team [REDACTED]
```
$edit <team_id> <league> <location> <sport> <team_name>
```
Note: The <team_id> in $teaminfo and $edit (as well as the <team_name> in the edit command) are different from the parameters of the same name outlined in the PSL URL in the $add command. Use $teams to get the correct id for the other bot commands, as the <team_id> in the PSL URL is only used by PSL, not by this discord bot.

### Games Commands:
- $games: Returns games for a given team
```
$games <league_id>
```
- $nextgame: Returns the next game for a given team
```
$nextgame <league_id>
```
- $gamein: Returns all games in the given amount of days
```
$gamein <days>
```
