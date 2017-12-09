import random

in_game = {}

def pname(p):
    if hasattr(p, 'nick') and p.nick:
        return p.nick
    return p.name

async def connect_four(message, client):
    if len(message.mentions) != 1:
        await client.send_message(message.channel, "Please mention another user to play the game with")
        return

    player = [message.author, message.mentions[0]]
    await client.send_message(message.channel, "{}, do you accept {}'s challenge? (Y/N)".format(pname(player[1]), pname(player[0])))
    msg = await client.wait_for_message(author=player[1], check = lambda x: x.content.lower() in ('yes', 'no', 'y', 'n'))
    if msg.content.lower() in ('no', 'n'):
        await client.send_message(message.channel, "{} does not want to play right now.")
        return

    random.shuffle(player)
    ap = 0
    board = [[2 for x in range(7)] for y in range(6)]
    last_msg = None

    while True:
        win = False
        for i in range(6):
            for j in range(7):
                if board[i][j] != 2:
                    horz = True
                    vert = True 
                    d1 = True 
                    d2 = True
                    for k in range(1, 4):
                        horz &= (j + k < 7 and board[i][j+k] == board[i][j])
                        vert &= (i + k < 6 and board[i+k][j] == board[i][j])
                        d1 &= (j + k < 7 and i + k < 6 and board[i+k][j+k] == board[i][j])
                        d2 &= (j + k >= 0 and i + k < 6 and board[i+k][j-k] == board[i][j])
                    if horz or vert or d1 or d2:
                        win = True
    
        if last_msg:
            await client.delete_message(last_msg)
        m = ""
        for x in board:
            for y in x:
                m += (':white_circle:' if y == 2 else ':red_circle:' if y == 0 else ':large_blue_circle:') + ' '
            m += '\n'
        m += ':one: :two: :three: :four: :five: :six: :seven:\n'
        
        if win:
            await client.send_message(message.channel, m)
            await client.send_message(message.channel, '{} wins!'.format(pname(player[ap^1])))
            return
        else:
            m += '{}, it is your turn!'.format(pname(player[ap]))
        
        last_msg = await client.send_message(message.channel, m)

        msg = await client.wait_for_message(author=player[ap], check = lambda x: x.content.isdigit() 
                                                                        and int(x.content) >= 1 and int(x.content) <= 7
                                                                        and board[0][int(x.content)-1] == 2)
        move = int(msg.content)-1
        try:
            await client.delete_message(msg)
        except:
            pass

        y = 5
        while board[y][move] != 2:
            y -= 1
        board[y][move] = ap
        ap ^= 1
