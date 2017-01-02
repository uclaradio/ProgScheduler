# ProgScheduler

Processes our dj's submitted entries to programming department's quarterly show application to create a preliminary schedule.

Usage: `python3 schedule.py Show_Apps_Wave_2.csv`

### File Format

Expects an input `.csv` with the following field names: (which could be generated by a google form)

```
"Timestamp", "Name", "Email", "#1 Preference", "#2 Preference", "#3 Preference", "#4 Preference", "#5 Preference", "#6 Preference", "#7 Preference", "#8 Preference", "#9 Preference", "#10 Preference"
```

And produces an output `Schedule.csv` listing dj requests, with the following field names: (which could be used to create a google docs sheet)

```
"Start Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
```
