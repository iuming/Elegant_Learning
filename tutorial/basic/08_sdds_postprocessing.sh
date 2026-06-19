! tutorial/basic/08_sdds_postprocessing.sh
! ============================================
! 学习 SDDS 工具包：后处理与数据分析
! 这是 shell 脚本，不是 elegant 输入文件
! 运行: bash sdds_postprocessing.sh

#!/bin/bash

# ---- SDDS 基本操作 ----
# sddsquery: 查询 SDDS 文件信息
echo "=== 查看文件结构 ==="
sddsquery my_run.twi

# sddsprintout: 打印文件内容
echo "=== 前 5 行数据 ==="
sddsprintout -col=ElementName,s,betax,betay my_run.twi | head -10

# ---- sddsprocess: 数据处理核心 ----
# 定义新列、筛选、计算
echo "=== 处理数据 ==="

# 提取 BPM 位置的 beta 函数
sddsprocess my_run.twi bpm_beta.sdds \
    -match=col,ElementType,MONI \
    -print=col,ElementName,s,betax,betay,alphax,alphay,etax

# 计算新列 (例如有效发射度)
sddsprocess my_run.bun processed.sdds \
    -define=col,r,xi yi sqr + sqrt,units=m \
    -define=col,pr,pxi pyi sqr + sqrt

# ---- sddsplot: 绘图 ----
echo "=== 绘制 beta 函数 ==="
sddsplot -graph=line,vary \
    -column=s,betax \
    -column=s,betay \
    my_run.twi \
    -legend -title="Beta Functions" \
    -xlabel="s (m)" -ylabel="β (m)"

# ---- sdds2stream: 转换为其他格式 ----
# 导出为 CSV
sdds2stream my_run.twi -col=s,betax,betay,etax > optics_data.csv

# ---- sddscombine: 合并多个文件 ----
# sddscombine file1.sdds file2.sdds merged.sdds -merge

# ---- sddsfilter: 按条件筛选行 ----
sddsfilter my_run.twi monitor_locations.sdds \
    -include=col,ElementType,MONI

# ---- sddssort: 排序 ----
# sddssort input.sdds output.sdds -col=s

# ---- sddscontour: 等高线图 ----
# sddscontour data.sdds -column=x,y,Intensity

echo "=== 后处理完成 ==="
