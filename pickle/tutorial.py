import pickle
from pathlib import Path


class Fruit:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color

    def __str__(self) -> str:
        return f"Fruit: {self.name}'s color is {self.color}"


if __name__ == "__main__":
    apple: Fruit = Fruit("Apple", "red")
    file_path = Path(__file__).parent / "test.pickle"

    with open(file_path, "wb") as file:
        pickle.dump(apple, file)

    print("Apple is saved!")

    with open(file_path, "rb") as file:
        new_apple: Fruit = pickle.load(file)

    print(new_apple, "is loaded")

    new_apple.color = "green"
    print(new_apple)
