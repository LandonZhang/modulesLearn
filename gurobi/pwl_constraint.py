import gurobipy as gp
from gurobipy import GRB


def run_pwl_optimization():
    """
    演示 Gurobi 分段线性约束 (Piecewise-Linear Constraints) 的用法

    数学模型:
    Max y
    s.t.
      0 <= x <= 5
      y = f(x), 其中 f(x) 是分段线性函数，由点 (0, 1), (2, 5), (5, 2) 定义

    函数形状:
      - 区间 [0, 2]: 从 (0, 1) 上升到 (2, 5) -> 斜率 = 2
      - 区间 [2, 5]: 从 (2, 5) 下降到 (5, 2) -> 斜率 = -1
    """
    print("=== Gurobi 分段线性约束演示 (addGenConstrPWL) ===")

    # 1. 创建模型
    model = gp.Model("pwl_demo")

    # 2. 定义变量
    x = model.addVar(lb=0.0, ub=5.0, vtype=GRB.CONTINUOUS, name="x")
    y = model.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y")

    # 3. 设置目标函数：最大化 y
    model.setObjective(y, GRB.MAXIMIZE)

    # 4. 添加分段线性约束
    # 定义关键点 (x, y)
    x_pts = [0.0, 2.0, 5.0]
    y_pts = [1.0, 5.0, 2.0]

    # model.addGenConstrPWL(xvar, yvar, xpts, ypts, name)
    # 含义: y = pwl(x)，其中 pwl 函数由 (x_pts, y_pts) 线性插值定义
    model.addGenConstrPWL(x, y, x_pts, y_pts, name="pwl_constraint")

    # --- 场景 1: 寻找全局最大值 ---
    print("\n--- 场景 1: 寻找函数最大值 ---")
    model.params.OutputFlag = 0
    model.update()
    model.write("./pwl.lp")
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}")
        model.write("./gurobi/pwl_solution.sol")
        print("分析: 求解器正确找到了分段函数的峰值点 (2, 5)。")

    # --- 场景 2: 验证中间点的插值 ---
    print("\n--- 场景 2: 验证插值 (强制 x=1) ---")
    # 在区间 [0, 2] 内，函数是从 (0, 1) 到 (2, 5) 的直线
    # 当 x=1 时，y 应该是 (1+5)/2 = 3

    # 固定 x = 1
    x.LB = 1.0
    x.UB = 1.0

    model.params.OutputFlag = 0
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f"目标函数值: {model.objVal}")
        print(f"变量值: x={x.x}, y={y.x}")
        print("分析: 当 x=1 时，y 自动计算为 3.0，验证了线性插值逻辑。")


if __name__ == "__main__":
    try:
        run_pwl_optimization()
    except gp.GurobiError as e:
        print(f"Gurobi 错误代码 {e.errno}: {e}")
    except AttributeError:
        print("遇到属性错误。请确保安装了 gurobipy 并且拥有有效的许可证。")
