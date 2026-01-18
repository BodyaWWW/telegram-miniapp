function addToCart(name, price, image) {
    let cartCount = document.getElementById('cart-count');
    cartCount.textContent = parseInt(cartCount.textContent) + 1;

    let notification = document.getElementById('notification');
    notification.textContent = `${name} добавлен в корзину!`;
    notification.style.display = 'block';
    setTimeout(() => notification.style.display = 'none', 3000);
}

function applyFilters() {
    let metal = document.getElementById('metal-filter').value.toLowerCase();
    let year = document.getElementById('year-filter').value;
    let price = document.getElementById('price-filter').value;

    document.querySelectorAll('.product-card').forEach(card => {
        let cardMetal = card.getAttribute('data-metal').toLowerCase();
        let cardYear = card.getAttribute('data-year');
        let cardPrice = card.getAttribute('data-price');

        if ((metal && cardMetal !== metal) || (year && cardYear !== year) || (price && cardPrice > price)) {
            card.style.display = 'none';
        } else {
            card.style.display = 'block';
        }
    });
}
// script.js

document.getElementById('shop').addEventListener('click', function() {
    alert('Ты в магазине!');
});

document.getElementById('categories').addEventListener('click', function() {
    alert('Ты в категориях!');
});

document.getElementById('favorites').addEventListener('click', function() {
    alert('Ты в избранном!');
});

document.getElementById('cart').addEventListener('click', function() {
    alert('Ты в корзине!');
});
function toggleFavorite(coinId) {
      let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
      if (favorites.includes(coinId)) {
        // Если товар уже в списке понравившихся, удаляем его
        favorites = favorites.filter(id => id !== coinId);
      } else {
        // Если товара нет в списке, добавляем его
        favorites.push(coinId);
      }
      localStorage.setItem('favorites', JSON.stringify(favorites));
      updateHeartButton(coinId);
    }

    // Функция для обновления состояния кнопки сердца
    function updateHeartButton(coinId) {
      let heartButton = document.querySelector(`[data-id="${coinId}"] .heart-button`);
      let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
      if (favorites.includes(coinId)) {
        heartButton.classList.add('liked');
      } else {
        heartButton.classList.remove('liked');
      }
    }

    // Функция для отображения страницы с понравившимися товарами
    function showFavorites() {
      let favoritesSection = document.getElementById('favorites-section');
      let favoritesList = document.getElementById('favorites-list');
      favoritesList.innerHTML = ''; // Очищаем список перед обновлением

      let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

      if (favorites.length === 0) {
        favoritesList.innerHTML = '<p>У вас нет понравившихся товаров.</p>';
      } else {
        // Здесь мы будем искать товары по id из списка понравившихся
        {% for coin in coins %}
          if (favorites.includes({{ coin.id }})) {
            let productDiv = document.createElement('div');
            productDiv.classList.add('lg:w-1/4', 'md:w-1/2', 'p-4', 'w-full');
            productDiv.innerHTML = `
              <div class="block relative h-48 rounded overflow-hidden">
                <img alt="{{ coin.name }}" class="object-cover object-center w-full h-full block" src="{{ coin.image.url }}">
              </div>
              <div class="mt-4">
                <h3 class="text-gray-500 text-xs tracking-widest title-font mb-1">{{ coin.name }}</h3>
                <h2 class="text-gray-900 title-font text-lg font-medium">{{ coin.price }}₴</h2>
                <p class="text-sm text-gray-500">Тираж: {{ coin.circulation }} шт.</p>
                <p class="text-sm text-gray-500">Матеріал: {{ coin.material }}</p>
              </div>
            `;
            favoritesList.appendChild(productDiv);
          }
        {% endfor %}
      }

      favoritesSection.classList.remove('hidden');
    }

    // Обновление кнопок сердечек на странице
    document.addEventListener('DOMContentLoaded', () => {
      let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
      favorites.forEach(coinId => {
        updateHeartButton(coinId);
      });
    });