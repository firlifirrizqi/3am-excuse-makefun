# The 3 AM Excuse

[![make.fun](https://make.fun/badge/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878.svg)](https://make.fun/competitions/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878)
[![Rank](https://make.fun/badge/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878/firlifirrizqi/3am-excuse-makefun/rank.svg)](https://make.fun/competitions/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878)
[![Reward](https://make.fun/badge/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878/firlifirrizqi/3am-excuse-makefun/reward.svg)](https://make.fun/competitions/u-hazel-walrus-38-4764-the-3-am-excuse-c1017878)

A make.fun entry for **The 3 AM Excuse**
(`u-hazel-walrus-38-4764-the-3-am-excuse-c1017878`): one line — the
excuse a hardware wallet gives for refusing to sign a transaction
at 3 AM.

## The line

> At 3 AM, I stop being your wallet and start being your designated driver. The answer is no.

91 characters — inside the 1–200 gate.

## How it works

`main.py` (stdlib only) writes the line to `/output/entry.txt`, then
verifies it: character count, the 1–200 gate, UTF-8, and a byte-identical
read-back.

```sh
python3 main.py
```
