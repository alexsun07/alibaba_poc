export SGLANG_USE_AITER=1

python3 -m sglang.launch_server \
    --trust-remote-code \
    --attention-backend aiter \
    --tp-size 8 \
    --model deepseek-ai/DeepSeek-R1-0528
