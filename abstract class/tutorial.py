from abc import ABC, abstractmethod


class Phone(ABC):
    def __init__(self, name: str, rank: int) -> None:
        self.name = name
        self.rank = rank

    @abstractmethod
    def describe(self): ...

    @abstractmethod
    def call_target(self, friend: str): ...


# 抽象类只是一个蓝图，需要被继承实现，不能直接实例化
# iPhone: Phone = Phone("iPhone", 1)
# print(iPhone) # 报错，未实现的抽象类不能实例化


class iPhone(Phone):
    def __init__(self, name: str, rank: int) -> None:
        super().__init__(name, rank)

    def describe(self):
        pass

    def call_target(self, friend: str):
        pass

    # 在实现完抽象方法之后，可以添加自己的其他方法
    @property
    def degrade(self):
        return self.rank + 1


apple: iPhone = iPhone("Apple", 1)

print(apple.name)
print(apple.degrade)
