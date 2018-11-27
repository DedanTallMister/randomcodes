print ('hello')
file = open("link auto.txt", "r")
links = file.read()
print (links)
file.close()
coin = input ("insert 1 coin: ")
if coin == "1" or ded == "coin":
	print ("Game start!")
	i = 0
	while True:
		num = int(input ("insert any value between 1 and 100: "))
		if num < 50:
			print ("Too low, try harder!")
		elif num >50:
			print ("Too High, lower your bounds!")
		else:
			print ("real NiBBa Hours!!")
			break
else:
	print ("no coin")