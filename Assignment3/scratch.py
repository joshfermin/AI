def DeleteIllegalMoves(self):
		for key in i_move:
			moveKey = (key[0], None)
		# DELETING INVALID MOVES
		if moveKey == ('BOT RIGHT', None):
			DeleteRightCol()
			DeleteBotRows()
			DeleteBotRight()
		if moveKey == ('BOT LEFT', None):
			DeleteLeftCol()
			DeleteBotRows()
			DeleteBotLeft()
		if moveKey == ('TOP RIGHT', None):
			DeleteRightCol()
			DeleteTopRows()
			DeleteTopRight()
		if moveKey == ('TOP LEFT', None):
			DeleteLeftCol()
			DeleteTopRows()
			DeleteTopLeft()
		for i in range((i_totalDistrict / 2), i_totalDistrict):
			if moveKey == ('BOT ROW ' + str(i), None):
				DeleteSpecificDistrict('BOT ROW ' + str(i))
				DeleteLeftCol()
				DeleteRightCol()
				DeleteBotLeft()
				DeleteBotRight()
			if moveKey == ('RIGHT COL ' + str(i), None):
				DeleteSpecificDistrict('RIGHT COL ' + str(i))
				DeleteTopRows()
				DeleteBotRows()
				DeleteTopRight()
				DeleteBotRight()
		for i in range(0 , i_totalDistrict):
			if moveKey == ('TOP ROW ' + str(i), None):
				DeleteSpecificDistrict('TOP ROW ' + str(i))
				DeleteLeftCol()
				DeleteRightCol()
				DeleteTopRight()
				DeleteTopLeft()
			if moveKey == ('LEFT COL ' + str(i), None):
				DeleteSpecificDistrict('LEFT COL ' + str(i))
				DeleteTopRows()
				DeleteBotRows()
				DeleteTopLeft()
				DeleteBotLeft()
		newMoveDictionary = i_movesRemaining
		return newMoveDictionary

def DeleteSpecificDistrict(self, key):
		deleteKey = list(PartialMatch((key, None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

	def DeleteBotRows(self):
		for i in range((i_totalDistrict / 2), i_totalDistrict):
			deleteKey = list(PartialMatch(('BOT ROW ' + str(i), None), i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del i_movesRemaining[deleteKey]

	def DeleteTopRows(self):
		for i in range(0, (i_totalDistrict / 2)):
			deleteKey = list(PartialMatch(('TOP ROW ' + str(i), None), i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del i_movesRemaining[deleteKey]

	def DeleteLeftCol(self):
		for i in range(0, (i_totalDistrict / 2)):
			deleteKey = list(PartialMatch(('LEFT COL ' + str(i), None), i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del i_movesRemaining[deleteKey]

	def DeleteRightCol(self):
		for i in range((i_totalDistrict / 2), i_totalDistrict):
			deleteKey = list(PartialMatch(('RIGHT COL ' + str(i), None), i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del i_movesRemaining[deleteKey]

	def DeleteTopLeft(self):
		deleteKey = list(PartialMatch(('TOP LEFT', None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

	def DeleteTopRight(self):
		deleteKey = list(PartialMatch(('TOP RIGHT', None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

	def DeleteBotLeft(self):
		deleteKey = list(PartialMatch(('BOT LEFT', None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

	def DeleteBotRight(self):
		deleteKey = list(PartialMatch(('BOT RIGHT', None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]