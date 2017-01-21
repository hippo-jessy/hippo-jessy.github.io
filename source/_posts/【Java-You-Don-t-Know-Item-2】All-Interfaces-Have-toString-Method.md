---
title: 【Java You Don't Know - Item 2】All Interfaces Have toString() Method
date: 2017-01-22 00:30:29
categories: [Java, Java You Don't Know]
tags: [Java]
description:
---

## Introduction



最近总结**Thinking in Java 读书笔记**时，涉及到下面这段简单代码：

```java
Collection<String> list = new ArrayList<String>();
Collections.addAll(list, "tomorrow","hi","yes");
//内部调用list.toString方法
System.out.print(list);
```

上面这段代码的运行结果如下：

```java
[tomorrow, hi, yes]
```

进而引出了两个问题：

- Collection是一个接口，其内部并没有toString方法，为什么声明为Collection类型的list对象可以调用toString方法？

- list对象的toString方法明显被重写过了，重写toString方法是在哪里实现的？

<!-- more -->

## Solution



首先解决第二个问题：

​       ArrayList的继承关系是 ArrayList -> AbstractList -> AbstractCollection。而AbstractCollection中重写了toString方法，具体实现如下：

```java
 public String toString() {
        Iterator<E> it = iterator();
        if (! it.hasNext())
            return "[]";

        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (;;) {
            E e = it.next();
            sb.append(e == this ? "(this Collection)" : e);
            if (! it.hasNext())
                return sb.append(']').toString();
            sb.append(',').append(' ');
        }
    }
```

 然而这个解答并不能解决全部问题，就算是ArrayList中的toString方法已经通过继承父类得到重写，ArrayList创建出的对象被向上转型赋值给了Collection类型的list引用，于是又绕回到第一个问题了，Collection接口源码中没有toString方法，为何list对象可以调用toString方法？

下面这张图通过Eclipse的自动补全工具给我们提供了一点线索：

![All%20Interfaces%20Have%20toString%28%29%20Method](http://ojnnon64z.bkt.clouddn.com/All%20Interfaces%20Have%20toString%28%29%20Method.png)

可以看出，其实list调用的是Object中的toString方法。实际上Collection中有toString方法，只不过是隐式添加的。

个中原因简而言之，所有接口都会有对应于Object类中public实例方法的抽象方法。也就是说所有接口都会有toString,  hashCode, wait, notify, getClass, equals等方法。Java Language Specification 中的原话如下：

```
If an interface has no direct superinterfaces, then the interface implicitly declares a
public abstract member method m with signature s, return type r, and throws clause t
corresponding to each public instance method m with signature s, return type r, and
throws clause t declared in Object, unless a method with the same signature, same return
type, and a compatible throws clause is explicitly declared by the interface.
```

总结一下整个过程，Collection中没有显式声明toString方法，因此会隐式添加对应于Object类中toString的同名抽象方法，```System.out.println(list)``` list调用Collection接口中的toString方法，list实际类型为ArrayList, 由于动态绑定（此处涉及多态），调用的是ArrayList实例对象中的toString方法，ArrayList中并没有重写toString方法，又因为ArrayList的超父类AbstractCollection重写了toString方法，因此最后调用的是AbstractCollection 中的toString方法。从而实现了打印Collection所有元素的最终效果。



由此进行一下拓展，如果接口中显式声明了toString等方法又会怎样呢？此时，实现该接口的类不会被强制要求实现toString方法，原因很简单，所有的类都已经通过继承Object类实现了toString方法。因此，在平时coding的时候，如果想在接口中定义有效的强制被实现的抽象方法，最好避免与Object类中public实例方法重名。



## Reference

[http://stackoverflow.com/questions/12124163/do-interfaces-have-tostring-method](http://stackoverflow.com/questions/12124163/do-interfaces-have-tostring-method)