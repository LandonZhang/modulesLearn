import gurobipy as gp
from gurobipy import GRB


def run_optimization():
    """
    演示使用 Python 重载运算符 (>>) 添加指示符约束
    数学模型:
    Max x + y
    s.t.
      0 <= x, y <= 10
      flag in {0, 1}
      如果 flag = 1, 则 x + y <= 5
    """
    print("=== Gurobi 指示符约束演示 (重载运算符: >>) ===")

    # 1. 创建模型
    model = gp.Model("indicator_overloaded")

    # 2. 定义变量
    x = model.addVar(lb=0.0, ub=10.0, vtype=GRB.CONTINUOUS, name="x")
    y = model.addVar(lb=0.0, ub=10.0, vtype=GRB.CONTINUOUS, name="y")
    flag = model.addVar(vtype=GRB.BINARY, name="flag")

    # 3. 设置目标函数：最大化 x + y
    model.setObjective(x + y, GRB.MAXIMIZE)

    # 4. 添加指示符约束 (Indicator Constraint) - 使用更直观的语法
    # 语法: (BinaryVar == Value) >> (LinearConstraint)
    # 读作: "如果 BinaryVar 等于 Value，那么 LinearConstraint 必须成立"
    model.addConstr((flag == 1) >> (x + y <= 5), name="indicator_constr")

    # --- 场景 1: 让求解器自动决定 flag 的值 ---
    print("\n--- 场景 1: 自由求解 ---")
    model.Params.OutputFlag = 0
    model.update()
    model.write("./indicator_constr.lp")
    print(" 调试文件写入成功")
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}, flag={flag.x}")
        print("分析: 同理，求解器选择 flag=0 以避开约束，达到最大值 20。")

    # --- 场景 2: 强制 flag = 1 ---
    print("\n--- 场景 2: 强制 flag = 1 ---")
    flag.LB = 1

    model.Params.OutputFlag = 0
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}, flag={flag.x}")
        print("分析: 强制 flag=1，约束生效，结果限制为 5。")
        print("      注意：使用 '>>' 符号让代码的可读性大大增强。")


if __name__ == "__main__":
    try:
        run_optimization()
    except gp.GurobiError as e:
        print(f"Gurobi 错误代码 {e.errno}: {e}")
    except AttributeError:
        print("遇到属性错误。请确保安装了 gurobipy 并且拥有有效的许可证。")
