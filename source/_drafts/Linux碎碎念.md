---
title: Linux碎碎念
date: 2016-04-09 08:13:19
categories: [Linux, Basic]
tags: [Linux]
description:
---

“Linux碎碎念”系列，笔记向，小白入。

Linux系列博文主要根据个人的日常使用经验，以及参考“X哥”的Linux教程来总结，侵删。Linux一些比较琐碎的基础知识点以及使用常识会用mind map的形式呈现。



windows: PE

linux: ELF (可执行二进制文件格式)



文件系统：

根文件系统：rootfs

FHS： file hierachy system

根目录下的主要文件夹：

/boot: 系统启动相关的文件，如内核，initrd，以及grub(bootloader)

/dev: 设备文件  （Linux下一切皆文件）

​           设备文件：

​			块设备： 随机访问，数据块

​			字符设备： 线性访问，按字符为单位

​			设备号：主设备号和次设备号

/etc: 配置文件（纯文本文件）

/home:   用户家目录    /home/USERNAME

​		例外： root用户的家目录  /root

/root: 管理员（root用户）的家目录

/lib: 库文件

​	静态库:   Linux:  .a

​	动态库： win: .dll    Linux:   .so (shared object)

​        分析动态库和静态库的区别

​	/lib/modules: 内核模块文件

动态库文件也是ELF文件，但是却不是LSB executable。因为库文件不能单独运行，只能被其他程序调用，它没有程序访问入口。

eg: file ***.so 显示ELF LSB shared object

​      file /bin/ls  显示 ELF LSB executable

/media: 挂载点目录，主要用来挂载移动设备

/mnt: 挂载点目录，主要用来挂载额外的临时文件系统

/opt: 原来的第三方程序安装目录（现在一般都放在/usr/local目录下），可选目录

**/proc: 伪文件系统， 内核映射文件**（内核的统计数据和可调参数等如寄存器大小，cacheline的大小，网卡接受的数据包个数）

**/sys: 伪文件系统， 跟硬件设备相关的属性映射文件**

/proc 和 /sys这两个文件夹和系统调优紧密相关

/tmp: 临时文件（另一个临时文件：/var/tmp）

/var: 可变化的文件

/bin: 可执行文件，用户命令

/sbin: 管理命令

​	