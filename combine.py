import copy
import json
import sys
from add_offset import add_offset


def combine(source_1: str, source_2: str, destination=None, alignment=None, source_2_x_offset=0.0,
            source_2_y_offset=0.0,
            source_2_z_offset=0.0):
    with open(source_1, 'r') as json_data_1:
        data_1 = json.load(json_data_1)

    with open(source_2, 'r') as json_data_2:
        data_2 = json.load(json_data_2)

    if (destination is None):
        destination = source_1
    if (alignment is None):
        data_2 = add_offset(data_2, source_2_x_offset, source_2_y_offset, source_2_z_offset)

    data_1['buildingBlocks'].extend(data_2['buildingBlocks'])

    with open(destination, 'w') as json_data:
        json_data.write(json.dumps(data_1))


if __name__ == '__main__':
    src1 = 'saveFile5.json'
    src2 = 'saveFile6.json'
    #dest = 'saveFile7.json'
    combine(src1, src2,source_2_x_offset=3)
