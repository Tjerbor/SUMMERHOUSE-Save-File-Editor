import json

def offset(json,x_offset,y_offset,z_offset):
    for block in json['buildingBlocks']:
        block = block['position']
        block['x'] += offset_x
        block['y'] += offset_y
        block['z'] += offset_z
    return json

if __name__ == '__main__':
    json_file = 'saveFile5.json'

    offset_x = 0.0 #(left:'-', right:'+')
    offset_y = 0.0 #(down:'-', up:'+')
    offset_z = 5.0 #(closer:'-', farther:'+')

    with open(json_file, 'r') as json_data:
        data = json.load(json_data)
    print(len(data['buildingBlocks']))

    index = -1
    data = offset(data,offset_x,offset_y,offset_z)


    with open(json_file, 'w') as json_data:
        json_data.write(json.dumps(data))