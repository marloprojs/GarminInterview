from resource import *
import sys

token = getToken()
userIds = listUserIds(token)

def displayMenu():
	print("Menu")
	print("1. Get 10 users with card and device info (press 1 and then Enter)")
	print("2. Get a specific user's card and device info (press 2 and then Enter)")
	print("3. Quit (press Enter)")

loop = True
while(loop):
	displayMenu()
	userInput = input("Enter option: ")
	user = ""

	if(userInput=="1"):
		filterCC = input("If you would like to filter the credit cards by state enter a desired state (ERROR or ACTIVE), else press Enter: ")
		filterD = input("If you would like to filter the devices by state enter a desired state (INITIALIZED OR FAILED_INITIALIZATION), else press Enter: ")

		for i in range(len(userIds)):
			makeJsonObjects(token, userIds[i], filterCC, filterD)
	elif(userInput=="2"):
		userId = input("Enter a user id: ")
		filterCC = input("If you would like to filter the credit cards by state enter a desired state (ERROR or ACTIVE), else press Enter: ")
		filterD = input("If you would like to filter the devices by state enter a desired state (INITIALIZED OR FAILED_INITIALIZATION), else press Enter: ")
		makeJsonObjects(token, userId, filterCC, filterD)
	else:
		loop = False
