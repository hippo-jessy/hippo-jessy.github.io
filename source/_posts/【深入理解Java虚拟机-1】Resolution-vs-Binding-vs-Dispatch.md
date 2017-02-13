---
title: 【深入理解Java虚拟机-1】Resolution vs Binding vs Dispatch
date: 2017-02-13 23:18:13
categories: [JVM, 深入理解Java虚拟机]
tags: [JVM, Java]
description:
---

最近总结《深入理解Java虚拟机》方法调用相关内容时，发现对下面这几个概念理解有偏差：

Resolution, Static Binding/Dynamic Binding, Static Dispatch/Dynamic Dispatch, Single Dispatch/Multiple Dispatch

其中最容易产生混淆的是Binding和Dispatch这两个概念，本篇博客会从一般角度以及Java的角度来分析上述几种概念的差别，并对“JVM方法调用“这一话题展开一些延伸思考和讨论。

<!-- more -->

在开始讨论之前，需要明确下面几个概念：

**1. Static Type(Apparent Type) 静态类型（外观类型）， Actual Type（实际类型）**

二者的区别用一个例子就能解释：

```java
Person sample = new Man();
```

这里，sample变量的静态类型（编译时类型）是Person， 实际类型（运行时类型）是Man

**2. 方法的接收者(Receiver)**

```java
Person man = new Man();
man.speak();
```

上例中，对象man就是speak()方法的所有者，也是speak()方法的接收者

**3. 属性的所有者**

```java
//		class Person{
//  		String name = "unknown";
//		}

Person man = new Man();
System.out.println(man.name)
```

上例中, 对象man是属性name的所有者

**4. 宗量**

方法的接收者和方法的参数统称宗量，主要在单分派和多分派中用到这个概念，单分派是仅根据一种宗量（比如方法的接收者）对方法进行选择，多分派是根据多种宗量对方法进行选择。

**5. Java中的 虚方法 vs 非虚方法**

非虚方法主要包括invokestatic和invokespecial指令调用的方法以及final方法，即类方法，私有方法，构造器，final方法等。个人将其理解为无法被重写的方法集合。

虚方法主要包括invokevirtual指令调用的方法（除了final方法），即不用final修饰的实例方法。

## Resolution

Resolution, 解析是指**将符号引用替换为直接引用的过程**，JVM Specification并未规定其发生时间，只是规定在下面十六条指令执行前必须完成这些指令涉及的符号引用的解析: 

new, getstatic, putstatic, invokestatic, getfield, putfield, invokespecial, invokevirtual, invokeinterface, invokedynamic, anewarray, multianewarray, ldc, ldc_w, checkcast, instanceof。

一般来说，解析可以发生在两个时间段：类加载时期和符号引用将被使用时。其中，invokedynamic必须等到指令执行时才能进行解析动作，其它指令都可以随意选择两个时间段中的一个（根据虚拟机的具体实现而定）。通常，非虚方法的解析都在类加载时期完成了。

## Binding

绑定是针对**类型**而言的，指的是类型确定的过程，**通常发生在访问对象成员或者方法调用的过程中**。当我们谈论方法或属性的访问时动态绑定还是静态绑定时，实际上指的是方法的**接收者**和属性的**所有者**的**类型确定**（determine by atual type or determine by static type）。

根据类型确定发生在运行期还是编译期以及依据实际类型还是静态类型，可以将Binding分为Dynamic Binding和Static Binding两类。下面这个经典的例子反映了二者的区别。

```java
class Person{
  int age = 30;
  int getAge(){
    return age;
  }
}
class Man extends Person{
  int age = 40;
  int height = 160;
  int getAge(){
    return age;
  }
}

public class Demo{
  public static void main(String[] args){
    Person a = new Man();
    //	a.age内部主要通过如下字节码实现：
    //	getfield      #5                  // Field test/Person.age:I
    System.out.println(a.age);
    //	a.getAge()内部主要通过如下字节码实现：
    //	invokevirtual #7                  // Method test/Person.getAge:()I
    System.out.println(a.getAge());
  }
}
```

输出的结果如下：

```java
30
40
```

这个例子实际上涉及了很多本篇博客要讨论的概念：静态绑定，动态绑定，属性隐藏，方法重写，动态分派，单分派等等，这里主要从静态绑定和动态绑定的角度进行分析。

### Static Binding

类型在编译期就已经可以确定，并且该类型确定在运行期保持不变，即**最终**通过静态类型确定该变量类型。Java中，静态绑定通常用于属性所有者的类型绑定，非虚方法（类方法，私有方法，构造器方法，final方法）接收者的类型绑定，以及方法参数的类型绑定。

**上例中，age属性是对象属性，age属性的所有者（对象a）在此次访问中是静态绑定**，因此这里对象a的类型在编译期被确定为a的静态类型Person，并且该类型确定后在运行期执行getfield指令时也不会发生改变，最后"a.age"调用的是a的静态类型Person的age属性值。这里也涉及到了属性隐藏的问题：父类和子类有同名域时，域的访问是通过域的所有者的静态类型决定的。比如上面例子中如果想访问子类Man中的age，则必须将对象a强制转型为Man，或者在当时创建之初就声明为Man类型而非Person类型。

通过静态绑定来实现访问对象属性所有者类型绑定的**好处**在于：编译期就可以确定最终类型，避免了动态查找，高效快速，但是是以牺牲一部分灵活性为代价的。

### Dynamic Binding

类型在运行时才能最终确定，通过**最终**实际类型（运行时类型）来确定变量类型。Java中，动态绑定通常用于虚方法（如非私有的实例方法等）接收者的类型绑定。

某些动态类型语言将动态绑定作为默认的内部实现。Java作为一种静态类型语言，采取了一些其他的方法来实现动态绑定（比如invokevirtual指令动态识别对象的实际类型）。

**上面例子中，getAge()属于虚方法， getAge()方法的接收者（对象a）在此次访问中是动态绑定**，因此这里对象a的类型尽管在编译期被标记为Person，最后在运行期会被invokevirtual指令重新确定为a的实际类型Man，并在Man中查找能够匹配符号引用中方法名和描述符的方法，因此"a.getAge()"调用的是a的实际类型Man的getAge方法。

## Dispatch

分派是针对**方法**而言的，指的是方法确定的过程，**通常发生在方法调用的过程中**。分派根据方法选择的发生时机可以分为静态分派和动态分派，其中对于动态分派，根据宗量种数又可以分为单分派和多分派。

我更倾向于将分派理解为是**方法选择**的过程而非方法确定，“确定”这个词有“一劳永逸”的赶脚，让人进入一种误区：一次分派就能最终确定执行哪个方法。但是实际上从方法代码到JVM最终确定执行哪个方法的过程中，中间可能经过多次分派，比如某些重载的实例方法，在编译期进行一次方法选择（静态分派），在运行期可能还会进行一次方法选择（动态分派）。

### Static Dispatch

静态分派指的是在编译期间进行的方法选择，通常以方法名称，方法接收者和方法参数的静态类型来作为方法选择的依据。这些可以静态分派的方法一般都具有“签名唯一性”的特点（签名只考虑参数的静态类型而不管参数的实际类型），即不会出现相同签名的方法，因此可以在编译期就实现方法确定。Java中的非虚方法（主要包括静态方法，私有方法，final方法等，这些方法一般不可重写，故而不会有相同签名的情况出现）通常仅需要静态分派就可以实现方法的最终确定，更特别一点的例子是静态方法的隐藏，也是利用了静态分派，后面会专门讲解。虚方法的重载在编译时也用到了静态分派（尽管虚方法的调用在运行时还会涉及动态分派）。

#### 关于《深入理解Java虚拟机》中8.3.1解析部分的一些想法（Resolution vs Dispatch）

《深入理解Java虚拟机》书中在方法调用8.3.1对静态分派以及解析两个概念的解释有些混乱，参考了一些资料之后，这里提出一些更为清晰的分析。

首先区分Static Dispatch 与Resolution的区别(顺便附带Dynamic Dispatch)：

个人理解的是resolution是符号引用转化为直接引用的过程，发生在类加载期或者运行期，而dispatch是方法确定的过程，static dispatch发生在编译期。一个方法从最初的代码调用到最后的直接引用（或者说入口地址），实际上先要经过dispatch后要经过resolution。也就是说，对于非虚方法的调用过程，方法签名唯一，在编译期就可以确定，使用static dispatch就可以实现方法确定。static dispatch 就是产生符号引用的过程，并且该符号引用在类加载时期转化为该符号引用的直接引用(此过程为resolution)（非虚方法的解析通常在类加载时期完成）。而对于虚方法的调用过程，编译期产生的符号引用无法直接用于确定最终调用的方法（方法的确定无法在编译期完成，但是在编译期间也会进行静态分派，比如重载）,使用dynamic dispatch来实现最终的方法确定。dynamic dispatch则会在运行期根据方法接收者的实际类型，去实际类型的虚方法表上找与符号引用相同方法签名的方法，找到后如果该方法已被解析，则返回该方法的直接引用；否则，则此时执行resolution然后返回直接引用。

- 非虚方法 —> 静态分派 —> resolution发生在类加载时期
- 虚方法 —>静态分派—> 动态分派 —> resolution发生在类加载时期或者run-time（动态连接）

而《深入理解Java虚拟机》中有下面这段话：

> 调用目标在代码写好、编译器进行编译时就必须确定下来。这类方法的调用称为解析（Resolution）。

这里将”解析“换做“静态分派”似乎更加合适。而且书中在8.3.1的“解析”这一部分中的讲解似乎容易让人混淆解析和静态分派的概念。

### Dynamic Dispatch

动态分派是指方法的确定在run-time才能最终完成。使用动态分派来实现方法确定的方法一般在编译期间都是一些“不明确”的方法（比如一些重写方法，拥有相同的方法签名并且方法接收者的静态类型可能也相同），因此只能在运行时期根据方法接收者和方法参数的实际类型最终实现方法确定。Java中的虚方法（主要指实例方法） 通常需要在运行期采用动态分派来实现方法确定（利用invokevirtual指令获取方法接收者的实际类型，后文会有具体例子分析）。

#### Single Dispatch / Multiple Dispatch

单分派和多分派是根据分派时使用的原理来分类的，只根据一种宗量（宗量的概念请见文章开头）进行方法选择是单分派，根据多种宗量进行方法选择是多分派。

**单分派(Single [dynamic] Dispatch)**：只根据方法接收者的实际类型来实现方法的确定（Java采用此种分派方法）

**多分派(Multiple [dynamic] Dispatch)**：根据方法的接收者类型以及方法参数的实际类型来实现方法的确定

单分派多分派的概念区分一般只存在于动态分派当中。由于单分派多分派需要考虑实际类型，而对于静态分派只会根据静态类型来分派，因此没有所谓的静态单分派静态多分派的概念。（这种理解与《深入理解Java虚拟机》中的解释有所不同，个人比较倾向于单分派和多分派的分类只适用于动态分派）

### 如何理解Java的“静态多分派，动态单分派”

这种说法是不准确的。Java确实是动态单分派，但是对于静态分派而言其实没有所谓的单分派多分派的概念。但是我们可以这样来理解所谓的”静态多分派“概念： 由于java的静态分派需要同时考虑方法接收者和方法参数的静态类型，某种层度上而言是考虑了两种宗量，尽管没有涉及任何实际类型，依然可以从行为上勉强理解为”多分派“。

这里通过一个例子来理解Java中的分派。

```java
class Food{}
class Meat extends Food{}

class Person{
  public void buy(Food food){
    System.out.println("A person buy food");
  }
  public void buy(Meat meat){
    System.out.println("A person buy meat");
  }
}

class Man extends Person{
  public void buy(Food food){
    System.out.println("A man buy food");
  }
  public void buy(Meat meat){
    System.out.println("A man buy meat");
  }
}

public class Test{
  public static void main(String[] args){
    Person a = new Man();
    Food b = new Meat();
    a.buy(b);
  }
}
```

输出的结果为：

```java
A man buy food
```

这里涉及到了java里面的重载和重写。利用上文中提到的各种概念来对```a.buy(b)```方法调用过程进行分析：

首先在编译期间进行了静态分派，利用方法名，方法接收者和方法参数的静态类型进行方法选择，于是方法的符号引用确定为```Person.buy:(Ltest/Food;)V```，这里明确可以看到此时经过静态分派对重载方法进行选择后确定的方法为Person类的buy(Food food)方法。

但是对于虚方法的调用会在运行阶段利用动态分派再进行一次方法选择。如果此时采取动态单分派，则会根据方法接收者的实际类型再进行一次方法选择。由于对象a的实际类型是Man，因此最后确定调用的方法为Man类的buy(Food food)方法，输出结果将会是```A man buy food```。如果此时采取动态多分派，则会根据方法接收者以及方法参数的实际类型再进行一次方法选择。由于对象a的实际类型是Man，参数b的实际类型是Meat，因此最后确定调用的方法为Man类的buy(Meat meat)方法，输出结果将会是```A man buy meat```。

显然，我们看到最后程序输出结果为```A man buy food```，也证明了Java采用了动态单分派。

最后再从字节码的层面啰嗦一句，这里Java的动态分派是依靠invokevirtual指令的多态查找完成的。```a.buy(b)```方法调用对应的核心字节码为```invokevirtual #6  // Method test/Person.buy:(Ltest/Food;)V```，invokevirtual指令会首先找到操作数栈的第一个元素指向的对象（此例中为对象a）的实际类型（动态绑定方法接收者类型），并从实际类型中查找与指令参数中符号变量描述的方法签名（此例中为```buy:(Ltest/Food;)V```）相同的方法，并返回该方法的直接引用。

## Resolution vs Binding vs Dispatch

Resolution是指将符号引用转化为直接引用的过程，通常发生在类加载时期和运行期（运行期发生的resolution又被称为动态连接）。

这里从一般意义上(不限于Java)来对Binding和Dispatch来做一个区分：二者主要的区别在于作用的对象不同。

Binding是针对类型而言，指的是类型确定的过程，通常发生在对象属性的访问或方法调用时，也就是说Binding是属性的所有者以及方法的接收者的类型确定。

Dispatch是针对方法而言的，通常发生在方法调用时，指的是方法确定的过程。然而方法的确定也依赖于方法接收者类型的确定，这也是导致Binding和dispatch容易概念混淆的原因之一。举个例子来说，由于虚方法通过动态分派实现方法的最终选择，动态分派需要借助于方法接收者的**实际类型**，其实也就是意味着虚方法的接收者的类型确定是通过动态绑定实现的。这也是动态分派和动态绑定的关系所在：方法的确定通过动态分派实现，意味着方法接收者类型的确定通过动态绑定实现。前文已对Binding和Dispatch展开讨论，这里不再赘述。

网上有很多解释说”绑定指的是把一个方法的调用与方法所在的类(方法主体)关联起来“，个人觉得是不准确的，这种说法一定程度上将binding和dispatch的概念混淆在一起。这种说法本意是指”方法绑定”而非一般意义上的绑定（类型绑定）。但是目前看来，在Java中，大家还是比较倾向于将绑定和分派当做同义词来使用（方法绑定），都表示方法与方法接收者关联的过程。这些概念性的问题没必要细纠，弄明白原理就好。

## Overloading / Overriding / Hiding

下面通过Java中的重载，重写，隐藏（属性隐藏和方法隐藏）来综合理解上文中提到的多种概念。

### Overloading

非虚方法的重载是通过静态绑定以及静态多分派实现的。

虚方法的重载是通过动态绑定以及静态多分派和动态单分派实现的。

### Overriding

重写是实现多态的关键之一（多态三要素：继承，重写，父类引用指向子类对象），重写是通过 动态绑定以及动态单分派实现的。

由于重载和重写在上文中已经举过例子分析方法调用时的分派问题，这里不再赘述。

### Hiding

先明确覆盖和隐藏的区别：

**覆盖（重写）**：方法或属性的所有者实际类型和静态类型不相符时（静态类型为父类，实际类型为子类），最后实际被访问的是实际类型的方法或属性。

**隐藏**：方法或属性的所有者实际类型和静态类型不相符时（静态类型为父类，实际类型为子类），最后实际被访问的是静态类型的方法或属性。（静态方法，类属性或实例属性都只能被隐藏而无法覆盖）

造成二区别的原因在于是否会进行动态类型识别，这些都与属性所有者以及方法接收者的类型确定方式有关（Binding）。

#### Field Hiding

前文讨论Binding时介绍过：属性所有者的类型确定是通过静态绑定实现的，意味着属性所有者不会进行动态类型识别。前文举过例子，不再详述。

#### Method Hiding

实例方法可以被重写，而静态方法不能被重写（覆盖），只能被隐藏（Method Hiding）。

本质原因在于实例方法接收者的类型确定是通过动态绑定，实例方法的最终确定是通过动态分派，意味着实例方法的接收者类型由实际类型决定，最终访问的是实际类型的方法。

而静态方法接收者的类型确定是通过静态绑定，静态方法的最终确定是通过静态分派，意味着静态方法的接收者类型仅通过静态类型决定，不会在运行时识别接收者的实际类型，最终访问的也就是静态类型的方法。



由于本人对编译原理以及JVM的内部原理了解并不深入，如有纰漏，欢迎斧正~~

## References

[《深入理解Java虚拟机》第二版](https://book.douban.com/subject/6522893/)

http://softwareengineering.stackexchange.com/questions/200115/what-is-early-and-late-binding/200123#200123

[https://www.zhihu.com/question/28462483](https://www.zhihu.com/question/28462483)

