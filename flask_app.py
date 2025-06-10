from flask import Flask, request, jsonify, render_template
import json
import random
import time

app = Flask(__name__)

# Character classes and their base stats
CHARACTER_CLASSES = {
    'monk': {
        'hit_die': 8,
        'proficiencies': ['dexterity', 'strength'],
        'skills': ['acrobatics', 'athletics', 'history', 'insight', 'religion', 'stealth']
    },
    'wizard': {
        'hit_die': 6,
        'proficiencies': ['intelligence', 'wisdom'],
        'skills': ['arcana', 'history', 'insight', 'investigation', 'medicine', 'religion']
    },
    'fighter': {
        'hit_die': 10,
        'proficiencies': ['strength', 'constitution'],
        'skills': ['acrobatics', 'animal_handling', 'athletics', 'history', 'insight', 'intimidation', 'perception', 'survival']
    }
}

# Detailed RPG scenarios with rich world-building
SCENARIOS = {
    'northern-realms': {
        'title': 'The Elder Scrolls: Tamriel Adventures',
        'setting': 'Elder Scrolls Universe',
        'world_description': 'The ancient continent of Tamriel, where the Elder Scrolls have foretold of great changes. You are Ra\'el, a wandering monk seeking balance in a world torn by conflict.',
        'starting_location': 'Border between Cyrodiil and Valenwood',
        'current_scene': 'fork_in_road',
        'available_locations': {
            'culdenwatch': 'A ruined town to the north, abandoned after mysterious events',
            'whispering_vale': 'Dense eastern forests known for strange phenomena',
            'imperial_waystation': 'A crumbling outpost to the west'
        }
    },
    'whispering-town': {
        'title': 'Mysteries of Millbrook',
        'setting': 'Modern Mystery',
        'world_description': 'The quiet suburb of Millbrook harbors dark secrets beneath its perfect facade.',
        'starting_location': 'Main Street, Millbrook',
        'current_scene': 'arrival',
        'available_locations': {
            'town_center': 'The heart of Millbrook with its pristine shops',
            'old_cemetery': 'Ancient burial ground with weathered headstones',
            'abandoned_house': 'The house that no one talks about'
        }
    },
    'neo-tokyo': {
        'title': 'Neo-Tokyo 2087: Digital Dreams',
        'setting': 'Cyberpunk Future',
        'world_description': 'In the neon-soaked megacity of Neo-Tokyo, corporations rule with digital fists while hackers fight in the shadows.',
        'starting_location': 'District 7 Underground',
        'current_scene': 'jack_in',
        'available_locations': {
            'data_haven': 'Hidden server farm in the deep web',
            'corpo_plaza': 'Gleaming corporate headquarters above',
            'black_market': 'Underground tech bazaar'
        }
    }
}

def roll_dice(sides=20, modifier=0, advantage=False, disadvantage=False):
    """Roll dice with D&D 5E mechanics"""
    rolls = [random.randint(1, sides)]
    
    if advantage or disadvantage:
        rolls.append(random.randint(1, sides))
        if advantage:
            result = max(rolls)
        else:  # disadvantage
            result = min(rolls)
    else:
        result = rolls[0]
    
    total = result + modifier
    
    return {
        'dice': f'd{sides}',
        'rolls': rolls,
        'base_roll': result,
        'modifier': modifier,
        'total': total,
        'advantage': advantage,
        'disadvantage': disadvantage
    }

def get_ability_modifier(score):
    """Convert ability score to modifier"""
    return (score - 10) // 2

def determine_success(roll_total, difficulty_class=15):
    """Determine if a roll succeeds"""
    if roll_total >= difficulty_class + 10:
        return 'critical_success'
    elif roll_total >= difficulty_class:
        return 'success'
    elif roll_total >= difficulty_class - 5:
        return 'partial_success'
    else:
        return 'failure'

def generate_loot(loot_type='basic', location='forest'):
    """Generate random loot based on location and type"""
    loot_tables = {
        'forest': {
            'basic': [
                {'name': 'Healing Herbs', 'icon': 'fas fa-leaf', 'description': 'Restores 1d4 HP when used'},
                {'name': 'Wild Berries', 'icon': 'fas fa-apple-alt', 'description': 'Provides sustenance for 1 day'},
                {'name': 'Wooden Branch', 'icon': 'fas fa-tree', 'description': 'Improvised club weapon'},
                {'name': 'Animal Hide', 'icon': 'fas fa-paw', 'description': 'Can be crafted into basic armor'}
            ],
            'valuable': [
                {'name': 'Potion of Minor Healing', 'icon': 'fas fa-flask', 'description': '+1d4+2 HP when used'},
                {'name': 'Scroll of Sparks', 'icon': 'fas fa-scroll', 'description': 'Lightning spell (2 HP cost)'},
                {'name': 'Silver Pieces', 'icon': 'fas fa-coins', 'description': f'{random.randint(5, 20)} coins'},
                {'name': 'Enchanted Key', 'icon': 'fas fa-key', 'description': 'Opens magical locks'}
            ]
        }
    }
    
    items = []
    table = loot_tables.get(location, loot_tables['forest'])
    loot_list = table.get(loot_type, table['basic'])
    
    # Generate 1-4 items
    num_items = random.randint(1, min(4, len(loot_list)))
    selected_items = random.sample(loot_list, num_items)
    
    for item in selected_items:
        if 'coins' in item['description']:
            amount = random.randint(5, 20)
            item['description'] = f'{amount} silver pieces'
            item['quantity'] = amount
        items.append(item)
    
    return items

@app.route('/')
def index():
    return render_template('scenario_selection.html')

@app.route('/create-character')
def create_character():
    scenario = request.args.get('scenario', 'northern-realms')
    return render_template('character_creation.html', scenario=scenario)

@app.route('/game')
def game():
    scenario = request.args.get('scenario', 'northern-realms')
    return render_template('game_interface.html', scenario=scenario)

@app.route('/api/turn', methods=['POST'])
def handle_turn():
    try:
        data = request.get_json()
        choice = data.get('choice')
        choice_text = data.get('choice_text', '')
        custom_action = data.get('action', '')
        game_state = data.get('game_state', {})
        
        # Extract current scenario and game state
        scenario_id = game_state.get('game', {}).get('scenario', 'northern-realms')
        scenario = SCENARIOS.get(scenario_id, SCENARIOS['northern-realms'])
        
        # Initialize response structure
        response = {
            'success': True,
            'story': '',
            'choices': [],
            'game_state': game_state,
            'dice_roll': None,
            'loot': None,
            'quest_update': None
        }
        
        # Determine action to process
        action = custom_action if custom_action else choice_text
        
        # Process different actions based on scenario and choice
        if scenario_id == 'northern-realms':
            response = process_northern_realms_action(action, choice, game_state, response)
        elif scenario_id == 'whispering-town':
            response = process_whispering_town_action(action, choice, game_state, response)
        elif scenario_id == 'neo-tokyo':
            response = process_neo_tokyo_action(action, choice, game_state, response)
        else:
            response = process_generic_action(action, choice, game_state, response)
        
        # Update turn number and time
        if 'game' in response['game_state']:
            response['game_state']['game']['turnNumber'] += 1
            
            # Advance time occasionally
            if response['game_state']['game']['turnNumber'] % 3 == 0:
                advance_time(response['game_state']['game'])
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

def process_northern_realms_action(action, choice, game_state, response):
    """Process actions specific to the Northern Realms scenario"""
    
    # Get character stats for skill checks
    character = game_state.get('character', {})
    abilities = character.get('abilities', {})
    
    action_lower = action.lower()
    
    if 'follow' in action_lower and 'track' in action_lower:
        # Following the barefoot tracks
        wisdom_modifier = abilities.get('wisdom', {}).get('modifier', 2)
        survival_roll = roll_dice(20, wisdom_modifier + 2)  # +2 for tracking proficiency
        
        response['dice_roll'] = {
            'type': 'Survival (Tracking)',
            'formula': f"d20 + (Wisdom {wisdom_modifier} + Proficiency +2)",
            'total': survival_roll['total'],
            'success': survival_roll['total'] >= 15
        }
        
        if survival_roll['total'] >= 20:
            response['story'] = """You move silently through the Whispering Vale, your monk training serving you well. The tracks are clear as daylight to your experienced eye - small, bare feet moving with purpose but showing signs of fatigue. 
            
            After an hour of careful tracking, you discover a hidden grove where a young wood elf sits by a dying campfire, injured and alone. She looks up with wide, frightened eyes as you approach."""
            
            response['quest_update'] = {
                'text': 'New: Rescue the Lost Wood Elf - The tracks have led you to an injured wood elf who may need assistance.'
            }
            
            response['choices'] = [
                'Approach slowly with hands visible to show peaceful intent',
                'Call out softly in Elvish to reassure her', 
                'Use your herbalism kit to offer medical aid',
                'Ask what happened and how you can help',
                'Scan the area for threats before approaching',
                'Offer food and water from your supplies'
            ]
            
        elif survival_roll['total'] >= 15:
            response['story'] = """You follow the tracks deeper into the Whispering Vale. The ancient trees grow closer together here, their branches forming a canopy that blocks most sunlight. The tracks become harder to follow in the soft earth, but you persist.
            
            Strange whispers seem to echo through the woods - not quite voices, but something that makes the hair on your neck stand up. You sense you're getting close to something important."""
            
            response['choices'] = [
                'Continue following the tracks despite the eerie atmosphere',
                'Stop and listen carefully to the whispers',
                'Use your meditation training to center yourself',
                'Look for a safe place to rest and observe',
                'Turn back - this feels too dangerous'
            ]
        else:
            response['story'] = """You attempt to follow the tracks into the Whispering Vale, but the dense undergrowth and shifting light play tricks on your eyes. After twenty minutes of searching, you realize you've lost the trail completely.
            
            The forest seems to close in around you, and you hear distant sounds that could be wildlife... or something else. You'll need to try a different approach or risk getting lost in these ancient woods."""
            
            response['choices'] = [
                'Backtrack to the fork and try a different path',
                'Use your dart to mark trees and continue exploring',
                'Climb a tall tree to get your bearings',
                'Meditate to enhance your senses and try again',
                'Head toward the sound of running water you hear nearby'
            ]
    
    elif 'culdenwatch' in action_lower or 'north' in action_lower:
        # Heading to the ruined town
        response['story'] = """You take the northern path toward Culdenwatch. The broken signpost creaks in the wind as you pass, and the road becomes increasingly overgrown. Ancient cobblestones peek through patches of moss and weeds.
        
        As you crest a small hill, the ruins of Culdenwatch spread before you. Once-proud buildings stand like broken teeth against the sky, their roofs collapsed and walls crumbling. Vines and strange, luminescent fungi have claimed many structures.
        
        At the town's heart, you spot what appears to be an intact tower, its windows glowing with an eerie blue light."""
        
        # Check for perception
        wisdom_modifier = abilities.get('wisdom', {}).get('modifier', 2)
        perception_roll = roll_dice(20, wisdom_modifier)
        
        response['dice_roll'] = {
            'type': 'Perception',
            'formula': f"d20 + (Wisdom {wisdom_modifier})",
            'total': perception_roll['total'],
            'success': perception_roll['total'] >= 12
        }
        
        if perception_roll['total'] >= 15:
            response['story'] += "\n\nYour keen senses detect movement among the ruins - shadowy figures that seem to glide between the buildings. They haven't noticed you yet, giving you the advantage of surprise."
            
            response['choices'] = [
                'Sneak closer to investigate the shadowy figures',
                'Head directly to the glowing tower',
                'Circle around the town to find another entrance',
                'Use a dart to test if the figures react to sound',
                'Attempt to communicate with the figures',
                'Retreat and observe from a safe distance'
            ]
        else:
            response['choices'] = [
                'Approach the glowing tower carefully',
                'Search the outer ruins for useful items',
                'Call out to see if anyone is alive in the town',
                'Look for a safe place to make camp nearby',
                'Explore the collapsed buildings methodically'
            ]
    
    elif 'imperial' in action_lower or 'west' in action_lower:
        # Heading to the Imperial waystation
        response['story'] = """You take the western path toward the old Imperial waystation. The road here is in better condition, with remnants of ancient stonework still visible beneath centuries of weathering.
        
        The waystation appears as a squat, fortified structure built into the side of a hill. Its heavy wooden doors hang askew, and Imperial banners flutter in tatters from rusted poles. Moss and ivy have claimed much of the exterior walls."""
        
        # Automatic loot discovery
        response['loot'] = {
            'description': 'Searching the waystation\'s abandoned barracks, you find supplies left behind by long-dead soldiers:',
            'items': generate_loot('valuable', 'ruins')
        }
        
        response['choices'] = [
            'Explore the waystation\'s underground storage areas',
            'Examine the Imperial records and maps',
            'Rest here for the night - it seems secure',
            'Search for any surviving Imperial equipment',
            'Look for signs of recent visitors',
            'Check the watchtower for a better view of the area'
        ]
    
    elif 'potion' in action_lower or 'scroll' in action_lower:
        # Using magical items
        if 'potion' in action_lower:
            healing = roll_dice(4, 2)  # 1d4+2 healing
            current_hp = character.get('health', {}).get('current', 20)
            max_hp = character.get('health', {}).get('max', 20)
            new_hp = min(current_hp + healing['total'], max_hp)
            
            response['game_state']['character']['health']['current'] = new_hp
            
            response['story'] = f"""You uncork the small glass vial and drink the healing potion. The liquid tastes of mint and spring water, with an underlying warmth that spreads through your body.
            
            The potion restores {healing['total']} hit points. Your health is now {new_hp}/{max_hp}."""
            
            # Remove potion from inventory
            inventory = response['game_state']['character']['inventory']
            response['game_state']['character']['inventory'] = [
                item for item in inventory if 'Potion of Minor Healing' not in item['name']
            ]
            
        else:  # Using scroll
            current_hp = character.get('health', {}).get('current', 20)
            response['game_state']['character']['health']['current'] = max(0, current_hp - 2)
            
            response['story'] = """You unroll the magical scroll and speak the incantation written in Ancient Draconic. Lightning crackles between your fingers as you cast the spell, but channeling the magic drains some of your life force.
            
            You lose 2 HP from casting the spell, but now have a lightning bolt ready to unleash at your enemies."""
            
            # Remove scroll from inventory
            inventory = response['game_state']['character']['inventory']
            response['game_state']['character']['inventory'] = [
                item for item in inventory if 'Scroll of Sparks' not in item['name']
            ]
            
            response['quest_update'] = {
                'text': 'Sparks spell ready - You can cast lightning bolt (1d8 damage, 30ft range) as your next action.'
            }
        
        response['choices'] = [
            'Continue following the tracks into the Whispering Vale',
            'Head north to Culdenwatch', 
            'Explore the Imperial waystation to the west',
            'Search the area more thoroughly',
            'Rest and meditate to recover'
        ]
    
    else:
        # Generic exploration or other actions
        response['story'] = process_generic_exploration(action, game_state)
        response['choices'] = [
            'Search for more clues in the immediate area',
            'Follow the barefoot tracks eastward',
            'Head north toward Culdenwatch',
            'Investigate the Imperial waystation to the west',
            'Rest and consider your options carefully',
            'Try a completely different approach'
        ]
    
    return response

def process_whispering_town_action(action, choice, game_state, response):
    """Process actions for the modern mystery scenario"""
    response['story'] = f"""You decide to {action.lower()}. The suburban streets of Millbrook seem quiet, almost too quiet. Manicured lawns stretch endlessly, and curtains twitch in windows as unseen eyes watch your every move.
    
    Something is definitely not right in this perfect little town."""
    
    response['choices'] = [
        'Knock on doors to introduce yourself to neighbors',
        'Visit the local coffee shop to gather information',
        'Check the town records at city hall',
        'Investigate the old cemetery on the edge of town',
        'Follow the suspicious person you spotted earlier'
    ]
    
    return response

def process_neo_tokyo_action(action, choice, game_state, response):
    """Process actions for the cyberpunk scenario"""
    response['story'] = f"""You {action.lower()} in the neon-lit underbelly of Neo-Tokyo. Holographic advertisements flicker overhead while data streams flow like digital rivers through the city's neural networks.
    
    Your cybernetic implants detect encrypted traffic nearby - someone is conducting illegal business in the shadows."""
    
    response['choices'] = [
        'Jack into the nearest data terminal',
        'Follow the encrypted signal to its source',
        'Contact your fixer for information',
        'Upgrade your gear at the black market',
        'Infiltrate the corporate facility above'
    ]
    
    return response

def process_generic_action(action, choice, game_state, response):
    """Process generic actions when scenario-specific handling isn't needed"""
    response['story'] = process_generic_exploration(action, game_state)
    response['choices'] = [
        'Explore the surrounding area more thoroughly',
        'Try to find other travelers or inhabitants',
        'Look for shelter or a place to rest',
        'Search for useful resources or items',
        'Continue on your intended path'
    ]
    
    return response

def process_generic_exploration(action, game_state):
    """Generate generic exploration narrative"""
    scenario_id = game_state.get('game', {}).get('scenario', 'northern-realms')
    scenario = SCENARIOS.get(scenario_id, SCENARIOS['northern-realms'])
    
    narratives = [
        f"You {action.lower()}, taking in the atmosphere of {scenario['setting']}. The world around you feels alive with possibility and hidden dangers.",
        f"As you {action.lower()}, you notice details that others might miss. Your training has taught you to be observant and patient.",
        f"Your decision to {action.lower()} leads you deeper into the mysteries of this place. Each step brings new questions."
    ]
    
    return random.choice(narratives)

def advance_time(game_state):
    """Advance the time of day and potentially the date"""
    time_periods = ['Morning', 'Afternoon', 'Evening', 'Night']
    current_period = game_state.get('timePeriod', 'Morning')
    
    try:
        current_index = time_periods.index(current_period)
        next_index = (current_index + 1) % len(time_periods)
        game_state['timePeriod'] = time_periods[next_index]
        
        # If we've cycled back to morning, advance the day
        if next_index == 0:
            game_state['currentDay'] += 1
            
    except ValueError:
        game_state['timePeriod'] = 'Morning'

if __name__ == '__main__':
    app.run(debug=True, port=5000) 