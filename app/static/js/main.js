document.querySelectorAll("button").forEach((link) => {
    link.addEventListener("click", () => {
        document.getElementById("preloader").style.display = "grid";
    });
});

const input = document.getElementById('searchInput');

input.addEventListener('change', () => {
document.getElementById("preloader").style.display = "grid";    
const query = input.value.trim();
    const baseUrl = window.location.origin + window.location.pathname;
    const newUrl = query ? `${baseUrl}?q=${encodeURIComponent(query)}` : baseUrl;
    window.location.href = newUrl;
});

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();
        const bookItems = document.querySelectorAll('.book-item');
        bookItems.forEach(function(item) {
            const title = item.querySelector('h3').textContent.toLowerCase();
            const author = item.querySelector('p').textContent.toLowerCase();
            if (title.includes(filter) || author.includes(filter)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
});