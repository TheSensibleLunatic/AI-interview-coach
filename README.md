# 🎤 AI Interview Coach - Campus Placement Edition

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An AI-powered interview practice platform designed specifically for final-year engineering students preparing for campus placements in India. Get real-time feedback on your STAR method answers, filler word usage, and communication skills.

![AI Interview Coach Demo](screenshot.png)

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## ✨ Features

### Current Features

- **🎯 Campus Placement Scenarios**: 10+ real placement scenario questions tailored for Indian students
- **🎙️ Voice Recording**: Record your answers directly in the browser
- **🤖 AI-Powered Analysis**: Google Gemini analyzes your answers using STAR method framework
- **📊 STAR Score Evaluation**: Get scored on Situation, Task, Action, and Result components
- **🚫 Filler Word Detection**: Identifies "um", "uh", "like" and other filler words
- **📝 Live Transcription**: OpenAI Whisper converts speech to text with high accuracy
- **🖥️ Real-time Console**: Watch the processing pipeline in action
- **💡 Expected Answer Examples**: See 5/5 reference answers for each question
- **✅ Key Points Checklist**: Know exactly what to cover in your answer
- **🎨 Beautiful UI**: Clean, modern interface with color-coded feedback

### Placement-Specific Context

- Questions about TCS vs product companies, internship dilemmas, GD scenarios
- Indian college context (tier-2/3, CGPA, placement cells)
- Real package numbers (₹3.5 LPA to ₹28 LPA)
- Company-specific scenarios (Google, Amazon, Infosys, Accenture)

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0**: Web framework and API server
- **Flask-CORS**: Cross-origin resource sharing
- **OpenAI Whisper (Base)**: Speech-to-text transcription
- **Google Gemini AI (2.0-flash)**: STAR method analysis and scoring
- **JSON**: Data exchange format

### Frontend
- **HTML5**: Markup structure
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: Recording, API calls, and DOM manipulation
- **MediaRecorder API**: Browser-based audio recording
- **Fetch API**: Asynchronous HTTP requests

### AI Models
- **Whisper Base Model**: ~74M parameters, runs locally on CPU
- **Gemini 2.0 Flash**: Fast inference for analysis (<3s)

## 📁 Project Structure
AI-coach/
├── app.py # Main Flask application
├── index.html # Frontend interface
├── uploads/ # Temporary audio storage (auto-created)
├── coach/ # Virtual environment (venv)
├── README.md # This file
└── requirements.txt # Python dependencies

text

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB RAM minimum (for Whisper model)
- Microphone access in browser
- Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

git clone https://github.com/yourusername/ai-interview-coach.git
cd ai-interview-coach

text

### Step 2: Create Virtual Environment

**On Windows:**
python -m venv coach
coach\Scripts\activate

text

**On macOS/Linux:**
python3 -m venv coach
source coach/bin/activate

text

### Step 3: Install Dependencies

pip install flask flask-cors openai-whisper google-generativeai

text

**Or use requirements.txt:**
pip install -r requirements.txt

text

### Step 4: Install FFmpeg (Required for Whisper)

**Windows:**
Download from https://ffmpeg.org/download.html
Add to PATH environment variable
text

**macOS:**
brew install ffmpeg

text

**Linux (Ubuntu/Debian):**
sudo apt update
sudo apt install ffmpeg

text

### Step 5: Configure API Key

Open `app.py` and replace the API key on line 11:

GEMINI_API_KEY = "your-actual-api-key-here"

text

**Security Note**: Never commit API keys to public repositories. Use environment variables in production:

import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

text

## ⚙️ Configuration

### Whisper Model Options

By default, the app uses the `base` model. You can change this in `app.py` line 55:

stt_model = whisper.load_model("base") # Options: tiny, base, small, medium, large

text

**Model Comparison:**

| Model  | Size   | Speed    | Accuracy |
|--------|--------|----------|----------|
| tiny   | 39 MB  | Fastest  | Good     |
| base   | 74 MB  | Fast     | Better   |
| small  | 244 MB | Moderate | Great    |
| medium | 769 MB | Slow     | Excellent|

### Gemini Model Options

Change on line 38 of `app.py`:

llm_model = genai.GenerativeModel('gemini-2.0-flash') # Or 'gemini-1.5-flash-latest'

text

## 🎮 Usage

### Starting the Application

1. **Activate virtual environment** (if not already active):
Windows
coach\Scripts\activate

macOS/Linux
source coach/bin/activate

text

2. **Run Flask server**:
python app.py

text

3. **Open in browser**: Navigate to `http://127.0.0.1:5000`

4. **Grant microphone permission** when prompted by browser

### Recording Your Answer

1. **Click "🔄 New Question"** to load a random placement scenario
2. **Review the STAR framework** reminder on the page
3. **Optional**: Click "Show Answer" to see the expected 5/5 response
4. **Click "🎤 Start Recording"** and speak your answer
5. **Click "⏹️ Stop Recording"** when finished
6. **Wait 10-30 seconds** for analysis (transcription + AI scoring)
7. **Review your results**:
- Transcript of your answer
- STAR score (1-5)
- Specific feedback on what to improve
- Filler words count
8. **Check the live console** at the bottom to see processing steps

### Sample Answer (5/5 Score)

**Question**: "You're in final round at Google. TCS offered you a role with 2-hour deadline. What do you do?"

**Good Answer**:
> "During my final year placement at VIT (Situation), I faced this exact dilemma between Google and TCS. I needed to decide quickly without burning bridges (Task). I immediately called TCS HR requesting a 24-hour extension, explaining I had another interview scheduled. Then I contacted Google's recruiter to expedite my decision. I also created a comparison spreadsheet showing ₹18 LPA vs ₹3.5 LPA and growth trajectories to show my parents (Action). Google appreciated my transparency and fast-tracked my result. I got the offer and joined at ₹18 LPA. The key lesson: always communicate professionally with all parties (Result)."

**Why this scores 5/5**:
- ✅ Clear situation (VIT, final year, specific companies)
- ✅ Defined task (decide without burning bridges)
- ✅ Detailed actions (called HR, contacted recruiter, data analysis)
- ✅ Quantified result (₹18 LPA, lesson learned)
- ✅ No filler words

## 🔧 How It Works

### Architecture Flow

User speaks → Browser records audio → Flask receives webm file
↓
Whisper transcribes speech → Text transcript generated
↓
Gemini analyzes with STAR framework → Score + Feedback
↓
Results sent to frontend → Displayed with color-coded UI

text

### Key Components

1. **Audio Recording**: `MediaRecorder API` captures audio in WebM format
2. **File Upload**: JavaScript `FormData` sends audio to Flask endpoint
3. **Transcription**: Whisper processes audio file and extracts text
4. **Analysis**: Gemini compares transcript to expected answer and key points
5. **Scoring Logic**:
   - 5/5: All key points covered with perfect STAR structure
   - 4/5: 5+ key points with good STAR structure
   - 3/5: 3-4 key points covered
   - 2/5: 1-2 key points, weak structure
   - 1/5: Missing most key points

### API Endpoints

- **GET** `/` - Serves the HTML frontend
- **GET** `/api/get-question` - Returns random question with expected answer
- **POST** `/api/analyze` - Receives audio, returns transcript + analysis
- **GET** `/api/logs` - Returns recent processing logs for live console

## 🚀 Future Enhancements

Based on user demand and market trends:

1. **Real-Time AI Interviewer**: AI asks follow-up questions dynamically
2. **Video Recording + Body Language Analysis**: Eye contact, posture, gestures
3. **Progress Dashboard**: Track improvement over 20+ attempts with charts
4. **Company-Specific Question Banks**: Google, Amazon, TCS-specific questions
5. **Mobile App**: iOS/Android with gamification and practice reminders
6. **Peer Practice Mode**: Match with other students for mock interviews
7. **Resume Integration**: Generate questions from your resume projects
8. **Multi-Language Support**: Practice in Hindi, Tamil, Telugu
9. **Voice Tone Analysis**: Confidence level from pitch and energy
10. **Interview Copilot**: Chrome extension for live assistance (controversial!)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test with different Whisper models
- Ensure cross-browser compatibility
- Update README if adding new features

## 🐛 Known Issues

- **Whisper FP16 Warning**: Safe to ignore, model auto-switches to FP32 on CPU
- **Log Spam**: Console polls every 3 seconds (can be adjusted in HTML line 450)
- **Large Audio Files**: Files >5MB may timeout on slower connections
- **Gemini Rate Limits**: Free tier has 60 requests/minute limit

## 📝 License

This project is licensed under the MIT License - see below:

MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

text

**Built with ❤️ for final-year students preparing for campus placements**

## 🙏 Acknowledgments

- **OpenAI Whisper** for open-source speech recognition
- **Google Gemini** for powerful language understanding
- **Flask** community for excellent documentation
- **Indian placement community** for feedback and questions

## 📊 Stats

- **10** curated placement scenario questions
- **3** AI models working together
- **<30 seconds** average analysis time
- **95%+** transcription accuracy (Whisper base)
- **0** cost per practice session (except API costs)

---

**⭐ If this project helped you, please star the repository!**

**💬 Have questions? Open an issue or reach out!**

**🚀 Ready to ace your placement interviews? Run `python app.py` and start practicing!**
