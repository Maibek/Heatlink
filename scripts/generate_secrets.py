#!/usr/bin/env python3
import os
from pathlib import Path

def load_env(env_path):
    """Простая загрузка .env файла (без сторонних библиотек)"""
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()
    return env_vars

def generate_secrets_h(env_vars, output_path):
    content = """// Автоматически сгенерированный файл. Не редактировать!
#ifndef SECRETS_H
#define SECRETS_H

#include <Arduino.h>

"""
    # WiFi
    content += f'const char* WIFI_SSID = "{env_vars.get("WIFI_SSID", "")}";\n'
    content += f'const char* WIFI_PASSWORD = "{env_vars.get("WIFI_PASSWORD", "")}";\n\n'
    # MQTT
    content += f'const char* MQTT_HOST = "{env_vars.get("MQTT_HOST", "")}";\n'
    content += f'int MQTT_PORT = {env_vars.get("MQTT_PORT", "1883")};\n'
    content += f'const char* MQTT_USER = "{env_vars.get("MQTT_USER", "")}";\n'
    content += f'const char* MQTT_PASSWORD = "{env_vars.get("MQTT_PASSWORD", "")}";\n\n'
    # Device ID
    content += f'const char* DEVICE_ID = "{env_vars.get("DEVICE_ID", "")}";\n\n'
    content += "#endif // SECRETS_H\n"
    
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Secrets generated: {output_path}")

if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    env_path = repo_root / ".env"
    output_path = repo_root / "firmware" / "include" / "secrets.h"
    
    if not env_path.exists():
        print("Error: .env file not found. Please create it from .env.example")
        exit(1)
    
    env_vars = load_env(env_path)
    generate_secrets_h(env_vars, output_path)