---
title: 【读薄Thinking in Java】Container Primer
date: 2017-01-23 21:30:39
categories: [Java, Java Basics, Thinking in Java]
tags: [Java, Container]
description:
---

## Container重要的继承实现关系

Container vs Collection :  Container包含Collection 和 Map两大类

下面这张图提供了Java中容器的基本实现框架(图片来自Thinking in Java)：

![Screen Shot 2017-01-23 at 8.09.48 PM](/Users/hippo/Desktop/Screen Shot 2017-01-23 at 8.09.48 PM.png)

<!--more-->

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

## 给Collection添加一组元素的几种方法对比：

1. Collection.addAll(Collection<? extends E> c) **对比** Collection Constructor taking a Conllection as a parameter

   第一种方法Collection.addAll要快一些，并且灵活一些

2. Collections.addAll(Collection<? super T> c, T... elements) **对比** Collection.addAll(Collection<? extends E> c)

   第一种方法Collections.addAll要比Collection.addAll更灵活，它可以有多个参数，意味着可以同时add多个Collection， 而后者只能参数列表只能有一个参数

3. Collections.addAll(Collection<? super T> c, T... elements) **对比** Arrays.asList(T... a)

   第一种方法更好，第一种返回的是Collection<? super T> c，是真正的Collection对象，而asLIst虽然返回的也是List，但是实际上是Arrays的一个内部类ArrayList实现的，不可以resize

> Arrays.asList(array) vs ArrayList
>
> Arrays.asList(array)返回的List实际上是Arrays类的一个内部类ArrayList，和java.lang.util中定义的ArrayList是两个不同的类，不同的概念。它的容量不是可变的，并且底层保存数据的结构依然是传入的参数数组array，因此返回的List和传入的参数数组无法解除关联。如下例：
>
> ```java
> Integer[] array = {1,2,3,4,5};
> List<Integer> list = Arrays.asList(array);
> list.set(0,9);
> list.set(1,8);
> System.out.println(Arrays.toString(array));
> ```
>
> 运行后得到的结果为：
>
> ```
> [9, 8, 3, 4, 5]
> ```
>
> 也就是说改变Arrays.asList(array)返回的List中的元素，则原始的array数组中的元素也会发生相应改变



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

上述问题在[**Java You Don't Know**](http://hippo-jessy.com/categories/Java/Java-You-Don-t-Know/)系列博文中的一篇中进行了解答，请移步 ☞ [【Java You Don't Know - Item 2】All Interfaces Have toString() Method](hippo-jessy.com/)

## Iterator

关于迭代器模式以及其在Java Collection的框架中的应用， 在[**Design Pattern**](http://hippo-jessy.com/categories/Design-Pattern/)系列中的[【Design Pattern】Iterator 迭代器模式](http://hippo-jessy.com/2017/01/22/%E3%80%90Design-Pattern%E3%80%91Iterator-%E8%BF%AD%E4%BB%A3%E5%99%A8%E6%A8%A1%E5%BC%8F/)这一篇中进行了详细讲解。

这里简单提一下迭代器在foreach

