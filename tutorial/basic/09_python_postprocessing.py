# tutorial/basic/09_python_postprocessing.py
# ============================================
# 使用 Python 读取/分析 SDDS 输出文件
# 推荐使用 PySDDS 或直接解析 SDDS ASCII 格式
# 运行: python3 python_postprocessing.py

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os


# ---- 方法 1: 使用 sdds2stream 转换为文本 ----
def read_sdds_with_sdds2stream(filename, columns=None):
    """使用 sdds2stream 将 SDDS 转换为表格文本"""
    if columns:
        col_str = " ".join(f"-col={c}" for c in columns)
        cmd = f"sdds2stream {filename} {col_str}"
    else:
        cmd = f"sdds2stream {filename}"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    data = []
    for line in lines[1:]:  # 跳过标题行
        if line.strip():
            data.append([float(x) for x in line.split()])
    return np.array(data)


# ---- 方法 2: 使用 SDDS Python 库 (如果已安装) ----
try:
    from SDDS import SDDS
    HAS_SDDS_PY = True
except ImportError:
    HAS_SDDS_PY = False
    print("PySDDS 未安装，使用 sdds2stream 替代")


def read_sdds(filename):
    """读取 SDDS 文件，返回数据字典"""
    if HAS_SDDS_PY:
        sdds = SDDS(0)
        sdds.Load(filename)

        data = {}
        for i in range(sdds.ColumnCount()):
            name = sdds.GetColumnName(i)
            values = []
            for page in range(sdds.PageCount()):
                row_data = sdds.GetColumnValues(page, name)
                values.extend(row_data)
            data[name] = np.array(values)
        return data
    else:
        print(f"使用 sdds2stream 读取 {filename}")
        return None


# ---- 读取 Twiss 文件并绘图 ----
def plot_twiss(twi_file):
    """从 Twiss 文件绘制光学函数"""
    if not os.path.exists(twi_file):
        print(f"文件不存在: {twi_file}")
        print("请先运行 elegant 仿真")
        return

    # 使用 sdds2stream 提取关键列
    data = read_sdds_with_sdds2stream(
        twi_file,
        columns=['s', 'betax', 'betay', 'etax', 'alphax', 'alphay']
    )

    if data is None or len(data) == 0:
        return

    s  = data[:, 0]
    bx = data[:, 1]
    by = data[:, 2]
    ex = data[:, 3]

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Beta 函数
    axes[0].plot(s, bx, 'C0', linewidth=1.5, label='βx')
    axes[0].plot(s, by, 'C3', linewidth=1.5, label='βy')
    axes[0].set_ylabel('β (m)')
    axes[0].set_title('Optical Functions from elegant Twiss Output')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 色散函数
    axes[1].plot(s, ex, 'C2', linewidth=1.5)
    axes[1].set_ylabel('ηx (m)')
    axes[1].set_title('Dispersion')
    axes[1].grid(True, alpha=0.3)

    # 相移
    from scipy.integrate import cumulative_trapezoid
    dpsi_x = np.gradient(  # 近似 dψ/ds = 1/β
        cumulative_trapezoid(1.0 / bx, s, initial=0)
        if len(s) > 1 else [0]
    )
    axes[2].plot(s, np.mod(np.cumsum(1.0 / bx) * np.mean(np.diff(s)) / (2*np.pi), 1),
                  'C0', linewidth=1.5, label='νx')
    axes[2].plot(s, np.mod(np.cumsum(1.0 / by) * np.mean(np.diff(s)) / (2*np.pi), 1),
                  'C3', linewidth=1.5, label='νy')
    axes[2].set_ylabel('Phase / 2π')
    axes[2].set_xlabel('s (m)')
    axes[2].set_title('Phase Advance')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('optics_plot.png', dpi=150)
    print("图片已保存到 optics_plot.png")
    plt.show()


# ---- 读取粒子分布并绘图 ----
def plot_bunch(bun_file):
    """绘制束团相空间分布"""
    if not os.path.exists(bun_file):
        print(f"文件不存在: {bun_file}")
        return

    data = read_sdds_with_sdds2stream(
        bun_file,
        columns=['x', 'xp', 'y', 'yp', 't', 'p']
    )

    if data is None or len(data) == 0:
        return

    x  = data[:, 0] * 1e3  # → mm
    xp = data[:, 1] * 1e3   # → mrad
    y  = data[:, 2] * 1e3
    yp = data[:, 3] * 1e3
    p  = data[:, 5]         # δ = dp/p

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # x - x'
    axes[0, 0].hist2d(x, xp, bins=50, cmap='hot')
    axes[0, 0].set_xlabel('x (mm)')
    axes[0, 0].set_ylabel("x' (mrad)")
    axes[0, 0].set_title('Horizontal Phase Space')

    # y - y'
    axes[0, 1].hist2d(y, yp, bins=50, cmap='hot')
    axes[0, 1].set_xlabel('y (mm)')
    axes[0, 1].set_ylabel("y' (mrad)")
    axes[0, 1].set_title('Vertical Phase Space')

    # x - y (实空间)
    axes[1, 0].hist2d(x, y, bins=50, cmap='hot')
    axes[1, 0].set_xlabel('x (mm)')
    axes[1, 0].set_ylabel('y (mm)')
    axes[1, 0].set_title('Transverse Cross-Section')

    # δ 分布
    axes[1, 1].hist(p, bins=50, color='steelblue', edgecolor='white')
    axes[1, 1].set_xlabel('δ')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_title('Energy Spread')

    # 计算统计量
    print(f"RMS x:  {np.std(x):.3f} mm")
    print(f"RMS x': {np.std(xp):.3f} mrad")
    print(f"RMS y:  {np.std(y):.3f} mm")
    print(f"RMS y': {np.std(yp):.3f} mrad")
    print(f"RMS δ:  {np.std(p):.5f}")

    plt.tight_layout()
    plt.savefig('bunch_phase_space.png', dpi=150)
    print("图片已保存到 bunch_phase_space.png")
    plt.show()


if __name__ == '__main__':
    # 使用示例
    plot_twiss('tutorial/basic/my_run.twi')
    plot_bunch('tutorial/basic/my_run.bun')
