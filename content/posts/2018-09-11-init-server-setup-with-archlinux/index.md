+++
title = "Initial Server Setup with Arch Linux"
description = "Creating an Arch Linux server with vps2arch and configuring SSH, users, sudo, and a basic firewall."
date = 2018-09-11
slug = "init-server-setup-with-archlinux"

[taxonomies]
tags = ["Arch Linux", "Server"]

[extra]
lang = "en"
+++

**The steps in this article were only verified on Alibaba Cloud, but they should also apply to other cloud service providers.**

## Part 0: Preface

I have just completed the process of ~~fully~~ migrating from the Red Hat family, Fedora and CentOS, to [Arch Linux](https://www.archlinux.org/). This is not exactly a very safe choice, because the Red Hat family has always been known for high reliability. Even Fedora, often called the testing ground, rarely crashes because of strange problems. However, as a rolling-release distribution, Arch Linux satisfies my curiosity about new things, and the Arch Wiki and AUR provided by the distribution are indeed worth loving.

After switching my desktop system to Manjaro Linux, an Arch Linux-based distribution that is easier to get started with, I began preparing to switch my Alibaba Cloud ECS instance to Arch Linux as well. There is a small debate here, because most people think this is not a safe choice: frequent updates may cause instability, and reboots may be needed to ensure services start correctly. On the other hand, the benefits of using Arch Linux are also obvious. Always being up to date helps improve security, abundant software and an excellent user group provide help in every aspect, and yes, I think they are active enough, which at least means your questions can receive more timely responses. Most importantly, Arch Wiki is encyclopedic. Among all GNU/Linux systems, only two are this excellent in that regard, and the other is Gentoo. I know this is not enough to convince operations people who pursue stable services, but at least I convinced myself. It is worth mentioning that the official Arch Linux website runs on Arch Linux servers.

All right, let us begin.

## Part 1: Creating an Arch Linux Server with vps2arch

To be honest, I prefer Vultr because it provides newer operating system versions and Fedora, which I have always liked. But none of that matters now, because they do not directly support Arch Linux. I am considering whether to add its logo to the website I am designing; that would definitely attract attention.

Creating a custom image is troublesome. It takes time and is not beginner-friendly. Fortunately, we have [vps2arch](https://gitlab.com/drizzt/vps2arch/). Thanks to [@drizzt](https://gitlab.com/drizzt) and other contributors for their work. On an ECS instance initially created as CentOS 7.4, we only need to run three commands, then follow the prompts.

**Note that all data will be erased, but your root password will be preserved and a basic SSH-capable system will be provided.**

```shell
wget http://tinyurl.com/vps2arch
chmod +x vps2arch
./vps2arch
```

After rebooting, you will enter Arch Linux, and everything is ready.

## Part 2: Basic Configuration Steps

### Remote SSH Connection

You can first try `ssh root@your.ecs.ip.address` locally. If you have not used SSH to connect to this host before, it may work. If you have, a large warning may appear and the connection will fail.

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
```

At this point, use `ssh-keygen -R your.ecs.ip.address` to remove the old conflicting key, then connect again. Tired of entering a password every time? Consider using `ssh-copy-id username@your.ecs.ip.address` locally to add your public key to the server. After that, you should be able to connect directly to the ECS instance.

### Creating a Non-Root User and Granting Administrative Privileges with sudo

Connect to your server with SSH.

`useradd newusername` adds a user named newusername, and `passwd newusername` sets a password for that user.

Next, create the user's home directory and assign ownership. Otherwise, after switching to the new user, you will still remain in the root directory, which the command prompt will show.

```shell
mkdir /home/newusername
chown newusername:newusername /home/newusername
```

To grant administrative privileges to the new user, first install sudo and edit `/etc/sudoers`. Use `pacman -S sudo` to install sudo, `chmod u+w /etc/sudoers` to add write permission, then edit with `vi /etc/sudoers`. Add `newusername ALL=(ALL) ALL` below `root ALL=(ALL) ALL`, save and exit, and then run `chmod u-w /etc/sudoers` to revoke write permission.

Use `su - newusername` to switch to newusername.

### Basic Firewall

iptables is already installed in Arch Linux. If you do not like using this complex configuration tool, we can use ufw for the next steps. Alibaba Cloud security groups already provide firewall-like access control, but I think the server side should also apply control.

At this point, we only need to make sure the firewall allows SSH connections.

```shell
sudo pacman -S ufw
sudo ufw app list
sudo ufw allow SSH
sudo ufw enable
```

The firewall is now enabled. Use `sudo ufw status` to check the current status.

```text
Status: active

To                         Action      From
--                         ------      ----
SSH                        ALLOW       Anywhere
SSH (v6)                   ALLOW       Anywhere (v6)
```

### SSH Access for the Normal User

You should be able to log in to the remote server over SSH in a way similar to the ROOT user: `ssh newusername@your.ecs.ip.address`, then enter the password.

The `ssh-copy-id` command mentioned above can help enable key-based authentication.

If SSH key authentication has already been enabled for the root user, you can copy it into the normal user's directory with rsync. This assumes you are still using the normal user above.

```shell
sudo pacman -S rsync
mkdir .ssh
sudo su - root
rsync --archive --chown=newusername:newusername ~/.ssh /home/newusername
```

The last command was tested to work only under the root user; using sudo did not work.

Close the connection and use `ssh newusername@your.ecs.ip.address`. Key authentication should now work normally.

## Part 3: What Comes Next...

The basic server configuration is done. You can start doing what you want to do. Choosing a self-hosted service from [Awesome Selfhosted](https://github.com/Kickball/awesome-selfhosted) might be a good option.
