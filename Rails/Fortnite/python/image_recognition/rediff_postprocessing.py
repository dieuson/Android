# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-06-04 19:39:51
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-04 20:36:57

import json
import csv
from numpy import loadtxt

def post_process_slash(date):
	date = date.replace(" ", "").replace("201B", "2018")
	date = date.split("/")
	format_date = "{}/{}/{}".format(date[0], date[1], date[2][0:4])
	datetime = date[2][4:len(date[2])]
	hour = datetime[0:2]
	minutes = datetime[(len(datetime) - 2):len(datetime)]
	new_datetime = "{}:{}".format(hour, minutes)
	new_date = "{} {}".format(format_date, new_datetime)
	return new_date

def post_process_dash(date):
	date = date.replace("—", "-")
	date = date.split("-")
	format_date = "{}-{}-{}".format(date[0], date[1], date[2][:2])
	datetime = date[2][2:len(date[2])]
	hour = datetime[0:2]
	minutes = datetime[(len(datetime) - 2):len(datetime)]
	new_datetime = "{}:{}".format(hour, minutes).replace("-", "")
	new_date = "{} {}".format(format_date, new_datetime)
	return new_date

def post_processing_date(date):
	date = date.replace(" ", "").replace(";", ":")
	new_date = None

	if ("/" in date):
		new_date = post_process_slash(date)
	elif("-" in date):
		new_date = post_process_dash(date)
	return new_date

def post_processing_rank(rank):
	new_rank = rank.replace("O", "0").replace(" ", "")
	return(new_rank)

def post_processing_eliminations(eliminations):
	new_eliminations = eliminations.replace("O", "0").replace("D", "0").replace(" ", "").replace(":", "8")
	return(new_eliminations)

def post_processing_duration(duration):
	duration = duration.replace(" ", "")
	if (len(duration) == 4):
		duration = "0" + duration
	hour = duration[0:2]
	minutes = duration[(len(duration) - 2):len(duration)]
	new_duration = "{}:{}".format(hour, minutes)
	return new_duration

def compare_algo_results():
	filename = "algo analyse screenshots - sample.csv"
	# results = None
	name_valid = 0
	name_invalid = 0

	date_valid = 0
	date_invalid = 0

	duration_valid = 0
	duration_invalid = 0

	rank_valid = 0
	rank_invalid = 0

	eliminations_valid = 0
	eliminations_invalid = 0

	with open(filename) as csvfile:
		results = csv.DictReader(csvfile)
		for result in results:
			if (result['name'] != result['expected_name']):
				name_invalid += 1
			else:
				name_valid += 1

			if (result['name'] != result['expected_name']):
				name_invalid += 1
			else:
				name_valid += 1

			tmp = post_processing_date(result['date'])
			if (tmp):
				result['date'] = tmp
			if (result['date'] != result['expected_date']):
				date_invalid += 1
			else:
				date_valid += 1

			tmp = post_processing_duration(result['duration'])
			if (tmp):
				result['duration'] = tmp
			if (result['duration'] != result['expected_duration']):
				duration_invalid += 1
			else:
				duration_valid += 1

			tmp = post_processing_rank(result['rank'])
			if (tmp):
				result['rank'] = tmp
			if (result['rank'] != result['expected_rank']):
				rank_invalid += 1
			else:
				rank_valid += 1

			tmp = post_processing_eliminations(result['eliminations'])
			if (tmp):
				result['eliminations'] = tmp
			if (result['eliminations'] != result['expected_eliminations']):
				eliminations_invalid += 1
			else:
				eliminations_valid += 1

	name_ratio = round(((name_valid / (name_invalid + name_valid)) * 100), 2)
	date_ratio = round(((date_valid / (date_invalid + date_valid)) * 100), 2)
	duration_ratio = round(((duration_valid / (duration_invalid + duration_valid)) * 100), 2)
	rank_ratio = round(((rank_valid / (rank_invalid + rank_valid)) * 100), 2)
	eliminations_ratio = round(((eliminations_valid / (eliminations_invalid + eliminations_valid)) * 100), 2)

	print("Name: {}".format(name_ratio))
	print("Date: {}".format(date_ratio))
	print("Duration: {}".format(duration_ratio))
	print("Rank: {}".format(rank_ratio))
	print("Eliminations: {}".format(eliminations_ratio))


compare_algo_results()