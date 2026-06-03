# stepaudio-2.5-tts API Reference

Exact request/response shapes for `stepaudio-2.5-tts`. Verified 2026-04-23 against the live StepFun API. Read this when you need to call the API by hand (curl, custom HTTP client) instead of using the bundled `scripts/tts_generate.py`.

## Endpoint

```
POST https://api.stepfun.com/v1/audio/speech
Content-Type: application/json
Authorization: Bearer <STEPFUN_API_KEY>
```

## Request body

```json
{
  "model": "stepaudio-2.5-tts",
  "input": "你好，我是蕾格。",
  "voice": "shuangkuaijiejie",
  "response_format": "mp3",
  "speed": 1.0,
  "volume": 1.0,
  "instruction": "克制的悲伤，语气低沉柔弱"
}
```

| Field | Required | Type | Notes |
|---|---|---|---|
| `model` | yes | string | Must be `stepaudio-2.5-tts` |
| `input` | yes | string | ≤1000 chars; can contain inline `(directive)` parentheses |
| `voice` | yes | string | e.g. `shuangkuaijiejie`. Zero-shot clones use the clone's ID |
| `response_format` | yes | string | `mp3` (default), `wav`, or `opus` |
| `speed` | no | float | 0.5-2.0, default 1.0 |
| `volume` | no | float | 0.0-2.0, default 1.0 |
| `instruction` | no | string | Global tone directive, natural language, ≤200 chars |
| `voice_label` | — | — | **DO NOT SEND**. Returns `voice_label is not supported for v2 models`. Belongs to step-tts-2 |

## Inline directives inside `input`

Parentheses `()` in the `input` are consumed as TTS control signals, not pronounced. Examples that work:

- `(停顿一下)` — insert a pause
- `(轻声)` — reduce volume / breathy
- `(加重)` — stress the following word
- `(试探着问)` — apply a tone shift mid-sentence
- `(突然沉下来)` — emotion pivot

You can mix `instruction` (global tone) with inline `()` (per-phrase micro-control):

```json
{
  "instruction": "富有情绪弧线的独白",
  "input": "(试探着问)你好吗？(开心地)太好了！(突然沉下来)不过...我快要消失了。"
}
```

## Response

On success: binary audio stream in the requested `response_format`. HTTP 200. No JSON wrapper. Save the body directly as `.mp3`/`.wav`/`.opus`.

## Known error responses

```json
{"error":{"message":"voice_label is not supported for v2 models","type":"request_params_invalid"}}
```
→ Remove `voice_label`, use `instruction` instead.

```json
{"error":{"message":"The content you provided or machine outputted is blocked.","type":"censorship_block"}}
```
→ Content triggered censorship. Common triggers: 死, 消失, politically sensitive terms. See `known_issues.md`.

## Comparison with sibling and legacy endpoints

| Model | Endpoint | Request format |
|---|---|---|
| `stepaudio-2.5-tts` (this skill) | `/v1/audio/speech` | JSON with `instruction` (no voice_label) |
| `stepaudio-2.5-asr` (sibling, see `stepfun-asr` skill) | `/v1/audio/asr/sse` | JSON + base64 audio + SSE response |
| `step-tts-2` / `step-tts-mini` (legacy) | `/v1/audio/speech` | JSON with `voice_label` |
| `step-asr` / `step-asr-1.1` (legacy) | `/v1/audio/transcriptions` | multipart/form-data |

Legacy `step-tts-2` still works. It's the baseline in `migration_from_v2.md` and the per-line fallback when `stepaudio-2.5-tts` hits `censorship_block`.

## Auth and key handling

- Key header: `Authorization: Bearer <key>`
- Keys can be retrieved at https://platform.stepfun.com/ → API Keys
- "Plan" keys (cheaper subscription) are **restricted** to text models on `api.stepfun.com/step_plan`. They **cannot** call audio endpoints. Use a "Normal" key for all TTS calls.
- Same key works for both TTS and ASR — no separate scopes

## Rate / throughput notes (observed, not officially documented)

- ~400ms sleep between batch requests avoids 429s in practice
- MP3 responses consistently at 128kbps 24kHz mono (TTS default)
