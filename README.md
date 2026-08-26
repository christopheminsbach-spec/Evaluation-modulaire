# Hyrule Quest Board

Application web Django permettant aux aventuriers d'Hyrule de consulter les quêtes et les lieux du royaume.

## Présentation

Hyrule Quest Board est une application développée avec Django permettant de :

- consulter les quêtes disponibles ;
- consulter les quêtes terminées ;
- voir les détails d'une quête ;
- explorer les différents lieux d'Hyrule ;
- voir les quêtes associées à chaque lieu ;
- utiliser un chatbot dédié à l'univers de Zelda ;
- administrer les quêtes et les lieux depuis l'interface Django Admin.

## Architecture

```text
Hyrule Quest Board
│
├── hyrule/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── quests/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   │
│   └── templates/
│       └── quests/
│           ├── base.html
│           ├── home.html
│           ├── quest_list.html
│           ├── quest_detail.html
│           ├── location_list.html
│           ├── location_detail.html
│           └── chat.html
│
├── static/
│   └── css/
│       ├── style.css
│       ├── hyrule-animations.css
│       └── icons/
│           ├── fairy.svg
│           ├── heart.svg
│           ├── hylian-shield.svg
│           ├── hyrule-map.svg
│           ├── master-sword.svg
│           ├── rupee.svg
│           ├── sheikah-eye.svg
│           └── triforce.svg
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md