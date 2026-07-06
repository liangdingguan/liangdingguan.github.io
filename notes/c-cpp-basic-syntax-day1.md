---
title: C/C++补充1：C与C++基本语法对比与补充
date: 2026-07-06
tags: [C++, 课程笔记]
summary: 从 C/C++ 基础关系、语法差异、函数与运算符重载，到 C++11/14/17 常用现代特性的一篇课程笔记。
slug: c-cpp-basic-syntax-day1
---

# 进阶学习其一：C与C++基本语法对比与补充

> author：梁鼎冠

---

## 一、C 与 C++ 的基本关系
- C++ 是 C 的超集（绝大多数 C 代码可在 C++ 编译），但两者在思想上有本质区别。
- C 是**面向过程**，C++ 支持**面向对象 + 泛型 + 函数式**。
- 基本语法：
  - 三大基础结构：顺序结构、分支结构、循环结构
    - 顺序结构：基本的输入输出、运算符应用、基本类型书写、类型转换问题
    - 分支结构：if ->else if->else 、switch-case
    - 循环结构：while、for、break、continue、return

  - 函数、结构体、指针
    - 指针、引用、函数定义与调用、结构体

  - 面向对象基础
    - 封装
    - 继承
    - 多态


---

## 二、基础语法对比（C vs C++）

### 2.1 头文件与命名空间
**C 风格**

```c
#include <stdio.h>
#include <stdlib.h>
```
**C++ 风格**

```cpp
#include <cstdio>   // C 库的 C++ 包装，声明在 std 命名空间
#include <cstdlib>
#include <iostream> // C++ 流库
using namespace std; // 推荐仅在 cpp 文件中使用
```
- **区别**：C++ 引入命名空间 `namespace`，避免名字冲突；C 无命名空间概念。

### 2.2 基本数据类型
| 数据类型 | C                                       | C++                                              |
| -------- | --------------------------------------- | ------------------------------------------------ |
| 布尔型   | `_Bool` (C99)，需 `stdbool.h` 得 `bool` | 内置 `bool`，字面值 `true/false`                 |
| 字符型   | `char`                                  | `char`                                           |
| 整型     | `int, short, long, long long`           | 同左，增加 `wchar_t, char16_t, char32_t` (C++11) |
| 浮点型   | `float, double, long double`            | 同左                                             |
| 空类型   | `void`                                  | `void`                                           |
| 空指针   | `NULL` (通常为 `((void*)0)`)            | `nullptr` (C++11，类型安全)                      |

**示例**
```cpp
bool flag = true;            // C++ 内置
int* p = nullptr;            // C++11，替代 NULL
```

### 2.3 变量定义位置
- **C89**：变量必须在块开头定义。
- **C99 / C++**：允许在任意位置定义变量（如 `for(int i=0;;)`）。
```cpp
for (int i = 0; i < 5; ++i) { /*...*/ } // C++ 与 C99 均允许
```

### 2.4 常量与 const
- C 中 `const` 为只读变量，不可用于数组大小（除非 C99 VLA）。
- C++ 中 `const` 为编译期常量，可用于数组大小。
```cpp
const int MAX = 100;
int arr[MAX]; // C++ 合法，C 中传统非法（C99 可变长数组另算）
```

### 2.5 强制类型转换
- **C 风格**：`(type)value`。

```
double a=3.14;
std::cout<<(int)a;
```

- **C++ 风格**：`static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`（更安全、可读）。

```cpp
double d = 3.14;
int i = static_cast<int>(d); // C++ 推荐
```

### 2.6 函数
#### 函数默认参数（C++ 有，C 无）
```cpp
void func(int a, int b = 10) { /*...*/ } //这个也叫做缺省参数
```

#### 函数重载（C++ 有，C 无）
```cpp
void print(int x);
void print(double x);//若调用时函数重名了，会根据参数类型来选择不一样的函数来调用
```

### 2.7 动态内存管理
- **C**：`malloc / free`，需手动计算大小，返回 `void*`。
- **C++**：`new / delete`，自动计算大小，调用构造函数/析构函数。
```cpp
// C
int* p = (int*)malloc(sizeof(int)*10);
free(p);

// C++
int* p2 = new int[10];
delete[] p2;
```

### 2.8 结构体与枚举与pair<>
**结构体**

```cpp
// C 结构体
typedef struct PointC{ int x,int y} PointC;  PointC p1={123,456}；
struct PointC2{int x,int y};  struct PointC2 a;//声明时必须带上struct关键字
typedef struct { int x,int y} PointC3;  PointC3 p3={123,456}；//匿名结构体写法
// C++ 结构体 (直接使用类型名，且可包含成员函数)
struct PointCPP { int x; void show() { /*...*/ } };
PointCPP p; // 无需 typedef
```
**枚举**

```cpp
// C 枚举 (值暴露在外)
enum Color { RED, GREEN };
// C++11 强类型枚举
enum class Color { RED, GREEN };
Color c = Color::RED; // 必须带作用域
```

**pair<>**

```cpp
//多数时候可以平替两种类型聚合的结构体
pair<int,int>p;
p.first=123;
p.second=456;
//需要与map<>稍作区分，map是键值对，通过键可以以O(logn)的复杂度查寻值。pair只是单纯把两个值以一对的形式存储

```
### 2.9函数重载与运算符重载

**函数重载**

```cpp
#include <iostream>
using namespace std;

// 打印整数
void print(int x) {
    cout << "int: " << x << endl;
}

// 打印浮点数
void print(double x) {
    cout << "double: " << x << endl;
}

// 打印字符串
void print(const char* s) {
    cout << "string: " << s << endl;
}

// 打印两个整数
void print(int a, int b) {
    cout << "two ints: " << a << ", " << b << endl;
}

int main() {
    print(10);          // 调用 print(int)
    print(3.14);        // 调用 print(double)
    print("hello");     // 调用 print(const char*)
    print(1, 2);        // 调用 print(int, int)
    return 0;
}
/*
顶层 const（指针本身是常量）不参与重载：void f(int) 与 void f(const int) 相同。

底层 const（指向常量的指针/引用）可以参与重载：void f(int&) 与 void f(const int&) 不同。

*/
```

**运算符重载**

- 大部分运算都可以重载。**不能重载**的有：`.`, `.*`, `::`, `?:`, `sizeof`, `alignof`, `typeid`, `noexcept`。`->*` 是可以重载的，但很少用。
- 两种实现方式
  - 成员函数
    - 左操作数为 `*this`，参数列表少一个（右操作数）。
    - 例如：`operator+(const T& right)` 对应 `a + b` → `a.operator+(b)`。
  - 非成员函数(通常是友元函数)
    - 需要两个参数（二元运算符），左右操作数对称。
    - 适用于左操作数不是自定义类型的情况（如 `cout << obj`）。

```cpp
//1.成员函数重载< 实现结构体比大小
struct Students{
    int age;
    int height;
    // 成员函数版本（只需一个参数，右操作数）
    bool operator < (const Students& y)const{
        //这里可以写成 if(this->age!+y.age)return this->age<y.age
        if(age!=y.age)return age<y.age; 
        else return height>y.height;
    }
}
//2.友元函数
struct Students{
    private:
        int age;
        int height;
   public:
    	friend bool operator < (const Students & y)const{
            .......
        }
}
//3.非成员函数(在结构体或类之外的地方写)，类似于写sort排序中的cmp函数

bool operator < (const Students& x,const Students& y){
    if(x.age!=y.age)return x.age<y.age;
    else return x.height<y.height;
}
```

```cpp
//重载<<,使得输出时候可以直接输出整个结构体
ostream& operator<<(ostream& os, const Point& p) {
    os << "(" << p.x << ", " << p.y << ")";
    return os;
}
```

### 2.9 输入输出

- **C**：`printf / scanf`，格式字符串控制。
- **C++**：`cin / cout`，类型安全，可重载。
```cpp
int age;
cout << "Enter age: ";
cin >> age;
cout << "Age: " << age << endl;
```

### 2.10 字符串
- **C**：`char str[]` 或 `char*`，以 `\0` 结尾，操作靠 `<string.h>`。
- **C++**：`std::string` 类，功能丰富且安全。
```cpp
string s = "Hello";
s += " World";
cout << s.length();
```

---



## 三、现代 C++ 语法大全（C++11/14/17）

以下特性在编译时若无特别说明，均可使用 `-std=c++11` 或 `-std=c++14`。需要 C++17 的会标注。

### 3.1 类型推导（C++11）
#### auto
```cpp
auto x = 42;           // int
auto y = 3.14;         // double
auto z = "hello";      // const char*
vector<int> v;
for (auto it = v.begin(); it != v.end(); ++it) { /*...*/ }
```
#### decltype
```cpp
int a = 5;
decltype(a) b = 10;   // b 为 int
```
#### 返回类型后置（C++11）
```cpp
auto add(int x, int y) -> int { return x + y; }
//最好的写法是
auto add(int x, int y) -> decltype(x+b){return x + y ;}
```

### 3.2 范围 for 循环（C++11）
```cpp
vector<int> arr = {1,2,3,4};
for (int val : arr)        // 值拷贝
    cout << val;
for (int& val : arr)       // 引用修改
    val *= 2;
```

### 3.3 nullptr（C++11）
```cpp
void func(int*);
void func(int);
func(nullptr); // 调用 int* 版本，避免二义性
```

### 3.4 统一的初始化列表（C++11）
```cpp
int a{5};
vector<int> v{1,2,3,4};
map<string, int> m{{"a",1}, {"b",2}};

struct Point { int x, y; };
Point p{3, 4};
```

### 3.5 左右值引用与移动语义（C++11）

- **左值**与右值这两个概念是从 C 中传承而来的，左值指既能够出现在等号左边，也能出现在等号右边的变量；**右值**则是只能出现在等号右边的变量。

```cpp
int a; // a 为左值
a = 3; // 3 为右值
```

- **左值**是可寻址的变量，有持久性；**右值**一般是不可寻址的常量，或在表达式求值过程中创建的无名临时对象，短暂性的。
- 左值引用：引用一个对象；
- 右值引用：就是必须绑定到右值的引用，C++11中右值引用可以实现**移动语义**，通过 && 获得右值引用。

```cpp
int x = 6; // x是左值，6是右值
int &y = x; // 左值引用，y引用x

int &z1 = x * 6; // 错误，x*6是一个右值
const int &z2 =  x * 6; // 正确，可以将一个const引用绑定到一个右值

int &&z3 = x * 6; // 正确，右值引用
int &&z4 = x; // 错误，x是一个左值
```



```cpp
string s1 = "Hello";
string s2 = std::move(s1); // s1 变为空，避免深拷贝
vector<int> createVector() {
    vector<int> res{1,2,3};
    return res; // 编译器自动移动 (NRVO)
}
```
- **右值引用** `&&` 绑定临时对象。
- **`std::move`** 将左值强制转为右值。

### 3.6 智能指针（C++11/14）
```cpp
#include <memory>
// unique_ptr (独占所有权)
auto u = unique_ptr<int>(new int(10));  // C++11
auto u2 = make_unique<int>(20);        // C++14

// shared_ptr (共享所有权)
auto sp = make_shared<int>(30);        // C++11
// weak_ptr (解决循环引用)
weak_ptr<int> wp = sp;
```

### 3.7 Lambda 表达式（C++11）
```cpp
// 完整形式
auto func = [/*捕获*/](int a, int b) -> int { return a + b; };
// 常用捕获
int x = 10;
auto add_x = [x](int y) { return x + y; };     // 值捕获
auto add_ref = [&x](int y) { x += y; };        // 引用捕获
auto printAll = [=]() { cout << x; };          // 隐式值捕获
auto modifyAll = [&]() { x = 5; };             // 隐式引用捕获
```
- **泛型 Lambda（C++14）**
```cpp
auto identity = [](auto val) { return val; };
cout << identity(5) << identity(3.14);
```

### 3.8 constexpr 常量表达式（增强）
```cpp
constexpr int square(int x) { return x * x; }   // C++11
constexpr int val = square(5);                  // 编译期计算
```
- C++14 放宽了 constexpr 函数约束，可包含局部变量、循环等。

### 3.9 委托构造函数（C++11）
```cpp
class MyClass {
public:
    MyClass() : MyClass(0, 0) {}          // 委托
    MyClass(int a, int b) : x(a), y(b) {}
private:
    int x, y;
};
```

### 3.10 继承构造函数（C++11）
```cpp
class Base {
public:
    Base(int x) {}
};
class Derived : public Base {
    using Base::Base;  // 继承基类所有构造函数
};
```

### 3.11 默认/删除函数（C++11）
```cpp
class NonCopyable {
public:
    NonCopyable() = default;            // 使用编译器默认生成
    NonCopyable(const NonCopyable&) = delete;       // 禁止拷贝构造
    NonCopyable& operator=(const NonCopyable&) = delete;
};
```

### 3.12 override 和 final（C++11）
```cpp
class Base {
    virtual void f() const;
};
class Derived : public Base {
    void f() const override;   // 确保重写正确
    // void f(int) override;   // 编译错误，签名不匹配
};
class FinalClass final {};      // 禁止被继承
void func() final;              // 禁止虚函数被进一步重写
```

### 3.13 强类型枚举（C++11）
```cpp
enum class Color { Red, Green, Blue };
Color c = Color::Red;
// int i = Color::Red;  // 错误，无法隐式转换
int i = static_cast<int>(Color::Red); // 需显式转换
```

### 3.14 静态断言（C++11）
```cpp
static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");
```

### 3.15 类型别名（C++11）
```cpp
using uint = unsigned int;                // 等同于 typedef
template<typename T>
using Vec = std::vector<T>;               // 模板别名，typedef 无法做到
Vec<int> vi;
```

### 3.16 可变参数模板（C++11）
```cpp
template<typename... Args>
void print(Args... args) {
    // 通常配合递归或逗号表达式展开
}
// 使用 sizeof...(Args) 获取参数个数
```

### 3.17 线程支持（C++11）
```cpp
#include <thread>
void hello() { cout << "Hello from thread" << endl; }
std::thread t(hello);
t.join();
```
另有 `std::mutex`, `std::lock_guard`, `std::condition_variable` 等。

### 3.18 正则表达式、计时等库（C++11）
```cpp
#include <regex>
#include <chrono>
std::regex pattern(R"(\d+)");
auto start = std::chrono::steady_clock::now();
```

---

### 3.19 C++14 新增特性补充
- **泛型 lambda** （见 3.7）
- **变量模板**
```cpp
template<typename T>
constexpr T pi = T(3.1415926535897932385);
float f = pi<float>;
```
- **`std::make_unique`** （见 3.6）
- **二进制字面量** `0b1010`
- **数字分位符** `1'000'000`
- **`decltype(auto)`**
```cpp
int x = 5;
decltype(auto) y = x;  // int
decltype(auto) z = (x); // int&
```

---

### 3.20 C++17 新特性（常用，C++20 之前）
以下特性需 `-std=c++17` 支持。

#### 结构化绑定
```cpp
pair<int, string> p{1, "hello"};
auto [id, msg] = p;  // id=1, msg="hello"

map<int, string> m{{1,"a"}};
for (const auto& [key, value] : m) { ... }
```

#### if constexpr (编译期 if)
```cpp
template<typename T>
auto getValue(T t) {
    if constexpr (std::is_pointer_v<T>)
        return *t;
    else
        return t;
}
```

#### 内联变量
```cpp
// 头文件中可定义
inline int myVar = 42;
```

#### 折叠表达式（配合可变参数模板）
```cpp
template<typename... Args>
auto sum(Args... args) {
    return (... + args); // 一元右折叠
}
```

#### 类模板参数推导 (CTAD)
```cpp
vector v{1,2,3};         // 自动推导为 vector<int>
pair p{2, "world"};      // pair<int, const char*>
```

#### 新标准库组件
- `std::optional<T>` 表示可能缺失的值。
- `std::variant<Ts...>` 类型安全的联合体。
- `std::any` 存储任意类型。
- `std::string_view` 字符串视图，避免拷贝。
- 文件系统库 `<filesystem>`。

---

## 四、总结：C/C++ 核心区分速查表

| 特性     | C 语言                           | C++ 语言                        |
| -------- | -------------------------------- | ------------------------------- |
| 编程范式 | 面向过程                         | 面向对象、泛型、函数式          |
| 布尔类型 | C99 `_Bool` (需宏)               | 内置 `bool`                     |
| 空指针   | `NULL`                           | `nullptr`                       |
| 函数重载 | 不支持                           | 支持                            |
| 默认参数 | 不支持                           | 支持                            |
| 引用     | 无                               | 左值引用 &、右值引用 &&         |
| 动态内存 | `malloc/free`                    | `new/delete`，智能指针          |
| 字符串   | 字符数组                         | `std::string`                   |
| 命名空间 | 无                               | `namespace`                     |
| 类型转换 | `(type)`                         | `static_cast` 等四种            |
| 结构体   | 只能包含数据                     | 可以有成员函数、继承            |
| 枚举     | 普通枚举，值泄露                 | `enum class` 强作用域           |
| 输入输出 | `printf/scanf`                   | `cin/cout` 流                   |
| 头文件   | `<stdio.h>`                      | `<cstdio>` 或 `<iostream>`      |
| 常量     | `const` 只读变量（C99 VLA 例外） | `const` 编译期常量，`constexpr` |
| 新标准   | C11 原子、线程等（很少用）       | C++11/14/17 大量现代特性        |

