#!/usr/bin/env python3
"""
使用 uvicorn 启动 BionicMemory 服务器
"""

import os
import sys
import uvicorn
import socket
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_port_available(host, port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return True

def main():
    """启动BionicMemory代理服务器"""
    print("🚀 启动 BionicMemory 仿生记忆系统...")
    print("📖 项目文档: https://github.com/caoyc/BionicMemory")
    
    # 从环境变量读取配置
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    # 检查端口是否可用
    if not check_port_available(host, port):
        print(f"❌ 端口 {port} 已被占用，请检查是否有其他服务在运行")
        print(f"💡 可以尝试修改环境变量 API_PORT 使用其他端口")
        return
    
    print(f"🔧 API文档: http://localhost:{port}/docs")
    print(f"💡 健康检查: http://localhost:{port}/health")
    print("-" * 50)
    
    try:
        # 启动服务器
        uvicorn.run(
            "bionicmemory.api.proxy_server:app",
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=False  # 生产环境建议设为False
        )
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保已安装所有依赖包: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查配置文件和依赖包")

if __name__ == "__main__":
    main()
