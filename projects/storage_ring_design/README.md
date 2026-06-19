# projects/storage_ring_design/README.md
# 储存环设计 — 从光学到动力学孔径

## 目标
完整设计一个 3 GeV 电子储存环，经过光学匹配、动力学孔径分析和误差评估。

## 设计参数

| 参数 | 目标 | 方法 |
|------|------|------|
| 能量 | 3 GeV | `p_central` |
| 周长 | 180 m | 18 单元 |
| 发射度 | ≤ 2 nm·rad | 优化工作点 |
| 自然色品 | 校正到 +1 | SF/SD 六极 |
| DA | ≥ 10 mm | 频率图验证 |
| 轨道 | RMS ≤ 50 μm | SVD 校正 |

## 文件说明

```
storage_ring_design/
├── lattice_sr.lte    ← Lattice 定义 (18 单元 Chasman-Green)
├── run_optics.ele    ← 光学计算 (Twiss, 辐射积分, 耦合)
├── run_da.ele        ← 动力学孔径 + 频率图
├── run_errors.ele    ← 误差分析 (对准 + 场质量 Monte Carlo)
├── mc_analysis.py    ← 多误差种子统计分析
└── README.md         ← 本文件
```

## 运行流程

```bash
# 1. 基本光学验证
elegant run_optics.ele

# 检查关键参数
sdds2stream sr_optics.twi -col=s,betax,betay,etax | head -20

# 2. 动力学孔径
elegant run_da.ele

# 查看 DA
sddsquery sr_da.da

# 3. 误差分析 (单次)
elegant run_errors.ele

# 4. 误差分析 (MC: 20 个种子)
bash ../../examples/batch_runner.sh mc run_errors.ele 20 mc_results/

# 5. 统计 MC 结果
python3 mc_analysis.py mc_results/
```

## Lattice 结构

```
180 m 环 = 18 单元 Chasman-Green
  每单元: QF - B(S=2面) - SD - QD - SF
  含: 1 注入单元 + 1 腔单元 + 16 标准单元
  BPM 和校正磁铁: 每单元
```
