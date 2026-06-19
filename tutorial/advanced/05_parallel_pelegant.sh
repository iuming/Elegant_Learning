# tutorial/advanced/05_parallel_pelegant.sh
# ============================================
# Pelegant — elegant 的 MPI 并行版本
# 适用于大量粒子 (>10k) 的跟踪仿真
# Pelegant 与 elegant 输入文件完全兼容

#!/bin/bash

# ---- Pelegant 使用说明 ----
echo "=========================================="
echo "Pelegant (Parallel elegant) 使用指南"
echo "=========================================="

# 1. 单个节点 (多核)
echo "1. 单节点运行 (4 核)"
mpirun -np 4 Pelegant input.ele

# 2. 多节点 (使用 hostfile)
echo "2. 多节点运行"
# mpirun -np 16 -hostfile hosts.txt Pelegant input.ele

# 3. 同时使用 GPU (需要 gpu-Pelegant)
echo "3. GPU 版本"
# gpu-Pelegant input.ele
# mpirun -np 4 gpu-Pelegant input.ele

# ---- 何时使用 Pelegant ----
# - 粒子数 > 10,000
# - 长时间跟踪 (>1,000 圈)
# - 需要多误差种子 Monte Carlo
# - 动力学孔径大量扫描

# ---- 性能对比 ----
echo ""
echo "性能参考 (10k 粒子, 1000 圈, FODO 环):"
echo "  elegant     1 核心:  ~30 分钟"
echo "  Pelegant    4 核心:  ~9 分钟 (3.3x 加速)"
echo "  Pelegant   16 核心:  ~3 分钟 (10x 加速)"

# ---- Pelegant 输入文件注意事项 ----
echo ""
echo "注意事项:"
echo "  - Pelegant 与 elegant 输入文件兼容"
echo "  - 输出文件名自动包含 rank 标识"
echo "  - &sdds_beam 从共用文件读取，需可并行访问"
echo "  - 使用 &subprocess 需考虑并行安全性"

# ---- 示例: 并行动力学孔径 ----
echo ""
echo "并行 DA 扫描示例:"

cat > parallel_da.ele << 'EOF'
&run_setup
    lattice       = "da_ring.lte",
    use_beamline  = "RING",
    p_central     = 3000.0,
    default_order = 3,
    rootname      = "para_da",
&end

&dynamic_aperture
    output  = %s.da,
    xmin    = -0.02,  xmax  = 0.02,   nx = 51,
    ymin    = -0.005, ymax = 0.005,  ny = 21,
    n_turns = 500,
&end

&run_control &end
&track &end
EOF

echo "运行: mpirun -np 8 Pelegant parallel_da.ele"
echo ""
echo "并行效率: 51×21×500 = 535,500 次跟踪"
echo "  串行: ~2 小时"
echo "  8 核:  ~18 分钟"
