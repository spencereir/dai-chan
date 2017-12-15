from commands import random, general, admin, games, sound, fun

bot_names = ['dai', 'dai-chan', 'daichan', 'daiyousei', 'small cirno']

command_map = {
    'choose|pick': random.choose,
    'roll|calc|calculate': random.roll,
    'reorder|shuffle': random.reorder,
    'say': general.say
}

interactive_command_map = {
    'purge|delete': admin.purge,
    'connect four|connect4': games.connect_four,
    'music': sound.music,
    'title card|isaip': fun.title_card
}
