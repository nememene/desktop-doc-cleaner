import os
import shutil
import datetime
import ctypes
from pathlib import Path

EXTENSIONS = {
    '.xls', '.pptx', '.xlsx', '.xlsm', '.pdf', '.ppt', '.txt',
    '.word', '.eml', '.jpg', '.jpeg', '.bmp', '.doc', '.docx',
}


def get_desktop():
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
        )
        value, _ = winreg.QueryValueEx(key, 'Desktop')
        winreg.CloseKey(key)
        expanded = os.path.expandvars(value)
        if os.path.isdir(expanded):
            return expanded
    except OSError:
        pass

    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if os.path.isdir(desktop):
        return desktop

    return desktop


def get_target_dir():
    now = datetime.datetime.now()
    month_folder = f'{now.month}月文档'
    target = Path(f'E:\\Document\\IPF\\{now.year}\\{month_folder}')
    return target, month_folder


def move_files(desktop, target_dir):
    moved = 0
    errors = []

    for file in Path(desktop).iterdir():
        if not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS:
            continue

        dest = target_dir / file.name
        counter = 1
        while dest.exists():
            dest = target_dir / f'{file.stem}_{counter}{file.suffix}'
            counter += 1

        try:
            shutil.move(str(file), str(dest))
            moved += 1
        except OSError as exc:
            errors.append(f'{file.name}: {exc}')

    return moved, errors


def shortcut_points_to(shortcut_path, target_dir):
    try:
        import win32com.client

        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(str(shortcut_path))
        return Path(shortcut.TargetPath).resolve() == target_dir.resolve()
    except Exception:
        return False


def shortcut_already_exists(desktop, target_dir):
    for item in Path(desktop).glob('*.lnk'):
        if shortcut_points_to(item, target_dir):
            return True
    return False


def create_folder_shortcut(target_dir, month_folder, desktop):
    if shortcut_already_exists(desktop, target_dir):
        return False

    import win32com.client

    shortcut_path = os.path.join(desktop, f'{month_folder}.lnk')
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = str(target_dir)
    shortcut.WorkingDirectory = str(target_dir)
    shortcut.Description = f'文档归档文件夹 - {month_folder}'
    shortcut.Save()
    return True


def show_message(moved, target_dir, shortcut_created, errors):
    if shortcut_created:
        shortcut_text = '已创建'
    else:
        shortcut_text = '已存在，未重复创建'

    lines = [
        '桌面文档清理完成',
        '',
        f'目标文件夹: {target_dir}',
        f'已移动文件: {moved} 个',
        f'快捷方式: {shortcut_text}',
    ]

    if errors:
        lines.append('')
        lines.append('以下文件移动失败:')
        lines.extend(f'  - {err}' for err in errors)

    ctypes.windll.user32.MessageBoxW(
        0,
        '\n'.join(lines),
        '桌面文档清理',
        0x40,
    )


def show_error(message):
    ctypes.windll.user32.MessageBoxW(
        0,
        message,
        '桌面文档清理 - 错误',
        0x10,
    )


def main():
    if not Path('E:\\').exists():
        show_error('E: 盘不存在，无法创建目标文件夹 E:\\Document\\IPF')
        return

    desktop = get_desktop()
    target_dir, month_folder = get_target_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    moved, errors = move_files(desktop, target_dir)
    shortcut_created = create_folder_shortcut(target_dir, month_folder, desktop)
    show_message(moved, target_dir, shortcut_created, errors)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        show_error(str(exc))
