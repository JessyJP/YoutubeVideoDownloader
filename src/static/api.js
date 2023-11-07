const API_PROXY = "http://localhost:5000";  // Replace with your actual IP and port.

async function analyzeURL(url) {
    console.log("Analyze API call made!");
    const response = await fetch(`${API_PROXY}/api/analyse`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    });
    
    return await response.json();
}

async function analyzeVideo(url) {
    const response = await fetch(`${API_PROXY}/api/analyze_video`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    });

    return await response.json();
}

async function getAudioBitrateList() {
    const response = await fetch(`${API_PROXY}/api/audio_bitrate_list`);
    return await response.json();
}

async function getVideoResolutionList() {
    const response = await fetch(`${API_PROXY}/api/video_resolution_list`);
    return await response.json();
}

async function getFPSValueList() {
    const response = await fetch(`${API_PROXY}/api/fps_value_list`);
    return await response.json();
}

async function downloadVideo(data) {
    const response = await fetch(`${API_PROXY}/api/download_video`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

async function playVideoPreview(videoPath) {
    const response = await fetch(`${API_PROXY}/api/play_video_preview`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_path: videoPath }),
    });

    return await response.json();
}

async function selectDownloadLocation() {
    const response = await fetch(`${API_PROXY}/api/select_download_location`);
    return await response.json();
}

export {
    analyzeURL,
    analyzeVideo,
    getAudioBitrateList,
    getVideoResolutionList,
    getFPSValueList,
    downloadVideo,
    playVideoPreview,
    selectDownloadLocation,
};
