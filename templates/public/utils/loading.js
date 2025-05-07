window.addEventListener('pageshow', function () {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.add('hidden');
        loadingScreen.classList.remove('flex');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const loadingScreen = document.getElementById('loading-screen');

    if (loadingScreen) {
        loadingScreen.classList.add('hidden');
        loadingScreen.classList.remove('flex');
    }

    form.addEventListener('submit', function (event) {
        const formInput = document.getElementById('steamid').value;

        if (formInput.trim() !== '') {
            loadingScreen.classList.remove('hidden');
            loadingScreen.classList.add('flex');
        } else {
            event.preventDefault();
        }
    });
});
