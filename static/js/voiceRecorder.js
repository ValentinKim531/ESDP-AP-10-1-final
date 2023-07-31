import { handleFileUpload } from './fileSharing.js';

let mediaRecorder;
let recordedChunks = [];

async function startRecording(centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = function (event) {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = async function() {
        const blob = new Blob(recordedChunks, { type: 'audio/mpeg' });
        recordedChunks = [];

        handleFileUpload(blob, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl);
    };

    mediaRecorder.start();
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}

export { startRecording, stopRecording };
