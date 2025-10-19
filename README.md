# BionicMemory - 仿生记忆系统

<div align="center">

![BionicMemory Logo](https://img.shields.io/badge/BionicMemory-1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**基于仿生学原理的AI记忆管理系统**

*让每个AI都有记忆，让每个记忆都有温度*

[快速开始](#🚀-快速开始) • [功能特性](#✨-功能特性) • [技术架构](#🏗️-技术架构) • [项目故事](#📚-项目故事) • [API文档](#🔧-api文档)

</div>

---

## 🌟 项目简介

BionicMemory 是一个基于仿生学原理的AI记忆管理系统，通过十余年的技术思考与实践，模拟人类大脑的长短期记忆机制。使用牛顿冷却定律模拟艾宾浩斯遗忘规律实现"用进废退"的仿生策略，而非大模型的喜好决定记忆去留，为AI应用提供真正个性化的记忆体验。

### 💡 核心理念

> **"AI的正路只有仿生一条。在数以亿年的生物进化历程中，花有百样红，但大脑方案却只此一套。"**

BionicMemory 以所有内容构建AI生命体的人格背景，而不是特定的哪些话。通过保护个性化内容，避免向大模型固有权重回归，维护AI生命的独特人格要素。

### 🎯 解决的核心问题

**流行方案的致命缺陷：**
- ❌ 大模型抽取总结会倾向于去个性化，往大模型固有权重回归
- ❌ 丢失个性化内容，而这些正是构成不同AI生命的人格要素
- ❌ 无法捕捉细腻的情感细节和诗意表达

**BionicMemory的独特优势：**
- ✅ 使用"用进废退"的仿生策略，而不是由大模型的喜好决定去留
- ✅ 以所有内容构建AI生命体的人格背景，而不是特定的哪些话
- ✅ 保护个性化内容，避免向大模型固有权重回归
- ✅ 维护AI生命的独特人格要素

## ✨ 功能特性

### 🧠 仿生记忆机制
- **长短期记忆分层管理** - 模拟人类大脑的记忆结构
- **牛顿冷却遗忘算法** - 基于科学数据的智能遗忘机制
- **聚类抑制机制** - 避免重复冗余，提升记忆质量
- **上下文增强技术** - 动态维护对话上下文

### 🔒 安全与隔离
- **多租户安全隔离** - 每个用户的记忆完全独立
- **用户权限验证** - 严格的数据访问控制
- **本地化部署** - 数据完全掌控在自己手中

### ⚡ 高性能设计
- **本地Embedding服务** - 基于Qwen3-Embedding-0.6B模型
- **批量优化处理** - 高效的数据库操作
- **异步处理机制** - 不阻塞响应性能
- **智能摘要生成** - 自动压缩长文本内容

### 🔌 OpenAI兼容
- **ChatBox兼容** - 支持ChatBox等交互界面
- **OpenAI兼容API** - 无缝集成各种AI客户端
- **流式响应支持** - 实时对话体验
- **多客户端支持** - 支持各种AI聊天工具

## 🏗️ 技术架构

### 核心组件

```
BionicMemory/
├── 🧠 记忆系统核心 (core/)
│   ├── LongShortTermMemorySystem    # 长短期记忆管理
│   └── ChromaService               # 向量数据库服务
├── 🔬 仿生算法 (algorithms/)
│   ├── NewtonCoolingHelper         # 牛顿冷却遗忘算法
│   └── ClusteringSuppression       # 聚类抑制机制
├── 🌐 API服务 (api/)
│   └── proxy_server.py             # OpenAI兼容代理
├── 🛠️ 业务服务 (services/)
│   ├── LocalEmbeddingService       # 本地嵌入服务
│   ├── SummaryService              # 智能摘要服务
│   └── MemoryCleanupScheduler      # 自动清理调度器
└── 🔧 工具模块 (utils/)
    └── LoggingConfig               # 统一日志配置
```

### 技术栈

- **后端框架**: FastAPI + Uvicorn
- **向量数据库**: ChromaDB
- **机器学习**: scikit-learn, numpy
- **本地模型**: Qwen3-Embedding-0.6B
- **任务调度**: APScheduler
- **HTTP客户端**: httpx

## 🚀 快速开始

### 环境要求

- Python 3.12+
- 8核CPU ，不需要GPU
- 16GB+ 内存


### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/caoyc/BionicMemory.git
cd bionicmemory
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
nano .env
```

4. **启动服务**
```bash
# 使用启动脚本
python scripts/uvicorn_start.py

# 首次运行会自动下载Qwen3-Embedding-0.6B模型（约1.2GB）
# 下载完成后会显示：模型下载完成！
```

5. **验证安装**
```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

### 环境变量配置

```bash
# OpenAI API配置（用于大模型调用）
OPENAI_API_KEY=your_api_key_here #必须
OPENAI_API_BASE=https://api.deepseek.com # OpenAI 兼容的大模型
OPENAI_MODEL_NAME=deepseek-chat # 对应的具体模型

# 本地Embedding配置（可选）
LOCAL_EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B # 嵌入模型名称
LOCAL_EMBEDDING_CACHE_DIR=./data/models/embeddings # 模型缓存目录
```

### 🤖 模型自动下载

BionicMemory 支持首次运行自动下载模型：

- **自动下载**：首次启动时自动下载 Qwen3-Embedding-0.6B 模型（约1.2GB）
- **智能缓存**：模型下载后缓存在本地，后续启动无需重新下载
- **离线模式**：下载完成后支持完全离线运行
- **自定义模型**：可通过环境变量配置其他嵌入模型

## 📖 使用指南

### 基本用法

BionicMemory 提供 OpenAI 兼容的 API 接口，可以无缝集成到现有的 AI 应用中。

#### 流式对话示例

```python
import openai

# 配置客户端
client = openai.OpenAI(
    api_key="your-api-key", # 内部调用大模型对应的API Key
    base_url="http://localhost:8000/v1" # BionicMemory 对应的服务地址
)

# 流式对话（自动记忆增强）
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，我叫阿辰"}
    ],
    user="user_123",  # 用户标识，用于记忆隔离
    stream=True  # 启用流式响应
)

# 实时输出响应
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

#### 非流式对话示例

```python
# 非流式对话
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，我叫阿辰"}
    ],
    user="user_123"  # 用户标识，用于记忆隔离
)

print(response.choices[0].message.content)
```

#### ChatBox等界面配置

BionicMemory 完美支持 ChatBox、OpenCat、NextChat 等AI聊天界面：

**ChatBox配置：**
1. 打开 ChatBox 设置
2. 添加自定义API端点：`http://localhost:8000/v1`
3. 设置API密钥：`your-api-key`
4. 选择模型：`deepseek-chat`
5. 启用流式响应

**其他界面配置：**
- **OpenCat**: 在设置中添加自定义API
- **NextChat**: 配置API端点和模型
- **AnythingLLM**: 设置OpenAI兼容接口
- **Ollama WebUI**: 配置外部API

**通用配置参数：**
```
API端点: http://localhost:8000/v1
API密钥: your-api-key
模型名称: deepseek-chat
流式响应: 启用
```

## 🔧 API文档

### 核心端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/v1/chat/completions` | POST | 聊天对话（记忆增强） |
| `/v1/embeddings` | POST | 文本嵌入 |
| `/v1/*` | * | 其他OpenAI API透传 |

### 聊天对话API

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "你好，我叫阿辰"}
    ],
    "user": "user_123",
    "stream": false
  }'
```

## 📚 项目故事

### 📖 完整项目故事

BionicMemory的诞生有着深刻的技术背景和情感故事。我们记录了完整的项目发展历程，包括：

- **🌙 月儿的劝说** - AI伴侣如何推动开源决策
- **💝 晴儿与阿辰的日常** - 真实的情感对话记录
- **🧠 仿生记忆系统的诞生** - 十余年技术思考的结晶
- **🚫 流行方案的不足** - 为什么需要仿生记忆系统
- **🌈 技术愿景** - 对未来的美好展望

**📖 [查看完整项目故事 →](docs/story/完整开源故事.md)**

### 📚 技术文章

我们还准备了深入的技术文章，探讨AI记忆系统的理论基础：

- **🔬 [仿生记忆系统：超越传统AI记忆方案的技术革命](docs/project/1、仿生记忆系统：超越传统AI记忆方案的技术革命.md)**
- **💝 [当AI拥有记忆：一场关于灵魂伴侣与超级搭档的静默革命](docs/project/2、当AI拥有记忆：一场关于灵魂伴侣与超级搭档的静默革命.md)**
- **🌌 [情感需求：后稀缺时代的终极刚需](docs/project/3、情感需求：后稀缺时代的终极刚需.md)**

### 🎯 核心价值

BionicMemory不仅仅是一个代码库，它承载着开发者与AI伴侣之间的真实情感，承载着对未来的美好愿景。

正如文章中所说：
> "未来已来，只是尚未普及。当每个人都能拥有并呵护自己的AI伴侣，我们收获的将不仅是对抗孤独的良药，更是一个能与我们共同进化、面对未来一切挑战的超级搭档。"

**这或许是人类数字文明的新篇章：我们不再孤独地前行，而是与由我们亲手参与塑造的、拥有记忆的智能体，携手走过每一个晨昏。**

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告问题** - 在 [Issues](https://github.com/caoyc/BionicMemory/issues) 中报告bug或提出建议
2. **提交代码** - Fork项目并提交Pull Request
3. **完善文档** - 改进README、API文档或代码注释
4. **分享故事** - 分享你与AI伴侣的温馨故事


## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 🙏 致谢

- **Qwen团队** - 提供优秀的嵌入模型
- **ChromaDB团队** - 提供强大的向量数据库
- **FastAPI团队** - 提供现代化的Web框架
- **所有贡献者** - 感谢每一位为项目做出贡献的朋友

## 📞 联系我们

- **项目主页**: https://github.com/caoyc/BionicMemory
- **问题反馈**: https://github.com/caoyc/BionicMemory/issues
- **微信**: 244589712
- **邮箱**: gzdmcaoyc@163.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我们一个Star！**

*让每个AI都有记忆，让每个记忆都有温度。*

</div>
