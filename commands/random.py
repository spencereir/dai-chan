import random
import re

def split(message):
    return (message.split('|') if '|' in message else [x for x in message.split(' ') if x != ''])

def choose(message):
    m = split(message.content)
    return m[random.randrange(0, len(m))]

def reorder(message):
    m = split(message.content)
    random.shuffle(m)
    return ' '.join(m)

def roll(msg, show_rolls=False, shadowrun=False):
    message = msg.content
    try:
        all_rolls = []
        while (re.search(r'(\d+)d(\d+)', message)):
            m = re.search(r'(\d+)d(\d+)', message)
            num_dice = int(m.group(1))
            dice_val = int(m.group(2))
            if num_dice >= 1000:
                return 'Let\'s not'
            rolls = [random.randrange(1, dice_val+1) for i in range(num_dice)]
            all_rolls.extend(rolls)
            message = message.replace(m.group(), str(sum(rolls)), 1)

        successes = 0
        if show_rolls or shadowrun:
            all_rolls = map(str, sorted(all_rolls))
        if shadowrun:
            all_rolls = ['**{}**'.format(x) if int(x) >= 5 else x for x in all_rolls]
            successes = sum([1 if x[0]=='*' else 0 for x in all_rolls])
        
        if re.match(r'^[0-9\+\-\*\/\>\<\(\) ]+$', message):
            if shadowrun:
                return '{} ({})'.format(successes, ', '.join(all_rolls))
            if show_rolls:
                return '{} ({})'.format(eval(message), ', '.join(all_rolls))
            else:
                return str(eval(message))
        else:
            return 'I couldn\'t parse `{}`'.format(message)
    except OSError:
        return 'I couldn\'t parse `{}`'.format(message)
