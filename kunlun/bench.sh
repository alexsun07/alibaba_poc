cd kunlun-benchmark
# 3.0~3.6k/0.3~0.5k
# 16~20k/0.3~0.5k
# 0.8~1k/1.6~2k
# 3.6~4.4k/1.8~2.2k
# 11~15k/2.5~2.9k
INPUT_OUTPUT_COMBOS=(
    "800 1000 1600 2000"
    "3000 3600 300 500"
    "16000 20000 300 500"
    "3600 4400 1800 2200"
    "11000 15000 2500 2900"
)
for COMBO in "${INPUT_OUTPUT_COMBOS[@]}"; do
    read -r MIN_INPUT MAX_INPUT MIN_OUTPUT MAX_OUTPUT <<< "$COMBO"
    CONCURRENCY="32 64 128 256"
    if [ $MIN_INPUT -ge 10000 ]; then
        CONCURRENCY="8 16 32 64"
    fi
    for CON in $CONCURRENCY; do
        echo "test config: concurrency=$CON, min_input=$MIN_INPUT, max_input=$MAX_INPUT, min_output=$MIN_OUTPUT, max_output=$MAX_OUTPUT"
        if [ $CON -le 30 ]; then
          PROMPTS=$((CON * 4))
        else
          PROMPTS=$((CON * 2))
        fi
        ./kunlun-benchmark vllm server \
            --port 30000 \
            --work_mode manual \
            --max_input_len $MAX_INPUT \
            --min_input_len $MIN_INPUT \
            --max_output_len $MAX_OUTPUT \
            --min_output_len $MIN_OUTPUT \
            --concurrency $CON \
            --query_num $PROMPTS \
            --result_dir ~/results/ \
            --model_path $MODEL \
            --is_sla False \
            --sla_decode 50 \
            --sla_prefill 3000

        sleep 2

    done
done