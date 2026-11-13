# 安装与恢复

## 安装技能

将仓库的 `skills/cad-agent-workflow` 整个文件夹复制到宿主支持的用户技能目录。在支持用户级 `.agents/skills` 的环境中，目标是 `<用户目录>/.agents/skills/cad-agent-workflow`。也可通过宿主的 GitHub 技能安装器，选择本仓库及 `skills/cad-agent-workflow` 路径。

安装后刷新技能列表或新开会话，用 `$cad-agent-workflow` 显式调用。已有同名技能时先比较和备份，再更新。只下载仓库不代表自动安装了技能或 CAD 软件。

## 按交付准备依赖

1. **二维修订和复核**：安装 [CAD Operations](https://github.com/XiaoGuai23/cad-operations-skill)，保留完整运行时、知识库和模板。参考版本是 `e6b1a5f`；后续版本按其 README 配置。它是独立的上游依赖，本仓库没有复制完整运行时。
2. **AutoCAD 原生文件**：确认 AutoCAD 授权及 Core Console 可用，把实际路径传给转换脚本。随附脚本仅支持毫米模型空间的 DXF，PDF 可选，窗口是 A4 横向 `(0,0)` 到 `(297,210)`，按 1:1 输出。其他图幅、单位和布局另行设置。
3. **SolidCraft 三维建模**：从 [官方发布页](https://github.com/tangency-labs/solidcraft/releases) 获取适用平台的版本。辅助脚本参考 [v0.30.1](https://github.com/tangency-labs/solidcraft/releases/tag/v0.30.1)。优先通过宿主连接 MCP；也可用 Node.js 运行本技能的 `solidcraft-mcp.cjs`，启动 `solidcraft-cli mcp --headless --allow-path <任务目录>`。调用前读取实际工具目录，遵循已装版本的参数契约。
4. **SOLIDWORKS 原生格式**：确认安装、授权、版本和原生接口可用。本技能提供流程指导，未包含覆盖所有零件、装配与工程图的通用生成器。

CAD Operations 参考安装命令。先把变量设置为实际路径，使用独立虚拟环境：

```powershell
# $cadOpsPath 为完整上游源码目录，$cadVenv 为尚未存在的虚拟环境目录
py -3.12 -m venv $cadVenv
$cadPython = Join-Path $cadVenv 'Scripts\python.exe'
& $cadPython -m pip install -r (Join-Path $cadOpsPath 'requirements.txt') -e (Join-Path $cadOpsPath 'runtime\cad-2d-skill')
& $cadPython -X utf8 -m cad_skill_core operations --json
```

先检查版本、路径和所需接口，再用小型独立试件验证目标格式的保存、重开和尺寸。只做二维图时无需安装所有三维软件。

## 个人要求独立保存

输出位置、显示语言、作者名和本机软件路径放在技能文件夹之外。分享技能时只分享通用文件夹；用户自行决定是否另外提供个人配置。技能本体不依赖某一份私人配置。
