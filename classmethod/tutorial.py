from typing import Dict, Optional, Self, Union


class Car:
    # 设定一个类属性，并非实例属性
    car_number: int = 0

    def __init__(self, name: str, top_speed: int) -> None:
        self.name = name
        self.top_speed = top_speed
        # 每新建一个汽车，汽车总数就加1
        Car.car_number += 1

    def __str__(self) -> str:
        return f"{self.name} ({self.top_speed}km/h)"

    @classmethod
    def car_count(cls):
        return f"We now have {cls.car_number} cars."

    # 实现一个类方法，用户只需要输入车名，速度查数据库得到，返回实例化对象
    @classmethod
    def init_instance(cls, name: str) -> Self:
        database: Dict[str, int] = {"bmw": 120, "tesla": 130, "xiaomi": 150}
        top_speed: Optional[int] = database.get(name.lower())
        if top_speed:
            print(f"We have got {name}'s top speed")
        else:
            print(f"We can't get {name}'s top speed. Set it to default")
            top_speed = 100

        # 返回实例化对象
        return cls(name, top_speed)


# 实现对汽车总数的统计
tesla = Car("Tesla", 130)
print(Car.car_number)
bmw = Car("BMW", 120)
print(Car.car_number)
# 调用类方法实例化已有汽车
xiaomi = Car.init_instance("Xiaomi")
print(xiaomi)
print(Car.car_count())
# 调用类方法实例化没有汽车
huawei = Car.init_instance("Huawei")
print(huawei)
print(Car.car_count())
