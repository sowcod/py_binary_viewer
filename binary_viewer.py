#-*- coding: utf-8 -*-

import io
import typing
import sys
import unicodedata
import codecs

replacement_escape = str.maketrans('\'\"\a\b\f\n\r\t\v', '         ')

def replace_error_bytes(ex):
    return (chr(65533) * (ex.end - ex.start), ex.end)

codecs.register_error('binary_viewer.replace_error_bytes', replace_error_bytes)

ByteType = typing.TypeVar('ByteType', bytes, io.BufferedIOBase)
def to_bytestream(bindata : ByteType) -> io.BufferedIOBase:
    if isinstance(bindata, io.BufferedIOBase) :
        return bindata
    else:
        return io.BytesIO(bindata)

def to_bytes(bindata : ByteType) -> bytes:
    if isinstance(bindata, io.BufferedIOBase) :
        return bindata.read()
    else:
        return bindata

def binary_to_text(bindata : ByteType, encoding : str = 'utf-8') -> str :
    data = to_bytes(bindata)

    # if encoding is defaul then use default
    use_encoding = encoding if encoding is not None else sys.getdefaultencoding()

    # replace escape sequence and error byte to 1 char
    encoded_str = data.decode(encoding,
            errors='binary_viewer.replace_error_bytes').translate(replacement_escape)

    result_str = ''

    bytepos = 0
    for char in encoded_str:
        reencoded = char.encode(encoding)

        # check by east_asian_width
        if unicodedata.east_asian_width(char) in ('F','W','A') :
            # if wide character
            # get actual byte size
            if reencoded == data[bytepos:bytepos+len(reencoded)] :
                bytesize = len(reencoded)
            else:
                # if replaced character then set bytesize to 1 force
                bytesize = 1

            # insert after char until fulfill bytes
            result_str += char + ' ' * (bytesize - 2)
        else:
            # if narrow character
            # get actual byte size
            bytesize = len(reencoded)

            # insert after char until fulfill bytes
            result_str += char + ' ' * (bytesize - 1)

        bytepos += bytesize

    return result_str

def print_binary(bindata : ByteType) -> None:
    stream = to_bytestream(bindata)

    # print header
    print('          ' + ' '.join(map(lambda x:'{:02X}'.format(x), range(16))) + '  0123456789ABCDEF')
    print('-' * 75)
    position = 0
    while True :
        position_str = '{:08X}'.format(position)

        current = stream.read(16)
        if len(current) == 0 : break

        hexprint = ' '.join([''.join(d) for d in zip(*[iter(bytes.hex(current))]*2)])
        hexprint += '   ' * (16 - len(current))

        current_str = binary_to_text(current)
        print(f'{position_str}  {hexprint}  {current_str}'.format())
        position += 16

if __name__ == '__main__' :
    test_bin = '0123456789ABCDEFあいえお\t'.encode('utf-8') + b'\x80\x81\\'
    test_bin += 'あいうえおかきくけこさしすせそ'.encode('utf-8')
    print_binary(test_bin)

