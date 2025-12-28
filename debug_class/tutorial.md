以下是 **launch.json 主要字段及常用配置说明** 的 Markdown 格式笔记教程，适用于在 VS Code 中 Python 调试场景：

---

# launch.json 主要字段及常用配置说明（VS Code Python 调试）

## 基本结构

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      // 你的调试配置
    }
  ]
}

```

## 字段详解

| 字段名          | 含义与用途                                                                                         | 常用设置/举例                                        |
| --------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `name`        | 配置名称，显示在调试配置下拉菜单                                                                   | `"Python: 当前文件"`                               |
| `type`        | 调试器类型，Python用 `debugpy`                                                                   | `"debugpy"`                                        |
| `request`     | 启动方式，`launch`为直接启动，`attach`为附加到已有进程                                         | `"launch"`或 `"attach"`                          |
| `program`     | 指定启动的 python 脚本路径                                                                         | `"${file}"`或 `"${workspaceFolder}/main.py"`     |
| `module`      | 指定以模块方式运行（等价于 `python -m xxx`，不可与 `program`同时用）                           | `"module": "my_module.main"`                       |
| `args`        | 传递给被调试程序的命令行参数（数组，每个参数一个字符串，如果接收多个参数需要分开写，不能空格合并） | `["--port", "1593"], ["--numbers", "1", "2", "3"]` |
| `cwd`         | 当前工作目录，调试时生效                                                                           | `"${workspaceFolder}"`                             |
| `env`         | 传递给调试进程的环境变量                                                                           | `{"ENV_VAR": "value"}`                             |
| `python`      | 指定使用的 python 解释器路径                                                                       | 可省略，默认用 VS Code 检测到的解释器                |
| `console`     | 控制输出窗口类型：`integratedTerminal`(集成终端) /`externalTerminal`                           | `"console": "integratedTerminal"`（常用）          |
| `stopOnEntry` | 是否在第一行自动断点                                                                               | `true`/`false`                                   |
| `justMyCode`  | 是否仅断在用户源代码                                                                               | `true`/`false`（调库源码时可设为 false）         |
| ...             | 更多进阶参数详见官方文档                                                                           |                                                      |

以 **module** 形式运行文件能确保运行时的根目录是最外层目录，否则 python 将以脚本目录为根目录，比如以下结构：

```txt
root/
-- folder/
---- module.py
```

如果在 `root`目录下直接 run `module.py`，那么 python 将自动把根目录切换到 `folder`，导致一些 `import` 意外失效。但如果以 module 形式运行：`"module": "folder.module"`，那么将继续保持以 `root` 为项目根目录。

---

## 配置样例 1：调试当前打开的 Python 文件

```json
{
  "name": "Python: 当前文件",
  "type": "debugpy",
  "request": "launch",
  "program": "${file}",
  "console": "integratedTerminal"
}

```

## 配置样例 2：以模块方式调试

```json
{
  "name": "Python: 模块方式运行",
  "type": "debugpy",
  "request": "launch",
  "module": "my_module.main",
  "console": "integratedTerminal"
}

```

## 配置样例 3：附加到已有进程

```json
{
  "name": "Python: Attach",
  "type": "debugpy",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  },
  "console": "integratedTerminal"
}

```

---

## 常用变量

* `${workspaceFolder}`：当前工作区根目录
* `${file}`：当前打开的文件路径

---

## 进阶用法

* `envFile`：设置环境变量文件路径，如 `.env`
* `django`、`jinja`、`flask` 等特殊项目模式支持
* 配合断点条件（Hit Count/Condition）实现灵活调试

---

如需更多官方字段及高级参数详解，可参考 VS Code 官方文档配置说明。

1. [https://code.visualstudio.com/docs/python/debugging#_set-configuration-options](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options)
