import VideoItem from "./ItemManager/VideoItem.js";
import {getClientUiSettingsConfiguration, updateProgressBarUi}from "./functions.js"

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

async function getClientStateSettings() {
    try {
        const response = await fetch(`${API_PROXY}/api/update_client_state`, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Received client state settings from server:", data);

        return data;
    } catch (error) {
        console.error("Failed to fetch client state settings:", error);
        // Handle the error appropriately
    }
}

// ============= SET state POST methods ============= 

async function postClientStateSettings(itemManager) {
    const clientStateSettings = getClientUiSettingsConfiguration();
    const columnVisibilityConfig = itemManager.columnManager.getAllColumnsVisibility();

    const combinedSettings = {
        uiSettings: clientStateSettings,
        columnVisibility: columnVisibilityConfig
    };

    console.log("Posting combined client UI state and column visibility settings:", combinedSettings);

    // Send this combined object to the backend
    const response = await fetch(`${API_PROXY}/api/update_client_state`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(combinedSettings)
    });

    // Check the response from the server
    if (response.ok) {
        console.log("Client state and column visibility settings updated successfully.");
    } else {
        console.error("Failed to update client state and column visibility settings.");
    }
}

async function changeStatusForItemsSelectedByID(instruction, videoIds) {
    console.log(`Applying instruction '${instruction}' to items with IDs: `, videoIds);

    // Send the instruction and list of IDs to the backend
    const response = await fetch(`${API_PROXY}/api/changeStatusForItemsSelectedByID`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ instruction, videoIds })
    });

    // Check the response from the server
    if (response.ok) {
        const responseData = await response.json(); // Assuming the backend sends a response
        console.log(`Instruction '${instruction}' applied successfully to items: `, videoIds, "Response:", responseData);
        return responseData;
    } else {
        console.error(`Failed to apply instruction '${instruction}' to items: `, videoIds);
        throw new Error(`Failed to apply instruction '${instruction}'.`);
    }
}


// ============= POST methods for processing =============

async function analyzeURLtext(url_text) {
    // Update the latest client settings. Assume  postClientStateSettings(itemManager) is called just prior
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
    // Update the latest client settings. Assume  postClientStateSettings(itemManager) is called just prior
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

// ============= Transfer file methods =============
// TODO: NOTE: Test api call 
async function getSaveOutputToDevice() {
    const urlGetList = `${API_PROXY}/api/getFileList`;
    let fileList;
    updateProgressBarUi(0); // Initialize the progress bar to 0%

    try {
        const response = await fetch(urlGetList);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        fileList = await response.json();
    } catch (error) {
        console.error("Error in fetching file list: ", error);
        return null;
    }

    let urlTransferFile = `${API_PROXY}/api/transferFile`;
    // Download each file
    for (let i = 0; i < fileList.length; i++) {
        let file = fileList[i];
        try {
            let downloadResponse = await fetch(`${urlTransferFile}?video_id=${encodeURIComponent(file.video_id)}&symbol_key=${encodeURIComponent(file.symbol_key)}`);
            
            if (!downloadResponse.ok) {
                throw new Error(`HTTP error! status: ${downloadResponse.status}`);
            }

            let blob = await downloadResponse.blob();
            saveFile(blob, `${file.save_output_filename}`); // Adjust file name format as needed
            
            // Update the progress bar UI with the current progress
            updateProgressBarUi((i / fileList.length) * 100);
        } catch (downloadError) {
            console.error(`Error downloading file ${file.video_title}: `, downloadError);
        }
    }
    // Ensure the progress bar shows 100% when all files are processed
    updateProgressBarUi(100);
}

function saveFile(blob, fileName) {
    // Create a link and set the URL using createObjectURL
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href); // Clean up
}

export {
    getState,
    getStatusMsg,
    getProgressbarValue,
    getVideoItemList,
    getClientStateSettings,
    postClientStateSettings,
    changeStatusForItemsSelectedByID,
    analyzeURLtext,
    downloadVideoList,
    // selectDownloadLocation,
    getSaveOutputToDevice
};
