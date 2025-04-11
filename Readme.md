# 📧 SmartReach AI Email Generator

An AI-powered email generator and sender built using Streamlit, powered by the `Gemma 3B` model via [OpenRouter.ai](https://openrouter.ai). This tool allows users to generate professional emails from a prompt, edit the output, and send them to multiple recipients using SMTP.

---

## 🔗 Live Demo

👉 [Click here to try the live deployed app](https://ai-email-sender-lumio.streamlit.app/)

---

## 🧠 Features

- ✨ Generate AI-based email **subject and body** from a prompt
- 🖊️ Edit the generated content before sending
- 📤 Send email to multiple recipients
- 🔒 Secure credentials via Streamlit Secrets
- ⚠️ Graceful fallback in case of API failure
- 🧼 Clean and minimal UI built for quick use

---

## 💻 Tech Stack

| Layer        | Technology                     |
|--------------|---------------------------------|
| Frontend     | Streamlit                      |
| Backend      | Streamlit + Python             |
| AI Model     | `google/gemma-3-27b-it:free` via [OpenRouter](https://openrouter.ai) |
| Email Engine | `smtplib` + `EmailMessage`     |
| Deployment   | [Streamlit Cloud](https://streamlit.io/cloud) |

---

## 🚀 How It Works

1. **Enter Prompt**: Describe the type of email you'd like to generate.
2. **Generate Email**: Uses the Gemma model to produce a professional subject and body.
3. **Edit Content**: Review and tweak the AI's output as needed.
4. **Send Email**: Input credentials and send to one or more recipients.

---

## 🛠️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/noeltiju/lumioai-round
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Streamlit secrets**

Create a .streamlit/ directory if it doesn’t exist, and add a secrets.toml file inside it.
```bash
OPENROUTER_API_KEY = "your_openrouter_api_key"
```


4. **Run Locally**

```bash
streamlit run app.py
```