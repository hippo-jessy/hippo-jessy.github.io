---
title: 【Design Pattern】Iterator 迭代器模式
date: 2017-01-22 03:32:07
categories: [Design Pattern]
tags: [Design Pattern, Java]
description:
---

# Class Diagram

![【Design Pattern】Iterator 迭代器模式](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern】Iterator%20迭代器模式.png)

# Introduction

迭代器模式其目的是将容器的遍历与容器的内部实现解耦，从而利用一种通用统一的方式遍历内部实现各异的多种容器。迭代器模式的使用已经非常普遍，这里不再赘述。此篇博客重点在于介绍迭代器的内部实现，以及在JDK源码中迭代器模式的实际运用。

<!--more-->

# Implementation

既然是要与容器内部实现解耦，很自然地想到要加一层针对容器的抽象。如何加抽象？这里采用interface的形式。根据上文中的类图，我们可以看到Aggregate接口，这个接口就保证了凡是实现了该接口的容器（不管其内部是如何实现的）都可以利用Iterator对其进行遍历。Aggregate接口声明的createIterator()方法非常关键(对应于java中的iterator()方法），它实现了Iterator与容器的关联绑定。给一个更具体的ConcreteIterator类图：

![【Design Pattern】Iterator 迭代器模式_1](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern】Iterator%20迭代器模式_1.png)

具体来说，ConcreteIterator的构造器有一个参数，这个参数必须是一个实现了Aggregate接口的类的对象。这样，通过createIterator()的内部实现  return new ConcreteIterator(this) 使得ConcreteIterator关联了ConcreteAggregate的对象，从而可以直接利用createItertor()返回的Iterator对象来对ConcreteAggregate进行遍历。

# Examples

> 所有【Design Pattern】系列博文的示例代码都可以在这个repo中找到[https://github.com/hippo-jessy/design_pattern](https://github.com/hippo-jessy/design_pattern)

这里给出一个实现迭代器模式的一个例子(ConcreteAggregate用ArrayList作为内部结构存储)：

- **Aggregate Interface**

```java
public interface Aggregate<E> {
	Iterator<E> createIterator();
}
```

- **Iterator Interface**


```java
public interface Iterator<E> {
	E next();
	boolean hasNext();
}
```

- **ConcreteAggregate Class**

```java
public class ConcreteAggregate<E> implements Aggregate<E> {
	private ArrayList<E> internalData;
	
	public ConcreteAggregate(){
		internalData = new ArrayList<E>();
	}
	
	@Override
	public Iterator<E> createIterator() {
		return new ConcreteIterator<E>(this);
	}
	
	public E get(int index){
		return internalData.get(index);
	}
	
	public void add(E element){
		internalData.add(element);
	}
	
	public int size(){
		return internalData.size();
	}
}
```

- **ConcreteIterator Class**

```java
public class ConcreteIterator<E> implements Iterator<E> {

	private ConcreteAggregate<E> aggregate;
	private int cursor = 0;

	public ConcreteIterator(ConcreteAggregate<E> aggregate) {
		this.aggregate = aggregate;
	}

	@Override
	public E next() {
		return aggregate.get(cursor++);
	}

	@Override
	public boolean hasNext() {
		return (cursor < aggregate.size()) ? true : false;
	}

}
```

- **Client 端代码**

```java
public class Client {
	public static void main(String[] args){
		ConcreteAggregate<String> aggregate = new ConcreteAggregate<String>();
		aggregate.add("This");
		aggregate.add("is");
		aggregate.add("a");
		aggregate.add("bright");
		aggregate.add("day");
		Iterator<String> iter = aggregate.createIterator();
		while(iter.hasNext()){
			System.out.print(iter.next()+"/");
		}
	}
}
```

运行输出结果为：

```
This/is/a/bright/day/
```

<br/>

# Extension

参照上面的类图和例子，又产生了如下疑问：

这里产生了一个新的问题，如果ConcreteIterator必须设一个ConcreteAggregate类型的属性，那岂不是每定义一种ConcreteAggregate都得重新定义一个与之对应的ConcreteIterator类？**从某种程度上来说**，java中确实是这样做的。

为什么说是“从某种程度上“ ？原因主要有两点：

1. 以Collection框架为例，从最初的Iterable接口, Collection接口到最后的ArrayList, LinkedList, HashSet, PriorityQueue等最终实现，中间添加了多重抽象层，比如AbstractCollection, AbstractList等等。因此在JDK中ConcreteAggregate的这个概念变得模糊了。以ArrayList和LinkedList为例，实际上充当ConcreteAggregate的是它们的父类AbstractList。也就是说只需要定义与AbstractList对应的ConcreteIterator类即可，而不必要给ArrayList，LinkedList都创建对应的ConcreteIterator。

2. 严格地来说，java是在ConcreteAggregate类中定义一个与之对应的ConcreteIterator**内部类**。这样做其实是一种很明智的做法，从上面的两张类图以及Example中的示例代码我们可以清楚的看到Client端（也就是JDK使用者）通常只会和Aggregate接口，ConcreteAggregate类以及Iterator接口打交道（Client端遍历容器只需要使用Iterator接口暴露的方法即可，没有任何调用ConcreteIterator的需求）。ConcreteIterable类除了在ConcreteAggregate类的createIterator方法中被实例化以外，不会在其他地方实例化。而且这种关联关系存在的意义是为了让ConcreteIterable使用ConcreteAggregate内部的某些方法以便实现Iterator接口定义的next()等方法。很明显在将ConcreteIterable作为ConcreteAggregate的内部类来定义非常合适。甚至可以直接在createIterator方法中定义匿名内部类实现Iterable接口。

   > 适合使用匿名类情形：该类只会在定义的地方被实例化；
   >
   > 适合使用内部类的特征： 该类需要使用外部类的某些属性方法而该类又不会在外部类以外的地方被调用或实例化。

于是上面Example部分的实例代码可以进行改写（Iterator接口用匿名内部类实现，无需专门单独定义ConcreteIterator类）：

- **改进版ConcreteAggregate**

```java
public class ConcreteAggregateOptim<E> implements Aggregate<E> {

	private ArrayList<E> internalData;

	public ConcreteAggregateOptim() {
		this.internalData = new ArrayList<E>();
	}

	@Override
	public Iterator<E> createIterator() {
      //使用匿名内部类实现Iterator接口
		return new Iterator<E>() {
			private int cursor = 0;

			@Override
			public E next() {
				return get(cursor++);
			}

			@Override
			public boolean hasNext() {
				return (cursor < size()) ? true : false;
			}

		};
	}

	public E get(int index) {
		return internalData.get(index);
	}

	public void add(E element) {
		internalData.add(element);
	}

	public int size() {
		return internalData.size();
	}

}
```

JDK中对迭代器模式的实现和上面这段改进代码比较类似，只不过它更倾向于采用内部类而非匿名内部类。

JDK库中Iterable接口相当于上文类图中的Aggregate接口，Iterable接口中声明的方法Iterator()对应于createIterator()方法，Iterator接口对应于Iterator接口，AbstractList类对应于ConcreteAggregate类，而AbstractList类中的内部类Itr实现了Iterator接口，相当于ConcreteIterator。ArrayList和LinkedList均为AbstractList的子类，可以直接使用iterator()方法来得到Concreteiterator从而实现遍历。

```java
ArrayList<String> sampleList = new ArrayList<String>();
Collections.addAll(sampleList,"a","b","c","d");
//sampleList.iterator()调用的是ArrayList的父类AbstractList中实现Iterable接口的方法
Iterator<String> iter = sampleList.iterator();
while(iter.hasNext()){
  System.out.println(iter.next());
}
```

   <br/>

# References

Design Pattern(GOF)
