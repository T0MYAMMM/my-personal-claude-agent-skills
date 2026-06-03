# AI Research Skills Scraping Status

**Last Updated**: November 2025

---

## ✅ Configs Generated (15 total)

### Phase 1: Fine-Tuning Stack (5)
- [x] axolotl (300 pages)
- [x] trl-fine-tuning (300 pages) - **rate_limit: 2.0s** (HF)
- [x] llama-factory (300 pages)
- [x] unsloth (200 pages)
- [x] huggingface-peft (250 pages) - **rate_limit: 2.0s** (HF)

### Phase 2: Distributed Training (4)
- [x] deepspeed (400 pages)
- [x] pytorch-fsdp (200 pages)
- [x] huggingface-accelerate (300 pages) - **rate_limit: 2.0s** (HF)
- [x] megatron-core (400 pages)

### Phase 3: Infrastructure (2)
- [x] pytorch-lightning (400 pages)
- [x] ray-train (300 pages)

### Phase 4: Safety & Data (3)
- [x] nemo-guardrails (300 pages)
- [x] nemo-curator (250 pages)
- [x] huggingface-tokenizers (200 pages) - **rate_limit: 2.0s** (HF)

### Phase 5: Architecture (1)
- [x] litgpt (200 pages)

---

## 🔄 Currently Scraping (3 processes)

1. **axolotl** - docs.axolotl.ai
2. **deepspeed** - deepspeed.ai
3. **pytorch-fsdp** - pytorch.org/docs/stable/fsdp.html

---

## ⏸️ Rate Limited (Need Retry)

**HuggingFace Sites** - Got 429 errors, now fixed with 2.0s rate_limit:
- trl-fine-tuning
- huggingface-peft
- huggingface-accelerate
- huggingface-tokenizers

**Action**: Retry after current batch completes

---

## 📋 Next Steps

1. ✅ Wait for current 3 to complete
2. ⏳ Retry 4 HuggingFace sites with 2.0s rate limits
3. ⏳ Scrape remaining 8 sites:
   - llama-factory
   - unsloth
   - megatron-core
   - pytorch-lightning
   - ray-train
   - nemo-guardrails
   - nemo-curator
   - litgpt

4. ⏳ Organize completed skills into directories
5. ⏳ Package skills as .zip files
6. ⏳ Move to claude-ai-research-skills organized structure

---

## 📁 Target Directory Structure

```
claude-ai-research-skills/
├── 3-fine-tuning/
│   ├── axolotl/
│   ├── trl/
│   ├── llama-factory/
│   └── unsloth/
├── 4-peft/
│   └── huggingface-peft/
├── 8-distributed-training/
│   ├── deepspeed/
│   ├── pytorch-fsdp/
│   ├── megatron-core/
│   └── accelerate/
├── 9-infrastructure/
│   ├── pytorch-lightning/
│   └── ray-train/
├── 7-safety-alignment/
│   └── nemo-guardrails/
├── 5-data-processing/
│   └── nemo-curator/
├── 2-tokenization/
│   └── huggingface-tokenizers/
└── 1-model-architecture/
    └── litgpt/
```

---

## 📊 Progress Tracker

**Total**: 15 skills
**Configs Created**: 15/15 ✅
**Currently Scraping**: 3/15 🔄
**Completed**: 0/15
**Failed (Need Retry)**: 4/15 (HF rate limits)
**Pending**: 8/15

**Estimated Time**:
- Current batch: ~20-30 minutes
- HF retry batch: ~40-60 minutes (4 skills × 2s rate limit)
- Remaining 8: ~2-3 hours

**Total**: ~3-4 hours for all 15 skills
