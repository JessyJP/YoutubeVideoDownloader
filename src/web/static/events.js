import { 
    getVideoItemList,
    analyzeURLtext,
    downloadVideoList,
    postClientStateSettings,
    clearItemSelectionByID,
    // playVideoPreview, 
    // selectDownloadLocation
} from './api.js';

import { getClientDeviceInfo,
    // printDeviceInfo, 
    switchTheme 
} from './functions.js';

import ItemManager from './ItemManager/ItemManager.js';

// ==========================================================================================
// Page main event handling

// Start checking on page load
window.addEventListener("load", () => {
    const deviceInfo = getClientDeviceInfo();
    // printDeviceInfo(deviceInfo)

    // Set the default theme
    const defaultTheme = 'dark-theme'
    switchTheme(defaultTheme);
    
    // This is for last
    tableManager.checkAndUpdateState();
});

// Ensure the auto-update process is stopped when leaving the page
window.addEventListener("unload", () => {
    tableManager.checkModeFlag = false;
});

//  ==========================================================================================

// Instantiate ItemManager only once
const tableManager = new ItemManager();

// Function to handle button clicks
function onUserInteraction() {
    tableManager.checkAndUpdateState();
}

//  ==========================================================================================
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
document.getElementById("download-btn").addEventListener("click", async () => {
    // Call downloadVideoList and handle the response
    const response = await downloadVideoList();
    console.log(response.message);
    // Optionally, update the UI or perform additional actions based on the response
    onUserInteraction();
});

// Clear Items Button Event Listener
document.getElementById("clear-items-btn").addEventListener("click", async () => {
    // TODO: LAZY SELECTION the selection has to be acquired here and passed to the function 
    const videoList = await getVideoItemList();
    // TODO: generally there should be a selection of items
    // TODO: in this case we are doing a lazy all
    const videoIds = videoList.map(video => video.video_id); // Extract video IDs

    // Call downloadVideoList and handle the response
    const response = await clearItemSelectionByID(videoIds);
    console.log(response.message);
    // Optionally, update the UI or perform additional actions based on the response
    onUserInteraction();
});


// document.getElementById("play-btn").addEventListener("click", async () => {
//     // TODO: still unfinished
//     const videoPath = 'path/to/selected/video'; // Implement the mechanism to get the selected video path
//     try {
//         const data = await playVideoPreview(videoPath);
//         if (data.message) {
//             alert(data.message);
//         }
//     } catch (error) {
//         console.error("Error playing video preview: ", error);
//         alert("Failed to play video preview.");
//     }
//     onUserInteraction();
// });

// document.getElementById("location-btn").addEventListener("click", async () => {
//     // TODO: still unfinished
//     try {
//         const locationData = await selectDownloadLocation();
//         const inputLocation = document.getElementById("download-location");
//         inputLocation.value = locationData.download_location;
//     } catch (error) {
//         console.error("Error selecting download location: ", error);
//         alert("Failed to select download location.");
//     }
//     onUserInteraction();
// });

// ==========================================================================================
// Update client state settings
document.getElementById("theme-btn").addEventListener("click", () => {
    // Determine the new theme based on the current one
    const currentTheme = document.querySelector("html").getAttribute("data-theme");
    const newTheme = currentTheme === 'dark-theme' ? 'light-theme' : 'dark-theme';

    // Switch to the new theme
    switchTheme(newTheme);
    // Update the client state after switching the theme
    postClientStateSettings(tableManager); 
    // Trigger state check
    onUserInteraction();
});
// document.getElementById("download-location").addEventListener("change", () => postClientStateSettings(tableManager));

document.getElementById("audio-limiter").addEventListener("change", () => postClientStateSettings(tableManager));

document.getElementById("video-limiter").addEventListener("change", () => postClientStateSettings(tableManager));

document.getElementById("fps-limiter").addEventListener("change", () => postClientStateSettings(tableManager));


// ==========================================================================================
document.getElementById('viewMode').addEventListener('change', (event) => {
    const selectedViewMode = event.target.value;
    tableManager.viewMode = selectedViewMode;
    onUserInteraction();
});