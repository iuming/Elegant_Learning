# elegant 加速器设计工作流（从需求到可跟踪模型）

本文把一个真实加速器设计任务拆成可执行步骤。它不依赖本仓库之外的文件，适合配合 `tutorial/` 中的 `.ele/.lte` 示例逐步练习。

## 1. 从物理需求写成仿真指标

| 需求语言 | elegant/SDDS 中的可观测量 | 常用输出 |
|---|---|---|
| 束斑要小 | `betax/betay`、发射度、色散 `etax` | `&twiss_output` → `.twi` |
| 环能稳定储存 | 动量孔径、RF 桶、辐射损失 | `&rf_setup`、`&momentum_aperture` |
| 注入效率高 | 注入点 beta、相空间接受度、孔径 | `&track`、`&aperture_data` |
| 对误差不敏感 | 闭轨 RMS、校正子强度、beta beating | `&error_control`、`&correct` |
| 寿命/稳定性 | 动力学孔径、频率扩散、损失图 | `&dynamic_aperture`、turn-by-turn 数据 |

> 建议：先把每个需求写成“目标值 + 允许范围 + 检查文件”。例如：`nux=18.22±0.01`、`max(betax)<25 m`、`|x_orbit| RMS < 0.2 mm`。

## 2. 建 lattice：先线性，后非线性

1. **线性骨架**：只放 `DRIF`、`QUAD`、`SBEN/CSBEN`、`MONI`、`MARK`。
2. **闭合并匹配**：用 `&twiss_output matched=1` 检查 tune、beta、色散。
3. **加入六极**：用 `SEXT` 修正色品；此时 `default_order` 至少设为 3。
4. **加入真实效应**：RF、孔径、误差、尾场、CSR、同步辐射量子激发等。
5. **批量扫描/优化**：保存每次运行的 SDDS 输出，不要只看终端日志。

## 3. 推荐文件命名

```text
lattice_*.lte        # 元素与 beamline
run_optics.ele       # 只算 Twiss/闭轨/辐射积分
run_track.ele        # 粒子跟踪
run_errors.ele       # 误差与校正
run_scan_*.ele       # 参数扫描
analysis_*.py        # SDDS 后处理脚本
```

## 4. 最小闭环检查清单

- [ ] `.ele` 中的 `lattice` 文件存在，`use_beamline` 名称在 `.lte` 中定义。
- [ ] 传输线：`matched=0`；储存环：通常先用 `matched=1`。
- [ ] 有六极/非线性/DA：`default_order=3` 或更高。
- [ ] 输出文件使用 `%s.xxx`，避免不同 run 覆盖彼此。
- [ ] 所有扫描结果可用 `sddsquery`、`sdds2stream` 或 Python 读取。

## 5. 设计迭代节奏

```text
需求 → 线性 lattice → Twiss 检查 → 匹配/优化 → 非线性校正 →
误差与校正 → 多粒子跟踪 → SDDS 统计 → 回到需求表
```

如果某一步失败，优先退回到更简单模型。例如 DA 很差时，先关掉误差和孔径，只保留六极非线性，确认裸 lattice 是否稳定。
