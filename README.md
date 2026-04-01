# Python 俄罗斯方块

这是一个使用 Python + pygame 编写的简易俄罗斯方块小程序。

## 功能

- 经典俄罗斯方块玩法
- 分数统计
- 下一个方块预览
- 键盘控制移动、旋转和快速下落

## 运行环境

- Python 3.9 及以上
- `pygame`（已写入 `requirements.txt`）

## 安装依赖（使用本项目虚拟环境）

```bash
python3 -m venv Venv
./Venv/bin/pip install -r requirements.txt
```

## 启动游戏

```bash
./Venv/bin/python tetris.py
```

如果你在绝对路径运行，也可以使用：

```bash
"/Users/leigao/Cursor/projects/learn/预习课文件夹/新的文件夹/Venv/bin/python" "/Users/leigao/Cursor/projects/learn/预习课文件夹/新的文件夹/tetris.py"
```

## 操作说明

- `←` / `→`：左右移动
- `↑`：旋转方块
- `↓`：加速下落
- `Space`：直接落到底部
- 游戏结束后按 `ESC` 退出

## 项目文件

- `tetris.py`：游戏主程序
- `requirements.txt`：Python 依赖
- `README.md`：项目说明文档
- `Venv/`：本地虚拟环境（已在 `.gitignore` 中忽略）
# demo-repo
this is description
