import random
import re
from logger import logger

def split(message):
    return (message.split('|') if '|' in message else [x for x in message.split(' ') if x != ''])

def choose(message):
    m = split(message.content)
    return m[random.randrange(0, len(m))]

def reorder(message):
    m = split(message.content)
    random.shuffle(m)
    return ' '.join(m)

def swroll(msg, **kwargs):
    roll(msg, starwars=True, **kwargs)

def roll(msg, show_rolls=False, shadowrun=False, starwars=False):
    message = msg.content
    try:
        if starwars:
            swdice = {}
            swdice['b'] = [" ", " ", "S", "S|A", "A|A", "A"]
            swdice['s'] = [" ", " ", "F", "F", "T", "T"]
            swdice['a'] = [" ", "S", "S", "S|S", "A", "A", "S|A", "A|A"]
            swdice['d'] = [" ", "F", "F|F", "T", "T", "T", "T|T", "F|T"]
            swdice['p'] = [" ", "S", "S", "S|S", "S|S", "A", "S|A", "S|A", "S|A", "A|A", "A|A", "TRI"]
            swdice['c']= [" ", "F", "F", "F|F", "F|F", "T", "T", "F|T", "F|T", "T|T", "T|T", "DSP"]
            swdice['f'] = ["D", "D", "D", "D", "D", "D", "DD", "L", "L", "LL", "LL", "LL"]
            res = ""
            for c in message:
                res += "[{}] ".format(swdice[c][random.randrange(0, len(swdice[c]))])
            num_s = res.count('S')
            num_a = res.count('A')
            num_f = res.count('F')
            num_t = res.count('T') - res.count('TRI')
            num_tri = res.count('TRI')
            num_dsp = res.count('DSP')
            num_d = res.count('D') - res.count('DSP')
            num_l = res.count('L')
            return "{}\nSuccesses: {}, Failures: {}\nTriumphs: {}, Despairs: {}\n, Advantages: {}, Threats: {}\nDark Side: {}, Light Side: {}".format(res, num_s, num_f, num_tri, num_dsp, num_a, num_t, num_d, num_l)

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
            logger.log_msg('Failed to parse {} => {} as a math expression'.format(msg.content, message))
            return 'I couldn\'t parse `{}`'.format(message)
    except:
        logger.log_msg('Failed to parse {} => {} as a math expression'.format(msg.content, message))
        return 'I couldn\'t parse `{}`'.format(message)
