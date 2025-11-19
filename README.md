# AI-Voice-Assistant

A lightweight Python AI voice assistant that listens for voice commands, searches on google, plays audio, plays YouTube videos, opens web pages and YouTube, fetches headlines, tells jokes, and proxies other queries to Google Gemini (via `google.generativeai`).  
Built with `speech_recognition`, `pyttsx3` / `edge-tts` for TTS, `pygame` for simple audio playback, and a few useful helpers.

---

## Features
- Wake phrase handling (`hello`) → activate assistant.
- Play songs from YouTube using a natural voice cue.
- Open websites and search Google.
- Short news headlines (NewsAPI).
- Jokes (pyjokes).
- Short Wikipedia summaries.
- Responses powered by Google Gemini for general queries (configurable).
- Supports both local TTS (`pyttsx3`) and higher-quality neural TTS (`edge-tts`).

---

## Files you should have
- `main.py` (your script — the code you shared)
- `Initializing.mp3`, `yesSir.mp3`, `GoodByeSir.mp3` — small audio cues used by the assistant (place in same folder or adjust paths)
  - `voice.mp3` will be created temporarily by `edge-tts` when using `speakNatural()`

---

## Prerequisites
- Python 3.9+ recommended (some packages may require 3.8+)
- A working microphone and speakers
- Internet connection for:
  - YouTube search/opening links
  - NewsAPI requests
  - Google Gemini (if you use it)
  - `edge-tts` (it performs local TTS, but may require network depending on engine)

---

## Environment / API keys
This project uses external services that require API keys. Do **not** hardcode keys in production; use environment variables or a `.env` file.

Required keys:
- `NEWSAPI` (NewsAPI.org API key) — used for headlines
- `GEMINI_API_KEY` (Google Generative AI / Gemini API key) — used by `google.generativeai`

Example `.env` (or set environment variables directly):
