---
title: 【深入理解Java虚拟机-0】思维导图汇总
date: 2017-02-03 22:59:05
categories: [JVM, 深入理解Java虚拟机]
tags: [JVM, MindMap]
description:
---

此篇博文主要用于汇总JVM初级学习阶段的思维导图，主要根据《深入理解Java虚拟机》书中的脉络，结合JVM Specification中的知识点进行拓展和总结。思维导图通过**iThoughtsX 4.3**绘制，文中会提供原始格式文件(低于4.3版本的iThoughtsX可能无法打开原始文件)和导出的图片。由于有些章节的思维导图过大，我可能会进行拆分，但是尽量不会影响理解。 

内容有些杂乱，主要用作个人笔记整理，同时也希望这些思维导图能帮助大家更好地理解《深入理解Java虚拟机》(配合JVM Specification食用更佳）。有些导图目前还是半成品，暂时不会放上来，文章持续更新中。
<!-- more -->

## 第二部分 自动内存管理

### 第二章 Java内存区域与内存溢出异常 

这一章节主要涉及三方面的内容： 

- 运行时数据区域
- HotSpot虚拟机对象的表示
- OutOfMemoryError的相关实践

思维导图如下( 点击放大再放大😑 ) ：![](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Java%20Memory%20Area.pdf)

iThoughtsX原格式文件地址:

[http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Java%20Memory%20Area.itmz](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Java%20Memory%20Area.itmz)

### 第三章 垃圾收集器与内存分配策略

[http://qifuguang.me/2015/09/02/[Java并发包学习七]解密ThreadLocal/](http://qifuguang.me/2015/09/02/[Java并发包学习七]解密ThreadLocal/)

## 第三部分 虚拟机执行子系统

### 第六章 类文件结构

这一章节思维导图拆分为两部分，第一部分是关于Class类文件结构的，第二部分是关于字节码指令简介的。由于第二部分知识点比较琐碎，目前还在考虑对此部分是否有制作思维导图的必要。首先献上第一部分思维导图 ( 点击放大再放大😑 ) ：![Class File Mind Map](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】Class%20File%20Mind%20Map.pdf)

iThoughtsX原格式文件地址:

 [http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】Class%20File%20Mind%20Map.itmz](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】Class%20File%20Mind%20Map.itmz)

### 第七章 虚拟机类加载机制

这一章节分为类加载机制以及类加载器两部分。

#### 类加载机制

![Class Loading](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading%20.pdf?%20v=20170214)

iThoughtsX原格式文件地址:

[http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading%20.itmz](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading%20.itmz)

#### 类加载器

![](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading_1%20.pdf?%20imageView2/3/w/400/h/400/q/75)

iThoughtsX原格式文件地址:

[http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading_1%20.itmz](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20Class%20Loading_1%20.itmz)

### 第八章 虚拟机字节码执行引擎

这一章节主要分为三个部分：

- 运行时栈帧结构

- 方法调用

- 基于栈的字节码解释执行引擎

这三部分都集中在下面这张图中进行总结：![](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20JVM%20Bytecode%20Execution%20Engine.pdf)

iThoughtsX原格式文件地址:

[【Understanding%20the%20JVM】%5BMind%20Map%5D%20JVM%20Bytecode%20Execution%20Engine.itmz](http://ojnnon64z.bkt.clouddn.com/【Understanding%20the%20JVM】%5BMind%20Map%5D%20JVM%20Bytecode%20Execution%20Engine.itmz)


## 第四部分 程序编译与代码优化

敬请期待。。。😪

## 第五部分 高效并发

这一部分书中主要分为两个章节来讲解： Java内存模型与线程、线程安全与锁优化。但是《深入理解Java虚拟机》并没有用很大的篇幅来讲并发这一部分，因此还需结合《Java Concurrency in Practice》等书来加深理解。更多关于java并发的总结可以关注Java Primer系列的相关博文。

### 第十二章 Java内存模型与线程







### 第十三章 线程安全与锁优化



