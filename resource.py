#How the requirements are fulfilled

#Requirement: We need a new API resource that composes these 3 separate calls 
#into a single JSON structure so our API clients don't need to make 3 network calls anymore:
#	- This is fulfilled with the method makeJsonObjects. This method creates a json object for
#	a specified user that includes: userId, creditCardIds, deviceIds, and the states for the 
#	devices and credit cards.

#Please note this also takes care of the requirement for including the userId, creditCardIds, deviceIds, and the states for the 
#	devices and credit cards

#Please note: based on how the return json object is structured, we know that the state of creditCardIds[i] is
#			creditCardStates[i] (i is some integer) and the same concept applies to devices.

#Requirement: The devices and creditCards MUST support lists of 0-n values:
#			This is fulfilled by looping through the list of credit cards and devices when making the JSON object,
#			as I loop through the lists, the current index number is appended to the json key, i.e. creditCard0
#			or device5. If the user has two credit cards, they'll be listed as creditCard0 and creditCard1.

#Requirement: The API SHOULD support two optional filters: creditCardState, deviceState
#			The filter for the credit card state is fulfilled by the method addCreditCardsToJson. This
#			method only adds the credit cards if the state is equal to the filter (it's a case insensitive check).
#			The filter for the device state is fulfilled by the method addDevicesToJson. This method
#			only adds the devices if the state is equal to the filter (it's a case insensitive check).



import requests, json
requests.packages.urllib3.disable_warnings() 

#TODO: After getting logic working, make filters, optimize, say which methods satisfy which requirements

def invalidIdInput(resp):
	#Check to make sure it was a valid response
	if(resp.status_code == 400):
		print("400 - Bad Request")
	elif(resp.status_code == 401):
		print("401 - Unauthorized")
	elif(resp.status_code == 402):
		print("402 - Request Failed")
	elif(resp.status_code == 404):
		print("404 - Not Found")
	elif(resp.status_code == 500 or resp.status_code == 502 or resp.status_code == 503 or resp.status_code == 504):
		print("Server error")

#Generate a new access token
def getToken():
	params = (('grant_type', 'client_credentials'),)
	resp = requests.get('https://auth.qa.fitpay.ninja/oauth/token', params=params, verify=False, auth=('xyqxRLn7', 'WXyBxggE'))
	j = json.loads(resp.text)

	#Check to make sure it was a valid response
	if(resp.status_code == 200):
		return j['access_token']

	invalidIdInput(resp)
	return None

#Makes get request for credit card info for a user
def getCards(token, userId):
	headers = { "Authorization" : "Bearer "+token}
	resp = requests.get('https://api.qa.fitpay.ninja/users/'+ userId +'/creditCards', headers=headers, verify=False)

	#Check to make sure it was a valid response
	if(resp.status_code != 200):
		invalidIdInput(resp)
		return None

	j = json.loads(resp.text)
	return j

#Makes a get request 10 users
def getIds(token):
	headers = { "Authorization" : "Bearer "+token}
	params = (('limit', '10'),)
	resp = requests.get('https://api.qa.fitpay.ninja/users', headers=headers, params=params, verify=False)

	#Check to make sure it was a valid response
	if(resp.status_code != 200):
		invalidIdInput(resp)
		return None

	j = json.loads(resp.text)
	return j

#Makes a get request for a user's devices
def getDevices(token, userId):
	headers = { "Authorization" : "Bearer "+token}
	resp = requests.get('https://api.qa.fitpay.ninja/users/'+ userId +'/devices', headers=headers, verify=False)

	#Check to make sure it was a valid response
	if(resp.status_code != 200):
		invalidIdInput(resp)
		return None

	j = json.loads(resp.text)
	return j

#Returns a list of 10 user ids
def listUserIds(token):
	j = getIds(token)
	usersList = []
	#Appends all of the users to a list and return list
	for user in j["results"]:
		usersList.append(user["userId"])
	return usersList

#Returns a list of credit card ids for a user
def listCreditCardIds(j):
	creditCardList = []
	#Appends all of the credit card ids to a list for a user
	for i in j["results"]:
		creditCardList.append(i["creditCardId"])
	return creditCardList

#Returns a list of credit card states to a list for a user
def listCreditCardState(j):
	creditCardStateList = []
	#Appends all of the credit cards' states to a list for a user
	for i in j["results"]:
		creditCardStateList.append(i["state"])
	return creditCardStateList

#Returns a list of device ids for a user
def listDeviceIds(j):
	deviceIdsList = []
	#Appends all of the device ids to a list
	for i in j["results"]:
		deviceIdsList.append(i["deviceIdentifier"])
	return deviceIdsList

#Returns a list of devices' states for a user
def listDeviceStates(j):
	deviceStatesList = []
	#Appends all of the devices' states to a list
	for i in j["results"]:
		deviceStatesList.append(i["state"])
	return deviceStatesList

#Add credit card IDs and states to JSON object
def addCreditCardsToJson(jObj, creditCards, cardStates, f):
	#Check if there's a filter
	if(f == ""):
		for i in range(len(creditCards)):
			jObj["creditCard"+str(i)] = {"creditCardId":creditCards[i], "state":cardStates[i]}
	else:
		for i in range(len(creditCards)):
			if(cardStates[i] == f.upper()):
				jObj["creditCard"+str(i)] = {"creditCardId":creditCards[i], "state":cardStates[i]}

	return jObj

#Add devices' ids and states to JSON object
def addDevicesToJson(jObj, deviceIds, deviceStates, f):
	#Check if there's a filter
	if(f == ""):
		for k in range(len(deviceIds)):
			jObj["device"+str(k)] = {"deviceId":deviceIds[k], "state":deviceStates[k]}
	else:
		for k in range(len(deviceIds)):
			if(deviceStates[k] == f.upper()):
				jObj["device"+str(k)] = {"deviceId":deviceIds[k], "state":deviceStates[k]}
	
	return jObj

#Makes a JSON object for a specified user that has credit card ids, their states, device ids, and their states
def makeJsonObjects(token, userId, filterCC, filterD):
	#Add user Id to the newly created JSON object
	jObj = {"userId":userId}
	reqCards = getCards(token, userId)

	if(reqCards == None):
		return
	reqDevices = getDevices(token, userId)

	if(reqDevices == None):
		return

	creditCards = listCreditCardIds(reqCards)
	cardStates = listCreditCardState(reqCards)
	deviceIds = listDeviceIds(reqDevices)
	deviceStates = listDeviceStates(reqDevices)

	jObj = addCreditCardsToJson(jObj, creditCards, cardStates, filterCC)
	jObj = addDevicesToJson(jObj, deviceIds, deviceStates, filterD)

	#print(json.dumps(jObj, indent=4))
	return jObj
