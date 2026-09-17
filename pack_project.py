import os
import zipfile
readme_content = """# GFC Financial Chatbot - Documentation
## 1. Overview
The GFC Financial Assistant is a rule-based web chatbot built with Python (Flask) and JavaScript that analyzes financial metrics for Apple, Microsoft, and Tesla across fiscal years 2023–2025.

## 2. System Architecture
- **Backend**: Python Flask server handling asynchronous JSON POST requests (`/chat`).
- **Frontend**: Responsive HTML/CSS interface using JavaScript `fetch` API.
- **Query Parser**: Custom NLP keyword extractor (supporting English & Arabic) utilizing regular expressions to parse entities, metrics, and temporal constraints.

## 3. Supported Queries
- Direct Lookups: "Apple revenue 2023"
- Summaries: "Tesla summary"
- Trends: "Microsoft net income trend"
- Comparisons: "Compare cash flow between Apple and Tesla"

## 4. Limitations
- Rule-based pattern matching (No generative LLM).
- Static dataset limited to 3 companies (2023–2025).
- Stateless interaction without conversation history.
"""
with open('README.md', 'w', encoding='utf-8') as f:
  f.write(readme_content)
files_to_pack = [
    'app.py',
    'README.md',
    os.path.join('templates', 'index.html'),
    os.path.join('static', 'style.css'),]

zip_filename = 'gfc_chatbot_submission.zip'

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
  for file in files_to_pack:
    if os.path.exists(file):
      zipf.write(file, arcname=file)
      print(f"✔ Added to zip: {file}")
    else:
      print(f"✖ Warning: File not found - {file}")

print(f"\n🎉 Package created successfully: {os.path.abspath(zip_filename)}")