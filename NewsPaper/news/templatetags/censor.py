from django import template

register = template.Library()


@register.filter()
def censor(value: str) -> str:
    """Цензурирует переданное строковое значение, если оно начинается с верхнего регистра.
    Например, "Привет" -> "П*****"."""
    if not isinstance(value, str):
        raise TypeError('Значение должно быть строкой.')

    temp = []
    parts = value.split()

    for part in parts:
        if part.istitle():
            temp.append(f'{part[0]}{"*" * len(part[1:])}')
        else:
            temp.append(part)

    return ' '.join(temp)


if __name__ == '__main__':
    test_str = 'Hello friend! Pleased to meet you!'
    assert censor(test_str) == 'H**** friend! P****** to meet you!'

    not_str = 123
    assert censor(not_str) == '***'