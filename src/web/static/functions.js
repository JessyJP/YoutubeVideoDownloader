// ========== Device Information Methods ==========

/**
 * Retrieves various details about the client's device.
 * @returns {Object} An object containing device information.
 */
export function getClientDeviceInfo() {
    const screenWidth = window.screen.width;
    const screenHeight = window.screen.height;

    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    const userAgent = navigator.userAgent.toLowerCase();
    const isMobile = /mobile/.test(userAgent);
    const isTablet = /tablet/.test(userAgent) || (isMobile && screenWidth >= 768);
    const isDesktop = !isMobile && !isTablet;

    const orientation = (screen.orientation || {}).type || screen.mozOrientation || screen.msOrientation;

    const pixelRatio = window.devicePixelRatio;

    const browserName = navigator.appName;
    const browserVersion = navigator.appVersion;

    return {
        screenWidth,
        screenHeight,
        windowWidth,
        windowHeight,
        deviceType: {
            isMobile,
            isTablet,
            isDesktop
        },
        orientation,
        pixelRatio,
        browser: {
            name: browserName,
            version: browserVersion
        }
    };
}

/**
 * Prints device information to the console.
 * @param {Object} deviceInfo - The device information object.
 */
export function printDeviceInfo(deviceInfo) {
    console.log("Screen Width:", deviceInfo.screenWidth, "Screen Height:", deviceInfo.screenHeight);
    console.log("Window Width:", deviceInfo.windowWidth, "Window Height:", deviceInfo.windowHeight);
    console.log("Is Mobile:", deviceInfo.deviceType.isMobile, "Is Tablet:", deviceInfo.deviceType.isTablet, "Is Desktop:", deviceInfo.deviceType.isDesktop);
    console.log("Device Orientation:", deviceInfo.orientation);
    console.log("Device Pixel Ratio:", deviceInfo.pixelRatio);
    console.log("Browser Name:", deviceInfo.browser.name, "Version:", deviceInfo.browser.version);
}

// ========== Theme Management Methods ==========

/**
 * Gets the current theme.
 * @returns {String} The current theme.
 */
export function getUiThemeElement() {
    return document.querySelector("html");
}

export function getTheme()
{
    return getUiThemeElement().getAttribute("data-theme");
}

/**
 * Switches to a specified theme.
 * @param {String} newTheme - The theme to switch to.
 */
export function setTheme(newTheme) {
    let htmlElement = getUiThemeElement();

    switch(newTheme) {
        case 'dark-theme':
            htmlElement.setAttribute('data-theme', 'dark-theme');
            break;
        case 'light-theme':
            htmlElement.setAttribute('data-theme', 'light-theme');
            break;
        default:
            console.error("Unknown theme:", newTheme);
            return;
    }

    
}

// ========== View Mode Methods ==========

/**
 * Retrieves the current view mode.
 * @returns {String} The current view mode.
 */
export function getCurrentViewModeUiElementState() {
    return document.getElementById('viewMode').value;
}

/**
 * Sets the current view mode.
 * @param {String} newViewMode - The new view mode to set.
 */
export function setCurrentViewModeUiElementState(newViewMode) {
    document.getElementById('viewMode').value = newViewMode;
}

/**
 * Adjusts the grid layout based on the device type.
 * @param {Object} tableManager - The table manager instance.
 */
export function adjustGridBasedOnDevice(tableManager) {
    if (tableManager.viewMode === "grid") {
        const deviceInfo = getClientDeviceInfo();
        if (deviceInfo.deviceType.isMobile) {
            tableManager.adjustGridLayout(1);
        } else if (deviceInfo.deviceType.isTablet) {
            tableManager.adjustGridLayout(2);
        } else {
            // Adjust the number of columns based on screen width
            const numColumns = Math.floor(deviceInfo.windowWidth / 600);
            tableManager.adjustGridLayout(numColumns);
        }
    }
}

// ========== Get/Set function pairs for the dropdown quality limiters  ==========

function setAudioLimit(value) {
    document.getElementById("audio-limiter").value = value;
}

function getAudioLimit() {
    return document.getElementById("audio-limiter").value;
}

function setVideoLimit(value) {
    document.getElementById("video-limiter").value = value;
}

function getVideoLimit() {
    return document.getElementById("video-limiter").value;
}

function setFpsLimit(value) {
    document.getElementById("fps-limiter").value = value;
}

function getFpsLimit() {
    return document.getElementById("fps-limiter").value;
}


// ========== Client Settings Configuration Methods ==========

/**
 * Retrieves the current client settings configuration.
 * @returns {Object} The current settings configuration.
 */
export function getClientUiSettingsConfiguration() {
    const currentTheme = getTheme();
    const audioBitrate = getAudioLimit();
    const videoResolution = getVideoLimit();
    const fpsValue = getFpsLimit();
    const viewMode = getCurrentViewModeUiElementState();

    return {
        audioBitrate,
        videoResolution,
        fpsValue,
        currentTheme,
        viewMode
    };
}

/**
 * Sets the client settings based on the provided configuration.
 * @param {Object} configuration - The configuration object to set.
 */
export function setClientUiSettingsConfiguration(configuration, tableManager) {
    if (configuration.audioBitrate) {
        setAudioLimit( configuration.audioBitrate );
    }
    if (configuration.videoResolution) {
        setVideoLimit( configuration.videoResolution );
    }
    if (configuration.fpsValue) {
        setFpsLimit( configuration.fpsValue );
    }
    if (configuration.currentTheme) {
        // Switch the theme
        setTheme(configuration.currentTheme);
        // TODO: maybe we should consolidate the switching and the UI state update
        // Update the button to reflect the current theme
        const themeButton = document.getElementById("theme-btn");
        themeButton.textContent = configuration.currentTheme === 'dark-theme' ? 'Light Mode' : 'Dark Mode';
    }
    if (configuration.viewMode) {
        setCurrentViewModeUiElementState(configuration.viewMode);
        tableManager.viewMode = configuration.viewMode;
        adjustGridBasedOnDevice(tableManager);
        // TODO: maybe we should consolidate the switching and the UI state update
    }
}

// ========== Progress Bar Update Method ==========

/**
 * Updates the progress bar to the specified progress.
 * @param {Number} progress - The progress percentage to set.
 */
export function updateProgressBarUi(progress) {
    var progressBar = document.getElementById("progress-bar-id");

    // Round the progress to two decimal places
    var roundedProgress = parseFloat(progress).toFixed(2);

    progressBar.style.width = roundedProgress + '%';
    progressBar.innerText = roundedProgress + '%';
}

// ========== Enable/Disable controls Method ==========

export function setWebUIcontrolsEnabled(enable) {
    // Select the elements by their IDs or classes
    const controls = [
        document.getElementById("url-entry"),
        document.getElementById("analyze-btn"),
        document.getElementById("download-btn"),
        document.getElementById("theme-btn"),
        document.getElementById("viewMode"),
        document.getElementById("audio-limiter"),
        document.getElementById("video-limiter"),
        document.getElementById("fps-limiter"),
        document.getElementById("save-to-device")
    ];

    // this.analyzeBtn.disabled = true;
    // this.downloadBtn.disabled = true;
    // this.analyzeBtn.classList.add("disabled-button");
    // this.downloadBtn.classList.add("disabled-button");
    // Set other buttons as needed
    
    // Loop through each control and set its disabled property
    controls.forEach(control => {
        if (control) {
            control.disabled = !enable;
        }
    });
}
