import random
if __name__=='__main__':
    # Input room size
    while 1:
        room_size=float(input('Please enter a room size:'))
        if room_size<1.0:
            print("Room size should be larger than one. Please reenter it.")
        else:
            break
    # Generate starting and exit point 
    loc_x=random.randint(1,int(room_size))
    loc_y = random.randint(1, int(room_size))
    exit_x = random.randint(1, int(room_size))
    exit_y = random.randint(1, int(room_size))
    print('Your current location:({0},{1})'.format(loc_x, loc_y))
    print('The exit point:({0},{1})'.format(exit_x, exit_y))
    if loc_x==exit_x and loc_y==exit_y:
        print('Luckly,you are just at the exit point!')
    else:
        print('You need at least {0} steps to go out.'.format(abs(loc_x - exit_x) + abs(loc_y - exit_y)))
        # Initiate the total moving steps
        step_num=0 
        # Execute movement
        while 1:
            # Choose a move direction
            direction=int(input('Choose your next move direction(1.North 2.South 3.East 4.West):'))
            if direction>4 or direction<1:
                print("Please choose a valid direction.")
            # Move North
            elif direction==1:
                loc_y=loc_y+1
                step_num=step_num+1
                if loc_y > room_size:
                    print("Sorry,you hit the wall! Please move toward another direction.")
                    loc_y=loc_y-1
                    step_num = step_num - 1
            # Move South
            elif direction==2:
                loc_y=loc_y-1
                step_num = step_num + 1
                if loc_y <0:
                    print("Sorry,you hit the wall! Please move toward another direction.")
                    loc_y = loc_y + 1
                    step_num = step_num - 1
            # Move East
            elif direction==3:
                loc_x=loc_x+1
                step_num = step_num + 1
                if loc_x > room_size:
                    print("Sorry,you hit the wall! Please move toward another direction.")
                    loc_x = loc_x - 1
                    step_num = step_num - 1
            # Move West
            elif direction==4:
                loc_x=loc_x-1
                step_num = step_num + 1
                if loc_x < 0:
                    print("Sorry,you hit the wall! Please move toward another direction.")
                    loc_x=loc_x+1
                    step_num = step_num - 1
            # Print out messages
            if loc_x!=exit_x or loc_y!=exit_y:
                print('Your current location:({0},{1})'.format(loc_x,loc_y))
                print('The exit point:({0},{1})'.format(exit_x,exit_y))
                print('You have moved {0} steps.'.format(step_num))
                print('You still need at least {0} steps to go out.'.format(abs(loc_x-exit_x)+abs(loc_y-exit_y)))
            else:
                print('Bingo! you have reached the exit with moving total {0} steps.'.format(step_num))
                break