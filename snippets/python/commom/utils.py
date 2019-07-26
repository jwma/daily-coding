class StringUtil(object):
    zh_unit = 2  # 常用中文的自定义长度单位
    other_unit = 1  # 其他字符的自定义长度单位

    @staticmethod
    def is_zh(s: str) -> bool:
        """检查传入的单个字符是不是中文（常用字符-「中日韩统一表意文字」）"""
        if len(s) != 1:
            raise Exception('传入的字符串长度必须为1')
        if not ('\u4e00' <= s <= '\u9fa5'):
            return False
        return True

    @staticmethod
    def get_zh_count(s: str) -> int:
        """获取传入字符串中常用中文字符的个数（常用字符-「中日韩统一表意文字」）"""
        count = 0
        for c in s:
            if StringUtil.is_zh(c):
                count += 1
        return count

    @classmethod
    def get_char_units(cls, s: str) -> list:
        """遍历一个字符串，获取一个单个字符与其对应的自定义长度单位的列表，[('h', 1), ('哈', 2)]"""
        units = [(c, cls.zh_unit if StringUtil.is_zh(c) else cls.other_unit) for idx, c in enumerate(s)]
        return units

    @classmethod
    def beautify(cls, input_str: str, zh_unit: int = 2, other_unit: int = 1, len_limit: int = 18,
                 suffix='') -> str:
        """美化字符串"""
        cls.zh_unit = zh_unit
        cls.other_unit = other_unit

        username_length = len(input_str)
        zh_count = StringUtil.get_zh_count(input_str)
        other_count = username_length - zh_count
        custom_unit = zh_count * cls.zh_unit + other_count * cls.other_unit
        if custom_unit > len_limit:
            units = StringUtil.get_char_units(input_str)
            result = ''
            limit_count = 0
            for unit in units:
                c, cl = unit
                if limit_count + cl > len_limit:
                    break
                limit_count += cl
                result += c
            return result + suffix
        return input_str


print(StringUtil.beautify('ha哈ha哈', len_limit=5, suffix='...'))
print(StringUtil.beautify('哈哈哈哈test哈haha哈', len_limit=10, suffix='...'))