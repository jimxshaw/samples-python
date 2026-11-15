# NLP Using Transformers

Four transformer NLP tasks on *Alice's Adventures in Wonderland* (Project Gutenberg #11):
text summarization, English→French translation, question answering (chatbot), and text generation.

## Data (global URLs only — nothing to download manually)
- English book: https://www.gutenberg.org/cache/epub/11/pg11.txt
- French reference translation (Henri Bué, 1869, Gutenberg #55456): https://www.gutenberg.org/cache/epub/55456/pg55456.txt
- All models download automatically from the Hugging Face Hub.

## How to run
1. Python 3.10+. Install dependencies:  `pip install -r requirements.txt`
2. Open the notebook in Jupyter, VS Code, or Google Colab.
3. Run all cells top to bottom (Kernel → Restart & Run All).
   - GPU is optional. On a 6-core CPU, a full run from scratch takes roughly 20–30 minutes.
   - Heavy results are cached in `cache/` as `.pkl` files; reruns load them in seconds.
     Delete `cache/` to recompute everything from scratch.

## Models
| Task | Model | Architecture |
|---|---|---|
| Summarization | facebook/bart-large-cnn | encoder-decoder |
| Translation | Helsinki-NLP/opus-mt-en-fr (+ opus-mt-fr-en for back-translation) | encoder-decoder |
| Q&A reader | distilbert-base-cased-distilled-squad | encoder-only |
| Q&A retriever | sentence-transformers/all-MiniLM-L6-v2 (+ TF-IDF baseline) | encoder-only |
| Generation | gpt2 (+ distilgpt2 for comparison) | decoder-only |

## Outputs
`final_results.csv`, `summarization_tuning_results.csv`, `summarization_length_tradeoff.png`,
`translation_vs_bue_scores.csv`, `translation_beam_tuning.csv`, `qa_tuning_results.csv`,
`qa_predictions.csv`, `generation_decoding_sweep.csv`

## Assumptions
- Transformers v5 removed the summarization, translation, and question-answering pipelines, so
  models are called directly (`AutoModelForSeq2SeqLM`, `AutoModelForQuestionAnswering`,
  `AutoModelForCausalLM` + `generate()`). Pretrained weights are unchanged.
- Evaluation uses chapters 1–3. Reference summaries and Q&A pairs were written by the author.
- Translation is evaluated two ways: back-translation (EN→FR→EN) and against Bué's 1869 translation,
  paragraph-aligned automatically with chrF similarity; unmatched paragraphs (rewritten poems/wordplay) are excluded.
- Sentences are split with a regex, which can fragment dialogue.
- Random seed: 42.
