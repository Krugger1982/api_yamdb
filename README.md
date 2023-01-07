# api_yamdb
api_yamdb


Это реализация интерфейса api для работы с сервисом YAMDB, который позволяет хранить и добавлять отзывы
и оценки к медиаконтенту (фильмам, музыке, книгам), различных жанров, а также комментировать эти отзывы

## При помощи api- интерфейса реализованы возможности:
- зарегистрироваться как пользователь, получить токен авторизации,
- прочитать отзывы других пользователей на произведение, написать(изменить, удалить) свой,
- прочитать комментарии других пользователей к отзыву, написать(изменить, удалить) свой.

Отзывы и комментарии модерируются.
Администратор сервиса имеет право удалять пользователей (по их просьбе или за нарушения порядка)

## Технологии, использованные при разработке
- python 3.7  
- Django 3.2
- djangorestframework 3.12.4  

## Установка

Для того чтоб установить проект на локальную машину клонируйте репозиторий  
```
git clone https://github.com/Krugger1982/
```

### Запуск

Для запуска проекта в режиме разработчика установите и активируйте виртуальное окружение.  
Cоздание виртуального окружения:  
```
$ python3 -m venv venv
```

Активация виртуального окружения:  
```$ source venv/bin/activate``` (команда для Linux/MacOS)  
или:  
```$ source venv/Scripts/activate``` (команда для Windows)  
при активированном виртуальном окружении установите зависимости из файла requirements.txt
выполните команду:  
```$ pip install -r requirements.txt```

В папке с файлом manage.py выполните команду запуска сервера:  
```$ python3 manage.py runserver```  

### Работа сервиса  
  
Обращаться к сервису можно по следующим эндпойнтам:  

`api/v1/signup/`                    
    
    (POST): передаём username и email, получаем код подтвержденияна электронную почту (доступно без токена).

`api/v1/token/`           

    (POST): передаём username и confirmation_code, получаем токен (доступно без токена)

`api/v1/categories/`                
    
    (GET): получить список категорий(доступно без токена)

    POST): добавить категорию (Права доступа: Администратор).  

`api/v1/categories/<slug>`          
    
    (DELETE): удалить категорию (Права доступа: Администратор). 

`api/v1/genres/`                    
    (GET): получить список жанров(доступно без токена)

    (POST): добавить новый жанр (Права доступа: Администратор)
                                    .  
`api/v1/genres/{slug}`              
                                    
    (DELETE): удалить жанр (Права доступа: Администратор). 

`api/v1/titles/`

    (GET): получить список произведний(доступно без токена)

    (POST): добавить произведение (Права доступа: Администратор).  

`api/v1/titles/{title_id}`          
    
    (GET): получить данные о произведнии(доступно без токена)

    (PATCH): изменить данные о произведении (Права доступа: Администратор).  

    (DELETE): удалить произведение (Права доступа: Администратор). 

`api/v1/titles/{title_id}/reviews/` 
    
    (GET): получить список отзывов на произвелдение(доступно без токена)

    (POST): добавить новый отзыв (Права доступа - аутентифицированный пользователь)

`api/v1/titles/{title_id}/reviews/{review_id}`
                                    
    (GET): получить отзыв по его id (Доступно без токена)

    (POST): добавить новый отзыв (Права доступа - аутентифицированный пользователь)   

    (PATCH): изменить данные об отзыве (Права доступа: Автор отзыва, модератор или администратор).  

    (DELETE): удалить отзыв (Права доступа: Автор отзыва, модератор или администратор). 

`api/v1/titles/{title_id}/reviews/{review_id}/comments/`
                                    
    (GET): получить список комментов на отзыв(доступно без токена)

    (POST): добавить новый комментарий (Права доступа - аутентифицированный пользователь)

`api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
                                    
    (GET): получить комментарий по его id (Доступно без токена)

    (PATCH): изменить данные о комментарии (Права доступа: Автор комментария, модератор или администратор).  

    (DELETE): удалить комментарий (Права доступа: Автор комментария, модератор или администратор). 

`api/v1/users/`                     

    (GET): получить список всех пользователей (Права доступа: администратор)

    (POST): добавить нового пользователя (Права доступа: администратор)

`api/v1/users/{username}/`         

    (GET): получить данные пользователя по его username (Права доступа: администратор)

    (PATCH): изменить данные о пользователе по его username (Права доступа: администратор).  

    (DELETE): удалить пользователя по его username (Права доступа: администратор). 

`api/v1/users/me/`             

    (GET): получить данные своей учетной записи(Права доступа: аутентифицированный пользователь)

    (PATCH): изменить данные своей учетной записи(Права доступа: аутентифицированный пользователь)

Авторы:
Алексей
Виктор
Влад