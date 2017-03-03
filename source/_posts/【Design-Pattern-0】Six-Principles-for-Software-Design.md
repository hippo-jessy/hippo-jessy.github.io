---
title: 【Design Pattern-0】Six Principles for Software Design
date: 2017-02-16 13:02:04
categories: [Design Pattern]
tags: [Design Pattern]
description:
---

设计模式重要性不言而喻，但是设计模式的学习只有结合具体项目实践才有意义。这里新开【Design Pattern】系列博文来总结设计模式相关的知识点，并尽量结合一些工程实践来帮助自己理解。

在具体介绍各个常见的设计模式之前，先花一点时间总结软件设计的六大原则：

单一职责原则(SRP)，开闭原则(OCP)，里氏替换原则(LSP)， 依赖倒置原则(DIP)，接口隔离原则(ISP)， 迪米特法则(LoD)

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



## 开闭原则（Open Close Principle, OCP）

<blockquote><font color="green" size="3px"><big>Software entities (classes, modules, functions, etc.) should be open for extension and closed for modification</big></font></blockquote> <br/>

开闭原则核心在于：软件应该对扩展开放，对修改关闭。通俗来说，就是指应该尽量通过扩展软件实体来解决需求变化，而非通过修改代码来实现。

开闭原则看似是一个比较“缥缈”的原则，它六个设计原则中最为宏观也最为模糊的一个。实际上我们可以将其它五条设计原则看做是我们在从无到有设计软件时应遵守的具体原则，而将OCP当做是软件设计完成后应对需求变化时应有的表现。如果该软件在原始设计时很好地遵守了其它五条设计原则，那么在应对需求变更时就很容易遵守OCP了。建议先看完下面其它原则之后再回到这一部分来看应该会有更好的理解。

鉴于目前能力有限，在这里先挖个坑，以后在实践中有更深领悟的时候，我再来谈谈对开闭原则的理解。

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

这是由于传统的某些结构化设计倾向于创建高层模块依赖于底层模块的结构。需要定义子模块的层次之后才能确定高层次的调用逻辑。这样一来，高层次依赖自层次，策略依赖实现细节。

而DIP原则的核心在于让高层次模块相对独立于子层次模块，通过高层次依赖抽象，低层次实现抽象，来实现高层次对低层次模块的调用。 抽象先制定契约（这种抽象通常表现为接口），高层模块通过契约来了解功能进而实现调用，子模块按照契约来具体实现抽象。所以经常将DIP总结为不管是高层模块还是底层模块都需要面向接口编程。这种依赖关系和前面描述的传统结构化设计的依赖关系是相反的，因此该原则被命名为依赖倒置原则。

这里先提一下什么叫“依赖”，本文开头也提到过类之间的几种关系（依赖，关联，聚合，组合，继承，实现），实际上这几种关系都可以表示上面一段话中的“依赖”这个抽象概念。高层模块对抽象的依赖更像是类之间的前四种关系（特别是第一种关系），通过局部变量，方法参数传递，静态方法调用，成员变量等实现。而底层模块对抽象的依赖则是通过类之间的后两种关系来实现的。

说了一堆抽象概念，不弄点实例，感觉就快飘上天了。如果要你设计一个简单软件实现让一个年轻驾驶员驾驶汽车的功能（用打印字符串来表示驾驶，以及车移动的速度）。

底层模块实现涉及到的主要对象（车，年轻驾驶员），然后通过调用底层模块的类和其暴露的方法来实现高层模块主要逻辑，从而实现驾驶（这种设计思考过程看似很自然，也完全满足当前的需求，但是明显违背了DIP）。上面这种思考过程对应下面这个设计：

```java
//底层模块
public class Car{
  private int speed = 100;
  public void move(){
    System.out.println("Car move at the speed of " + speed);
  }
}

//底层模块
public class YoungDriver{
  public void drive(Car car){
    System.out.println("A young driver start driving");
    car.move();
  }
}

//高层模块
public class HighLevelClient{
  public static void main(String[] args){
 	 Car car = new Car();
 	 YoungDriver driver = new YoungDriver();
 	 driver.drive(car);
  }
}  
```

上述代码类图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_2.png?%20v=20170302)

从类图可以清晰看到，高层模块HighLevelClient直接依赖于底层模块YoungDriver以及Car的具体实现，底层模块YoungDriver和Car之间也是直接相互依赖。这样的设计看起来很简洁，也完美解决了当前的需求。但是软件需求总是处于不断变动中，我们只需要稍微改动或者扩展下当前需求就可以轻易发现这种设计的僵硬性（rigidity）和脆弱性（fragility）。

比如现在不仅要求年轻驾驶员驾驶汽车，还要年轻驾驶员驾驶自行车，并且老年驾驶员也要驾驶自行车。很明显此时底层需要多加两个类Bike和OldDriver，并且需要对所有直接依赖底层细节的地方进行更改，比如HighLevelClient和YoungDriver类。修改后的代码如下：

```java
//【不变】底层模块
public class Car{
  private int speed = 100;
  public void move(){
    System.out.println("Car move at the speed of " + speed);
  }
}

//【扩展】底层模块
public class Bike{
  private int speed = 30;
  public void move(){
    System.out.println("Bike move at the speed of " + speed);
  }
}

//【修改】底层模块
public class YoungDriver{
  public void driveCar(Car car){
    System.out.println("A young driver start driving");
    car.move();
  }
  //【扩展】添加驾驶自行车的方法
  public void driveBike(Bike bike){
    System.out.println("A young driver start driving");
    bike.move();
  }
}

//【扩展】底层模块
public class OldDriver{
  public void driveCar(Car car){
    System.out.println("An old driver start driving");
    car.move();
  }
  public void driveBike(Bike bike){
    System.out.println("An old driver start driving");
    bike.move();
  }
}

//【修改】高层模块
public class HighLevelClient{
  public static void main(String[] args){
 	 Car car = new Car();
     Bike bike = new Bike();
 	 YoungDriver youngDriver = new YoungDriver();
     OldDirver oldDriver = new OldDriver();
 	 youngDriver.drive(car);
     youngDriver.drive(bike);
 	 oldDriver.drive(bike);
  }
}  
```

现在新的类图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_3.png?%20v=20170302)

不管你们能不能看懂这个类图，反正我是尽力了🐶。仅仅是为了满足一个这么简单的需求变化，竟然需要原始代码做这么多修改。这也就忍了，可是这样修改之后高层模块需要依赖几乎所有的底层细节不说，底层各个模块之间的细节依赖也相当严重。设想如果再加上第三次，第四次需求变化，呵呵，请自行脑补☞。

前面的开放关闭原则（OCP）也提到过，程序要对扩展开放，对修改关闭。从上面代码我们也看到了有一部分新的类需要加进去，这属于扩展，是应对需求变更的正常做法，但是对于YoungDriver和HighLevelClient的修改是我们需要想办法减少或避免的。其实导致现在看到的这些扩展性差，逻辑杂乱的根源在于我们一开始的设计思路是按照传统模块化设计思路来的，高层模块直接依赖于底层细节，违背了DIP，直接导致了需求变更时牵一发而动全身的后果。

我们依照DIP重新开始设计，再来感受一下DIP是如何做到灵活应对需求变更的。DIP的思路很简单，这种设计思路是通过客户需求抽象出接口，高层业务逻辑调用这些接口暴露的功能来实现用户需求，底层模块具体实现这些接口契约所规定的功能。这就好比是设计生产一辆车，首先我们需要根据车的需求定义出抽象层（汽车的四大基本组成）：发动机，底盘，车身，电气设备。然后高层开发人员研究如何利用这四大接口的功能组装成一辆符合需求的汽车，而底层开发人员主要关心如何具体实现发动机，底盘等底层部件。这种设计思路可以很好地应对需求变更，使软件具有更好的可扩展性。这一点也很容易理解，因为需求变更通常是在原来的需求上增加一些新功能，或者做一些微调。还是用汽车举例，需求的变更通常是针对于细节来的，比如我们之前的需求是实现一辆经济型SUV，现在需求变成了一辆豪华跑车。由于我们之前的高层设计和底层实现是围绕汽车的四大基础部件的抽象层来展开的，而SUV和跑车的基本结构也都是基于这四大部件来的，因此此时我们只需要在底层扩展出针对跑车特征的类，然后对高层模块稍做调整即可（遵守DIP的设计，间接也使软件在应对需求变更时更轻易地遵守OCP）。万变不离其宗大概讲的就是这个道理，所以我们的设计不应该围绕底层细节展开，而是应该围绕“宗”展开，才能以不变应万变（“宗”就是我们从需求中分析出来的抽象层）。

现在换成DIP来重新设计之前的例子：目前需求是设计一个简单软件实现让一个年轻驾驶员驾驶汽车的功能（用打印字符串来表示驾驶，以及车移动的速度），首先思考一下高层模块可能需要用到哪些抽象的功能：1.高层模块需要用到驾驶员的驾驶功能；2. 驾驶员需要用到交通工具。根据DIP，核心要义是面向接口编程，高层模块和底层模块都需要依赖抽象，这里先设计出接口，高层模块根据接口的功能契约来调用接口的方法，实现高层逻辑；底层根据接口的功能契约来实现细节（底层需要严格按照接口的契约来实现，这也是遵守里氏替换原则LSP的表现）。

```java
//先设计抽象模块
public interface Driver{
  public void drive(Vehicle vehicle);
}

public interface Vehicle{
  public void move();
}
```

当接口设计好之后，高层模块，以及用抽象隔开的底层模块之间就可以实现并行开发了(分别交给不同的人同时开发)。下面是具体的实现：

```java
//底层模块
public class YoungDriver implements Driver{
  public void drive(Vehicle vehicle){
    System.out.println("A young driver start driving");
    vehicle.move();
  }
}

//底层模块
public class Car implements Vehicle{
  private int speed = 100;
  public void move(){
    System.out.println("move at the speed of " + speed);
  }
}

//高层模块
public class HighLevelClient{
  public static void main(String[] args){
     Driver youngDriver = new YoungDriver();
 	 Vehicle car = new Car();
     //全部依赖抽象层定义的功能来实现高层逻辑
     youngDriver.drive(car);
  }  
}
```

上述代码的类图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_4.png?%20v=20170302)

至此，这种设计实现了基本需求。对比前面传统思维的设计，可以清楚的看到DIP的设计看上去要复杂一些，因为它在前面的设计上加了一层抽象。但是，一旦软件需求发生改变，这种面向接口的设计的优势就会立即体现出来。

同样的，需求此时变更为：不仅要求年轻驾驶员驾驶汽车，还要年轻驾驶员驾驶自行车，并且老年驾驶员也要驾驶汽车和自行车。我们只需扩展出Bike和OldDriver两个类，并少量修改高层代码即可应对需求变化。

```java
//【不变】底层模块
public class YoungDriver implements Driver{
  public void drive(Vehicle vehicle){
    System.out.println("A young driver start driving");
    vehicle.move();
  }
}

//【扩展】底层模块
public class OldDriver implements Driver{
  public void drive(Vehicle vehicle){
    System.out.println("An old driver start driving");
    vehicle.move();
  }
}

//【不变】底层模块
public class Car implements Vehicle{
  private int speed = 100;
  public void move(){
    System.out.println("move at the speed of " + speed);
  }
}

//【扩展】底层模块
public class Bike implements Vehicle{
  private int speed = 30;
  public void move(){
    System.out.println("move at the speed of " + speed);
  }
}

//【修改】高层模块
public class HighLevelClient{
  public static void main(String[] args){
     Driver youngDriver = new YoungDriver();
     Driver oldDriver = new OldDriver();
 	 Vehicle car = new Car();
     Vehicle bike = new Bike();
     //下面是高层事务逻辑的代码实现，全部依赖抽象层定义的功能来实现高层事务逻辑
     youngDriver.drive(car);
     youngDriver.drive(bike);
     oldDriver.drive(bike);
  }  
}
```

上述代码的类图如下：

![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】Six%20Principles%20of%20Software%20Design_5.png?%20v=20170302)

这一次没有修改底层代码，而是通过扩展底层代码和少量调整高层代码来应对需求变化。并且扩展后的程序依然逻辑结构分明，高层和底层都依赖接口（这也侧面证明了当初接口的设计是合理的）。

有些人可能会认为高层代码中也用到了Car，Bike，YoungDriver等底层具体类，这是不是说明实际上这一种设计也让高层模块依赖底层细节了？

这里我们需要留意变量类型的两个概念：引用类型（外观类型）和实际类型（不明白的可以参考[http://hippo-jessy/2017/02/13/【深入理解Java虚拟机-1】Resolution-vs-Binding-vs-Dispatch/](http://localhost:4000/2017/02/13/【深入理解Java虚拟机-1】Resolution-vs-Binding-vs-Dispatch/)的开头部分）。在高层模块中尽量在创建变量时，将变量的引用类型定义为接口类型，也就是说局部变量使用的是接口类型，在真正事务逻辑代码编写时调用的是抽象模块的方法（即接口暴露的方法和功能)。也就是说整体上而言高层模块依赖的是抽象层，这个设计符合DIP。

遵守了DIP的设计明显比之前的设计有更好地可扩展性，模块间的耦合性明显降低（模块间尽量通过接口来耦合）。遵守DIP的设计可以轻易地通过扩展底层模块的实现类来应对需求的变化，并尽量最小化代码的修改（OCP）。之前分析OCP时也提到了OCP是一个相对抽象和整体化的原则，但是从上面的例子我们也可以看到当设计遵守了DIP原则，某些程度上也能保证程序在应对需求变化时可以遵守OCP。后文的分析中，还可以进一步看到的，如果保证了其它五个设计原则，就可以更好地使程序在应对需求变化时遵守OCP。

## 接口隔离原则（Interface Segregation Principle, ISP）

<blockquote><font color="green" size="3px"><big>Client should not be forced to depend on methods that they do not use </big></font></blockquote> <br/>



## 迪米特法则（Law of Demeter, LoD）

<blockquote><font color="green" size="3px"><big>Only talk to your friends who share your concerns</big></font></blockquote> <br/>



最后用一段话总结这六大设计原则：

**SRP规定一个类的职责要单一；LSP表示子类重写要遵守父类（或父接口）方法的功能契约；DIP告诉我们要面向接口编程；ISP是说接口方法要尽量精简，内聚性强；LoD告诉我们不要和陌生人说话（类与类之间要尽量减少耦合）；OCP是说软件要对扩展开放，对修改关闭。尽量遵守前五种原则能使得软件设计更合理，让软件应对需求变更时更容易实现OCP。**

这篇文章只是设计模式总结的开始，很多知识的理解和运用并不是很透彻，待内功修炼以后，再回过来补充一些新的感悟吧，在此先立一个Flag🇨🇳

---

为了实现将复杂问题简单化，模式化，整出graceful code，了解常见的设计招式还是很有必要的。虽说金庸先生教导大家“无招胜有招”，但是对于我这种战五渣而言，从一招一式学起显然更为稳妥。

23种常见设计模式根据其特征和应用场合可以分为三大类，如下图所示（开启思维导图模式，持续修改更新）![](http://ojnnon64z.bkt.clouddn.com/【Design%20Pattern-0】%5BMind%20Map%5D%20Design%20Pattern.pdf?%20v=20170303)

具体每种设计模式的分析总结，会抽时间陆续更新在下面这个目录中：

[<font color="green" size="3px">http://hippo-jessy.com/categories/Design-Pattern/</font>](http://hippo-jessy.com/categories/Design-Pattern/)

---

## References

[1] 《设计模式之禅》

[2] Agile Software Development, Principle, Patterns, Practices

\[3] [http://blog.csdn.net/zhengzhb/article/details/7296944](http://blog.csdn.net/zhengzhb/article/details/7296944) 

\[4] [http://blog.csdn.net/zhengzhb/article/details/7190158](http://blog.csdn.net/zhengzhb/article/details/7190158)