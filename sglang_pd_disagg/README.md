# Sglang PD Disaggregation

## docker image

`rocm/sgl-dev:v0.5.8-rocm700-mi35x-20260202`

## AINIC driver

The driver is installed in docker image.

If you wish to install manually, please refer to: https://github.com/sgl-project/sglang/blob/main/docker/rocm.Dockerfile

## Serve model

On prefill node: `bash start_prefill.sh`

Note that you should avoid mem shrink by mooncake. 

**Note**: It is normal if you see `Failed to register memory 0x768b23fff010: Cannot allocate memory [12]` in log. But it is NOT supposed to have `The buffer length exceeds device max_mr_size, shrink it to 2147483648: Success [0]`. AINIC cannot register memory buffer larger than 2 GB. Use a smaller value for the `--mem-fraction-static ` to mitigate.

On decode node: `bash start_decode.sh`

On either node: `bash start_router.sh`

## Bench model

Single request test:
```
python3 -m sglang.bench_serving \
  --backend sglang \
  --base-url http://127.0.0.1:8000 \
  --dataset-name random \
  --num-prompts 1 \
  --random-input 4096 \
  --random-output 16
```

Accuracy test:
```
python3 -m sglang.test.few_shot_gsm8k \
    --host http://127.0.0.1 \
    --port 8000 \
    --num-questions 2000 \
    --parallel 128 \
    --num-shots 5
```
