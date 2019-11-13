[TOC]
# 前言
最近一直到在弄**蓝牙**的项目，主要是因为**Amazon Alexa**、**小度蓝牙**APP使用的**AMA**、**DMA**协议都是使用的Protobuf定义的，所以需要对它有一些了解。

Protocol Buffers 是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。它很适合做数据存储或 RPC 数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式。目前提供了多种语言的 API。

ubuntu安装了protobuf编译环境后，执行` $ protoc-c -h` or `$ protoc -h`这2个命令就可以知道目前可以支持非常多的语音；
> --c_out=OUT_DIR             Generate C/H files
>--cpp_out=OUT_DIR      Generate C++ header and source.
  --csharp_out=OUT_DIR        Generate C# source file.
  --java_out=OUT_DIR          Generate Java source file.
  --js_out=OUT_DIR            Generate JavaScript source.
  --objc_out=OUT_DIR          Generate Objective C header and source.
  --php_out=OUT_DIR           Generate PHP source file.
  --python_out=OUT_DIR        Generate Python source file.
  --ruby_out=OUT_DIR          Generate Ruby source file.

# 定义.proto文件
我这里随便定义了一个`UserInformation.proto`.
```c
syntax = "proto3";
option optimize_for = LITE_RUNTIME;

enum UserStatus {
	UNKNOWN = 0;
	IDLE = 1;
	BUSY = 2;
}

message UserInformation {
	string name = 1;
	uint32 age = 2;	
	string phone = 3;
	UserStatus stat = 4;
	string email = 5;
}
```
在`.proto`中**optimize_for**的参数：
`option optimize_for = LITE_RUNTIME;`
**optimize_for**是文件级别的选项，Protocol Buffer定义三种优化级别`SPEED/CODE_SIZE/LITE_RUNTIME`。缺省情况下是`SPEED`。

**SPEED**: 表示生成的代码运行效率高，但是由此生成的代码编译后会占用更多的空间。
**CODE_SIZE**: 和`SPEED`恰恰相反，代码运行效率较低，但是由此生成的代码编译后会占用更少的空间，通常用于资源有限的平台，如Mobile。
**LITE_RUNTIME**: 生成的代码执行效率高，同时生成代码编译后的所占用的空间也是非常少。这是以牺牲Protocol Buffer提供的反射功能为代价的。因此我们在C++中链接Protocol Buffer库时仅需链接libprotobuf-lite，而非libprotobuf。在Java中仅需包含protobuf-java-2.4.1-lite.jar，而非protobuf-java-2.4.1.jar。
>注：对于LITE_MESSAGE选项而言，其生成的代码均将继承自MessageLite，而非Message。

# 编译.proto文件
- 编译C code命令：`protoc-c --c_out=./ UserInformation.proto`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190124194447499.png)
- 编译C++ code命令：`protoc --cpp_out=./ UserInformation.proto`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190124194921152.png)
- 编译Java code命令：`protoc --java_out=./ UserInformation.proto`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190124200327758.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1pIT05HQ0FJMDkwMQ==,size_16,color_FFFFFF,t_70)
编译java code的时候需要修改一下之前定义的`UserInformation.proto`，添加java需要的包名：
```c
syntax = "proto3";
option java_package = "com.benjamin.protobuf";
```
# 测试demo code
对user data进行封包，主要4个步骤：
- 定义`UserInformation userInfo`变量；
- 使用proto编译生成的`user_information__init`函数初始化`userInfo`;
- 对`userInfo`进行赋值；
- 使用proto编译生成的`user_information__pack`函数将`userInfo`封包存储到`buffer`中；

```c
static size_t pack_user_data(uint8_t *buffer)
{
    UserInformation userInfo;

    user_information__init(&userInfo);

    userInfo.name = "Benjamin";
    userInfo.age = 18;    
    userInfo.phone = "0755-12345678";
    userInfo.stat = USER_STATUS__IDLE;
    userInfo.email = "ZhangSan@123.com";

    return user_information__pack(&userInfo, buffer);
}
```
对user data进行解包，主要2个步骤：
- 使用proto编译生成的`user_information__unpack`函数将`buffer`数据解包;
- 使用完后，需要使用`user_information__free_unpacked`函数释放给UserInformation `malloc`的空间；

```c
static size_t unpack_user_data(const uint8_t *buffer, size_t len)
{
    UserInformation *userInfo =  user_information__unpack(NULL, len, buffer);
    if(!userInfo){
        printf("user_information__unpack is fail!!!\n");
        return 1;
    }

    printf("Unpack: %s %d %s %s\n", userInfo->name, userInfo->age, userInfo->phone, userInfo->email);
    user_information__free_unpacked(userInfo, NULL);

    return 0;
}
```
> 注意：反序列化，xx_unpack 接口是会申请空间后返回指针出来，使用完成后需调用 xx__free_unpacked 进行释放；

main函数进行调用
```c
int main()
{
    uint8_t buffer[1024];
    
    size_t lenght = pack_user_data(buffer);
    printf("User data len: %ld\n",lenght);
    unpack_user_data(buffer, lenght);
	
	return 0;
}
```
运行的结果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190124203445421.png)

>参考博客地址：
