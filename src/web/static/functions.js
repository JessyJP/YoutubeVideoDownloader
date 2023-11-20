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