"""
BionicMemory 安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bionicmemory",
    version="2.0.0",
    author="BionicMemory Team",
    author_email="gzdmcaoyc@163.com",
    description="基于仿生学原理的AI记忆管理系统",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/caoyc/BionicMemory",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "bionicmemory=scripts.start_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "bionicmemory": ["data/*", "docs/*"],
    },
    keywords="ai memory system bionic chromadb vector database",
    project_urls={
        "Bug Reports": "https://github.com/caoyc/BionicMemory/issues",
        "Source": "https://github.com/caoyc/BionicMemory",
        "Documentation": "https://github.com/caoyc/BionicMemory/docs",
    },
)
