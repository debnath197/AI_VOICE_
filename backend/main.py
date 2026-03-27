<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Live Voice Answer App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            text-align: center;
            background: #f7f7f7;
        }

        h1 {
            margin-bottom: 20px;
        }

        button {
            padding: 12px 20px;
            margin: 10px 5px;
            cursor: pointer;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            background: #222;
            color: white;
        }

        button:hover {
            opacity: 0.9;
        }

        textarea {
            width: 100%;
            min-height: 120px;
            margin-top: 20px;
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
            resize: vertical;
        }

        #answer {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ccc;
            min-height: 80px;
            background: white;
            font-size: 18px;
            text-align: left;
            white-space: pre-wrap;
            border-radius: 8px;
        }

        .status {
            margin-top: 15px;
            font-size: 15px;
            color: #444;
        }

        .hint {
            font-size: 14px;
            color: #666;
            margin-top: 8px;
        }
    </style>
</head>
<body>

    <h1>🎤 Live Voice Answer App</h1>

    <button id="startBtn">🎙 Start Speaking</button>
    <button id="stopBtn">⏹ Stop</button>
    <button id="askBtn">💬 Ask from Text</button>

    <div class="status" id="status">Status: Ready</div>
    <div class="hint">Tip: Click Start Speaking and speak immediately in Chrome.</div>

    <h3>Your Speech / Question:</h3>
    <textarea id="transcript" placeholder="Speak or type your question here..."></textarea>

    <h3>Answer:</h3>
    <div id="answer">Waiting for your question...</div>

    <script>
        const startBtn = document.getElementById("startBtn");
        const stopBtn = document.getElementById("stopBtn");
        const askBtn = document.getElementById("askBtn");
        const transcriptBox = document.getElementById("transcript");
        const answerBox = document.getElementById("answer");
        const statusBox = document.getElementById("status");

        const API_BASE = window.location.origin;
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        let recognition = null;
        let isListening = false;
        let finalTranscript = "";

        function speakText(text) {
            window.speechSynthesis.cancel();
            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = "en-US";
            speech.rate = 1;
            speech.pitch = 1;
            window.speechSynthesis.speak(speech);
        }

        async function askBackend(question) {
            if (!question.trim()) {
                answerBox.innerText = "⚠️ Please say or type a question first.";
                return;
            }

            answerBox.innerText = "⏳ Thinking...";
            statusBox.innerText = "Status: Getting AI answer...";

            try {
                const response = await fetch(`${API_BASE}/ask`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: question.trim() })
                });

                const data = await response.json();

                if (data.answer) {
                    answerBox.innerText = data.answer;
                    statusBox.innerText = "Status: Answer received";
                    speakText(data.answer);
                } else {
                    answerBox.innerText = "❌ No answer received.";
                    statusBox.innerText = "Status: No answer";
                }

            } catch (error) {
                console.error("Fetch Error:", error);
                answerBox.innerText = "❌ Failed to get answer from backend.";
                statusBox.innerText = "Status: Backend request failed";
            }
        }

        function setupRecognition() {
            if (!SpeechRecognition) {
                statusBox.innerText = "Status: Speech Recognition not supported. Use Google Chrome.";
                return;
            }

            recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = true;
            recognition.continuous = false;
            recognition.maxAlternatives = 1;

            recognition.onstart = () => {
                isListening = true;
                finalTranscript = "";
                transcriptBox.value = "";
                answerBox.innerText = "🎧 Listening... Speak now.";
                statusBox.innerText = "Status: Listening...";
            };

            recognition.onresult = (event) => {
                let tempTranscript = "";

                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;

                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + " ";
                    } else {
                        tempTranscript += transcript;
                    }
                }

                transcriptBox.value = (finalTranscript + tempTranscript).trim();
                statusBox.innerText = "Status: Speech detected";
            };

            recognition.onerror = (event) => {
                console.error("Speech Recognition Error:", event.error);
                isListening = false;

                if (event.error === "no-speech") {
                    answerBox.innerText = "⚠️ No speech detected. Click Start Speaking and speak immediately.";
                    statusBox.innerText = "Status: No speech detected";
                } else if (event.error === "not-allowed") {
                    answerBox.innerText = "⚠️ Microphone permission denied. Please allow microphone access in Chrome.";
                    statusBox.innerText = "Status: Mic permission denied";
                } else if (event.error === "audio-capture") {
                    answerBox.innerText = "⚠️ No microphone found. Please check your microphone.";
                    statusBox.innerText = "Status: No microphone";
                } else {
                    answerBox.innerText = "❌ Speech Recognition Error: " + event.error;
                    statusBox.innerText = "Status: Speech error - " + event.error;
                }
            };

            recognition.onend = () => {
                isListening = false;
                statusBox.innerText = "Status: Listening stopped";

                const question = transcriptBox.value.trim();

                if (question.length > 0) {
                    askBackend(question);
                }
            };
        }

        setupRecognition();

        startBtn.addEventListener("click", () => {
            if (!recognition) {
                setupRecognition();
            }

            try {
                window.speechSynthesis.cancel();
                transcriptBox.value = "";
                finalTranscript = "";
                answerBox.innerText = "🎧 Preparing microphone...";
                statusBox.innerText = "Status: Starting microphone...";

                setTimeout(() => {
                    recognition.start();
                }, 300);

            } catch (e) {
                console.error("Recognition start issue:", e);
                statusBox.innerText = "Status: Could not start microphone";
            }
        });

        stopBtn.addEventListener("click", () => {
            if (recognition && isListening) {
                recognition.stop();
                statusBox.innerText = "Status: Stopped listening";
            }
        });

        askBtn.addEventListener("click", () => {
            askBackend(transcriptBox.value);
        });
    </script>

</body>
</html>
