# ROB RUN Справочник — Telegram Mini App + бот-помощник

Устроен так же, как D9 Справочник:
- `RobRun_Guide/` — мини-приложение (один файл `index.html` + `sw.js`), хостинг GitHub Pages:
  `https://pochtamur228-png.github.io/robrun-guide/`
- `RobRun_Bot/` — бот на Cloudflare Worker `robrun-helper` (напоминания о рейде и новых штатах, отзывы, /news, /stats).

## Что умеет
- **Гайд**: с чего начать, роли, деньги, арест и взятка, игра за копа, ограбления, база, тюрьма, FPS. У каждого пункта есть пометка:
  «в игре», «точно» или «не подтверждено».
- **Вайп**: таймер федерального рейда в твоём штате (регион и день открытия), таймер нового штата, что сгорит и что останется.
- **Счёт**: цена у скупщика или контрабандиста с бонусом известности, срок после рейда, отмывка.
- **Инфо**: ссылка на YouTube-канал, «Что нового», форма «нашёл ошибку» (уходит владельцу в бота).
- **Бот**: /remind — напоминание о рейде за сутки и за 2 часа, новые штаты EU/US за 15 минут; /raid, /app, /idea;
  владельцу ещё /stats и /news.

## Запуск (один раз)
1. **@BotFather** → `/newbot` → имя «ROB RUN Помощник», username — у нас `rob_runhelper_bot`.
   Токен никому не присылай, его вводишь сам в шаге 3.
   `/setuserpic` → `assets/avatar.png`.
2. **GitHub Pages**: репозиторий `robrun-guide` с содержимым этой папки, затем Settings → Pages → main / root.
3. **Cloudflare** (из папки `RobRun_Bot`):
   ```
   npx.cmd wrangler kv namespace create SUBS      # id вписать в wrangler.toml
   npx.cmd wrangler secret put BOT_TOKEN          # вставить токен из BotFather
   npx.cmd wrangler deploy
   ```
   Потом открыть `https://robrun-helper.9--ot.workers.dev/setup`: он регистрирует вебхук, команды, кнопку «Справочник» и описание.
4. **@BotFather** → `/newapp` → выбрать бота → обложка `assets/cover.png` → ссылка из шага 2 → короткое имя `app`.
   Прямая ссылка на справочник: `t.me/<бот>/app`.

Username бота — константа `BOT` в `index.html`.

## Обновления
- Данные — массивы `GUIDE`, `HEISTS`, `LOSE`, `KEEP` в начале скрипта `index.html`.
- На каждый релиз добавляй запись в `NEWS`, а при изменении файлов из кэша поднимай `V` в `sw.js`.
- Картинки: `python -I assets/make_art.py`.
