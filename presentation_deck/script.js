document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const counter = document.getElementById('current-slide');
    let currentIdx = 0;

    function updateDeck() {
        slides.forEach((slide, index) => {
            if (index === currentIdx) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });
        
        counter.textContent = currentIdx + 1;
        
        prevBtn.disabled = currentIdx === 0;
        nextBtn.disabled = currentIdx === slides.length - 1;
    }

    prevBtn.addEventListener('click', () => {
        if (currentIdx > 0) {
            currentIdx--;
            updateDeck();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentIdx < slides.length - 1) {
            currentIdx++;
            updateDeck();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.code === 'Space') {
            if (currentIdx < slides.length - 1) {
                currentIdx++;
                updateDeck();
            }
        } else if (e.key === 'ArrowLeft') {
            if (currentIdx > 0) {
                currentIdx--;
                updateDeck();
            }
        }
    });
});
