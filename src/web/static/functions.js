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

export function printDeviceInfo(deviceInfo) {
    // const deviceInfo = getClientDeviceInfo();

    console.log("Screen Width:", deviceInfo.screenWidth, "Screen Height:", deviceInfo.screenHeight);
    console.log("Window Width:", deviceInfo.windowWidth, "Window Height:", deviceInfo.windowHeight);
    console.log("Is Mobile:", deviceInfo.deviceType.isMobile, "Is Tablet:", deviceInfo.deviceType.isTablet, "Is Desktop:", deviceInfo.deviceType.isDesktop);
    console.log("Device Orientation:", deviceInfo.orientation);
    console.log("Device Pixel Ratio:", deviceInfo.pixelRatio);
    console.log("Browser Name:", deviceInfo.browser.name, "Version:", deviceInfo.browser.version);
}


export function getClientSettingsConfiguration() {
    const audioBitrate = document.getElementById('audio-limiter').value;
    const videoResolution = document.getElementById('video-limiter').value;
    const fpsValue = document.getElementById('fps-limiter').value;
    const currentTheme = document.body.className; // Or other logic to get the current theme

    // If there's an input field for download location
    // const downloadLocation = document.getElementById('download-location').value;

    return {
        audioBitrate,
        videoResolution,
        fpsValue,
        currentTheme,
        // downloadLocation
    };
}



export function switchTheme(newTheme) {
    console.log("Set the theme to: [" + newTheme + "]");

    let htmlElement = document.documentElement;

    switch(newTheme) {
        case 'dark-theme':
            htmlElement.setAttribute('data-theme', 'dark-theme');
            break;
        case 'light-theme':
            htmlElement.setAttribute('data-theme', 'light-theme');
            break;
        default:
            console.error("Unknown theme:", newTheme);
    }
}


export function updateProgressBar(progress) {
    var progressBar = document.getElementById("progress-bar-id");
    progressBar.style.width = progress + '%';
    progressBar.innerText = progress + '%';
}