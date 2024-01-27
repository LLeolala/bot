import sys
import os
# 获取命令行参数
# sys.argv 是一个包含脚本名称和传递给脚本的参数的列表
# 第一个元素是脚本名称，后面的元素是传递给脚本的参数
arguments = sys.argv

# 打印脚本名称
q = arguments[0]
a = os.path.basename(q)
print(a)
# 打印传递给脚本的参数
