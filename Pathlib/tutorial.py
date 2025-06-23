import os
from pathlib import Path
import shutil
from tempfile import tempdir

# * 获取主文件夹路径
# 使用 os
BASE_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_FILE)

# # 使用 pathlib
BASE_FILE = Path(__file__).parent.parent
print(BASE_FILE)

# * 获取工作目录 (current working directory)
print(Path.cwd())

# * 遍历目录中的文件
file_path = Path.cwd()
for f in Path().iterdir():
    print(f)

# * 获取文件名
# 创建一个 Path 实例对象
my_txt = Path("hello.txt")
my_dir = Path("Pathlib")

print(my_dir.name)
print(my_txt.name)
# 获取文件后缀
print(my_txt.suffix)

# 不要后缀
print(my_txt.stem)

# * 连接路径, 检查文件是否存在
new_file = my_dir / "new_file.txt"
print(new_file)
print(my_txt.exists())
print(new_file.exists())

# * 处理相对路径与绝对路径
print(my_dir.parent)
print(new_file.parent)
print(my_txt.parent)

print("-" * 20)

print(my_dir.parent.absolute())
print(new_file.parent.absolute())
print(my_txt.parent.absolute())

# * resolve 方法与 absolute 方法
p = Path("..").absolute()
# 没有正确解读相对路径
print(p)  # E:\Life Style\Python学习\modules_learn\..
# 正确解读相对路径
p = Path("..").resolve()
print(p)  # E:\Life Style\Python学习

print(Path(__file__).resolve())

# * 操作主文件夹
print(Path.home())

for f in Path.home().iterdir():
    print(f)

# * 搜索文件
target_file = Path()

# 包含hello的文件
for f in target_file.glob("*hello*"):
    print(f"搜索结果是: {f}")

# 以 .txt 结尾的文件
for f in target_file.glob("*.txt"):
    print(f"搜索结果是: {f}")

# 搜索子文件夹
for f in target_file.rglob("*.txt"):
    print(f"递归搜索结果是: {f}")

# * 打开文件并操作
with my_txt.open() as f:
    print("文件内容是：\n", f.read())

# * 创建文件夹
my_dir = Path() / "Tempdir"
my_dir.mkdir(exist_ok=True)  # 存在就不创建

# * 删除“空”文件夹
my_dir.rmdir()

# * 创建多级文件夹
my_multiple_dir = Path() / "tempDir" / "subDir"
my_multiple_dir.mkdir(
    parents=True, exist_ok=True
)  # parents 参数用于控制父文件夹不在时是否创建

for f in my_dir.iterdir():
    print(f)

# * 创建文件
my_txt = my_multiple_dir / "new.txt"
my_txt.touch()

# * 删除文件
os.remove(my_txt.resolve())
print("文件删除成功")

# * 删除非空文件夹
tempdir = Path() / "tempDir"
shutil.rmtree(tempdir.resolve())
print("文件夹删除成功")

# 重命名文件
my_txt = Path() / "hello.txt"
my_txt.rename("newName.txt")
print("重命名成功")

# * 删除文件
my_txt = Path() / "newName.txt"
my_txt.touch()
my_txt.unlink()
print("删除成功")

# ! 实战：创建一个 Week 1-Week 10 的课程目录

class_dir = Path() / "dateClass"
# 创建一个课程文件夹
class_dir.mkdir(exist_ok=True)
# 创建10个文件夹
for num in range(1, 11):
    sub_dir_path = class_dir / f"Week {num:02d}"
    sub_dir_path.mkdir(exist_ok=True)
    print(f"{sub_dir_path}已经创建完成")
    txt_file = sub_dir_path / "kiss.txt"
    txt_file.touch(exist_ok=True)
    print(f"{txt_file}已经创建完成")
print("全十个文件夹以及相关文件创建完成")

# 删除文件
shutil.rmtree(class_dir.resolve())
print("实战多余文件删除完成！")
