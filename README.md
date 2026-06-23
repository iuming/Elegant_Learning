# Elegant Learning ⚛️

从零开始学习 [elegant](https://ops.aps.anl.gov/elegant.html) —— APS 开发的加速器六维粒子跟踪仿真工具。

## 什么是 elegant？

**elegant**（ELEctron Generation ANd Tracking）是由 Argonne 国家实验室 Advanced Photon Source (APS) 开发的加速器仿真软件，用于：

- 加速器六维相空间（x, x', y, y', s, δ）粒子跟踪
- 储存环、直线加速器、传输线设计与优化
- 同步辐射效应（经典 + 量子）、尾场、空间电荷
- 轨道校正、色品校正、误差分析
- 基于 SDDS 文件格式的后处理与协作

## 安装

```bash
# 安装依赖 SDDS 库
git clone https://github.com/rtsoliday/SDDS.git
cd SDDS && make -j && cd ..

# 安装 elegant
git clone https://github.com/rtsoliday/elegant.git
cd elegant && make -j

# 验证
./bin/Linux-x86_64/elegant --version
```

## 目录结构

```
Elegant_Learning/
├── docs/                  # 设计工作流、概念说明
├── cheatsheets/           # elegant/SDDS 速查表
├── tutorial/              # 22 个教程（按难度递进）
│   ├── basic/             # 10 基础篇：lattice 语法、元素、命令
│   ├── intermediate/      #  6 进阶篇：环、注入、匹配
│   └── advanced/          #  6 高级篇：误差分析、阻抗、FMA、并行
├── examples/              #  6 实用脚本与模板
├── projects/              #  2 综合项目
├── RUNNING.md             # 运行说明
├── requirements.txt       # Python 后处理依赖
├── INDEX.md               # 文件索引
└── README.md
```


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=iuming/Elegant_Learning&type=Date)](https://www.star-history.com/#iuming/Elegant_Learning&Date)

## 📊 内容总览

| 难度 | 数量 | 涵盖主题 |
|------|------|----------|
| 🟢 基础 | 10 | Lattice 文件语法、元素类型、run_setup、束团生成、Twiss 计算 |
| 🟡 进阶 | 6 | 闭合轨道、轨道校正、色品校正、优化、RF 加速、匹配约束 |
| 🔴 高级 | 6 | 误差与容差分析、尾场效应、CSR、动力学孔径、FMA、并行 Pelegant |
| 🛠 工具 | 6 | SDDS 处理脚本、Python 后处理、批量仿真、FMA 与参数扫描模板 |
| 📚 文档 | 2 | 设计工作流、elegant/SDDS 速查 |
| 🚀 项目 | 2 | FODO 线完整仿真、储存环 lattice 从设计到 DA |
| **合计** | **30 个主题** | 实际含配套 `.lte`/脚本共 58+ 文件 |

## 快速开始

```bash
# 克隆本仓库
git clone git@github.com:iuming/Elegant_Learning.git
cd Elegant_Learning

# 运行第一个示例（建议从文件所在目录运行）
cd tutorial/basic
elegant 01_hello_elegant.ele
```

```elegant
! elegant 输入文件示例 — 最简单的工作流
&run_setup
    lattice       = "simple.lte",
    use_beamline  = "MAIN",
    p_central     = 1000.0,          ! MeV/c
    default_order = 2,
&end

&run_control &end
&sigma_matrix  &end
&bunched_beam  &end
&track         &end
```

## 🔗 学习路径

```
基础 01-05  →  理解 elegant 输入文件结构与元素语法
基础 06-10  →  掌握束流参数计算（Twiss、包络、动量紧缩因子）
进阶 01-06  →  环动力学核心（闭轨、校正、色品、优化、匹配）
高级 01-06  →  物理效应与工程分析（误差、尾场、CSR、DA、FMA）
工具 + 项目  →  独立完成加速器 lattice 设计
```

## 资源

- [elegant 用户手册](https://ops.aps.anl.gov/manuals/elegant_latest/elegant.html)
- [elegant 官方页面](https://ops.aps.anl.gov/elegant.html)
- [elegant 论坛](https://www3.aps.anl.gov/forums/elegant/)
- [elegant GitHub 源码](https://github.com/rtsoliday/elegant)
- [SDDS 工具包文档](https://www.aps.anl.gov/Accelerator-Operations-Physics/Documentation)

## 运行说明

多数 `.ele` 文件引用同目录下的 `.lte` 文件；运行细节、SDDS 输出和 Python 后处理说明见 `RUNNING.md`。

## License

MIT
