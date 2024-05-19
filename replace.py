import json
import sys


def replace_blocks(json_decoded, original_block_IDs, replace_block_ids):
    replaced = 0

    for block in json_decoded['buildingBlocks']:
        if block['blockID'] in original_block_IDs:
            replaced += 1
            index = original_block_IDs.index(block['blockID'])
            block['blockID'] = replace_block_ids[index]

    print(f"{replaced} blocks replaced.")

    return json_decoded


def replace_blocks_json(filepath, original_block_IDs, replace_block_ids):
    with open(filepath, 'r') as json_data:
        data = json.load(json_data)

    data = replace_blocks(data, original_block_IDs, replace_block_ids)

    with open(filepath, 'w') as json_data:
        json_data.write(json.dumps(data))


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        try:
            originals = []
            replacers = []

            for pair in sys.argv[2:]:
                curr = pair.split(",")
                originals.append(int(curr[0]))
                replacers.append(int(curr[1]))

            replace_blocks_json(f'saveFile{sys.argv[1]}.json', originals, replacers)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    else:
        print("Illegal amount of arguments given. Save file number and at least 1 blockID,replaceID pair must be specified.")
