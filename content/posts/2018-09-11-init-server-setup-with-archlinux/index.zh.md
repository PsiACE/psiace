+++
title = "Arch Linux 初始服务器设置"
description = "使用 vps2arch 创建 Arch Linux 服务器，并完成 SSH、用户、sudo 和防火墙基础配置。"
date = 2018-09-11
slug = "init-server-setup-with-archlinux"

[taxonomies]
tags = ["Arch Linux", "Server"]

[extra]
lang = "zh"
+++

**本文所涉步骤仅在阿里云上进行了验证，但应当同样适用于其它云服务供应商。**

## Part 0：前言

我刚刚完成从 Red Hat 系（Fedora, CentOS）~~完全~~迁移到 [Arch Linux](https://www.archlinux.org/) 的过程，这并不算是一个十分稳妥的选择，因为 Red Hat 系向来以高可靠性著称，即便是被称作试验田的 Fedora 也很少会因为稀奇古怪的问题而崩溃。但是，Arch Linux 作为一个滚动更新的发行版，它可以满足我对新鲜事物的好奇，并且该发行版提供的 Arch Wiki 以及 AUR 确实是值得我喜爱。

在将桌面系统更换为 Manjaro Linux（一个基于 Arch Linux 的发行版，便于上手）之后，我开始准备将我在阿里云的 ECS 实例也切换到 Arch Linux 上。在这里有一个小小的争论，因为大部分人认为这不是一个稳妥的选择，频繁更新造成的不稳定，以及需要重启以确保它可以正常启用服务。但另一方面，使用 Arch Linux 的好处同样很明显，时刻最新有助于安全性的提升，丰富的软件和优秀的用户群在各个方面提供帮助（是的，而且我觉得他们足够活跃，这至少意味着你的问题可以得到更加及时的回应），最重要的，百科全书式的 Arch Wiki（在所有 GNU/Linux 系统里，只有两个在相关方面如此出色，另一个是 Gentoo）。我知道这并不足以说服那些追求稳定服务的运维人员，但至少我说服了我自己。值得一提的是 Arch Linux 的官网是运行在 Arch Linux 服务器上的。

好吧，让我们开始！

## Part 1：使用 vps2arch 创建 Arch Linux 服务器

说实在的，我更喜欢 Vultr，因为它提供的操作系统版本更新，而且有我一直喜爱的 Fedora。不过这都不重要了，因为它们都不直接支持 Arch Linux，我正在考虑要不要添加它的徽标到正在设计的网站上，这样一定会吸引不少人的目光。

创建自定义镜像是一件麻烦的工作，它需要花费一定的时间，而且并不是一项对新手友好的事情。好在，我们有 [vps2arch](https://gitlab.com/drizzt/vps2arch/)，感谢 [@drizzt](https://gitlab.com/drizzt) 以及其他贡献者所作出的努力。在一个初始创建为 CentOS 7.4 的 ECS 实例上，我们仅仅需要执行三条命令，接下来就可以完全按照提示进行了。

**注意，一切数据将会被清空，但将保留你的 root 密码并提供一个支持 SSH 的基础系统。**

```shell
wget http://tinyurl.com/vps2arch
chmod +x vps2arch
./vps2arch
```

重启之后，你将进入到 Arch Linux 中，一切都准备好了。

## Part 2：采取一些配置步骤作为基本设置的一部分

### 远程 SSH 连接

你可以先在本地尝试一下 `ssh root@your.ecs.ip.address`，如果你此前没有使用过 SSH 连接，它可能是可用的。但如果用过，则会出现一大段警告，并无法连接。

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
```

这个时候，我们需要使用 `ssh-keygen -R your.ecs.ip.address` 来清除产生冲突的旧密钥。再重新进行连接。厌倦了每次输入密码？那么考虑在本地使用 `ssh-copy-id username@your.ecs.ip.address` 将公钥添加到服务器中。之后，你应当可以直接连接到 ECS 实例。

### 创建非 ROOT 用户并采用 SUDO 授予管理权限

使用 SSH 连接到你的服务器。

`useradd newusername` 将添加一个名为 newusername 的用户，而 `passwd newusername` 将为他设置密码。

接下来需要创建用户主目录并赋权，否则在你切换到新用户后仍然停留在根目录里（命令行提示会指出）。

```shell
mkdir /home/newusername
chown newusername:newusername /home/newusername
```

为了能够给新建用户授予管理权限，我们首先要安装 sudo 并编辑 `/etc/sudoers` 文件。`pacman -S sudo` 安装 sudo，`chmod u+w /etc/sudoers` 增加写权限；采用 `vi /etc/sudoers` 编辑，在 `root ALL=(ALL) ALL` 下面一行添加 `newusername ALL=(ALL) ALL`，保存退出；`chmod u-w /etc/sudoers` 撤销写权限。

采用 `su - newusername` 切换用户到 newusername。

### 基本防火墙

iptables 已经被安装到了 Arch Linux 中，如果你不是很喜欢使用这个复杂的配置工具，我们可以选择使用 ufw 来进行接下来的步骤。（阿里云的安全组特性已经提供了类似防火墙的访问控制功能，但我认为服务器端也应该做出控制）

此时我们只需要确保防火墙允许 SSH 可以正常连接。

```shell
sudo pacman -S ufw
sudo ufw app list
sudo ufw allow SSH
sudo ufw enable
```

此时防火墙已经开启，使用 `sudo ufw status` 可以查看当前状态。

```text
Status: active

To                         Action      From
--                         ------      ----
SSH                        ALLOW       Anywhere
SSH (v6)                   ALLOW       Anywhere (v6)
```

### 普通用户的 SSH 访问

你应当可以用类似 ROOT 用户的方法通过 SSH 登录到远程服务器，`ssh newusername@your.ecs.ip.address`，输入密码。

本地采用上面提到的 `ssh-copy-id` 命令可以帮助你启用密钥身份验证。

如果你在 root 用户下已经启用了 SSH 密钥验证，可以通过 rsync 将其复制到普通用户的目录下。（这里假设你仍是上面的普通用户）

```shell
sudo pacman -S rsync
mkdir .ssh
sudo su - root
rsync --archive --chown=newusername:newusername ~/.ssh /home/newusername
```

最后一条语句经测试只能在 root 用户下使用，采用 sudo 指令不可行。

关闭连接，采用 `ssh newusername@your.ecs.ip.address`，这时应该可以正常使用密钥验证。

## Part 3：接下来...

基本的服务器配置已经处理好了，你可以着手去做你想要做的事情，或许从 [Awesome Selfhosted](https://github.com/Kickball/awesome-selfhosted) 中挑选一个自托管服务是一个不错的选择。
