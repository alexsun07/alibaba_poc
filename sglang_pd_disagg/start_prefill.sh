set -ex

export SGLANG_USE_AITER=1

# These env vars should adjust according to your environment
export GLOO_SOCKET_IFNAME=enp193s0f1np1
export SGLANG_HOST_IP=10.2.224.31
export MC_GID_INDEX=2


python -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-R1-0528 \
  --tp-size 8 \
  --disaggregation-mode prefill \
  --disaggregation-ib-device ionic_0,ionic_1,ionic_2,ionic_3,ionic_4,ionic_5,ionic_6,ionic_7 \
  --disaggregation-transfer-backend mooncake \
  --load-balance-method round_robin \
  --host $SGLANG_HOST_IP \
  --port 30002 \
  --mem-fraction-static 0.5 \
  --disable-radix-cache \
  --trust-remote-code \
  2>&1 | tee log_prefill.log
