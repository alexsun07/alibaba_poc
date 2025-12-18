# Kunlun-benchmark

use correct python(main version) and ubuntu verison. For example:
```
wget https://sinian-metrics-platform.oss-cn-hangzhou.aliyuncs.com/ai_perf/pack/kunlun_benchmark/main/ubuntu22.04/py3.12.8/kunlun-benchmark.tar.gz
# or
# wget https://sinian-metrics-platform.oss-cn-hangzhou.aliyuncs.com/ai_perf/pack/kunlun_benchmark/main/ubuntu22.04/py3.10.12/kunlun-benchmark.tar.gz
```

```
tar -xvzf kunlun-benchmark.tar.gz
pip install "requests" "prettytable" "pytz" "transformers" "pydantic" "datasets" "click" "loguru" "oss2" "jsonlines"
```
Run benchmark see [bench.sh](./bench.sh)
