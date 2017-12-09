import re

async def option_call(f, message, client=None):
    f_kwargs = {}
    while (re.search(r'^(.*)--([a-zA-Z0-9_]+)(.*)$', message.content)):
        m = re.search(r'^(.*)--([a-zA-Z0-9_]+)(.*)$', message.content)
        f_kwargs[m.group(2)] = True
        message.content = re.sub(' --{}$'.format(m.group(2)), '', message.content)
        message.content = message.content.replace('--{} '.format(m.group(2)), '')

    if client:
        await f(message, client, **f_kwargs)
    else:
        return f(message, **f_kwargs)
