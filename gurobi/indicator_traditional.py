import gurobipy as gp
from gurobipy import GRB


def run_optimization():
    """
    演示使用传统方法 (addGenConstrIndicator) 添加指示符约束
    数学模型:
    Max x + y
    s.t.
      0 <= x, y <= 10
      flag in {0, 1}
      如果 flag = 1, 则 x + y <= 5
    """
    print("=== Gurobi 指示符约束演示 (传统方法: addGenConstrIndicator) ===")

    # 1. 创建模型
    model = gp.Model("indicator_traditional")

    # 2. 定义变量
    # x, y 是连续变量，范围 0 到 10
    x = model.addVar(lb=0.0, ub=10.0, vtype=GRB.CONTINUOUS, name="x")
    y = model.addVar(lb=0.0, ub=10.0, vtype=GRB.CONTINUOUS, name="y")
    # flag 是二进制变量 (0 或 1)
    flag = model.addVar(vtype=GRB.BINARY, name="flag")

    # 3. 设置目标函数：最大化 x + y
    model.setObjective(x + y, GRB.MAXIMIZE)

    # 4. 添加指示符约束 (Indicator Constraint)
    # 逻辑含义: 如果 flag == 1, 则 x + y <= 5
    # 方法签名: model.addGenConstrIndicator(binvar, binval, lhs, sense, rhs, name)
    # 参数说明:
    #   binvar: 指示变量 (flag)
    #   binval: 触发值 (1) - 当 flag 取这个值时约束生效
    #   lhs: 线性约束左侧 (x + y)
    #   sense: 符号 (GRB.LESS_EQUAL)
    #   rhs: 线性约束右侧 (5.0)
    model.addGenConstrIndicator(
        flag, 1, x + y, GRB.LESS_EQUAL, 5.0, name="indicator_constr"
    )

    # --- 场景 1: 让求解器自动决定 flag 的值 ---
    print("\n--- 场景 1: 自由求解 ---")
    # 我们不限制 flag，让 Gurobi 自己选择 flag 是 0 还是 1 以获得最大目标值
    model.Params.OutputFlag = 0
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}, flag={flag.x}")
        print("分析: 因为 flag=0 时约束不生效，x+y 可以达到最大值 20 (x=10, y=10)。")
        print("      求解器为了最大化目标，智能地选择了 flag=0。")

    # --- 场景 2: 强制 flag = 1 ---
    print("\n--- 场景 2: 强制 flag = 1 ---")
    # 我们强制将 flag 设为 1，看看约束是否生效
    # 注意：修改变量边界是固定变量值的常用方法
    flag.lb = 1.0

    model.Params.OutputFlag = 0
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}, flag={flag.x}")
        print("分析: 强制 flag=1 后，指示符约束 (x+y <= 5) 被激活。")
        print("      此时最大可能的 x+y 只能是 5。")


if __name__ == "__main__":
    try:
        run_optimization()
    except gp.GurobiError as e:
        print(f"Gurobi 错误代码 {e.errno}: {e}")
    except AttributeError:
        print("遇到属性错误。请确保安装了 gurobipy 并且拥有有效的许可证。")
