
from functools import *

bits = bin(int(open("input-16.txt").read().strip(), 16))[2:]
while len(bits) % 4 != 0:
    bits = "0" + bits

pos = 0

def get_bits(n):
    global pos
    b = bits[pos:pos + n]
    pos += n
    return int(b, 2)

def parse_packet():
    version_number = get_bits(3)
    packet_type = get_bits(3)
    if packet_type == 4:
        value = 0
        more = True
        while more:
            more = get_bits(1)
            value = (value << 4) + get_bits(4)
        return value
    else:
        values = []
        if get_bits(1) == 1:
            values.extend(parse_packet() for i in range(get_bits(11)))
        else:
            packet_sublength = get_bits(15)
            end_pos = pos + packet_sublength
            while pos < end_pos:
                values.append(parse_packet())

        if packet_type == 0: return sum(values)
        elif packet_type == 1: return reduce(lambda acc, x: acc*x, values, 1)
        elif packet_type == 2: return min(values)
        elif packet_type == 3: return max(values)
        elif packet_type == 5: return 1 if values[0] > values[1] else 0
        elif packet_type == 6: return 1 if values[0] < values[1] else 0
        elif packet_type == 7: return 1 if values[0] == values[1] else 0

print(parse_packet())

