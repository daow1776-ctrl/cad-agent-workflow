# 三维建模和装配

## SolidCraft

SolidCraft 自带几何引擎和 MCP，可做二维草图、三维特征、零件和装配。SC 保存建模历史和参数，STEP 保存交换用实体，STL 是网格。建模时把需要日后改动的尺寸设为驱动参数，至少改一次并复测依赖特征。有些按坐标创建的轮廓点要从尺寸规格重建，交付时按实测结果说明可改范围。

- 优先用已经暴露的 SolidCraft MCP 工具，把任务文件放在当前服务已允许的范围内。便携版可用 solidcraft-cli.exe mcp --headless --allow-path 任务目录 启动本地 JSON-RPC 会话。将权限限制在该次任务所需目录。需要复用操作时，也可把原生命令写成 JSON，使用 CLI 的 run 命令。 [MCP 文档](https://github.com/tangency-labs/solidcraft/blob/v0.30.1/docs/mcp.md)
- 依次核对单位、零件尺寸、孔径和坐标、实体闭合。装配件再核对放置关系和必要的干涉。导出的 STEP 可回读并复测包络、实体数或关键尺寸。STL 检查网格及比例。
- 二维工程图按当前任务的目标软件和图样要求制作。已验证路径是共用规格分别生成 SC 和 DXF，再由 AutoCAD 出 DWG/PDF。 [SolidCraft 格式文档](https://docs.solidcraft.io/guide/files.html)

### 本地 MCP 辅助脚本

当前会话没有已注册的 MCP 时，[scripts/solidcraft-mcp.cjs](../scripts/solidcraft-mcp.cjs) 可用 Node.js 执行明确列出的 MCP 调用，使用当前任务目录作为文件范围。输入 JSON 为对象数组，每项写 tool 和 arguments。涉及文件时使用任务目录内的绝对路径。

~~~json
[
  {
    "tool": "batch",
    "arguments": {
      "commands": [
        {"command": "sketch.create", "params": {"plane": "XY"}},
        {"command": "sketch.rectangle.two_point", "params": {"p0": [0, 0], "p1": [20, 15]}},
        {"command": "sketch.finish", "params": {}},
        {"command": "solid.extrude", "params": {"distance": 8}}
      ]
    }
  },
  {"tool": "measure", "arguments": {"summary": true}}
]
~~~

~~~powershell
Get-Content -LiteralPath $mcpScript -Raw | node - $solidcraftCli $cadJob $planPath
~~~

每次运行开启新的临时设计会话。需要后续编辑或查看时，在计划中保存 SC，下一次运行先打开。工具报错后脚本停止。保存或导出之后的步骤失败时，检查任务目录中已生成的文件及实际模型状态。

## SOLIDWORKS

客户指定 SLDPRT、SLDASM、SLDDRW 时，先确认目标版本及对可编辑特征、配合、图纸模板的要求。机器安装或 COM 已注册，只是启动验证的起点。可用本机 SOLIDWORKS 和授权会话建立独立试件，执行所需的建模或导入、重建、保存和重开。STEP 导入后按实际几何和特征树交付，指定原生特征树时在目标软件建立对应特征。工程图应在目标应用检查视图及模型引用。
