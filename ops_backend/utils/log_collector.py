
import subprocess

def get_recent_logs(lines: int = 50):
    """
    获取系统日志，调用 journalctl 读取最近 n 行
    """
    try:
        logs = subprocess.check_output(
            ["journalctl", "-n", str(lines), "--no-pager"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        return logs.splitlines()
    except Exception as e:
        return [f"读取日志失败: {e}"]

