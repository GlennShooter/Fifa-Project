import pandas as pd
from random import randint
from random import shuffle

#Reads in the data creating the constraint variable for the algorithum, finds the length of the data set and creates a df of players
def read_data(file):
	df = pd.read_csv(file)
	n_players = len(df)
	c_wage = input("Enter your wage budget: ")#184328
	c_wage = int(c_wage)
	c_budget = input("Enter your Transfer budget: ")#33916529
	c_budget = int(c_budget)
	players = df[["full_name","overall","eur_value","eur_wage","league"]]
	return n_players,c_wage,c_budget,players

#Reduces data set to only selected leagues 
def sel_leg(league,players):
	l = len(players)
	i = 0 
	league_lst = [league]
	df_players = players
	df_players = df_players[df_players.league.isin(league_lst)]
	return df_players

#Evaluates sovlutions
def evaluate(transfer,players):
	l = len(players)
	wage = sum([transfer[i]*players.iloc[i]["eur_wage"] for i in range(l)]) #calculate the wage total for proposed transfers
	budget = sum([transfer[i]*players.iloc[i]["eur_value"] for i in range(l)]) #calculate the cost of total transfers
	if wage > c_wage:
		fit = 0
	if budget > c_budget:
		fit = 0
	else:
		fit = sum([transfer[i]*players.iloc[i]["overall"] for i in range(l)])
	return transfer,fit,wage,budget

#Initialises an initial solution (this is an empty solution then the 1 flip neighbours are all possible options in the list)
def initialise(size,players):
	s = [randint(0,1) for i in range(size)]
	dif = len(players) - len(s)
	i = 0
	while i < dif:
		s.append(0)
		i = i + 1
	shuffle(s)
	return s

#Create a new oneflip neighbour
def one_flip(transfer,players):
	l = len(transfer)
	i = 0
	neighbours = []

	while i < l:
		#Create all the 1 filp neighbours
		neighbour = []
		if transfer[i] == 1:
			transfer[i] = 0
		else:
			transfer[i] = 1
		#Compile the neighbour list
		x = 0
		while x < l:
			neighbour.append(transfer[x])
			x = x + 1


		#Append the neighbour to a master list of neighbours 
		neighbours.append(neighbour)

		#revert transfer list back to origional form
		if transfer[i] == 0:
			transfer[i] = 1
		else:
			transfer[i] = 0

		#move up the counter
		i = i + 1

	


	#return master list of all neighbours
	return neighbours

    #evaluate the neighbouring transfers of the random seed 
    #Try store solutions in the return with each solution 
def neighbour_eval(neighbours,players):
	l = len(neighbours[0])
	x = 0
	neighbour_evals = []
	while x < l:
		#Find wage and budget total for each transfer
		wage = sum([neighbours[x][i]*players.iloc[i]["eur_wage"] for i in range(l)])
		budget = sum([neighbours[x][i]*players.iloc[i]["eur_value"]for i in range(l)])
		#Are the wage and budget for the transfer within the constraints
		if wage > c_wage or budget > c_budget:
			fit = 0
		if wage < c_wage and budget < c_budget: 
			fit = sum([neighbours[x][i]*players.iloc[i]["overall"] for i in range(l)])
			solution = neighbours[x]
			#Add evaluation of neighbour to master list of evaluations
			neighbour_evals.append([solution,fit,wage,budget])
			

			#move the counter
		x = x + 1
	
	return(neighbour_evals)

#compairs initial random seed against neighbours and returns the best result

def compair_neighbours(neighbour_sol,initial_sol):
	l = len(neighbour_sol)
	i = 0
	best_fit_neighbour = 0
	best_solution_neighbour = []
	best_fit_wage = 0
	best_fit_budget = 0
	df =players
	done = False 
	x = 0
	while x < l:
		if neighbour_sol[x][1] > best_fit_neighbour:
			best_fit_neighbour = neighbour_sol[x][1]
			best_fit_wage = neighbour_sol[x][2]
			best_fit_budget = neighbour_sol[x][3]
			best_solution_neighbour =  neighbour_sol[x][0]
			count = x
		x = x + 1 

	i = 0
	targets = []
	while i < len(best_solution_neighbour):
		if best_solution_neighbour[i] == 1:
			targets.append(players.iloc[i][["full_name","overall","eur_wage"]])
		i = i + 1


		
	print("BEST SOLUTION ",best_solution_neighbour,best_fit_neighbour,count)
	best_neighbour = []
	best_neighbour =[best_solution_neighbour, best_fit_neighbour,best_fit_wage,best_fit_budget,count]


	if best_neighbour[1] > initial_sol[1]:
		return best_neighbour 
	else:
		random_fit =[random_solution,initial_fit]
		return random_fit

#Produces the final list of transfer targets
def transfer_targets(best_solution, players):
	l = len(best_solution[0])
	targets = []

	i = 0
	while i < l:
		if best_solution[0][i] == 1:
			targets.append(players.iloc[i][["full_name","overall","eur_wage"]])
		i = i + 1
	return targets 


####Main
#Read in data 
inpu = read_data("C:\\Users\\Glenn's pc\\Documents\\Uni\\Python\\Kaggle\\learn\\Fifa transfer project\\fifa.csv")
done = False 
while done == False:
#Define the length of the df the constraints and the data to test
	n_players = inpu[0]
	c_wage = inpu[1]
	c_budget = inpu[2]
	players = inpu[3]
	print(players["league"].unique())
	league = players["league"].unique()

	i = 0
	while i < len(league):
		print(i,". ",league[i])
		i = i + 1

	choice = input("please enter the number of the league you wish to search: ")
	choice = int(choice)
	print("Searching, this may take a few minutes")
	players = sel_leg(league[choice],players)


#Create an initial transfer list 
	trans = initialise(0,players) #Holds the initial transfer solutions
#I made a while loop to reveal the player name in the random seed

	result = evaluate(trans,players)

#create a list of neighbouring solutions
	nei = one_flip(trans,players)


#Evaluate neighbours
	nei_eval = neighbour_eval(nei,players)

#print best result
	final = compair_neighbours(nei_eval,result)
	#print(final)


#parse out the final solutions list 
	targets = transfer_targets(final,players)
	print(targets[1])

	y_n = input("Would you like to sign this player 1 = yes, 0 = no: ")
	y_n = int(y_n)

	if y_n ==  0:
		done = False
		while done == False:
			nei_eval.pop(final[4])
			final = compair_neighbours(nei_eval,result)
			buy = transfer_targets(final,players)
			print("We recommed signing: ", buy[1]) 
			y_n = input("Would you like to sign this player: 1 = yes, 0 = no: ")
			y_n = int(y_n)
			if y_n == 0:
				done = False
			if y_n == 1:
				done = True 
	else:
		print()

	quit = input("Enter 0 to leave.  Enter 1 to search again: ")
	quit =int(quit)
	if quit == 0:
		done = True
	else:
		print()


