+++
title = "在 Fedora 上为 Btrfs 新建 32GiB Swapfile"
description = "在 Fedora 的 Btrfs 文件系统上创建 32GiB swapfile 的记录。"
date = 2022-01-23
slug = "btrfs-32gib-swapfile-on-fedora"

[taxonomies]
tags = ["2022", "Databend", "Btrfs", "Swapfile", "Fedora", "Linux", "Notes"]

[extra]
lang = "zh"
+++

受到 [Databend - set swap to 10G](https://github.com/datafuselabs/databend/pull/3946) 的感召，检查了一下自己本子的 Swap ，只有大概 8G 的 zram 。

```shell
[psiace@fedora ~]$ swapon -s
Filename        Type       Size       Used    Priority
/dev/zram0      partition  8388604    0       100
```

完蛋，不能顺利跑完 grcov 限定版 unit-test 的原因大概就在这里了（之前有讨论过是 OOM）。本着「大就是好，多就是美」的原则，决定给它来个超级加倍，再塞个 32 GiB 的 Swapfile 上去。

## Btrfs 限定之初始化 Swapfile

自 5.0 内核之后，Btrfs 才支持创建 Swapfile ，而且有一些特别的要求：

- Swapfile 不能放在 snapshotted subvolume （快照子卷）上。
- 不支持跨多设备文件系统上的 Swapfile 。

所以正确的做法是：新建一个 non-snapshotted subvolume ，然后在该子卷之下创建禁用压缩的 Swapfile 。

```shell
# Create a non-snapshotted subvolume.
[psiace@fedora /]$ sudo btrfs subvolume create swap
Create subvolume './swap'
# Enter the subvolume.
[psiace@fedora /]$ cd swap
# Create a zero-length swapfile.
[psiace@fedora swap]$ sudo truncate -s 0 ./swapfile
# Set the swapfile attribute to avoid copy-on-write.
[psiace@fedora swap]$ sudo chattr +C ./swapfile
# Disable compression.
[psiace@fedora swap]$ sudo btrfs property set ./swapfile compression none
```

注意，这些需要在系统根目录下完成，以避免权限问题和设置问题。

## 设定 Swapfile 作为 Swap 成分之一

Swapfile 是创建特定交换分区的一种替代方案，好处是方便创建和删除、也便于动态变更大小。

这种方案比较适合 SSD 空间充裕的情况。刚好可以组成一个 memory -> zram -> swapfile 的多级交换。

```shell
# Fill the swapfile to a suitable size, usually half of memory or close to memory size.
# This is only for fun, so I chose a huge 32GiB, which is admittedly wasteful.
[psiace@fedora swap]$ sudo dd if=/dev/zero of=./swapfile bs=1M count=32768 status=progress
33980153856 bytes (34 GB, 32 GiB) copied, 20 s, 1.7 GB/s
32768+0 records in
32768+0 records out
34359738368 bytes (34 GB, 32 GiB) copied, 21.2624 s, 1.6 GB/s
# Set correct permissions.
[psiace@fedora swap]$ sudo chmod 600 ./swapfile
# Format the swapfile as swap.
[psiace@fedora swap]$ sudo mkswap ./swapfile
Setting up swapspace version 1, size = 32 GiB (34359734272 bytes)
no label, UUID=2e48f371-62a9-487a-9613-382b386b2836
# Enable the swapfile and set its priority.
# Since zram has priority 100, set this to 50. After all, zram is much faster than a swapfile.
[psiace@fedora swap]$ sudo swapon --priority 50 ./swapfile
```

## 检查 Swap 空间并设置自动挂载

那么，经过之前两步，已经得到了接近 40GiB 的 Swap 空间，接下来就是检查一下，并设置挂载。

```shell
# Use free to check the overview.
[psiace@fedora ~]$ free -m
               total        used        free      shared  buff/cache   available
Mem:           15453        5206         290         109        9956        9808
Swap:          40959           2       40957
# Use swapon to check details.
[psiace@fedora ~]$ swapon -s
Filename        Type       Size       Used    Priority
/dev/zram0      partition  8388604    2560    100
/swap/swapfile  file       33554428   0       50
# Edit fstab and add an entry to mount it.
# The subvolume name must be included here. UUID is optional.
[psiace@fedora ~]$ sudo nano /etc/fstab
/swap/swapfile    none    swap    defaults    0    0
```

## 参考资料

笑死，一个多年 Fedora 用户看的文档大多都来自 Arch Wiki 。

- https://wiki.archlinux.org/title/Improving_performance#zram_or_zswap
- https://wiki.archlinux.org/title/Btrfs#Swap_file
- https://wiki.archlinux.org/title/Swap#Swap_file_creation
- https://wiki.archlinux.org/title/Fstab

---

克制 Rust 编译大型项目时 OOM 还有一些小技巧，也许下次可以水一点内容。

我没有摸鱼！（手动狗头）
