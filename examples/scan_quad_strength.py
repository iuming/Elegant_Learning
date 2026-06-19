#!/usr/bin/env python3
"""
examples/scan_quad_strength.py
============================================
批量扫描四极磁铁强度并收集 Twiss 指标的模板。

这个脚本故意写得保守：
- 不修改原始 `.lte/.ele`；每个扫描点放到独立 workdir；
- 如果没有安装 elegant，会给出命令预览，便于学习流程；
- 中文注释说明每一步，方便迁移到真实 lattice。
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
from pathlib import Path


def write_case(case_dir: Path, k1: float) -> Path:
    """写出一个最小 FODO lattice 和 elegant 输入文件。"""
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "scan.lte").write_text(
        f"""! 自动生成的扫描 lattice；K1={k1:.6f}\n"
        "D:  DRIF, L=1.0\n"
        f"QF: QUAD, L=0.25, K1={k1:.8f}\n"
        f"QD: QUAD, L=0.25, K1={-k1:.8f}\n"
        "BPM: MONI\n"
        "CELL: LINE=(D,QF,D,BPM,D,QD,D,BPM)\n"
        "FODO: LINE=(6*CELL)\n"
        """,
        encoding="utf-8",
    )
    ele = case_dir / "scan.ele"
    ele.write_text(
        """! 自动生成的 elegant 扫描输入\n"
        "&run_setup\n"
        "    lattice = \"scan.lte\",\n"
        "    use_beamline = \"FODO\",\n"
        "    p_central = 1000.0,\n"
        "    default_order = 2,\n"
        "    rootname = \"scan\",\n"
        "&end\n"
        "&run_control n_steps = 1 &end\n"
        "&bunched_beam n_particles_per_bunch = 1 &end\n"
        "&twiss_output filename = %s.twi, matched = 0, output_at_each_step = 1 &end\n"
        "&track center_momentum_also = 1 &end\n"
        """,
        encoding="utf-8",
    )
    return ele


def try_extract_max_beta(case_dir: Path) -> tuple[float | None, float | None]:
    """从 scan.twi 提取 max(betax/betay)。没有 SDDS 工具时返回 None。"""
    twi = case_dir / "scan.twi"
    if not twi.exists() or not shutil.which("sdds2stream"):
        return None, None
    out = subprocess.check_output(["sdds2stream", str(twi), "-col=betax", "-col=betay"], text=True)
    bx, by = [], []
    for line in out.splitlines():
        try:
            a, b = [float(x) for x in line.split()[:2]]
        except Exception:
            continue
        bx.append(a); by.append(b)
    return (max(bx) if bx else None, max(by) if by else None)


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描 FODO 四极强度并汇总 beta 指标")
    parser.add_argument("--out", type=Path, default=Path("scan_results"), help="输出目录")
    parser.add_argument("--start", type=float, default=0.4, help="K1 起点")
    parser.add_argument("--stop", type=float, default=1.4, help="K1 终点")
    parser.add_argument("--points", type=int, default=6, help="扫描点数")
    parser.add_argument("--run", action="store_true", help="实际调用 elegant；默认只生成文件")
    args = parser.parse_args()

    elegant = shutil.which("elegant")
    rows = []
    for i in range(args.points):
        k1 = args.start + (args.stop - args.start) * i / max(args.points - 1, 1)
        case_dir = args.out / f"k1_{k1:.3f}"
        ele = write_case(case_dir, k1)
        if args.run and elegant:
            subprocess.run([elegant, ele.name], cwd=case_dir, check=False)
        elif args.run and not elegant:
            print("未找到 elegant，可先检查生成文件；安装后重新加 --run。")
        max_bx, max_by = try_extract_max_beta(case_dir)
        rows.append({"k1": k1, "case": str(case_dir), "max_betax": max_bx, "max_betay": max_by})

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["k1", "case", "max_betax", "max_betay"])
        writer.writeheader(); writer.writerows(rows)
    print(f"完成：{args.out / 'summary.csv'}")


if __name__ == "__main__":
    main()
