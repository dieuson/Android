# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-06-04 19:39:51
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-04 20:51:50

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

def process(part_type, text):
	part_type_names = ["name", "date", "duration", "rank", "eliminations"]
	if (part_type in part_type_names[0]):
		return text

	elif(part_type in part_type_names[1]):
		return post_processing_date(text)

	elif(part_type in part_type_names[2]):
		return post_processing_duration(text)

	elif(part_type in part_type_names[3]):
		return post_processing_rank(text)

	elif(part_type in part_type_names[4]):
		return post_processing_eliminations(text)



