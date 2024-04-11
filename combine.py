import copy
import json
import sys
import re
import argparse
from collections import Counter
from add_offset import add_offset


def combine(source_1: str, source_2: str, destination: str, alignment=None, source_2_x_offset=0.0,
            source_2_y_offset=0.0,
            source_2_z_offset=0.0):
    with open(source_1, 'r') as json_data_1:
        data_1 = json.load(json_data_1)

    with open(source_2, 'r') as json_data_2:
        data_2 = json.load(json_data_2)

    if (alignment is not None):
        extremes = find_extremes(data_2)
        alignment_point = find_alignment_point(data_1)
        if 'l' in alignment:
            source_2_x_offset += alignment_point[0] - extremes[0]
        elif 'r' in alignment:
            source_2_x_offset += alignment_point[0] - extremes[1]
        if 'b' in alignment:
            source_2_y_offset += alignment_point[1] - extremes[2]
        elif 't' in alignment:
            source_2_y_offset += alignment_point[1] - extremes[3]
        if 'c' in alignment:
            source_2_z_offset += alignment_point[2] - extremes[4]
        elif 'f' in alignment:
            source_2_z_offset += alignment_point[2] - extremes[5]

    data_2 = add_offset(data_2, source_2_x_offset, source_2_y_offset, source_2_z_offset)
    print(f'Entire offset: (x,y,z) {source_2_x_offset} {source_2_y_offset} {source_2_z_offset}')

    data_1['buildingBlocks'].extend(data_2['buildingBlocks'])

    with open(destination, 'w') as json_data:
        json_data.write(json.dumps(data_1))


def find_extremes(json_decoded):
    left = json_decoded['buildingBlocks'][0]['position']['x']
    right = json_decoded['buildingBlocks'][0]['position']['x']
    down = json_decoded['buildingBlocks'][0]['position']['y']
    up = json_decoded['buildingBlocks'][0]['position']['y']
    close = json_decoded['buildingBlocks'][0]['position']['z']
    far = json_decoded['buildingBlocks'][0]['position']['z']

    for block in json_decoded['buildingBlocks']:
        block = block['position']
        left = min(left, block['x'])
        right = max(right, block['x'])
        down = min(down, block['y'])
        up = max(up, block['y'])
        close = min(close, block['z'])
        far = max(far, block['z'])

    return (left, right, down, up, close, far)


def find_alignment_point(json_decoded):
    # Only selects building blocks with the id 219
    blocks = [
        json_decoded['buildingBlocks'][i] for i in range(len(json_decoded['buildingBlocks'])) if
        json_decoded['buildingBlocks'][i]['blockID'] == 219
    ]
    coords = [
        (block['position']['x'],
         block['position']['y'],
         block['position']['z']
         ) for block in blocks]
    result = Counter(coords)
    keys = result.keys()
    stacks_of_three = []
    for i in keys:
        if (result[i] == 3):
            stacks_of_three.append(i)

    x = stacks_of_three[0][0]
    y = stacks_of_three[0][1]
    z = stacks_of_three[0][2]

    # removes the 3 alignment blocks
    deleted = 0
    for block in blocks:
        if block['position']['x'] == x and block['position']['y'] == y and block['position']['z'] == z:
            json_decoded['buildingBlocks'].remove(block)
            deleted += 1
        if deleted >= 3:
            break

    return stacks_of_three[0]


if __name__ == '__main__':
    arg_amount = [4, 5, 7, 8]
    if (len(sys.argv) in arg_amount):
        try:
            src1 = f'saveFile{sys.argv[1]}.json'
            src2 = f'saveFile{sys.argv[2]}.json'
            dest = f'saveFile{sys.argv[3]}.json'
            if len(sys.argv) == 4:
                combine(src1, src2, dest)
            elif len(sys.argv) == 7:
                combine(src1, src2, dest,
                        source_2_x_offset=float(sys.argv[4]),
                        source_2_y_offset=float(sys.argv[5]),
                        source_2_z_offset=float(sys.argv[6])
                        )
            else:
                if (re.match("^(l|r)?(b|t)?(c|f)?$", sys.argv[4])):
                    if len(sys.argv) == 5:
                        combine(src1, src2, dest, sys.argv[4])
                    elif len(sys.argv) == 8:
                        combine(src1, src2, dest, sys.argv[4],
                                source_2_x_offset=float(sys.argv[5]),
                                source_2_y_offset=float(sys.argv[6]),
                                source_2_z_offset=float(sys.argv[7])
                                )
                else:
                    print("Illegal alignment string")
        except  Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    else:
        print("Illegal amount of arguments given")
