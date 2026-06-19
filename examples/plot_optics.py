#!/usr/bin/env python3
# examples/plot_optics.py
# ============================================
# 通用 optics 绘图工具
# 从 elegant 输出创建高质量加速器光学图
# 用法: python3 plot_optics.py <twiss_output.twi>

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无头模式


def read_sdds_twiss(filename):
    """读取 SDDS Twiss 文件 (通过 sdds2stream)"""
    import subprocess
    
    cols = ['s', 'betax', 'betay', 'alphax', 'alphay',
            'etax', 'etaxp', 'psix', 'psiy']
    
    cmd = f"sdds2stream {filename} {' '.join('-col=' + c for c in cols)}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    lines = result.stdout.strip().split('\n')
    if len(lines) < 2:
        raise ValueError("sdds2stream 无输出")
    
    # 跳过参数行
    data_lines = [l for l in lines if not l.startswith('!') and l.strip()]
    
    data = {}
    for i, col in enumerate(cols):
        data[col] = []
    
    for line in data_lines:
        vals = line.split()
        if len(vals) >= len(cols):
            for i, col in enumerate(cols):
                data[col].append(float(vals[i]))
    
    return {k: np.array(v) for k, v in data.items()}


def plot_lattice_optics(data, output='optics.png'):
    """绘制完整的光学函数图"""
    s = data['s']
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    
    # β 函数
    ax = axes[0]
    ax.plot(s, data['betax'], 'C0', linewidth=1.5, label='βx')
    ax.plot(s, data['betay'], 'C3', linewidth=1.5, label='βy')
    ax.set_ylabel('β (m)', fontsize=12)
    ax.set_title('Lattice Optical Functions', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    # α 函数
    ax = axes[1]
    ax.plot(s, data['alphax'], 'C0', linewidth=1.5, label='αx')
    ax.plot(s, data['alphay'], 'C3', linewidth=1.5, label='αy')
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_ylabel('α')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 色散
    ax = axes[2]
    ax.plot(s, data['etax'] * 1e3, 'C2', linewidth=1.5, label='ηx')
    ax.set_ylabel('ηx (mm)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 相移
    ax = axes[3]
    # 相位每 2π 回绕
    psix = np.unwrap(data['psix']) / (2 * np.pi)
    psiy = np.unwrap(data['psiy']) / (2 * np.pi)
    ax.plot(s, psix - psix[0], 'C0', linewidth=1.5, label='νx')
    ax.plot(s, psiy - psiy[0], 'C3', linewidth=1.5, label='νy')
    ax.set_xlabel('s (m)', fontsize=12)
    ax.set_ylabel('Phase / 2π', fontsize=12)
    ax.set_title(f'Tune: νx ≈ {psix[-1]-psix[0]:.3f}, νy ≈ {psiy[-1]-psiy[0]:.3f}')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    print(f"图片已保存: {output}")
    return fig


def plot_envelope(data, output='envelope.png'):
    """绘制束流包络"""
    s = data['s']
    
    # 假设发射度和初始 Twiss 参数
    emit_x = 1.0e-9
    emit_y = 1.0e-9
    
    env_x = np.sqrt(data['betax'] * emit_x + (data['etax'] * 1e-3)**2)
    env_y = np.sqrt(data['betay'] * emit_y)
    
    fig, ax = plt.subplots(figsize=(14, 5))
    
    ax.fill_between(s, env_x * 1e3, -env_x * 1e3, alpha=0.3, color='C0',
                    label=f'σx (ε={emit_x*1e9:.1f} nm)')
    ax.fill_between(s, env_y * 1e3, -env_y * 1e3, alpha=0.3, color='C3',
                    label=f'σy (ε={emit_y*1e9:.1f} nm)')
    
    ax.set_xlabel('s (m)')
    ax.set_ylabel('Beam Size (mm)')
    ax.set_title('Beam Envelope Along Lattice')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    print(f"图片已保存: {output}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 plot_optics.py <twiss_output.twi>")
        sys.exit(1)
    
    twi_file = sys.argv[1]
    data = read_sdds_twiss(twi_file)
    
    plot_lattice_optics(data, 'lattice_optics.png')
    plot_envelope(data, 'beam_envelope.png')
