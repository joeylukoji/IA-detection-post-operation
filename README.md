# MedDiag: AI-Assisted Post-Operative Diagnosis

Desktop application that helps clinicians pre-assess post-operative patients: enter the patient profile and observed symptoms, get a ranked differential diagnosis from a medical inference engine, and ask an LLM for plain-language medical information.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-desktop-41CD52)
![Infermedica](https://img.shields.io/badge/Infermedica-API%20v3-orange)
![Replicate](https://img.shields.io/badge/Replicate-Llama%202-black)

> ⚠️ **Research prototype, not a medical device.** Results are decision support only and must be validated by a qualified physician.

## Features

| Tab | What it does |
|---|---|
| **Home** | Overview and instructions |
| **Patient information** | Sex, age, blood group, known chronic or genetic conditions |
| **Diagnosis** | Sends the patient profile and symptom IDs to the **Infermedica** `/diagnosis` endpoint and displays the ranked conditions with their probabilities |
| **Medical information** | Answers a medical question with **Llama 2 7B Chat** hosted on **Replicate** |

Dark UI with QDarkStyle; packaged as a standalone executable with PyInstaller.

## Architecture

```
main.py ──▶ ui_main.py (PyQt5 MainWindow, 4 tabs)
                 │
                 ▼
           api_handler.py ──▶ Infermedica API v3  (diagnosis)
                          └─▶ Replicate API       (Llama 2 LLM answers)
```

## Getting started

```bash
git clone https://github.com/joeylukoji/IA-detection-post-operation.git
cd IA-detection-post-operation
pip install -r requirements.txt
cp .env.example .env    # then fill in your API keys
python main.py
```

### API keys (`.env`)

| Variable | Where to get it |
|---|---|
| `INFERMEDICA_APP_ID`, `INFERMEDICA_APP_KEY` | [Infermedica developer portal](https://developer.infermedica.com/) |
| `REPLICATE_API_TOKEN` | [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) |

The app starts without keys but the corresponding features return an error message.

### Build a standalone executable

```bash
pip install pyinstaller
pyinstaller main.spec    # output in dist/
```

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point: loads `.env`, applies the dark theme, opens the window |
| `ui_main.py` | PyQt5 interface (tabs, forms, result views) |
| `api_handler.py` | Infermedica and Replicate clients with timeouts and error handling |
| `styles.qss` | Optional Qt stylesheet |
| `main.spec` | PyInstaller build configuration |

## Roadmap

- Symptom search by name instead of Infermedica IDs
- Post-operative complication scoring (infection, bleeding, thrombosis)
- Export of the patient report as PDF

## Author

**Joy Lukoji**, Independent AI Researcher · [Portfolio](https://joyportfolio-six.vercel.app/)
