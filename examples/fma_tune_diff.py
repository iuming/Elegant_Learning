#!/usr/bin/env python3
"""
examples/fma_tune_diff.py
============================================
用简单 FFT 估计 turn-by-turn 数据的 tune 与频率扩散。

用途：
    python examples/fma_tune_diff.py tutorial/advanced/fma_demo.cen

说明：
- 这是教学版 FMA：用 FFT 峰值估计 tune，不是高精度 NAFF。
- 输入优先支持由 `sdds2stream file -col=Pass -col=x -col=y` 导出的文本；
  若直接给 SDDS 文件，脚本会尝试调用 `sdds2stream`。
- 中文注释保留关键步骤，便于按机器需求改造。
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np


def load_turn_by_turn(path: Path) -> np.ndarray:
    """读取 Pass/x/y 三列；必要时调用 sdds2stream 从 SDDS 转为文本。"""
    text = ""
    if path.suffix.lower() in {".txt", ".dat", ".csv"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
    elif shutil.which("sdds2stream"):
        cmd = ["sdds2stream", str(path), "-col=Pass", "-col=x", "-col=y"]
        text = subprocess.check_output(cmd, text=True)
    else:
        raise SystemExit("未找到 sdds2stream；请先把 SDDS 导出为三列文本：Pass x y")

    rows = []
    for line in text.splitlines():
        line = line.strip().replace(",", " ")
        if not line or line.startswith("!") or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            rows.append([float(parts[0]), float(parts[1]), float(parts[2])])
        except ValueError:
            continue
    if len(rows) < 16:
        raise SystemExit("有效 turn-by-turn 数据太少，至少需要 16 行。")
    return np.asarray(rows)


def estimate_tune(signal: np.ndarray) -> float:
    """用 Hann 窗 + FFT 峰值估计 0~0.5 之间的小数 tune。"""
    signal = np.asarray(signal, dtype=float)
    signal = signal - np.mean(signal)
    windowed = signal * np.hanning(signal.size)
    spectrum = np.abs(np.fft.rfft(windowed))
    freqs = np.fft.rfftfreq(signal.size, d=1.0)
    if spectrum.size <= 1:
        return float("nan")
    spectrum[0] = 0.0  # 去掉直流分量
    return float(freqs[int(np.argmax(spectrum))])


def main() -> None:
    parser = argparse.ArgumentParser(description="教学版 FMA tune 扩散估计")
    parser.add_argument("input", type=Path, help="SDDS 文件或 Pass/x/y 文本")
    args = parser.parse_args()

    data = load_turn_by_turn(args.input)
    x = data[:, 1]
    y = data[:, 2]
    mid = len(data) // 2

    qx1, qx2 = estimate_tune(x[:mid]), estimate_tune(x[mid:])
    qy1, qy2 = estimate_tune(y[:mid]), estimate_tune(y[mid:])

    print("# 教学版频率图分析结果")
    print(f"turns = {len(data)}")
    print(f"Qx(first half) = {qx1:.6f}, Qx(second half) = {qx2:.6f}, |dQx| = {abs(qx2-qx1):.3e}")
    print(f"Qy(first half) = {qy1:.6f}, Qy(second half) = {qy2:.6f}, |dQy| = {abs(qy2-qy1):.3e}")
    print("提示：真实 FMA 应对每个初始振幅粒子分别计算 tune，并绘制 tune footprint。")


if __name__ == "__main__":
    main()
