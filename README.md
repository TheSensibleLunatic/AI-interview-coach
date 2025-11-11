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

