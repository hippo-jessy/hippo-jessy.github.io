---
title: 【Java Primer Concurrency】从指令重排序到volatile
date: 2017-03-15 22:08:22
categories: [Java, Java Primer, Concurrency]
tags: [Java, Concurrency]
description:
---

volatile，老生常谈两大特点，第一，volatile修饰的共享变量可以保证其在多线程环境下的可见性；第二，volatile可以禁止重排序。然而，对于第一点，尚且可以理解，对于第二点，我始是觉得有些抽象，重排序是一个大概念，volatile所谓的“禁止重排序”到底是禁止全部指令重排序？还是仅仅限制一部分指令重排序？具体是禁止哪些指令重排序？

此篇博文主要用来总结对volatile的一些理解，以及对volatile的实现原理进行一些扩展讨论。笔记向，略杂乱。





## Reordering



## volatile



## volatile为什么可以保证一次性安全发布（one-time safe publication）？

https://www.ibm.com/developerworks/cn/java/j-jtp06197.html

https://www.ibm.com/developerworks/java/library/j-jtp06197/index.html



## volatile为什么可以保证DCL的安全发布？

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link





## MESI





## False Sharing

http://ifeve.com/falsesharing/

https://software.intel.com/zh-cn/blogs/2011/12/16/false-sharing-2

http://ifeve.com/from-javaeye-false-sharing/