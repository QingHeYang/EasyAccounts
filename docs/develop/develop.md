# 贡献指南

感谢你对本项目的贡献！为了帮助你更顺利地参与开发，请按照以下步骤操作。

## 开发流程

所有的开发工作都将通过`dev`分支进行，然后最终合并到`main`分支。以下是详细的开发流程：

### 1. **Fork 仓库**
   如果你还没有该项目的副本，请点击右上角的 "Fork" 按钮，创建一个属于你的仓库副本。

### 2. **克隆项目**
   将你自己的Fork仓库克隆到本地，进行开发。
```bash
git clone https://github.com/QingHeYang/EasyAccountsOpenSource.git
cd EasyAccountsOpenSource
```

### 3. 切换到 `dev` 分支
在开始任何开发工作之前，请确保你已经切换到dev分支，这个分支包含最新的开发代码。  
```bash
git checkout dev
git pull origin dev
```

### 4. 创建自己的工作分支
基于`dev`分支创建你自己的工作分支。根据你要处理的任务类型，可以选择命名为`feature/your-feature-name`（新特性）或`bugfix/your-bugfix-name`（bug修复）。  
```bash
git checkout -b feature/your-feature-name
```
或者
```bash
git checkout -b bugfix/your-bugfix-name
```

### 5. 进行开发
在你的工作分支上进行开发。完成所需功能或修复bug后，执行以下命令提交更改：  
```bash
git add .
git commit -m "简要描述你的修改"
```

### 6. 推送分支
将你的更改推送到你Fork仓库中的工作分支：
```bash
git push origin feature/your-feature-name
```
或者
```bash
git push origin bugfix/your-bugfix-name
```

### 7. 创建 Pull Request (PR)
你可以在GitHub上创建一个PR，将你的分支合并到`dev`分支。在PR的描述中，简要说明你的更改内容、修复的bug或者新增的功能。  
目前PR有两个模板，请选择对应的模板进行提交  

### 8. 代码审查与合并
我会在PR创建后进行代码审查，检查代码质量和是否符合项目规范。如果一切无误，我将会主动将PR合并到`dev`分支。  

### 9. 从 `dev` 合并到 `main`
在所有功能都已经合并并经过测试后，dev分支将被合并到main分支。此步骤将由我进行操作，确保代码的稳定性和生产环境的部署。

### 其他注意事项
- 提交信息：请使用简洁明了的提交信息，描述本次修改的目的和内容。
- 测试：请确保在提交代码之前，已经进行过适当的测试，确保不破坏已有功能。
- 代码风格：请遵循项目中的代码风格，保持一致性和可读性。
