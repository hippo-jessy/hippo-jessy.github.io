---
title: 【Java Primer】Head First Thread Safety & Object Sharing
date: 2017-03-17 15:20:20
categories: [Java Primer]
tags: [Java, Concurrency]
description:
---

本文对于Java线程安全和对象共享的内容进行一些初步总结，重点是帮助自己理清思路，关联一些零散知识点。大神移步，小白入。

<!-- more -->

## Thread Safety



## Sharing Objects 

什么情况下会使得对象有被多个线程共享的风险？

### runnable中的实例域

### 局部对象引用

对象逸出