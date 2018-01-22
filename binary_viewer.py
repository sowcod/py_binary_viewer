#-*- coding: utf-8 -*-

import io

def print_binary(bindata) :
    if isinstance(bindata, io.BufferedIOBase) :
        stream = bindata
    else:
        stream = io.BytesIO(bindata)

    # print header
    print('         ' + ' '.join(map(lambda x:'{:02X}'.format(x), range(16))))

    # read per 16 bytes
    position = 0
    while True :
        position_str = '{:08X}'.format(position)

        current = stream.read(16)
        if len(current) == 0 : break

        hexprint = ' '.join([''.join(d) for d in zip(*[iter(bytes.hex(current))]*2)])
        hexprint += '   ' * (16 - len(current))
        print(f'{position_str} {hexprint} {current}'.format())
        position += 16

if __name__ == '__main__' :
    print_binary(b'''0123456789ABCDEF0123456789ABCD''')

