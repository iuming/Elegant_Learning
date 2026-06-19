# projects/fodo_line_full/README.md
# FODO 传输线完整仿真

## 目标
从零设计一个 40 米 FODO 传输线，进行光学验证和束流跟踪。

## 文件说明

| 文件 | 功能 |
|------|------|
| `lattice_fodo.lte` | Lattice 设计文件 (8 个 FODO 单元) |
| `run_optics.ele`   | 光学计算 (Twiss, 矩阵) |
| `run_tracking.ele` | 粒子跟踪 (1000 粒子的束流演化) |

## 运行方法

```bash
# 1. 光学计算
elegant run_optics.ele

# 2. 查看结果
sdds2stream fodo_optics.twi -col=s,betax,betay | head -20

# 3. 粒子跟踪
elegant run_tracking.ele

# 4. 分析束团
python3 -c "
from sdds_utils import read_columns
bun = read_columns('fodo_track.bun', ['x', 'xp', 'y', 'yp', 'p'])
print('RMS x:', bun['x'].std() * 1e3, 'mm')
print('RMS y:', bun['y'].std() * 1e3, 'mm')
print('RMS δ:', bun['p'].std())
"
```

## 设计参数

| 参数 | 值 |
|------|-----|
| 能量 | 1 GeV/c |
| 单元长度 | 5 m |
| 总长度 | 40 m (8 单元) |
| β_max | ~10 m |
| β_min | ~3 m |
| 相移 / 单元 | ~60° |
