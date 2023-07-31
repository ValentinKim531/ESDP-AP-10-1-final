async function handleFileUpload(fileOrBlob, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl) {
    let file;

    if (fileOrBlob instanceof Blob) {
        file = new File([fileOrBlob], 'voiceMessage.mp3', { type: 'audio/mpeg' });
        uploadFile(file, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl);
    } else {
        fileOrBlob.onchange = async function(e) {
            e.preventDefault();

            file = fileOrBlob.files[0];

            if (!file) {
                return;
            }

            uploadFile(file, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl);
        };
    }
}

async function uploadFile(file, centrifuge, roomId, userEmail, userFirstName, userLastName, userAvatarUrl) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`/chat/chatfiles/${roomId}/`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        alert('File upload failed');
        return;
    }

    const data = await response.json();

    const message = {
        'message': file.name,
        'fileUrl': data.file_url,
        'fileMessage': true,
        'isImage': data.is_image,
        'isAudio': data.is_audio,
        'isVideo': data.is_video,
        'user': userEmail,
        'timestamp': new Date().toISOString(),
        'userFirstName': userFirstName,
        'userLastName': userLastName,
        'avatarUrl': userAvatarUrl
    };

    const channelName = 'rooms:' + roomId;
    centrifuge.publish(channelName, message);
}

export { handleFileUpload };
