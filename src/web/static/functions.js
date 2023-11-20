export function getClientStateSettings() {
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