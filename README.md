# L2F: Learning to Fly Simulator


```
git submodule update --init --recursive
pip install -e .
```

This repo contains Python bindings for the simulator introduced in [Learning to Fly in Seconds](https://arxiv.org/abs/2311.13081).

Please check the [example](./examples/test.py) for how to use it.

The only change in this fork is the increased action length of 32, which is the length from the original learning to fly article. This length is used for the guiding controller.

## CUDA

For the CUDA usage please refer to [rl-tools/l2f-benchmark](https://github.com/rl-tools/l2f-benchmark)
