import { 
    getVideoItemList,
    getClientStateSettings,
    postClientStateSettings,
    changeStatusForItemsSelectedByID,
    analyzeURLtext,
    downloadVideoList,
    getSaveOutputToDevice,
} from './api.js';

import { 
    getTheme,
    setTheme,
    adjustGridBasedOnDevice,
    setClientUiSettingsConfiguration,
    setWebUIcontrolsEnabled
} from './functions.js';

import ItemManager from './ItemManager/ItemManager.js';
// === Define ===
const environment = "development" 
//  ==========================================================================================
// Instantiate ItemManager only once
const tableManager = new ItemManager();

// Function to handle button clicks
function onUserInteraction() {
    // Post the latest state to the server
    postClientStateSettings(tableManager);
    // Get back the latest update from the server
    tableManager.checkAndUpdateState();
}

// ==========================================================================================
// Page main event handling

// Start checking on page load
window.addEventListener("load", async () => {

    if (environment === 'production') {
        // Disable console.log
        console.log = function() {};
    }
    
 
    // Set the default theme
    const defaultTheme = 'dark-theme'
    setTheme(defaultTheme);

    // Try to get state from the server
    const appState = await getClientStateSettings();

    // If available and valid set the client state to the the server snapshot
    setClientUiSettingsConfiguration(appState.uiSettings, tableManager);
    // If available also set the column state
    tableManager.columnManager.updateColumnManagerState(appState.columnVisibility)
    
    tableManager.checkAndUpdateState();
});

// Ensure the auto-update process is stopped when leaving the page
window.addEventListener("unload", () => {
    tableManager.checkModeFlag = false;
});

window.addEventListener('resize', () => {
    adjustGridBasedOnDevice(tableManager);
});


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

// Save to my device Button Event Listener
document.getElementById("save-to-device").addEventListener("click", async () => {
    setWebUIcontrolsEnabled(false)
    // Call downloadVideoList and handle the response
    await getSaveOutputToDevice();
    console.log("Finished transferring the downloaded files!");
    // Optionally, update the UI or perform additional actions based on the response
    setWebUIcontrolsEnabled(true)
    onUserInteraction();
});

// ==========================================================================================
// Update client state settings
document.getElementById("theme-btn").addEventListener("click", () => {
    // Determine the new theme based on the current theme
    // TODO: NOTE his could also be done based on the current button state
    const currentTheme = getTheme()
    const newTheme = currentTheme === 'dark-theme' ? 'light-theme' : 'dark-theme';

    // Switch to the new theme
    setTheme(newTheme);
    // Trigger state check
    onUserInteraction();
});

document.getElementById("view-mode-dropdown").addEventListener('change', (event) => {
    tableManager.viewMode = event.target.value;
    adjustGridBasedOnDevice(tableManager);
    onUserInteraction();
});

document.querySelectorAll('input[type="radio"][name="radio"]').forEach(radio => {
    radio.addEventListener('change', (event) => {
        if (event.target.checked) {
            tableManager.viewMode = event.target.value;
            adjustGridBasedOnDevice(tableManager);
            onUserInteraction();
        }
    });
});


document.getElementById("audio-limiter").addEventListener("change", () => onUserInteraction());

document.getElementById("video-limiter").addEventListener("change", () => onUserInteraction());

document.getElementById("fps-limiter").addEventListener("change", () => onUserInteraction());

// ==========================================================================================
// Keyboard event handler
document.addEventListener("keydown", async (event) => {
    // Handle the Delete key
    if (event.key === "Delete") {
        const selectionVideoIDs = tableManager.getSelectedItemIds();
        console.log("Selected item IDs:", selectionVideoIDs);

        // Call changeStatusForItemsSelectedByID and handle the response
        const response = await changeStatusForItemsSelectedByID("remove",selectionVideoIDs);
        console.log(response.message);

        onUserInteraction();
    }

    // Handle Ctrl+A key combination
    if (event.ctrlKey && event.key === "a") {
        event.preventDefault(); // Prevent default text selection
        tableManager.setAllItemsAsSelected();
        // onUserInteraction();//NOTE: Not needed
    }

    // Handle ESC key for deselecting all items
    if (event.key === "Escape") {
        tableManager.setAllItemsAsDeselected();
        // Optionally, trigger a state check or UI update
        // onUserInteraction();//NOTE: Not needed
    }
});
