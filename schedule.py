#!/usr/bin/env python

import csv
import re
import sys

if len(sys.argv) < 2:
	print("usage: py schedule.py [input file name]")
	exit(1)

inputFilename = sys.argv[1]

def buildScheduleCSV(inputFilepath, outputFilepath):
	schedule = {}
	csvFieldNames = ["Start Time", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
	scheduleDays = [day.lower() for day in csvFieldNames[1:]]
	for day in scheduleDays:
		schedule[day] = {}
	# print(schedule)

	# Input file
	with open(inputFilepath) as csvfile:
		reader = csv.DictReader(csvfile)

		timepattern = re.compile('[0-9][0-9]?')
		daypattern = re.compile('[a-z]+')

		# process app entries
		for row in reader:
			name = row["Name"]
			email = row["Email"]
			requests = []

			# "#1 Preference"
			for i in range(1, 11):
				requestIndex = "#%d Preference" % i
				if requestIndex not in row:
					continue

				request = row[requestIndex].lower().strip()
				if request in requests:
					# skip duplicate requests
					continue
				else:
					requests.append(request)

				times = timepattern.findall(request)
				days = daypattern.findall(request)
				if len(times) < 1 or len(days) < 1:
					print("skipping invalid entry")
					print("-> \"%s #%d: %s\"" % (name, i, request))
					continue

				time = int(times[0]) % 12
				day = days[0]
				if "pm" in request:
					time += 12

				# print("processed", "#%d" % i, name, request, " => ", day, time)
				if day in schedule:
					if time not in schedule[day]:
						schedule[day][time] = []
					schedule[day][time].append((i, name))

	# print(schedule)

	# Output file
	with open(outputFilepath, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csvFieldNames)
		writer.writeheader()

		minHour = min(min(schedule[day]) for day in scheduleDays)
		maxHour = max(max(schedule[day]) for day in scheduleDays)
		for time in range(minHour, maxHour + 1):
			humanTime = "%d%s" % ((12 if (time % 12) == 0 else (time % 12)), "am" if time < 12 else "pm")
			fields = {csvFieldNames[0]: humanTime}

			for day in csvFieldNames[1:]:
				if time in schedule[day.lower()]:
					# format people who want this spot
					peeps = schedule[day.lower()][time]
					# sort people by first element in tuple: their preference #
					peeps.sort(key=lambda tup: tup[0])
					people = "\n".join("#%d: %s" % peep for peep in peeps)
					fields[day] = people
				else:
					# nobody wants this spot
					fields[day] = ""

			writer.writerow(fields)

	print("")
	print("Finished.")


buildScheduleCSV(inputFilename, "Schedule.csv")
