
def valid_num(msisdn):
	msisdnLen = len(msisdn)
	flag = 0
	if msisdnLen == 13:
		temp = msisdn[0:5]
		if temp == '88013' or temp == '88014' or temp == '88015' or temp == '88016' or temp == '88017' or temp == '88018' or temp == '88019':
			alChk = msisdn.isalnum()
			#print(alChk)
			if alChk == True:
				flag = 0
				#print("Hello")
			else:
				flag = 1
		else:
			flag = 1

	elif msisdnLen == 11:
		temp = msisdn[0:3]
		if temp == '013' or temp == '014' or temp == '015' or temp == '016' or temp == '017' or temp == '018' or temp == '019':
			alChk = msisdn.isalnum()
			#print(alChk)
			if alChk == True:
				flag = 0
				#print("Hello non")
			else:
				flag = 1
		else:
			flag = 1

	elif msisdnLen == 10:
		temp = msisdn[0:2]
		if temp == '13' or temp == '14' or temp == '15' or temp == '16' or temp == '17' or temp == '18' or temp == '19':
			alChk = msisdn.isalnum()
			#print(alChk)
			if alChk == True:
				flag = 0
				#print("Hello non")
			else:
				flag = 1
		else:
			flag = 1

	else:
		flag = 1

	if flag == 0:
		return True
	elif flag == 1:
		return False
	else:
		return "None"


def telco_name(mob):
	#print(msisdn)
	temp = str(mob)
	msisdnLen = len(temp)
	if msisdnLen == 13:
		temp = mob[0:5]
		if temp == '88017' or temp == '88013':
			return 'GRAMEEN'
		elif temp == '88019' or temp == '88014':
			return 'BANGLALINK'
		elif temp == '88018':
			return 'AKTEL'
		elif temp == '88016':
			return 'WARID'
		elif temp == '88015':
			return 'TELETALK'
		else:
			return 'None'
	elif msisdnLen == 11:
		temp = mob[0:3]
		if temp == '017' or temp == '013':
			return 'GRAMEEN'
		elif temp == '019' or temp == '014':
			return 'BANGLALINK'
		elif temp == '018':
			return 'AKTEL'
		elif temp == '016':
			return 'WARID'
		elif temp == '015':
			return 'TELETALK'
		else:
			return 'None'
	elif msisdnLen == 10:
		temp = mob[0:2]
		if temp == '17' or temp == '13':
			return 'GRAMEEN'
		elif temp == '19' or temp == '14':
			return 'BANGLALINK'
		elif temp == '18':
			return 'AKTEL'
		elif temp == '16':
			return 'WARID'
		elif temp == '15':
			return 'TELETALK'
		else:
			return 'None'
	else:
		return 'none'

#print(telco_name('01789668366'))
