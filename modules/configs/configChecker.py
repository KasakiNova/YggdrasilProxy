def validate_config(config: dict) -> bool:
    # 定义配置的正确类型
    schema = {
        "General": {
            "debug": bool,
            "ip": str,
            "port": int,
            "CheckKeysTime": int
        },
        "Log": {
            "save-log": bool,
            "log_dir": str,
            "max_save_log": int
        },
        "Proxy": {
            "enable": bool,
            "address": str,
            "enable_auth": bool,
            "username": str,
            "password": str
        },
        "Server": {
            # 每个服务器条目是一个字典列表，每个字典项都应满足以下格式
            "Name": str,
            "ServerType": str,
            "NeedProxy": bool,
            "Url": str
        }
    }

    errors = []  # 用于存储类型不匹配的错误信息

    # 遍历 `General`，`Log` 和 `Proxy` 中的简单字段
    for section, fields in schema.items():
        # 如果是服务器配置，单独处理
        if section == "Server":
            continue

        if section in config:
            for field, expected_type in fields.items():
                if field in config[section]:
                    actual_value = config[section][field]
                    if not isinstance(actual_value, expected_type):
                        errors.append(
                            f"{section}.{field}: Expected {expected_type.__name__}, got {type(actual_value).__name__}"
                        )

    # 检查服务器列表类型
    for key, server_config in config.items():
        if key.startswith("Server.") and isinstance(server_config, dict):
            for field, expected_type in schema["Server"].items():
                if field in server_config:
                    actual_value = server_config[field]
                    if not isinstance(actual_value, expected_type):
                        errors.append(
                            f"{key}.{field}: Expected {expected_type.__name__}, got {type(actual_value).__name__}"
                        )

    # 输出错误信息
    if errors:
        for error in errors:
            print("Error:", error)
        return False
    else:
        return True

