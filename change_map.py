import json
import sys


def change_map(json_decoded, mapname):
    json_decoded['mapName'] = f'Environment {mapname}'
    return json_decoded


def change_map_json(filepath, mapname):
    json_file = filepath

    with open(json_file, 'r') as json_data:
        data = json.load(json_data)
    data = change_map(data, mapname)

    with open(json_file, 'w') as json_data:
        json_data.write(json.dumps(data))


if __name__ == '__main__':
    maps = ["Lake", "Grass", "City", "Desert"]
    if (len(sys.argv) == 3 and sys.argv[2] in maps):
        try:
            change_map_json(f"saveFile{sys.argv[1]}.json", sys.argv[2])
        except  Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)


    else:
        print(f"Illegal arguments given. First argument is the number of the save file. For the second argument only {maps} is accepted.")
