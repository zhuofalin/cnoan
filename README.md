## Chinese numerals and Arabic numerals conversion

There should be emojis here (●'◡'●)

Project Description and Description [English Version](readme.md)  
工程说明与描述[中文版本](readme_cn.md)

♠ **`cnoan`** is a toolkit to quickly convert `Chinese numbers` and `Arabic numbers`! in  
  **`cn`** refers to Chinese numerals  
  **`an`** refers specifically to Arabic numerals  
  **`o`** stands for reciprocal  

♥ The Chinese `互` in the interchange is difficult to translate and shorthand /(ㄒoㄒ)/~~
If the first letter of `mutual` is used, then the name of this project will feel like 🐎 people  
(spread bad speech 🔪, close the small black house❎);   
Roughly, it means mutual rotation. The two are connected through __c__, which can only reflect the meaning of one-way or one-path 👉;   
Therefore, `o` is used to connect in the middle, which can reflect the concept of `·mutual·` `·ring·` to a certain extent;  

♦ This project is based on the ideas and guidance of [cn2an](https://github.com/Ailln/cn2an.git) to update the functions of the problems encountered or existing;
Welcome to star and follow, everyone to maintain and improve together;   

♣ Hey, it's great *★,°*:.☆(￣▽￣)/$:*.°★* .  

-----

## Directory Structure
````
   Catalog Name                 Function and Description                             What's New
|--------------------------------------------------------------------------------------------------------
|---an2cn.py         Convert Arabic numerals to Chinese numerals               Newly defined class names
|--------------------------------------------------------------------------------------------------------
|---base.py          This is the base class of the project,                             None
                     which contains the base class of ConvertBase 
|--------------------------------------------------------------------------------------------------------
|---cn2an.py         Convert Chinese numbers to Arabic numbers                 Newly defined class names
|--------------------------------------------------------------------------------------------------------
|---config.yaml      The configuration of the project,                         Add the abnormal field
                     mainly the definition of the matching rules 
|--------------------------------------------------------------------------------------------------------
|---setup.py         Project packaging and publishing                          Add my information
|--------------------------------------------------------------------------------------------------------
|---translate.py     Convert the content in the sentence                       Modified regular expression
                     that determines the conversion
                     With parameters
|--------------------------------------------------------------------------------------------------------
|---utils.py         Definition of basic functions in utils.py                          None
|--------------------------------------------------------------------------------------------------------
|---requirement.txt  The package required by the project                                None
|--------------------------------------------------------------------------------------------------------
````
------

## Project Function
### basic function
#### 1.1 `Chinese numbers` => `Arabic numbers`

- Support `Chinese numbers` => `Arabic numbers`;
- Support `Uppercase Chinese numbers` => `Arabic numbers`;
- Support `Chinese numbers and Arabic numbers` => `Arabic numbers`;

#### 1.2 `Arabic numbers` => `Chinese numbers`

- Support `Arabic numbers` => `Chinese numbers`;
- Support `Arabic numbers` => `Uppercase Chinese numbers`;
- Support `Arabic numerals` => `Uppercase RMB`;

#### 1.3 Sentence Transformation

- Support `Chinese numbers` => `Arabic numbers`;
    - support `date`;
    - support `score`;
    - support `percent`;
    - support `Celsius`;

- Support `Arabic numbers` => `Chinese numbers`;
    - support `date`;
    - support `score`;
    - support `percent`;
    - support `Celsius`;

#### 1.4 Others

- support `decimal`;
- support `negative numbers`;
- Support for `HTTP API`.

### Function updates & Fixes
- 🎈 Redefine the field position to be translated (translated) (●'◡'●)
  The original project (transform+cn2en) will have the following situations
    ````
    七上八下 --> 7上8下
    两人    --> 2人
    一旦    --> 1旦
    ````
  In fact, in practical applications, we do not want it to be converted. Therefore, the premise of conversion is redefined in this project
   ```python
    'Original': 
        self.cn_pattern = f"负?([零一二三四五六七八九十拾百佰千仟万亿]+点)?[零一二三四五六七八九十拾百佰千仟万亿]+"
    ```
  ```python
  'Now':
        self.cn_pattern = f"负?-?正?\+?([零一二三四五六七八九十][\s\t]*[十拾百佰千仟万亿]+)(点[零一二三四五六七八九十]+)?"
  ```
  Of course, I can't guarantee that this rule can help you solve the corresponding business needs. Therefore, you can redefine it in __self.cn_pattern__ of [translate](translate.py).

- 🎈 Introduced isolation conversion and regression of abnormal words o(*￣▽￣*)ブ
When the above redefinition criteria are defined, situations such as `Wanning`, `In case`, and `seven up and eight down` can be avoided, but it is still necessary to sigh the vastness and profoundness of Chinese  

![1](https://img1.baidu.com/it/u=1108671039,3873010749&fm=253&fmt=auto&app=138&f=GIF?w=254&h=245)
````python
'E.g':
    '一五一十'
...
````
If the word is thrown in directly, the following results will be obtained:
````python
:return: '一五10'
````
This doesn't work. In this project, I classify this similar content as `abnormal words`, refer to [abnormal_words in config](config.yaml)
````python
'Thinking':
# encoder
  masks = ['1510', ''] # list[str, str, ...] define abnormal words
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
````
- 🎈 Modify a point in the original project
There is a situation in the original engineering quantity: when `两`、`甘`，`幺`, etc. appear in the text, and are not the content to be converted, when the following demo segment is executed,
````python
  inputs = str('XXXXxxx')
  inputs = inputs.replace("甘", "twenty").replace("半", "0.5").replace("两", "2")
````
These words will be converted in advance, so this project will do the corresponding conversion after regularization judgment.

- 🎈 Do a little of detail
We often define an unwritten rule in our daily tasks and writing papers:
10,000 has to be written in the style of 10,000, so this project is also 'forced' to join this rule 😔  

After the above series of operations, the final effect is as follows:
```python
from cnoan.translate import Translate
inputs = '这人坏滴很，王尼玛一五一十的收入为一万元, 而两人却告诉我是二千元'
mode = 'cn2an'
tans = Translate()
print(tans.convert("这人坏滴很，王尼玛一五一十的收入为一万元, 而两人却告诉我是二千元", "cn2an"))
# 这人坏滴很，王尼玛一五一十的收入为10,000元, 而两人却告诉我是2,000元
```
----
## Project Installation & Usage
### Install
+ Method 1:
    ```
  pip install cnocn
  ```
+ Method 2:
 ```
git clone https://github.com/zhuofalin/cnoan.git
cd cnoan
python setup.py install
```
+ Method 3:
  ```
  git clone https://github.com/zhuofalin/cnoan.git
  copy cnoan to your project
  ```
### Usage
```python
# import package which you need
import cnoan

# View the current version number
print(cnoan.__version__)
# 0.5.16  #  will be different
```

### 3.1 `Chinese numbers` => `Arabic numerals`

> The maximum support is `10**16`, that is, `Terabillion`  
> and the minimum support is `10**-16`.

```python
import cnoan

output = cnoan.cn2an("一百二十三")
# or
output = cnoan.cn2an("一百二十三", "strict")
# output:
# 123

output = cnoan.cn2an("一二三", "normal")
# output:
# 123

output = cnoan.cn2an("1百23", "smart")
# output:
# 123

# The above three modes all support negative numbers
output = cnoan.cn2an("负一百二十三", "strict")
# output:
# -123

# All three modes above support decimals
output = cnoan.cn2an("一点二三", "strict")
# output:
# 1.23
```

### 3.2 `Arabic numerals` => `Chinese numbers`

> The maximum support is `10**16`, that is, `Terabillion`  
> and the minimum support is `10**-16`.

```python
import cnoan

output = cnoan.an2cn("123")
# or
output = cnoan.an2cn("123", "lower")
# output:
# 一百二十三

output = cnoan.an2cn("123", "upper")
# output:
# 壹佰贰拾叁

output = cnoan.an2cn("123", "rmb")
# output:
# 壹佰贰拾叁元整

output = cnoan.an2cn("-123", "lower")
# output:
# 负一百二十三

output = cnoan.an2cn("1.23", "low")
# output:
# 一点二三
```

### 3.3 sentence transformation

> ⚠️：Experimental feature that may cause undesired conversions.

```python
import cnoan

output = cnoan.translate("小王捡了一百块钱")
# or
output = cnoan.translate("小王捡了一百块钱", "cn2an")
# output:
# 小王捡了100块钱

output = cnoan.translate("小王捡了100块钱", "an2cn")
# output:
# 小王捡了一百块钱


## data
output = cnoan.translate("小王的生日是二零零一年三月四日", "cn2an")
# output:
# 小王的生日是2001年3月4日

output = cnoan.translate("小王的生日是2001年3月4日", "an2cn")
# output:
# 小王的生日是二零零一年三月四日

## support score
output = cnoan.translate("抛出去的硬币为正面的概率是二分之一", "cn2an")
# output:
# 抛出去的硬币为正面的概率是1/2

output = cnoan.translate("抛出去的硬币为正面的概率是1/2", "an2cn")
# output:
# 抛出去的硬币为正面的概率是二分之一

## support %
## support ℃
```
-----------
## License

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)
[![](https://award.dovolopor.com?lt=Ailln's&rt=idea&lbc=lightgray&rbc=red&ltc=red)](https://github.com/Ailln/award)

-----
##  communicate

If you have any questions, you can communicate with me through [email] (1822643111@qq.com), and I will reply as soon as possible.

-----
## Thanks

- [Thunder Bouble](https://github.com/sfyc23): A lot of useful feedback, including some bugs and new features;
- [Damon Yu](https://github.com/20071313): Added support for full-width numbers and full-width symbols.

##  Reference

- [cn2an core code analysis](https://www.v2ai.cn/2020/06/30/python/8-cn2an/)
- [How to publish your own package to pypi](https://www.v2ai.cn/2018/07/30/python/1-pypi/)
- [Small traps in Python](https://www.v2ai.cn/2019/01/01/python/4-python-trap/)
- [Chinese characters to Arabic numerals](https://www.zouyesheng.com/han-number-convert.html)
- [Chinese Text Normalization for Speech Processing](https://github.com/speechio/chinese_text_normalization)
- [The Best Tool of Chinese Number to Digits](https://github.com/Wall-ee/chinese2digits)
- [Microsoft Recognizers Text Overview](https://github.com/microsoft/Recognizers-Text)
- [process: data preprocessing pipeline](https://github.com/Ailln/proces)
