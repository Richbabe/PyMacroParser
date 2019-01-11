# coding=utf-8
import string

# 保存当前是否带有'/*'
HAS_COMMENT_BEGIN = False

# 保存可用宏指令
MACRO_INSTRUCTIONS = ['#ifdef', '#ifndef', '#else', '#endif', '#define', '#undef']

# 保存cpp的布尔类型
CPP_BOOL = ['true', 'false']

# 保存字符串中未转义字符对应的转义字符的map
ENCODE_MAP = {'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', 'v': '\v', "'": "\'",
              '"': '\"', '\\': '\\', '?': '\?'}

# 保存字符中未转义字符对应的转义字符的map
ENCODE_CHAR_MAP = {'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', 'v': '\v', "'": "\'",
                   '"': '\"', '\\': '\\', '?': '\?', '0': '\0'}

# 保存转义字符对应的未转义字符的map
DECODE_MAP = {'\a': '\\a', '\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\v': '\\v', "\'": "\\'",
              '\"': '\\"', '\\': '\\\\', '\?': '\\?'}

# ****************************定义区分Cpp整形和浮点型的有限状态机类相关****************************
# 能输入的ascii码个数
ASCII_COUNT = 128

# 定义有限状态机不合法的状态为-1
INVALID_STATE = -1

# 定义有限状态机初始状态为0
INIT_STATE = 0

# 浮点型状态机中浮点数状态
FLOAT_STATE = [2, 4, 6, 7, 8]

# 整形状态机中10进制整形状态
DECIMAL_STATE = [1, 4, 5, 6, 9]

# 整形状态机中8进制整形状态
OCTAL_STATE = [2, 10, 11, 12, 15]

# 整形状态机中16进制整形状态
HEXADECIMAL_STATE = [3, 16, 17, 18, 21]


# 词法分析器
class FSM:
    def __init__(self):
        """
            函数名：__init__
            功能：状态机的构造函数
            参数：无
            返回值：无
        """
        self.state_count = 0  # FSM状态数
        self.fsm_table = [[INVALID_STATE for i in xrange(ASCII_COUNT)] for i in xrange(self.state_count)]  # FSM的状态表
        self.cur_state = INIT_STATE  # 初始状态为0

    # ****************************浮点型部分有限状态机相关****************************
    def init_for_decimal_number(self, begin, end):
        """
            函数名：init_for_decimal_number
            功能：初始化FSM状态表当前状态begin时输入10进制数字（[0-9]）到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        for i in xrange(10):
            self.fsm_table[begin][ord('0') + i] = end

    def init_for_first_decimal_number(self, begin, end):
        """
            函数名：init_for_first_decimal_number
            功能：初始化FSM状态表当前状态begin时输入非首位的10进制数字（[1-9]）到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        for i in xrange(1, 10):
            self.fsm_table[begin][ord('0') + i] = end

    def init_for_octal_number(self, begin, end):
        """
            函数名：init_for_octal_number
            功能：初始化FSM状态表当前状态begin时输入8进制数字（[0-7]）到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        for i in xrange(0, 8):
            self.fsm_table[begin][ord('0') + i] = end

    def init_for_hexadecimal_number(self, begin, end):
        """
            函数名：init_for_hexadecimal_number
            功能：初始化FSM状态表当前状态begin时输入16进制数字（[0-9],[a-f],[A-f]）到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        for i in xrange(10):
            self.fsm_table[begin][ord('0') + i] = end

        for i in xrange(ord('a'), ord('f') + 1):
            self.fsm_table[begin][i] = end

        for i in xrange(ord('A'), ord('F') + 1):
            self.fsm_table[begin][i] = end

    def get_next_state(self, cur_state, c):
        """
            函数名：get_next_state
            功能：当当前状态cur_state输入字符c时返回状态机的下一个状态
            参数：当前状态cur_state,输入的字符c
            返回值：状态机的下一个状态
        """
        # 不合法的情况
        if cur_state == INVALID_STATE or ord(c) >= ASCII_COUNT:
            return INVALID_STATE

        return self.fsm_table[cur_state][ord(c)]

    def init_for_sign(self, begin, end):
        """
            函数名：init_for_sign
            功能：初始化FSM状态表当前状态begin时输入符号位(+,-)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('-')] = end
        self.fsm_table[begin][ord('+')] = end

    def init_for_float_suffix(self, begin, end):
        """
            函数名：init_for_float_suffix
            功能：初始化FSM状态表当前状态begin时输入浮点型后缀(l,L,f,F)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('l')] = end
        self.fsm_table[begin][ord('L')] = end
        self.fsm_table[begin][ord('f')] = end
        self.fsm_table[begin][ord('F')] = end

    def init_for_float_e(self, begin, end):
        """
            函数名：init_for_float_e
            功能：初始化FSM状态表当前状态begin时输入浮点型指数标志(e,E)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('e')] = end
        self.fsm_table[begin][ord('E')] = end

    def init_float_fsm(self):
        """
            函数名：init_float_fsm
            功能：初始化识别浮点型的状态机
            参数：无
            返回值：无
        """
        self.state_count = 8  # 浮点型FSM状态数
        self.fsm_table = [[INVALID_STATE for i in xrange(ASCII_COUNT)] for i in xrange(self.state_count)]  # FSM的状态表
        self.cur_state = INIT_STATE  # 初始状态为0

        # 建立浮点型状态机的状态表
        self.init_for_decimal_number(0, 1)
        self.init_for_decimal_number(1, 1)
        self.init_for_decimal_number(2, 2)
        self.init_for_decimal_number(3, 2)
        self.init_for_decimal_number(4, 4)
        self.init_for_decimal_number(5, 4)

        self.init_for_sign(0, 0)
        self.fsm_table[0][ord('.')] = 3

        self.fsm_table[1][ord('.')] = 2
        self.fsm_table[1][ord('f')] = 7
        self.fsm_table[1][ord('F')] = 7
        self.init_for_float_e(1, 5)

        self.init_for_float_e(2, 5)
        self.init_for_float_suffix(2, 6)

        self.init_for_float_suffix(4, 8)

        self.init_for_sign(5, 5)

    def value_is_float(self, value):
        """
            函数名：value_is_float
            功能：判断value是否为浮点型
            参数：字符串value
            返回值：bool值，True为浮点型，False为不是浮点型
        """
        self.init_float_fsm()

        for c in value:
            self.cur_state = self.get_next_state(self.cur_state, c)

        if self.cur_state in FLOAT_STATE:
            return True
        else:
            return False

    # ****************************整型部分有限状态机相关****************************
    def init_for_int_u(self, begin, end):
        """
            函数名：init_for_int_u
            功能：初始化FSM状态表当前状态begin时输入整形后缀(u,U)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('u')] = end
        self.fsm_table[begin][ord('U')] = end

    def init_for_int_l(self, begin, end):
        """
            函数名：init_for_int_l
            功能：初始化FSM状态表当前状态begin时输入整形后缀(l,L)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('l')] = end
        self.fsm_table[begin][ord('L')] = end

    def init_for_int_i(self, begin, end):
        """
            函数名：init_for_int_i
            功能：初始化FSM状态表当前状态begin时输入整形后缀(i,I)到达的目标状态end
            参数：当前状态begin,目标状态end
            返回值：无
        """
        self.fsm_table[begin][ord('i')] = end
        self.fsm_table[begin][ord('I')] = end

    def init_int_fsm(self):
        """
            函数名：init_int_fsm
            功能：初始化识别整型的状态机
            参数：无
            返回值：无
        """
        self.state_count = 21  # 整形FSM状态数
        self.fsm_table = [[INVALID_STATE for i in xrange(ASCII_COUNT)] for i in xrange(self.state_count)]  # 整形FSM状态表
        self.cur_state = INIT_STATE  # 初始状态为0

        # 建立整型状态机的状态表
        self.init_for_first_decimal_number(0, 1)
        self.init_for_decimal_number(1, 1)
        self.init_for_octal_number(2, 2)
        self.init_for_hexadecimal_number(3, 3)

        self.init_for_sign(0, 0)
        self.fsm_table[0][ord('0')] = 2
        self.fsm_table[2][ord('x')] = 3
        self.fsm_table[2][ord('X')] = 3

        self.init_for_int_u(1, 4)
        self.init_for_int_l(1, 5)
        self.init_for_int_i(1, 7)

        self.init_for_int_l(4, 5)
        self.init_for_int_i(4, 7)
        self.init_for_int_l(5, 6)
        self.fsm_table[7][ord('6')] = 8
        self.fsm_table[8][ord('4')] = 9

        self.init_for_int_u(2, 10)
        self.init_for_int_l(2, 11)
        self.init_for_int_i(2, 13)

        self.init_for_int_l(10, 11)
        self.init_for_int_i(10, 13)
        self.init_for_int_l(11, 12)
        self.fsm_table[13][ord('6')] = 14
        self.fsm_table[14][ord('4')] = 15

        self.init_for_int_u(3, 16)
        self.init_for_int_l(3, 17)
        self.init_for_int_i(3, 19)

        self.init_for_int_l(16, 17)
        self.init_for_int_i(16, 19)
        self.init_for_int_l(17, 18)
        self.fsm_table[19][ord('6')] = 20
        self.fsm_table[20][ord('4')] = 21

    def value_is_int(self, value):
        """
            函数名：value_is_int
            功能：判断value是否为整型
            参数：字符串value
            返回值：int值，如果是10进制返回10，8进制返回8，16进制返回16，非整数返回-1
        """
        self.init_int_fsm()

        for c in value:
            self.cur_state = self.get_next_state(self.cur_state, c)

        if self.cur_state in DECIMAL_STATE:
            return 10
        elif self.cur_state in OCTAL_STATE:
            return 8
        elif self.cur_state in HEXADECIMAL_STATE:
            return 16
        else:
            return -1


# 定义解析错误异常
class ParseError(Exception):
    def __init__(self, message):
        """
            函数名：__init__
            功能：自定义异常ParseError的构造函数
            参数：string类型的错误信息message
            返回值：无
        """
        self.error_message = message


# ****************************定义Python预处理器类相关****************************
class PyMacroParser:
    def __init__(self):
        """
            函数名：__init__
            功能：Python预处理器类的构造函数
            参数：无
            返回值：无
        """
        self.pre_define_macro = []  # 保存预定义宏
        self.code_lines = []  # 保存宏代码段

    # ****************************字符串处理相关****************************
    def sign_in_string(self, line, index):
        """
            函数名：sign_in_string
            功能：用于判断当前符号是否在双引号中
            参数：string类型当前行line,int类型当前符号索引index
            返回值：bool型，True为在，False为不在
        """

        # 记录引号的栈
        quotation_mark_stack = []

        for i in xrange(len(line)):
            # 如果"合法
            if line[i] == '"' and (i != 0 or self.is_transfer_char(line, index)):
                if len(quotation_mark_stack) == 0:
                    quotation_mark_stack.append('"')
                else:
                    quotation_mark_stack.pop()
            if i == index:
                return len(quotation_mark_stack) != 0

    # 用于判断当前符号是否在单引号中
    def sign_in_char(self, line, index):
        """
            函数名：sign_in_char
            功能：用于判断当前符号是否在单引号中
            参数：string类型当前行line,int类型当前符号索引index
            返回值：bool型，True为在，False为不在
        """

        # 记录引号的栈
        quotation_mark_stack = []

        for i in xrange(len(line)):
            # 如果'合法
            if line[i] == "'" and (i != 0 or self.is_transfer_char(line, index)):
                if len(quotation_mark_stack) == 0:
                    quotation_mark_stack.append("'")
                else:
                    quotation_mark_stack.pop()
            if i == index:
                return len(quotation_mark_stack) != 0

    def is_transfer_char(self, line, index):
        """
            函数名：is_transfer_char
            功能：用于判断当前符号是否是转义字符（前面得有奇数个连续的\）
            参数：string类型当前行line,int类型当前符号索引index
            返回值：bool型，True为是转义字符，False为不是转义字符
        """
        cnt = 0  # 记录当前符号前面'\\'的个数
        while index >= 1:
            if line[index - 1] == '\\':
                cnt += 1
            else:
                break
            index -= 1
        # print cnt
        return cnt % 2 == 1

    def delete_comment(self, init_lines):
        """
            函数名：delete_comment
            功能：删除注释函数
            参数：list类型的初始代码init_lines
            返回值：list类型的删除注释后的代码out_put
        """
        in_string = False  # 是否在双引号里
        in_char = False  # 是否在单引号里
        global HAS_COMMENT_BEGIN
        out_put = []
        lines = []

        for line in init_lines:
            will_delete = False  # 当前行是否删除

            res = []  # 去了注释的结果

            index = 0
            while index < len(line):
                # 判断是否进入双引号
                if line[index] == '"':
                    if (index == 0 or not self.is_transfer_char(line, index)) and not in_char:
                        if not HAS_COMMENT_BEGIN and not will_delete:
                            in_string = not in_string

                # 判断是否进入单引号
                if line[index] == "'":
                    if (index == 0 or not self.is_transfer_char(line, index)) and not in_string:
                        if not HAS_COMMENT_BEGIN and not will_delete:
                            in_char = not in_char

                elif index < len(line) - 1:
                    if not HAS_COMMENT_BEGIN and not will_delete:
                        if line[index] == "/" and line[index + 1] == "/" and not in_string:
                            will_delete = True
                            index += 2
                            continue
                        elif line[index] == "/" and line[index + 1] == "*" and not in_string:
                            HAS_COMMENT_BEGIN = True
                            will_delete = True
                            index += 2
                            continue
                    elif HAS_COMMENT_BEGIN:
                        if line[index] == "*" and line[index + 1] == "/" and not in_string:
                            if HAS_COMMENT_BEGIN:
                                HAS_COMMENT_BEGIN = False
                                will_delete = False
                                res.append(' ')
                                index += 2
                                continue
                if HAS_COMMENT_BEGIN:
                    # 如果在注释段里选择删除
                    will_delete = True
                else:
                    if line[index] == '\n' and not in_string:
                        # 如果遇到换行符（一行结束）且为单行注释，停止删除
                        will_delete = False
                if not will_delete:
                    res.append(line[index])
                index += 1
            res = ''.join(res)
            lines.append(res)

        '''    
        for line in lines:
            print line,
        '''
        # 删除换行符
        temp = []
        for line in lines:
            temp.append(line)
        temp = ''.join(temp)
        lines = temp.split("\n")
        for line in lines:
            if line.strip() != "":
                out_put.append(line.strip())
        '''
        for line in out_put:
            print(line)
        '''
        return out_put

    # ****************************处理转义相关****************************
    def encode(self, s):
        """
            函数名：encode
            功能：处理字符串中转义的转义函数（比如将'\\t'转换成'\t'）
            参数：字符串s
            返回值：转义后的字符串s
        """
        res = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                if i < len(s) - 1:
                    if s[i + 1] in ENCODE_MAP:
                        res.append(ENCODE_MAP[s[i + 1]])
                        i += 1
                    elif s[i + 1] == 'x':
                        # 如果是16进制字符,遇到第一个非16进制时停止
                        value = []
                        index = i + 1
                        while index + 1 < len(s) and s[index + 1] in string.hexdigits:
                            value.append(s[index + 1])
                            i += 1
                            index += 1
                        temp = ''.join(value)  # 16进制字符
                        print(temp)
                        char = chr(int(temp, 16))
                        res.append(char)
                    elif s[i + 1] in string.octdigits:
                        # 如果不满足8进制字符条件
                        if s[i + 1] == '0' and i + 2 < len(s) and s[i + 2] not in string.octdigits:
                            res.append(chr(int('0', 8)))
                            i += 1
                        else:
                            value = [s[i + 1]]
                            index = i + 1
                            # 8进制最多只有3位
                            for k in xrange(2):
                                if index + 1 < len(s) and s[index + 1] in string.octdigits:
                                    value.append(s[index + 1])
                                    i += 1
                                    index += 1
                            temp = ''.join(value)  # 8进制字符
                            print(temp)
                            char = chr(int(temp, 8))
                            res.append(char)
                    else:
                        res.append('\\')
            else:
                res.append(s[i])
            i += 1
        res = ''.join(res)
        # print res
        return res

    # 处理字符中转义的转义函数
    def encode_char(self, s):
        """
            函数名：encode_char
            功能：处理字符中转义的转义函数（比如将'\\t'转换成'\t'）
            参数：字符串s
            返回值：转义后的字符串s
        """
        res = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                if i < len(s) - 1:
                    if s[i + 1] in ENCODE_CHAR_MAP:
                        res.append(ENCODE_CHAR_MAP[s[i + 1]])
                        i += 1
                    else:
                        res.append('\\')
            else:
                res.append(s[i])
            i += 1
        res = ''.join(res)
        return res

    def not_in_string_encode(self, s):
        """
            函数名：encode_char
            功能：处理非字符串内的转义函数（将'\t'转换成' '，方便切割）
            参数：字符串s
            返回值：转义后的字符串s
        """
        res = []
        i = 0
        while i < len(s):
            # 非字符串且非字符
            if not self.sign_in_char(s, i) and not self.sign_in_string(s, i):
                if s[i] == '\t':
                    res.append(' ')
                else:
                    res.append(s[i])
            else:
                res.append(s[i])
            i += 1
        res = ''.join(res)
        return res

    def decode(self, s):
        """
            函数名：decode
            功能：反转义函数（比如'\t'变成'\\t'）
            参数：字符串s
            返回值：反转义后的字符串s
        """
        res = []
        i = 0

        while i < len(s):
            if s[i] in DECODE_MAP:
                res.append(DECODE_MAP[s[i]])
                i += 1
            else:
                res.append(s[i])
                i += 1
        res = ''.join(res)
        return res

    # ****************************将Cpp类型转换成Python类型相关****************************
    def is_cpp_char(self, macro_value):
        """
            函数名：is_cpp_char
            功能：检查macro_value是否是cpp的字符类型
            参数：字符串macro_value
            返回值：如果macro_value是cpp的字符类型返回True，否则返回False
        """
        if len(macro_value) >= 2:
            if macro_value[0] == "'" and macro_value[-1] == "'":
                return True
        else:
            return False

    def is_cpp_string(self, macro_value):
        """
            函数名：is_cpp_string
            功能：检查macro_value是否是cpp的字符串类型（包括宽字符串）
            参数：字符串macro_value
            返回值：如果macro_value是cpp的字符串或者宽字符串类型返回True，否则返回False
        """
        if len(macro_value) >= 2:
            if (macro_value[0] == '"' or macro_value[0] == 'L') and macro_value[-1] == '"':
                return True
        else:
            return False

    def is_cpp_aggregation(self, macro_value):
        """
            函数名：is_cpp_aggregation
            功能：检查macro_value是否是cpp的聚合类型
            参数：字符串macro_value
            返回值：如果macro_value是cpp的聚合类型返回True，否则返回False
        """
        if len(macro_value) >= 2:
            if macro_value[0] == "{":
                return True
        else:
            return False

    def cpp_bool_to_python(self, macro_value):
        """
            函数名：cpp_bool_to_python
            功能：将CPP的布尔类型转换成Python的布尔类型
            参数：字符串macro_value
            返回值：返回macro_value对应的Python布尔类型
        """
        if macro_value == "true":
            return True
        else:
            return False

    def cpp_float_to_python(self, macro_value):
        """
            函数名：cpp_float_to_python
            功能：将CPP的浮点数类型转换成Python的浮点数类型
            参数：字符串macro_value
            返回值：返回macro_value对应的Python浮点类型
        """
        # 去除后缀l、L、f、F
        value = macro_value.rstrip("lLfF")
        return float(value)

    def cpp_string_to_python(self, macro_value):
        """
            函数名：cpp_string_to_python
            功能：将CPP的字符串类型转换为Python的字符串类型
            参数：字符串macro_value
            返回值：返回macro_value对应的Python字符串类型
        """
        # 记录引号的栈
        quotation_mark_stack = []

        # 保存一行里多个字符串用于拼接
        string_list = []

        # 当前字符串
        cur_string = []

        # 拼接后的字符串
        res_string = []

        # 字符串是否宽类型l
        is_l_string = False

        index = 0

        for c in macro_value:
            if c == 'L' and len(quotation_mark_stack) == 0:
                is_l_string = True

            if c == '"':
                if len(quotation_mark_stack) == 0:
                    quotation_mark_stack.append(c)
                else:
                    if index == 0 or not self.is_transfer_char(macro_value, index):
                        quotation_mark_stack.pop()
                        cur_string = ''.join(cur_string)
                        string_list.append(cur_string)
                        cur_string = []
                    else:
                        cur_string.append(c)
            else:
                if len(quotation_mark_stack) != 0:
                    cur_string.append(c)
            index += 1

        for item in string_list:
            res_string.append(self.encode(item))
        res_string = ''.join(res_string)

        if is_l_string:
            # 如果是宽字符转换成Unicode返回
            return unicode(res_string)

        else:
            return res_string

    def cpp_char_to_python(self, macro_value):
        """
            函数名：cpp_char_to_python
            功能：将CPP的字符类型转换成Python的字符类型
            参数：字符串macro_value
            返回值：返回macro_value对应的Python字符类型
        """

        # 去掉前后单引号
        macro_value = macro_value[1:-1]

        if len(macro_value) == 1:
            return ord(macro_value)

        # 处理16进制或者8进制转义字符
        elif len(macro_value) > 2:
            if macro_value[0] == '\\' and macro_value[1] == 'x':
                # 如果是16进制字符
                macro_value = macro_value[2:]
                return int(macro_value, 16)
            elif macro_value[0] == '\\':
                # 如果是8进制字符
                macro_value = macro_value[1:]
                return int(macro_value, 8)

        # 处理普通转义字符
        else:
            value = self.encode_char(macro_value)
            return ord(value)

    def cpp_int_to_python(self, macro_value, system):
        """
            函数名：cpp_char_to_python
            功能：将CPP的整形转换成Python的整形
            参数：字符串macro_value,进制(整形)system
            返回值：返回macro_value对应的Python整形
        """

        # 去除i64/I64的后缀
        value = macro_value.replace("i64", "")
        value = value.replace("I64", "")

        # 去除uUlL的后缀
        value = value.rstrip("uUlL")

        # 转换成python的整形
        return int(value, system)

    def get_end_bracket_position(self, macro_value):
        """
            函数名：get_end_bracket_position
            功能：获得当前{对应的}的位置
            参数：字符串macro_value
            返回值：返回m当前{对应的}的位置（int类型）
        """
        stack = ['{']
        in_string = False
        in_char = False

        for index in xrange(1, len(macro_value)):
            # 判断是否进入双引号
            if macro_value[index] == '"':
                if (index == 0 or not self.is_transfer_char(macro_value, index)) and not in_char:
                    in_string = not in_string

            # 判断是否进入单引号
            elif macro_value[index] == "'":
                if (index == 0 or not self.is_transfer_char(macro_value, index)) and not in_string:
                    in_char = not in_char

            if not in_string and not in_char:
                if macro_value[index] == '{':
                    stack.append(macro_value[index])
                elif macro_value[index] == '}':
                    stack.pop()
                    if len(stack) == 0:
                        return index

        return 0

    def cpp_aggregation_to_string_list(self, macro_value):
        """
            函数名：cpp_aggregation_to_string_list
            功能：将聚合按逗号分隔成元素为字符串的list
            参数：字符串macro_value
            返回值：返回元素为字符串的list
        """
        # print(macro_value)
        # 除去首尾的大括号
        macro_value = macro_value[1:-1].strip()

        string_list = []
        cur_string = []

        in_string = False
        in_char = False

        index = 0
        while index < len(macro_value):
            c = macro_value[index]

            # 判断是否遍历结束
            if index == len(macro_value) - 1:
                if c not in "{},":
                    cur_string.append(c)
                cur_string = ''.join(cur_string).strip()
                if cur_string != "":
                    string_list.append(cur_string)
                cur_string = []

            # 判断是否进入双引号
            elif c == '"':
                if (index == 0 or not self.is_transfer_char(macro_value, index)) and not in_char:
                    in_string = not in_string
                cur_string.append(c)

            # 判断是否进入单引号
            elif c == "'":
                if (index == 0 or not self.is_transfer_char(macro_value, index)) and not in_string:
                    in_char = not in_char
                cur_string.append(c)

            # 判断是否进入{}
            elif c == '{' and not in_string and not in_char:
                end_pos = self.get_end_bracket_position(macro_value[index:])
                string_list.append(self.cpp_aggregation_to_string_list(macro_value[index:index + end_pos + 1]))
                index += end_pos

            # 判断是否遇到分隔符
            elif c == ',' and not in_char and not in_string:
                cur_string = ''.join(cur_string).strip()
                if cur_string != "":
                    string_list.append(cur_string)
                cur_string = []
            else:
                cur_string.append(c)
            index += 1

        return string_list

    def cpp_aggregation_string_list_to_python(self, string_list):
        """
            函数名：cpp_aggregation_string_list_to_python
            功能：将CPP的聚合类型转化的string_list转化成Python的tuple类型
            参数：字符串macro_value
            返回值：返回对应的Python的tuple类型
        """

        res = []  # 先保存成list，最后转换为tuple
        for item in string_list:
            if isinstance(item, list):
                res.append(self.cpp_aggregation_string_list_to_python(item))
            else:
                res.append(self.cpp_data_to_python(item))
        return tuple(res)

    def cpp_data_to_python(self, macro_value):
        """
            函数名：cpp_data_to_python
            功能：将CPP的数据类型（字符串）转化成Python数据类型
            参数：字符串macro_value
            返回值：返回对应的Python的数据类型
        """
        try:
            fsm = FSM()

            # 如果是空直接返回None
            if macro_value is None:
                return None

            # 如果是布尔类型
            elif macro_value in "'true', 'false'":
                return self.cpp_bool_to_python(macro_value)

            # 如果是字符类型
            elif self.is_cpp_char(macro_value):
                return self.cpp_char_to_python(macro_value)

            # 如果是浮点类型
            elif fsm.value_is_float(macro_value):
                return self.cpp_float_to_python(macro_value)

            # 如果是整形
            elif fsm.value_is_int(macro_value) != -1:
                return self.cpp_int_to_python(macro_value, fsm.value_is_int(macro_value))

            # 如果是字符串类型
            elif self.is_cpp_string(macro_value):
                return self.cpp_string_to_python(macro_value)

            # 如果是聚合类型
            elif self.is_cpp_aggregation(macro_value):
                string_list = self.cpp_aggregation_to_string_list(macro_value)
                return self.cpp_aggregation_string_list_to_python(string_list)

            # 输入类型错误
            else:
                raise ParseError("类型错误")

        except ParseError as e:
            print("ParseError: {}".format(e.error_message))

    # ****************************if-else逻辑匹配相关****************************
    # 找到当前代码段中匹配最外层#ifdef和#ifndef的#else的行数
    def get_else_line_index(self, code_lines):
        """
            函数名：get_else_line_index
            功能：找到#ifndef对应的#else的行数
            参数：list类型的代码段
            返回值：#ifndef对应的#else的行数（整形）
        """

        stack = []
        for index in range(len(code_lines)):
            code = code_lines[index]
            instruction = code.split(' ')[0]
            if instruction == "#ifdef" or instruction == "#ifndef":
                stack.append(instruction)
            elif instruction == "#else":
                if len(stack) == 1:
                    return index
            elif instruction == "#endif":
                stack.pop()
                if len(stack) == 0:
                    return -1  # 如果没有找到else返回-1
        return -1  # 如果没有找到else返回-1

    def get_endif_line_index(self, code_lines):
        """
            函数名：get_endif_line_index
            功能：找到#ifndef对应的#endif的行数
            参数：list类型的代码段
            返回值：#ifndef对应的#endif的行数（整形）
        """

        stack = []
        for index in xrange(len(code_lines)):
            code = code_lines[index]
            instruction = code.split(' ')[0]
            if instruction == "#ifdef" or instruction == "#ifndef":
                stack.append(instruction)
            elif instruction == "#endif":
                stack.pop()
                if len(stack) == 0:
                    return index
        return -1  # 如果没有找到endif返回-1

    # 解析宏命令并保存到字典函数
    def parse_to_dict(self, code_lines, macro_dict):
        """
            函数名：parse_to_dict
            功能：解析宏命令并保存到字典函数
            参数：list类型的代码段,所要保存的字典
            返回值：无
        """

        global MACRO_INSTRUCTIONS
        try:
            length = len(code_lines)
            index = 0
            while index < length:
                code = code_lines[index].split(' ', 2)
                instruction = code[0]

                if instruction not in MACRO_INSTRUCTIONS:
                    raise ParseError("宏指令输入错误（不在规定范围内）")

                if instruction == "#ifdef":
                    else_index = self.get_else_line_index(code_lines[index:])
                    endif_index = self.get_endif_line_index(code_lines[index:])
                    macro_name = code[1]

                    if macro_name is None:
                        raise ParseError("宏命令输入错误，格式为:#ifdef XX")

                    if macro_name in macro_dict:
                        if else_index != -1:
                            end_line = index + else_index
                        else:
                            end_line = index + endif_index
                        self.parse_to_dict(code_lines[index + 1:end_line], macro_dict)
                    elif else_index != -1:
                        self.parse_to_dict(code_lines[index + else_index + 1:index + endif_index], macro_dict)
                    index += endif_index + 1

                elif instruction == "#ifndef":
                    else_index = self.get_else_line_index(code_lines[index:])
                    endif_index = self.get_endif_line_index(code_lines[index:])
                    macro_name = code[1]

                    if macro_name is None:
                        raise ParseError("宏命令输入错误，格式为:#ifdef XX")

                    if macro_name not in macro_dict:
                        if else_index != -1:
                            end_line = index + else_index
                        else:
                            end_line = index + endif_index
                        self.parse_to_dict(code_lines[index + 1:end_line], macro_dict)
                    elif else_index != -1:
                        self.parse_to_dict(code_lines[index + else_index + 1:index + endif_index], macro_dict)
                    index += endif_index + 1

                elif instruction == "#define":
                    macro_name = code[1]

                    if macro_name is None:
                        raise ParseError("宏命令输入错误，格式为:#define XX xx")

                    if len(code) == 2:
                        macro_dict[macro_name] = None
                    elif len(code) == 3:
                        macro_value = code[2]
                        macro_dict[macro_name] = self.cpp_data_to_python(macro_value)
                    else:
                        raise ParseError("宏命令输入错误，格式为:#define XX xx")

                    index += 1

                elif instruction == "#undef":
                    macro_name = code[1]
                    if macro_name is None:
                        raise ParseError("宏命令输入错误，格式为:#undef XX xx")
                    if macro_name in macro_dict:
                        del macro_dict[macro_name]
                    index += 1

                elif instruction == "#else":
                    index += 1

                elif instruction == "#endif":
                    index += 1

                else:
                    raise ParseError("宏指令输入错误（不在规定范围内）")

        except ParseError as e:
            print("ParseError: {}".format(e.error_message))

    # ****************************预处理相关****************************
    def process_marco(self, code_lines):
        """
            函数名：process_marco
            功能：将cpp代码解析成宏命令并保存到code_lines中
            参数：list类型的代码段
            返回值：由宏命令组成的代码段
        """
        res = []

        try:
            for line in code_lines:
                # print(line)
                line = self.not_in_string_encode(line)

                temp = line.strip().split(' ', 1)

                if len(temp) > 1:
                    if temp[0] == '#':
                        temp = temp[1].strip().split(' ', 1)
                        instruction = '#' + temp[0]
                    else:
                        instruction = temp[0]
                else:
                    instruction = temp[0]

                if instruction is None:
                    raise ParseError("缺少宏指令")

                if len(temp) > 1:
                    temp2 = temp[1]
                else:
                    temp2 = None

                if temp2 is None:
                    macro_name = None
                    macro_value = None
                else:
                    # temp2 = temp2.replace("\\t", ' ')
                    temp3 = temp2.strip().split(' ', 1)
                    if temp3 is not None:
                        macro_name = temp3[0]  # 宏名
                        if len(temp3) > 1:
                            macro_value = temp3[1]  # 字段值
                        else:
                            macro_value = None  # 字段值
                    else:
                        macro_name = None
                        macro_value = None

                if instruction:
                    instruction = instruction.strip()
                if macro_name:
                    macro_name = macro_name.replace('\t', ' ').strip()
                if macro_value:
                    macro_value = macro_value.strip()
                    if macro_value.find('False') != -1:
                        raise Exception

                if macro_name and macro_value:
                    res.append(instruction + ' ' + macro_name + ' ' + macro_value)
                elif macro_name:
                    res.append(instruction + ' ' + macro_name)
                else:
                    res.append(instruction)

        except ParseError as e:
            print("ParseError: {}".format(e.error_message))

        return res

    # ****************************将Python数据类型转化成Cpp数据类型相关****************************
    def python_bool_to_cpp(self, macro_value):
        """
            函数名：python_bool_to_cpp
            功能：将Python的bool类型转换成CPP的bool类型
            参数：字符串macro_value
            返回值：macro_value对应的CPP的bool类型（保存成Python的字符串）
        """
        if macro_value:
            return "true"
        else:
            return "false"

    def python_string_to_cpp(self, macro_value):
        """
            函数名：python_string_to_cpp
            功能：将Python的string类型转换成CPP的string
            参数：字符串macro_value
            返回值：macro_value对应的CPP的string类型（保存成Python的字符串）
        """
        return '"' + self.decode(macro_value) + '"'

    def python_tuple_to_cpp(self, macro_value):
        """
            函数名：python_tuple_to_cpp
            功能：将Python的tuple类型转换成CPP的聚合
            参数：字符串macro_value
            返回值：macro_value对应的CPP的聚合类型（保存成Python的字符串）
        """
        res = ""
        if macro_value != ():
            for item in macro_value:
                res = res + self.python_data_to_cpp(item) + ','
            res = res[:-1]  # 去掉最后一个多余的逗号
        res = '{' + res + '}'
        return res

    def python_data_to_cpp(self, macro_value):
        """
            函数名：python_data_to_cpp
            功能：将Python类型转化为cpp类型（以字符串的形式）
            参数：字符串macro_value
            返回值：macro_value对应的CPP的数据类型（保存成Python的字符串）
        """
        if macro_value is None:
            return ""
        elif isinstance(macro_value, str):
            return self.python_string_to_cpp(macro_value)
        elif isinstance(macro_value, unicode):
            return 'L' + self.python_string_to_cpp(str(macro_value))
        elif isinstance(macro_value, bool):
            return self.python_bool_to_cpp(macro_value)
        elif isinstance(macro_value, tuple):
            return self.python_tuple_to_cpp(macro_value)
        else:
            return str(macro_value)

    # ****************************主函数****************************
    def load(self, f):
        """
            函数名：load
            功能：读取cpp文件函数，并把读取的代码转化成宏命令保存在self.code_lines中
            参数：文件路径（文件名）
            返回值：无
        """
        try:
            with open(f, 'r') as f:
                init_lines = f.readlines()
                macro_lines = self.delete_comment(init_lines)
                self.code_lines = self.process_marco(macro_lines)
        except IOError:
            print "Error: 没有找到文件或读取文件失败"
        else:
            print"读取文件成功！"

    def preDefine(self, s):
        """
            函数名：preDefine
            功能：预定义宏函数，将读取的预定义宏保存在self.pre_define_macro中
            参数：预定义宏字符串
            返回值：无
        """
        self.not_in_string_encode(s)

        # 清空之前保存的预定义宏
        self.pre_define_macro = []

        temp = s.strip().split(";")
        for item in temp:
            if item != "":
                self.pre_define_macro.append(item.strip())

    def dumpDict(self):
        """
            函数名：dumpDict
            功能：输出字典函数
            参数：无
            返回值：保存所有可用宏的字典
        """
        macro_dict = {}
        for macro_name in self.pre_define_macro:
            macro_dict[macro_name] = None

        self.parse_to_dict(self.code_lines, macro_dict)

        # self.process_marco(self.code_lines)

        res = {}
        for key in macro_dict:
            res[key] = macro_dict[key]

        print(res)
        return res

    def dump(self, f):
        """
            函数名：dump
            功能：输出字典到cpp文件
            参数：输出文件名
            返回值：无
        """
        macro_dict = {}
        for macro_name in self.pre_define_macro:
            macro_dict[macro_name] = None

        self.parse_to_dict(self.code_lines, macro_dict)

        try:
            with open(f, 'w') as f:
                for key in macro_dict:
                    if macro_dict[key] is not None:
                        f.write("#define {0} {1}\n".format(key, self.python_data_to_cpp(macro_dict[key])))
                    else:
                        f.write("#define {}\n".format(key))
        except IOError:
            print "Error: 写入文件失败"
        else:
            print"写入文件成功！"


if __name__ == '__main__':

    test = PyMacroParser()

    test.preDefine("")

    test.load("a.cpp")

    filename = "b.cpp"

    test.dumpDict()

    test.dump(filename)





