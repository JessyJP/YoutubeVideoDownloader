import { 
    analyzeURL,
    analyzeVideo, 
    getAudioBitrateList, 
    getVideoResolutionList, 
    getFPSValueList, 
    downloadVideo, 
    playVideoPreview, 
    selectDownloadLocation
} from './api.js';


document.getElementById("analyze-btn").addEventListener("click", async () => {
    console.log("Analyze Button press!")
    const url = document.getElementById("url-entry").value;
    if (!url) return alert("Please enter a video URL.");

    const data = await analyzeURL(url);

    if (data.message) {
        alert(data.message);
    }

    // Handle the response data further as needed.
    // E.g., update the table with the video data.
});

document.getElementById("analyze-btn").addEventListener("click", async () => {
    const url = document.getElementById("url-entry").value;
    
    if (!url) return alert("Please enter a video URL.");

    const data = await analyzeVideo(url);

    if (data.message) {
        alert(data.message);
    }

    // Handle the response data further as needed.
    // E.g., update the table with the video data.
});

document.getElementById("play-btn").addEventListener("click", async () => {
    const videoPath = 'path/to/selected/video'; // You'll need a mechanism to select a specific video
    const data = await playVideoPreview(videoPath);
    if (data.message) {
        alert(data.message);
    }
});

document.getElementById("location-btn").addEventListener("click", async () => {
    const locationData = await selectDownloadLocation();
    const inputLocation = document.getElementById("download-location");
    inputLocation.value = locationData.download_location;
});

// Optionally populate drop-down lists on page load or based on certain actions
// window.addEventListener("load", async () => {
//     const audioBitrateList = await getAudioBitrateList();
//     const videoResolutionList = await getVideoResolutionList();
//     const fpsValueList = await getFPSValueList();

//     // Populate the drop-downs
//     const audioLimiter = document.getElementById("audio-limiter");
//     audioBitrateList.forEach(bitrate => {
//         let option = document.createElement("option");
//         option.value = bitrate;
//         option.text = `${bitrate} kbps`;
//         audioLimiter.appendChild(option);
//     });

//     const videoLimiter = document.getElementById("video-limiter");
//     videoResolutionList.forEach(resolution => {
//         let option = document.createElement("option");
//         option.value = resolution;
//         option.text = `${resolution}p`;
//         videoLimiter.appendChild(option);
//     });

//     const fpsLimiter = document.getElementById("fps-limiter");
//     fpsValueList.forEach(fps => {
//         let option = document.createElement("option");
//         option.value = fps;
//         option.text = `${fps} fps`;
//         fpsLimiter.appendChild(option);
//     });
// });

// You can continue to add more event listeners as needed.
