\# 🖐️ Virtual Mouse using Hand Gestures



Control your computer mouse using just your webcam and hand gestures — no hardware needed!



\## ✨ Features



\- ☝️ \*\*Cursor Movement\*\* — Move cursor with your index finger

\- 🤏 \*\*Left Click\*\* — Pinch thumb and index finger together

\- ✌️ \*\*Scroll\*\* — Two fingers up, move hand up/down

\- 🎯 \*\*Smooth Tracking\*\* — Deque-based smoothing for jitter-free cursor

\- 📊 \*\*Real-time FPS\*\* — Performance monitoring

\- 🛡️ \*\*Fail-Safe\*\* — Move cursor to top-left corner to stop



\## 🛠️ Tech Stack



| Technology | Purpose |

|-----------|---------|

| Python 3.12 | Core language |

| OpenCV | Webcam feed \& drawing |

| MediaPipe | 21-point hand landmark detection |

| PyAutoGUI | Mouse control |

| NumPy | Coordinate interpolation |



\## 🚀 Installation



```bash

git clone https://github.com/YOUR\_USERNAME/virtual-mouse.git

cd virtual-mouse

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

python virtual\_mouse.py



