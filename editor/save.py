# -*- coding: utf-8 -*-
from textwrap import TextWrapper

FULL_START = chr(1)
THIRD_START = chr(2)
TEXT_END = chr(3)
MAX_X = 39 # characters
MAX_Y = 32 # characters
WRAPPER = TextWrapper(width=MAX_X)

REPLACE_SYMBOLS = {u"А":"A", u"Б":"v", u"В":"B", u"Г":"g", u"Д":"d",
                   u"Е":"E", u"Ё":"a", u"Ж":"j", u"З":"3", u"И":"i",
                   u"Й":"y", u"К":"K", u"Л":"l", u"М":"M", u"Н":"H",
                   u"О":"O", u"П":"p", u"Р":"P", u"С":"C", u"Т":"T",
                   u"У":"u", u"Ф":"f", u"Х":"X", u"Ц":"c", u"Ч":"t",
                   u"Ш":"o", u"Щ":"h", u"Ъ":"r", u"Ы":"s", u"Ь":"b",
                   u"Э":"e", u"Ю":"k", u"Я":"m"}
REPLACE_SYMBOLS_REVERT = dict((v, k) for k, v in {u"Б":"v", u"Г":"g", u"Д":"d",
                   u"Ё":"a", u"Ж":"j", u"И":"i",
                   u"Й":"y", u"Л":"l",
                   u"П":"p",
                   u"У":"u", u"Ф":"f", u"Ц":"c", u"Ч":"t",
                   u"Ш":"o", u"Щ":"h", u"Ъ":"r", u"Ы":"s", u"Ь":"b",
                   u"Э":"e", u"Ю":"k", u"Я":"m"}.iteritems())

def decode(contents):
    contents = u"".join([REPLACE_SYMBOLS_REVERT.get(x, x) for x in contents])
    if contents[12] == FULL_START:
        return {"sound":contents[:12], "image":contents[13:25], "single_resource":contents[25:]}
    elif contents[12] == THIRD_START:
        result = {"sound":contents[:12], "image":contents[13:25]}
        
        text = list(contents[25:])
        
        bigtext = ""
        while True:
            char = text.pop(0)
            if char == TEXT_END:
                break
            else:
                bigtext += char
        
        variants = []
        vartext = ""
        while len(text) > 0:
            char = text.pop(0)
            if char == TEXT_END:
                variants.append((vartext, "".join(text[:12])))
                vartext = ""
                del text[:12]
            else:
                vartext += char
        
        result["text"] = bigtext
        result["variants"] = variants
        
        return result
    else:
        return {}

def code_full(sound, image, next_file):
    return sound.split("/")[-1] + FULL_START + image.split("/")[-1] + next_file.split("/")[-1]

def code_third(sound, image, text, variant_tuples):
    string = sound.split("/")[-1] + THIRD_START + image.split("/")[-1] + "".join([REPLACE_SYMBOLS.get(x, x) for x in "\n".join(WRAPPER.wrap(text[:-1])).upper() if ord(REPLACE_SYMBOLS.get(x, x)) <= 127]) + TEXT_END
    for variant in variant_tuples if len(variant_tuples) == 1 else variant_tuples[:-1]:
        string += "".join([REPLACE_SYMBOLS.get(x, x) for x in variant[0].upper() if ord(REPLACE_SYMBOLS.get(x, x)) <= 127]) + TEXT_END + ("" if variant[1] == "pick scene" else variant[1].split("/")[-1])
    return string

def validate_full(sound, image, next_file):
    if len(image.split("/")[-1]) != 12:
        return False, "wrong image name"
    if len(image.split("/")[-1]) != 12:
        return False, "wrong image name"
    if next_file != "" and len(next_file.split("/")[-1]) != 12:
        return False, "wrong resource name"
    return True, ""

def validate_third(sound, image, text, variant_tuples):
    if len(WRAPPER.wrap(text)) > MAX_X:
        return False, "text is too big"
    if len(sound.split("/")[-1]) != 12:
        return False, "wrong soundtrack name"
    if len(image.split("/")[-1]) != 12:
        return False, "wrong image name"
    isLast = False
    for i, variant in enumerate(variant_tuples if len(variant_tuples) == 1 else variant_tuples[:-1]):
        if (i > 6):
            return False, "too many variants"
        if len(variant[0]) > MAX_X:
            return False, "variant'" + variant[0] + "' is too big"
        if isLast:
            return False, "cannot mix empty and not empty variants " + variant
        if variant[0] == "":
            isLast = True
        if variant[0] != "" and variant[1] == "pick scene":
            return False, "cannot use non-empty variant string with an empty resource file"
    return True, ""
