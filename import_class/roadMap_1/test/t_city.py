import os
import sys

print("__name__ =", __name__)
print("__package__ =", __package__)
print("cwd =", os.getcwd())
print("sys.path[0] =", sys.path[0])

# 绝对导入（roadMap为起点）
from utils.city_road_service import hello
# 绝对导入（import_class 为起点）
# from ..utils.city_road_service import hello
# from .t_country import main


def main() -> None:
    """示例入口：打印问候语。"""
    print(hello("示例"))


if __name__ == "__main__":
    main()
