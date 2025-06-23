from dataclasses import dataclass
from os import name
from turtle import st
from typing import Optional, Dict

from regex import P


# dataclass 重写了 __str__ 方法
@dataclass
class Fruit:
    name: str
    calories: int
    # 表示可选参数
    color: Optional[str] = None


banana: Fruit = Fruit("Banana", 10, "yellow")
print(banana)  # Fruit(name='Banana', color='yellow', calories=10)

# dataclass 重写了 __eq__ 方法用于比较两个数据类是否值一致
banana_1: Fruit = Fruit("Banana", 10, "green")
print(banana_1 == banana)  # True

banana_2: Fruit = Fruit("Banana", 20)
print(banana_2)


# 借助 dataclass 你甚至可以将一个数据模型改成只读的模式
# 只会冻结 dataclass 的顶层属性，不会递归冻结嵌套的可变对象
@dataclass(frozen=True)
class People:
    name: str
    grades: Dict[str, float]


# 正常打印
zzzongzii: People = People("zzzongzii", {"math": 98})
print(zzzongzii)

# 可以进行修改
zzzongzii.grades["math"] = 59
print(zzzongzii)


# 拒绝进行修改
# zzzongzii.name = "Landon"
# print(zzzongzii)


# * 实战演练，对于获取的 JSON 形式数据进行格式约束
# slots 用于降低类的内存占用与提升属性的访问速度
@dataclass(slots=True, frozen=True)
class Person:
    name: str
    age: int
    job: Optional[str] = None
    friends: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old and work as a {self.job}. His friends are: {self.friends}"


json: dict = {
    "name": "Bob",
    "age": 10,
    "job": "Salesman",
    "friends": ["Mario", "Luigi"],
}

# 使用序列解包的方式来使用数据模型规范属性值的获取
Bob: Person = Person(**json)
print(Bob.name)
