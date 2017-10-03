import socket
import struct
import subprocess
import threading
import commands
from hexdump import hexdump
import time
import sys
import os

class Pwn:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def sendline(self, data):
        self.send(data + '\n')

    def recvuntil(self, delim):
        ret = ""
        while True:
            ret += self.recv(1)
            if ret.endswith(delim):
                return ret

    def sendafter(self, data, delim):
        self.recvuntil(delim)
        self.send(data)

    def sendlineafter(self, data, delim):
        self.recvuntil(delim)
        self.sendline(data)

    def recvline(self):
        return self.recvuntil('\n')[:-1]

    def listener(self):
        while True:
            data = self.recv(1)
            if data:
                sys.stdout.write(data)
            else:
                print "\n*** Connection closed ***"
                break

    def interact(self):
        print "[*] Switching to interactive mode"
        t = threading.Thread(target = self.listener)
        t.start()
        time.sleep(0.1)
        print ""
        while t.is_alive():
            print "$",
            try:
                data = raw_input()
            except EOFError:
                self.close()
                break
            self.sendline(data)
            time.sleep(0.2)

class Remote(Pwn):
    def __init__(self, ip, port):
        self.sock = socket.create_connection((ip, port))

    def close(self):
        self.sock.shutdown(socket.SHUT_WR)

    def send(self,data):
        self.sock.sendall(data)
        time.sleep(0.03)

    def recv(self, n):
        return self.sock.recv(n)

class Local(Pwn):
    def __init__(self, args, env = {}):
        self.proc = subprocess.Popen(args, stdin = subprocess.PIPE, stdout = subprocess.PIPE, env = env)

    def close(self):
        self.proc.stdin.close()

    def send(self,data):
        self.proc.stdin.write(data)
        time.sleep(0.03)

    def recv(self, n):
        return self.proc.stdout.read(n)

def p32(x):
    return struct.pack('<I',x)

def u32(x):
    return struct.unpack('<I',x.ljust(4,'\0'))[0]

def p64(x):
    return struct.pack('<Q',x)

def u64(x):
    return struct.unpack('<Q',x.ljust(8,'\0'))[0]

def get_shellcode(name):
    try:
        with open(os.path.dirname(__file__) + '/shellcodes/' + name + '.asm', 'r') as f:
            if '32' in name:
                frmt = 'elf32'
            else:
                frmt = 'elf64'
            return asm(f.read(),frmt)
    except Exception:
        print "\n*** error: %s.asm does not exist ***" % name
        exit(0)

def run(cmd):
    return commands.getoutput(' '.join(cmd))

shellcodes = {}

def asm(code,frmt = 'elf64'):
    global shellcodes
    if code not in shellcodes:
        asmfile = 'tmp.asm'
        objfile = 'tmp.o'
        assembler = ['nasm', '-f', frmt, asmfile]
        objcopy = ['objcopy', '-j', '.text', '-O', 'binary', objfile]

        try:
            with open(asmfile,'wb') as f:
                f.write(code)
            run(assembler)
            run(objcopy)
            with open(objfile,'rb') as f:
                shellcodes[code] = f.read()
        except Exception:
            print "\n*** error: following shellcode can't be assemble. ***"
            print code
            return None
            # exit(1)
    return shellcodes[code]
