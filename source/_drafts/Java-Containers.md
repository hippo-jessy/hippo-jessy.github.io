---
title: Java Containers
date: 2017-01-21 01:25:39
categories: [Java, Java Basics]
tags: [Java, Container]
description:
---

### Container重要的接口继承关系

Container vs Collection :  Container包含Collection 和 Map两大类

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



## Printing Containers

Collection 和 Map均可以直接使用System.out.println()来打印容器内部的所有元素：

```java
Collection<String> list = new ArrayList<String>();
//运用上文中提到的添加一组元素最好的方法Collections.addAll
Collections.addAll(list, "tomorrow","hi","yes");
//调用了list.toString
System.out.print(list);
```

上面这段代码的运行结果如下：

```java
[tomorrow, hi, yes]
```

很明显，list对象调用的toString方法是重写之后的方法，那么这又引出了两个问题：

- Collection是一个接口，其内部并没有toString方法，为什么声明为Collection类型的list对象可以调用toString方法？
- 重写toString方法是在哪里实现的？

上述问题在**Java You Don't Know**系列的一篇博文中进行了解答，请移步 ☞ [【Java You Don't Know - Item 2】All Interfaces Have toString() Method](hippo-jessy.com/)



## Iterator



