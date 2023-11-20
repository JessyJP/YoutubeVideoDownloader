import VideoItem from "./TableManger/VideoItem.js";
import {getClientSettingsConfiguration}from "./functions.js"

const API_PROXY = "http://localhost:80";  // Replace with your actual IP and port.

// ============= GET state GET methods ============= 

async function getState() {
    const url = `${API_PROXY}/api/getState`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.text(); 
    } catch (error) {
        console.error("Error in getState: ", error);
        return null; // Return null or a default state in case of an error
    }
}

async function getStatusMsg() {
    const url = `${API_PROXY}/api/getStatusMsg`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.text();
    } catch (error) {
        console.error("Error in getStatusMsg: ", error);
        return ""; // Return an empty string in case of an error
    }
}

async function getProgressbarValue() {
    const url = `${API_PROXY}/api/getProgressbarValue`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.text();
    } catch (error) {
        console.error("Error in getProgressbarValue: ", error);
        return "0%"; // Return an empty string in case of an error
    }
}

async function getVideoItemList() {
    const url = `${API_PROXY}/api/getVideoItemList`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const videoItemsData = await response.json();// NOTE: this is directly exported as array of objects
        return videoItemsData.map(videoData => new VideoItem(videoData));
    } catch (error) {
        console.error("Error in getVideoItemList: ", error);
        return []; // Return an empty array in case of an error
    }
}

// ============= SET state POST methods ============= 

async function postClientStateSettings(tableManager) {
    const clientStateSettings = getClientSettingsConfiguration();

    console.log("Posting client state settings: ", clientStateSettings);

    // Send this object to the backend
    const response = await fetch(`${API_PROXY}/api/update_client_state`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(clientStateSettings)
    });

    // Check the response from the server
    if (response.ok) {
        console.log("Client state settings updated successfully.");
    } else {
        console.error("Failed to update client state settings.");
    }
}

async function clearItemSelectionByID(videoIds) {
    console.log("Clearing items with IDs: ", videoIds);

    // Send this list of IDs to the backend
    const response = await fetch(`${API_PROXY}/api/clearItemSelectionByID`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoIds: videoIds })
    });

    // Check the response from the server
    if (response.ok) {
        console.log("Items cleared successfully.");
        return await response.json(); // Assuming the backend sends a response
    } else {
        console.error("Failed to clear items.");
        throw new Error("Failed to clear items.");
    }
}

// ============= POST methods for processing =============

async function analyzeURLtext(url_text) {
    postClientStateSettings()// Update the latest client settings
    console.log("Analyze API call made : ["+url_text+"]");
    const response = await fetch(`${API_PROXY}/api/analyzeURLtext`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url_text }),
    });
    
    return await response.json();
}

async function downloadVideoList() {
    postClientStateSettings()// Update the latest client settings
    console.log("Download API call started");
    const response = await fetch(`${API_PROXY}/api/downloadVideoList`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(),
    });

    return await response.json();
}

// ============= UNUSED methods =============

// async function playVideoPreview(videoPath) {
//     const response = await fetch(`${API_PROXY}/api/play_video_preview`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ video_path: videoPath }),
//     });
//     return await response.json();
// }

// async function selectDownloadLocation() {
//     const response = await fetch(`${API_PROXY}/api/select_download_location`);
//     return await response.json();
// }

export {
    getState,
    getStatusMsg,
    getProgressbarValue,
    getVideoItemList,
    postClientStateSettings,
    clearItemSelectionByID,
    analyzeURLtext,
    downloadVideoList,
    // playVideoPreview,
    // selectDownloadLocation,
};
