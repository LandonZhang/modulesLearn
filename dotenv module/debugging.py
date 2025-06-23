def func_1():
    print("The function_1 is running!")
    for i in range(10):
        print(f"This is the turn {i} for func_1")
    func_2()
    print("func_2 is finished")


def func_2():
    print("The function_2 is running!")
    for i in range(5):
        print(f"This is the turn {i} for func_2")


if __name__ == "__main__":
    print("The program is running")
    func_1()
    print("ENDING")
