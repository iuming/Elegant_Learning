# examples/sdds_utils.py
# ============================================
# SDDS 文件处理工具集
# 封装常用的 SDDS 文件操作，方便 Python 集成

import subprocess
import numpy as np
import os
from typing import Dict, List, Optional


def sdds_info(filename: str) -> str:
    """查看 SDDS 文件头信息"""
    return subprocess.check_output(
        ['sddsquery', filename],
        text=True
    )


def read_columns(filename: str, columns: List[str]) -> Dict[str, np.ndarray]:
    """读取指定列的数据
    Args:
        filename: SDDS 文件路径
        columns: 要读取的列名列表
    Returns:
        Dict[str, np.ndarray]: 列名 → 数据
    """
    col_args = []
    for col in columns:
        col_args.extend(['-col', col])
    
    result = subprocess.run(
        ['sdds2stream', filename] + col_args,
        capture_output=True, text=True
    )
    
    lines = [l for l in result.stdout.strip().split('\n')
             if l.strip() and not l.startswith('!')]
    
    if len(lines) < 1:
        return {}
    
    # 解析数据
    n_cols = len(columns)
    data = {col: [] for col in columns}
    
    for line in lines:
        try:
            vals = [float(x) for x in line.split()]
            for i, col in enumerate(columns):
                if i < len(vals):
                    data[col].append(vals[i])
        except (ValueError, IndexError):
            continue
    
    return {k: np.array(v) for k, v in data.items()}


def extract_bpm_data(twiss_file: str) -> Dict[str, np.ndarray]:
    """从 Twiss 文件提取 BPM 位置数据"""
    # 先检查哪些是 MONI 位置
    result = subprocess.run(
        ['sddsprocess', twiss_file, '-',
         '-match=col,ElementType,MONI',
         '-print=col,ElementName,s,betax,betay,etax'],
        capture_output=True, text=True
    )
    
    # 实际上 sddsprocess 会产生新文件，这里简化为两步
    tmp_file = '/tmp/bpm_data.sdds'
    subprocess.run([
        'sddsfilter', twiss_file, tmp_file,
        '-include=col,ElementType,MONI'
    ], capture_output=True)
    
    return read_columns(tmp_file, ['s', 'betax', 'betay', 'etax'])


def combine_runs(file_pattern: str, output: str, n_runs: int):
    """合并多次 Monte Carlo 运行结果"""
    files = [file_pattern % i for i in range(1, n_runs + 1)]
    existing = [f for f in files if os.path.exists(f)]
    
    if not existing:
        print("没有找到匹配的文件")
        return
    
    cmd = ['sddscombine'] + existing + [output, '-merge']
    subprocess.run(cmd)


def filter_by_range(filename: str, col: str, vmin: float, vmax: float,
                    output: str):
    """按数值范围筛选行"""
    subprocess.run([
        'sddsfilter', filename, output,
        '-include', f'col,{col},{vmin},{vmax}'
    ])


def histogram(filename: str, col: str, bins: int = 50,
              output: Optional[str] = None) -> Dict[str, np.ndarray]:
    """利用 sddshist 创建直方图"""
    out_file = output or f'/tmp/hist_{col}.sdds'
    subprocess.run([
        'sddshist', filename, out_file,
        '-data=col,' + col,
        f'-binCount={bins}'
    ])
    return read_columns(out_file, ['Frequency', 'BinCenter'])


def compute_stats(filename: str, col: str) -> dict:
    """计算列统计量"""
    result = subprocess.run(
        ['sddsprocess', filename, '-',
         f'-define=col,{col}_sq,{col} {col} *',
         f'-process=col,{col},mean,output=/dev/stdout',
         f'-process=col,{col},sigma,output=/dev/stdout'],
        capture_output=True, text=True
    )
    
    data = read_columns(filename, [col])
    if col in data:
        arr = data[col]
        return {
            'mean': np.mean(arr),
            'std': np.std(arr),
            'min': np.min(arr),
            'max': np.max(arr),
            'rms': np.sqrt(np.mean(arr**2)),
        }
    return {}


def export_csv(filename: str, columns: List[str],
               output: str) -> str:
    """导出为 CSV 文件"""
    col_args = []
    for col in columns:
        col_args.extend(['-col', col])
    
    result = subprocess.run(
        ['sdds2stream', filename] + col_args,
        capture_output=True, text=True
    )
    
    # 转换为 CSV (空格 → 逗号)
    lines = result.stdout.strip().split('\n')
    data_lines = [l for l in lines if not l.startswith('!') and l.strip()]
    
    with open(output, 'w') as f:
        f.write(','.join(columns) + '\n')
        for line in data_lines:
            f.write(','.join(line.split()) + '\n')
    
    print(f"写出 {len(data_lines)} 行到 {output}")
    return output


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("SDDS Utils — 加速器数据分析工具")
        print()
        print("函数列表:")
        print("  read_columns(file, [col1, col2, ...])")
        print("  extract_bpm_data(twiss_file)")
        print("  combine_runs(pattern, output, n_runs)")
        print("  filter_by_range(file, col, vmin, vmax, out)")
        print("  histogram(file, col, bins)")
        print("  compute_stats(file, col)")
        print("  export_csv(file, [cols], output)")
    else:
        # 快速测试
        twi = sys.argv[1]
        info = sdds_info(twi)
        print(info)
