# prs_scheduler_bot

This repository provides a discord bot that uses [prs_scheduler_api](https://github.com/jmusone/prs_scheduler_api). It contains near-similar functionality, outlined in the commands listed below.

## Commands:
### League Commands:
- $leagues: Returns all leagues
- $add: Adds a new league
```
$add https://pittsburghsportsleague.leaguetab.com/team/<team_id>/<team_name>
```
- $edit: Edit a previously added league
```
$edit <league_id> <league> <location> <sport> <team name>
```
Note: The <league_id> in the edit command is the team's id in the database, but is separate from the <team_id> listed in the add command. It's called <league_id> because that's what it's called in the database, but you can add multiple teams from the same league with no repercussions. Bad naming on my part, sorry! 🙁

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
