.. _armstardupandinitialization:

ARM 内核启动和初始化
========================


ARM 官网资料
~~~~~~~~~~~~~~

`ARM 的官方学习资料链接 <https://developer.arm.com/documentation/>`_

这里我下载了 `Arm Compiler armasm User Guide Version 6.6 <https://documentation-service.arm.com/static/5f4e199fca7b6a33993777ec?token=>`_ 。
可以用来查看ARM的指令以及用法。

以及 `ARMv7-M Architecture Reference Manual <https://documentation-service.arm.com/static/5f10695d0daa596235e7f8e6?token=>`_ 。
可以用来学习 Crotex-M3/M4 的CPU架构以及内存。


`ARM Compiler C Library Startup and Initialization <https://documentation-service.arm.com/static/5ed10b24ca06a95ce53f8bbf?token=>`_ 。
这个应用笔记可以用来学习基于ARM架构的芯片启动流程。

`ARM Compiler toolchain Developing Software for ARM Processors <https://documentation-service.arm.com/static/5ea0469a9931941038de4e40?token=>`_ 。
适用于ARM处理器的ARM编译器工具链开发软件。

`Arm C and C++ Libraries and Floating-Point Support User Guide <https://documentation-service.arm.com/static/5f8020b8bcda971b1456832a?token=>`_ 。 

`ARM Compiler toolchain Linker Reference <https://documentation-service.arm.com/static/5ea6aec39931941038def203?token=>`_ 。 

ARM 启动代码
~~~~~~~~~~~~~~~

嵌入式应用程序在用户定义的 `main()` 函数启动之前需要初始化序列。 这称为启动代码( `startup code` 或者 `boot code` )。 
`ARM C` 库包含启动应用程序所必需的预编译和预组装代码段。链接应用程序时，链接器会根据应用程序从 C 库中包含必要的代码，
以便为应用程序创建自定义启动代码。但需要注意的是，ARM 自己的编译套件提供了如下三种库：

- C standardlib
- C microlib
- C++

本文档中描述的启动代码适用于标准 ARM C 库。 它不适用于 ARM C 微库。 对于ARMv4T和更高版本的体系结构，这也是常见的。

C库的入口地址
~~~~~~~~~~~~~~~

函数 `__main` 默认是C库的入口点。 函数 `__main` 是C库的入口点。 除非进行更改，否则__main是ARM链接器（armlink）在创建映像时使用的ELF映像的默认入口点。 
下图显示了C库启动期间 `__main` 调用的函数。

__rt_entry 函数会在后面专门讲解。

__scatterload
----------------

我们可以先来看看官方文档的描述。(这里我翻译的可能不是很好。)

应用程序代码和数据可以在根区域或非根区域中。根区域具有相同的加载时间和执行时间地址。非根区域具有不同的加载时间和执行时间地址。
根区域包含ARM链接器输出的区域表。区域表包含需要初始化的非根代码和数据区域的地址。区域表还包含一个函数指针，该指针指示该区域需要进行哪些初始化，
例如复制，清零或解压缩函数。

`__scatterload` 遍历区域表并初始化各种执行时区域。 有以下功能：

- 将零初始化区域 （Zero Initialized sections：简称ZI sections ） 初始化为零
- 将非根(RO和RW)运行区域从其加载时位置复制或解压缩到执行时区域。如果压缩了任何数据段，则将它们从加载地址解压缩到执行地址。

`__main` 总是在启动期间在调用 `__rt_entry` 之前调用此函数。

其实，简单的讲， `__scatterload` 主要的职责就是把 `RW/RO` 输出段从加载地址( `LMA` )复制到运行地址( `VMA` )，并完成了ZI运行域的初始化工作。

比如比较常见的， 我们经常把固件烧录到芯片的 Flash 里面，运行的时候需要把 RW/RO 输出段 从 Flash 搬到 RAM 上运行。当然了，我们也可以指定部分代码直接在 RAM 当中。

“ARM程序” 是指在ARM系统中正在执行的程序，而非保存在ROM或者Flash 中的 .bin(.axf,.hex)映像（image）文件。

一个ARM程序包含3部分：RO，RW和ZI

- RW  : Read-write , 可读写的数据，程序中已经初始化并且非0的变量。
- RO  : Read Only , 只读数据，程序中的指令和常量。
- ZI  : Zero Initialized, 程序中未初始化的变量和初始化为0的变量。

其次，我们在编译结束之后，可以在 `*.map` 或者 编译信息的结尾可以看到 `RAM size` 和 `ROM size` 之类的信息。
 
这个是如何计算出来的的。

- ZI Data: Zero Initialized Data

- RO Data 是常量。另外 一些常量（RO数据）是由编译器/链接器生成的，也可能来自库。因此它们也将存在，无论您的程序有没有显式定义任何常量。

  :: 

    Total RAM Size = RW Data + ZI Data
    Total ROM Size = Code + RO Data + RW Data


__rt_entry
----------------

我们可以先看下官网的说明，这里我翻译的可能不是太准确，

`__main` 调用 `__rt_entry` 来初始化堆栈，堆和其他C库子系统。 `__rt_entry` 调用各种初始化函数，然后调用用户级别的 `main()` 。

这里列出了 _rt_entry 可以调用的函数。 这些函数按调用顺序列出：

1. `_platform_pre_stackheap_init`
2. __ `user_setup_stackheap` 或通过其他方法设置 `StackPointer(SP)`
3. `_platform_post_stackheap_init`
4. `__rt_lib_init`
5. `_platform_post_lib_init`
6. `main()`
7. `exit()`


`_platform_ *` 函数不是标准C库的一部分。 如果定义它们，则链接器将在 `__rt_entry` 中对它们进行调用。
`main()` 是用户级别应用程序的入口点。 寄存器 `r0` 和 `r1` 包含 `main()` 的参数。 如果 `main()` 返回，
则将其返回值传递给 `exit()` ，然后应用程序退出。

`__rt_entry` 还负责设置栈和堆。但是，设置栈和堆取决于用户指定的方法。
可以通过以下任何一种方法来设置堆栈和堆：

* 调用 `__user_setup_stackheap` 。这还将获取堆使用的内存范围（堆顶部和堆底部）。
* 用符号 `__initial_sp` 的值加载 SP。
* 使用链接器分散文件中指定的 `ARM_LIB_STACK` 或 `ARM_LIB_STACKHEAP` 区域的顶部。


__rt_entry和__rt_lib_init在C库中不作为完整函数存在。这些函数的小部分出现在C库的一部分内部对象中。
并非所有这些代码段都对给定的用户应用程序有用。链接器确定给定应用程序需要那些代码节的哪个子集，并且仅在启动代码中包括那些节。
链接器按正确的顺序放置这些部分，以根据用户应用程序的要求创建自定义__rt_entry和__rt_lib_init函数。
__rt_lib_init调用的函数中介绍了__rt_lib_init调用的函数。



库函数 `__rt_entry()` 如下运行程序：

1. 可以通过多种方式设置堆栈和堆，比如调用 `__user_setup_stackheap()` 函数 ,或者调用 `__rt_stackheap_init()` 或者加载分散加载区域的绝对地址。

2. 调用 `__rt_lib_init()` 初始化引用的库函数，初始化语言环境，并在必要时为 `main()` 设置 `argc` 和 `argv` 。
对于 C++，通过 `__cpp_initialize__aeabi_` 调用任何顶级对象的构造函数。

3. 调用 `main()` ，即应用程序的用户级根目录。在 `main()` 中，您的程序可能会调用库函数。

4.使用 `main()` 返回的值调用 `exit()` 。


主应用程序结束执行后，`__rt_entry` 将库关闭，然后把控制权交换给调试器。函数标签main()具有特殊含义。
Main()函数的存在强制链接器链接到 `__main` 和 `__rt_entry` 中的代码。如果没有标记为main()的函数，则没有链接到初始化序列，
因而部分标准C库功能得不到支持。

function
~~~~~~~~~~~~~~~

_platform_pre_stackheap_init
--------------------------------
C 标准库没有提供这个函数，但是如果你有需要的话，可以自己定义它。比如，你可以使用它来设置硬件。
如果你定义了的话，`__rt_entery()` 函数需要在初始化堆栈之前调用此函数。

__user_setup_stackheap
--------------------------------
此函数可以用来设置并返回初始堆栈和堆的位置。 C库默认不提供此功能，但是您可以根据需要定义它。 
如果您定义了此函数或定义了旧版函数 `__user_initial_stackheap` ，则 `__rt_entry` 会调用此函数。 
如果定义 `__user_initial_stackheap` ，则C库提供默认的 `__user_setup_stackheap` 作为 `__user_initial_stackheap` 函数的包装。

_platform_post_stackheap_init
-------------------------------------
C 标准库没有提供这个函数，但是如果你有需要的话，可以自己定义它。比如，你可以使用它来设置硬件。
如果你定义了的话，`__rt_entery()` 函数需要在初始化堆栈之前调用此函数。

__rt_lib_init
-------------------
此函数初始化各种 C库子系统。 它初始化引用的库函数，初始化语言环境，并在必要时为 `main()`  设置 `argc` 和 `argv` 。
`__rt_entry` 始终在启动期间调用此函数。
如果使用 `__user_setup_stackheap` 或 `__user_initial_stackheap` 函数设置堆栈指针和堆，则分别将堆存储块的起始地址和结束地址
作为参数传递给寄存器 `r0` 和 `r1` 中的 `__rt_lib_init` 。
如果用户级 `main()` 需要，则该函数分别在寄存器 `r0` 和 `r1` 中返回 `argc` 和 `argv` 。

_platform_post_lib_init
---------------------------

279/5000
C 库不提供此功能，但是您可以根据需要定义它。 例如，您可以使用此功能来设置硬件。 
如果定义了此函数 `__rt_entry` 调用之后，，则在调用 `__rt_lib_init` 之后且在调用用户级 `main()` 函数之前调用此函数。


Nordic 的启动文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


启动文件里面有三大部分：

1. 堆栈的初始化
#. 初始化中断向量表
#. Reset_Handler 函数


这里我以 `Nordic` 的 `nrf52840` 的启动文件为例讲解：

因为 `Nordic` 的 SDK 中启动文件是有4种类型的。
有 Keil编译器 、IAR编译器、 SES编译器和直接调用GCC编译 4种。这里会逐个进行讲解。

Keil 编译器调用的是 `arm_startup_nrf52840.s`,
IAR 编译器调用的是 `iar_startup_nrf52840.s`,
SES 编译器调用的是 `ses_startup_nrf52840.s`,
GCC 直接编译调用的是 `gcc_startup_nrf52840.S`.

.. note::
  前面三种启动文件可以通过编译器设置配置。一般工程都是已经配置好了的，如果是自己新建的工程需要自己配置。
  最后 使用GCC 直接编译的方法需要自己在 Makefile 中添加启动文件。
  一般我们看到的 STM32的启动文件基本上几基于 Keil 编译器的。


在讲解启动文件之前，我们需要先了解一下程序的入口地址。
我们都知道通过链接器LD文件设置进程入口地址。方法有以下五种：(排名越靠前，优先级越高)

  1. `ld` 命令行的 -`e` 选项
  #. 链接脚本的ENTRY(SYMBOL)命令
  #. 如果定义了 `start` 符号, 使用 `_start` 符号值
  #. 如果存在 `.text` 段(section), 使用 `.text` 段(section) 的第一字节的位置值
  #. 直接使用数值 `0`



启动文件讲解1 
-------------------

我们先来讲解 基于 Keil 编译器的启动文件

