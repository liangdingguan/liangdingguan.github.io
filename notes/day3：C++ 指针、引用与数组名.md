---
title: C/C++补充3:指针、引用、数组名
date: 2026-07-06
tags: [C++, 笔记]
summary:  内存与指针相关内容
slug: c-cpp-basic-syntax-content23
---
## 进阶学习其三：C++ 指针、引用与数组名

> author:梁鼎冠

## 一、指针（Pointer）基础

### 1.1 什么是指针
- 指针是一个变量，存储另一个变量的**内存地址**。
- 通过地址可以间接访问该变量。
- 类型：`类型*`，例如 `int* p` 表示指向 `int` 的指针。

### 1.2 基本操作
- `&` 取地址运算符。
- `*` 解引用运算符（访问指针指向的对象）。

#### 示例1：指针的基本声明、赋值与使用

```cpp
#include <iostream>
using namespace std;

int main() {
    int var = 42;
    int* ptr = &var;   // ptr 指向 var 的地址

    cout << "var 的值: " << var << endl;
    cout << "var 的地址: " << &var << endl;
    cout << "ptr 存储的地址: " << ptr << endl;
    cout << "ptr 解引用后的值: " << *ptr << endl;

    // 通过指针修改变量
    *ptr = 100;
    cout << "修改后 var 的值: " << var << endl;

    return 0;
}
```

### 1.3 指针的运算
- 指针加减整数：移动 `sizeof(指向类型)` 个字节。
- 指针相减：得到元素个数差。

#### 示例2：指针算术运算

```cpp
#include <iostream>
using namespace std;

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int* p = arr;      // 指向数组第一个元素
    cout << "*p = " << *p << endl;

    p++;               // 现在指向 arr[1]
    cout << "*p = " << *p << endl;

    p += 2;            // 指向 arr[3]
    cout << "*p = " << *p << endl;

    int* q = &arr[4];
    cout << "q - p = " << q - p << endl;  // 输出 1（相差1个元素）

    return 0;
}
```

### 1.4 动态内存分配（new / delete）
- `new` 在堆上分配内存，返回指针。
- `delete` 释放内存。
- 对于数组：`new[]` 和 `delete[]` 匹配使用。

#### 示例3：动态分配与释放

```cpp
#include <iostream>
using namespace std;

int main() {
    // 单个对象
    int* p = new int(99);
    cout << "*p = " << *p << endl;
    delete p;

    // 数组
    int* arr = new int[10];
    for (int i = 0; i < 10; ++i)
        arr[i] = i * i;

    for (int i = 0; i < 10; ++i)
        cout << arr[i] << " ";
    cout << endl;

    delete[] arr;   // 注意数组释放需用 delete[]

    return 0;
}
```

> **注意**：避免内存泄漏，每个 `new` 都要有对应的 `delete`。

---

## 二、引用（Reference）

### 2.1 引用的概念
- 引用是已存在变量的**别名**，不占用额外内存（逻辑上）。
- 定义时必须初始化，且不能再引用其他变量。
- 语法：`类型& 引用名 = 变量;`

#### 示例4：引用的基本使用

```cpp
#include <iostream>
using namespace std;

int main() {
    int original = 5;
    int& ref = original;   // ref 是 original 的别名

    cout << "original = " << original << ", ref = " << ref << endl;

    ref = 10;
    cout << "修改 ref 后：original = " << original << endl;

    // int& ref2;  // 错误：引用必须初始化

    return 0;
}
```

### 2.2 引用作为函数参数（传引用）
- 可以修改实参，避免拷贝开销（尤其是大对象）。

#### 示例5：交换两个数（比较传值与传引用）

```cpp
#include <iostream>
using namespace std;

// 传值：无法改变实参
void swapByValue(int a, int b) {
    int temp = a; a = b; b = temp;
}

// 传指针：可以改变实参
void swapByPointer(int* a, int* b) {
    int temp = *a; *a = *b; *b = temp;
}

// 传引用：可以改变实参，语法更简洁
void swapByReference(int& a, int& b) {
    int temp = a; a = b; b = temp;
}

int main() {
    int x = 1, y = 2;
    swapByValue(x, y);
    cout << "swapByValue: x=" << x << " y=" << y << endl; // 未交换

    x = 1; y = 2;
    swapByPointer(&x, &y);
    cout << "swapByPointer: x=" << x << " y=" << y << endl;

    x = 1; y = 2;
    swapByReference(x, y);
    cout << "swapByReference: x=" << x << " y=" << y << endl;

    return 0;
}
```

### 2.3 引用作为函数返回值
- 可以返回局部变量的引用？**危险**（局部变量在函数结束时销毁，返回悬空引用）。
- 可返回静态变量、全局变量、类成员、或者通过参数传入的引用。

#### 示例6：返回引用（正确用法）

```cpp
#include <iostream>
using namespace std;

int& getElement(int arr[], int index) {
    return arr[index];   // 返回数组元素的引用
}

int main() {
    int arr[] = {10, 20, 30};
    getElement(arr, 1) = 99;   // 通过引用修改数组元素
    cout << "arr[1] = " << arr[1] << endl;  // 输出 99
    return 0;
}
```

### 2.4 指针与引用的区别总结

| 特性         | 指针               | 引用                           |
| ------------ | ------------------ | ------------------------------ |
| 是否可为空   | 是（需判空）       | 否，必须初始化                 |
| 可否重新指向 | 可以（改存地址）   | 不可，终身绑定                 |
| 算术运算     | 支持（如 ++）      | 不支持                         |
| 占用内存     | 通常占用4/8字节    | 逻辑上不占（编译器实现可能占） |
| 访问成员     | 用 `->` 或 `(*p).` | 用 `.`                         |

> 在C++中，推荐优先使用引用，除非需要“空值”或“重新绑定”的能力。

---

## 三、数组名（Array Name）

### 3.1 数组名是指针常量
- 一维数组名可以看作指向第一个元素的常量指针，不能改变其指向。
- `sizeof(数组名)` 返回整个数组大小（字节），而 `sizeof(指针)` 返回指针本身大小。

#### 示例7：数组名与指针的区别

```cpp
#include <iostream>
using namespace std;

int main() {
    int arr[5] = {1,2,3,4,5};
    int* ptr = arr;   // 合法：数组名隐式转换为指针

    cout << "sizeof(arr) = " << sizeof(arr) << " 字节" << endl; // 20 (4*5)
    cout << "sizeof(ptr) = " << sizeof(ptr) << " 字节" << endl; // 8 (64位系统)

    // arr = ptr;     // 错误：数组名是常量，不能赋值
    ptr = arr + 2;    // 指针可以重新指向

    cout << "arr[2] = " << arr[2] << endl;
    cout << "ptr[0] = " << ptr[0] << endl;  // 指针也可用下标

    return 0;
}
```

### 3.2 数组名作为函数参数
- 传递数组名实际上传递的是**指向首元素的指针**，大小信息丢失，需额外传递长度。

#### 示例8：数组参数退化为指针

```cpp
#include <iostream>
using namespace std;

void printArray(int arr[], int size) {   // 这里的 arr 其实是 int*
    cout << "函数内 sizeof(arr) = " << sizeof(arr) << endl; // 8（指针大小）
    for (int i = 0; i < size; ++i)
        cout << arr[i] << " ";
    cout << endl;
}

int main() {
    int arr[5] = {1,2,3,4,5};
    cout << "main内 sizeof(arr) = " << sizeof(arr) << endl; // 20
    printArray(arr, 5);
    return 0;
}
```

---

### 3.3 关于堆空间与栈空间的补充说明

| 内存区域   | 管理者     | 分配速度 | 大小限制         | 生命周期                       | 典型用途           |
| :--------- | :--------- | :------- | :--------------- | :----------------------------- | :----------------- |
| **栈**     | 编译器自动 | 很快     | 小（通常1~8MB）  | 函数执行期间，结束时自动释放   | 局部变量、函数参数 |
| **堆**     | 程序员手动 | 较慢     | 大（可申请GB级） | new/delete 或 malloc/free 控制 | 大块数据、动态大小 |
| **静态区** | 编译器     | 中等     | 中等（全局区）   | 整个程序运行期间               | 全局变量、静态变量 |

```cpp
#include <iostream>

int global_var = 10;      // 静态区（全局变量）
static int static_var = 20; // 静态区（静态全局变量）

void func() {
    int local_var = 30;   // 栈空间（局部变量）
    static int local_static = 40; // 静态区（函数内静态变量，只初始化一次）

    int* heap_var = new int(50);  // 堆空间（手动分配）
    delete heap_var;              // 必须手动释放
}

int main() {
    func();
    return 0;
}
```

- 本质上都是内存的某块区域，只是使用方式不同导致叫法不同，堆空间因为不是自动的，使用delete之后可能会存在内存空缺，而栈内存不会在中间某一块空缺。
