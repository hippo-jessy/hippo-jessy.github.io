---
title: 【Java Primer】Head First Thread Safety & Object Sharing
date: 2017-03-17 15:20:20
categories: [Java Primer]
tags: [Java, Concurrency]
description:
---

本文对于Java线程安全和对象共享的内容进行一些初步总结，重点是帮助自己理清思路，关联一些零散知识点。大神移步，小白入。

《Java Concurrency in Practice》第三章中对对象共享部分的讲解比较散乱，特别是对象发布这一块。下面主要按照我自己的理解对线程安全以及对象共享部分进行梳理总结。

<!-- more -->

## Thread Safety

我们经常将线程安全挂在嘴边，但是到底什么是线程安全？那些做法会威胁到线程安全？



## Sharing Objects 

什么情况下会使得对象有被多个线程共享的风险？

### runnable中的实例域

### 局部对象引用

对象逸出