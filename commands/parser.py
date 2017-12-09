import re

def option_call(f, message):
    f_kwargs = {}
    while (re.search(r'^(.*)--([a-zA-Z0-9_]+)(.*)$', message)):
        m = re.search(r'^(.*)--([a-zA-Z0-9_]+)(.*)$', message)
        f_kwargs[m.group(2)] = True
        message = re.sub(' --{}$'.format(m.group(2)), '', message)
        message = message.replace('--{} '.format(m.group(2)), '')

    return f(message, **f_kwargs)
