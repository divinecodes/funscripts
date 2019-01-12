""" solution to the josephus problem """
def safe_position(n):
	"""
		function to get the safe position
		formulae
		Initial(n) = 2^a +l
		W(n) = 2l + 1;
	    where n = the total number 
			  a = the power of two
			  l = the reminder after the power is deducted from n				
	"""
	pow_two = 0
	i = 0
	while (n - pow_two) >= pow_two: 
		pow_two = 2**i
		i = i+1
	l = n - pow_two
	safe_p =(2* l) +1

	return safe_p

def main(): 
	""" main function """
	print("Input the number of in circle: ")
	n = int(input())
	print("Safe Position: ",safe_position(n))

main()
	
	
