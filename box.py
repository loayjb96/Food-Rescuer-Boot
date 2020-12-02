UL, UR = '╔', '╗'
SL, SR = '╠', '║'
DL, DR = '╚', '╝'
AL, AR = '═', '>'


def padded(
        line, info=None, width=30, intro='>', outro='<', filler='.', chopped='..'
):
    # cleanup input
    line = ''.join([' ', line.strip()]) if line else ''
    info = info.strip() if info else ''

    # determine available width
    width -= sum([len(intro), len(outro), len(line), len(info)])
    if width < 0:
        # chop off overflowing text
        line = line[:len(line) + width]
        if chopped:
            # place chopped characters (if set)
            chopped = chopped.strip()
            line = ' '.join([line[:len(line) - (len(chopped) + 1)], chopped])

    return ''.join(e for e in [
        intro,
        info,
        line,
        ''.join(filler for _ in range(width)),
        outro
    ] if e)


def box(food_id, servings, food_types, distance, user_name, *extras):
    arrow = (AL + AR)
    res = [
        # head line
        padded(
            'food no. {:03d} <'.format(food_id), (AL + AL + arrow),
            intro=UL, outro=UR, filler=AL
        ),
        # first line
        padded(
            'Number of servings: {:3d}'.format(servings), arrow,
            intro=SL, outro=' ', filler=' '
        ),
        padded(
            'food types. ' + food_types, arrow,
            intro=SL, outro=' ', filler=' '
        ),
        padded(
            'Contact: ' + user_name, arrow,
            intro=SL, outro=' ', filler=' '
        ),
        padded(
            'Distance: ' + distance + 'Km', arrow,
            intro=SL, outro=' ', filler=' '
        ),

    ]
    # following lines
    res.extend(padded(e, arrow, intro=SL, outro=SR, filler=' ') for e in extras)
    # bottom line
    res.append(padded(None, None, intro=DL, outro=DR, filler=AL))

    return '\n'.join(res)

# print(
#     box(485, 3, 'Fumatori', 'Televisione')
# )
# print(
#     box(123, 4, 'Fumatori', 'Televisione', 'Aria Condizionata')
# )
# print(
#     box(1, 1, 'this is so much text it will be chopped off')
# )
