---
title: Summary for Sorting
date: 2017-02-20 22:59:05
categories: [Algorithm, Sort]
tags: [Algorithm, Java]
description:
---

​	这篇笔记集中主要对常见的八大排序算法的原理，复杂度以及稳定性比较。后续会在另开一篇博文专门分析java中的排序算法的实现。本篇博客的所有代码都可以在这个路径找到：[https://github.com/hippo-jessy/algorithm/tree/master/src/sorting](https://github.com/hippo-jessy/algorithm/tree/master/src/sorting)

## Overall

​	排序是一个大话题，下面这张图可以给我们一个较为宏观的概念：

![sort](http://ojnnon64z.bkt.clouddn.com/Java/Java%20Basics/Summary%20for%20Sorting/sort.png)

<!--more-->

​	排序主要分为内部排序和外部排序，其中内排是指只利用内存来进行排序，外排是指利用内存和辅存一起来排序。通常情况下，数据量比较小我们采用内排足够了。当数据量超出内存容量时，不得不借助外排来实现全排序。现在很多流行的分布式计算框架比如Hadoop, Spark等在对海量数据进行处理时都会用到外排。以后有空再专门开篇博客来讨论Hadoop以及Spark排序算法的实现。

​	这里只专注于讨论内部排序的**八大常见算法**，其它排序算法及它们的相关优化：

1. **冒泡排序(bubble sort)**
   - 一般冒泡排序(最佳时间复杂度O(n^2^))
   - 优化冒泡排序(最佳时间复杂度O(n))
2. **选择排序(selection sort)**
3. **直接插入排序(direct insertion sort)**
4. **希尔排序(shell sort)**
5. **归并排序(merge sort)**

   - 一般归并排序
   - 原地归并排序(in-place merge sort)
6. **快速排序(quick sort)**

   - 一般快速排序
   - 三路快速排序(quick sort with three-way)
   - 双枢纽快速排序(dual pivot quick sort)
7. **堆排序(heap sort)**
8. **基数排序(radix sort)**
9. **其它常见排序** 
   - 桶排序（Bucket Sort）
   - 计数排序（Counting Sort）


各种排序的性能对比如下表所示：
https://www.toptal.com/developers/sorting-algorithms



为什么要研究这么多的排序算法？为什么不使用一种算法一劳永逸？

各个算法有自己擅长的领域： 针对不同输入数据的特征地方，表现各有利弊



## Exchange Sort

​	交换排序，顾名思义，就是利用多次交换数值的方式来排序。交换并不是一个简单的一步到位的操作，实际上它相当于三个copy过程（如果使用临时变量来实现交换）。交换排序主要涉及到了bubble sort和quick sort两种算法。

### Bubble Sort

​	冒泡排序，核心原理是通过多次比较、交换使数组中的最大数交换到数组的最高位。基本思想和步骤如下：

1. 外轮循环从数组最大index开始依次确定当前乱序子序列中的最大数值放到有序子数列的正确位置，由后向前由大到小确定有序子数列，直到有序子数列覆盖整个数组序列。（外轮循环每执行一次，位于数组前部的较小数乱序子数列减少一个，位于数组后部的较大数有序子序列增加一个）
2. 内层循环从乱序子数列的最小位开始，不断比较相邻的两个数，遇见较大数则使之通过交换上升到较大index的位置，直到到达当前乱序子序列的index最大位。

```java
public class BubbleSort {
	@Test
	public void testBubbleSort() {
		int[] a = new int[] { 4, 19, 345, 1, 0, 90, 24, 12, 3, 4, 31, 10, 28, 19 };
		bubbleSort(a);
		System.out.println(Arrays.toString(a));
	}

  	/**
	 * Bubble sort implementation  
	 * @param data the array to be sorted
	 */
	public static void bubbleSort(int[] data) {
		for (int i = data.length - 1; i > 0; i--) {
			for (int j = 0; j < i; j++) {
				if (data[j] > data[j + 1]) {
                  	//swap data[j] and data[j+1]
					data[j] ^= data[j + 1];
					data[j + 1] ^= data[j];
					data[j] ^= data[j + 1];
				}
			}
		}
	}

}
```

**时间复杂度：** 最佳情况O(n^2^)，一般情况O(n^2^)，最差情况O(n^2^)

**空间复杂度：** O(1)

**稳定性：** 稳定

#### 优化

上述代码还可以进行优化，前文也提到过对排序算法进行优化可以从几方面来考虑，但是这里只是基于冒泡排序的主体逻辑进行一些小的优化，因此可以从输入数组的特征入手，考虑优化策略。

由于冒泡排序根据不断比较相邻元素大小并换位来实现“子序列最大数“上升的目的，我们可以利用不断比较相邻元素这一步骤判断出子序列自身是否是有序的：如果子序列相邻元素的比较过程全部完成以后，没有任何元素需要交换，也就说明了子序列是有序的，于是也就没必要再对该子序列的子序列进行进一步冒泡排序了。

这种优化可以使得**最佳情况（输入的待排序数组本身为有序数组的情况）的时间复杂度降低到O(n)**，也可以很大程度提高特定情况下（输入的待排序数组靠前的子序列有序，例如1，2，3，4，9，8）的排序效率，其他情况时间复杂度不变

```java
	/**
	 * Optimization version of bubble sort.
	 * 
	 * @param data
	 *            the array to be sorted
	 */
	public static void bubbleSortOptimization(int[] data) {
		boolean hasSwap = false;
		for (int i = data.length - 1; i > 0; i--) {
			for (int j = 0; j < i; j++) {
				if (data[j] > data[j + 1]) {
					data[j] ^= data[j + 1];
					data[j + 1] ^= data[j];
					data[j] ^= data[j + 1];
					hasSwap = true;
				}
			}
          	// add a flag to judge whether the array has been sorted.
			if (!hasSwap) {
				return;
			}
		}
	}
```



<br>

> 额外说明

​	此处使用了异或来实现两个数的交换，可以节约一个临时变量的存储空间（在bubble sort中使用异或交换数据不会有问题，但是在某些情况下使用异或实现数据交换存在风险，具体原因在Simple Selection Sort部分讲解），当然我们也可以用一个临时变量来帮助实现数的交换。排序过程大部分只用到了原数组的内存空间，并没有分配新的内存辅助排序(in-place sort 原地排序)，除了临时变量用来帮助数的交换, 这样**空间复杂度**为O(1)。

​ 这里额外提一下异或实现数的交换过程。按位异或的规则很简单，相同位数值相同则为0，数值不同则为1。异或运算满足交换律和集合律，**a^a=0 a^0=a**，实际上我们可以推导出一个规律，**偶数个相同数做异或运算得0，奇数个相同数做异或运算得到该数本身**。

​	使用异或运算来交换a和b变量数值的过程如下：

 ```
 a= a^b;
 b= a^b;
 a= a^b;
 ```

 过程实际上很清晰：使用交换律和集合律，综合运算过程实际为:

上述第二行代码展开： b=a ^ b ^ b = a ^ (b ^ b)=a ^ 0=a     （使用结合律）

上述第三行代码展开：a=a ^ b ^ ((a ^ b) ^ b) =( a ^ a ) ^ (b ^ b ^ b) = 0 ^ b = b	(使用交换律和结合律)

借助上面总结的异或运算规律，可以很快解决下面这道面试题：

**一个数组存放若干整数，一个数出现奇数次，其余数均出现偶数次，找出这个出现奇数次的数？**

​  答案很清晰了，直接将该数组所有元素一起做异或运算，得到的结果便是出现奇数次的数。

 其实除了异或来实现原地交换，我们还可以利用加减乘除来实现：

```java
 int a,b;
 //加减实现
 a = a + b;
 b = a - b;
 a = a - b;

 //乘除实现；
 a = a * b;
 b = a / b;
 a = a / b;
```

但是这两种方法都存在明显弊端：加和乘的过程可能出现溢出。

最后对稳定性进行分析，所谓稳定性即指排序前后，数值相同的数的前后相对次序保持不变。Bubble sort对于数的替换原则是：对于index小的数，只有当其数值大于index大的数的数值时，才会被交换。根据这个逻辑，对于数值相同的数，index较小的数排序之后index还是较小，因此bubble sort是稳定排序。

### Quick Sort

快速排序，运用了分治思想，简单来说就是选定一个元素作为锚点，将数组中大于该元素的数移到一侧，小于该元素的数移到另一侧，然后对每一侧的子数组递归进行快速排序。

该排序算法的核心在于如何将大于锚点元素的数移到数组的一侧，小于该元素的数移到数组的另一侧。这一部分主要靠**partition()** 方法来实现。

先上代码：

```java
public class QuickSort {

    public static void quickSort(int[] data, int low, int high) {
        if (low >= high || data == null || data.length <= 1) {
            return;
        }
        
        int index = partition(data, low, high);
        quickSort(data, low, index - 1);
        quickSort(data, index + 1, high);
    }
    
  // partition方法选取序列的第一个元素作为锚点，将数组按照锚点重新分好后，返回锚点应在的数组下标
    private static int partition(int[] data, int low, int high) {
        int left = low + 1;
        int right = high;
        while (true) {
            // 左指针始终指向数组从左向右找的第一个大于锚点的数(如果没有，则指向high+1)
            for (; left <= high && data[left] <= data[low]; left++) ;
            // 右指针始终指向数组从右向左找的第一个小于锚点的数(如果没有，则指向low)
            for (; right > low && data[right] >= data[low]; right--) ;
            if (left < right) {
                data[left] ^= data[right];
                data[right] ^= data[left];
                data[left] ^= data[right];
            } else {
             // 如果左侧指针大于等于右侧指针，则说明已经将大于锚点的数分在右侧, 小于锚点的数分在左侧
             // 现在只需将锚点和数组从右向左找的第一个小于锚点的数交换位置即可
                int tmp = data[right];
                data[right] = data[low];
                data[low] = tmp;
                return right;
            }
        }
    }
}
```

**时间复杂度：** 最佳情况O(nlogn)，一般情况O(nlogn)，最差情况O(n^2^)

**空间复杂度：** O(1)

**稳定性：** 稳定(要看代码的具体实现，对于前文的代码而言，是稳定的)

这里简单讨论下时间复杂度的推导：

**最佳情况：** 

当每次锚点都选择恰当，刚好平分数组，则时间复杂度推导公式为： T(n) = 2T(n/2) + n

T(n) = 2T(n/2) + n

T(n) = 2(2T(n/4) + n/2) + n = 4T(n/4) + 2n

T(n) = 4(2T(n/8) + n/4) + 2n =8T(n/8)  + 3n

……

T(n) = nT(n/n) + (logn) * n = nT(1) + nlogn = nlogn

**最差情况：** 

当带排序数组本身为有序数列时，每次选取的锚点都是的当前子序列的最小数，根本无法起到将数组一分为二的作用，则时间复杂度推导公式为： T(n) = T(n-1)  + n

T(n) = T(n-1) + n 

T(n) = (T(n-2) + n-1) + n = T(n-2) + n-1 + n

……

T(n) = 1 + 2 + … + n = O(n^2^)

**一般情况：** 

一般情况下锚点的选择不会像最佳情况那样刚好将数组一分为二。这里以1：9划分为例来分析，一般情况下的分析和最佳情况比较类似。递归深度为 $\log_{10/9} n$ 即O($\log n$)，而每次递归之前需要进行partition操作的复杂度一定小于等于cn，因此一般情况下的时间复杂度为O($n\log n$)。

#### 优化

针对带有较多重复元素的待排序数组，可以使用三路快排来对一般快速排序算法进行优化，避免重复元素进行不必要的反复递归排序；

针对一般待排序数组，可以使用双枢纽快排来对一般快速排序算法进行优化，使得锚点的选择更为合理。

##### 三路快排（three-way partition）

之前的一般快速排序直接利用锚点将数组切分为两个子数组（大于等于锚点的子数组和小于等于锚点的子数组）进行递归排序。然而对于重复元素较多的待排序数组，这种做法明显不妥：举个最极端的例子，数组里面的元素全相同，哪怕在partition()方法执行的时候我们依然需要将这些元素分成子数组进行递归排序，最后时间复杂度为最差情况的O(n^2^)。

对于带有较多重复元素的待排序数组，一般快速排序明显具有弊端。这里可以采用三路快排来进行优化。其核心思想是将数组划分为三个子序列：小于锚点的数，等于锚点的数，大于锚点的数，然后只对第一个和第三个子序列进行递归。这样避免了对重复元素进行递归。（具体讲解见下面的代码注释）

```java
public class QuickSort {
 /**
     * Quick sort with three-way.
     * This is an optimized version of general quick sort.
     * This version performs better and is used in preference to general quick sort
     * if multiple elements of the array have the same values.
     *
     * @param data
     * @param low
     * @param high
     */
    public static void threeWayQuickSort(int[] data, int low, int high) {
        if (data == null || low >= high) {
            return;
        }
        int[] index = threeWayPartition(data, low, high);
        threeWayQuickSort(data, low, index[0] - 1);
        threeWayQuickSort(data, index[1] + 1, high);
    }

    /**
     * The traditional 3-way partition, that is "Dutch National Flag" solution.
     *
     * @param data the array to be partitioned.
     * @param low  the index of the first element, inclusively, to be partitioned
     * @param high the index of the last element, inclusively, to be partitioned
     * @return the traditional 3-way partition
     * (or "Dutch National Flag") schema:
     * <p>
     * left part    center part              right part
     * +-------------------------------------------------+
     * |  < pivot  |   == pivot   |     ?    |  > pivot  |
     * +-------------------------------------------------+
     * ^              ^        ^
     * |              |        |
     * index[0]           p     index[1]
     * <p>
     * Invariants:
     * <p>
     * all in (left, index[0])   < pivot
     * all in [index[0], p)     == pivot
     * all in (index[1], right) > pivot
     * <p>
     * Pointer p is the first index of ?-part.
     */
    private static int[] threeWayPartition(int[] data, int low, int high) {
        int[] index = new int[2];
        int pivot = data[low];
        index[0] = low;
        index[1] = high;
        for (int p = low; p <= index[1]; ) {
            if (data[p] < pivot) {
                // Attention: p++
                swap(data, index[0]++, p++);
            } else if (data[p] > pivot) {
                swap(data, index[1]--, p);
            } else {
                p++;
            }
        }
        return index;
    }

    private static void swap(int[] data, int a, int b) {
        int tmp = data[a];
        data[a] = data[b];
        data[b] = tmp;
    }
}
```

三路快排的思想还可以用在很多其它的地方，比如可以先看一看leetcode这道题：

https://leetcode.com/problems/sort-colors/?tab=Description

**简单复述下题目：给一个数组，元素只可能为0，1，2，要你设计一个算法使得最后该数组中同样大小的元素一定相邻，并且大体上按照0，1，2的顺序排列。** 

很容易想到的解法是利用计数排序（Counting Sort，后文会专门讲解这种排序算法）的思想：先遍历一遍数组，然后统计出大小为0，1，2的元素各有多少个，然后再遍历一遍数组按照题目要求重新填充数组。

但是这样一来，需要遍历两遍数组。题目中的follow up要求只能遍历一遍数组，并且只能使用常数大小的空间。这里就可以用到三路快排的partition()方法中的思想： 选取1作为锚点数，用两个index划分数组为三个部分（小于1的部分，等于1的部分以及大于1的部分）。代码如下：

```java
public class Solution {
    public void sortColors(int[] nums) {
        if(nums == null || nums.length<=1){
            return;
        }
        int[] index = new int[2];
        int pivot = 1;
        index[0] =0;
        index[1] = nums.length-1;
        for(int p =0; p<=index[1];){
            if(nums[p]>pivot){
                swap(nums, index[1]--, p);
            }else if(nums[p]<pivot){
                swap(nums, index[0]++, p++);
            }else{
                p++;
            }
        }
    }    
    private void swap(int[] data, int a, int b){
        if(a != b){
            data[a] ^= data[b];
            data[b] ^= data[a];
            data[a] ^= data[b];
        }
    }
}
```

##### 双枢纽快速排序(dual pivot quick sort）

虽然三路快排可以解决重复元素较多的情况，却无法解决nearly sorted的待排序数组的困境：

对于本身就是有序数组的待排序数组，一般排序算法选取的锚点基本不会起到划分数组的作用，导致最后时间复杂度为O(n^2^) 。

一个好的锚点能够相对平衡地划分数组（当然最佳情况是1:1划分），这个锚点的大小最好就是数组所有元素的中位数的大小。那么如何才能理智地选择锚点？想要选择一个好的锚点，必须对数组元素的大小分布有所了解，而想要对整体数据特征进行了解，最常见的手段就是采样。双枢纽快排选择锚点时就采用了一定得技巧。

Java中默认的排序算法用到了快速排序，并且采用了双枢纽快排，考虑到文章篇幅，这里不对双枢纽快排的实现进行额外讲解，以后会用另外的博客专门探讨Java 8 中的排序算法的实现以及双枢纽快排的细节。

## Selection Sort

### Simple Selection Sort

​	简单选择排序实际上是将冒泡排序的排序思想，只不过不是将最大数通过连续相邻交换的形式推到最高index位，而是通过额外的变量保存最大数当前所在的index，只需要交换一次使最大数放在正确的位置上，这样一定程度上减少了交换的次数，提高了性能。然而实质上虽然交换操作的次数减少，但是比较操作的次数与冒泡排序基本一致，因此时间复杂度上并没有什么区别。

​	简单选择排序主要思路步骤如下：

1. 外部循环的作用和bubble sort外部循环的作用基本一致，不同的地方在于bubble sort的内部循环会将乱序子数列中的最大数通过连续交换上升到有序子数列中的正确位置，而简单选择排序的却需要通过外层循环的一次交换来将乱序子数列中的最大数放到有序子数列中的恰当位置。
2. 内部循环不同于bubble sort，简单选择排序的内部循环没有任何交换的操作，它只是通过遍历比较无序子数列，利用一个额外的变量记录了当前无序子数列中最大数的index，以便外部循环根据这个index来进行交换，通过外层循环的交换，确保该数放在有序数列的正确位置。

```java
	/**
	 * Simple selection sort implementation.
	 * 
	 * @param data
	 *            the array to be sorted
	 */
	public static void simpleSelectionSort(int[] data) {
		int indexFlag;
		for (int i = data.length - 1; i > 0; i--) {
			indexFlag = i;
			for (int j = 0; j < i; j++) {
				if (data[j] > data[indexFlag]) {
					indexFlag = j;
				}
			}
			int tmp = data[i];
			data[i] = data[indexFlag];
			data[indexFlag] = tmp;
		}
	}
```

​	**时间复杂度：** 最佳情况、一般情况和最差情况均为O(n^2^)。

​	**空间复杂度：** 和bubble sort类似，也为O(1)。

​	**稳定性：** 不稳定。

​	时间空间复杂度和bubble sort类似，这里主要讨论下简单选择排序的稳定性问题。一般来说只有相邻数之间交换的排序是稳定的，存在相差多个index的数交换的排序一般是不稳定的（这并不是一条普遍规律，只能用以参考）。简单插入排序的交换就是相差多个index的数的交换。不稳定的具体例子如下：

15，8，3^1^，2，3^2^

​	进行进行第一次外层循环操作时会得到最大数的indexFlag为0，则此时会交换15和3^2^,变成如下序列：

3^2^，8，3^1^，2，15

​	后面的步骤不再一一解释：

3^2^，2，3^1^，8，15

3^2^，2，3^1^，8，15

2，3^2^，3^1^，8，15 ——最终结果

​	可以看到在第一次交换时就已经发生了不稳定的情况，最后的结果也确实将3^1^和3^2^的次序改变了。

​	细心的读者应该可以注意到简单插入排序这里并未像冒泡排序那样使用异或来进行数据交换，原因是直接使用异或进行数交换会出现问题，比如下面代码在运行时得到的结果一定不正确：

```java
 //错误示范
 public static void simpleSelectionSort(int[] data) {
 		int indexFlag;
 		for (int i = data.length - 1; i > 0; i--) {
 			indexFlag = i;
 			for (int j = 0; j < i; j++) {
 				if (data[j] > data[indexFlag]) {
 					indexFlag = j;
 				}
 			}
 			data[i] ^= data[indexFlag];
 			data[indexFlag] ^= data[i];
 			data[i] ^= data[indexFlag];
 		}
 	}
```

```java
 //正确示范
 public static void simpleSelectionSort(int[] data) {
 		int indexFlag;
 		for (int i = data.length - 1; i > 0; i--) {
 			indexFlag = i;
 			for (int j = 0; j < i; j++) {
 				if (data[j] > data[indexFlag]) {
 					indexFlag = j;
 				}
 			}
           	//增加一个判断语句，确保不让同一个数组元素与自身发生异或交换
 			if (i != indexFlag) {
 				data[i] ^= data[indexFlag];
 				data[indexFlag] ^= data[i];
 				data[i] ^= data[indexFlag];
 			}
 		}
 	}
```

 ​	你发现问题的根源了吗？

 ​	当需要交换的两个数是同一个数时，异或交换会使该数变为0而不是得到该数本身。更准确地说，对同一块内存区域保存的内容进行异或交换时，会使该内存区域最终保存的值变为0。

 ​	结合上面的代码，当 **"i == indexFlag"** 为true时，其实交换过程就变成了：

```java
 data[i] ^= data[i];	//data[i] = data[i] ^ data[i] = 0
 data[i] ^= data[i]; //data[i] = 0^0 = 0
 data[i] ^= data[i]; //data[i] = 0^0 = 0
```

因此，为了避免上述情况的发生，当我们使用异或来对数据进行交换处理时一定要**事先保证不会出现同一个内存地址保存的值进行自身异或交换**。在bubble sort中，由于所有的交换都发生在相邻的数组元素中而不会发生同一个数组元素自身进行交换的情况，因而在bubble sort中进行异或交换是不会有任何风险的。

### Heap Sort



## Insertion Sort

​	插入排序， 

### Direct Insertion Sort

​	直接插入排序，原理和我们打扑克起牌时将牌排序的思想一致。或者更加贴切的说，和如下场景的思想一致：





​	虽然都是思路比较简单的排序算法，直接插入排序却似乎比选择排序以及冒泡排序的实现方法多样化一些。这里主要列出三种实现方式来讨论各自利弊：





将交换的部分换成copy来实现。因此相比冒泡排序节省了很多交换的步骤(一次交换相当于三次copy)，性能上会有所提升。



### Shell Sort



## Merge Sort

​	归并排序



### In-place Merge Sort



> 基于比较的排序算法性能上限分析
>
> dfsdf
>
> sdfds



## Radix Sort



## Other Common Sorting Algorithm

### Bucket Sort



### Counting Sort

https://leetcode.com/problems/find-all-duplicates-in-an-array/?tab=Description

## Optimisation Strategy

### Overall Optimisation

#### Time Optimisation

#### Space Optimisation



整体性优化

### Optimisation based on Specific Features of Input Array

针对特定输入数组特征的优化

比如对bubble sort 的优化



## Performance

这里对本文讨论过的所有排序算法的性能分析进行总结：

|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |



## Reference

\[1] [https://www.toptal.com/developers/sorting-algorithms](https://www.toptal.com/developers/sorting-algorithms)
