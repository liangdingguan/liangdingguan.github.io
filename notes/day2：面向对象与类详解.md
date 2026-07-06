---
title: content2
date: 2026-07-06
tags: [C++, 课程笔记]
summary: 面向对象相关
slug: c-cpp-basic-syntax-content2
---

# 进阶学习其二：面向对象与类详解

> author:梁鼎冠

## 一、面向对象编程（OOP）思想简介

- **程序 = 数据 + 算法** → 传统过程式编程以函数为核心。
- **OOP**：将数据和对数据的操作封装在一起，形成“对象”，通过对象之间的交互解决问题。
- **三大特性**：封装、继承、多态。

---

## 二、类（Class）与对象（Object）

- **类**：用户自定义的数据类型，是对象的“蓝图”或“模板”。它描述了该类对象具有的数据成员（属性）和成员函数（方法）。
- **对象**：根据类创建的具体实例，占用实际内存。

### 示例1：定义一个简单的`Student`类并创建对象

```cpp
#include <iostream>
#include <string>
using namespace std;

// 类的定义
class Student {
public:   // 公共访问权限
    // 数据成员
    string name;
    int age;
    float score;

    // 成员函数
    void display() {
        cout << "Name: " << name << ", Age: " << age << ", Score: " << score << endl;
    }
};

int main() {
    // 创建对象
    Student stu1;
    stu1.name = "张三";
    stu1.age = 20;
    stu1.score = 89.5;
    stu1.display();

    Student stu2 = {"李四", 21, 93.0}; // C++11 聚合初始化
    stu2.display();

    return 0;
}
```

---

## 三、访问修饰符（Access Modifiers）

| 修饰符      | 类内部 | 派生类 | 类外部（对象） |
| ----------- | ------ | ------ | -------------- |
| `public`    | ✔️      | ✔️      | ✔️              |
| `protected` | ✔️      | ✔️      | ❌              |
| `private`   | ✔️      | ❌      | ❌              |

- **封装原则**：将数据成员设为 `private`，通过 `public` 成员函数间接访问，以保护数据完整性。

### 示例2：使用`private`与`public`实现封装

```cpp
#include <iostream>
#include <string>
using namespace std;

class BankAccount {
private:
    string owner;
    double balance;   // 私有，外部不能直接访问

public:
    // 存款
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            cout << "存款成功，当前余额: " << balance << endl;
        } else {
            cout << "存款金额无效" << endl;
        }
    }

    // 取款
    void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            cout << "取款成功，当前余额: " << balance << endl;
        } else {
            cout << "余额不足或金额无效" << endl;
        }
    }

    // 查询余额（只读）
    double getBalance() const {
        return balance;
    }

    // 设置账户持有人
    void setOwner(const string& name) {
        owner = name;
    }

    string getOwner() const {
        return owner;
    }
};

int main() {
    BankAccount myAccount;
    myAccount.setOwner("王小明");
    // myAccount.balance = 10000;  // 错误：private成员不可访问
    myAccount.deposit(1000);
    myAccount.withdraw(300);
    cout << "账户持有者: " << myAccount.getOwner() << endl;
    cout << "最终余额: " << myAccount.getBalance() << endl;
    return 0;
}
```

---

## 四、构造函数（Constructor）

- 构造函数在对象创建时自动调用，用于初始化对象。
- 函数名与类名相同，**无返回值**，可以有参数（支持重载）。
- 如果不写任何构造函数，编译器自动生成一个默认构造函数（不初始化成员）。

### 示例3：编写多种构造函数

```cpp
#include <iostream>
#include <string>
using namespace std;

class Book {
private:
    string title;
    string author;
    double price;

public:
    // 无参构造函数（默认构造函数）
    Book() {
        title = "未命名";
        author = "未知";
        price = 0.0;
        cout << "默认构造函数被调用" << endl;
    }

    // 带参数构造函数
    Book(const string& t, const string& a, double p) {
        title = t;
        author = a;
        price = p;
        cout << "带参数构造函数被调用" << endl;
    }

    // 显示信息
    void display() const {
        cout << "《" << title << "》 作者: " << author << " 价格: " << price << "元" << endl;
    }
};

int main() {
    Book book1;                     // 调用无参构造函数
    Book book2("C++ Primer", "Stanley B. Lippman", 128.0); // 调用有参构造函数

    book1.display();
    book2.display();

    return 0;
}
```

---

## 五、*初始化列表（Initializer List）

- 在构造函数体执行之前对成员进行初始化。
- 对于 `const` 成员或引用成员，必须使用初始化列表。
- 效率高于在函数体内赋值。

### 示例4：使用初始化列表

```cpp
#include <iostream>
using namespace std;

class Point {
private:
    const int id;      // const成员必须初始化
    int x, y;

public:
    // 初始化列表 : 成员(值), ...
    Point(int _id, int _x, int _y) : id(_id), x(_x), y(_y) {
        // 这里可以写其他初始化代码
        cout << "Point对象 " << id << " 创建: (" << x << ", " << y << ")" << endl;
    }

    void print() const {
        cout << "Point(" << x << ", " << y << ")" << endl;
    }
};

int main() {
    Point p(101, 3, 5);
    p.print();
    return 0;
}
```

---

## 六、析构函数（Destructor）

- 对象生命周期结束时（如离开作用域、`delete`）自动调用。
- 函数名为 `~类名`，无参数，无返回值，不可重载。
- 用于释放动态分配的资源（如 `new` 的内存、文件句柄等）。

### 示例5：析构函数演示

```cpp
#include <iostream>
#include <cstring>
using namespace std;

class String {
private:
    char* data;

public:
    // 构造函数：分配内存并复制字符串
    String(const char* str = "") {
        data = new char[strlen(str) + 1];
        strcpy(data, str);
        cout << "构造: " << data << endl;
    }

    // 析构函数：释放内存
    ~String() {
        cout << "析构: " << data << endl;
        delete[] data;
    }

    void print() const {
        cout << data << endl;
    }
};

int main() {
    String s1("Hello");
    String s2("World");
    s1.print();
    s2.print();
    // 当main结束时，s1和s2自动调用析构函数
    return 0;
}
```

---

## 七、`this` 指针

- 每个非静态成员函数内部都有一个隐含的 `this` 指针，指向当前对象本身。
- 常用于：
  1. 区分同名参数和成员变量。
  2. 返回对象自身的引用（实现链式调用）。

### 示例6：使用`this`指针

```cpp
#include <iostream>
using namespace std;

class Counter {
private:
    int value;

public:
    Counter(int value = 0) {
        this->value = value;   // this->value 指成员变量
    }

    Counter& increment() {    // 返回当前对象的引用
        this->value++;
        return *this;
    }

    void print() const {
        cout << "value = " << this->value << endl;
    }
};

int main() {
    Counter c(5);
    c.increment().increment().increment(); // 链式调用
    c.print();  // 输出 value = 8
    return 0;
}
```

---

## 八、类的分离式开发（头文件与源文件分离）

- 通常将类声明放在 `.h` 头文件中，成员函数实现放在 `.cpp` 文件中。
- 好处：接口与实现分离，便于团队开发与编译。

### 示例7：分离式文件结构

**`Rectangle.h`**
```cpp
#ifndef RECTANGLE_H
#define RECTANGLE_H

class Rectangle {
private:
    double width, height;

public:
    Rectangle(double w = 1.0, double h = 1.0);
    double area() const;
    void scale(double factor);
};

#endif
```

**`Rectangle.cpp`**
```cpp
#include "Rectangle.h"

Rectangle::Rectangle(double w, double h) : width(w), height(h) {}

double Rectangle::area() const {
    return width * height;
}

void Rectangle::scale(double factor) {
    width *= factor;
    height *= factor;
}
```

**`main.cpp`**
```cpp
#include <iostream>
#include "Rectangle.h"
using namespace std;

int main() {
    Rectangle rect(3, 4);
    cout << "Area: " << rect.area() << endl;
    rect.scale(2);
    cout << "After scaling, area: " << rect.area() << endl;
    return 0;
}
```

编译命令（g++）：
```bash
g++ -c Rectangle.cpp -o Rectangle.o
g++ -c main.cpp -o main.o
g++ Rectangle.o main.o -o program
```

---

## 九、静态成员（static）

- **静态数据成员**：属于整个类，所有对象共享一份，必须在类外单独定义和初始化。
- **静态成员函数**：不依赖于具体对象，只能访问静态成员。

### 示例8：静态成员的使用

```cpp
#include <iostream>
using namespace std;

class Student {
private:
    string name;
    static int totalCount;   // 声明静态成员

public:
    Student(const string& n) : name(n) {
        totalCount++;
        cout << "学生 " << name << " 入学，当前总人数: " << totalCount << endl;
    }

    ~Student() {
        totalCount--;
        cout << "学生 " << name << " 离校，当前总人数: " << totalCount << endl;
    }

    static int getTotalCount() {   // 静态成员函数
        return totalCount;
    }
};

// 定义并初始化静态成员
int Student::totalCount = 0;

int main() {
    cout << "初始学生人数: " << Student::getTotalCount() << endl;
    Student s1("张三");
    Student s2("李四");
    {
        Student s3("王五");
        cout << "当前人数: " << Student::getTotalCount() << endl;
    }
    cout << "最终人数: " << Student::getTotalCount() << endl;
    return 0;
}
```

---

## 十、常量成员函数（const）

- 在函数参数列表后加 `const`，表示该函数不会修改任何数据成员。
- `const` 对象只能调用 `const` 成员函数。

### 示例9：const成员函数

```cpp
#include <iostream>
using namespace std;

class Data {
private:
    int value;
public:
    Data(int v) : value(v) {}

    // 非常量成员函数，可以修改成员
    void setValue(int v) {
        value = v;
    }

    // 常量成员函数，只读
    int getValue() const {
        // value = 10;  // 错误：const函数中不能修改成员
        return value;
    }
};

void printData(const Data& d) {
    // d.setValue(100);   // 错误：d是const引用，不能调用非常量成员
    cout << d.getValue() << endl;  // 可以调用const成员
}

int main() {
    Data d(42);
    printData(d);
    return 0;
}
```

---

## 十一、综合练习：设计一个简单的`Clock`类

要求：
- 私有成员：`hour`, `minute`, `second`
- 公有成员函数：
  - 构造函数（带默认参数）
  - `setTime` 设置时间
  - `tick` 增加一秒（处理进位）
  - `display` 显示时间
- 使用封装和合理性检查（小时0-23，分钟0-59，秒0-59）

### 示例10：`Clock` 类实现

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

class Clock {
private:
    int hour, minute, second;

    // 辅助函数：调整时间合法性
    void normalize() {
        if (second >= 60) {
            minute += second / 60;
            second %= 60;
        }
        if (minute >= 60) {
            hour += minute / 60;
            minute %= 60;
        }
        if (hour >= 24) {
            hour %= 24;
        }
        // 负数处理略，实际可以进一步扩展
    }

public:
    Clock(int h = 0, int m = 0, int s = 0) {
        setTime(h, m, s);
    }

    void setTime(int h, int m, int s) {
        hour = h;
        minute = m;
        second = s;
        normalize();
    }

    void tick() {
        second++;
        normalize();
    }

    void display() const {
        cout << setfill('0');
        cout << setw(2) << hour << ":"
             << setw(2) << minute << ":"
             << setw(2) << second << endl;
    }
};

int main() {
    Clock c(23, 59, 55);
    for (int i = 0; i < 10; i++) {
        c.display();
        c.tick();
    }
    return 0;
}
```

---

## 十二、常见错误与注意事项

1. **忘记在类定义末尾加分号`;`** → 编译错误。
2. **访问私有成员** → 必须在类内定义 `public` 函数接口。
3. **使用未初始化的对象** → 最好提供构造函数。
4. **动态内存忘记释放** → 在析构函数中 `delete`。
5. **浅拷贝问题** → 当类成员包含指针时，需要自定义拷贝构造函数和赋值运算符（后续进阶内容）。

---

## 十三、课后作业

1. 定义一个 `Circle` 类，包含半径（`private`），成员函数：设置半径、计算面积、计算周长。
2. 定义一个 `Student` 类，包含姓名、学号、三门课成绩，成员函数：计算平均分、输出信息。使用构造函初始化，并编写一个简单的主程序测试。
3. 改进 `Clock` 类，增加一个 `setAlarm` 功能（思考如何设计）。

