function DOMContentLoader(someFunction) {
    if (window.addEventListener) {
        window.addEventListener('DOMContentLoaded', someFunction, false);
    } else {
        window.attachEvent('onload', domReady);
    };
};

export {DOMContentLoader}
