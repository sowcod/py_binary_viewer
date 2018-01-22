#-*- coding: utf-8 -*-

def print_binary(bindata) :
    # print header
    print('         ' + ' '.join(map(lambda x:'{:02X}'.format(x), range(16))))

    # split per 16 bytes
    maxlen = len(bindata)
    count = 0
    maxcount = int(maxlen / 16)
    while True :
        position = count * 16
        position_str = '{:08X}'.format(position)

        current = bindata[count*16: count*16 + 16]
        hexprint = ' '.join([''.join(d) for d in zip(*[iter(bytes.hex(current))]*2)])
        hexprint += '   ' * (16 - len(current))
        print(f'{position_str} {hexprint} {current}'.format())
        count += 1
        if count > maxcount:
            break

if __name__ == '__main__' :
    print_binary(b'''0123456789ABCDEF0123456789ABCD''')

