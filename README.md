# 🚗 拼车平台 (Carpool Platform)

一个基于Flask的拼车信息分享平台，帮助用户找到同行的伙伴，让出行更便捷。

## ✨ 功能特点

- **智能搜索**: 根据目的地、出行日期和时间搜索匹配的拼车信息
- **用户管理**: 用户可以查看、编辑和删除自己发布的拼车请求
- **响应式设计**: 使用TailwindCSS构建，支持移动端和桌面端
- **本地存储**: 用户标识存储在浏览器本地，无需注册登录
- **简洁界面**: 原生HTML+CSS+JS，加载快速，操作简单

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Flask 2.3.3+

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/carpool-platform.git
   cd carpool-platform
   ```

2. **创建虚拟环境**（推荐）
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   打开浏览器访问: http://127.0.0.1:5000

## 📋 使用说明

### 搜索拼车信息

1. 在首页选择出发地和目的地
2. 选择出行日期和时间
3. 点击"查询拼车信息"按钮
4. 系统会显示匹配的拼车请求

### 发布拼车请求

1. 点击"发布拼车信息"按钮
2. 填写详细的出行信息
3. 选择联系方式类型（微信号/QQ号）
4. 填写联系信息和昵称
5. 提交发布

### 管理我的请求

1. 点击"我的拼车请求"进入管理页面
2. 查看所有自己发布的拼车信息
3. 可以编辑或删除现有请求

## 🛠️ 技术栈

- **后端**: Flask (Python)
- **数据库**: SQLite
- **前端**: 原生HTML + CSS + JavaScript
- **CSS框架**: TailwindCSS
- **图标**: 使用TailwindCSS内置样式

## 📁 项目结构

```
carpool-platform/
├── app.py                  # Flask应用主文件
├── requirements.txt        # Python依赖
├── README.md              # 项目说明
├── carpool.db             # SQLite数据库（运行时生成）
└── templates/             # HTML模板
    ├── index.html         # 主页
    ├── publish.html       # 发布页面
    └── my_requests.html   # 我的请求页面
```

## 🔧 配置说明

### 数据库模型

应用使用SQLite数据库存储拼车信息，主要字段包括：

- `id`: 主键ID
- `user_id`: 用户标识
- `departure`: 出发地
- `destination`: 目的地
- `travel_date`: 出行日期
- `travel_time`: 出行时间
- `details`: 详细信息
- `contact_type`: 联系方式类型
- `contact_info`: 联系信息
- `nickname`: 用户昵称
- `created_at`: 创建时间

### 搜索算法

搜索逻辑如下：
1. 目的地必须完全相同
2. 出行日期必须完全相同
3. 按以下优先级排序：
   - 出发地匹配优先
   - 出行时间最接近优先

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发建议

1. Fork项目到您的GitHub账户
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - 优秀的Python Web框架
- [TailwindCSS](https://tailwindcss.com/) - 实用的CSS框架

## 📞 联系方式

如果您有任何问题或建议，欢迎通过以下方式联系：

- 提交GitHub Issue
- 发送邮件至: your-email@example.com

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**