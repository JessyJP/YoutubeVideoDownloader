import { 
    analyzeURLtext,
    // getAudioBitrateList, 
    // getVideoResolutionList, 
    // getFPSValueList, 
    // downloadVideo, 
    // playVideoPreview, 
    // selectDownloadLocation
    // Import other necessary functions
} from './api.js';

import { switchTheme } from './functions.js';

import TableManager from './TableManager.js';

// ====================================
// Page main event handling

// Start checking on page load
window.addEventListener("load", () => {
    const defaultTheme = 'dark-theme'
    switchTheme(defaultTheme);
    // This is for last
    tableManager.checkAndUpdateState();
});

// Ensure the auto-update process is stopped when leaving the page
window.addEventListener("unload", () => {
    tableManager.checkModeFlag = false;
});

//  =======================================================

// Instantiate TableManager only once
const tableManager = new TableManager();

// Function to handle button clicks
function onUserInteraction() {
    tableManager.checkAndUpdateState();
}

//  =======================================================
// User event handling 

// Analyze Button Event Listener
document.getElementById("analyze-btn").addEventListener("click", async () => {
    const url = document.getElementById("url-entry").value;
    if (!url) {
        alert("Please enter a video URL.");
        return;
    }

    // Call analyzeURLtext and handle the response
    const data = await analyzeURLtext(url);
    console.log(data.message);
    // Optionally, update the UI or perform additional actions based on the response
    onUserInteraction()
});

// Download Button Event Listener
document.getElementById("download-btn").addEventListener("click", () => {
    // Implement the download logic here
    // Example: initiate the download process for the selected video
    onUserInteraction()
});

document.getElementById("play-btn").addEventListener("click", async () => {
    const videoPath = 'path/to/selected/video'; // Implement the mechanism to get the selected video path
    try {
        const data = await playVideoPreview(videoPath);
        if (data.message) {
            alert(data.message);
        }
    } catch (error) {
        console.error("Error playing video preview: ", error);
        alert("Failed to play video preview.");
    }
    onUserInteraction();
});

document.getElementById("location-btn").addEventListener("click", async () => {
    try {
        const locationData = await selectDownloadLocation();
        const inputLocation = document.getElementById("download-location");
        inputLocation.value = locationData.download_location;
    } catch (error) {
        console.error("Error selecting download location: ", error);
        alert("Failed to select download location.");
    }
    onUserInteraction();
});


// window.addEventListener("load", async () => {
//     // Existing load event logic
//     tableManager.checkAndUpdateState();

//     // Additional logic to populate drop-downs
//     try {
//         const audioBitrateList = await getAudioBitrateList();
//         const videoResolutionList = await getVideoResolutionList();
//         const fpsValueList = await getFPSValueList();

//         populateDropdown("audio-limiter", audioBitrateList, "kbps");
//         populateDropdown("video-limiter", videoResolutionList, "p");
//         populateDropdown("fps-limiter", fpsValueList, "fps");
//     } catch (error) {
//         console.error("Error populating dropdowns: ", error);
//     }
// });

// function populateDropdown(elementId, items, unit) {
//     const dropdown = document.getElementById(elementId);
//     items.forEach(item => {
//         let option = document.createElement("option");
//         option.value = item;
//         option.text = `${item} ${unit}`;
//         dropdown.appendChild(option);
//     });
// }


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


document.getElementById("theme-btn").addEventListener("click", () => {
    // Determine the new theme based on the current one
    const currentTheme = document.body.className;
    const newTheme = currentTheme === 'dark-theme' ? 'light-theme' : 'dark-theme';

    // Switch to the new theme
    switchTheme(newTheme);

    // Trigger state check
    onUserInteraction();
});
