+++
title = "Running MASM Assembly on Linux"
description = "Setting up a MASM learning environment on Linux with DOSBox and MASM 5.x."
date = 2018-09-06
slug = "masm-on-linux"

[taxonomies]
tags = ["MASM", "Assembly", "Linux", "DOSBox"]

[extra]
lang = "en"
+++

When using assembly on Linux, NASM or GNU AS is undoubtedly much more convenient. However, many domestic courses still use MASM for lectures and assignments, so we need to configure a learning environment for classroom needs.

First, install DOSBox with your favorite package manager, for example `sudo dnf install dosbox`. DOSBox is a DOS emulator built with the SDL library, and it can recreate an MS-DOS-compatible environment.

Second, prepare the MASM software you will use. Usually, the teacher will provide a MASM 5.0 lab environment, including MASM.EXE, LINK.EXE, LIB.EXE, and CREF.EXE. This is one of the versions that can run in a DOS environment, so download it. Of course, you can also find another suitable MASM version yourself and locate these programs.

Next, put the programs you found, at least MASM.EXE, LINK.EXE, LIB.EXE, and CREF.EXE, into `~/.dosbox/MASM`. You need to create this directory under `.dosbox`. Then add the following content to the `[autoexec]` section in `~/.dosbox/dosbox-0.74.conf`:

```conf
[autoexec]
# Lines in this section will be run at startup.
# You can put your MOUNT lines here.
MOUNT c /home/yourusername/.dosbox/MASM
set PATH= %PATH%;c:\;
mount E /home/yourusername/asm
E:
```

The installation preparation is complete. Now it is time to test it.

Create `hello.asm` in the folder you chose for `.asm` files, and enter the hello world example:

```asm
assume cs:codes, ds:datas
datas segment
        str db 'hello,world',13,10,'$'
datas ends
codes segment
    start:
        mov ax, datas
        mov ds, ax
        lea dx, str
        mov ah, 9
        int 21h
        mov ah, 4ch
        int 21h
codes ends
    end start
```

Open DOSBox and run `masm hello.asm`, `link hello.obj`, and `hello.exe` in sequence. If the configuration succeeds, the program will print `hello,world`, which means the MASM learning environment has been set up successfully.

---

Supplement on September 24:

About the configuration of `~/.dosbox/dosbox-0.74.conf`: `MOUNT c path/to/your/folder` specifies the location of the C drive, so it can be replaced with another path. `set PATH= %PATH%;c:\;` sets the environment variable.

About the DEBUG program: put it directly under the C drive directory, then enter `debug` to run it.

About downloads: related content can be found at <http://www.phatcode.net>. After downloading, extract it directly, then find the content you need and place it under the C drive.
