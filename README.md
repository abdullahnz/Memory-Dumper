# Memdump

Dump mapped memory regions of some process by pid.

## Usage

Use `-h` or `--help` argument.

```shell
usage: memdump.py [-h] -p PID [-o OUT] [-f]

Used for dump memory process.

optional arguments:
  -h, --help         show this help message and exit
  -p PID, --pid PID  select process id of the target
  -o OUT, --out OUT  select output file for dumped raw data (default: none)
  -f, --force        if maps/mem file is readable
```

Run with `sudo` or force argument if the user has read permissions to the `mem` and `maps` file.

```shell
$ sudo python3 memdump.py -p 6766
[00] 00005555a2ee3000 - 00005555a2ee4000 (1000)
[01] 00005555a30e3000 - 00005555a30e4000 (1000)
[02] 00005555a30e4000 - 00005555a30e5000 (1000)
[03] 00007f25ca3d9000 - 00007f25ca5c0000 (1e7000)
[04] 00007f25ca5c0000 - 00007f25ca7c0000 (200000)
[05] 00007f25ca7c0000 - 00007f25ca7c4000 (4000)
[06] 00007f25ca7c4000 - 00007f25ca7c6000 (2000)
[07] 00007f25ca7c6000 - 00007f25ca7ca000 (4000)
[08] 00007f25ca7ca000 - 00007f25ca7f3000 (29000)
[09] 00007f25ca9c2000 - 00007f25ca9c4000 (2000)
[10] 00007f25ca9f3000 - 00007f25ca9f4000 (1000)
[11] 00007f25ca9f4000 - 00007f25ca9f5000 (1000)
[12] 00007f25ca9f5000 - 00007f25ca9f6000 (1000)
[13] 00007ffdc5f70000 - 00007ffdc5f91000 (21000)
[14] 00007ffdc5ff6000 - 00007ffdc5ff9000 (3000)
[15] 00007ffdc5ff9000 - 00007ffdc5ffb000 (2000)
[16] ffffffffff600000 - ffffffffff601000 (1000)
[**] Select Region: 2
[**] Dump region: 
00005555a30e4000: 0000000000000000 00005555a30e4008 00007f25ca7c5760
00005555a30e4018: 0000000000000000 0000000000000000 0000000000000000
00005555a30e4ff0: 0000000000000000 0000000000000000 0000000000000000

[**] Saving into outfile 'out/raw_data.dump' : Done
```

Raw data in output file,

```sh
$ hd out/raw_data.dump 
00000000  00 00 00 00 00 00 00 00  08 40 0e a3 55 55 00 00  |.........@..UU..|
00000010  60 57 7c ca 25 7f 00 00  00 00 00 00 00 00 00 00  |`W|.%...........|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001000

```

## Requirements
- Run with `sudo` for accessing unreadable file.
- python version 3.x
