# 二维制图

## 输入和交付

- DWG 优先读原生图元、布局和必要的外部参照。只想了解结构时用副本或只读方式。改图的基准应是用户认可的版次。
- 矢量 PDF 可作为可测参考，导入后以题面已知尺寸复核比例和精度。扫描件和照片用已给的尺寸重画。尺寸依据优先于从像素测得的估值。
- 投影按题面要求。核对三视图对应关系、可见线与虚线、中心线、剖切标记、尺寸及单位。确认 PDF 纸张和比例，打印预览优先于只检查文件大小。

## AutoCAD 2024 本机路线

有工作站 AutoCAD 时，可以用它在 DWG 副本上编辑。批量二维原生绘图可用 Core Console 执行项目生成的 SCR。已验证简中 2024 可执行 LINE、CIRCLE、SAVEAS、-PLOT，并重开检查。命令提示会随语言和版本变化。向脚本传绝对路径，对带空格的路径加引号，检查退出后的实际文件和日志。 [Autodesk 命令脚本文档](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-LT-Customization/files/GUID-95BB6824-0700-4019-9672-E6B502659E9E.htm)

[scripts/convert-sheet.py](../scripts/convert-sheet.py) 是随技能携带的窄范围工具。用于已确认毫米单位的 DXF 模型空间图，生成 DWG 2018 并回读审计。指定 --pdf 时按模型空间 (0,0) 到 (297,210) 输出 A4 横向 1:1 PDF。图框、单位、比例或布局不同的项目，按实际需求使用 AutoCAD 布局、绘图设置或另一份任务脚本。

先把变量指向当前任务的源 DXF、新的目标目录、已建立的独立配置目录及本机 Core Console。若同一隔离配置用于连续运行，使用该配置对应的标识。

~~~powershell
& $cadPython $convertScript $inputDxf $nativeJob --exe $coreConsole --profile $profile --profile-id $profileId --pdf
~~~

若 AutoCAD 在受限环境初始化配置失败，按实际权限运行。诊断时区分启动、输入识别、保存、原生重开和打印。交付前确认输出 DWG、对象计数、单位和 AUDIT 结果。

## CAD Operations 的 DXF 复核

~~~powershell
& $cadOpsPython -X utf8 -m cad_skill_core inventory $drawing --json
& $cadOpsPython -X utf8 -m cad_skill_core review $baseline $revised --box $xmin $ymin $xmax $ymax --out $reviewFolder --json
~~~

用 inventory 看几何和图元类型。用 review 对比批注区域，按报告的覆盖范围解释结果。图纸原生行为在目标 CAD 里复核。确认没有 CAD Operations 或精度需要自定义检查时，也可用现有原生检查命令或 DXF 库完成。