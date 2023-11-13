export function switchTheme(newTheme) {
    console.log("Set the theme to: ["+newTheme+"]");
    // Set the theme based on the argument
    if (newTheme === 'dark-theme') {
        document.body.className = 'dark-theme';
    } else {
        document.body.className = 'light-theme';
    }
}