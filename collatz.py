# test practice of the the collatz sequence(the simplest impossible maths problem 

def collatz(number):
	while number != 1: 
		if number % 2 == 0: 
			number = number/2; 
			print(int(number))
		else: 
			number = (number*3) + 1
			print(int(number))

def main(): 
	print("Enter number: ")
	number = int(input())
	collatz(number)

main()
