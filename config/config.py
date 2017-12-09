import commands

bot_names = ['dai', 'dai-chan', 'daichan', 'daiyousei', 'small cirno']

command_map = {
    'choose|pick': commands.random.choose,
    'roll|calc|calculate': commands.random.roll,
    'reorder|shuffle': commands.random.reorder,
    'say': commands.general.say
}

interactive_command_map = {
    'connect four|connect4': commands.games.connect_four,
    'music': commands.sound.music
}
