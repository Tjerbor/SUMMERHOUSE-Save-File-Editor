import json
import sys


# default [-5.0,-17.5 (or -20.0)]
def zoom_json(filepath, z):
    with open(filepath, 'r') as json_data:
        data = json.load(json_data)

    data['cameraPos']['z'] = z

    with open(filepath, 'w') as json_data:
        json_data.write(json.dumps(data))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            zoom_json(f"saveFile{sys.argv[1]}.json", float(sys.argv[2]))
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    else:
        print(f"Illegal amount of arguments given. 2 expected, {len(sys.argv) - 1} given.")
