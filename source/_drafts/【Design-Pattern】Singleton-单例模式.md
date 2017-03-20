---
title: 【Design Pattern】Singleton 单例模式
date: 2016-11-25 16:49:14
categories: [Design Pattern]
tags: [Design Pattern, Java, Concurrency]
description:
---

单例模式应该来说是23种设计模式中最简单的一种，它不涉及类与类之间的关系，仅关注于如何保证让一个类只有一个实现对象。但是由于线程安全等问题，单例模式实际上又并不像它看上去那么简单。本文将主要介绍单例模式的五种常见的实现方法，并且基于线程安全，破解方法，垃圾回收，运行性能三个方面对这五种实现方式进行分析比较。

<!-- more -->

## 单例模式

单例模式是创建类模式之一，其主要特点如下：

1. 确保单例类只有一个实例
2. 该单例类自行实例化并向整个系统提供该实例

单例模式有如下五种常见的实现方式，按照是否延迟加载，可以分为懒加载（）和非懒加载两大类。

## 五种实现

### 1. 饿汉式(Non-lazy Initialization)



### 2. 懒汉式(Lazy Initialization)



### 3. 双重检查锁定(Double-check Locking)







http://www.cnblogs.com/coffee/archive/2011/12/05/inside-java-singleton.html#out-of-orderWrites

```java
public static SingletonThree getInstance() {
        if (instance == null) { 
            synchronized (SingletonThree.class) {           // 1
                SingletonThree temp = instance;             // 2
                if (temp == null) {
                    synchronized (SingletonThree.class) {   // 3
                        temp = new SingletonThree();        // 4
                    }
                    instance = temp;                        // 5
                }
            }
        }
        return instance;
    }
```



### 4. 内部类(Nested Initialization)



### 5. 枚举(Enum Based Singleton)





http://codebalance.blogspot.tw/2010/08/singleton-pattern-and-beyond.html

## 线程安全

结合volatile

## 破解方法



## 垃圾回收

http://blog.csdn.net/zhengzhb/article/details/7331354



## 运行性能



## Reference

http://spiritfrog.iteye.com/blog/214986

https://yq.aliyun.com/articles/11333

http://blog.csdn.net/zhengzhb/article/details/7331369

http://blog.csdn.net/zhengzhb/article/details/7331354

http://ifeve.com/from-singleton-happens-before/

http://codebalance.blogspot.tw/2010/08/singleton-pattern-and-beyond.html

https://zhuanlan.zhihu.com/p/25733866

[《设计模式之禅》]()