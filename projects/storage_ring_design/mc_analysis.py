#!/usr/bin/env python3
# projects/storage_ring_design/mc_analysis.py
# ============================================
# Monte Carlo 误差分析统计
# 读取多次误差运行的结果, 输出统计分布

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from glob import glob


def read_twiss_param(filename, param):
    """从 Twiss 文件中通过 sdds2stream 读取参数"""
    result = subprocess.run(
        ['sdds2stream', filename, '-parameters', f'{param}'],
        capture_output=True, text=True
    )
    # 尝试解析数值
    for line in result.stdout.split('\n'):
        try:
            return float(line.strip())
        except ValueError:
            continue
    return None


def analyze_mc_results(mc_dir):
    """分析 MC 误差结果"""
    twi_files = sorted(glob(f"{mc_dir}/*.twi"))
    
    if not twi_files:
        print(f"没有找到 Twiss 文件: {mc_dir}")
        return
    
    tunes_x = []
    tunes_y = []
    chrom_x = []
    chrom_y = []
    emit = []
    
    for f in twi_files:
        nux = read_twiss_param(f, 'nux')
        nuy = read_twiss_param(f, 'nuy')
        if nux is not None and nuy is not None:
            tunes_x.append(nux)
            tunes_y.append(nuy)
    
    tunes_x = np.array(tunes_x)
    tunes_y = np.array(tunes_y)
    
    if len(tunes_x) == 0:
        print("无法解析 tune 数据")
        return
    
    print("=" * 60)
    print("MC 误差分析结果")
    print("=" * 60)
    print(f"运行次数: {len(tunes_x)}")
    print()
    print(f"Tune x: {np.mean(tunes_x):.4f} ± {np.std(tunes_x):.4f}")
    print(f"Tune y: {np.mean(tunes_y):.4f} ± {np.std(tunes_y):.4f}")
    print(f"Tune 散布 x: {np.std(tunes_x)*1e3:.2f}e-3")
    print(f"Tune 散布 y: {np.std(tunes_y)*1e3:.2f}e-3")
    
    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    # Tune histogram
    ax = axes[0]
    ax.hist(tunes_x, bins=20, alpha=0.6, label='νx', color='C0')
    ax.hist(tunes_y, bins=20, alpha=0.6, label='νy', color='C3')
    ax.set_xlabel('Tune')
    ax.set_ylabel('Counts')
    ax.set_title(f'Tune Distribution\nσx={np.std(tunes_x)*1e3:.1f}e-3, σy={np.std(tunes_y)*1e3:.1f}e-3')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Tune scatter
    ax = axes[1]
    ax.scatter(tunes_x, tunes_y, alpha=0.7, s=30)
    ax.set_xlabel('νx')
    ax.set_ylabel('νy')
    ax.set_title('Tune Footprint')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # 箱线图
    ax = axes[2]
    bp = ax.boxplot([tunes_x, tunes_y], labels=['νx', 'νy'],
                     patch_artist=True)
    for patch, color in zip(bp['boxes'], ['C0', 'C3']):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    ax.set_ylabel('Tune')
    ax.set_title('Tune Spread Box Plot')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('mc_tune_analysis.png', dpi=150)
    print("\n图片已保存: mc_tune_analysis.png")
    plt.show()


def plot_da_comparison(files):
    """比较多个误差种子下的 DA 变化"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    for f in files[:10]:  # 最多 10 个
        label = os.path.basename(f)[:10]
        # 读取 DA 边缘
        # (简化: 仅演示框架)
        pass
    
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_title('DA Comparison (different error seeds)')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    plt.savefig('da_comparison.png', dpi=150)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        analyze_mc_results(sys.argv[1])
    else:
        print("用法: python3 mc_analysis.py <mc_results_dir>")
        print("示例: python3 mc_analysis.py mc_results/")
