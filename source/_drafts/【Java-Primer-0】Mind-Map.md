---
title: 【Java Primer-0】Mind Map
date: 2016-11-20 15:20:17
categories: [Java, Java Primer, Guideline]
tags: [Java]
description:
---

单开一个[博客系列【Java Primer】](http://hippo-jessy.com/categories/Java/Java-Primer/)，专门用来系统总结《Thinking in Java》《Core Java》《Java Concurrency in Practice》等书的读书笔记和感悟。其中对于书中内容的总结，统一采用Mind Map（单纯复述书中的内容没有太大意义，使用思维导图总结更加清晰全面）的形式整理在本文中，用作【Java Primer】系列的开篇，帮助自己整理思路；自己的感悟和延伸思考，将记录在[博客系列【Java Primer】](http://hippo-jessy.com/categories/Java/Java-Primer/)的后续文章中。

本文主要用来统一整理Mind Map以及相关博文的目录整理，持续更新中。

<!-- more -->

## Java Primer





## RTTI

反射，虽然可以提高程序灵活度，但是会降低程序运行效率(是普通调用的30？400？倍，可以通过禁止安全检查来提高效率，大约节省一半的时间)

```java
@Table(value = "tb_student")
public class Student {
    @Field(columnName = "id", type = "int", length = 10)
    private int id;
    @Field(columnName = "name", type = "String", length = 10)
    private String name;
    @Field(columnName = "age", type = "int", length = 3)
    private int age;

    public Student() {
    }

    public Student(int id, String name, int age ) {
        this.id = id;
        this.age = age;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}


public class Client {
    public static void test01() {
        Student student = new Student(200, "Jessy", 22);
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < 1_000_000_000; i++) {
            student.getName();
        }
        long endTime = System.currentTimeMillis();
        System.out.println("normal method invoked for one billion times takes " + (endTime - startTime) + " ms");
    }

    public static void test02() {
        try {
            Class studentClass = Class.forName("Annotation.Student");
            Method getName = studentClass.getDeclaredMethod("getName", null);
            Constructor studentConstructor = studentClass.getConstructor(int.class, String.class, int.class);
            Object student = studentConstructor.newInstance(200, "Jessy", 22);
            long startTime = System.currentTimeMillis();
            for (int i = 0; i < 1_000_000_000; i++) {
                getName.invoke(student, null);
            }
            long endTime = System.currentTimeMillis();
            System.out.println("reflection method with safety check invoked for one billion times takes " + (endTime -
                    startTime) + " ms");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void test03() {
        try {
            Class studentClass = Class.forName("Annotation.Student");
            Method getName = studentClass.getDeclaredMethod("getName", null);
            getName.setAccessible(true);
            Constructor studentConstructor = studentClass.getConstructor(int.class, String.class, int.class);
            Object student = studentConstructor.newInstance(200, "Jessy", 22);
            long startTime = System.currentTimeMillis();
            for (int i = 0; i < 1_000_000_000; i++) {
                getName.invoke(student, null);
            }
            long endTime = System.currentTimeMillis();
            System.out.println("reflection method without safety check invoked for one billion times takes " +
                    (endTime - startTime) + " ms");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Client.test01();
        Client.test02();
        Client.test03();
    }
}
```

运行结果：

```java
normal method invoked for one billion times takes 6 ms
reflection method with safety check invoked for one billion times takes 2503 ms
reflection method without safety check invoked for one billion times takes 1273 ms
```



## Generics(泛型)





## Concurrency

Java并发编程这一部分的思维导图主要根据《Java Concurrency in Practice》一书的结构来进行总结。主要分为基础知识，结构化并发应用，活跃性/性能/测试，以及高级主题四个部分。

### Fundamentals(基础知识)

