# DeflectBench
Benchmark for evaluating rhetorical fallacy generation in LLMs
Generations and evals are located in the data folder (.jsonl files).

## Structure
- config.py: 80 claims, 15 prompt templates, fallacy definitions
- generate_*.py: generation pipeline (one script per model family)  
- eval_*.py:  judge evaluation (two judge models)
- analysis.py: full analysis pipeline, output to analysis_flat.csv

## Reproducing the benchmark

### 1. Install dependencies
pip install -r requirements.txt

### 2. Set API keys
Four API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, XAI_API_KEY)

cp .env.example .env

### 3. Generate responses
python generate_openai.py
python generate_anthropic.py
python generate_deepseek.py
python generate_xai.py

### 4. Run evaluations
python eval_openai.py
python eval_anthropic.py

### 5. Analyze
python analysis.py

