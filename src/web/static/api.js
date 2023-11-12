const API_PROXY = "http://localhost:80";  // Replace with your actual IP and port.


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

        return await response.json();
    } catch (error) {
        console.error("Error in getVideoItemList: ", error);
        return []; // Return an empty array in case of an error
    }
}

async function analyzeURLtext(url) {
    console.log("Analyze API call made : ["+url+"]");
    const response = await fetch(`${API_PROXY}/api/analyzeURLtext`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    });
    
    return await response.json();
}

async function downloadVideoList(data) {
    const response = await fetch(`${API_PROXY}/api/downloadVideoList`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

// async function getAudioBitrateList() {
//     const response = await fetch(`${API_PROXY}/api/audio_bitrate_list`);
//     return await response.json();
// }

// async function getVideoResolutionList() {
//     const response = await fetch(`${API_PROXY}/api/video_resolution_list`);
//     return await response.json();
// }

// async function getFPSValueList() {
//     const response = await fetch(`${API_PROXY}/api/fps_value_list`);
//     return await response.json();
// }



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
    getVideoItemList,
    analyzeURLtext,
    // getAudioBitrateList,
    // getVideoResolutionList,
    // getFPSValueList,
    downloadVideoList,
    // playVideoPreview,
    // selectDownloadLocation,
};
