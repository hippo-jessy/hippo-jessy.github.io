---
title: 【Java Primer-1】老生常谈
date: 2017-04-12 19:28:15
categories: [Java, Java Primer]
tags: [Java]
description:
---

此篇博文可以看做是Java SE中老生常谈的基础问题大杂烩。有些可能是面试热门问题，另一些是学习过程中的常见问题。不管这些问题是不是被问烂了，只要有一定得价值，我都会尽量总结进来，并且写下一些自己的看法。

又是一个坑，持续更新，填坑中。。。

## Java语言



## Java线程安全

### 1. StringBuffer  vs StringBuilder



### 2. Vector vs ArrayList

Vector和ArrayList有什么区别？

通常见到的回答是Vector线程安全但效率较低而ArrayList线程不安全但效率高。

但是这个回答未免有些笼统。Vector源码中大部分方法都是同步方法，



### 3. Hashtable vs HashMap   