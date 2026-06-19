# elegant / SDDS 速查表

## elegant 输入文件骨架

```elegant
&run_setup
    lattice       = "lattice.lte",   ! lattice 文件
    use_beamline  = "RING",          ! beamline 名称
    p_central     = 3000.0,           ! MeV/c
    default_order = 2,                ! 线性/二阶；含六极 DA 常用 3
    rootname      = "demo",          ! 输出文件前缀
&end

&run_control
    n_steps = 1,                      ! 扫描或多步跟踪的步数
&end

&twiss_output
    filename = %s.twi,                ! %s 会替换为 rootname
    matched  = 1,                     ! 环用 1；传输线常用 0
&end

&track &end
```

## 常用 lattice 元素

| 元素 | 用途 | 关键字段 |
|---|---|---|
| `DRIF` | 漂移段 | `L` |
| `QUAD` | 四极磁铁 | `L`, `K1` |
| `SEXT` | 六极磁铁 | `L`, `K2` |
| `SBEN/CSBEN` | 偏转磁铁 | `L`, `ANGLE`, `E1`, `E2` |
| `RFCA` | RF 腔 | `VOLT`, `FREQUENCY`, `PHASE` |
| `MONI` | BPM/观测点 | 通常无长度 |
| `HKICK/VKICK` | 校正子 | `KICK` |
| `MARK` | 标记点 | 用于输出、匹配、切片定位 |

## 常用 elegant 命令

| 命令 | 典型用途 |
|---|---|
| `&twiss_output` | beta、alpha、色散、tune、辐射积分 |
| `&bunched_beam` | 生成宏粒子束团 |
| `&sdds_beam` | 从 SDDS 粒子文件读入束团 |
| `&vary_element` | 扫描或优化元素参数 |
| `&optimization_setup` | 设置优化算法与目标 |
| `&error_element` / `&error_control` | 对准、场误差、随机种子 |
| `&correct` | 闭轨校正，常配 BPM 和校正子 |
| `&chromaticity` | 色品计算与修正 |
| `&dynamic_aperture` | 横向动力学孔径扫描 |
| `&momentum_aperture` | 动量孔径扫描 |
| `&insert_elements` | 在 lattice 中批量插入元素 |

## SDDS 命令行最常用组合

```bash
sddsquery file.twi                         # 看列名、参数名、页结构
sddsprintout -col=s -col=betax file.twi    # 快速打印列
sdds2stream file.twi -col=s -col=betax     # 只输出数值，适合脚本
sddsplot -col=s,betax file.twi             # 画 beta_x
sddsprocess in.twi out.twi -define=col,... # 派生新列/统计
sddscombine run*.twi all.twi -merge        # 合并多次运行
```

## 排错关键词

- `unknown namelist`：命令名拼写或 elegant 版本不支持。
- `unknown element`：`.lte` 中元素名和 `use_beamline`/命令引用不一致。
- `unstable`：线性 optics 不稳定；先减小四极强度或检查弯铁角度。
- 输出为空：确认 `rootname`、当前目录、`filename=%s.xxx`、运行是否报错。
