
document.addEventListener("htmx:load", () => {

    document.querySelectorAll("form[data-autosave] textarea, form[data-autosave] select, form[data-autosave] input").forEach((input) => {

        const key = `${location.pathname}/${input.name}`;
        input.addEventListener("change", (e) => {
            localStorage[key] = e.target.value;
        });
        if (localStorage[key]) {
            input.value = localStorage[key];
        }
    });


});