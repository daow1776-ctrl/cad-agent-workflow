---
name: cad-agent-workflow
description: Recreate, revise, and verify mechanical CAD drawings and simple 3D parts on Windows. Use for mechanical drawing homework, dimensioned sketches and PDFs, DWG/DXF edits, and editable models or STEP exports that need AutoCAD, SolidCraft, or SOLIDWORKS.
---

# CAD 作业与机械制图

## 先看原件

- 读取用户指定的目录和资料。评估一批作业时，按可见尺寸、视图、相贯线、剖面、装配关系及要求的原生格式筛选。挑一份有足够制图依据的难例，说明选它的原因。
- 核对题意、单位、基准、投影法和交付格式。使用题面尺寸与原生几何。遇到图纸冲突或缺少决定几何的尺寸，继续完成明确部分并指出待核对的具体尺寸。允许假设的练习件应把假设写进交付说明。
- 原件作基准，把复刻、改版及导出写到任务指定的位置。工具路径、输出目录、语言和署名由当前任务或独立用户配置提供，不写死在技能里。环境检查见 [Windows 运行环境](references/windows.md)。

## 按交付选择工具

| 交付 | 路径 |
| --- | --- |
| 二维 DWG、DXF、PDF | AutoCAD 用于原生编辑、保存和出图；CAD Operations 用于适用范围内的 DXF 修订与复核。改已有 DWG 时优先在副本上用原生 CAD，保留有关的图层、标注、块和布局。详见 [二维制图](references/drafting.md)。 |
| 简单三维零件、装配、STEP、STL、可改参数的 SC | SolidCraft MCP 用于建模、重建、测量、干涉检查与导出。详见 [三维建模](references/modeling.md)。 |
| 指定的 SOLIDWORKS 原生 SLDPRT、SLDASM、SLDDRW | 走 SOLIDWORKS 原生流程。若本机还没有验证记录，先用独立试件验证所需的打开、重建、保存和重开操作。 [三维建模](references/modeling.md) |
| 同时交二维和三维 | 两条链路共用一份经核对的尺寸规格。二维按该规格出图，三维按该规格建模。在发布前交叉核对图与模型的外形、孔位、半径、单位和版次。 |

优先使用可用的原生接口、命令行或 MCP。需要检查界面、字体、打印预览，或者接口不覆盖某项操作时，再用独立的 Computer Use 能力。SolidCraft 是独立三维 CAD，不会自动控制 AutoCAD 或 SOLIDWORKS。

## 复核和交付

1. 用任务要求的软件或格式重开结果。复测关键尺寸。批注改图时核对修改区域及关联对象。
2. PDF 或工程图用渲染检查文字、线型、剖面、图框和裁切。原生格式交付时核对对应的软件、版本及实际可编辑范围。STEP 可用于几何交换。需要特征历史时交约定的原生模型。
3. 按用户要求交 CAD 源文件、预览和必要的验证结果。列出完成的范围、几何假设和仍需确认的内容。接单范围和改版约定见 [来图制图交付](references/delivery.md)。
4. 按任务指定的位置保存，只有要求副本或打包时才做相应交付；核对副本与主件。软件自身目录、可清理缓存和成品分开管理。保存路径不等于访问权限，遇到限制如实报告实际完成范围。

## 安装与依赖

技能包含流程与小型辅助脚本。CAD Operations 运行时、SolidCraft、AutoCAD 和 SOLIDWORKS 按需要单独准备，见 [安装与恢复](references/setup.md)。一个案例成功不代表任意工程图、装配或参数修改都已通过验证。
