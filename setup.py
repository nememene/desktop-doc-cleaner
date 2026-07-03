import os
import struct
import win32com.client
from pathlib import Path


SCRIPT_DIR = Path(r"C:\Users\zheng wei\DesktopTools")
ICON_PATH = SCRIPT_DIR / "icon.ico"
BAT_PATH = SCRIPT_DIR / "run.bat"
CLEANER_PATH = SCRIPT_DIR / "cleaner.pyw"
PYTHONW = r"C:\Users\zheng wei\AppData\Local\Programs\Python\Python312\pythonw.exe"
def get_desktop():
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        )
        value, _ = winreg.QueryValueEx(key, "Desktop")
        winreg.CloseKey(key)
        expanded = os.path.expandvars(value)
        if os.path.isdir(expanded):
            return expanded
    except OSError:
        pass

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.isdir(desktop):
        return desktop

    return desktop


DESKTOP = Path(get_desktop())
SHORTCUT_NAME = "桌面文档清理"


def generate_icon():
    width, height = 32, 32

    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            cx, cy = x - width // 2, height // 2 - y
            dist = (cx * cx + cy * cy) ** 0.5

            if 6 <= y <= 9 and 5 <= x <= 14:
                r, g, b, a = 80, 140, 230, 255
            elif 9 <= y <= 27 and 3 <= x <= 28:
                r, g, b, a = 100, 160, 250, 255
            elif 9 <= y <= 27 and (x == 3 or x == 28):
                r, g, b, a = 70, 130, 220, 255
            elif (y == 9 or y == 27) and 3 <= x <= 28:
                r, g, b, a = 70, 130, 220, 255
            elif 6 <= y <= 9 and (x == 5 or x == 14):
                r, g, b, a = 60, 120, 210, 255
            elif (y == 6 or y == 9) and 5 <= x <= 14:
                r, g, b, a = 70, 130, 220, 255
            else:
                r, g, b, a = 0, 0, 0, 0

            pixels.extend([b, g, r, a])

    bmp_header = struct.pack(
        '<IiiHHIIiiII',
        40,
        width, height * 2,
        1, 32,
        0, 0, 0, 0, 0, 0
    )

    and_mask = b'\x00' * ((width + 7) // 8 * height)

    image_data = bmp_header + bytes(pixels) + and_mask
    image_size = len(image_data)

    ico_header = struct.pack('<HHH', 0, 1, 1)
    ico_dir = struct.pack(
        '<BBBBHHII',
        width if width < 256 else 0,
        height if height < 256 else 0,
        0, 0, 1, 32, image_size, 22
    )

    with open(ICON_PATH, 'wb') as f:
        f.write(ico_header)
        f.write(ico_dir)
        f.write(image_data)


def create_run_bat():
    with open(BAT_PATH, 'w', encoding='gbk') as f:
        f.write('@echo off\n')
        f.write(f'cd /d "{SCRIPT_DIR}"\n')
        f.write(f'"{PYTHONW}" cleaner.pyw\n')
        f.write('exit\n')


def create_desktop_shortcut():
    shortcut_path = DESKTOP / f"{SHORTCUT_NAME}.lnk"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.TargetPath = str(BAT_PATH)
    shortcut.WorkingDirectory = str(SCRIPT_DIR)
    shortcut.IconLocation = str(ICON_PATH) + ", 0"
    shortcut.Description = "桌面文档清理工具 - 将桌面文档归档到E:\\Document\\IPF"
    shortcut.Save()
    print(f"快捷方式已创建：{shortcut_path}")


def main():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    if not ICON_PATH.exists():
        print("正在生成图标...")
        generate_icon()
        print(f"图标已生成：{ICON_PATH}")
    else:
        print(f"图标已存在：{ICON_PATH}")

    create_run_bat()
    print(f"启动脚本已更新：{BAT_PATH}")

    create_desktop_shortcut()

    print(f"\n安装完成！请在桌面上找到「{SHORTCUT_NAME}」图标，双击即可运行。")


if __name__ == "__main__":
    main()
