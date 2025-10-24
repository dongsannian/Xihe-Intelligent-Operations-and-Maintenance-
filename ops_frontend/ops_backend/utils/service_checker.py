
import subprocess

def check_service(service_name: str):
    """
    检查服务运行状态
    返回 {service, status, suggestion}
    """
    try:
        status = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True, text=True
        )
        if status.returncode == 0:
            return {"service": service_name, "status": "active"}
        else:
            return {
                "service": service_name,
                "status": "inactive",
                "suggestion": f"尝试执行: systemctl restart {service_name}"
            }
    except Exception as e:
        return {"service": service_name, "status": "unknown", "error": str(e)}

