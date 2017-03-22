---
title: 【Design Pattern】Singleton 单例模式
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Java
  - Concurrency
date: 2017-02-20 16:49:14
description:
---




单例模式应该来说是23种设计模式中最简单的一种，它仅关注于如何保证让一个类只有一个实现对象，不涉及类与类之间的关系，。但是由于线程安全等问题，单例模式实际上又并不像它看上去那么简单。很早之前开始构思这篇博文，无奈在写的过程中逐渐发现单例模式实在是个深坑，一直拖到现在都没完全填完这个坑。鉴于我对多线程以及JVM了解得并不深入，文章中如有纰误，欢迎指正。

本文将主要介绍单例模式的五种常见的实现方法，并且基于线程安全，破解方法，垃圾回收，运行性能四个方面对这五种实现方式进行分析比较。

<!-- more -->

## 单例模式

单例模式是创建类模式之一，其主要特点如下：

1. 确保单例类只有一个实例
2. 该单例类自行实例化并向整个系统提供该实例

单例模式有如下五种常见的实现方式，按照是否延迟加载(Initialization On Demand)，可以分为懒加载和非懒加载两大类。尽管几种实现方式各不相同，但是从根本上讲，为了达到唯一化实例的目的，都是采用了同一种思路：限制创建+限制更改。

1. 创建实例的途径被封装在单例类中：私有化构造器，禁止外界构造实例，单例类的唯一实例是在单例类内部被创建
2. 更改实例的途径被切断：该单例类只提供给外界“读取”该单例实例引用的入口，从而限制外界更改单例类中的唯一实例

然而，如果仅仅满足上面两点，仅仅能保证单例类只有一个实例，却无法保证线程安全。当单例对象被多个线程共享时，如果单例对象没有被安全发布或者访问单例类状态时存在竞态条件(Race Condition)时，则会出现线程安全问题。

## 五种实现

### 1. 饿汉式(Eager Initialization)

为了满足上文中提到的“限制创建+限制更改”的条件，饿汉式提出了一种解决方案（下面解释比较绕，仅作参考）：

为了禁止外界创建实例，私有化构造器，要使唯一实例在单例类内部创建，于是考虑将单例对象设计成单例类的一个域，在域初始化的时候创建唯一的单例实例；为了限制外界只能“读取”单例实例的引用，于是考虑将该域的访问权限设置为private，再额外提供一个“只读”的方法来访问该域。由于唯一的实例是单例类的域，则外界没有办法访问单例类的实例方法，于是这个“只读”的方法只能是静态方法，而该静态方法需要访问单例实例域，而由于静态方法只能访问静态域 ，因此单例实例域只能是静态域。

```java
public class Singleton{
  private static Singleton instance = new Singleton();
  private Singleton(){} 
  public static Singleton getInstance(){
    return instance;
  }
}
```

饿汉式的特点在于利用静态初始化器来静态构造单例对象。使用静态初始化器来初始化一个对象引用(Use static initializer to do the initializing stores)这也是《Java Concurrency in Practice》中提到的四种安全发布对象的方法之一。这种方法天然线程安全，因为它是在类初始化的时候创建唯一的单例实例的，而

> 回忆下四种安全发布对象的方法（关键在于对象的引用以及对象的状态必须同时对其他线程可见）：
>
> 1. use static initializer to do the initializing stores
> 2. storing a reference to it into a volatile field or ActomicReference
> 3. storing a reference to it into a final field

```java
public class Singleton{
  public static final Singleton instance = new Singleton();
  private Singleton(){}
}
```



#### 线程安全

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link



#### 加载

饿汉式的两种实现方式均为eager initialization，也就是说

### 2. 懒汉式(Lazy Initialization)

```java
public class Singleton{
  private static Singleton instance;
  private Singleton{}
  public static Singleton getInstance(){
    if(instance == null){
      instance = new Singleton();
	}
    return instance;
  }
}
```

懒汉式



```java
public class Singleton{
  private static Singleton instance;
  private Singleton{}
  public static synchronized Singleton getInstance(){
    if(instance == null){
      instance = new Singleton();
    }
    return instance;
  }
}
```



### 3. 双重检查锁定(Double-check Locking, Lazy Initialization)

```java
public class Singleton{
  private static Singleton instance;
  private Singleton(){}
  public static Singleton getInstance(){
    if(instance == null){
      synchronized(Singleton.class){
        if(instance == null){
          instance = new Singleton();
        }
      }
    }
    return instance;
	}
}
```

DCL的出现主要是

#### 线程安全

DCL的重点在于第5行到第7行

DCL看似是一种合理的单例模式实现，它既解决了Check-Than-Act的race condition，又避免了直接同步整个getInstance方法带来的性能效率问题，简直就是抖了个完美的机灵，权衡了同步和效率问题。但是，DCL在并发环境中却仍然会出现问题，这些问题涉及到很多JMM相关的知识，这一部分也是整篇博文的重点所在。

主要有两种原因导致DCL线程不安全（两种原因究其根本，都是由于指令重排序造成的）：

<font color="green" size="3px">1. 最老生常谈且容易理解的原因</font>

当一个线程在创建单例对象时，其它线程可能看到未被完全构造的对象。更确切地说，由于第8行代码  <font color="blue" >instance = new Singleton();</font>  内部的指令可能被编译器或处理器重排序，导致其他线程可能在单例对象还未被完全构造时就得到了单例对象的地址。  <font color="blue">instance = new Singleton();</font>  对应的字节码如下

```
new           #3                  // class singleton/Singleton4
dup
invokespecial #4                  // Method "<init>":()V
putstatic     #2                  // Field instance:Lsingleton/Singleton4;
```

说白了也就是三个步骤：

1. 给单例对象分配空间
2. 调用构造器初始化单例对象
3. 将单例对象的地址赋值给instance引用

但是由于第2步和第3步之间既不存在任何依赖关系又没有被插入任何内存屏障，在这种情况下，JMM允许重排序。于是当这两个步骤被重排序之后，问题就出现了，如下图所示

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern】Singleton%20单例模式_1.png)

线程A率先调用getInstance方法来创建单例对象，  <font color="blue" >instance = new Singleton();</font>  内部指令invokespecial与putstatic重排序（即图中A2与A3步骤被重排序），当A3执行完以后，线程B开始执行getInstance方法，此时instance引用已经指向尚未初始化的单例对象地址，因此如果线程B此时读取单例对象的field将会得到默认值而不是构造方法初始化后的值。这个例子实际上也是对象不安全发布的典型之一，对象的引用和对象的状态不能保证同时对其他线程可见。

<font color="green" size="3px">2. 较为隐蔽的原因</font>

DCL除了不安全发布对象之外，还有可能因为指令重排造成其他问题



尽管这里说有两种原因造成DCL线程不安全，但是究其根本，这两种原因都是由于指令重排序造成的。第一种由于  <font color="blue" >instance = new Singleton();</font>  内部指令重排序造成对象不安全发布，第二种由于互不依赖的load指令重排序造成返回失效值。

想要杜绝指令重排序造成的线程安全问题，内存屏障和锁以及final变量都是可能的解决办法

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link

[http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html](http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html)

两种结局方案： volatile  vs double checked and double locking

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



将instance标记为volatile的变量可以完全解决上面的困境（JDK 5.0以后才能放心使用volatile来解决DCL的问题），如果对volatile的实现原理不太了解，可以移步另一篇博文[【Java Primer】从volatile到指令重排序]()





### 4. 内部类(Nested Initialization, Lazy Initialization)

```java

```



### 5. 枚举法(Enum Based Singleton)





http://codebalance.blogspot.tw/2010/08/singleton-pattern-and-beyond.html

## 线程安全

前面已经对每种单例模式的实现方法进行了线程安全分析，在这里做一个总结的。





适用情况：



## 破解方法

除了枚举实现的单例模式，其他的四种实现方法都可以被破解。所谓破解也就是使得应用中出现单例类两个或两个以上的对象。主要有反射破解，序列化和克隆破解这三种破解方法。

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