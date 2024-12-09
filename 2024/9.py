
from heapq import *

data = open("input-9-test.txt").read().strip()
data = open("input-9.txt").read().strip()
#data = "12345"

def print_blocks(blocks):
    if False:
        print("".join("." if b is None else str(b) if b < 10 else f"[{b}]" for b in blocks))

def do_part(part):
    is_file = True
    blocks = []
    # Index is size of free area, value is heap of indexes.
    free_areas = [[] for i in range(10)]
    file_id = 0
    files = []
    for ch in data:
        size = int(ch)
        if is_file:
            files.append( (file_id, len(blocks), size) )
        else:
            free_areas[size].append(len(blocks))
        blocks.extend([file_id if is_file else None]*size)
        if is_file:
            file_id += 1
        is_file = not is_file
    for i in range(len(free_areas)):
        heapify(free_areas[i])
    print_blocks(blocks)

    if part == 1:
        last = len(blocks) - 1
        for i, file_id in enumerate(blocks):
            if file_id is None:
                while last > i and blocks[last] is None:
                    last -= 1
                if last > i:
                    file_id = blocks[last]
                    blocks[i] = file_id
                    blocks[last] = None
    else:
        for file_id, file_pos, file_size in reversed(files):
            possible_areas = []
            for area_size in range(file_size, len(free_areas)):
                if len(free_areas[area_size]) > 0:
                    possible_areas.append( (free_areas[area_size][0], area_size) )
            if possible_areas:
                free_pos, free_size = sorted(possible_areas)[0]
                if free_pos < file_pos:
                    blocks[file_pos:file_pos + file_size] = [None]*file_size
                    blocks[free_pos:free_pos + file_size] = [file_id]*file_size
                    heappop(free_areas[free_size])
                    free_pos += file_size
                    free_size -= file_size
                    if free_size > 0:
                        heappush(free_areas[free_size], free_pos)

    print_blocks(blocks)

    checksum = sum(i*file_id for i, file_id in enumerate(blocks) if file_id is not None)

    print(f"Part {part}: {checksum}")

do_part(1)
do_part(2)
