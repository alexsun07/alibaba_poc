import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

def parse_io_range_from_filename(filename: str) -> str:
    """
    从文件名中解析输入输出范围
    例如: Qwen3-8B-FP8_normal_distribution_unknown_server_vllm_tp-1_1000&800_2000&1600_128_256_sla-False_1765957493_ai_perf_benchmark.md
    输入: 800~1000, 输出: 1600~2000
    返回: 0.8~1k/1.6~2k
    """
    # 查找数字对，如 1000&800, 2000&1600
    pattern = r'(\d+)&(\d+)_(\d+)&(\d+)'
    match = re.search(pattern, filename)

    if match:
        # 提取四个数字
        input_max = int(match.group(1))  # 1000
        input_min = int(match.group(2))  # 800
        output_max = int(match.group(3))  # 2000
        output_min = int(match.group(4))  # 1600

        # 转换为k为单位
        def format_k_range(min_val: int, max_val: int) -> str:
            """格式化范围，如 0.8~1k"""
            if max_val >= 100:
                min_k = min_val / 1000
                max_k = max_val / 1000
                # 保留一位小数
                min_str = f"{min_k:.1f}".rstrip('0').rstrip('.')
                max_str = f"{max_k:.1f}".rstrip('0').rstrip('.')
                return f"{min_str}~{max_str}k"
            else:
                return f"{min_val}~{max_val}"

        input_range = format_k_range(input_min, input_max)
        output_range = format_k_range(output_min, output_max)

        return f"{input_range}/{output_range}"
    return "null"

def parse_md_file(filepath: str) -> Optional[Dict[str, str]]:
    """
    解析单个md文件，提取所需指标
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 初始化结果字典
        filename = os.path.basename(filepath)
        result = {
            'filename': filename,
            'io range': parse_io_range_from_filename(filename),
            'GTPS': None,
            'TPS': None,
            'QPS': None,
            'Concurrency': None,
            'avg TTFT': None,
            'avg TPOT': None
        }

        # 逐行解析
        lines = content.split('\n')
        for line in lines:
            # 匹配表格行
            if '|' in line and not line.startswith('|---') and not line.startswith('| :'):
                # 分割列
                parts = [part.strip() for part in line.split('|') if part.strip()]
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    # 根据key提取所需的值
                    if 'Generate Tokens  Per Second(GTPS)' in key:
                        result['GTPS'] = value.split()[0]  # 只取数字部分
                    elif 'Total    Tokens  Per Second(TPS)' in key:
                        result['TPS'] = value.split()[0]
                    elif 'Queries Per Second(QPS)' in key:
                        # 从 "3.3213 reqs/s" 中提取数字
                        match = re.search(r'([\d.]+)\s*reqs/s', value)
                        if match:
                            result['QPS'] = match.group(1)
                        else:
                            result['QPS'] = value.split()[0] if value else None
                    elif 'Concurrency' in key:
                        result['Concurrency'] = value
                    elif 'Average  Prefill Time (TTFT)' in key:
                        result['avg TTFT'] = value.split()[0] if value else None
                    elif 'Average  Decode Time (TPOT)' in key:
                        result['avg TPOT'] = value.split()[0] if value else None

        return result
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}", file=sys.stderr)
        return None

def process_md_files(directory_path: str) -> List[Dict[str, str]]:
    """
    遍历目录下的所有.md文件并解析
    """
    results = []

    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.", file=sys.stderr)
        return results

    # 遍历所有.md文件
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                result = parse_md_file(filepath)
                if result:
                    results.append(result)

    return results

def print_results(results: List[Dict[str, str]]) -> None:
    """
    打印结果表格
    """
    if not results:
        print("No .md files found or no valid data extracted.")
        return

    # 定义表头
    headers = ['io range', 'GTPS', 'TPS', 'QPS', 'Concurrency', 'avg TTFT', 'avg TPOT']

    # 计算每列的最大宽度
    col_widths = {header: len(header) for header in headers}

    for result in results:
        for header in headers:
            if header == 'Filename':
                value = result.get('filename', '')
            else:
                value = result.get(header, 'N/A')
            col_widths[header] = max(col_widths[header], len(str(value)) if value else 0)

    # 打印表头
    header_line = " | ".join([header.ljust(col_widths[header]) for header in headers])
    separator = "-+-".join(['-' * col_widths[header] for header in headers])
    print("=" * len(separator))
    print(header_line)
    print(separator)
    results.sort(key=lambda x: (x['io range'], int(x['Concurrency'])))

    # 打印数据行
    for result in results:
        row = []
        for header in headers:
            if header == 'Filename':
                value = result.get('filename', '')
            else:
                value = result.get(header, 'N/A')
            row.append(str(value).ljust(col_widths[header]))
        print("   ".join(row))
    print("=" * len(separator))

def main():
    """
    主函数
    """
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python parse_md_metrics.py <directory_path>")
        print("Example: python parse_md_metrics.py ./benchmark_results")
        sys.exit(1)

    directory_path = sys.argv[1]

    print(f"Processing .md files in: {directory_path}")

    # 处理文件
    results = process_md_files(directory_path)

    # 打印结果
    print_results(results)

    # 汇总信息
    print(f"\nTotal files processed: {len(results)}")

if __name__ == "__main__":
    main()
