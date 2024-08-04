# Sysdeep telegram bot

- https://t.me/sysdeep_bot
  - реальный бот
- https://t.me/sysdeep_debug_bot
  - бот для разработки

## TODO

- [ ] webhook
- [x] health
  - [x] uptime
  - [x] hdd
- [ ] отдельный сервис по накаплению данных о валютах

## Python deps

    pip install pytelegrambotapi
    pip install psutil

## Docs

https://pytba.readthedocs.io/ru/latest/quick_start.html#synchronous-telebot
https://www.gitbook.com/book/groosha/telegram-bot-lessons/details

## Token encrypt

Токен хранится в зашифрованном виде в файле token.enc
Для использования его необходимо предварительно расшифровать командой `decode_token.sh PASSWORD`

Инструкции по шифрованию

```bash

# encrypt
openssl enc -k NIKA_HELP_PHRASE -aes256 -base64 -e -in .token -out token.enc

# decrypt
openssl enc -k NIKA_HELP_PHRASE  -aes256 -base64 -d -in token.enc -out .token

```

## Data

- admin: 319597195

## Resources

- https://www.cbr.ru/development/SXML/ - ресурсы для получения данных ЦБРФ
  - https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2024 - котировки за день, если параметр не передать, то за последний день

## Docker

build

```bash
docker build . -t sysdeep_bot:0.1
```

run

```bash
docker run -it -e TOKEN=$(cat .token) --restart unless-stopped --name sysdeep_bot -d sysdeep_bot:0.1
```

## Очистка истории git

В историю были закомичены секреты, пришлось почистить по инструкции которая ниже

https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github

Deleting the .git folder may cause problems in your git repository. If you want to delete all your commit history but keep the code in its current state, it is very safe to do it as in the following:

Checkout/create orphan branch (this branch won't show in git branch command):

    git checkout --orphan latest_branch

Add all the files to the newly created branch:

    git add -A

Commit the changes:

    git commit -am "commit message"

Delete main (default) branch (this step is permanent):

    git branch -D main

Rename the current branch to main:

    git branch -m main

Finally, all changes are completed on your local repository, and force update your remote repository:

    git push -f origin main

PS: This will not keep your old commit history around. Now you should only see your new commit in the history of your git repository.
