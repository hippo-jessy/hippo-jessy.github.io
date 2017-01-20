---
title: Exception-and-Error
date: 2017-01-19 01:03:54
categories:
tags:
description:
---

Throwable

- Exception
- Error

Exception 和 Error的区别：





try catch finally return执行顺序

try -> catch(如果catch block中有return语句，则先给返回值赋值，如果没有finally, 则赋值后直接返回，否则继续执行finally后再返回) -> 执行finally(如果finally block中有return语句，则给返回值赋值并直接返回)

总结下来，顺序如下：

1. 执行try catch block, 如果有return则先给返回值赋值，如果没有finally block则直接返回，否则进入下一步；
2. 执行finally, 如果有return则给返回值赋值并返回；
3. 如果此时程序仍未返回，并且try catch block中有return语句，则此时返回。

注意： finally block中一般不要加return 语句



override

== 重写方法的签名==被重写方法

<= <= 重写方法的返回值类型<=被重写方法； 重写方法抛出的异常<=被重写方法

\>= 重写方法的访问权限应\>=被重写方法的访问权限



总结：

1. 类图 Throwable Exception Error  CheckedException RuntimeException UncheckedException
2. 五个关键词 try catch finally thows thow 
3. catch 处理范围小的异常， 再处理范围大的异常
4. override关于异常的限制