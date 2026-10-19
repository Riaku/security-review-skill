---
categories: [ai-llm, compliance-privacy]
domains: [data]
---

# Synthetic Data Memorisation Checks

**MUST NOT** treat synthetic records as non-personal until memorisation and nearest-neighbour tests show they cannot reproduce real individuals from the training set.

**Why:** Generative models emit training rows verbatim or near-verbatim for rare records, so a synthetic release can leak the very individuals it was generated to protect.

**Detect:** command: run a distance-to-closest-training-record test and a membership-inference check (`sdmetrics`, `synthcity`, or an explicit overlap count) before release; flag exports shipped with no test result recorded.

**References:** NIST SP 800-188 De-Identifying Government Datasets, https://csrc.nist.gov/pubs/sp/800/188/final, Shokri et al., Membership Inference Attacks Against Machine Learning Models, https://arxiv.org/abs/1610.05820, Carlini et al., Extracting Training Data from Large Language Models, https://arxiv.org/abs/2012.07805
