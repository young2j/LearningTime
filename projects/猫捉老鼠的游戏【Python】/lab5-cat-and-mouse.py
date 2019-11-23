import random
if __name__ == '__main__':
	print('The cat and mouse game is about to begin...')
	#Choose the room size(inner size) larger than at least one step.
	while 1:
		room_size = float(input('Please enter a room size:'))
		if room_size<1.0:
			print("Room size should be larger than one. Please reenter it.")
		else:
			break
	#Specify the maximum number of steps other than negative.
	while 1:
		max_steps = int(input('Please specify the maximum number of steps:'))
		if max_steps<0:
			print('Move steps should be a positive integer or zero.Please specify it again.')
		else:
			break
	#Generate random location of cat and mouse.
	cat_x = random.randint(0, int(room_size))
	cat_y = random.randint(0, int(room_size))
	mouse_x = random.randint(0, int(room_size))
	mouse_y = random.randint(0, int(room_size))
	print('The cat is located in:({0},{1})'.format(cat_x,cat_y))
	print('The mouse is located in:({0},{1})'.format(mouse_x,mouse_y))
	#Think of the situation that there might be the same location of cat and mouse when just beginning.
	if cat_x==mouse_x and cat_y==mouse_y:
		print('Unfortunately, the mouse was eaten by the cat at the beginning of the game.')
	#Otherwise the game continues.
	else:
		print('The cat must eat the mouse in {0} steps, or the mouse will run away.'.format(max_steps))
		step_count = 0 #generate a step counter
		direction={'North': 1, 'South': 2, 'East': 3, 'West': 4}
		while 1:
			#Generate random direction to move.
			cat_move_direction = random.randint(1, 4)
			mouse_move_direction = random.randint(1, 4)
			'''Note that when the cat or mouse is located in the edges of room,
			it will hit the wall if continuing to move toward the direction out of range. '''
			cat_hit_wall = (cat_x ==0 and cat_move_direction==direction['West']) or\
						   (cat_x ==room_size and cat_move_direction==direction['East']) or\
						   (cat_y ==0 and cat_move_direction==direction['South']) or\
							 (cat_y ==room_size and cat_move_direction==direction['North']) 
			mouse_hit_wall = (mouse_x ==0 and mouse_move_direction==direction['West']) or\
							 (mouse_x ==room_size and mouse_move_direction==direction['East']) or\
							 (mouse_y ==0 and mouse_move_direction==direction['South']) or\
						 	 (mouse_y ==room_size and mouse_move_direction==direction['North'])
			# When the cat and mouse all not hit the wall,take a move and change the location.
			if not (cat_hit_wall or mouse_hit_wall):
				if  cat_move_direction==direction['North']:
					cat_y = cat_y+1
					step_count = step_count + 1
				elif cat_move_direction ==direction['South']:
					cat_y = cat_y-1
					step_count = step_count + 1
				elif cat_move_direction ==direction['East']:
					cat_x = cat_x+1
					step_count = step_count + 1
				else:
					cat_x = cat_x-1
					step_count = step_count + 1
				if  mouse_move_direction==direction['North']:
					mouse_y = mouse_y+1
				elif mouse_move_direction ==direction['South']:
					mouse_y = mouse_y-1
				elif mouse_move_direction ==direction['East']:
					mouse_x = mouse_x+1	
				else:
					mouse_x = mouse_x-1
				#Print out some key and convenient for observation information.
				print('----------------------------------------------------')
				print('The cat is chasing toward {0} and located in:({1},{2})'.format(list(direction.keys())[cat_move_direction-1],cat_x,cat_y))
				print('The mouse is running toward {0} and located in:({1},{2})'.format(list(direction.keys())[mouse_move_direction-1],mouse_x,mouse_y))
				#Compute the remaining steps in order to control steps the cat moved no more than maximum steps. 
				remaining_steps = max_steps - step_count
				'''When the remaining steps is greater than zero and the cat and mouse are not at the same location,
					compute how many steps the cat moved and still leave.It means that game is over for cat and mouse
					to be at the same loaction or having no remain steps.''' 
				if remaining_steps>0:
					if cat_x!=mouse_x or cat_y!=mouse_y:
						print('The cat has chased {0} steps and only {1} steps left'.format(step_count,remaining_steps))
					else:
						print('After chasing {0} steps,the cat ate the mouse.'.format(step_count))
						break
				if remaining_steps==0:
					if cat_x != mouse_x or cat_y != mouse_y:
						print('After chasing {0} steps, the cat gave up and the mouse survived!'.format(step_count))
						break
					else:
						print('In the final step,the cat ate the mouse.')
						break