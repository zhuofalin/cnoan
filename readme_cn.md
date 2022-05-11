# cnoan: Chinese numerals and Arabic numerals conversion

-------

## 项目简介
♠ **`cnoan`** 是一个快速转化 `中文数字` 和 `阿拉伯数字` 的工具包！其中  
**`cn`** 是特指中文数字(Chinese numerals)  
**`an`** 是特指阿拉伯数字(Arabic numerals)  
**`o`** 代表的是互转  
♥ 互转中的`互`很难翻译 /(ㄒoㄒ)/~~  
如果使用`mutual`的首字母的话，那本工程名儿就感觉在🐎人（传播不良言论🔪，关小黑屋❎）;  
大致就是互转的意思，二者之间通过 __c__ 连接，又只能体现出单向👉的含义;  
因此，中间就用`o`来连接，可以在一定程度上体现出`·互·` `·环·`的概念;  
♦ 这个工程是在[cn2an](https://github.com/Ailln/cn2an.git)的思路和引导下就遇到或存在的问题作功能的更新；  
欢迎大家star和folk, 大家一起来维护和进步;  
♣ 哎，就很棒 *★,°*:.☆(￣▽￣)/$:*.°★* 。
----

## 目录结构
```
   目录名             功能与描述                       更新内容
|---an2cn.py    将阿拉伯数字转为中文数字                新定义类名
|---base.py     这是工程的基类，内有ConvertBase的基类       无
|---cn2an.py    将中文数字转为阿拉伯数字                新定义类名
|---config.yaml 工程的配置，主要是匹配规则的定义      新增abnormal字段
|---setup.py    工程的打包、封装和发布                 新增我的信息

|---translate.py 转换句子中的确定转换的内容           使用到abnormal字段
                 带参数                               修改了正则表达式
|---utils.py    基础功能的辅助定义                          无
|---requirement.txt 工程所需要的包                         无
```
------

## 项目功能
### 基础功能
#### 1.1 `中文数字` => `阿拉伯数字`

- 支持 `中文数字` => `阿拉伯数字`；
- 支持 `大写中文数字` => `阿拉伯数字`；
- 支持 `中文数字和阿拉伯数字` => `阿拉伯数字`；

#### 1.2 `阿拉伯数字` => `中文数字`

- 支持 `阿拉伯数字` => `中文数字`；
- 支持 `阿拉伯数字` => `大写中文数字`；
- 支持 `阿拉伯数字` => `大写人民币`；

#### 1.3 句子转化

- 支持 `中文数字` => `阿拉伯数字`；
    - 支持 `日期`；
    - 支持 `分数`；
    - 支持 `百分比`；
    - 支持 `摄氏度`；

- 支持 `阿拉伯数字` => `中文数字`；
    - 支持 `日期`；
    - 支持 `分数`；
    - 支持 `百分比`；
    - 支持 `摄氏度`；

#### 1.4 其他

- 支持 `小数`；
- 支持 `负数`；
- 支持 `HTTP API`。

### 功能更新和修复
- 🎈 重新定义待翻译（转换）的字段位置(●'◡'●)   
  原始工程(transform+cn2en)会出现以下情况
    ```
    七上八下 --> 7上8下
    两人    --> 2人
    ```
  其实，在实际应用中，我们是不希望其进行转换的。因此在本工程中重新定义了转换的前提  
    ```python
    '原始': 
        self.cn_pattern = f"负?([零一二三四五六七八九十拾百佰千仟万亿]+点)?[零一二三四五六七八九十拾百佰千仟万亿]+"
    ```
  ```python
  '现在':
        self.cn_pattern = f"负?-?正?\+?([零一二三四五六七八九十][\s\t]*[十拾百佰千仟万亿]+)(点[零一二三四五六七八九十]+)?"
  ```
  当然，我这儿也不敢保证该规则能够帮助大家解决相应的业务需求。因此，大家可以在[translate](translate.py)的 __self.cn_pattern__ 中进行重新定义。  

- 🎈 引入了异常词汇(abnormal words)的隔离转换和回归原位 o(*￣▽￣*)ブ  
当定义了上述重新定义的判别标准，可以避免了诸如`万宁`、`万一`，`七上八下`的情况，但是仍然需要感叹中文的博大精深
![1](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fp4.itc.cn%2Fq_70%2Fimages03%2F20201008%2Fcd02fb0107ba41c1aaafb8efb6e87e4e.gif&refer=http%3A%2F%2Fp4.itc.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1654829378&t=265ee0f768696f94d03b8900bdad556e)
```python
'例如':
    '一五一十'
...
```
这个词如果直接丢进去，就会得到下述结果：
```python
:return: '一五10'
```
这不行。在本工程中我将该类似的内容归为`abnormal words`,具体参照[config中的abnormal_words](config.yaml)  
```python
'思路'：
# encoder
  masks = ['一五一十', '']  # list[str, str, ...] define abnormal words 
  inputs = str('XXXxxx')
  mask_contents = {}
  for index, item in enumerate(masks):
      if item in inputs:
          mask = f'_MASK_{index}_'
          mask_contents[mask] = item
          inputs = inputs.replace(item, mask)
# decoder
  for contents in list(mask_contents.keys()):
      if contents in output:
          output = output.replace(contents, mask_contents[contents])
```
- 🎈 修改原始工程里面的一个点儿  
原始工程量存在一种情况：当`两`、`甘`，`幺`等出现在文中，且不是需转换的内容时，当执行下述demo段时，
```python
  inputs = str('XXXXXxxx')
  inputs = inputs.replace("廿", "二十").replace("半", "0.5").replace("两", "2")
```
就提前会将这些词儿转了，因此，本工程是在经过正则化判别之后再做相应的转换。

- 🎈 做一点点细节上的处理
我们在日常任务和书写paper中经常会定义一种不成文的规则：  
10000要书写成10,000的样式，因此，本工程也’被迫‘加入了该规则😔  

经过上述一系列操作之后，最终的效果如下所示：
```python
from cnoan.translate import Translate
inputs = '这人坏滴很，王尼玛一五一十的收入为一万元, 而两人却告诉我是二千元'
mode = 'cn2an'
tans = Translate()
print(tans.convert("这人坏滴很，王尼玛一五一十的收入为一万元, 而两人却告诉我是二千元", "cn2an"))
# 这人坏滴很，王尼玛一五一十的收入为10,000元, 而两人却告诉我是2,000元
```

## 项目安装和使用
### 安装
+ 方法一:
    ```
  pip install cnocn
  ```
+ 方法二:
  ```
  git clone https://github.com/zhuofalin/cnoan.git
  cd cnoan
  python setup.py install
  ```
+ 方法三:
  ```
  git clone https://github.com/zhuofalin/cnoan.git
  copy cnoan to your project
  ```

### 使用
```python
# 在文件首部引入包
import cnoan

# 查看当前版本号
print(cnoan.__version__)
# 0.5.16
```

### 3.1 `中文数字` => `阿拉伯数字`

> 最大支持到 `10**16`，即 `千万亿`，最小支持到 `10**-16`。

```python
import cnoan

# 在 strict 模式（默认）下，只有严格符合数字拼写的才可以进行转化
output = cnoan.cn2an("一百二十三")
# 或者
output = cnoan.cn2an("一百二十三", "strict")
# output:
# 123

# 在 normal 模式下，可以将 一二三 进行转化
output = cnoan.cn2an("一二三", "normal")
# output:
# 123

# 在 smart 模式下，可以将混合拼写的 1百23 进行转化
output = cnoan.cn2an("1百23", "smart")
# output:
# 123

# 以上三种模式均支持负数
output = cnoan.cn2an("负一百二十三", "strict")
# output:
# -123

# 以上三种模式均支持小数
output = cnoan.cn2an("一点二三", "strict")
# output:
# 1.23
```

### 3.2 `阿拉伯数字` => `中文数字`

> 最大支持到`10**16`，即`千万亿`，最小支持到 `10**-16`。

```python
import cnoan

# 在 low 模式（默认）下，数字转化为小写的中文数字
output = cnoan.an2cn("123")
# 或者
output = cnoan.an2cn("123", "low")
# output:
# 一百二十三

# 在 up 模式下，数字转化为大写的中文数字
output = cnoan.an2cn("123", "up")
# output:
# 壹佰贰拾叁

# 在 rmb 模式下，数字转化为人民币专用的描述
output = cnoan.an2cn("123", "rmb")
# output:
# 壹佰贰拾叁元整

# 以上三种模式均支持负数
output = cnoan.an2cn("-123", "low")
# output:
# 负一百二十三

# 以上三种模式均支持小数
output = cnoan.an2cn("1.23", "low")
# output:
# 一点二三
```

### 3.3 句子转化

> ⚠️：试验性功能，可能会造成不符合期望的转化。

```python
import cnoan

# 在 cn2an 方法（默认）下，可以将句子中的中文数字转成阿拉伯数字
output = cnoan.translate("小王捡了一百块钱")
# 或者
output = cnoan.translate("小王捡了一百块钱", "cn2an")
# output:
# 小王捡了100块钱

# 在 an2cn 方法下，可以将句子中的中文数字转成阿拉伯数字
output = cnoan.translate("小王捡了100块钱", "an2cn")
# output:
# 小王捡了一百块钱


## 支持日期
output = cnoan.translate("小王的生日是二零零一年三月四日", "cn2an")
# output:
# 小王的生日是2001年3月4日

output = cnoan.translate("小王的生日是2001年3月4日", "an2cn")
# output:
# 小王的生日是二零零一年三月四日

## 支持分数
output = cnoan.translate("抛出去的硬币为正面的概率是二分之一", "cn2an")
# output:
# 抛出去的硬币为正面的概率是1/2

output = cnoan.translate("抛出去的硬币为正面的概率是1/2", "an2cn")
# output:
# 抛出去的硬币为正面的概率是二分之一

## 支持百分比
## 支持摄氏度
```
## 7 许可证

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)
[![](https://award.dovolopor.com?lt=Ailln's&rt=idea&lbc=lightgray&rbc=red&ltc=red)](https://github.com/Ailln/award)

##  交流

大家有任何疑问可通过[邮件](1822643111@qq.com)和我交流，我将尽可能及时回复。

##  致谢

- [Thunder Bouble](https://github.com/sfyc23): 提出很多有效的反馈，包括一些 bug 和新功能；
- [Damon Yu](https://github.com/20071313): 增加对全角数字和全角符号的支持。

##  参考

- [🎈 cn2an 核心代码解析](https://www.v2ai.cn/2020/06/30/python/8-cn2an/)
- [如何发布自己的包到 pypi](https://www.v2ai.cn/2018/07/30/python/1-pypi/)
- [Python 中的小陷阱](https://www.v2ai.cn/2019/01/01/python/4-python-trap/)
- [汉字数字转阿拉伯数字](https://www.zouyesheng.com/han-number-convert.html)
- [Chinese Text Normalization for Speech Processing](https://github.com/speechio/chinese_text_normalization)
- [The Best Tool of Chinese Number to Digits](https://github.com/Wall-ee/chinese2digits)
- [Microsoft Recognizers Text Overview](https://github.com/microsoft/Recognizers-Text)
- [process: 数据预处理管道](https://github.com/Ailln/proces)
