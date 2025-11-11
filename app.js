document.addEventListener('DOMContentLoaded', () => {
    // Get references to all the HTML elements
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    const transcriptText = document.getElementById('transcriptText');
    const starScore = document.getElementById('starScore');
    const feedbackText = document.getElementById('feedbackText');
    const fillerList = document.getElementById('fillerList');

    // This is the URL of your local Python server
    const API_URL = 'http://127.0.0.1:5000/api/analyze';

    let mediaRecorder;
    let audioChunks = [];

    // --- 1. START RECORDING ---
    recordButton.addEventListener('click', async () => {
        try {
            // Get permission to use the microphone
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            // This runs when audio data is available
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            // This runs when the recorder is stopped
            mediaRecorder.onstop = sendAudioToServer;

            // Start recording
            mediaRecorder.start();
            
            // Update UI
            statusDiv.innerText = "Recording... Speak now.";
            recordButton.innerText = "Recording...";
            recordButton.classList.add('recording');
            recordButton.disabled = true;
            stopButton.disabled = false;
            resultsDiv.style.display = 'none'; // Hide old results

        } catch (error) {
            console.error('Error starting recording:', error);
            statusDiv.innerText = 'Error: Could not start recording. (Did you give permission?)';
        }
    });

    // --- 2. STOP RECORDING ---
    stopButton.addEventListener('click', () => {
        if (mediaRecorder) {
            mediaRecorder.stop(); // This will trigger the 'onstop' event
            
            // Update UI
            statusDiv.innerText = "Processing your answer... please wait.";
            recordButton.innerText = "Start Recording";
            recordButton.classList.remove('recording');
            recordButton.disabled = false;
            stopButton.disabled = true;
        }
    });

    // --- 3. SEND AUDIO TO PYTHON SERVER ---
    async function sendAudioToServer() {
        // Combine all audio chunks into one "blob"
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        audioChunks = []; // Clear for next recording

        // Use FormData to send the file to your Python backend
        const formData = new FormData();
        formData.append('audioFile', audioBlob, 'myAnswer.webm');

        try {
            statusDiv.innerText = "Uploading and Transcribing... (Whisper may take a moment)";

            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            statusDiv.innerText = "Analyzing feedback with AI...";
            const report = await response.json();

            // --- 4. DISPLAY THE FEEDBACK REPORT ---
            displayReport(report);

        } catch (error) {
            console.error('Error sending audio:', error);
            statusDiv.innerText = `Error: ${error.message}. (Is your Python 'app.py' server running?)`;
            recordButton.disabled = false;
        }
    }

    // --- 4. DISPLAY REPORT ON PAGE ---
    function displayReport(report) {
        // Show the results container
        resultsDiv.style.display = 'block';
        statusDiv.innerText = "Report complete! Record again?";

        // 1. Transcript
        transcriptText.innerText = report.transcript || "[No transcript available]";

        // 2. STAR Analysis
        if (report.starAnalysis) {
            starScore.innerText = report.starAnalysis.score || "?";
            feedbackText.innerText = report.starAnalysis.feedback || "[No feedback available]";
        }

        // 3. Filler Words
        fillerList.innerHTML = ''; // Clear the list
        if (report.fillerWords && Object.keys(report.fillerWords).length > 0) {
            for (const [word, count] of Object.entries(report.fillerWords)) {
                const li = document.createElement('li');
                li.innerText = `${word}: ${count}`;
                fillerList.appendChild(li);
            }
        } else {
            const li = document.createElement('li');
            li.innerText = "No common fillers detected. Great job!";
            li.style.color = "#27ae60"; // Green color
            li.style.backgroundColor = "#eaf8f1";
            fillerList.appendChild(li);
        }
    }
});