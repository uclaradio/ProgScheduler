#!/usr/bin/env python

import csv
import re

def buildScheduleCSV(inputFilepath, outputFilepath):
	schedule = {}
	csvFieldNames = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
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

			# "#1 Preference"
			for i in range(1, 11):
				requestIndex = "#%d Preference" % i
				if requestIndex not in row:
					continue

				request = row[requestIndex].lower().strip()
				times = timepattern.findall(request)
				days = daypattern.findall(request)
				if len(times) < 1 or len(days) < 1:
					print("error: skipping invalid entry")
					print("-> \"%s #%d: %s\"" % (name, i, request))
					continue

				time = int(times[0]) % 12
				day = days[0]
				if "pm" in request:
					time += 12

				# print("processed", name, request, " => ", day, time)
				if day in schedule:
					if time not in schedule[day]:
						schedule[day][time] = []
					schedule[day][time].append("#i: " + name)

	# print(schedule)

	# Output file
	with open(outputFilepath, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csvFieldNames)
		writer.writeheader()

		minHour = min(min(schedule[day]) for day in scheduleDays)
		maxHour = max(max(schedule[day]) for day in scheduleDays)
		for time in range(minHour, maxHour):
			fields = {"Time": time}

			for day in csvFieldNames[1:]:
				if time in schedule[day.lower()]:
					# format people who want this spot
					people = ",\n".join(str(peep) for peep in schedule[day.lower()][time])
					fields[day] = people
				else:
					# nobody wants this spot
					fields[day] = ""

			writer.writerow(fields)

	print("")
	print("Finished.")

buildScheduleCSV("Show Apps Wave 2.csv", "Schedule.csv")
