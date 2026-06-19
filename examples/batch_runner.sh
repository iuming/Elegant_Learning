#!/bin/bash
# examples/batch_runner.sh
# ============================================
# 批量运行 elegant 仿真的脚本框架
# 支持: 参数扫描、误差 Monte Carlo、并行执行

set -e

ELEGANT="${ELEGANT:-elegant}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- 颜色输出 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
function warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
function error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---- 参数扫描 ----
function momentum_scan() {
    local LATTICE="$1"
    local OUTPUT_DIR="${2:-scan_output}"
    
    mkdir -p "$OUTPUT_DIR"
    info "开始动量扫描: $LATTICE → $OUTPUT_DIR"
    
    for p in $(seq 500 200 3000); do
        info "  p_central = $p MeV/c"
        
        cat > /tmp/scan_run.ele << EOF
        &run_setup
            lattice = "$(realpath "$LATTICE")",
            use_beamline = "RING",
            p_central = $p,
            default_order = 2,
            rootname = "$(realpath "$OUTPUT_DIR")/p${p}",
        &end
        &twiss_output filename = %s.twi, output_at_each_step = 1, matched = 1 &end
        &run_control &end
        &bunched_beam n_particles_per_bunch = 1 &end
        &track &end
EOF
        
        $ELEGANT /tmp/scan_run.ele
    done
    
    info "扫描完成: $(ls "$OUTPUT_DIR"/*.twi | wc -l) 个 Twiss 文件"
}

# ---- 误差 Monte Carlo ----
function monte_carlo_errors() {
    local INPUT="$1"
    local N_RUNS="${2:-10}"
    local OUTPUT_DIR="${3:-mc_output}"
    
    mkdir -p "$OUTPUT_DIR"
    info "MC 误差分析: $N_RUNS 次运行"
    
    for seed in $(seq 1 $N_RUNS); do
        info "  运行 $seed/$N_RUNS (seed=$seed)"
        
        sed "s/random_number_seed = 12345/random_number_seed = $(date +%s)/" \
            "$INPUT" > /tmp/mc_run.ele
        
        $ELEGANT /tmp/mc_run.ele > "$OUTPUT_DIR/run_${seed}.log" 2>&1
    done
    
    info "MC 完成: $(ls "$OUTPUT_DIR"/*.log | wc -l) 次运行"
}

# ---- 并行执行 (GNU parallel) ----
function parallel_scan() {
    local TEMPLATE="$1"
    local PARAM_FILE="$2"
    
    if ! command -v parallel &> /dev/null; then
        warn "GNU parallel 未安装, 使用串行执行"
    fi
    
    info "并行扫描: $TEMPLATE"
    
    cat "$PARAM_FILE" | parallel -j $(nproc) \
        "$ELEGANT $TEMPLATE -macro={}"
}

# ---- 主函数 ----
function main() {
    echo "=========================================="
    echo "  elegant Batch Runner"
    echo "=========================================="
    
    case "${1:-help}" in
        scan)
            momentum_scan "${2}" "${3}"
            ;;
        mc)
            monte_carlo_errors "${2}" "${3}" "${4}"
            ;;
        help)
            echo "用法:"
            echo "  $0 scan <lattice.lte> [output_dir]"
            echo "  $0 mc <input.ele> [n_runs] [output_dir]"
            ;;
        *)
            error "未知命令: $1"
            exit 1
            ;;
    esac
}

main "$@"
