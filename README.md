# 桌面文档清理工具

双击运行后，自动将桌面上指定类型的文档**剪切**到按月归档的文件夹，并在桌面创建该文件夹的快捷方式（若尚未存在）。

## 功能

- 整理扩展名：`.xls` `.pptx` `.xlsx` `.xlsm` `.pdf` `.ppt` `.txt` `.word` `.doc` `.docx` `.eml` `.jpg` `.jpeg` `.bmp`
- 目标路径：`E:\Document\IPF\{年份}\{月份}月文档`
  - 例如：`E:\Document\IPF\2026\7月文档`
- 若桌面已有指向该文件夹的快捷方式，则不会重复创建
- 运行结束后弹出对话框，显示移动结果

## 环境要求

- Windows 10 / 11
- Python 3.12+
- `pywin32`

## 安装

```powershell
pip install pywin32
python setup.py
```

运行 `setup.py` 后，桌面会出现 **「桌面文档清理」** 快捷方式，双击即可使用。

## 文件说明

| 文件 | 说明 |
|------|------|
| `cleaner.pyw` | 主程序 |
| `setup.py` | 生成图标并创建桌面快捷方式 |
| `run.bat` | 启动脚本 |
| `icon.ico` | 应用图标（由 setup.py 生成） |

## 直接运行

```powershell
pythonw cleaner.pyw
```

## 注意事项

- 请确认 `E:\` 盘存在且可写入
- 若目标文件夹中已有同名文件，会自动重命名为 `文件名_1.pdf` 等形式
