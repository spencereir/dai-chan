import random
from logger import logger

in_game = {}

def pname(p):
    if hasattr(p, 'nick') and p.nick:
        return p.nick
    return p.name

async def init_game(message, client, num_players):
    if len(message.mentions) != num_players - 1:
        await client.send_message(message.channel, "Please mention another user to play the game with" 
                          if num_players == 2 else "Please mention {} other users to play the game with".format(num_players - 1))
        return

    for p in player:
        if in_game[p]:
            await client.send_message(message.channel, "{} is already in a game".format(pname(p)))
            return None

    player = [message.author] + message.mentions
    responses = []
    for m in message.mentions:
        await client.send_message(message.channel, "{}, do you accept {}'s challenge? (Y/N)".format(pname(m), pname(message.author)))
        resp = await client.wait_for_message(author=m, check=lambda x: x.content.lower() in ('yes', 'no', 'y', 'n')) 
        if resp.content.lower() in ('no', 'n'):
            await client.send_message(message.channel, "{} does not want to play right now.".format(pname(m)))
            return None

    random.shuffle(player)
    for p in player:
        in_game[p.id] = true
    return player

async def connect_four(message, client):
    if len(message.mentions) > 4:
        await client.send_message('Too many players. This connect 4 can be played with up to 5 players only')
    player = await init_game(message, client, len(message.mentions)+1)
    ap = 0
    rows = 2 + 2 * len(player)
    cols = min(10, 5 + len(player))
    board = [[0 for x in range(cols)] for y in range(rows)]
    last_msg = None
    token = [':white_circle:', ':red_circle:', ':large_blue_circle:', ':green_apple:', ':yellow_heart:', ':large_orange_diamond:']
    bottom_text = ' '.join([':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':keycap_ten:'][:cols])
    moves = 0
    if not player:
        return

    logger.log_msg('INFO', 'Starting connect four game between {} and {}'.format(pname(player[0]), pname(player[1])))

    
    while True:
        win = False
        for i in range(rows):
            for j in range(cols):
                if board[i][j] != 0:
                    horz = True
                    vert = True 
                    d1 = True 
                    d2 = True
                    for k in range(1, 4):
                        horz &= (j + k < cols and board[i][j+k] == board[i][j])
                        vert &= (i + k < rows and board[i+k][j] == board[i][j])
                        d1 &= (j + k < cols and i + k < rows and board[i+k][j+k] == board[i][j])
                        d2 &= (j + k >= 0 and i + k < rows and board[i+k][j-k] == board[i][j])
                    if horz or vert or d1 or d2:
                        win = True
    
        if last_msg:
            await client.delete_message(last_msg)
        m = ""
        for x in board:
            for y in x:
                m += token[y] + ' '
            m += '\n'
        m += bottom_text + '\n'
        
        if win:
            await client.send_message(message.channel, m)
            await client.send_message(message.channel, '{} wins!'.format(pname(player[(ap+len(player)-1)%len(player)])))
            return
        else:
            m += '{}, it is your turn!'.format(pname(player[ap]))
        
        last_msg = await client.send_message(message.channel, m)

        if moves == rows * cols:
            await client.send_message(message.channel, "Draw!")
            return

        msg = await client.wait_for_message(author=player[ap], check = lambda x: x.content.isdigit() 
                                                                        and int(x.content) >= 1 and int(x.content) <= cols
                                                                        and board[0][int(x.content)-1] == 0)
        move = int(msg.content)-1
        try:
            await client.delete_message(msg)
        except:
            pass

        y = rows-1
        while board[y][move] != 0:
            y -= 1
        board[y][move] = ap+1
        moves += 1
        ap = (ap + 1) % len(player)
