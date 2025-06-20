# Видалення фону з картинок

Цей скрипт автоматично видаляє фон з картинок за допомогою штучного інтелекту. Використовує бібліотеку `rembg` для високоякісного видалення фону.

**[English version](remove_background_README_EN.md)**

## Встановлення

1. Переконайтеся, що у вас встановлений Python 3.7+
2. Встановіть необхідні залежності:

```bash
pip install rembg Pillow
```

або оновіть `requirements.txt`:

```bash
echo "rembg" >> requirements.txt
pip install -r requirements.txt
```

## Використання

### Базове використання
```bash
python remove_background.py картинка.jpg
```

### З додатковими параметрами
```bash
# Вказати ім'я вихідного файлу
python remove_background.py картинка.jpg -o результат.png

# Використовувати alpha matting для кращої якості
python remove_background.py картинка.jpg -a

# Комбінація параметрів
python remove_background.py картинка.jpg -o результат.png -a
```

### Розширені налаштування alpha matting
```bash
python remove_background.py картинка.jpg -a \
    --foreground-threshold 250 \
    --background-threshold 5 \
    --erode-size 15
```

### Параметри

- `image_path` - шлях до картинки (обов'язковий)
- `-o, --output` - ім'я вихідного файлу (за замовчуванням: додається '_no_bg.png')
- `-a, --alpha-matting` - використовувати alpha matting для кращої якості
- `--foreground-threshold` - поріг для переднього плану (за замовчуванням: 240)
- `--background-threshold` - поріг для фону (за замовчуванням: 10)
- `--erode-size` - розмір ерозії (за замовчуванням: 10)

## Підтримувані формати

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- та інші формати, що підтримуються бібліотекою Pillow

## Особливості

- **Автоматичне видалення фону** за допомогою штучного інтелекту
- **Alpha matting** для кращої якості обробки складних країв
- **Збереження в PNG** з прозорим фоном
- **Налаштування параметрів** для різних типів картинок
- **Швидка обробка** для простих випадків

## Режими роботи

### Стандартний режим
- Швидка обробка
- Хороша якість для більшості картинок
- Автоматичне визначення об'єкта

### Alpha matting режим
- Повільніша обробка
- Краща якість для складних країв
- Налаштування параметрів для точного контролю

## Приклади використання

### Для різьблення по дереву
```bash
# Видалити фон з фотографії різьблення
python remove_background.py різьблення.jpg -o різьблення_чисте.png

# Використати alpha matting для кращої якості
python remove_background.py різьблення.jpg -a -o різьблення_високої_якості.png
```

### Для логотипів та ілюстрацій
```bash
# Швидке видалення фону
python remove_background.py логотип.png

# Висока якість для складних деталей
python remove_background.py логотип.png -a --foreground-threshold 255
```

## 👼 Ручна доробка маски прозорості

1. Запустіть видалення фону з опцією `--save-mask`:
   ```bash
   python remove_background.py ваша_картинка.jpg -a --save-mask
   ```
2. Відкрийте маску (`ваша_картинка_no_bg_mask.png`) у графічному редакторі, підправте деталі та збережіть.
3. Застосуйте маску до оригінального зображення:
   ```bash
   python apply_mask.py ваша_картинка.jpg ваша_картинка_no_bg_mask.png -o ваша_картинка_final.png
   ```

**Скрипт `apply_mask.py` входить до складу проекту!**

## Поради

1. **Для простих об'єктів** використовуйте стандартний режим
2. **Для складних країв** (волосся, хутро, прозорість) використовуйте alpha matting
3. **Результат завжди зберігається в PNG** для підтримки прозорості
4. **Експериментуйте з параметрами** alpha matting для найкращого результату

## Вимоги до системи

- Python 3.7+
- Мінімум 2GB RAM
- Інтернет-з'єднання для першого запуску (завантаження моделі) 