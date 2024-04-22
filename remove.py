import json
import sys


def remove_blocks(json_decoded, block_IDs):
    initial = len(json_decoded['buildingBlocks'])
    blocks = [
        json_decoded['buildingBlocks'][i] for i in range(initial)
        if json_decoded['buildingBlocks'][i]['blockID'] not in block_IDs
    ]
    json_decoded['buildingBlocks'] = blocks
    print(f"{initial - len(blocks)} blocks removed.")

    return json_decoded


def remove_blocks_json(filepath, block_IDs):
    with open(filepath, 'r') as json_data:
        data = json.load(json_data)

    data = remove_blocks(data, block_IDs)

    with open(filepath, 'w') as json_data:
        json_data.write(json.dumps(data))


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        try:
            removed = []
            for id in sys.argv[2:]:
                removed.append(int(id))

            remove_blocks_json(f'saveFile{sys.argv[1]}.json', removed)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    else:
        print("Illegal amount of arguments given. Save file number and at least 1 blockID must be specified.")
