#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhuofalin
@contact:1822643111@qq.com
@version: 1.0.0
@license: Apache Licence
@file: an2cn.py
@time: 2022/5/9 16:09
"""

from typing import Union
from proces import preprocess
from base import ConvertBase
import utils


class ArabicNumerals2CN(ConvertBase):
    """
    Convert Arabic numerals to Chinese numerals
    Same as function name
    """

    def __init__(self, simple: bool = True) -> None:
        """
        Initialize class properties or attributes
        :param simple: Whether it is in concise form, bool, default: True
        """
        super(ArabicNumerals2CN, self).__init__()
        self.conf = utils.get_default_config()
        self.base_number = '0123456789'
        self.number_low = self.conf['number_lower_an2cn']
        self.number_up = self.conf['number_upper_an2cn']
        self.mode_list = ['lower', 'upper', 'rmb', 'direct']
        self.simple = simple

    def convert(self,
                need_convert: Union[str, int, float] = None,
                mode: str = 'lower') -> str:
        """
        Convert the field to be converted to a standard format
        Achievable functions:
         1. Convert Arabic numerals to Chinese uppercase | lowercase | rmb | direct format,
            and the number level (unit) can reach 10,000 more;
         2. Arabic numerals can receive integers or data with decimal points;
         3. Please enter the upper | lower  | rmb | direct case identification by yourself.

        :param need_convert:  Number to be converted , Arabic numerals
        :param mode: lower | upper | rmb | direct, str
        :return: Chinese uppercase, str

        >>>   input  mode     output
               '1005' lower  一千零五
                1005  upper  壹仟零伍
                1005  rmb    壹仟零伍元整
                1005  direct 一零零五

        >>>    '.5' lower  零点五
                .5  upper  零点伍
                .5  rmb    伍角
                .5  direct 零点五
        """
        if need_convert is not None and need_convert != '':
            # Step 1: Verify the correctness of the mode parameter
            if mode not in self.mode_list:
                raise ValueError(f'The mode parameter only supports {str(self.mode_list)} !')

            # Step 2: Convert the number to a string, where Python will automatically do the conversion
            # eg: 1. -> 1.0 1.00 -> 1.0 -0 -> 0
            if not isinstance(need_convert, str):
                need_convert = str(need_convert).strip()
                need_convert = self.__number_to_string(need_convert)

            # Step 3: Data preprocessing:
            # <1>. Traditional Chinese to Simplified
            # <2>. Full-width to half-width
            need_convert = preprocess(need_convert, pipelines=[
                'traditional_to_simplified',
                'full_angle_to_half_angle'
            ])

            if isinstance(need_convert, str):
                need_convert = need_convert.replace(',', '').replace('，', '')

            # Step 4: Check if the data is valid
            self.__check_need_convert_is_valid(need_convert)

            # Step 5: Judging Positive and Negative
            if need_convert[0] == '-' or need_convert == '负':
                sign = '负'
                need_convert = need_convert[1:]
            else:
                sign = ''

            # Step 6: start --> just do it
            if mode == 'direct':
                output = self.__direct_convert(need_convert)
            else:
                # Considering that in some cases, the number xx (not others) starting with . will appear.
                # At this time, it is necessary to add 0 at the beginning to form the format of 0.xx
                if need_convert.startswith('.') and need_convert[1:].isdigit():
                    need_convert = f'0{need_convert}'
                # Split integer and fractional parts
                split_result = need_convert.split('.')
                len_split_result = len(split_result)
                if len_split_result == 1:
                    # input without decimals
                    integer_data = split_result[0]
                    if mode == 'rmb':
                        output = self.__integer_convert(integer_data, 'upper') + '元整'
                    else:
                        output = self.__integer_convert(integer_data, mode)
                elif len_split_result == 2:
                    # input with decimals
                    integer_data, decimal_data = split_result
                    if mode == "rmb":
                        int_data = self.__integer_convert(integer_data, 'upper')
                        dec_data = self.__decimal_convert(decimal_data, 'upper')
                        len_dec_data = len(dec_data)

                        if len_dec_data == 0:
                            output = int_data + '元整'
                        elif len_dec_data == 1:
                            raise ValueError(f'Abnormal output：{dec_data}')
                        elif len_dec_data == 2:
                            if dec_data[1] != '零':
                                if int_data == '零':
                                    output = dec_data[1] + '角'
                                else:
                                    output = int_data + '元' + dec_data[1] + '角'
                            else:
                                output = int_data + '元整'
                        else:
                            if dec_data[1] != '零':
                                if dec_data[2] != '零':
                                    if int_data == '零':
                                        output = dec_data[1] + '角' + dec_data[2] + '分'
                                    else:
                                        output = int_data + '元' + dec_data[1] + '角' + dec_data[2] + '分'
                                else:
                                    if int_data == '零':
                                        output = dec_data[1] + '角'
                                    else:
                                        output = int_data + '元' + dec_data[1] + '角'
                            else:
                                if dec_data[2] != '零':
                                    if int_data == '零':
                                        output = dec_data[2] + '分'
                                    else:
                                        output = int_data + '元' + '零' + dec_data[2] + '分'
                                else:
                                    output = int_data + '元整'
                    else:
                        output = self.__integer_convert(integer_data, mode) + \
                                 self.__decimal_convert(decimal_data, mode)
                else:
                    raise ValueError(f'Input format error：{need_convert}！')
        else:
            raise ValueError('Input data is empty！')

        return sign + output

    def __direct_convert(self, need_convert: str) -> str:
        _output = ""
        for d in need_convert:
            if d == '.':
                _output += '点'
            else:
                _output += self.number_low[int(d)]
        return _output

    @staticmethod
    def __number_to_string(number_data: Union[int, float]) -> str:
        # Decimal handling
        # python will automatically convert 0.00005 to 5e-05, so str(0.00005) != "0.00005"
        string_data = str(number_data)
        if "e" in string_data:
            string_data_list = string_data.split('e')
            string_key = string_data_list[0]
            string_value = string_data_list[1]
            if string_value[0] == '-':
                string_data = '0.' + '0' * (int(string_value[1:]) - 1) + string_key
            else:
                string_data = string_key + '0' * int(string_value)
        return string_data

    def __check_need_convert_is_valid(self, check_data: str) -> None:
        # Check if the input data is in the specified dictionary
        all_check_keys = self.base_number + '.-'
        for data in check_data:
            if data not in all_check_keys:
                raise ValueError(f'The data entered is not included in the conversion scope: {data}！')

    def __integer_convert(self, integer_data: str, mode: str) -> str:
        numeral_list = self.conf[f'number_{mode}_an2cn']
        unit_list = self.conf[f'unit_{mode}_order_an2cn']

        # Remove the leading 0
        # eg: 007 => 7
        integer_data = str(int(integer_data))

        len_integer_data = len(integer_data)
        if len_integer_data > len(unit_list):
            raise ValueError(f'Out of data range, the longest supported {len(unit_list)} ')

        output_an = ""
        for i, d in enumerate(integer_data):
            if int(d):
                output_an += numeral_list[int(d)] + unit_list[len_integer_data - i - 1]
            else:
                if not (len_integer_data - i - 1) % 4:
                    output_an += numeral_list[int(d)] + unit_list[len_integer_data - i - 1]

                if i > 0 and not output_an[-1] == '零':
                    output_an += numeral_list[int(d)]

        output_an = output_an.replace('零零', "零"'').replace('零万', '万').replace('零亿', '亿').replace('亿万', '亿') \
            .strip('零')

        # Solve 「一十X」 problems
        if output_an[:2] in ['一十']:
            if self.simple:
                output_an = output_an[1:]

        # decimal between 0 - 1
        if not output_an:
            output_an = '零'

        return output_an

    def __decimal_convert(self, decimal_data: str, o_mode: str) -> str:
        len_decimal_data = len(decimal_data)

        if len_decimal_data > 16:
            print(f'Note: The length of the fractional part is {len_decimal_data},'
                  f'and the first 16 digits of effective precision will be automatically truncated!')
            decimal_data = decimal_data[:16]

        if len_decimal_data:
            output_an = '点'
        else:
            output_an = ''
        numeral_list = self.conf[f'number_{o_mode}_an2cn']

        for data in decimal_data:
            output_an += numeral_list[int(data)]
        return output_an


if __name__ == '__main__':
    # import yaml
    # config_file = 'F:/document_standardization/cnoan/config.yaml'
    # with open(config_file, encoding='utf-8') as f:
    #     y = yaml.load(f, Loader=yaml.FullLoader)
    an2cn_obj = ArabicNumerals2CN(simple=True)
    print(an2cn_obj.convert('1,0000', mode='lower'))
    # print(an2cn_obj.convert(1000, mode='upper'))
    # print(an2cn_obj.convert(1000, mode='rmb'))
    # print(an2cn_obj.convert(10000, mode='direct'))
