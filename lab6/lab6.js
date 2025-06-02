document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const imageContainer = document.querySelector('.image-container');
    const menuPointer = document.getElementById('menu-pointer');
    const countryMenu = document.getElementById('country-menu');
    
    const countryImages = {
        'france': 'D:/Учеба/WEB/lab6/flag_frantsija_new.jpg',
        'japan': 'D:/Учеба/WEB/lab6/flag_japonija_enl.jpg',
        'usa': 'D:/Учеба/WEB/lab6/flag_usa_enl.jpg',
        'brazil': 'D:/Учеба/WEB/lab6/flag_brazilija_enl.jpg',
        'australia': 'D:/Учеба/WEB/lab6/flag_avstraliya_enl.jpg'
    };
    
    // Инициализация указателя
    updatePointerPosition(document.querySelector('.menu-item.active'));
    
    // Добавляем обработчик наведения на изображение
    document.getElementById('current-image').addEventListener('mouseover', startImageReduction);
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            updatePointerPosition(this);
            
            const country = this.getAttribute('data-country');
            const currentImg = document.getElementById('current-image');
            
            if (currentImg) {
                currentImg.remove();
            }
            
            const newImg = document.createElement('img');
            newImg.src = countryImages[country];
            newImg.alt = this.textContent.trim();
            newImg.className = 'country-image';
            newImg.id = 'current-image';
            newImg.addEventListener('mouseover', startImageReduction);
            
            imageContainer.appendChild(newImg);
        });
    });
    
    function updatePointerPosition(activeItem) {
        const itemRect = activeItem.getBoundingClientRect();
        const menuRect = countryMenu.getBoundingClientRect();
        const pointerLeft = itemRect.left - menuRect.left + itemRect.width / 2;
        menuPointer.style.left = pointerLeft + 'px';
        menuPointer.style.display = 'block';
    }
    
    function startImageReduction() {
        const image = this;
        let imageHeight = image.height;
        
        function reduce() {
            if (imageHeight > 150) {
                imageHeight -= 2;
                image.style.height = imageHeight + "px";
                setTimeout(reduce, 20);
            }
        }
        
        reduce();
        
        // Восстанавливаем размер при уходе курсора
        image.addEventListener('mouseout', function() {
            image.style.height = "400px";
        });
    }
});