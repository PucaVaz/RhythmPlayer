import socket 
import struct

def get_data(data, data_types, jumps):
    return_dict = {}

    passed_data = data
    
    for i in data_types:
        d_type = data_types[i]
        jump = jumps[d_type]
        current = passed_data[:jump]

        decoded = 0
        if d_type == 's32':
            decoded = int.from_bytes(current, byteorder='little', signed=True)
        elif d_type == 'u32':
            decoded = int.from_bytes(current, byteorder='little', signed=False)
        elif d_type == 'f32':
            decoded = struct.unpack('f', current)[0]
        elif d_type == 'u16':
            decoded = struct.unpack('H', current)[0]
        elif d_type == 'u8':
            decoded = struct.unpack('B', current)[0]
        elif d_type == 's8':
            decoded = struct.unpack('b', current)[0]

        return_dict[i] = decoded
        passed_data = passed_data[jump:]

    return return_dict

def get_speed_data():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5605
    data_types = {}
    with open('data_format.txt', 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    jumps = {
        's32': 4,
        'u32': 4,
        'f32': 4,
        'u16': 2,
        'u8': 1,
        's8': 1,
        'hzn': 12
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1500)
        returned_data = get_data(data, data_types, jumps)
        
        # Assuming 'Speed' is the key for speed data in the dictionary
        if 'Speed' in returned_data:
            yield returned_data['Speed']

# Acho que agora funciona melhor, pedi muita ajuda ao chatgpt pq tava perdido em relação ao yield
