#!/bin/python
FILENAME = 'player.txt'
list = []
class Player:
	def __init__(self,account,level):
		self.account = account
		self.level =level

def takeSecond(Player):
    return Player.level


def main():
	File = open(FILENAME,'r')
	for line in File:
		linesize = len(line)
		account = line[8:17]
		level = int(line[24:linesize])
		player = Player(account,level)
		list.append(player)
		
	list.sort(key=lambda Player: Player.level)
	for line in list:
		print line.account ,line.level
		print '-------'

if __name__ == "__main__":
	main()
