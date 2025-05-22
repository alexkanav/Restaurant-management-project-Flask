const sections = [];
const navItems = document.querySelector('.nav-scroller__items');

const initSections = (categoriesNum) => {
    for (let i = 1; i <= categoriesNum; i++) {
        const button = document.querySelector(`#pos${i}`);
        const section = document.querySelector(`#category${i}`);
        if (button && section) {
            sections.push({
                element: section,
                button: button
            });
        }
    }
};

const scrNav = (value) => {
    navItems.scrollLeft = value - 200;
};

const changeCss = () => {
    const scrollY = window.scrollY;
    for (const { element, button } of sections) {
        const rect = element.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        const bottom = rect.bottom + window.scrollY;

        if (scrollY > top - 10 && scrollY < bottom) {
            const navLeft = button.getBoundingClientRect().left + navItems.scrollLeft;
            scrNav(navLeft);
            sections.forEach(({ button: btn }) => btn.classList.remove("butcol"));
            button.classList.add("butcol");
            break;
        }
    }
};

document.addEventListener("DOMContentLoaded", () => {
    initSections(categoriesNum);
    window.addEventListener("scroll", changeCss, false);

    document.querySelectorAll('.nav-scr-add').forEach(button => {
        button.addEventListener('click', () => {
            const code = button.dataset.code;
            const description = button.dataset.description;

            addAddition(button.id, code, description);
        });
    });
});
