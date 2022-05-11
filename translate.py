#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhuofalin
@contact:1822643111@qq.com
@version: 1.0.0
@license: Apache Licence
@file: translate.py
@time: 2022/5/10 15:10
"""
import re

import utils
from base import ConvertBase
from cn2an import CN2ArabicNumerals as Cn2An
from an2cn import ArabicNumerals2CN as An2Cn


class Translate(ConvertBase):
    def __init__(self) -> None:
        super(Translate, self).__init__()
        self.conf = utils.get_default_config()
        self.all_num = "零一二三四五六七八九"
        self.all_unit = "".join(list(self.conf["unit_cn2an"].keys()))
        self.cn2an = Cn2An().convert
        self.an2cn = An2Cn().convert
        self.masks = self.conf['abnormal_words']
        # self.cn_pattern = f"负?([{self.all_num}{self.all_unit}]+点)?[{self.all_num}{self.all_unit}]+"
        # self.cn_pattern = f"负?-?正?\+?([零一二三四五六七八九]+[\s\t]*[十百千万亿]+)+点?[零一二三四五六七八九]+"
        self.cn_pattern = f"负?-?正?\+?([零一二三四五六七八九十][\s\t]*[十拾百佰千仟万亿]+)(点[零一二三四五六七八九十]+)?"
        self.smart_cn_pattern = f"-?([0-9]+.)?[0-9]+[{self.all_unit}]+"

    def convert(self, inputs: str, method: str = "cn2an") -> str:
        if method == "cn2an":
            mask_contents = {}
            for index, item in enumerate(self.masks):
                if item in inputs:
                    mask = f'_MASK_{index}_'
                    mask_contents[mask] = item
                    inputs = inputs.replace(item, mask)
                    # process
            # inputs = inputs.replace("廿", "二十").replace("半", "0.5").replace("两", "2")
            # date
            inputs = re.sub(
                fr"((({self.smart_cn_pattern})|({self.cn_pattern}))年)?([{self.all_num}十]+月)?([{self.all_num}十]+日)?",
                lambda x: self.__sub_util(x.group(), "cn2an", "date"), inputs)
            # fraction
            inputs = re.sub(fr"{self.cn_pattern}分之{self.cn_pattern}",
                            lambda x: self.__sub_util(x.group(), "cn2an", "fraction"), inputs)
            # percent
            inputs = re.sub(fr"百分之{self.cn_pattern}",
                            lambda x: self.__sub_util(x.group(), "cn2an", "percent"), inputs)
            # celsius
            inputs = re.sub(fr"{self.cn_pattern}摄氏度",
                            lambda x: self.__sub_util(x.group(), "cn2an", "celsius"), inputs)
            # number
            output = re.sub(self.cn_pattern,
                            lambda x: self.__sub_util(x.group(), "cn2an", "number"), inputs)

            for contents in list(mask_contents.keys()):
                if contents in output:
                    output = output.replace(contents, mask_contents[contents])

        elif method == "an2cn":
            mask_contents = {}
            for index, item in enumerate(self.masks):
                if item in inputs:
                    mask = f'_MASK_{index}_'
                    mask_contents[mask] = item
                    inputs = inputs.replace(item, mask)
            # date
            # inputs = inputs.replace(',', '').replace('，', '')

            inputs = re.sub(r"(\d{2,4}年)?(\d{1,2}月)?(\d{1,2}日)?",
                            lambda x: self.__sub_util(x.group(), "an2cn", "date"), inputs)
            # fraction
            inputs = re.sub(r"\d+/\d+",
                            lambda x: self.__sub_util(x.group(), "an2cn", "fraction"), inputs)
            # percent
            inputs = re.sub(r"-?(\d+\.)?\d+%",
                            lambda x: self.__sub_util(x.group(), "an2cn", "percent"), inputs)
            # celsius
            inputs = re.sub(r"\d+℃",
                            lambda x: self.__sub_util(x.group(), "an2cn", "celsius"), inputs)
            # number
            output = re.sub(r"(-?\d{1,3})(\d+|(\,{1}\d{3})+)(\.\d+)",
                            lambda x: self.__sub_util(x.group(), "an2cn", "number"), inputs)

            for contents in list(mask_contents.keys()):
                if contents in output:
                    output = output.replace(contents, mask_contents[contents])
        else:
            raise ValueError(f"error method: {method}, only support 'cn2an' and 'an2cn'!")

        return output

    def __sub_util(self, inputs, method: str = "cn2an", sub_mode: str = "number") -> str:
        try:
            if inputs:
                if method == "cn2an":
                    inputs = inputs.replace("廿", "二十").replace("半", "0.5").replace("两", "2")
                    if sub_mode == "date":
                        return re.sub(fr"(({self.smart_cn_pattern})|({self.cn_pattern}))",
                                      lambda x: str(self.cn2an(x.group(), "smart")), inputs)
                    elif sub_mode == "fraction":
                        if inputs[0] != "百":
                            frac_result = re.sub(self.cn_pattern,
                                                 lambda x: str(self.cn2an(x.group(), "smart")), inputs)
                            numerator, denominator = frac_result.split("分之")
                            return f"{denominator}/{numerator}"
                        else:
                            return inputs
                    elif sub_mode == "percent":
                        return re.sub(f"(?<=百分之){self.cn_pattern}",
                                      lambda x: str(self.cn2an(x.group(), "smart")), inputs).replace("百分之", "") + "%"
                    elif sub_mode == "celsius":
                        return re.sub(f"{self.cn_pattern}(?=摄氏度)",
                                      lambda x: str(self.cn2an(x.group(), "smart")), inputs).replace("摄氏度", "℃")
                    elif sub_mode == "number":
                        return format(self.cn2an(inputs, 'smart'), ',')
                        # return str(self.cn2an(inputs, "smart"))
                    else:
                        raise Exception(f"error sub_mode: {sub_mode} !")
                else:
                    if sub_mode == "date":
                        inputs = re.sub(r"\d+(?=年)",
                                        lambda x: self.an2cn(x.group(), "direct"), inputs)
                        return re.sub(r"\d+",
                                      lambda x: self.an2cn(x.group(), "lower"), inputs)
                    elif sub_mode == "fraction":
                        frac_result = re.sub(r"\d+", lambda x: self.an2cn(x.group(), "lower"), inputs)
                        numerator, denominator = frac_result.split("/")
                        return f"{denominator}分之{numerator}"
                    elif sub_mode == "celsius":
                        return self.an2cn(inputs[:-1], "lower") + "摄氏度"
                    elif sub_mode == "percent":
                        return "百分之" + self.an2cn(inputs[:-1], "lower")
                    elif sub_mode == "number":
                        return self.an2cn(inputs, "lower")
                    else:
                        raise Exception(f"error sub_mode: {sub_mode} !")
        except Exception as e:
            print(f"WARN: {e}")
            return inputs


if __name__ == '__main__':
    tans = Translate()
    print(tans.convert("这人坏滴很，王尼玛一五一十的收入为一万元, 而两人却告诉我是二千元", "cn2an"))
    # print(tans.convert("这人坏滴很，王尼玛一五一十的收入为10000元, 而二六二百却告诉我是2000元", "an2cn"))
