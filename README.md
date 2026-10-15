# AI Customer Feedback Automation

A Python-based AI automation system that processes customer feedback using **pandas, OpenAI API, and Streamlit**.

The application automates data cleaning, sentiment classification, and report generation through a simple web interface.

## Features

- Upload CSV or Excel files through Streamlit
- Validate and clean customer feedback data
- Remove empty and duplicate records
- Classify feedback sentiment using an LLM
- Generate structured summaries
- Validate AI responses and handle processing errors
- Export analysis results to Excel

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| pandas | Data processing and cleaning |
| OpenAI API | Sentiment analysis and summarization |
| Streamlit | Web interface |
| openpyxl | Excel export |
| pytest | Automated testing |

## Project Structure

```text
ai-feedback-automation/
├── app.py
├── pipeline.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── sample_data/
│   └── sample_feedback.csv
└── tests/
    └── test_pipeline.py
```

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ai-feedback-automation.git
cd ai-feedback-automation
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Copy `.env.example` to `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

**4. Run the application**

```bash
streamlit run app.py
```

## Usage

1. Upload a CSV or Excel file containing `feedback_id` and `feedback`.
2. Review the uploaded data.
3. Start the AI analysis.
4. View the processed results.
5. Download the Excel report.

## Testing

Run the automated tests:

```bash
python -m pytest -q
```

## Limitations

- AI-generated classifications may require human review.
- API requests may incur usage costs.
- Processing time depends on dataset size and API availability.

## Future Improvements

- Add sentiment distribution charts and processing metrics
- Improve API retry and rate-limit handling
- Evaluate classification accuracy using labeled datasets
- Add automated CI testing

---

**Project Type:** AI Automation / LLM Integration / Data Processing

**Language:** Python
