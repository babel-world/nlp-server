# 中文文本规范化（TN）

将非标准词（NSW，如数字、日期、电话）转为适合中文朗读/ G2P 的汉字形式。

## 来源

本目录代码自 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 的 `GPT_SoVITS/text/zh_normalization` 复制而来。

其最初来自 [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech) 的 `paddlespeech/t2s/frontend/zh_normalization`（PaddlePaddle Authors，Apache 2.0）。GPT-SoVITS 在中文 G2P 前使用同一套规则。

上游参考：[DeepSpeech PR #658](https://github.com/PaddlePaddle/DeepSpeech/pull/658/files)

## 许可

源文件头部的 Apache License 2.0 声明保留。使用与再分发请遵守该许可。

## 用法

```python
from nlp_server.services.tn.zh import TextNormalizer

normalizer = TextNormalizer()
sentences = normalizer.normalize("明天有62％的概率降雨")
# ['明天有百分之六十二的概率降雨']

text = "".join(sentences)
```

单句处理：

```python
normalizer.normalize_sentence("等会请在12:05请通知我")
# '等会请在十二点零五分请通知我'
```

## 支持的 NSW 示例

| 类型 | 原文 | 规范化后 |
|------|------|----------|
| 编号 | 编号27149 | 编号二七一四九 |
| 基数 | 重达324.75克 | 重达三百二十四点七五克 |
| 范围 | 12~23 | 十二到二十三 |
| 日期 | 1995年3月1日 | 一九九五年三月一日 |
| 时间 | 12:05 | 十二点零五分 |
| 温度 | -10°C | 零下十度 |
| 分数 | 7/12 | 十二分之七 |
| 百分数 | 62％ | 百分之六十二 |
| 金额 | 12块5 | 十二块五 |
| 电话 | 0421-33441122 | 零四二一三三四四一一二二 |

## 依赖

- `pypinyin`（`constants.py` 中 `SUPPORT_UCS4`）

## 说明

- 文件名 `text_normlization.py` 为上游拼写，未改。
- 当前仅 vendored 到本仓库，尚未挂 API 端点；后续可在 `g2p/zh` 等流程前调用。
