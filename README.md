# CAD Agent Workflow

给 AI Agent 使用的 Windows CAD 工作流技能。将 CAD Operations、SolidCraft MCP、AutoCAD 和 SOLIDWORKS 的适用路径组织到一个入口，完成读题、绘图、建模、复核和交付。

这是流程与辅助脚本的整合。CAD Operations 是上游技能及二维运行工具，SolidCraft 是独立三维 CAD；AutoCAD 和 SOLIDWORKS 仍需各自安装。仓库不包含这些软件本体。

## 怎么用

将 [skills/cad-agent-workflow](skills/cad-agent-workflow) 整体安装到宿主的技能目录，再提供原图、尺寸和交付格式：

> 使用 $cad-agent-workflow，按这张带尺寸的图制作零件。二维交 DWG 和 PDF，三维需要可在 SOLIDWORKS 中继续编辑的 SLDPRT；请核对关键尺寸并说明可编辑范围。

实际软件、许可、MCP 连接和文件权限仍需在本机准备，详见 [安装与恢复](skills/cad-agent-workflow/references/setup.md)。

## 包含什么

| 内容 | 作用 |
| --- | --- |
| [SKILL.md](skills/cad-agent-workflow/SKILL.md) | 按输入和交付格式选择绘图、建模与验证路径 |
| [二维制图](skills/cad-agent-workflow/references/drafting.md) | AutoCAD 原生保存/出图、CAD Operations 的 DXF 复核 |
| [三维建模](skills/cad-agent-workflow/references/modeling.md) | SolidCraft MCP、参数修改、交换格式及 SOLIDWORKS 原生路径 |
| [Windows 环境](skills/cad-agent-workflow/references/windows.md) | 工具探测、版本边界、任务目录和权限 |
| [交付流程](skills/cad-agent-workflow/references/delivery.md) | 来图需求、改版记录和文件交付 |
| [convert-sheet.py](skills/cad-agent-workflow/scripts/convert-sheet.py) | 毫米 DXF 转 DWG 2018、重开审计，可选 A4 横向 1:1 PDF |
| [solidcraft-mcp.cjs](skills/cad-agent-workflow/scripts/solidcraft-mcp.cjs) | 用 Node.js 启动任务级 SolidCraft MCP 并执行明确调用计划 |

## 工作边界

- 复杂度由输入尺寸、视图、几何、接口及目标格式决定，一个案例成功不代表所有作业都能自动完成。
- DWG/DXF、SLDPRT、SC、STEP 和 STL 的编辑能力不同。交换格式保留实体或网格，不保证原始特征树。
- 接口适合精确重复操作；检查窗口、字体或打印预览时可配合独立的 Computer Use 能力。
- 这里只保存通用技能。输出盘符、作者名、桌面目录和个人偏好由用户另行提供，个人配置不随本仓库发布。

## 上游与参考版本

- [CAD Operations](https://github.com/XiaoGuai23/cad-operations-skill)，参考 `e6b1a5f`，内置原生执行器针对 AutoCAD 2023/R24.2。
- [SolidCraft](https://github.com/tangency-labs/solidcraft)，辅助脚本参考 `0.30.1`。
- 转换脚本曾以简体中文 AutoCAD 2024 验证。SOLIDWORKS 2025 的草图、拉伸、改尺寸和 SLDPRT 重开有历史验证记录；新的版本、复杂特征、装配与工程图按任务复核。

上游及依赖遵循各自许可证。本仓库保留来源链接，不重新打包其完整代码、安装包或商业 CAD 软件。
