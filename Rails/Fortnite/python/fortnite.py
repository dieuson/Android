# COPYRIGHT Simon GAUDIN
# 05/04/2018
# All rights reserved
# Calice

import json
import string
import sys

NO_TEAM = -1
SOLO = 0
DUO = 1
SQUAD = 2

TRUE = 0
FALSE = 1

PSEUDO_CHARS = set(string.ascii_letters + string.digits + '-_')

FINAL_LIST = ""

def getType(message):
	type = NO_TEAM

	if message is not None and len(message) > 0:
		if message[0].lower().find("solo") != -1:
			type = SOLO
		elif message[0].lower().find("duo") != -1:
			type = DUO
		elif message[0].lower().find("squad") != -1:
			type = SQUAD
		else:
			type = NO_TEAM
	return type


def validFormat(message):
	i = 0
	for m in message:
		if m == '':
			message.pop(i)
		i += 1

	type = getType(message)

	if type == SOLO:
		return True if len(message) == 2 else False
	elif type == DUO:
		return True if len(message) == 4 else False
	elif type == SQUAD:
		return True if len(message) >= 4 and len(message) <= 6 else False

def checkPseudoValidity(pseudo):
	if ":" in pseudo:
		pseudo = pseudo.split(':')[1]
		if pseudo is not None and len(pseudo) > 0 and pseudo[0] == ' ':
			pseudo = pseudo[1:]
	pseudo = pseudo.strip()
	if len(pseudo) < 3 or len(pseudo) > 16:
		return FALSE, pseudo
	if any((c in PSEUDO_CHARS) for c in pseudo):
		return TRUE, pseudo
	else:
		return FALSE, pseudo

def soloPseudo(message):
	ret, newP1 = checkPseudoValidity(message[1])
	if ret == TRUE:
		return TRUE, newP1
	else:
		return FALSE, newP1

def duoPseudo(message):
	ret1, newP1 = checkPseudoValidity(message[2])
	ret2, newP2 = checkPseudoValidity(message[3])
	if ret1 == TRUE and ret2 == TRUE:
		return TRUE, newP1, newP2
	else:
		return FALSE, newP1, newP2

def squadThreePseudo(message):
	ret1, newP1 = checkPseudoValidity(message[2])
	ret2, newP2 = checkPseudoValidity(message[3])
	ret3, newP3 = checkPseudoValidity(message[4])
	if ret1 == TRUE and ret2 == TRUE and ret3 == TRUE:
		return TRUE, newP1, newP2, newP3
	else:
		return FALSE, newP1, newP2, newP3

def squadFourPseudo(message):
	ret1, newP1 = checkPseudoValidity(message[2])
	ret2, newP2 = checkPseudoValidity(message[3])
	ret3, newP3 = checkPseudoValidity(message[4])
	ret4, newP4 = checkPseudoValidity(message[5])
	if ret1 == TRUE and ret2 == TRUE and ret3 == TRUE and ret4 == TRUE:
		return TRUE, newP1, newP2, newP3, newP4
	else:
		return FALSE, newP1, newP2, newP3, newP4

def loopParse(jsonObj):
	global FINAL_LIST
	nb_part = 0
	i = 0
	for p in jsonObj:
		if p['message'] is not None:
			message = p['message'].rsplit('\n')

			if validFormat(message) == False:
				jsonObj.pop(i)
			else:
				type = getType(message)
				if type == SOLO:
					ret, newP1 = soloPseudo(message)
					if ret == TRUE:
						FINAL_LIST += ("SOLO\n\n" + newP1 + "\n*******************************************************\n")
						nb_part += 1
				elif type == DUO:
					ret, newP1, newP2 = duoPseudo(message)
					if ret == TRUE:
						FINAL_LIST += ("DUO\n" + message[1] + "\n\n" + newP1 + "\n" + newP2 + "\n*******************************************************\n")
						nb_part += 1
				elif type == SQUAD and len(message) == 5:
				 	ret, newP1, newP2, newP3 = squadThreePseudo(message)
				 	if ret == TRUE:
					 	FINAL_LIST += ("SQUAD\n" + message[1] + "\n\n" + newP1 + "\n" + newP2 + "\n" + newP3 + "\n*******************************************************\n")
					 	nb_part += 1
				elif type == SQUAD and len(message) == 6:
					ret, newP1, newP2, newP3, newP4 = squadFourPseudo(message)
					if ret == TRUE:
						FINAL_LIST += ("SQUAD\n" + message[1] + "\n\n" + newP1 + "\n" + newP2 + "\n" + newP3 + "\n" + newP4 + "\n*******************************************************\n")
						nb_part += 1

		i += 1

	print("\n\n\n FINAL_LIST \n\n")
	print(FINAL_LIST)
	print("\nNombre de participants : " + str(nb_part))


def main():
	if len(sys.argv) != 2:
		print("Error\nFile not found")
		return
	fileName = str(sys.argv[1])
	file = open(fileName, "r")
	jsonRead = file.read()
	jsonObj = json.loads(jsonRead)

	loopParse(jsonObj)


main()