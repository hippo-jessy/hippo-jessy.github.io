---
title: 【Design Pattern】Singleton 单例模式
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Java
  - Concurrency
  - JVM
date: 2017-02-20 16:49:14
description:
---

单例模式应该来说是23种设计模式中最简单的一种，它仅关注于如何保证让一个类只有一个实现对象，不涉及类与类之间的关系。但是由于线程安全等问题，单例模式实际上又并不像它看上去那么简单。很早之前开始构思这篇博文，无奈在写的过程中逐渐发现单例模式实在是个深坑，一直拖到现在都没完全填完这个坑。鉴于我对多线程以及JVM了解得并不深入，文章中如有纰误，欢迎指正。

本文将主要介绍单例模式的五种常见的实现方法，并且基于线程安全，破解方法，垃圾回收，运行性能四个方面对这五种实现方式进行分析比较。

<!-- more -->

## 单例模式

单例模式是创建类模式之一，其主要特点如下：

1. 确保单例类只有一个实例
2. 该单例类自行实例化并向整个系统提供该实例

单例模式有五种常见的实现方式，按照是否延迟加载(Initialization On Demand)，可以分为懒加载和非懒加载两大类。尽管几种实现方式各不相同，但是从根本上讲，为了达到唯一化实例的目的，都是采用了同一种思路：限制创建+限制更改。

1. 限制创建，创建实例的途径被封装在单例类中：私有化构造器，禁止外界构造实例，单例类的唯一实例是在单例类内部被创建
2. 限制更改，更改实例的途径被切断：该单例类只提供给外界“读取”该单例实例引用的权限，从而限制外界更改单例类中的唯一实例

然而，如果仅仅满足上面两点，仅仅能保证单例类只有一个实例，却无法保证线程安全。当单例对象被多个线程共享时，如果单例对象没有被安全发布或者访问单例类状态时存在竞态条件(Race Condition)时，则会出现线程安全问题。

## 五种实现

### 1. 饿汉式(Eager Initialization)

饿汉式的主要特征在于eager initialization，它在类初始化的时候就完成了唯一单例对象的创建，而不是等到真正需要用到单例对象的时候才创建。

为了满足上文中提到的“限制创建+限制更改”的条件，饿汉式提出了一种解决方案（下面解释比较绕，仅作参考）：

**为了限制外界创建实例**，饿汉式采用私有化构造器，并保证唯一实例在单例类内部创建，具体实现是将单例对象设计成单例类的一个域，采用eager initialization在域初始化的时候创建唯一的单例实例；

**为了禁止外界更改唯一单例对象的引用地址**，必须使得外界只能“读取”单例实例的引用，于是考虑将该域的访问权限设置为private，再额外提供一个“只读”的方法来访问该域。由于唯一的实例保存在单例类的内部，并且在单例类内部被创建，外界没有办法创建单例对象，进而无法访问单例类的实例方法，于是这个暴露给外界的“只读”方法只能是静态方法，而该静态方法需要访问单例实例域，而由于静态方法只能访问静态域 ，因此单例实例域只能是静态域。

```java
public class Singleton{
  private static Singleton instance = new Singleton();
  private Singleton(){} 
  public static Singleton getInstance(){
    return instance;
  }
}
```

饿汉式的特点在于利用静态初始化器来静态构造单例对象。使用静态初始化器来初始化一个对象引用(Use static initializer to do the initializing stores)这也是《Java Concurrency in Practice》中提到的四种安全发布对象的方法之一。这种方法天然线程安全，因为它是在类初始化的时候创建唯一的单例实例的，而JVM在执行类初始化期间会尝试去获取一个锁，这样多个线程初始化同一个类的时候可以实现同步（对类初始化阶段JVM如何获取锁感兴趣的童鞋可以查阅[双重检查锁定与延迟初始化](http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link)的后半部分内容）。

> 回忆下四种安全发布对象的方法（关键在于对象的引用以及对象的状态必须同时对其他线程可见）：
>
> 1. use static initializer to do the initializing stores(the underlying principle is somewhat the same as method 4) 
> 2. storing a reference to it into a volatile field or ActomicReference
> 3. storing a reference to it into a final field of a properly constructed object
> 4. storing a reference to it into a field that is properly guarded by a lock

上面这种实现方法为了限制外界只能“读取”单例实例的引用，采取了“private域”+“暴露只读方法访问private域”的解决办法。但是如果保存单例实例的域是final的，则外界必定无法修改单例对象的引用，只能读取。于是也就没有必要将该域的权限设为private也没有必要暴露一个只读方法来帮助外界访问单例对象。这种新的饿汉式实现方式如下：

```java
public class Singleton{
  public static final Singleton instance = new Singelton();
  private Singleton(){}
}
```

#### 线程安全

上面两种饿汉式的实现方式都是基于安全发布对象的第一种途径，因此在对象发布上是安全的。如果单例类的设计者为单例类添加更多的方法后，这里无法保证是否会出现一些线程不安全的访问方法。但是这不是我们讨论的重点。本文中所有的线程安全问题讨论都基于单例模式的最简单范式，而不考虑实际应用中的代码扩展。

### 2. 懒汉式(Lazy Initialization)

与饿汉式不同，懒汉式追求懒加载，即在需要使用单例对象的时候才创建单例对象。这样在某些情境下可以减少程序启动的时间，也可以最大程度的节省内存。当然，对应的弊端是，当第一次需要使用单例对象时可能需要花费更多时间来创建单例对象。

同样的，懒汉式也遵循文章开头提到的两点设计要求：“限制创建+限制更改”，懒汉式的实现思路如下：

**为了限制外界创建实例**，懒汉式同样采用私有化构造器，并保证唯一实例在单例类内部创建。具体实现也是将单例对象保存在单例类的一个域中，采用lazy initialization在外界第一次读取单例对象时创建唯一的单例对象（即在暴露给外界的“只读”方法中创建单例对象，该“只读”方法的内部逻辑保证只有第一次读取单例对象时才会创建对象，并且保证只会创建一次）。

**为了禁止外界更改单例类中保存的唯一单例对象的引用地址**，懒汉式和饿汉式的第一种实现方式采用了同样的处理技巧：将该域的访问权限设置为private，再额外提供一个“只读”的方法来访问该域。同样的，由于唯一的实例保存在单例类的内部，并且在单例类内部被创建，外界没有办法创建单例对象，进而无法访问单例类的实例方法，于是这个暴露给外界的“只读”方法只能是静态方法，而该静态方法需要访问单例实例域，而由于静态方法只能访问静态域 ，因此单例实例域只能是静态域。

懒汉式的初步的实现如下：

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

#### 线程安全

很明显这种实现不是线程安全的。首当其冲，getInstance()方法中出现了经典的race condition：第五行到第七行代码是典型的Check-Than-Act。线程A执行getInstance()时由于是第一次调用，instance此时还是null，执行完第五行代码时，系统切换执行线程B，此时线程B中看到的instance依然是null，于是继续执行创建单例对象，然后切换到线程A继续执行第六行代码，于是**第二个单例对象**被创建了，违反了单例模式的要求。

然而，就算我们忽略Check-Than-Act的race condition，上面的代码依旧是线程不安全的。原因在于多线程共享对象时，一定要保证该对象安全发布，否则有些线程会看到未被完全构造的共享对象。这一条暂不展开分析，对于对象安全发布的问题在后文讲解双重检查锁定时会重点讲解。

解决race condition以及对象不安全发布，都可以通过加锁来简单粗暴解决。比如下面这个就是利用隐式锁来实现线程安全懒汉式：

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

直接将getInstance方法改为同步方法。这样固然可以解决线程安全问题，但是线程安全和执行性能从来都是此长彼消的。本来上面的Check-Than-Act以及对象不安全发布的问题只会在第一次访问（创建）单例对象的时候发生，解决问题的关键在于同步第一次创建单例对象和第一次访问单例对象，现在我们却将每次访问单例对象的操作都同步了，虽然也解决了问题，却是杀鸡用牛刀，使得所有访问单例对象的操作都只能“串行”执行，极大地牺牲了效率。

### 3. 双重检查锁定(Double-check Locking, Lazy Initialization)

DCL的出现主要是为了解决前面直接同步整个方法带来的低效率问题。它通过增加一个判断语句来决定何时需要加锁（只有第一次创建单例对象时需要同步），然后再将Check-Than-Act的race condition用同步块锁定。具体实现如下：

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

DCL的重点在于第5行到第9行，第5行是用来判断是否是第一次创建单例对象，如果是，则需要对race condition加锁。而这里由于还未有任何单例对象被创建，因此无法使用单例对象的隐式锁。于是第6-9行只能借用单例类的Class对象的隐式锁来保证Check-Then-Act的原子性。

#### 线程安全（死磕DCL）

DCL看似是一种合理的单例模式实现，它既解决了Check-Than-Act的race condition，又避免了直接同步整个getInstance方法带来的性能效率问题，简直就是抖了个完美的机灵，权衡了同步和效率问题。但是，DCL在并发环境中却仍然会出现问题，DCL虽然解决了Check-Than-Act的竞态条件，却忽略了懒汉式的不安全发布问题以及可见性问题。

主要有两种原因导致DCL线程不安全：

<font color="green" size="3px">1. 最老生常谈且容易理解的原因（指令重排序造成的对象不安全发布）</font>

当一个线程在创建单例对象时，其它线程可能看到未被完全构造的对象。这就是对象不安全发布造成的结果，对象引用和对象状态没有同时对其他线程可见。更确切地说，由于第8行代码  <font color="blue" >instance = new Singleton();</font>  内部的指令可能被编译器或处理器重排序，导致其他线程可能在单例对象还未被完全构造时就得到了单例对象的地址。  <font color="blue">instance = new Singleton();</font>  对应的字节码如下

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

线程A率先调用getInstance方法来创建单例对象，  <font color="blue" >instance = new Singleton();</font>  内部指令invokespecial与putstatic重排序（即图中A2与A3步骤被重排序），当A3执行完以后，线程B开始执行getInstance方法，此时instance引用已经指向尚未初始化的单例对象地址，因此如果线程B此时读取单例对象的field将会得到默认值而不是构造方法初始化后的值。

上面的解释看似很合理，但是却回避了一个小问题。前文提到过对象安全发布的四种方法，其中第四种说可以利用锁来实现安全发布，DCL明明符合要求在发布对象时用锁同步了，为什么仍然不能保证安全发布对象，使得对象引用和对象状态同时对其他线程可见？而且A1, A2, A3明明都在同步语句块内部，同步语句块所保护的操作应该具有原子性，为什么中途还会被线程B的B1,B2操作打断？

原因其实很简单：DCL并没有对共享对象进行“合适地加锁“，它只对“写”共享对象的操作加锁，却没有对所有“读”共享对象的操作加锁，换言之，DCL仅仅保证了”写“共享对象的操作和另一个”写“共享对象的操作之间之间的互斥性（原子性），却无法保证”写“共享对象的操作和”读“共享对象的操作之间的互斥性（原子性）。 或者更直白些，B1，B2操作根本没有被加锁，它们根本不与A1, A2, A3互斥，当然可以打断A1, A2, A3的执行。                            

对象安全发布的四种方法中的最后一种：“storing a reference to it into a field that is **properly guarded** by a lock”，注意这种安全发布方法要求保存单利对象引用的域被**合适地加锁**。何谓对对象状态“合适地加锁”？这里引用《Java Concurrency In Practice》中的两段话来解释：

> For each mutable state variable that may be accessed by more than one thread, all accesses to that variable must be performed with the same lock held. In this case, we say that the variable is guarded by that lock.			

> Locking is not just about mutual exclusion; it is also about memory visibility. To ensure that all threads see the most up to date values of shared mutable variables, the reading and writing threads must synchronize on a common lock.

**简言之，对共享对象状态合适地加锁，不仅需要对所有“写”该对象状态的操作加锁，还需要对所有“读”该对象状态的操作加锁**。之所以“合适地加锁”可以保证对象安全发布，原因在于对所有“写”和“读”该对象状态的操作加锁可以保证：

1. 一个线程中”读“ 共享对象的操作对于另一个线程中”读”共享对象的操作具有互斥性（原子性）
2. 一个线程中”读“ 共享对象的操作对于另一个线程中”写”共享对象的操作具有互斥性（原子性）
3. 一个线程中”写“ 共享对象的操作对于另一个线程中”写”共享对象的操作具有互斥性（原子性）

这样，根据第二条和第三条，我们可以推出，“合适地加锁”可以保证一个线程还在创建共享对象时（”写”共享对象的操作），另一个线程不能同时访问未创建好的共享对象（”读”或“写”共享对象的操作），因此可以保证共享对象的安全发布。然而，我们在平时写程序时却经常进入一个误区：只有“写”共享对象的操作才需要加锁。DCL正是犯了这个错误，只对A2，A3等“写”共享对象的操作加锁，而没有对B1,B2等“读”共享对象的操作加锁，无法满足第二条原子性，“写”共享对象的操作（如A2, A3）对于另一个线程“读”共享对象的操作（如B1，B2）并不具备原子性，这也合理解释了之前的问题：“A1, A2, A3明明都在同步语句块内部，同步语句块所保护的操作应该具有原子性，为什么中途还会被线程B的B1,B2操作打断”。DCL中，一个线程还在创建共享对象时（”写”共享对象的操作），另一个线程可以同时访问未创建好的共享对象（”读”共享对象的操作），因而共享对象不能保证安全发布。

> 这里额外补充一个对于java多线程环境下原子性的定义：原子性（又被称为互斥性）是一种相对性的概念而非一种绝对的定义，我们无法在没有任何对比，没有任何参照系的情况下孤立地判断某个操作是否是原子操作。一个操作A只有在另一个访问共享状态的操作B的观察下才能判断该操作是否是原子的。因此，一个操作可能对于某些操作是原子的，但是对于另一些操作就可能是非原子的了。具体要看程序中如何加锁。更多关于原子性的讨论可以参见另一篇博文[【Java Primer - Concurrency】Thread Safety & Actomicity & Visibility & Object  Sharing]()中的Actomicity的分析。

<font color="green" size="3px">2. 较为隐蔽的原因（指令重排序造成方法返回失效值）</font>

DCL除了不安全发布对象之外，还有可能因为指令重排造成其他问题。为了方便阅读，这里再贴一次DCL的代码

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

很多人可能会忽略，第5行代码和第12行代码可能会被重排序。

啥？这可是条件判断语句和返回语句，这也能重排序？Are you kidding me?

还是直接看字节码，第5行代码“if(instance == null){”对应的字节码

```java
 0: getstatic     #2                  // Field instance:Lsingleton/Singleton;
 3: ifnonnull     37
```

第5行代码实际上就两个指令：读instance引用 + 判断跳转

第12行代码“return instance;”对应的字节码

```java
 37: getstatic     #2                  // Field instance:Lsingleton/Singleton;
 40: areturn
```

类似地，第12行代码也只有两个指令：读instance引用 + 返回

第5行和第12行都涉及到读instance引用的操作，这两个操作不存在任何数据依赖性（不熟悉的童鞋请参见[http://www.infoq.com/cn/articles/java-memory-model-2](http://www.infoq.com/cn/articles/java-memory-model-2)），因此这两个读操作可以被重排序。

那么DCL的getInstance方法重排序后可能等效于：

```java
 public static Singleton getInstance(){
    Singleton tmp = instance; //原本第12行中的读instance引用的操作被重排序到原来第5行代码之前
    if(instance == null){
      synchronized(Singleton.class){
        if(instance == null){
          instance = new Singleton();
        }
      }
    }
    return tmp;
	}
```

这样遇到下面这种情况就会出现线程安全问题：

线程X先执行getInstance()，此时instance还是null，刚赋值给tmp后，切换到线程Y执行getInstance方法，执行完后再切回线程X。但是此时instance已经不再是null了，

 尽管这里说有两种原因造成DCL线程不安全，但是究其根本，这两种原因都是由于指令重排序导致的问题。DCL专注于解决共享对象的竞态条件，保证了Check-Then-Act对于其它线程“写”共享对象的原子性，却忽略了     “读”原子性

指令重排序带来的。第一种由于  <font color="blue" >instance = new Singleton();</font>  内部指令重排序造成对象不安全发布，第二种由于互不依赖的load指令重排序造成返回失效值。



针对上面第一种原因（不安全发布的问题），有人想出了DCL的加强版，姑且称其为Double Checked and Double Locking，似乎可以保证对象安全发布。

```java
public class Singleton{
  private static Singleton instance;
  private Singleton(){}
  public Singleton getInstance(){
    //第一次checked
    if(instance == null){
	//第一次locking
      synchronized(Singleton.class){
        Singleton tmp = instance;
        //第二次checked
        if(tmp == null){
          //第二次locking
          synchronized(Singleton.class){
         	 tmp = new Singleton();
			}
          instance = tmp;
        }
      }
    }
    return instance;
  }
}
```

这种方法



想要杜绝指令重排序造成的线程安全问题，内存屏障和锁以及final变量都是可能的解决办法

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link

[http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html](http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html)

两种结局方案： volatile  vs double checked and double locking

http://www.cnblogs.com/coffee/archive/2011/12/05/inside-java-singleton.html#out-of-orderWrites





将instance标记为volatile的变量可以完全解决上面的困境（JDK 5.0以后才能放心使用volatile来解决DCL的问题），如果对volatile的实现原理不太了解，可以移步另一篇博文[【Java Primer】从volatile到指令重排序]()

volatile可以禁止局部重排序，解决了DCL的两种困境



### 4. 内部类(Nested Initialization, Lazy Initialization)

```java
public class Singleton{
  private Singleton(){}
  static class InnerSingleton(){
    public static final Singleton instance = new Singleton();
  }
  public static Singleton getInstance(){
    return InnerSingleton.instance;
  }
}
```



### 5. 枚举法(Enum Based Singleton)





http://codebalance.blogspot.tw/2010/08/singleton-pattern-and-beyond.html

## 线程安全

前面已经对每种单例模式的实现方法进行了线程安全分析，在这里做一个总结的。





适用情况：


<!---
## 破解方法

除了枚举实现的单例模式，其他的四种实现方法都可以被破解。所谓破解也就是使得应用中出现单例类两个或两个以上的对象。主要有反射破解，序列化和克隆破解这三种破解方法。

## 垃圾回收

http://blog.csdn.net/zhengzhb/article/details/7331354

https://www.zhihu.com/question/51014592

## 运行性能

-->

## Reference

http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization?utm_source=infoq&utm_campaign=user_page&utm_medium=link

[http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html](http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html)

http://spiritfrog.iteye.com/blog/214986

https://yq.aliyun.com/articles/11333

http://blog.csdn.net/zhengzhb/article/details/7331369

http://blog.csdn.net/zhengzhb/article/details/7331354

http://ifeve.com/from-singleton-happens-before/

http://codebalance.blogspot.tw/2010/08/singleton-pattern-and-beyond.html

https://zhuanlan.zhihu.com/p/25733866

[《设计模式之禅》]()