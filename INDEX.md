# Elegant_Learning 文件索引

所有文件列表及用途说明。

## tutorial/basic/ (10 个教程)
| 编号 | 文件 | 主题 |
|------|------|------|
| 01 | `01_hello_elegant.ele` + `.lte` | 第一个 FODO 仿真 |
| 02 | `02_element_types.ele` + `.lte` | 所有常用元素 (DRIF, QUAD, BEND, SEXT, RF...) |
| 03 | `03_lattice_commands.ele` + `.lte` | Lattice 高级语法 (RPN, LINE, REPEAT) |
| 04 | `04_bunch_generation.ele` + `.lte` | 束团生成 (sigma_matrix, bunched_beam, sdds_beam) |
| 05 | `05_twiss_and_optics.ele` + `.lte` | 光学计算 (Twiss, 辐射积分, 耦合) |
| 06 | `06_energy_scan.ele` + `.lte` | 参数扫描 (vary_element) |
| 07 | `07_run_control_and_files.ele` + `.lte` | 运行控制、%s 命名、多阶段仿真 |
| 08 | `08_sdds_postprocessing.sh` | SDDS 工具包后处理 (shell) |
| 09 | `09_python_postprocessing.py` | Python 后处理与绘图 |
| 10 | `10_csr_drift_benchmark.ele` + `.lte` | CSR 漂移基准测试 |

## tutorial/intermediate/ (5 个教程)
| 编号 | 文件 | 主题 |
|------|------|------|
| 01 | `01_closed_orbit_and_correction.ele` + `.lte` | 闭轨计算与 SVD 校正 |
| 02 | `02_chromaticity_correction.ele` + `.lte` | 色品计算与六极校正 |
| 03 | `03_optimization.ele` + `.lte` | 参数优化 (simplex/powell) |
| 04 | `04_rf_acceleration.ele` + `.lte` | RF 加速与纵向动力学 |
| 05 | `05_injection_and_extraction.ele` + `.lte` | 注入与引出仿真 |

## tutorial/advanced/ (5 个教程)
| 编号 | 文件 | 主题 |
|------|------|------|
| 01 | `01_error_tolerance_analysis.ele` + `.lte` | 误差与容差分析 (对准 + 场质量) |
| 02 | `02_wakefield_impedance.ele` + `.lte` | 尾场与阻抗 (纵向 ZLONGIT + 横向 TRWAKE) |
| 03 | `03_dynamic_aperture.ele` + `.lte` | 动力学孔径 (DA 扫描) |
| 04 | `04_momentum_aperture.ele` + `.lte` | 动量孔径 + 频率图 (FMA) |
| 05 | `05_parallel_pelegant.sh` | 并行 Pelegant (MPI/GPU 使用指南) |

## examples/ (4 个工具)
| 文件 | 用途 |
|------|------|
| `batch_runner.sh` | 批量仿真框架 (参数扫描, MC, 并行) |
| `plot_optics.py` | 通用光学图绘制脚本 |
| `template_ring.ele` | 储存环仿真模板 (可复用) |
| `sdds_utils.py` | SDDS Python 工具集 |

## projects/ (2 个项目)
| 目录 | 主题 |
|------|------|
| `fodo_line_full/` | FODO 传输线完整仿真 (lattice + optics + tracking) |
| `storage_ring_design/` | 3 GeV 储存环从光学到 DA 的全流程设计 |
