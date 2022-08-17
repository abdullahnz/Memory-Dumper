#!/usr/bin/python3

from struct import pack, unpack
import argparse, os

class Memdump:
    def __init__(self, pid):
        self.maps_path = f'/proc/{pid}/maps'
        self.mem_path  = f'/proc/{pid}/mem'
    
    def read_maps(self):
        maps = open(self.maps_path).read()
        maps = maps.splitlines()

        result = {}

        for index in range(len(maps)):
            region     = maps[index].split()[0]
            start, end = map(lambda x: int(x, 16), region.split('-'))
            result[index] = {
                'start'  : start,
                'length' : end - start
            }
        return result

    def dump_region(self, address, length):
        with open(self.mem_path, 'rb') as f:
            f.seek(address)
            data = f.read(length)
            f.close()
        return data

    def parsed_data_info(self, raw_data, address):
        print('[**] Dump region: ')
        current = 0
        
        for offset in range(0, len(raw_data), 8*3):
            skip = False
            data = [unpack("Q", raw_data[i:i+8].ljust(8, b'\0'))[0] for i in range(offset, offset + (8*3), 8)]
            if data != current:
                skip = True
                print(f'{address+offset:016x}: {data[0]:016x} {data[1]:016x} {data[2]:016x}')
            current = data
        
        if not skip:
            print(f'{address+offset:016x}: {data[0]:016x} {data[1]:016x} {data[2]:016x}')

    def error(self, message):
        print(f'memdump.py: error: {message}')
        exit(1)

    def dump(self, outfile='raw_data.dump'):
        mapping_address = self.read_maps()

        for i in range(len(mapping_address)):
            maps = mapping_address[i]
            end  = maps['start'] + maps['length']
            print(f'[{i:02d}] {maps["start"]:016x} - {end:016x} ({maps["length"]:x})')

        index    = int(input('[**] Select Region: '))
        maps     = mapping_address[index]
        raw_data = self.dump_region(maps['start'], maps['length'])
        
        outfile  = f'out/{outfile}'
        
        self.parsed_data_info(raw_data, maps['start'])
        
        if 'out' not in os.listdir('.'):
            os.mkdir('out')
            
        print(f'\n[**] Saving into outfile \'{outfile}\' : ', end='')

        with open(outfile, 'wb') as f:
            f.write(raw_data)
            f.close()
            
        print('Done')

if __name__ == "__main__":
    # Init some argument parser.
    parser = argparse.ArgumentParser(description='Used for dump memory process.')
    parser.add_argument('-p', '--pid', action='store', type=int, required=True, help='select process id of the target')
    parser.add_argument('-o', '--out', action='store', type=str, help='select output file for dumped raw data (default: none)')
    parser.add_argument('-f', '--force', action='store_true', help='if maps/mem file is readable')
    args = parser.parse_args()

    # Memdump class.
    process = Memdump(args.pid)
    
    # Check privilege to access unreadable file.
    if not args.force:
        if os.getuid() != 0:
            process.error(f'this script needs accessing an unreadable file, so try with sudo or with \'force\' argument.')
    try:
        if args.out:
            process.dump(outfile=args.out)
        else:
            process.dump()
    
    except FileNotFoundError:
        process.error(f'there is no such process for id: {args.pid}')

    except PermissionError as e:
        process.error(f'try run this script with sudo (permission denied).')

    