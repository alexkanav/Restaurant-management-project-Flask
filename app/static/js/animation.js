const onEntry = (entry) => {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('show-content');
        }
    });
}

const options = { threshold: [0.5] };
const observer = new IntersectionObserver(onEntry, options);
const elements = document.querySelectorAll('.element-animation');
elements.forEach(elm => observer.observe(elm));
