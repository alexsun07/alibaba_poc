set -ex


export GLOO_SOCKET_IFNAME=enp193s0f1np1

python -m sglang_router.launch_router \
  --pd-disaggregation --mini-lb \
  --prefill http://10.2.224.31:30002 \
  --decode http://10.2.224.32:30003 \
  --host 0.0.0.0 --port 8000 \
  2>&1 | tee log_router.log
