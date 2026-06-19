# 运行说明

## 重要：从示例所在目录运行

多数 `.ele` 文件引用同目录下的 `.lte` lattice 文件，因此推荐先进入对应目录再运行：

```bash
cd tutorial/basic
elegant 01_hello_elegant.ele
```

如果本机未配置 `RPN_DEFNS` 环境变量，可临时使用：

```bash
elegant -rpnDefns=/dev/null 01_hello_elegant.ele
```

项目目录也是一样：

```bash
cd projects/fodo_line_full
elegant run_optics.ele
elegant run_tracking.ele
```

## SDDS 输出

Elegant 会生成 `.twi`、`.bun`、`.matrix`、`.da`、`.fmap`、`.sdds` 等输出文件。这些已在 `.gitignore` 中排除。

## 常用检查命令

```bash
# 查看 SDDS 文件结构
sddsquery fodo_optics.twi

# 导出关键列
sdds2stream fodo_optics.twi -col=s -col=betax -col=betay | head
```

## Python 后处理

仓库中的 Python 工具依赖：

```bash
pip install numpy matplotlib scipy
```

部分脚本调用 `sdds2stream`、`sddsquery` 等外部 SDDS 命令，请确保 SDDS 工具在 `PATH` 中。
