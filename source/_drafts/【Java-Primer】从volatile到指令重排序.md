---
title: 【Java Primer】从volatile到指令重排序
date: 2017-03-15 22:08:22
categories: [Java, Java Primer]
tags: [Java, Concurrency]
description:
---

最近被volatile内部原理，对象发布以及线程安全等问题虐了好几天，现在总算是有些眉目了╮(￣▽￣)╭

这篇文章主要用来总结对volatile的一些理解，以及对volatile的实现原理进行一些扩展讨论。笔记向，结构略杂乱。

<!-- more -->



## volatile为什么可以保证一次性安全发布（one-time safe publication）？

https://www.ibm.com/developerworks/cn/java/j-jtp06197.html

https://www.ibm.com/developerworks/java/library/j-jtp06197/index.html



## volatile为什么可以保证DCL的安全发布？

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link









http://www.cnblogs.com/mengheng/p/3495379.html

http://ifeve.com/jvm-memory-reordering/



http://ifeve.com/from-singleton-happens-before/



延伸http://www.infoq.com/cn/articles/memory_barriers_jvm_concurrency