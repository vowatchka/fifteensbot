#!/usr/bin/env python

"""
Do it.
"""

# define metadata
__version__   = "1.0.0"
__author__    = "Vladimir Saltykov"
__copyright__ = "Copyright 2019, %s" % __author__
__email__     = "vowatchka@mail.ru"
__license__   = "MIT"
__date__      = "2019-08-05"

# import packages and modules
import telebot
import os
import time
from random import randint
from copy import deepcopy
	
def mixchips():
	chips = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,None]
	mixedchips = []
	gamefield = []
	
	# mix chips
	while len(chips):
		mixedchips.append(
			chips.pop(randint(0, len(chips)-1))
		)
		
	# fill game field
	gamefield.append(mixedchips[0:4])
	gamefield.append(mixedchips[4:8])
	gamefield.append(mixedchips[8:12])
	gamefield.append(mixedchips[12:16])
	return gamefield

def chiprowcol(chip, gamefield):
	for idx,fieldrow in enumerate(gamefield):
		if chip in fieldrow:
			return idx, fieldrow.index(chip)
	return -1, -1
	
def cantomovechip(torow, tocol, gamefield):
	if torow >= 0 and torow <= 3 and tocol >= 0 and tocol <= 3 and gamefield[torow][tocol] == None:
		return True
	else:
		return False
	
def movechip(fromrow, fromcol, torow, tocol, gamefield):
	updatedfield = deepcopy(gamefield)
	updatedfield[torow][tocol] = updatedfield[fromrow][fromcol]
	updatedfield[fromrow][fromcol] = None
	return updatedfield
	
def trytomovechip(row, col, gamefield):
	newrow, newcol = row+1, col
	if not cantomovechip(newrow, newcol, gamefield):
		newrow, newcol = row-1, col
		if not cantomovechip(newrow, newcol, gamefield):
			newrow, newcol = row, col+1
			if not cantomovechip(newrow, newcol, gamefield):
				newrow, newcol = row, col-1
				if not cantomovechip(newrow, newcol, gamefield):
					newrow, newcol = row, col
	
	if newrow == row and newcol == col:
		# not move chip
		return gamefield
	else:
		# move chip
		return movechip(row, col, newrow, newcol, gamefield)
		
def showgamefield(gamefield):
	# create keyboard
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
	
	# create keyboard buttons
	for idx,fieldrow in enumerate(gamefield):
		rowbuttons = list(map(lambda chip : telebot.types.KeyboardButton(text=str(chip) if chip != None else ""), fieldrow))
		keyboard.add(*rowbuttons)
		
	return keyboard
	
def main():
	# get token
	TG_TOKEN = os.environ["TOKEN"]
	# bot
	fifteensbot = telebot.TeleBot(TG_TOKEN)
	# game field
	gamefield = []
	
	@fifteensbot.message_handler(commands=["start"])
	def start(message):
		nonlocal gamefield
		gamefield = mixchips()
		fifteensbot.send_message(message.from_user.id, "Let's start!", reply_markup=showgamefield(gamefield))
		fifteensbot.send_message(message.from_user.id, "Select and move chip please...")
	
	@fifteensbot.message_handler(content_types=["text"])
	def getuserchip(message):
		nonlocal gamefield
		try:
			chip = int(message.text)
		except:
			fifteensbot.send_message(message.from_user.id, "Select and move chip please...", reply_markup=showgamefield(gamefield))
		else:
			chiprow, chipcol = chiprowcol(chip, gamefield)
			gamefield = trytomovechip(chiprow, chipcol, gamefield)
			fifteensbot.send_message(message.from_user.id, "You move chip \"%d\"" % chip, reply_markup=showgamefield(gamefield))
	
	try:
		fifteensbot.polling(none_stop=True, interval=1)
	except Exception as ex:
		time.sleep(5)
		print("Internet error!")
		print(ex)

if __name__ == "__main__":
	main()