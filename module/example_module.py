class ExampleModule:
    def __init__(self, name: str) -> None:
        self.name = name

    def say_hi(self):
        print(f"Hello, I'm {self.name}")
