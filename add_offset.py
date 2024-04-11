import json
import sys


def add_offset(json_decoded, x_offset, y_offset, z_offset):
    for block in json_decoded['buildingBlocks']:
        block = block['position']
        block['x'] += x_offset
        block['y'] += y_offset
        block['z'] += z_offset
    return json_decoded


# X (left:'-', right:'+')
# Y (down:'-', up:'+')
# Z (closer:'-', farther:'+')
def add_offset_json(filepath, x_offset, y_offset, z_offset):
    json_file = filepath

    with open(json_file, 'r') as json_data:
        data = json.load(json_data)

    data = add_offset(data, x_offset, y_offset, z_offset)

    with open(json_file, 'w') as json_data:
        json_data.write(json.dumps(data))


if __name__ == '__main__':
    if (len(sys.argv) == 5):
        try:
            add_offset_json(f"saveFile{sys.argv[1]}.json", float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
        except  Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    else:
        print(f'Illegal amount of arguments given. 4 excpected, {len(sys.argv) - 1} given.')
