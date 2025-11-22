import streamlit as st
import os
import re
import subprocess
import shutil
import platform
import tempfile
import sys

# Core imports with error handling
# These are required - if they fail, we'll handle it gracefully
try:
    import numpy as np
except ImportError:
    np = None
    # Don't use st.error here as Streamlit might not be ready yet
    import warnings
    warnings.warn("numpy is required but not installed")

try:
    from transformers import pipeline
except ImportError as e:
    pipeline = None
    import warnings
    warnings.warn(f"transformers library is required but not installed: {e}")

try:
    from gtts import gTTS
except ImportError as e:
    gTTS = None
    import warnings
    warnings.warn(f"gTTS library is required but not installed: {e}")
# Audio processing - LAZY IMPORTS ONLY
# pydub is imported only when needed to avoid any startup errors
# This function safely imports pydub and returns availability status
def _get_pydub():
    """Lazy import of pydub - only imports when actually needed"""
    global _pydub_cache
    if _pydub_cache is None:
        _pydub_cache = {'available': False, 'AudioSegment': None, 'speedup': None, 'normalize': None}
        try:
            # Check if audioop is available first (Python 3.11 has it built-in)
            try:
                import audioop
            except ImportError:
                # Try pyaudioop as fallback (but don't require it)
                try:
                    import pyaudioop  # type: ignore
                except ImportError:
                    return _pydub_cache  # No audioop available, pydub won't work
            
            # Now try to import pydub
            from pydub import AudioSegment  # type: ignore
            from pydub.effects import speedup, normalize  # type: ignore
            _pydub_cache = {
                'available': True,
                'AudioSegment': AudioSegment,
                'speedup': speedup,
                'normalize': normalize
            }
        except Exception:
            # pydub not available or failed to import - that's OK
            pass
    return _pydub_cache

# Initialize cache
_pydub_cache = None
from io import BytesIO
from datetime import datetime

# PDF and Document processing
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Text-to-Speech with voice selection
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Translation support
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# Supported languages for translation & TTS
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian"
}

GTT_LANGUAGE_MAP = {
    "zh": "zh-cn"
}


def get_tts_language_code(lang_code: str) -> str:
    """Map display language codes to gTTS compatible codes"""
    if not lang_code:
        return "en"
    return GTT_LANGUAGE_MAP.get(lang_code.lower(), lang_code.lower())

# Page configuration
st.set_page_config(
    page_title="Emotion-Aware Text-to-Speech Tutor",
    page_icon="🎙️",
    layout="wide"
)

# Initialize emotion classifier
@st.cache_resource
def load_emotion_model():
    """Load the emotion classification model"""
    if pipeline is None:
        return None
    try:
        # Use CPU for Streamlit Cloud compatibility
        try:
            import torch
            device = -1  # -1 means CPU (works on all platforms)
        except ImportError:
            device = -1  # Default to CPU if torch not available
        
        classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=1,
            device=device
        )
        return classifier
    except Exception as e:
        # Don't show error in UI during import, just return None
        # Error will be handled when model is actually used
        import warnings
        warnings.warn(f"Error loading emotion model: {e}")
        return None

# Global variable to cache FFmpeg path
_ffmpeg_path_cache = None

def find_ffmpeg_path():
    """Find FFmpeg installation path"""
    global _ffmpeg_path_cache
    
    # Return cached path if available
    if _ffmpeg_path_cache is not None:
        return _ffmpeg_path_cache
    
    # Common installation paths (platform-specific)
    common_paths = []
    system = platform.system()
    if system == "Windows":
        common_paths = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
            os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "ffmpeg", "bin", "ffmpeg.exe"),
        ]
    elif system == "Linux":
        # Linux common paths (including Streamlit Cloud)
        common_paths = [
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/opt/ffmpeg/bin/ffmpeg",
        ]
    elif system == "Darwin":  # macOS
        common_paths = [
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
            "/usr/bin/ffmpeg",
        ]
    
    # First check if ffmpeg is in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        # Check common installation paths
        for path in common_paths:
            if os.path.exists(path):
                ffmpeg_path = path
                break
    
    # Cache the result
    _ffmpeg_path_cache = ffmpeg_path
    return ffmpeg_path

# Check if ffmpeg is available
def check_ffmpeg():
    """Check if ffmpeg is installed and accessible"""
    # On Streamlit Cloud, FFmpeg is typically not available
    # Skip subprocess checks to avoid health check failures
    try:
        # Check if we're on Streamlit Cloud (common indicators)
        is_streamlit_cloud = (
            os.environ.get("STREAMLIT_SERVER_PORT") is not None or
            os.environ.get("STREAMLIT_SERVER_ADDRESS") is not None or
            "/mount/src" in os.path.abspath(__file__) if hasattr(os.path, 'abspath') else False
        )
        
        # On Streamlit Cloud, assume FFmpeg is not available (it's not installed)
        if is_streamlit_cloud:
            return False, "FFmpeg is not available on Streamlit Cloud. Basic TTS will still work."
    except Exception:
        pass  # Continue with normal check
    
    ffmpeg_path = find_ffmpeg_path()
    
    if ffmpeg_path is not None:
        try:
            # Try to run ffmpeg to verify it works (with very short timeout for health checks)
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=2,  # Shorter timeout for faster health checks
                check=False,  # Don't raise exception on non-zero return
                stderr=subprocess.DEVNULL,  # Suppress stderr
                stdout=subprocess.DEVNULL  # Suppress stdout for health checks
            )
            if result.returncode == 0:
                # If found in common path but not in PATH, add it to current session (Windows only)
                if platform.system() == "Windows":
                    try:
                        bin_dir = os.path.dirname(ffmpeg_path)
                        try:
                            current_path = os.environ.get("PATH", "")
                            if bin_dir not in current_path:
                                # Add to current session PATH
                                os.environ["PATH"] = bin_dir + os.pathsep + current_path
                        except Exception:
                            pass  # Continue even if PATH update fails
                        # Also set for subprocess calls
                        if hasattr(os, 'add_dll_directory') and os.path.exists(bin_dir):
                            try:
                                os.add_dll_directory(bin_dir)
                            except:
                                pass
                    except Exception:
                        pass  # Continue even if PATH update fails
                return True, None
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, Exception) as e:
            # Silently fail - FFmpeg not available
            pass
    
    # FFmpeg not found
    return False, """
    ### Quick Installation Guide
    
    **FFmpeg is optional** - Basic text-to-speech works without it!
    FFmpeg only enables advanced audio effects (pitch, speed, volume adjustments).
    
    ---
    
    **Windows (Easiest - if you have Chocolatey):**
    ```powershell
    choco install ffmpeg
    ```
    
    **Windows (Manual):**
    1. Download: https://www.gyan.dev/ffmpeg/builds/ (get "ffmpeg-release-essentials.zip")
    2. Extract to `C:\\ffmpeg`
    3. Add to PATH:
       - Press `Win + X` → System → Advanced system settings
       - Environment Variables → System variables → Path → Edit
       - Add: `C:\\ffmpeg\\bin`
    4. Restart terminal and verify: `ffmpeg -version`
    
    **macOS:**
    ```bash
    brew install ffmpeg
    ```
    
    **Linux:**
    ```bash
    sudo apt-get update && sudo apt-get install ffmpeg
    ```
    
    💡 **Tip:** Run `install_ffmpeg_simple.ps1` in PowerShell for automated Windows installation!
    
    After installing, restart this Streamlit app.
    """

# Emotion to voice parameters mapping
EMOTION_PARAMS = {
    "joy": {"pitch_shift": 1.05, "speed": 1.2, "volume": 1.1, "tone": "Energetic"},
    "love": {"pitch_shift": 1.05, "speed": 1.15, "volume": 1.05, "tone": "Warm"},
    "surprise": {"pitch_shift": 1.07, "speed": 1.25, "volume": 1.15, "tone": "Bright"},
    "anger": {"pitch_shift": 1.10, "speed": 1.3, "volume": 1.2, "tone": "Firm"},
    "sadness": {"pitch_shift": 0.95, "speed": 0.75, "volume": 0.9, "tone": "Soft"},
    "fear": {"pitch_shift": 0.90, "speed": 0.8, "volume": 0.85, "tone": "Low"},
    "neutral": {"pitch_shift": 1.0, "speed": 1.0, "volume": 1.0, "tone": "Balanced"}
}

def split_into_sentences(text):
    """Split text into sentences"""
    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    return sentences

def extract_text_from_pdf(file_bytes, filename):
    """Extract text from PDF file"""
    text = ""
    try:
        # Try pdfplumber first (better for complex PDFs)
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text.strip()
            except Exception as e:
                st.warning(f"pdfplumber extraction failed: {e}. Trying PyPDF2...")
        
        # Fallback to PyPDF2
        if PYPDF2_AVAILABLE:
            pdf_file = BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        
        # If neither library is available
        st.error("PDF processing libraries not installed. Please install pdfplumber or PyPDF2.")
        return None
        
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(file_bytes, filename):
    """Extract text from DOCX file"""
    try:
        if not DOCX_AVAILABLE:
            st.error("python-docx library not installed. Please install it to process DOCX files.")
            return None
        
        doc = Document(BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
        
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return None

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file based on file type"""
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name
    file_ext = filename.split('.')[-1].lower()
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(file_bytes, filename)
    elif file_ext in ['docx', 'doc']:
        return extract_text_from_docx(file_bytes, filename)
    elif file_ext in ['txt', 'md']:
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_bytes.decode('latin-1')
            except Exception as e:
                st.error(f"Error decoding text file: {e}")
                return None
    else:
        st.error(f"Unsupported file type: {file_ext}")
        return None

def translate_text(text, target_lang='en', source_lang='auto'):
    """Translate text to target language using Google Translator (matches Google Translate behavior)"""
    if not TRANSLATOR_AVAILABLE:
        return text, "Translation library not available"
    
    if not text or len(text.strip()) == 0:
        return text, ""
    
    # Don't translate if source and target are the same
    if source_lang != 'auto' and source_lang == target_lang:
        return text, ""
    
    try:
        # Create translator instance with Google Translator
        # GoogleTranslator uses the same engine as Google Translate
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        # Translate the text (this matches Google Translate output)
        # GoogleTranslator uses the same Google Translate API
        translated = translator.translate(text)
        
        # Verify translation actually happened
        if translated and translated.strip():
            translated = translated.strip()
            
            # Preserve original formatting/capitalization where appropriate
            # (Google Translate sometimes adjusts capitalization, which is expected)
            
            # Check if translation is different from original
            if translated.lower().strip() == text.lower().strip():
                # Translation returned original - might be same language
                # Try with explicit source language if auto-detect was used
                if source_lang == 'auto':
                    try:
                        # Try with explicit English source
                        translator_en = GoogleTranslator(source='en', target=target_lang)
                        translated_en = translator_en.translate(text)
                        if translated_en and translated_en.strip() and translated_en.lower().strip() != text.lower().strip():
                            translated = translated_en.strip()
                        else:
                            # Text might already be in target language or translation failed
                            return text, "Translation appears identical to original. Text might already be in target language."
                    except Exception as e2:
                        return text, f"Translation returned same text. Error: {str(e2)}"
                else:
                    return text, "Translation appears identical to original. Source and target might be the same."
            
            # Return successfully translated text
            return translated, ""
        else:
            return text, "Translation returned empty result"
            
    except Exception as e:
        error_msg = str(e)
        # Try with explicit source language if auto-detect failed
        if source_lang == 'auto':
            try:
                # Fallback: try with explicit English source
                translator = GoogleTranslator(source='en', target=target_lang)
                translated = translator.translate(text)
                if translated and translated.strip():
                    return translated.strip(), ""
            except Exception as e2:
                return text, f"Translation error: {error_msg}. Fallback error: {str(e2)}"
        return text, f"Translation error: {error_msg}"

def detect_emotion(text, classifier):
    """Detect emotion in text"""
    if not text or len(text.strip()) == 0:
        return "neutral", 0.0
    
    if classifier is None:
        return "neutral", 0.0
    
    try:
        result = classifier(text)
        # Handle different output formats
        if isinstance(result, list):
            if len(result) > 0:
                if isinstance(result[0], dict):
                    emotion = result[0].get('label', 'neutral').lower()
                    score = result[0].get('score', 0.0)
                elif isinstance(result[0], list) and len(result[0]) > 0:
                    emotion = result[0][0].get('label', 'neutral').lower()
                    score = result[0][0].get('score', 0.0)
                else:
                    emotion = "neutral"
                    score = 0.0
            else:
                emotion = "neutral"
                score = 0.0
        elif isinstance(result, dict):
            emotion = result.get('label', 'neutral').lower()
            score = result.get('score', 0.0)
        else:
            emotion = "neutral"
            score = 0.0
        
        return emotion, score
    except Exception as e:
        st.warning(f"Emotion detection error: {e}")
        return "neutral", 0.0

def adjust_audio_pitch(audio_segment, pitch_shift):
    """Adjust audio pitch using frame rate manipulation"""
    # Note: This method changes pitch but also affects speed slightly
    # For better pitch shifting, consider using librosa or similar libraries
    if pitch_shift != 1.0:
        # Change frame rate to shift pitch
        original_frame_rate = audio_segment.frame_rate
        new_sample_rate = int(original_frame_rate * pitch_shift)
        audio_segment = audio_segment._spawn(
            audio_segment.raw_data,
            overrides={"frame_rate": new_sample_rate}
        )
        # Set frame rate back to original to maintain duration
        audio_segment = audio_segment.set_frame_rate(original_frame_rate)
    return audio_segment

def generate_pdf_report(emotions_data, title="Emotion Analysis Report"):
    """Generate PDF report from emotion analysis results"""
    if not REPORTLAB_AVAILABLE:
        st.error("reportlab library not installed. Cannot generate PDF reports.")
        return None
    
    try:
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.leading = 14
        
        # Title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated:</b> {report_date}", normal_style))
        elements.append(Paragraph(f"<b>Total Sentences Analyzed:</b> {len(emotions_data)}", normal_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary statistics
        emotion_counts = {}
        total_confidence = 0
        for item in emotions_data:
            emotion = item['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_confidence += item['score']
        
        avg_confidence = total_confidence / len(emotions_data) if emotions_data else 0
        
        elements.append(Paragraph("Summary Statistics", heading_style))
        elements.append(Paragraph(f"<b>Average Confidence:</b> {avg_confidence:.2%}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Emotion distribution
        elements.append(Paragraph("Emotion Distribution:", normal_style))
        for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(emotions_data)) * 100
            elements.append(Paragraph(f"• {emotion.title()}: {count} ({percentage:.1f}%)", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(PageBreak())
        
        # Detailed results
        elements.append(Paragraph("Detailed Analysis", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Create table data
        table_data = [['#', 'Text', 'Emotion', 'Confidence', 'Tone']]
        
        for idx, item in enumerate(emotions_data, 1):
            params = EMOTION_PARAMS.get(item['emotion'], EMOTION_PARAMS["neutral"])
            text = item['sentence'][:80] + "..." if len(item['sentence']) > 80 else item['sentence']
            table_data.append([
                str(idx),
                text,
                item['emotion'].title(),
                f"{item['score']:.2%}",
                params['tone']
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.4*inch, 3.5*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
        
    except Exception as e:
        st.error(f"Error generating PDF report: {e}")
        return None

def get_available_voices():
    """Get available voices from pyttsx3"""
    if not PYTTSX3_AVAILABLE:
        return []
    
    try:
        # Try to initialize engine with driver selection
        try:
            engine = pyttsx3.init()
        except Exception as e:
            # Try with specific driver for Windows
            if platform.system() == "Windows":
                try:
                    engine = pyttsx3.init('sapi5')
                except:
                    return []
            else:
                return []
        
        voices = engine.getProperty('voices')
        engine.stop()
        
        voice_list = []
        for voice in voices:
            voice_info = {
                'id': voice.id,
                'name': voice.name,
                'gender': 'female' if 'female' in voice.name.lower() or 'zira' in voice.name.lower() else 'male'
            }
            # Try to detect gender from voice properties
            if hasattr(voice, 'gender'):
                voice_info['gender'] = 'female' if voice.gender == 'VoiceGenderFemale' else 'male'
            voice_list.append(voice_info)
        
        return voice_list
    except Exception as e:
        return []

def generate_speech_with_voice(text, voice_gender='female', lang='en', use_pyttsx3=True, prefer_gtts=False):
    """Generate speech using pyttsx3 with voice selection or fallback to gTTS"""
    try:
        tts_lang = get_tts_language_code(lang)
        # If prefer_gtts is True (e.g., for translated text), use gTTS directly
        # gTTS supports many languages better than pyttsx3
        if prefer_gtts:
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
            return tmp_file.name
        
        # Check if ffmpeg is available (needed for audio processing)
        ffmpeg_available, ffmpeg_message = check_ffmpeg()
        if not ffmpeg_available:
            # If ffmpeg not available, try pyttsx3 directly (no audio processing)
            if use_pyttsx3 and PYTTSX3_AVAILABLE and lang == 'en':
                # pyttsx3 works best with English, use gTTS for other languages
                try:
                    return generate_speech_pyttsx3(text, voice_gender)
                except:
                    pass
            # Use gTTS as fallback
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
            return tmp_file.name
        
        # Try pyttsx3 first if available and requested (only for English)
        # For other languages, use gTTS which has better language support
        if use_pyttsx3 and PYTTSX3_AVAILABLE and lang == 'en':
            try:
                return generate_speech_pyttsx3(text, voice_gender)
            except Exception as e:
                st.warning(f"pyttsx3 failed: {e}. Falling back to gTTS...")
        
        # Use gTTS for all languages (better language support)
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
        return tmp_file.name
        
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

def generate_speech_pyttsx3(text, voice_gender='female'):
    """Generate speech using pyttsx3 with voice gender selection"""
    if not PYTTSX3_AVAILABLE:
        raise Exception("pyttsx3 is not available")
    
    try:
        # Try to initialize engine with driver selection for headless environments
        try:
            engine = pyttsx3.init()
        except Exception as e:
            # Try with specific driver for Windows
            if platform.system() == "Windows":
                try:
                    engine = pyttsx3.init('sapi5')
                except:
                    engine = pyttsx3.init('nsss' if platform.system() == "Darwin" else 'espeak')
            else:
                raise e
        
        voices = engine.getProperty('voices')
        
        # Select voice based on gender
        selected_voice = None
        if voice_gender.lower() == 'female':
            # Try to find a female voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    selected_voice = voice
                    break
                if hasattr(voice, 'gender') and voice.gender == 'VoiceGenderFemale':
                    selected_voice = voice
                    break
            # If no female voice found, use last voice (often female on Windows)
            if selected_voice is None and len(voices) > 1:
                selected_voice = voices[-1]
        else:  # male
            # Try to find a male voice
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                    selected_voice = voice
                    break
                if hasattr(voice, 'gender') and voice.gender == 'VoiceGenderMale':
                    selected_voice = voice
                    break
            # If no male voice found, use first voice (often male on Windows)
            if selected_voice is None:
                selected_voice = voices[0] if len(voices) > 0 else None
        
        # Set voice
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
        
        # Set speech rate (words per minute)
        engine.setProperty('rate', 150)  # Normal speed
        
        # Generate speech to file
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        output_path.close()
        
        engine.save_to_file(text, output_path.name)
        engine.runAndWait()
        engine.stop()
        
        return output_path.name
        
    except Exception as e:
        raise Exception(f"Error with pyttsx3: {e}")

def generate_emotional_speech(text, emotion, lang='en', slow=False, voice_gender='female', use_pyttsx3=True, prefer_gtts=False):
    """Generate speech with emotional modulation and voice selection"""
    try:
        # Check if ffmpeg is available
        ffmpeg_available, ffmpeg_message = check_ffmpeg()
        if not ffmpeg_available:
            # If ffmpeg not available but pyttsx3 is, use it without audio processing (only for English)
            if use_pyttsx3 and PYTTSX3_AVAILABLE and lang == 'en' and not prefer_gtts:
                try:
                    audio_path = generate_speech_pyttsx3(text, voice_gender)
                    if audio_path and os.path.exists(audio_path):
                        # Convert WAV to MP3 if possible, otherwise return WAV
                        pydub = _get_pydub()
                        if pydub['available']:
                            try:
                                audio = pydub['AudioSegment'].from_wav(audio_path)
                                mp3_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                                mp3_path.close()
                                audio.export(mp3_path.name, format="mp3")
                                os.unlink(audio_path)
                                return mp3_path.name
                            except:
                                return audio_path
                        else:
                            return audio_path
                except Exception as e:
                    # Fallback to gTTS
                    pass
            # Use gTTS directly if ffmpeg not available (for non-English languages or when prefer_gtts is True)
            if prefer_gtts or lang != 'en':
                tts_lang_direct = get_tts_language_code(lang)
                tts = gTTS(text=text, lang=tts_lang_direct, slow=slow)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tts.save(tmp_file.name)
                return tmp_file.name
            else:
                st.warning(f"Audio processing unavailable: {ffmpeg_message}")
                return None
        
        # Get emotion parameters
        params = EMOTION_PARAMS.get(emotion, EMOTION_PARAMS["neutral"])
        
        # Generate base TTS with voice selection
        # Use gTTS for translated text (prefer_gtts=True) or non-English languages
        audio_file = generate_speech_with_voice(text, voice_gender, lang, use_pyttsx3, prefer_gtts=prefer_gtts)
        if not audio_file:
            return None
        
        # Determine file format and load audio
        pydub = _get_pydub()
        if not pydub['available']:
            st.warning("Audio processing (pydub) is not available. Returning audio file without emotion modulation.")
            return audio_file
        
        try:
            AudioSegment = pydub['AudioSegment']
            if audio_file.endswith('.wav'):
                audio = AudioSegment.from_wav(audio_file)
            elif audio_file.endswith('.mp3'):
                audio = AudioSegment.from_mp3(audio_file)
            else:
                # Try to auto-detect
                audio = AudioSegment.from_file(audio_file)
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "WinError 2" in error_msg or "cannot find the file" in error_msg.lower():
                st.error(f"""
                **FFmpeg Error: {error_msg}**
                
                FFmpeg is required for audio processing but cannot be found. Please:
                1. Install FFmpeg (see instructions in the sidebar or SETUP_FFMPEG.md)
                2. Add FFmpeg to your system PATH
                3. Restart this Streamlit app
                
                For detailed installation instructions, check SETUP_FFMPEG.md in the project directory.
                """)
            else:
                st.error(f"Error loading audio file: {error_msg}")
            # Clean up temp file
            try:
                os.unlink(audio_file)
            except:
                pass
            return None
        
        # Apply speed adjustment
        if params["speed"] != 1.0:
            # Speed up or slow down
            if params["speed"] > 1.0:
                # Use speedup for faster playback
                if pydub['speedup'] is not None:
                    audio = pydub['speedup'](audio, playback_speed=params["speed"])
                else:
                    # Fallback: adjust frame rate
                    original_frame_rate = audio.frame_rate
                    new_sample_rate = int(original_frame_rate * params["speed"])
                    audio = audio._spawn(
                        audio.raw_data,
                        overrides={"frame_rate": new_sample_rate}
                    )
                    audio = audio.set_frame_rate(original_frame_rate)
            else:
                # Slow down by changing frame rate and then resampling
                original_frame_rate = audio.frame_rate
                new_sample_rate = int(original_frame_rate * params["speed"])
                audio = audio._spawn(
                    audio.raw_data,
                    overrides={"frame_rate": new_sample_rate}
                )
                # Resample back to original frame rate to maintain quality
                audio = audio.set_frame_rate(original_frame_rate)
        
        # Apply volume adjustment
        if params["volume"] != 1.0:
            volume_change = 20 * np.log10(params["volume"])  # Convert to dB
            audio = audio + volume_change
        
        # Apply pitch adjustment (simplified)
        if params["pitch_shift"] != 1.0:
            audio = adjust_audio_pitch(audio, params["pitch_shift"])
        
        # Normalize audio
        if pydub['normalize'] is not None:
            audio = pydub['normalize'](audio)
        
        # Save processed audio
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        output_path.close()
        audio.export(output_path.name, format="mp3")
        
        # Clean up original temp file
        try:
            os.unlink(audio_file)
        except:
            pass
        
        return output_path.name
        
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

def main():
    # Title and header
    st.title("🎙️ Emotion-Aware Text-to-Speech Tutor (EA-TTS)")
    st.markdown("### Transform educational text into expressive, emotion-aware speech")
    st.markdown("📄 **Document Support:** Upload PDF, DOCX, TXT, or MD files | 🌍 **Translation:** Translate to any language | 📊 **Export:** Generate PDF reports")
    
    # Check ffmpeg availability at startup (with error handling)
    ffmpeg_message = ""
    try:
        ffmpeg_available, ffmpeg_message = check_ffmpeg()
        if not ffmpeg_available:
            # Show a less alarming message - FFmpeg is optional
            st.info("ℹ️ **Note:** FFmpeg not detected. Basic text-to-speech works fine! FFmpeg is only needed for advanced audio effects (pitch/speed adjustments).")
        else:
            st.success("✅ FFmpeg detected - Full audio processing available!")
    except Exception as e:
        # If FFmpeg check fails, assume it's not available (common on Streamlit Cloud)
        ffmpeg_available = False
        ffmpeg_message = "FFmpeg enables advanced audio processing features."
        st.info("ℹ️ **Note:** Basic text-to-speech works without FFmpeg. Advanced audio features require FFmpeg.")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Show ffmpeg status in sidebar
        if ffmpeg_available:
            st.success("✅ FFmpeg installed - Full features")
        else:
            st.info("ℹ️ FFmpeg optional - Basic TTS works")
        
        # Language selection for TTS
        st.markdown("### 🌍 Language Settings")
        
        # Translation toggle - store in session state
        if 'enable_translation' not in st.session_state:
            st.session_state.enable_translation = False
        
        enable_translation = False
        if TRANSLATOR_AVAILABLE:
            enable_translation = st.checkbox(
                "🔀 Enable Translation",
                value=st.session_state.enable_translation,
                help="Translate text to another language before generating speech (like Google Translate)",
                key="translation_checkbox"
            )
            # Update session state
            st.session_state.enable_translation = enable_translation
        else:
            st.info("💡 **Translation**: Install `deep-translator` for translation support")
            st.info("```bash\npip install deep-translator\n```")
            enable_translation = False
            st.session_state.enable_translation = False
        
        # Source language (for translation) - store in session state
        if 'source_language' not in st.session_state:
            st.session_state.source_language = "auto"
        
        source_language = "auto"
        if enable_translation:
            # Get index for selectbox
            source_options = ["auto", "en", "hi", "es", "fr", "de", "zh", "ja", "ko", "ru", "ar", "pt", "it", "nl"]
            try:
                source_index = source_options.index(st.session_state.source_language)
            except:
                source_index = 0
            
            source_language = st.selectbox(
                "Source Language (Auto-detect)",
                source_options,
                index=source_index,
                format_func=lambda x: {
                    "auto": "Auto-detect",
                    "en": "English",
                    "hi": "Hindi",
                    "es": "Spanish",
                    "fr": "French",
                    "de": "German",
                    "zh": "Chinese",
                    "ja": "Japanese",
                    "ko": "Korean",
                    "ru": "Russian",
                    "ar": "Arabic",
                    "pt": "Portuguese",
                    "it": "Italian",
                    "nl": "Dutch"
                }.get(x, x),
                key="source_language_select"
            )
            # Update session state
            st.session_state.source_language = source_language
        
        # Language options for translation
        language_options = {
            "en": "English",
            "hi": "Hindi",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "ar": "Arabic",
            "pt": "Portuguese",
            "it": "Italian",
            "nl": "Dutch",
            "tr": "Turkish",
            "pl": "Polish",
            "sv": "Swedish",
            "da": "Danish",
            "fi": "Finnish",
            "no": "Norwegian",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "ms": "Malay"
        }
        
        # Target language for TTS (if translation is enabled, this is the translation target)
        # Store in session state
        if 'target_lang_code' not in st.session_state:
            st.session_state.target_lang_code = "es"  # Default to Spanish for testing
        
        if enable_translation:
            # Get index for selectbox
            lang_keys = list(language_options.keys())
            try:
                lang_index = lang_keys.index(st.session_state.target_lang_code)
            except:
                lang_index = 2  # Default to Spanish (index 2)
            
            target_lang_code = st.selectbox(
                "Target Language (for translation & speech)",
                lang_keys,
                format_func=lambda x: language_options.get(x, x),
                index=lang_index,
                key="target_language_select"
            )
            # Update session state
            st.session_state.target_lang_code = target_lang_code
            language = target_lang_code  # Use translated language for TTS
        else:
            # Original language selection without translation
            if 'speech_language' not in st.session_state:
                st.session_state.speech_language = "en"
            
            lang_options = ["en", "hi", "es", "fr", "de"]
            try:
                lang_index = lang_options.index(st.session_state.speech_language)
            except:
                lang_index = 0
            
            language = st.selectbox(
                "Speech Language",
                lang_options,
                format_func=lambda x: {
                    "en": "English",
                    "hi": "Hindi",
                    "es": "Spanish",
                    "fr": "French",
                    "de": "German"
                }.get(x, x),
                index=lang_index,
                key="speech_language_select"
            )
            st.session_state.speech_language = language
            target_lang_code = language  # Set default for consistency
            st.session_state.target_lang_code = target_lang_code
        
        # Voice speed (base speed)
        base_speed = st.selectbox(
            "Base Speech Speed",
            ["Normal", "Slow", "Fast"],
            index=0
        )
        
        # Voice selection
        st.markdown("---")
        st.markdown("### 🎤 Voice Settings")
        
        # Voice gender selection
        if PYTTSX3_AVAILABLE:
            voice_gender = st.radio(
                "Voice Gender",
                ["Female", "Male"],
                index=0,
                horizontal=True,
                help="Select male or female voice for speech generation (requires pyttsx3)"
            )
            use_pyttsx3 = True
            
            # Show available voices if pyttsx3 is available
            try:
                available_voices = get_available_voices()
                if available_voices:
                    with st.expander("👀 Available Voices"):
                        for voice in available_voices:
                            gender_icon = "👩" if voice['gender'] == 'female' else "👨"
                            st.write(f"{gender_icon} {voice['name']} ({voice['gender']})")
            except Exception as e:
                pass
        else:
            st.info("💡 **Voice Selection**: Install `pyttsx3` for male/female voice options")
            st.info("```bash\npip install pyttsx3\n```")
            voice_gender = "Female"  # Default
            use_pyttsx3 = False
        
        st.markdown("---")
        st.markdown("### 🎭 Emotion Mapping")
        st.markdown("""
        | Emotion | Pitch | Speed | Tone |
        |---------|-------|-------|------|
        | Joy | +5% | Fast | Energetic |
        | Sadness | -5% | Slow | Soft |
        | Anger | +10% | Fast | Firm |
        | Fear | -10% | Slow | Low |
        | Surprise | +7% | Fast | Bright |
        | Neutral | 0% | Normal | Balanced |
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Text")
        input_method = st.radio(
            "Input Method",
            ["Paste Text", "Upload File"],
            horizontal=True
        )
        
        text_input = ""
        
        if input_method == "Paste Text":
            text_input = st.text_area(
                "Enter your educational text here:",
                height=300,
                placeholder="Type or paste your text here...\n\nExample: The discovery of gravity was a momentous occasion in scientific history. Scientists were thrilled! However, the initial reactions were mixed with surprise and curiosity."
            )
        else:
            # Determine supported file types
            file_types = ['txt', 'md']
            file_labels = ["Text files (.txt, .md)"]
            
            if PDFPLUMBER_AVAILABLE or PYPDF2_AVAILABLE:
                file_types.append('pdf')
                file_labels.append("PDF files (.pdf)")
            
            if DOCX_AVAILABLE:
                file_types.append('docx')
                file_labels.append("Word documents (.docx)")
            
            file_type_label = ", ".join(file_labels)
            
            uploaded_file = st.file_uploader(
                f"Upload a document ({file_type_label})",
                type=file_types,
                help=f"Supported formats: {', '.join(file_types).upper()}"
            )
            if uploaded_file is not None:
                with st.spinner(f"Extracting text from {uploaded_file.name}..."):
                    text_input = extract_text_from_file(uploaded_file)
                    
                if text_input:
                    st.success(f"✅ Successfully extracted text from {uploaded_file.name}")
                    # Show preview of extracted text
                    preview_length = 500
                    if len(text_input) > preview_length:
                        st.text_area(
                            f"Extracted text preview (first {preview_length} characters):",
                            text_input[:preview_length] + "...",
                            height=200,
                            disabled=True
                        )
                        st.info(f"📄 Full text extracted: {len(text_input)} characters. Click 'Analyze Emotions' to process.")
                    else:
                        st.text_area("Extracted text:", text_input, height=200)
                else:
                    st.error(f"❌ Failed to extract text from {uploaded_file.name}")
                    text_input = ""
    
    with col2:
        st.subheader("🎭 Emotion Analysis")
        
        if st.button("🔍 Analyze Emotions", type="primary", use_container_width=True):
            # Load emotion model on demand to avoid slow startups
            with st.spinner("Loading emotion detection model..."):
                try:
                    classifier = load_emotion_model()
                except Exception as e:
                    classifier = None
                    st.error(f"Failed to load emotion model: {e}")
            if classifier is None:
                st.error("Emotion model is unavailable right now. Please check your internet connection and try again.")
                st.stop()
            if not text_input or len(text_input.strip()) == 0:
                st.warning("Please enter some text first!")
            else:
                # Get translation settings from session state
                enable_translation = st.session_state.get('enable_translation', False)
                source_language = st.session_state.get('source_language', 'auto')
                target_lang_code = st.session_state.get('target_lang_code', 'es')
                
                # Split into sentences
                sentences = split_into_sentences(text_input)
                
                if len(sentences) == 0:
                    st.warning("No sentences found in the text.")
                else:
                    # Translate text if translation is enabled
                    translated_sentences = []
                    if enable_translation and TRANSLATOR_AVAILABLE:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        status_text.text(f"Translating from {language_options.get(source_language if source_language != 'auto' else 'auto', 'Auto-detect')} to {language_options.get(target_lang_code, target_lang_code)}...")
                        
                        # Translate entire text first for better context (like Google Translate does)
                        # This ensures proper context and accurate translation
                        full_text = " ".join(sentences)
                        
                        # Show what's being translated
                        with st.expander("🔍 Translation Details", expanded=False):
                            st.write(f"**Original text:** {full_text[:200]}...")
                            st.write(f"**Source:** {language_options.get(source_language if source_language != 'auto' else 'en', 'Auto-detect')}")
                            st.write(f"**Target:** {language_options.get(target_lang_code, target_lang_code)}")
                        
                        translated_full, error = translate_text(full_text, target_lang_code, source_language)
                        
                        # Verify translation result immediately
                        if translated_full == full_text or (translated_full.lower().strip() == full_text.lower().strip()):
                            st.error(f"❌ **Translation failed:** Output is identical to input!")
                            st.error(f"Original: '{full_text[:100]}'")
                            st.error(f"Translated: '{translated_full[:100]}'")
                            if error:
                                st.error(f"Error message: {error}")
                            st.warning("⚠️ **Possible issues:**")
                            st.warning("1. Source and target language might be the same")
                            st.warning("2. Text might already be in the target language")
                            st.warning("3. Translation API might be unavailable")
                        
                        if error and error != "":
                            # If full translation failed, try sentence by sentence
                            st.warning(f"⚠️ Full text translation warning: {error}")
                            status_text.text("Translating sentence by sentence...")
                            translated_sentences = []
                            for i, sentence in enumerate(sentences):
                                if sentence.strip():  # Only translate non-empty sentences
                                    translated, err = translate_text(sentence, target_lang_code, source_language)
                                    if err and err != "":
                                        st.warning(f"⚠️ Sentence {i+1} translation: {err}")
                                    translated_sentences.append(translated if translated else sentence)
                                else:
                                    translated_sentences.append(sentence)
                                progress_bar.progress((i + 1) / len(sentences) * 0.5)
                        else:
                            # Full text translation succeeded
                            # Split translated text back into sentences for individual processing
                            translated_sentences = split_into_sentences(translated_full)
                            
                            # Ensure we have same number of sentences
                            # If sentence count differs, translate individually to maintain structure
                            if len(translated_sentences) != len(sentences):
                                status_text.text("Adjusting sentence boundaries...")
                                # Translate each sentence individually but with context
                                translated_sentences = []
                                for i, sentence in enumerate(sentences):
                                    if sentence.strip():
                                        translated, err = translate_text(sentence, target_lang_code, source_language)
                                        translated_sentences.append(translated if translated else sentence)
                                    else:
                                        translated_sentences.append(sentence)
                                    progress_bar.progress((i + 1) / len(sentences) * 0.5)
                            else:
                                progress_bar.progress(0.5)
                        
                        # Store translated text in session state
                        st.session_state.translated_text = " ".join(translated_sentences)
                        st.session_state.source_lang_used = source_language
                        st.session_state.target_lang_used = target_lang_code
                        
                        # Show translation preview with verification
                        if translated_sentences and len(translated_sentences) > 0:
                            preview_text = " ".join(translated_sentences[:3])  # First 3 sentences
                            if len(translated_sentences) > 3:
                                preview_text += "..."
                            
                            # Verify translation is different
                            original_preview = " ".join(sentences[:3])
                            if original_preview.lower().strip() != preview_text.lower().strip():
                                st.success(f"✅ Translation successful to {language_options.get(target_lang_code, target_lang_code)}!")
                                st.info(f"📝 Translated text preview: {preview_text[:200]}...")
                            else:
                                st.warning(f"⚠️ Translation appears unchanged. Original: '{original_preview[:50]}' → Translated: '{preview_text[:50]}'")
                                st.error("Translation may not have worked. Please check your language settings.")
                    else:
                        translated_sentences = sentences
                        st.session_state.translated_text = None
                    
                    # Store results in session state
                    st.session_state.sentences = sentences
                    st.session_state.translated_sentences = translated_sentences if enable_translation else None
                    st.session_state.emotions = []
                    
                    # Analyze each sentence (use original text for emotion detection - works better)
                    if enable_translation:
                        status_text.text("Analyzing emotions in original text...")
                    else:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                    
                    for i, sentence in enumerate(sentences):
                        status_text.text(f"Analyzing sentence {i+1}/{len(sentences)}...")
                        emotion, score = detect_emotion(sentence, classifier)
                        emotion_data = {
                            'sentence': sentence,
                            'emotion': emotion,
                            'score': score
                        }
                        # Add translated sentence if available
                        if enable_translation and translated_sentences:
                            emotion_data['translated_sentence'] = translated_sentences[i]
                        st.session_state.emotions.append(emotion_data)
                        if enable_translation:
                            progress_bar.progress(0.5 + ((i + 1) / len(sentences) * 0.5))  # Second half for analysis
                        else:
                            progress_bar.progress((i + 1) / len(sentences))
                    
                    status_text.text("Analysis complete!")
                    progress_bar.empty()
                    
                    # Show translation info if enabled
                    if enable_translation and TRANSLATOR_AVAILABLE and translated_sentences:
                        # Verify translation is different from original
                        original_text = " ".join(sentences)
                        translated_text_full = " ".join(translated_sentences)
                        
                        # CRITICAL: Verify translation actually happened
                        is_translated = original_text.lower().strip() != translated_text_full.lower().strip()
                        
                        # Show clear success/failure message
                        st.markdown("---")
                        if is_translated:
                            st.success(f"🎉 **TRANSLATION SUCCESSFUL!** Text translated to **{language_options.get(target_lang_code, target_lang_code)}**")
                            st.balloons()  # Celebrate!
                        else:
                            st.error(f"❌ **TRANSLATION FAILED!** Text is identical to original.")
                            st.error(f"**This means translation didn't work!**")
                            st.warning("**Troubleshooting:**")
                            st.warning(f"1. Source: {language_options.get(source_language if source_language != 'auto' else 'en', 'Auto-detect')}")
                            st.warning(f"2. Target: {language_options.get(target_lang_code, target_lang_code)}")
                            st.warning("3. Make sure source and target are **DIFFERENT** languages")
                            st.warning("4. Check internet connection")
                        
                        # Show side-by-side comparison - ALWAYS show when translation is enabled
                        st.markdown("### 📊 Translation Comparison")
                        st.markdown("**Compare original text with translated text:**")
                        col_orig, col_trans = st.columns(2)
                        
                        with col_orig:
                            st.markdown(f"**📝 Original ({language_options.get(source_language if source_language != 'auto' else 'en', 'English')}):**")
                            st.text_area("Original:", original_text, height=300, key="original_text_display", disabled=True, label_visibility="collapsed")
                            st.caption(f"📊 {len(original_text.split())} words")
                        
                        with col_trans:
                            if is_translated:
                                st.markdown(f"**🌍 Translated ({language_options.get(target_lang_code, target_lang_code)}) ✅:**")
                                st.success("✅ **This translated text will be used for speech!**")
                            else:
                                st.markdown(f"**🌍 Translated ({language_options.get(target_lang_code, target_lang_code)}) ❌:**")
                                st.error("❌ **Translation failed - text is identical!**")
                            st.text_area("Translated:", translated_text_full, height=300, key="translated_text_display", disabled=True, label_visibility="collapsed")
                            st.caption(f"📊 {len(translated_text_full.split())} words")
                        
                        # Show what will be spoken
                        st.markdown("---")
                        if is_translated:
                            st.success(f"✅ **When you click 'Generate Speech', it will speak:**")
                            st.info(f"**'{translated_text_full[:200]}...'**")
                            st.success(f"**In {language_options.get(target_lang_code, target_lang_code)} language**")
                        else:
                            st.error(f"❌ **Translation failed! Speech will NOT be in {language_options.get(target_lang_code, target_lang_code)}**")
                            st.error("Please fix translation settings above.")
                        
                        # Store source and target language info
                        st.session_state.source_lang_display = language_options.get(source_language if source_language != 'auto' else 'en', 'English')
                        st.session_state.target_lang_display = language_options.get(target_lang_code, target_lang_code)
                        st.session_state.translation_verified = is_translated
    
    # Display results
    if 'emotions' in st.session_state and len(st.session_state.emotions) > 0:
        st.markdown("---")
        
        # Results header with export options
        st.subheader("📊 Analysis Results")
        
        # Create results table data first
        results_data = []
        for item in st.session_state.emotions:
            params = EMOTION_PARAMS.get(item['emotion'], EMOTION_PARAMS["neutral"])
            # Show translated text if available, otherwise show original
            display_text = item.get('translated_sentence', item['sentence'])
            results_data.append({
                "Text": display_text[:100] + "..." if len(display_text) > 100 else display_text,
                "Emotion": item['emotion'].title(),
                "Confidence": f"{item['score']:.2%}",
                "Pitch": f"{params['pitch_shift']*100:.0f}%",
                "Speed": f"{params['speed']:.2f}x",
                "Tone": params['tone']
            })
            
            # Show original text in tooltip if translated
            if 'translated_sentence' in item:
                item['display_text'] = item['translated_sentence']
            else:
                item['display_text'] = item['sentence']
        
        # Export options
        export_col1, export_col2 = st.columns([1, 1])
        with export_col1:
            if REPORTLAB_AVAILABLE:
                # Generate or retrieve cached PDF report
                pdf_cache_key = f"pdf_report_{len(st.session_state.emotions)}"
                if pdf_cache_key not in st.session_state:
                    # Generate PDF report (cached per emotion count)
                    pdf_bytes = generate_pdf_report(st.session_state.emotions)
                    if pdf_bytes:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"emotion_analysis_report_{timestamp}.pdf"
                        st.session_state[pdf_cache_key] = pdf_bytes
                        st.session_state[f"{pdf_cache_key}_filename"] = filename
                
                # Download button
                if pdf_cache_key in st.session_state:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=st.session_state[pdf_cache_key],
                        file_name=st.session_state[f"{pdf_cache_key}_filename"],
                        mime="application/pdf",
                        use_container_width=True,
                        help="Download a formatted PDF report with analysis results"
                    )
            else:
                st.info("📄 PDF export requires reportlab library")
        
        with export_col2:
            # Export as CSV
            try:
                import pandas as pd
                df = pd.DataFrame(results_data)
                csv = df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_filename = f"emotion_analysis_{timestamp}.csv"
                st.download_button(
                    label="📊 Download CSV",
                    data=csv,
                    file_name=csv_filename,
                    mime="text/csv",
                    use_container_width=True,
                    help="Download analysis results as CSV file"
                )
            except ImportError:
                st.info("📊 CSV export requires pandas library")
        
        # Display results table
        st.dataframe(results_data, use_container_width=True, hide_index=True)
        
        # Generate speech button
        st.markdown("---")
        st.subheader("🎵 Generate Emotional Speech")
        
        col_gen1, col_gen2 = st.columns([3, 1])
        
        with col_gen1:
            generate_option = st.radio(
                "Generate speech for:",
                ["All sentences (combined)", "Individual sentences"],
                horizontal=True
            )
        
        with col_gen2:
            if st.button("🎤 Generate Speech", type="primary", use_container_width=True):
                # Get translation settings from session state
                enable_translation = st.session_state.get('enable_translation', False)
                target_lang_code = st.session_state.get('target_lang_code', 'en')
                language = target_lang_code if enable_translation else st.session_state.get('speech_language', 'en')
                
                if generate_option == "All sentences (combined)":
                    # Use translated text if available, otherwise use original
                    # Check if translation is enabled and translated text exists
                    has_translated_text = ('translated_text' in st.session_state and 
                                          st.session_state.translated_text and 
                                          st.session_state.translated_text.strip())
                    
                    if enable_translation:
                        # Translation is enabled - check if we have translated text
                        if has_translated_text:
                            full_text = st.session_state.translated_text
                            st.success(f"🔀 **Generating speech from TRANSLATED text** ({language_options.get(target_lang_code, target_lang_code)})")
                            st.info(f"✅ Using translated text: **'{full_text[:100]}...'**")
                        else:
                            # Translation enabled but no translated text - show helpful error
                            full_text = " ".join([item['sentence'] for item in st.session_state.emotions])
                            st.error(f"❌ **Translation is enabled but no translated text found!**")
                            st.warning(f"⚠️ **Please click 'Analyze Emotions' first** to translate the text.")
                            st.info(f"📝 Using original text for now: **'{full_text[:100]}...'**")
                            st.error(f"**Speech will be in original language, NOT {language_options.get(target_lang_code, target_lang_code)}!**")
                    else:
                        # Translation not enabled
                        full_text = " ".join([item['sentence'] for item in st.session_state.emotions])
                        st.info(f"📝 Using original text (translation not enabled in sidebar)")
                    
                    # Use dominant emotion or neutral
                    dominant_emotion = max(st.session_state.emotions, key=lambda x: x['score'])['emotion']
                    
                    with st.spinner("Generating emotional speech..."):
                        # Show what text will be spoken
                        if enable_translation and 'translated_text' in st.session_state and st.session_state.translated_text:
                            st.info(f"🔊 **Generating speech in {language_options.get(target_lang_code, target_lang_code)}**")
                            st.caption(f"📝 Text to speak: {full_text[:200]}...")
                        
                        # Use gTTS for translated text (better language support)
                        # Ensure we use the correct language code for gTTS
                        tts_lang = target_lang_code if enable_translation else language
                        prefer_gtts = enable_translation or (language != 'en')  # Use gTTS for non-English
                        
                        audio_path = generate_emotional_speech(
                            full_text,
                            dominant_emotion,
                            lang=tts_lang,  # Use target language for TTS
                            slow=(base_speed == "Slow"),
                            voice_gender=voice_gender.lower(),
                            use_pyttsx3=use_pyttsx3 and not enable_translation and language == 'en',  # Only use pyttsx3 for English without translation
                            prefer_gtts=prefer_gtts
                        )
                    
                    if audio_path:
                        # Determine audio format
                        audio_format = 'audio/mp3' if audio_path.endswith('.mp3') else 'audio/wav'
                        file_ext = 'mp3' if audio_path.endswith('.mp3') else 'wav'
                        st.audio(audio_path, format=audio_format)
                        with open(audio_path, 'rb') as f:
                            st.download_button(
                                label="📥 Download Audio",
                                data=f.read(),
                                file_name=f"emotion_aware_speech.{file_ext}",
                                mime=audio_format
                            )
                else:
                    # Generate for each sentence
                    # Get translation settings from session state
                    enable_translation = st.session_state.get('enable_translation', False)
                    target_lang_code = st.session_state.get('target_lang_code', 'en')
                    language = target_lang_code if enable_translation else st.session_state.get('speech_language', 'en')
                    
                    # Check if we have translated sentences
                    has_translated_sentences = ('translated_sentences' in st.session_state and 
                                               st.session_state.translated_sentences)
                    
                    if enable_translation:
                        if has_translated_sentences:
                            st.success(f"🔀 **Generating speech from TRANSLATED text** ({language_options.get(target_lang_code, target_lang_code)})")
                            st.info(f"✅ Using translated sentences")
                        else:
                            st.error(f"❌ **Translation is enabled but no translated sentences found!**")
                            st.warning(f"⚠️ **Please click 'Analyze Emotions' first** to translate the text.")
                            st.error(f"**Speech will be in original language, NOT {language_options.get(target_lang_code, target_lang_code)}!**")
                    else:
                        st.info(f"📝 Using original sentences (translation not enabled in sidebar)")
                    
                    audio_files = []
                    for i, item in enumerate(st.session_state.emotions):
                        # Use translated text if available
                        if enable_translation and has_translated_sentences and 'translated_sentence' in item:
                            text_to_speak = item['translated_sentence']
                            if i == 0:  # Show example for first sentence
                                st.caption(f"📝 Example: Speaking translated text: '{text_to_speak[:80]}...'")
                        else:
                            text_to_speak = item['sentence']
                            if i == 0:  # Show example for first sentence
                                st.caption(f"📝 Example: Speaking original text: '{text_to_speak[:80]}...'")
                        
                        with st.spinner(f"Generating speech for sentence {i+1}/{len(st.session_state.emotions)}..."):
                            # Use gTTS for translated text (better language support)
                            prefer_gtts = enable_translation
                            tts_lang = target_lang_code if enable_translation else language
                            audio_path = generate_emotional_speech(
                                text_to_speak,
                                item['emotion'],
                                lang=tts_lang,  # Use target language
                                slow=(base_speed == "Slow"),
                                voice_gender=voice_gender.lower(),
                                use_pyttsx3=use_pyttsx3 and not enable_translation and tts_lang == 'en',  # Don't use pyttsx3 for translated text
                                prefer_gtts=prefer_gtts
                            )
                            if audio_path:
                                audio_files.append((audio_path, item))
                    
                    # Display all audio players
                    for idx, (audio_path, item) in enumerate(audio_files):
                        # Show translated text if available
                        display_text = item.get('translated_sentence', item['sentence'])
                        st.markdown(f"**{item['emotion'].title()}** - {display_text[:50]}...")
                        # Show original text if translated
                        if 'translated_sentence' in item:
                            st.caption(f"Original: {item['sentence'][:50]}...")
                        # Determine audio format
                        audio_format = 'audio/mp3' if audio_path.endswith('.mp3') else 'audio/wav'
                        file_ext = 'mp3' if audio_path.endswith('.mp3') else 'wav'
                        st.audio(audio_path, format=audio_format)
                        
                        # Download button for each audio
                        with open(audio_path, 'rb') as f:
                            st.download_button(
                                label=f"📥 Download ({item['emotion'].title()})",
                                data=f.read(),
                                file_name=f"speech_{item['emotion']}_{idx+1}.{file_ext}",
                                mime=audio_format,
                                key=f"download_{idx}"
                            )
        
        # Cleanup temporary files (optional - files will be cleaned on app restart)
        # Note: In production, implement proper cleanup mechanism

if __name__ == "__main__":
    import sys
    # Check if running with streamlit
    if 'streamlit' not in sys.modules:
        print("\n" + "="*60)
        print("⚠️  WARNING: This is a Streamlit application!")
        print("="*60)
        print("\nPlease run this app using the following command:")
        print("  streamlit run app.py")
        print("\nRunning with 'python app.py' will cause errors.")
        print("="*60 + "\n")
        sys.exit(1)
    try:
        main()
    except Exception as e:
        # Ensure app doesn't crash completely - show error to user
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page or check the logs for more details.")
        import traceback
        st.code(traceback.format_exc())

