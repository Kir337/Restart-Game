# Initial values for game variables
INITIAL_VALUES = {
    'basement_door_lock': False,
    'bathroom_elevator_down': False,
    'well_activated' : False,
    'toilet_clogged': False,
    'anvil': 0,
    'bed': 0,
    'blue_gem': 0,
    'support_beam': 0,
    'trapper': 0,
    'money': 0,
    'bedroom_choices': ['bed', 'alarm clock', 'window', 'support beam', 'door'],
    'bathroom_choices': ['toilet', 'trapper', 'pacifier', 'toilet paper', 'door'],
    'basement_choices': ['switch', 'axe', 'skrewdriver', 'battery', 'anvil', 'door'],
    'refridgerator_choices': ['door', 'glue', 'eggs', 'safe', 'gem', 'money'],
    'inventory': [],
    'random' : [None, None, None]
}

def reset_game(keep_vars=None):
    """
    Reset game variables to initial values, optionally keeping some variables unchanged.
    
    Args:
        keep_vars (set): Set of variable names to preserve current values for.
    """
    if keep_vars is None:
        keep_vars = set()
    
    for var_name, initial_value in INITIAL_VALUES.items():
        if var_name not in keep_vars:
            globals()[var_name] = initial_value.copy() if isinstance(initial_value, list) else initial_value

def start(keep_vars=None):
    #######################################################################################################################################
    #Initializing the Variables
    #######################################################################################################################################
    # Declare all variables as global
    global anvil, basement_door_lock, bathroom_elevator_down, bed, blue_gem, support_beam, trapper, toilet_clogged
    global bedroom_choices, bathroom_choices, basement_choices, refridgerator_choices, money, inventory
    
    # Reset variables to initial values, keeping specified ones
    reset_game(keep_vars)
    
    #######################################################################################################################################
    #######################################################################################################################################
    #Functions for Large Scale Room Actions
    #######################################################################################################################################
    #######################################################################################################################################
    def bedroom():
        global bedroom_choices
        global inventory
        print('You are in a bedroom')
        print('In the room, there is a:\n\tBed -', bedroom_choices.index('bed')+1)
        if 'alarm clock' in bedroom_choices:
            print('\tTicking Alarm Clock -', bedroom_choices.index('alarm clock')+1)
        print('\tWindow -', bedroom_choices.index('window')+1, '\n\tSupport Beam -', bedroom_choices.index('support beam')+1, '\n\tDoor -', bedroom_choices.index('door')+1)
        while True:
            try:
                choice = int(input('What would you like to do? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == bedroom_choices.index('bed')+1:
            bed_interaction()
            return
        elif 'alarm clock' in bedroom_choices and choice == bedroom_choices.index('alarm clock')+1:
            if len(inventory) < 6:
                print('You got an Alarm Clock')
                inventory.append('Alarm Clock')
                bedroom_choices.remove('alarm clock')
            else:
                print('Inventory is full')
        elif choice == bedroom_choices.index('window')+1:
            window_interaction()
            return
        elif choice == bedroom_choices.index('support beam')+1:
            support_beam_interaction()
            return
        elif choice == bedroom_choices.index('door')+1:
            if 'alarm clock' in bedroom_choices:
                print('As you go to grab the bedroom\'s door knob, the alarm clock suddenly stops ticking and explodes, visciously throwing you across the room\nYOU WERE BLOWN UP BY AN ALARM CLOCK')
                #Death
                choice = input('Would you like to play again? (y/n) ')
                if choice == 'y':
                    start(keep_vars={'random'})
                else:
                    print('You failed to break free from the time loop')
                return
            else:
                print('You walk down to the first floor')
                first_floor()
                return
        else:
            print('Invalid action')
        bedroom()

    def first_floor():
        global trapper
        global inventory
        print('In the room, there is a:\n\tBedroom Door - 1\n\tBathroom Door - 2\n\tRefridgerator - 3\n\tFront Door - 4')
        while True:
            try:
                choice = int(input('What would you like to do? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == 1:
            bedroom()
            return
        elif choice == 2:
            if trapper == 0:
                bathroom_door_check()
                return
            elif trapper >= 1:
                print('You walk into the bathroom')
                bathroom()
                return
        elif choice == 3:
            print('You open the fridge')
            refridgerator()
            return
        elif choice == 4:
            if anvil == 2:
                print('You walk into the front yard')
                frontyard()
                return
            else:
                print('You open the door to a man standing a few feet away with a gun trained at you\nHe fires a single shot into your head, killing you instantly\nYOU WERE SHOT BY A GUNMAN')
                #Death
                choice = input('Would you like to play again? (y/n) ')
                if choice == 'y':
                    start(keep_vars={'random'})
                else:
                    print('You failed to break free from the time loop')
                return
        else:
            print('Invalid action')
        first_floor()

    def bathroom():
        global bathroom_elevator_down
        global trapper
        global inventory
        global bathroom_choices
        global toilet_clogged
        if toilet_clogged == False:
            print('In the bathroom there is a:\n\tToilet -', bathroom_choices.index('toilet')+1)
        else:
            print('In the bathroom there is a:\n\tClogged Toilet -', bathroom_choices.index('toilet')+1)
        print('\tTrapper Husk -', bathroom_choices.index('trapper')+1)
        if 'pacifier' in bathroom_choices:
            print('\tPacifier -', bathroom_choices.index('pacifier')+1)
        if 'toilet paper' in bathroom_choices:
            print('\tToilet Paper Roll -', bathroom_choices.index('toilet paper')+1)
        print('\tDoor -', bathroom_choices.index('door')+1)
        while True:
            try:
                choice = int(input('What would you like to do? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == bathroom_choices.index('toilet')+1:
            if toilet_clogged == False:
                toilet_interaction()
                return
            else:
                print('You flush the clogged toilet causing the water to rise before quickly draining\nSuddenly, you hear a deep reverburating hum as the entire room begins to shake and move before jolting to a stop')
                bathroom_elevator_down = not bathroom_elevator_down
        elif choice == bathroom_choices.index('trapper')+1:
            if trapper == 1:
                trapper_interaction()
                return
            elif trapper == 2:
                if len(inventory) < 6:
                    print('You got some Gunpowder')
                    inventory.append('Gunpowder')
                    bathroom_choices.remove('trapper')
                    trapper = 3
                else:
                    print('Inventory is full')
        elif 'pacifier' in bathroom_choices and choice == bathroom_choices.index('pacifier')+1:
            if len(inventory) < 6:
                print('You got a Pacifier')
                inventory.append('Pacifier')
                bathroom_choices.remove('pacifier')
            else:
                print('Inventory is full')
        elif 'toilet paper' in bathroom_choices and choice == bathroom_choices.index('toilet paper')+1:
            if len(inventory) < 6:
                print('You got a Roll of Toilet Paper')
                inventory.append('Roll of Toilet Paper')
                bathroom_choices.remove('toilet paper')
            else:
                print('Inventory is full')
        elif choice == bathroom_choices.index('door')+1:
            if bathroom_elevator_down == True:
                print('You leave the bathroom and enter a hidden basement')
                basement()
                return
            else:
                print('You walk into the main room')
                first_floor()
                return
        else:
            print('Invalid action')
        bathroom()

    def basement():
        global anvil
        global basement_choices
        global basement_door_lock
        global inventory
        print('In the room, there is a:\n\tEmergency Switch -', basement_choices.index('switch')+1)
        if 'axe' in basement_choices:
            print('\tAxe -', basement_choices.index('axe')+1)
        if 'skrewdriver' in basement_choices:
            print('\tSkrewdriver -', basement_choices.index('skrewdriver')+1)
        if 'battery' in basement_choices:
            print('\tBattery Pack -', basement_choices.index('battery')+1)
        if 'anvil' in basement_choices:
            print('\tAnvil -', basement_choices.index('anvil')+1)
        print('\tBathroom Door -', basement_choices.index('door')+1)
        while True:
            try:
                choice = int(input('What would you like to do? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == basement_choices.index('switch')+1:
            print('You hear the bathroom door lock click')
            basement_door_lock = not basement_door_lock
        elif 'axe' in basement_choices and choice == basement_choices.index('axe')+1:
            if len(inventory) < 6:
                print('You got an Axe')
                inventory.append('Axe')
                basement_choices.remove('axe')
            else:
                print('Inventory is full')
        elif 'skrewdriver' in basement_choices and choice == basement_choices.index('skrewdriver')+1:
            if len(inventory) < 6:
                print('You got a Skrewdriver')
                inventory.append('Skrewdriver')
                basement_choices.remove('skrewdriver')
            else:
                print('Inventory is full')
        elif 'battery' in basement_choices and choice == basement_choices.index('battery')+1:
            if len(inventory) < 6:
                print('You got a Battery Pack')
                inventory.append('Battery Pack')
                basement_choices.remove('battery')
            else:
                print('Inventory is full')
        elif 'anvil' in basement_choices and choice == basement_choices.index('anvil')+1:
            if len(inventory) < 6:
                print('You got an Anvil')
                inventory.append('Anvil')
                basement_choices.remove('anvil')
                anvil = 1
            else:
                print('Inventory is full')
        elif choice == basement_choices.index('door')+1:
            if basement_door_lock == True:
                print('The bathroom door is locked')
            else:
                print('You walk into the bathroom')
                bathroom()
                return
        else:
            print('Invalid action')
        basement()

    def frontyard():
        global inventory
        global well_activated
        global random
        print('There is a:\n\tFront Door - 1\n\tStone Path - 2\n\tWell - 3\n\tDirt Path - 4')
        print('')
        while True:
            try:
                choice = int(input('What would you like to do?'))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == 1:
            first_floor()
        elif choice == 2:
            print('You follow the rocky path northward')
            stone_path()
            return
        elif choice == 3:
            if well_activated == False:
                if 'Red Gem' and 'Yellow Gem' and 'Green Gem' and 'Blue Gem' and 'Purple Gem' in inventory:
                    print('A holy glow emits from the well before you vision goes completely dark...')
                    print('')
                    start(keep_vars={'well_activated','random'})
                    return
                else:
                    print('There are 5 strange indents on the base of the well')
            else:
                print('The well emits a holy glow')
        elif choice == 4:
            print('You follow the dirt path southward')
            dirt_path()
            return
        frontyard()
        
    def stone_path():
        global inventory

    def dirt_path():
        global inventory


    def refridgerator():
        global blue_gem
        global inventory
        global refridgerator_choices
        global money
        print('In the fridge, there is a:\n\tDoor -', refridgerator_choices.index('door')+1)
        if 'glue' in refridgerator_choices:
            print('\tContainer of Glue -', refridgerator_choices.index('glue')+1)
        if 'eggs' in refridgerator_choices:
            print('\tCarton of Eggs -', refridgerator_choices.index('eggs')+1)
        if 'safe' in refridgerator_choices:
            print('\tLocked Safe -', refridgerator_choices.index('safe')+1)
        if not 'safe' in refridgerator_choices and 'gem' in refridgerator_choices:
            print('\tBlue Gem -', refridgerator_choices.index('gem')+1)
        if not 'safe' in refridgerator_choices and 'money' in refridgerator_choices:
            print('\t5 Dollars -', refridgerator_choices.index('money')+1)
        print('')
        while True:
            try:
                choice = int(input('What would you like to do? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
        elif choice == refridgerator_choices.index('door')+1:
            print('You close the refridgerator door')
            first_floor()
            return
        elif 'glue' in refridgerator_choices and choice == refridgerator_choices.index('glue')+1:
            if len(inventory) < 6:
                print('You got a Container of Glue')
                inventory.append('Glue')
                refridgerator_choices.remove('glue')
            else:
                print('Inventory is full')
        elif 'eggs' in refridgerator_choices and choice == refridgerator_choices.index('eggs')+1:
            if len(inventory) < 6:
                print('You got a Carton of Eggs')
                inventory.append('Eggs')
                refridgerator_choices.remove('eggs')
            else:
                print('Inventory is full')
        elif 'safe' in refridgerator_choices and choice == refridgerator_choices.index('safe')+1:
            safe_interaction()
            return
        elif not 'safe' in refridgerator_choices and 'gem' in refridgerator_choices and choice == refridgerator_choices.index('gem')+1:
            if len(inventory) < 6:
                print('You got a Blue Gem')
                inventory.append('Blue Gem')
                refridgerator_choices.remove('gem')
            else:
                print('Inventory is full')
        elif not 'safe' in refridgerator_choices and 'money' in refridgerator_choices and choice == refridgerator_choices.index('money')+1 and blue_gem == 1:
            if len(inventory) < 6:
                print('You got 5 Dollars')
                inventory.append('5 Dollars')
                refridgerator_choices.remove('money')
            else:
                print('Inventory is full')
        refridgerator()



    #######################################################################################################################################
    #When ever there is a choice, the player can press 0 to run this function to check their inventory
    #######################################################################################################################################
    def check_inventory():
        global inventory
        print('Inventory:')
        if inventory:
            for i, item in enumerate(inventory, start=1):
                print(f'\t{item} - {i}')
        else:
            print('\tEmpty')
        print('')

    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    #All individual intercations
    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    def support_beam_interaction():
        global support_beam
        global inventory
        if support_beam == 0:
            while True:
                try:
                    choice = int(input('What item would you like to use? '))
                    print('')
                    break
                except ValueError:
                    print('Invalid response')
            if choice == 0:
                check_inventory()
                support_beam_interaction()
                return
            elif 'Glue' in inventory and choice == inventory.index('Glue')+1:
                print('You fix the support beam')
                support_beam = 1
                inventory.remove('Glue')
            else:
                print('The support beam is cracked')
        else:
            print('The support beam was fixed with a heavy application of super glue')
        bedroom()

    def window_interaction():
        global anvil
        global inventory
        if anvil <= 1:
            while True:
                try:
                    choice = int(input('What item would you like to use? '))
                    print('')
                    break
                except ValueError:
                    print('Invalid response')
            if choice == 0:
                check_inventory()
                window_interaction()
                return
            elif 'Anvil' in inventory and choice == inventory.index('Anvil')+1:
                print('You drop the anvil out the window, crushing the gunman\'s head and killing him instantly')
                anvil = 2
                inventory.remove('Anvil')
            else:
                print('There is a gunman waiting outside your front door')
        else:
            print('The gunman is laying dead outside your front door')
        bedroom()

    def bed_interaction():
        global bed
        global inventory
        if bed == 0:
            while True:
                try:
                    choice = int(input('What item would you like to use? '))
                    print('')
                    break
                except ValueError:
                    print('Invalid response')
            if choice == 0:
                check_inventory()
                bed_interaction()
                return
            elif 'Inkling' in inventory and choice == inventory.index('Inkling')+1:
                print('You give the Inkler the Inkling\nIt pushes a key out from under the bed before retreating further under the bed')
                bed = 1
                inventory.remove('Inkling')
            else:
                print('An inky darkness slithers out from the bed, wrapping around your leg and pulling you under')
                print('YOU ARE TORN APART BY AN INKLER')
                #Death
                choice = input('Would you like to play again? (y/n) ')
                if choice == 'y':
                    start(keep_vars={'random'})
                else:
                    print('You failed to break free from the time loop')
                return
        elif bed == 1:
            if len(inventory) < 6:
                print('You got a Key')
                inventory.append('Key')
                bed = 2
            else:
                print('Inventory is full')
        else:
            print('The Inkler has retreated to the far cornder of the bed with the Inkling')
        bedroom()

    def bathroom_door_check():
        global trapper
        global inventory
        while True:
            try:
                choice = int(input('What item would you like to use? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
            bathroom_door_check()
            return
        elif 'Alarm Clock' in inventory and choice == inventory.index('Alarm Clock')+1:
            print('You toss the ticking alarm clock into the bathroom\nAn enormous green and pink plant descends into view, swallowing the alarm clock and returning to the ceiling\nSeconds later, the alarm clock explodes, blowing up the Trapper from the inside out\nYou walk into the recently cleared out bathroom')
            trapper = 1
            inventory.remove('Alarm Clock')
            bathroom()
            return
        else:
            print('You walk unsuspectingly into the bathroom\nAn enormous green and pink plant descends from above you\nThe Trapper swallows your head and plunges razor sharp thorns into your neck, cutting off blood flow\nYOU WERE EATEN BY A TRAPPER')
            #Death
            choice = input('Would you like to play again? (y/n) ')
            if choice == 'y':
                start(keep_vars={'random'})
            else:
                print('You failed to break free from the time loop')
            return

    def toilet_interaction():
        global toilet_clogged
        global inventory
        while True:
            try:
                choice = int(input('What item would you like to use? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
            toilet_interaction()
            return
        elif 'Roll of Toilet Paper' in inventory and choice == inventory.index('Roll of Toilet Paper')+1:
            toilet_clogged = True
            inventory.remove('Roll of Toilet Paper')
            print('You lodge the roll of toilet paper into the toilet before flushing and clogging the toilet')
        else:
            print('You flush the toilet')
        bathroom()

    def trapper_interaction():
        global trapper
        global bathroom_choices
        global inventory
        while True:
            try:
                choice = int(input('What item would you like to use? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
            trapper_interaction()
            return
        elif 'Axe' in inventory and choice == inventory.index('Axe')+1:
            trapper = 2
            print('You break open the trapper and find some gun powerder')
        else:
            print('The smoldering trapper is laying on the bathroom floor')
        bathroom()

    def safe_interaction():
        global inventory
        global refridgerator_choices
        while True:
            try:
                choice = int(input('What item would you like to use? '))
                print('')
                break
            except ValueError:
                print('Invalid response')
        if choice == 0:
            check_inventory()
            safe_interaction()
            return
        elif 'Key' in inventory and choice == inventory.index('Key')+1:
            print('You unlock the safe with the key')
            inventory.remove('Key')
            refridgerator_choices.remove('safe')
        else:
            print('The safe is locked with a key-shaped hole')
        refridgerator()

    #######################################################################################################################################
    #Starts the game
    #######################################################################################################################################
    print('>To choose an action, type 1-9 depending on the options. Type 0 to check inventory at any time (you can hold a maximum of 6 items at once)<')
    bedroom()
start()
