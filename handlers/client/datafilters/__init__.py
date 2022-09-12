import re


async def correct_name(name):
    name = name.split(" ")

    if len(name) == 2:
        for i in name:
            if not (i.istitle()) and (bool(re.search('[а-яА-Я]', i))):
                return False

    else:
        return False

    return True
