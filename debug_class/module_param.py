"""
通过导入的成功与否来确定文件是否按照 python -m 的形式运行
1. python -m debug_class.module_param 可以正常执行，因为可以识别 module 模块
2. 直接 python -u .\debug_class\module_param.py 无法执行, module 模块报错
-------
在 launch.json 中配置 module 方式运行, 删除 program 字段即可成功调试
"""

from module.example_module import ExampleModule

example_module = ExampleModule("Python")

example_module.say_hi()
