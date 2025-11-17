# 🎙️ Emotion-Aware Text-to-Speech Tutor (EA-TTS)

An AI-powered system that reads educational text aloud with automatic emotional tone modulation based on the detected emotion of each sentence.

## 🎯 Features

- **Emotion Detection**: Automatically analyzes each sentence to detect emotions (joy, sadness, anger, fear, surprise, love, neutral)
- **Emotional Speech Synthesis**: Converts text to speech with emotion-appropriate pitch, speed, and tone
- **Interactive Web Interface**: User-friendly Streamlit app for easy interaction
- **Multiple Input Methods**: Paste text directly or upload text files
- **Multi-language Support**: Supports English, Hindi, Spanish, French, and German
- **Real-time Analysis**: View detected emotions and confidence scores for each sentence
- **Audio Export**: Download generated speech as MP3 files

## 🧩 Tech Stack

- **Python 3.8+**
- **Streamlit**: Web interface
- **HuggingFace Transformers**: Emotion detection using `j-hartmann/emotion-english-distilroberta-base`
- **gTTS (Google Text-to-Speech)**: Speech synthesis
- **pydub**: Audio processing and modulation
- **NumPy & SciPy**: Audio signal processing

## 📦 Installation

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies (if needed)**
   - For audio playback, you may need `ffmpeg`:
     - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
     - macOS: `brew install ffmpeg`
     - Linux: `sudo apt-get install ffmpeg`

## 🚀 Usage

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

3. **Use the application**
   - Paste your text or upload a file
   - Click "Analyze Emotions" to detect emotions in each sentence
   - Review the emotion analysis results
   - Click "Generate Speech" to create emotion-aware audio
   - Download the generated audio file

## 🎭 Emotion-Voice Mapping

| Emotion | Pitch Change | Speed | Voice Tone |
|---------|-------------|-------|------------|
| Joy / Excited | +5% | Fast (1.2x) | Energetic |
| Love | +5% | Fast (1.15x) | Warm |
| Surprise | +7% | Fast (1.25x) | Bright |
| Anger | +10% | Fast (1.3x) | Firm / Sharp |
| Sadness | -5% | Slow (0.75x) | Soft / Calm |
| Fear | -10% | Slow (0.8x) | Low volume |
| Neutral | 0% | Normal (1.0x) | Balanced |

## 📝 Example Usage

**Input Text:**
```
The discovery of gravity was a momentous occasion in scientific history. 
Scientists were thrilled! However, the initial reactions were mixed with 
surprise and curiosity. Some researchers felt anxious about the implications.
```

**Output:**
- Sentence 1: Neutral emotion → Normal speech
- Sentence 2: Joy emotion → Fast, energetic speech
- Sentence 3: Surprise emotion → Bright, fast speech
- Sentence 4: Fear/Anxiety emotion → Slow, low-volume speech

## 🧪 Testing

Try these example texts:

1. **Happy/Excited Text:**
   ```
   Congratulations! You've won the grand prize! This is amazing news!
   ```

2. **Sad Text:**
   ```
   The loss was devastating. Everyone felt the weight of disappointment.
   ```

3. **Mixed Emotions:**
   ```
   The results were surprising. Some were happy, others were concerned.
   ```

## 🛠️ Project Structure

```
Emotion-Aware Text-to-Speech Tutor/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

## 🔧 Configuration

You can modify emotion parameters in `app.py`:

```python
EMOTION_PARAMS = {
    "joy": {"pitch_shift": 1.05, "speed": 1.2, "volume": 1.1, "tone": "Energetic"},
    # ... modify values as needed
}
```

## 🚧 Limitations & Future Enhancements

### Current Limitations:
- Audio pitch shifting is simplified (uses frame rate manipulation)
- Emotion detection works best with English text
- Requires internet connection for emotion model download and gTTS

### Planned Enhancements:
- [ ] Advanced pitch shifting using PSOLA or phase vocoder
- [ ] Multi-language emotion detection models
- [ ] PDF document support
- [ ] Emotion timeline visualization
- [ ] Voice selection (male/female)
- [ ] Batch processing for long documents
- [ ] Integration with Coqui TTS for higher quality speech

## 📚 Dependencies

- `streamlit>=1.28.0`: Web interface
- `transformers>=4.35.0`: HuggingFace models
- `torch>=2.0.0`: PyTorch for model inference
- `gtts>=2.4.0`: Google Text-to-Speech
- `pydub>=0.25.1`: Audio processing
- `numpy>=1.24.0`: Numerical operations
- `scipy>=1.11.0`: Scientific computing
- `soundfile>=0.12.1`: Audio file I/O

## 🐛 Troubleshooting

**Issue: Model download fails**
- Solution: Ensure you have internet connection. The model will download on first run.

**Issue: Audio playback doesn't work**
- Solution: Install `ffmpeg` and ensure `pydub` can find it.

**Issue: gTTS rate limiting**
- Solution: If you hit rate limits, wait a few minutes or use a VPN.

**Issue: Memory errors**
- Solution: Process text in smaller chunks or use a machine with more RAM.

## 📄 License

This project is open source and available for educational purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or issues, please open an issue on the repository.

---

**Built with ❤️ for educational purposes**

