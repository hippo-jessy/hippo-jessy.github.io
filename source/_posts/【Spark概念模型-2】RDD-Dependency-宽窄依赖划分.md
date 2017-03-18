---
title: 【Spark概念模型-2】RDD & Dependency & 宽窄依赖划分
date: 2016-08-15 12:45:41
categories: [Spark, Spark概念模型]
tags: [Spark]
description:
---

## RDD

RDD是由诸多partition所构成的分布式只读数据集以及相关算子的封装，它只是一个逻辑概念上的数据集而并非是一个将所有数据都载入内存的数据结构（这里只是简单提一下RDD，在另一篇博客详细讲解RDD的概念，本文重点在于Dependency）。

## Dependency

Dependency描述了RDD之间的依赖关系，每个RDD内部都记录了它与其他RDD（parent RDD）的依赖关系。通过Dependency类的getParents(partitionId:Int)我们可以获取当前RDD的每个partition所依赖的parent partitions。

<!-- more -->

RDD之间的依赖关系可以分为Narrow Dependency和Shuffle(Wide) Dependency。到底应该如何区分RDD之间的关系是宽依赖还是窄依赖？

这主要取决于parent RDD的一个partition被child RDD的多少个partition所利用：如果parent RDD的每一个partition最多只会被child RDD的一个partition利用，则父子RDD之间的关系为窄依赖，相反，如果被child RDD的多个partition利用，则为宽依赖。

这种定义无疑是正确的，但是并不是很形象

现在把每一条数据看做是一个带有序号和颜色的小球（序号可以重复），将partition看做是放小球的盒子（盒子也有序号且序号不重复），一个RDD是指一个持有多个盒子的人。每个人都有自己放置小球的策略，将partitioner看做是人将小球放置到盒子中的策略（比如常见的HashPartitioner)，而且每个人根据自己的职业都有自己对小球处理的喜好。现在进行盒子传递（一个人把盒子给另一个人）。传递盒子的人是父RDD,接受盒子的人是子RDD，由于接受盒子的人有自己的处理喜好和放置小球的策略，因此凡是进行了盒子传递必定会进行小球的处理和重新放置（相当于transformation）。

> "不同的算子会产生不同的RDD"，这句话其实并不是那么准确，我们知道每个RDD都有compute方法，但是不同的RDD对应的compute实现并不相同（如MappedRDD的compute方法里对每一条数据进行了map操作，相当于在RDD内部包含了算子定义的操作，详见[RDD源码解析](../Spark源码分析/RDD源码解析)）。因此，个人觉得这句话改成不同的RDD带有不同的算子更为恰当。同理，RDD中有一个属性partitioner，因此，分区策略也是RDD的固有属性。

对应于现在的场景，不同的人根据自己的职业有不同的处理小球的喜好，且有自己放置小球的策略，对应于不同的RDD带有不同的算子，且传入了不同的partitioner。

其实上面的比喻也可以帮助我们更好地理解RDD，如果我们想在一群人之间传递盒子以便让不同职业的人对盒子中的小球进行处理（此过程相当于将一系列partition中的数据用不同算子处理以得到目标结果），则对于每个人我们至少需要五个信息：当前人所持有的所有盒子的列表，当前人对小球的处理喜好，传递盒子给当前人的人是哪些人，当前人对小球的放置策略，以及当前人放置盒子的地点  

这恰好和[RDD的概念理解](./RDD的概念理解)中提到过RDD类的五个重要特征相对应：  
1、partitions的列表（“当前人”所持有的盒子列表)  
2、compute方法来计算iterator（“当前人”对小球的处理喜好）  
3、getDependencies(传递给“当前人”盒子的人有哪些)  
4、partitioner（“当前人”放置小球的策略）  
5、getPreferredLocations（“当前人”放置盒子的位置）

现在有一个人持有多个箱子，他按照放置策略A放置好了小球，你可以选择让他把箱子传给下面不同职业的人

将算子作用于小球的变化过程看做是如下操作：  

> eg：  
> map() -> 当做是给小球涂色 -> 对应于MappedRDD，相当于将盒子传递给了一个画匠  

> filter() -> 当做是从盒子里取出小球扔掉  -> 对应于FilteredRDD，相当于将盒子传递给了一个投手。。。想不到更合适的职业了。。。 

> union(rdd) -> 当做是将多个小盒子合成一个大盒子（所有被合并小盒子的编号均可看做合并后大盒子的编号）-> 对应于UnionRDD，相当于将盒子传递给了一个装箱工人 
>
> join(rdd,partitioner) -> 当做是将号码相同的小球（不管是不是在一个盒子里）熔成一个大球，并根据放置策略partitioner重新放置 -> 相当于将盒子传递给了一个铁匠 

如果经过上述某个操作后，对于所有留下来的小球，如果原来在同一个盒子里的小球现在全部还在同一个盒子里，则为窄依赖；如果任何一个小球和原来在同一个盒子里的其他小球分开了，则为宽依赖。 通俗一点来说，不管被传递的人怎么折腾，原本在同一个盒子里的小球都还在一个盒子里（或者衍生的大盒子），这个传递关系就是窄依赖；否则，则是宽依赖。  

逐一看一下上面列举的算子，显然，map和filter是窄依赖，因为都只是简单的传递了盒子，对单个小球涂色或扔掉，并没有传入新的partitioner，即接收盒子的人并没有对小球进行重新放置。因此所有小球都待在自己原来的盒子里，显然是窄依赖。对于union，也是窄依赖，因为每个小球都会在原来小盒子所衍生的大盒子中。

### join

对于join(rddB)既可能是窄依赖，也有可能是宽依赖，实际上讨论join是宽依赖还是窄依赖其实相当于讨论cogroup，可以参看下面源码可知，join内部是调用cogroup实现的

```scala
 def join[W](other: RDD[(K, W)], partitioner: Partitioner): RDD[(K, (V, W))] = {
    this.cogroup(other, partitioner).flatMapValues( pair =>
      for (v <- pair._1; w <- pair._2) yield (v, w)
    )
  }
```

我们需要分情况讨论：  

#### 窄依赖join

想要窄依赖，则必须保证原来同一个盒子里的球传递个另一个人之后依然在同一个盒子里。

如果传递盒子的人和接受盒子的人有相同的放置小球的策略，并且传递盒子的人和接受盒子的人的盒子数目相同，则join为窄依赖，否则为宽依赖。比如传递者A和传递者B（rddB）两人都采用了HashParitioner（比如用小球的序号对盒子的序号取余），则二人所持有的相同序号的小球一定放在序号相同的盒子里，join之后接受盒子的人也使用同样的HashParitioner，则熔成的打球一定还会被放置在序号相同的盒子里，这样看来，原本放在盒子1中的小球最后一定还是会被放置在盒子1中。（如后文图中的join with inputs co-partitioned）

#### 宽依赖join

大多数情况的join都是宽依赖，第一个人将相同序号的球打散放置在不同的盒子里，传递给第二个人之后，如果采用不同的放置策略，基本都会使原本在同一个盒子里的球分散到不同的盒子中去。

这种区别也就是我们常见的join with inputs co-partitioned 和 join with inputs not co-partitioned(如下图所示)

> 下图中的 join with inputs co-partitioned 对应于上述窄依赖的情况3
> 图中涉及到一个人向另一个人传递盒子以及两个人向第三个人传递盒子的情况

![](http://ojnnon64z.bkt.clouddn.com/【Spark概念模型-2】RDD%20&%20Dependency%20&%20宽窄依赖划分.png)

实际上我们也可以从源码角度来看如何区分cogroup是否为宽依赖，cogroup方法实际上创建了CoGroupedRDD，该RDD的getDependencies方法如下：

```scala
 override def getDependencies: Seq[Dependency[_]] = {
  //rdds是CoGroupedRDD的父RDD列表，part是CoGroupedRDD的partitioner
    rdds.map { rdd: RDD[_ <: Product2[K, _]] =>
      if (rdd.partitioner == Some(part)) {
        logDebug("Adding one-to-one dependency with " + rdd)
        new OneToOneDependency(rdd)
      } else {
        logDebug("Adding shuffle dependency with " + rdd)
        new ShuffleDependency[K, Any, CoGroupCombiner](rdd, part, serializer)
      }
    }
  }
```



代码逻辑非常清晰，如果CoGroupedRDD和其父RDD有相同的partitioner则二者关系为窄依赖，否则为宽依赖。

## References

[http://smallx.me/2016/06/07/spark%E4%BD%BF%E7%94%A8%E6%80%BB%E7%BB%93/](http://smallx.me/2016/06/07/spark%E4%BD%BF%E7%94%A8%E6%80%BB%E7%BB%93/)  [https://github.com/JerryLead/SparkInternals/blob/master/markdown/2-JobLogicalPlan.md](https://github.com/JerryLead/SparkInternals/blob/master/markdown/2-JobLogicalPlan.md)  [https://github.com/JerryLead/SparkInternals/blob/master/markdown/3-JobPhysicalPlan.md](https://github.com/JerryLead/SparkInternals/blob/master/markdown/3-JobPhysicalPlan.md)