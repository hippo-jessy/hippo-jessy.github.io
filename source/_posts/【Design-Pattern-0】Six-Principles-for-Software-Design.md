---
title: 【Design Pattern-0】Six Principles for Software Design
date: 2016-12-28 13:02:04
categories: [Design Pattern]
tags: [Design Pattern]
description:
---

设计模式重要性不言而喻，但是设计模式的学习只有结合具体项目实践才有意义。这里新开【Design Pattern】系列博文来总结设计模式相关的知识点，并尽量结合一些工程实践来帮助自己理解。

在具体介绍各个常见的设计模式之前，先花一点时间总结软件设计的六大原则：

单一职责原则(SRP)，里氏替换原则(LSP)， 依赖倒置原则(DIP)，接口隔离原则(ISP)， 迪米特法则(LoD)，开闭原则(OCP)

<!--more-->

## 类之间的关系

在介绍六大设计原则之前，先来回顾一下类之间常见的关系： **依赖(Dependence)，关联(Association)，聚合(Aggregation)， 组合(Composition) ， 继承(Generalization)，实现(Implementation)**

对于最后两种关系一般没有争议，继承和实现描述了类与类或类与接口之间的纵向关系，而前四种其实都是关联关系的一种，用以描述类与类之间或者类与接口之间的相互引用，是横向关系，耦合度（这里可以将耦合度简单理解为一个类发生变更时另一个类受影响的程度）的强弱依次递增：依赖 < 关联 <  聚合 < 组合。这四种关系的确定是比较容易出现争议的，特别是后三种。

下面主要分析下前四种关系的区别以及UML绘制：

### 依赖（dependence）

依赖关系是前四种关系中最容易辨别的关系，通常通过局部变量，方法形参，静态方法调用等方式实现类与类之间的关联。具体例子如下：

```java
public class Gun{
  public static void staticShoot(){
	System.out.println("static shooting");    
  }
  public void shoot(){
    System.out.println("shooting");
  }
}

public class Sniper{
  //通过局部变量实现依赖
  public void tryGun1(){
    Gun gun = new Gun();
    gun.shoot();
  }
  //通过方法形参实现依赖
  public void tryGun2(Gun gun){
    gun.shoot();
  }
  //通过静态方法调用实现依赖
  public void tryGun3(){
    Gun.staticShoot();
  }
}
```

依赖关系在UML中采用虚线+箭头表示，上例的UML图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_00.png)

### 关联（Association）

关联关系表示两个类处于平级关系的关联，比如你和你的同事，猫和狗，苹果和梨。产生关联关系又是仅仅是为了方便一个类使用另一个类的某些属性或方法。关联关系可以是单向的，也可以是双向的，通过成员变量来实现类与类之间的关联。

```java
public class Man{
  private Colleague colleague;
  public void getInfo(){
    colleague.getInfo();
  }
}
public class Colleague{
  public void getInfo(){
    System.out.println("look!!! lots of information");
  }
}
```

关联关系在UML中采用实线+箭头表示，上例的UML图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_01.png)

### 聚合（Aggregation）

聚合关系表示两个类处于从属或包含关系的关联，比如你和你的电脑，门和它的锁，汽车和车轮，公司与员工等。这是一种强耦合关系，但是涉及到的两个对象不一定有相同的生命周期。通过成员变量来实现类与类之间的关联。但是成员变量的赋值一般通过setter方法来单独实现(并非严格要求如此)。

```java
public class Man{
  private Computer computer;
  public void setComputer(Computer computer){
    this.computer = computer;
  }
  public void startComputer(){
    computer.start();
  }
}

public class Computer{
  public void start(){
    System.out.println("start the computer");
  }
}

```

聚合关系在UML中采用空心菱形+实线+箭头表示，上例的UML图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_02.png)

### 组合（Composition）

组合关系表示两个类处于包含关系的关系，这两个类相互依存，比如你和你的思想，书和它的内容等。这是一种更强的耦合关系，涉及到的两个类的对象有相同的生命周期。通过成员变量来实现类与类之间的关联。但是成员变量的赋值一般通过构造函数实现（体现出相同生命周期）。

```java
public class Man{
  private Mind mind;
  public Man(Mind mind){
    this.mind = mind;
  }
 public void think(){
   mind.think();
 }
}

public class Mind{
  public void think(){
    System.out.println("Mind is thinking");
  }
}
```

组合关系在UML中采用实心菱形+实线+箭头表示，上例的UML图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_03.png)

关联关系，聚合关系，组合关系，三者通常都是通过成员变量来实现类与类之间的关联。因此有时很难仅仅通过代码就轻易区分这三种关系，通常我们需要结合一些上下文语义和契约来区分这三种关系。可以借用下面这句话来帮助理解： 关联关系表示使用或借用（uses a）另一个类，聚合关系拥有（has a）另一个类，组合关系拥有并且不可或缺（contains a）另一个类。

**聚合关系和组合关系如何进行区分？**

聚合关系的两个类对应的对象生命周期不一定一致，并且两者并不是相互依存的关系。比如你和你的电脑，你没了电脑依然可以存在，你的电脑换一个主人同样也可以存在。这种关系更像是两个独立个体通过某种契约绑定在一起，形成一种上下级或者整体和部分的关系；这种契约一旦打破，两个个体依然可以独立存在。比如说公司和应聘者A签了工作协议，两个不相关的个人现在变成了整体和部分的关系，一旦A选择辞职，则契约被打破，但公司和A依然可以单独工作。

组合关系的两个类对应的对象有完全一致（表示部分的对象会随着表示整体的对象的消亡而消亡）。比如书烧了，它的内容也随之不见了，人不在了，人的思想也随之消亡了。这种关系是与生俱来的，一旦表示整体的对象消亡，则表示部分的对象也会消亡，不存在二者脱离关系独立存在的情况。

## 单一职责原则（Single Responsibility Principle, SRP）

<blockquote><font color="green" size="3px"><big>A class should have only one reason to change</big></font></blockquote> <br/>

该原则的核心是：只有一个理由可以导致类的更改。更通俗的说，就是让一个类最好只负责一个职责。如果让一个类承担两种或以上职责时，当需求改变时，很多原因都容易导致类的更改（比如第一个职责的需求发生改变，第二个职责的需求发生改变等等）。

这里使用《Agile Software Development: Principles, Patterns, and Practices》以及《设计模式之禅》中用到的经典例子来对单一职责模式进行举例讲解。

```java
public interface phone{
  public void dial(String phoneNumber);
  public void hangup();
  public void send(char c);
  public char recv();
}
```

上面这个接口的设计违背了单一职责原则，将负责连接管理的职责以及数据通信的职责混在了同一个接口中。将上述两个职责拆分，重新设计成以下结构：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design.png)

这样一来，虽然PhoneImplementation中依然包含了两种职责，但是在接口设计时严格实现了单一职责原则。并且在应用的其他部分可以直接调用职责对应的接口，无需考虑实现类的细节，从某种层度上来说，也实现了解耦。

这里为什么不直接将单个职责设计成单个类呢？这样不就能严格遵守单一职责原则了吗？

如果按照上面的说法设计，则会出现下面这样的结果：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_1.png?%20v=20170228)

这样虽然保证了SRP，却明显增加了整个设计结构的复杂度。PhoneImplementation需要依赖两个类才能完成业务（强耦合）。

单一职责原则看似容易理解，实则难以把握。有时过分追求单一职责原则可能增加程序设计的复杂度。通常情况会优先保证接口遵循单一职责原则，尽量让**类和方法**也遵循单一职责原则。



## 里氏替换原则（Liskov Substitution Principle, LSP）

<blockquote><font color="green" size="3px"><big>Subtypes must be substitutable for their base types</big></font></blockquote> <br/>

里氏替换原则的核心是：子类型**必须能替换**他们的父类型。刚看到这句定义时，我很自然地想到**多态**，多态的三大要素在于：继承，重写，父类引用指向子类对象。想到这里，理所当然的认为多态一定是满足LSP的：对于所有多态运用，子类由于继承了父类的所有方法属性，因此子类替换父类似乎是一件再正常不过的事情了。实际上这是对里氏替换原则的一种误解，“必须能替换”，指的不仅仅是代码上能替换（替换后编译不报错），更重要的是功能上能替换（替换后程序的运行逻辑和功能执行不会出现问题）。

更通俗地说，LSP是指子类可以继承并拓展父类的功能（拓展功能，比如子类定义新的方法实现新功能），更改这些功能的实现细节（比如重写某些方法），但是子类不可以改变这些原有的功能（比如重写方法时不管父类被重写方法的原始功能契约，重写时修改方法的功能）。

下面是**违背**LSP的一个经典例子：

```java
public class Base{
  public void printSelf(){
    System.out.println("I'm base");
  }
}

public class Derived extends Base{
  @Override
  public void printSelf(){
  }
}
//客户端代码
public class Client{
  public static void main(String[] args){
    Base a = new Derived();
    a.printSelf();
  }
}
```

这是一个派生类退化函数的例子。派生类出于某种原因认为不再需要printSelf方法了，于是将该方法重写成了一个空方法。但是这样一来，子类重写的方法就打破了父类方法的契约（父类方法的预定功能是打印自身实际类名）。尽管这样重写对于派生类自身而言很合理，但是客户端代码一般不会知道也不在意这些继承实现细节，很多时候还是会利用父类暴露的契约来调用方法：比如调用a.printSelf时，客户端默认遵循父类功能契约，默认这个方法用来打印自身实际类名的。然而客户端并不知道子类Derived已经悄悄打破了这个契约，因此客户端本意是想实现打印类名的功能，却发现实际运行结果并没有达到预期功能。这种异常现象就是由于设计类时违背LSP造成的。

可能这个例子还是有些抽象，下面再举个类似的更加具体化的例子（此例子来自《设计模式之禅》，进行了简化)

```java
public abstract class AbstractGun{
  //功能契约: 此方法打印一句话来表示射击
  public abstract void shoot();
}

public class HandGun extends AbstractGun{
  @Override
  public void shoot(){
    System.out.println("shooting with handgun !!!");
  }
} 

public class Rifle extends AbstractGun{
  @Override
  public void shoot(){
    System.out.println("shooting with rifle !!!");
  }
}

public class ToyGun extends AbstractGun{
  @Override
  //玩具枪没有必要再使用射击功能，直接重写为空方法
  public void shoot(){}
}

//客户端代码，默认shoot方法是用来打印一句话表示射击的
//客户端打算利用该契约下的shoot方法完成一些事情
public class Client{
  AbstractGun[] guns = new AbstractGun[3];
  guns[0] = new HandGun();
  guns[1] = new Rifle();
  guns[2] = new ToyGun();
  for(AbstractGun gun: guns){
    gun.shoot();
  }
}
```

结果发现有一把枪无法完成预期效果，这就是前面提到的派生类函数退化造成子类重写方法打破父类方法功能契约带来的结果。由于类的设计违背了LSP，造成了客户端运行异常（无法达到预期功能）。

按照网络上很多博客流行的说法，LSP在代码实现时通常包括下面的四层含义：

1. 子类可以实现父类的抽象方法，但是不能覆盖父类的非抽象方法
2. 子类可以增加自己特有的方法
3. 子类**重载**父类的方法时，必须保证子类方法的前置条件（即方法的形参）要比父类方法的输入参数更宽松
4. 子类实现父类的抽象方法时，必须保证子类方法的后置条件（即方法的返回值）要比父类更严格

对于2和4没什么好说的，第4点直接就是方法重写的必要条件。我并不是很认同第1点，子类可以覆盖父类的非抽象方法，前提是重写时保证满足该方法在父类中定下的契约，即重写时不更改父类中该方法实现的功能和用途即可。

对于第3点其实也不难理解，如果子类的重载方法的参数范围小于父类的方法（比如重载方法的参数类型是父类的方法参数类型的子类），很容易造成原本客户端代码想要调用父类方法时调成子类重载方法（由于重载方法匹配优先级，优先匹配参数范围最小的方法，如果找不到精准匹配的方法，则将参数自动向上转型再寻找）。

讨论了这些之后，我们再回到开始时提到的多态和LSP之间的关系，从下面这几个方面分析，就能很容易理解它们的关系了：

1. 多态的实现是通过实现父类的抽象方法时：时满足父类方法契约，实现父类方法预定的功能，则为合理的设计，符合LSP。
2. 多态的实现是通过重写父类的非抽象方法时：重写时满足父类方法契约，实现父类方法预定的功能，则为合理的设计，符合LSP。
3. 多态的实现是通过重写父类的非抽象方法时：如果必须通过重写时打破父类方法契约，违背父类方法预定功能这种途径来实现某种新的功能需求，则此时建议重新思考设计，采用依赖，关联，聚合，组合等关系代替继承和多态来实现这种功能需求(比如前面的ToyGun的例子最好更改为采用依赖或关联关系来实现ToyGun而非直接继承AbstractGun和重写shoot()方法)。

实际上对于LSP只需要记住一点就好：重写时尽量保证子类方法遵循父类方法契约（预定功能）。

## 依赖倒置原则（Dependence Inversion Principle, DIP）

<blockquote><font color="green" size="3px"><big>1.  High-level modules should not depend on low-level modules. Both should depend on abstractions <br/>2.  Abstractions should not depend on details. Details should depend on abstractions. </big></font></blockquote> <br/>

依赖倒置原则的核心说白了就是面向接口编程。但是为啥要整出“依赖倒置”这么高大上的名字？

## 接口隔离原则（Interface Segregation Principle, ISP）

<blockquote><font color="green" size="3px"><big>Client should not be forced to depend on methods that they do not use </big></font></blockquote> <br/>



## 迪米特法则（Law of Demeter, LoD）

<blockquote><font color="green" size="3px"><big>Only talk to your friends who share your concerns</big></font></blockquote> <br/>





## 开闭原则（Open Close Principle, OCP）

<blockquote><font color="green" size="3px"><big>Software entities (classes, modules, functions, etc.) should be open for extension and closed for modification</big></font></blockquote> <br/>

开闭原则核心在于：软件应该对扩展开放，对修改关闭。通俗来说，就是指应该尽量通过扩展软件实体来解决需求变化，而非通过修改代码来实现。

开闭原则看似是一个比较“缥缈”的原则，它六个设计原则中最为基础也最为模糊的一个。鉴于目前能力有限，在这里先挖个坑，以后在实践中有更深领悟的时候，我再来谈谈对开闭原则的理解。

最后用一段话总结这六大设计原则：









这篇文章只是设计模式总结的开始，很多知识的理解和运用并不是很透彻，待内功修炼以后，再回过来补充一些新的感悟吧，在此先立一个Flag🇨🇳

---

为了实现将复杂问题简单化，模式化，整出graceful code，了解常见的设计招式还是很有必要的。虽说金庸先生教导大家“无招胜有招”，但是对于我这种战五渣而言，从一招一式学起显然更为稳妥。

23种常见设计模式根据其特征和应用场合可以分为三大类，如下图所示（开启思维导图模式）：





具体每种设计模式的分析总结，会抽时间陆续更新在下面这个目录中：

[http://hippo-jessy.com/categories/Design-Pattern/](http://hippo-jessy.com/categories/Design-Pattern/)

---

## References

[1] 《设计模式之禅》

[2] Agile Software Development, Principle, Patterns, Practices

\[3] [http://blog.csdn.net/zhengzhb/article/details/7296944](http://blog.csdn.net/zhengzhb/article/details/7296944) 

\[4] [http://blog.csdn.net/zhengzhb/article/details/7190158](http://blog.csdn.net/zhengzhb/article/details/7190158)