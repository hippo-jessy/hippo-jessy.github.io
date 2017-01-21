---
title: Java Containers
date: 2017-01-21 01:25:39
categories: [Java, Java Basics]
tags: [Java, Container]
description:
---

### Container重要的接口继承关系

Container vs Collection : Container包含Collection

Container(容器): 

五大接口： Collection(Set, List), Map, Iterator

- Collection(集合)
  - 无序不重复-> Set -> HashSet 
  - 有序重复-> List
  - 有序重复-> Queue

Set的其他扩展：HashSet(快速获取元素), TreeSet(按照字母表顺序存储), LinkedHashSet(按照存入顺序存储)


- Map(映射)
  - HashMap


Map的其他扩展(和Set类似)： HashMap(快速查找), TreeMap, LinkedHashMap




### 给Collection添加一组元素的几种方法对比：

- Collection.addAll(Collection<? extends E> c) vs Collection Constructor taking a Conllection as a parameter 

第一种方法Collection.addAll要快一些，并且灵活一些

- Collections.addAll(Collection<? super T> c, T... elements) vs Collection.addAll(Collection<? extends E> c)

第一种方法Collections.addAll要比Collection.addAll更灵活，它可以有多个参数，意味着可以同时add多个Collection， 而后者只能参数列表只能有一个参数

- Collections.addAll(Collection<? super T> c, T... elements) vs Arrays.asList(T... a)

第一种方法更好，第一种返回的是Collection<? super T> c，是真正的Collection对象，而asLIst虽然返回的也是List，但是实际上是Arrays的一个内部类ArrayList实现的，不可以resize

> Arrays.asList() vs ArrayList
>
> Arrays.asLIst()返回的List实际上是Arrays的一个内部类定义的ArrayList，它的容量不是可变的，和java.lang.util中定义的ArrayList是两个不同的类，不同的概念



综上所诉，给集合添加一组元素，或者为集合初始化一组数据，最方便的办法是使用Collections.addAll(Collection<? super T> c, T... elements)





