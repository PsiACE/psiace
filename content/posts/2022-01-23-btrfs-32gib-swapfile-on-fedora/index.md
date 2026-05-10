+++
title = "Creating a 32GiB Swapfile for Btrfs on Fedora"
description = "A note on creating a 32GiB swapfile on Fedora with Btrfs."
date = 2022-01-23
slug = "btrfs-32gib-swapfile-on-fedora"

[taxonomies]
tags = ["2022", "Databend", "Btrfs", "Swapfile", "Fedora", "Linux", "Notes"]

[extra]
lang = "en"
+++

Inspired by [Databend - set swap to 10G](https://github.com/datafuselabs/databend/pull/3946), I checked the swap on my laptop and found only about 8G of zram.

```shell
[psiace@fedora ~]$ swapon -s
Filename        Type       Size       Used    Priority
/dev/zram0      partition  8388604    0       100
```

Well, that is probably why I could not smoothly finish the grcov-limited unit tests. We had discussed earlier that it was likely OOM. Following the principle of "bigger is better, more is beautiful", I decided to double down and add a 32 GiB swapfile.

## Initializing a Btrfs-Specific Swapfile

Btrfs has only supported swapfiles since kernel 5.0, and it comes with several special requirements:

- The swapfile cannot be placed on a snapshotted subvolume.
- Swapfiles on multi-device file systems are not supported.

So the correct approach is to create a non-snapshotted subvolume, then create a swapfile with compression disabled under that subvolume.

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

Note that these steps need to be completed under the system root directory to avoid permission and configuration issues.

## Setting the Swapfile as Part of Swap

A swapfile is an alternative to creating a dedicated swap partition. Its advantages are that it is easy to create, delete, and resize dynamically.

This approach is suitable when there is plenty of SSD space. It also happens to form a multi-level swap path of memory -> zram -> swapfile.

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

## Checking Swap Space and Enabling Automatic Mounting

After the previous two steps, I had nearly 40GiB of swap space. The next step was to check it and configure mounting.

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

## References

Funny enough, as a long-time Fedora user, most of the documentation I read comes from the Arch Wiki.

- https://wiki.archlinux.org/title/Improving_performance#zram_or_zswap
- https://wiki.archlinux.org/title/Btrfs#Swap_file
- https://wiki.archlinux.org/title/Swap#Swap_file_creation
- https://wiki.archlinux.org/title/Fstab

---

There are a few more small tricks for restraining OOM when compiling large Rust projects. Maybe I can turn those into a light post next time.

I was not slacking off!
