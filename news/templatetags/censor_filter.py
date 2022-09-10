from django import template

register = template.Library()


@register.filter
def censor(parser: str, token='one'):
    words = parser.split()
    token = token.lower()
    good_word = []
    for word in words:
        lower = word.lower()
        if token == lower:
            rep = lower.replace(token, word[0] + '*' * len(token[1:]))
            good_word.append(rep)
        else:
            good_word.append(word)
    return ' '.join(good_word)
