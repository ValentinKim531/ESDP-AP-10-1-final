import { handleFileUpload } from './fileSharing.js';
import { startRecording, stopRecording } from './voiceRecorder.js';

const roomId = JSON.parse(document.getElementById('room-id').textContent);
const chatThread = document.querySelector('#chat-thread');
const messageInput = document.querySelector('#chat-message-input');
const picker = document.querySelector('#emoji-picker');
const emojiButton = document.querySelector('#emoji-button');
const sendButton = document.getElementById("send-button");

function initializeUI() {
    toggleSendOrVoiceButton();
}

function toggleSendOrVoiceButton() {
    if (messageInput.value.trim() !== "") {
        voiceRecordingButton.style.display = "none";
        sendButton.style.display = "flex";
    } else {
        voiceRecordingButton.style.display = "flex";
        sendButton.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', initializeUI);

const voiceRecordingButton = document.createElement('button');
voiceRecordingButton.innerHTML = "🎙️";
voiceRecordingButton.id = "voice-recording-button";
voiceRecordingButton.classList.add('chat-file-label');
document.querySelector('.chat-message').appendChild(voiceRecordingButton);

let isRecording = false;
voiceRecordingButton.addEventListener('click', function() {
    if (sendButton.style.display === "none") {
        if (!isRecording) {
            startRecording(centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl);
            voiceRecordingButton.innerHTML = "⬆️";
            isRecording = true;
        } else {
            stopRecording();
            voiceRecordingButton.innerHTML = "🎙️";
            isRecording = false;
        }
    }
});

messageInput.addEventListener('click', function() {
    picker.style.display = 'none';
});

messageInput.addEventListener('input', toggleSendOrVoiceButton);

function refreshPage() {
    location.reload(true);
}

emojiButton.addEventListener('click', () => {
    if (picker.style.display === 'none') {
        const messageInputField = document.querySelector('.chat-message');
        const boundingRect = messageInputField.getBoundingClientRect();
        picker.style.left = `${boundingRect.left}px`;
        picker.style.bottom = `${window.innerHeight - boundingRect.top}px`;
        picker.style.display = 'block';
    } else {
        picker.style.display = 'none';
    }
});

picker.addEventListener('emoji-click', event => {
    const messageInputDom = document.querySelector('#chat-message-input');
    messageInputDom.value += event.detail.emoji.unicode;
    toggleSendOrVoiceButton();
});

const centrifuge = new Centrifuge("ws://" + window.location.host + "/connection/websocket");
centrifuge.on('connect', function (ctx) {
    console.log("connected", ctx);
});
centrifuge.on('disconnect', function (ctx) {
    console.log("disconnected", ctx);
});

let userFirstName = document.getElementById('user-first-name') ? document.getElementById('user-first-name').value : '';
let userLastName = document.getElementById('user-last-name') ? document.getElementById('user-last-name').value : '';
let userEmail = document.getElementById('user-email') ? document.getElementById('user-email').value : '';
let userAvatarUrl = document.getElementById('user-avatar-url') ? document.getElementById('user-avatar-url').value : '';

const channelName = 'rooms:' + roomId;

const sub = centrifuge.subscribe(channelName, function (ctx) {
    const chatNewThread = document.createElement('li');
    const chatMessageBody = document.createElement('div');
    chatMessageBody.classList.add('message-body');

    const chatAvatar = document.createElement('div');
    chatAvatar.classList.add('user-avatar');
    chatAvatar.style.backgroundImage = 'url(' + ctx.data.avatarUrl + ')';

    const chatUserName = document.createElement('div');
    chatUserName.classList.add('user-name');
    chatUserName.innerText = ctx.data.userFirstName + ' ' + ctx.data.userLastName;

    const chatTimestamp = document.createElement('div');
    chatTimestamp.classList.add('timestamp');
    chatTimestamp.innerText = new Date(ctx.data.timestamp).toLocaleString();

    const chatMessageContent = document.createElement('div');
    chatMessageContent.classList.add('message-content');

    if (ctx.data.fileMessage) {
        if (ctx.data.isImage) {
            const chatImage = document.createElement('img');
            chatImage.src = ctx.data.fileUrl;
            chatImage.alt = ctx.data.message;
            chatImage.classList.add('responsive-image');
            chatImage.onload = function() {
                chatThread.scrollTop = chatThread.scrollHeight;
            };
            chatMessageContent.appendChild(chatImage);
        } else if (ctx.data.isAudio) {
            const audioPlayer = document.createElement('audio');
            audioPlayer.setAttribute('controls', '');
            const audioSource = document.createElement('source');
            audioSource.src = ctx.data.fileUrl;
            audioSource.type = 'audio/mpeg';
            audioPlayer.appendChild(audioSource);
            chatMessageContent.appendChild(audioPlayer);
        } else if (ctx.data.fileUrl.endsWith('.mp3') || ctx.data.fileUrl.endsWith('.wav')) {
            const chatAudioPlayer = document.createElement('audio');
            chatAudioPlayer.controls = true;
            chatAudioPlayer.src = ctx.data.fileUrl;
            chatMessageContent.appendChild(chatAudioPlayer);
        } else if (ctx.data.isVideo || ctx.data.fileUrl.endsWith('.mp4') || ctx.data.fileUrl.endsWith('.webm') || ctx.data.fileUrl.endsWith('.ogg')) {
            const videoPlayer = document.createElement('video');
            videoPlayer.setAttribute('controls', '');
            videoPlayer.setAttribute('preload', 'metadata');
            videoPlayer.classList.add('video-player');
            videoPlayer.addEventListener('loadedmetadata', function() {
                chatThread.scrollTop = chatThread.scrollHeight;
            });
            chatMessageContent.appendChild(videoPlayer);
            videoPlayer.src = ctx.data.fileUrl;
            videoPlayer.load();
        }  else {
            const chatFileLink = document.createElement('a');
            chatFileLink.href = ctx.data.fileUrl;
            chatFileLink.target = '_blank';
            chatFileLink.textContent = ctx.data.message;
            chatMessageContent.appendChild(chatFileLink);
        }
    } else {
        const chatNewMessage = document.createTextNode(ctx.data.message);
        chatMessageContent.appendChild(chatNewMessage);
    }

    chatMessageBody.appendChild(chatUserName);
    chatMessageBody.appendChild(chatMessageContent);
    chatMessageBody.appendChild(chatTimestamp);
    chatNewThread.appendChild(chatAvatar);
    chatNewThread.appendChild(chatMessageBody);

    if (ctx.data.user === userEmail) {
        chatNewThread.classList.add('current-user');
    } else {
        chatNewThread.classList.add('other-user');
    }

    chatThread.appendChild(chatNewThread);
    chatThread.scrollTop = chatThread.scrollHeight;
});

centrifuge.connect();

messageInput.focus();

messageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        const message = messageInput.value;
        if (!message) {
            return;
        }

        sub.publish({
            'message': message,
            'user': userEmail,
            'timestamp': new Date().toISOString(),
            'userFirstName': userFirstName,
            'userLastName': userLastName,
            'avatarUrl': userAvatarUrl
        });

        messageInput.value = '';
        toggleSendOrVoiceButton();
        picker.style.display = 'none';
    }
};

sendButton.addEventListener('click', function() {
    const message = messageInput.value;
    if (!message.trim()) {
        return;
    }

    sub.publish({
        'message': message,
        'user': userEmail,
        'timestamp': new Date().toISOString(),
        'userFirstName': userFirstName,
        'userLastName': userLastName,
        'avatarUrl': userAvatarUrl
    });

    messageInput.value = '';
    toggleSendOrVoiceButton();
    picker.style.display = 'none';
});

const fileOrBlob = document.querySelector('#chat-file-input');
handleFileUpload(fileOrBlob, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl);
