+++
title = "在 Linux 上运行 MASM 汇编"
description = "在 Linux 环境下通过 DOSBox 和 MASM 5.x 配置 MASM 学习环境。"
date = 2018-09-06
slug = "masm-on-linux"

[taxonomies]
tags = ["MASM", "Assembly", "Linux", "DOSBox"]

[extra]
lang = "zh"
+++

在 Linux 环境下使用汇编，使用 NASM 或是 GNU AS 无疑会方便很多，但国内的课程大多采用 MASM 进行讲解和作业，为了适应课堂需要，我们需要配置学习环境。

首先，使用最喜欢的包管理工具安装 DOSBox，例如 `sudo dnf install dosbox`。该软件是一个使用 SDL 库的 DOS 模拟程序，可以再现一个 MS-DOS 兼容环境。

其次，你需要准备使用的 MASM 软件，通常情况下，教师会为你提供 MASM 5.0 上机学习环境（包括 MASM.EXE LINK.EXE LIB.EXE 以及 CREF.EXE），这是可以在 DOS 环境下运行的几个版本之一，请下载它。当然你也可以自行寻找其它合适版本的 MASM，并找出这些程序。

接下来，把你找到的程序（至少包括 MASM.EXE LINK.EXE LIB.EXE 以及 CREF.EXE）放入 `~/.dosbox/MASM` 之中（需要在 `.dosbox` 下新建），然后在 `~/.dosbox/dosbox-0.74.conf` 中的 `[autoexec]` 部分录入：

```conf
[autoexec]
# Lines in this section will be run at startup.
# You can put your MOUNT lines here.
MOUNT c /home/yourusername/.dosbox/MASM
set PATH= %PATH%;c:\;
mount E /home/yourusername/asm
E:
```

好了，我们的安装准备已经完成，接下来是测试时间。

在你上面选择存放 `.asm` 的文件中新建 `hello.asm`，将 hello world 例程录入：

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

打开 DOSBox，在命令行依次执行 `masm hello.asm`、`link hello.obj` 以及 `hello.exe`。如果配置成功，程序会输出 `hello,world`，这意味着我们的 MASM 学习环境已经配置成功了。

---

9 月 24 日补充：

关于 `~/.dosbox/dosbox-0.74.conf` 的设置：`MOUNT c path/to/your/folder` 是指定 C 盘的位置，所以完全可以用其他位置来代替。`set PATH= %PATH%;c:\;` 一句设定了环境变量。

关于 DEBUG 程序：直接放置到 C 盘目录之下即可，输入 `debug` 即可运行。

关于下载：可以在 <http://www.phatcode.net> 找到相关内容。下载后直接解压，然后找出你所需要的内容放置在 C 盘下即可。
