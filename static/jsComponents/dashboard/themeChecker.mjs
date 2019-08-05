function themeChecker(colorTheme) {
    
    let targetThemeChanger = document.querySelector('body');

    if (colorTheme == "bl") {
        targetThemeChanger.classList.add("dark-edition");
    } else {
        targetThemeChanger.classList.remove("dark-edition");
    };

};

export {themeChecker};