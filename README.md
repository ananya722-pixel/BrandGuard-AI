# 🛡️ BrandGuard AI
### AI-Powered Brand Compliance Checker

BrandGuard AI is an AI-powered web application designed to help businesses review marketing content against their brand guidelines. It combines rule-based validation with Google's Gemini AI to identify potentially risky claims, explain possible violations, and suggest improvements.

The goal is to help marketing teams create consistent, trustworthy, and brand-compliant content while reducing the time required for manual reviews.

🔗 **Live Demo:** [Add your Streamlit Community Cloud URL here]  
💻 **GitHub Repository:** https://github.com/ananya722-pixel/BrandGuard-AI

---

## 📌 Problem Statement

Marketing teams frequently produce advertisements, promotional messages, product descriptions, and other customer-facing content.

This content may contain:
- Unsupported or exaggerated claims.
- Absolute promises, such as guaranteed results.
- Potentially misleading marketing statements.
- Language that conflicts with established brand guidelines.
- Inconsistent messaging across different materials.

Manual compliance reviews can be time-consuming. BrandGuard AI provides an accessible first-pass review to help identify potential issues before content is published.

## 💡 Our Solution

BrandGuard AI combines traditional rule-based checks with AI-powered contextual analysis.

Users submit marketing content and provide brand guidelines. The application analyses the content, flags potential violations, explains the identified risks, and suggests alternative wording.

The application is intended to support human reviewers, not replace legal, regulatory, or professional compliance review.

## ✨ Features

- **Brand Guideline Analysis:** Review submitted marketing content against user-provided brand guidelines.
- **Rule-Based Detection:** Use predefined rules and regular expressions to identify known risky phrases and claims.
- **AI-Powered Analysis:** Use Google's Gemini API to analyse content in context.
- **Violation Explanations:** Present explanations of potential brand compliance issues.
- **Suggested Corrections:** Generate alternative wording to help users improve flagged content.
- **Severity Classification:** Categorise detected issues by severity.
- **Review History:** Use SQLite to persist review records.
- **JSON Export:** Export analysis results for further use.
- **Interactive Dashboard:** Review analysis results through a Streamlit web interface.

*Note: The reliability of individual features depends on the deployed version and the configured API. See Known Limitations below.*

## ⚙️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and analysis |
| Streamlit | Web interface and interactive dashboard |
| Google Gemini API | Contextual content analysis and suggested corrections |
| `google-genai` | Python SDK for accessing Gemini |
| Regular Expressions | Detection of predefined risky phrases and patterns |
| SQLite | Persistent review-history storage |
| Git and GitHub | Version control and source-code hosting |
| Streamlit Community Cloud | Web application deployment |

## 🏗️ System Architecture

```text
                ┌─────────────────────────┐
                │         User            │
                │ Marketing Content +     │
                │ Brand Guidelines        │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │    Streamlit Interface  │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │    Analysis Workflow    │
                └────────────┬────────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
       ┌──────────────────┐   ┌──────────────────┐
       │ Rule-Based Engine│   │   Gemini API     │
       │ Python + Regex   │   │ Contextual AI    │
       └─────────┬────────┘   └─────────┬────────┘
                 │                      │
                 └──────────┬───────────┘
                            ▼
                ┌─────────────────────────┐
                │   Analysis Results      │
                │ Flags, Severity,        │
                │ Explanations, Fixes      │
                └────────────┬────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
        ┌─────────────────┐  ┌─────────────────┐
        │ SQLite Review   │  │ JSON Export     │
        │ History         │  │ Analysis Data   │
        └─────────────────┘  └─────────────────┘
```

### How It Works

1. **Input:** The user submits marketing content and the relevant brand guidelines.
2. **Rule-Based Validation:** Python rules and regular expressions check for predefined risky phrases and claims.
3. **AI Analysis:** The Gemini API evaluates the content in context and generates explanations and suggested corrections.
4. **Results:** The application presents identified issues and their associated severity levels.
5. **Persistence and Export:** Review records can be stored in SQLite, and supported analysis results can be exported as JSON.

Rule-based and AI-generated findings may differ. Results should therefore be reviewed by a human before making compliance decisions.

## 🚀 Getting Started

Follow these instructions to run BrandGuard AI locally.

### Prerequisites

- Python 3.12 recommended.
- Git.
- A Google Gemini API key.
- An internet connection for Gemini API requests.

### 1. Clone the Repository

```bash
git clone https://github.com/ananya722-pixel/BrandGuard-AI.git
```

Navigate to the project directory:

```bash
cd BrandGuard-AI
```

### 2. Create a Virtual Environment

**Windows:**

```bash
py -3.12 -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If it does not, install the packages required by the application:

```bash
pip install streamlit google-genai python-dotenv
```

Install any additional dependencies used by your actual code.

### 4. Configure the Gemini API Key

Create a file named `.env` in the project root if your application loads its configuration from environment variables.

Add:

```env
GEMINI_API_KEY=your_actual_api_key
```

Replace `your_actual_api_key` with your own Gemini API key.

**Security:** Never commit `.env` or expose your API key in source code, screenshots, logs, or public repositories. Add `.env` to `.gitignore`.

Example `.gitignore` entries:

```gitignore
.env
venv/
__pycache__/
*.py[cod]
```

If your application reads Streamlit secrets instead, configure `GEMINI_API_KEY` in the Streamlit Community Cloud app settings using the secrets format expected by your code.

### 5. Run the Application

Run the following command from the directory containing your Streamlit entry-point file:

```bash
streamlit run app.py
```

If your main application file has a different name or location, use the appropriate path.

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## 🧪 Example Use Case

**Brand guideline:** Marketing claims must be evidence-based. Absolute guarantees and unsupported superiority claims should be avoided.

**Sample marketing content:**

> Our product guarantees results with 100% accuracy. We are the best in the world.

### Expected Analysis

| Potential issue | Example finding |
|---|---|
| Absolute guarantee | "guarantees results" |
| Absolute accuracy claim | "100% accuracy" |
| Unsupported superiority claim | "best in the world" |

Depending on the configured rules and AI response, BrandGuard AI may flag these statements, explain the potential risks, and suggest more qualified alternatives.

**Example suggested revision:**

> Our product is designed to deliver reliable results. Actual performance may vary depending on the use case and available data.

This is an illustrative example. Actual findings and severity classifications may vary.

## 📊 Responsible Use

BrandGuard AI is a decision-support tool, not a guarantee of compliance.

- AI-generated findings may be incomplete or inaccurate.
- Rule-based checks may miss violations that are expressed in unfamiliar language.
- Severity classifications may differ between the rule-based engine and the AI model.
- Users should verify factual claims and supporting evidence independently.
- A qualified human reviewer should make final publication and compliance decisions.
- Do not submit confidential or sensitive business information unless its processing is authorised and appropriate.

## ⚠️ Known Limitations

- The human-review decision button is not yet reliably functional.
- Rule-based and AI-generated severity classifications may differ.
- Detection accuracy depends on the supplied guidelines, predefined rules, and AI responses.
- Advanced capabilities such as approved-asset verification and collaborative team reviews are not yet implemented.
- Multi-format document and image analysis is not currently a completed feature.

These limitations are acknowledged so that users can evaluate the application's current capabilities accurately.

## 🔮 Future Improvements

### 1. Approved Claims Verification
Compare marketing statements against a verified library of approved claims and messaging to help identify unsupported promises.

### 2. Multi-Format Content Analysis
Extend analysis to PDFs, documents, and images using document text extraction and OCR.

### 3. Collaborative Review and Audit Trail
Enable team members to review flagged content, record approval decisions, and maintain a traceable history of compliance reviews.

These are proposed improvements, not claims about currently implemented functionality.

## 🔐 API Key Security

BrandGuard AI requires a valid Gemini API key for AI-powered analysis.

- Store credentials in environment variables or deployment secrets.
- Do not hard-code API keys.
- Never commit `.env` files to GitHub.
- If a key is accidentally exposed, revoke or rotate it.
- Review API usage and applicable provider terms before deploying the application publicly.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your implementation.
5. Submit a pull request describing the changes.

Please avoid including API keys, private credentials, or confidential data in contributions.

## 👩‍💻 Project Information

**Project:** BrandGuard AI  
**Category:** Artificial Intelligence / Brand Compliance  
**Primary Language:** Python  
**Interface:** Streamlit  
**AI Integration:** Google Gemini API

**Developed as a project exploring the use of AI and rule-based systems to support safer, more consistent marketing content.**

---

*BrandGuard AI is an assistive compliance tool. Its results should be verified by a human reviewer before publication.*
