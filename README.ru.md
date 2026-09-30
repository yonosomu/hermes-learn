# hermes-learn

Переносимые навыки обучения и локальные инструменты для **Hermes Agent**.
Оригинальная реализация, вдохновлённая идеями amosblomqvist/learn, а не форк или
расширение Pi. Подробный контракт и ограничения: [English README](README.md).

## Возможности

- `teach`: проверка предпосылок, небольшие уроки, активное воспроизведение,
  исправление заблуждений и проверка переноса знаний на новую задачу.
- `visualize`: Mermaid для связей, SVG для геометрии; запись, точное редактирование,
  необязательный рендеринг и отдельная визуальная проверка результата.
- Самодостаточные задания для researcher, svg-maker и mermaid-maker. Это инструкции
  для `delegate_task`, не автоматически зарегистрированные именованные агенты.
- Нативные инструменты `learn_quiz`, `learn_journal`, `learn_visual` и Python CLI.
- Ответы тестов скрыты в create/show, попытки хранятся в SQLite. Есть один/несколько
  вариантов, объяснение после ответа, заметка, «не знаю» и пропуск.
- Явный структурированный Markdown-журнал, **без** скрытого копирования чата.

Python 3.10+, без обязательных библиотек времени выполнения. PNG требует отдельно
установленного `mmdc` или `rsvg-convert`; установка не выполняется автоматически.
Если рендерера нет, возвращается честный source-only результат без вымышленной PNG.
Созданная PNG ещё не означает, что изображение просмотрено или верно по смыслу.

## Попробовать без изменения профиля

Из корня полного репозитория:

```sh
python -m hermes_learn --help
python -m hermes_learn --data ./learn-data quiz create examples/quiz.json
python -m hermes_learn --data ./learn-data quiz submit QUIZ_ID --answers 1
python -m hermes_learn journal ./session.md goal "Понять граф предпосылок"
python -m hermes_learn visual write ./viz/vector.svg examples/vector.svg
python -m hermes_learn visual render ./viz/vector.svg ./viz/vector.png
```

Замените QUIZ_ID на возвращённый id; индексы начинаются с 1. `--status unknown`
означает «не знаю», `--status skipped` сохраняет пропуск без раскрытия ключа.
Параметры предпочтений выясняются нативным Hermes `clarify` или вопросом в чате.
Ключи всё равно есть в аргументах создания и локальной базе: это не защищённый экзамен.

## Установка в выбранный профиль

```sh
python -m hermes_learn install --home /path/to/profile --dry-run
python -m hermes_learn install --home /path/to/profile
hermes plugins list
hermes plugins enable hermes-learn
hermes plugins doctor /path/to/profile/plugins/hermes-learn --ci
```

Укажите реальный путь выбранного профиля, либо задайте HERMES_HOME. Неявной установки
в действующий профиль нет. Копируются только два навыка, плагин с локальным runtime
и манифест владения. config.yaml и глобальные подсказки не изменяются. Активация
плагина выполняется отдельно командой Hermes в том же профиле; перезапустите сессию.

Существующие каталоги вызывают конфликт. **Сначала самостоятельно сохраните резервную
копию и перенесите личные навыки**. Автоматической перезаписи нет. Удаление откажется
при изменённых/лишних файлах или символических ссылках. Учебные данные сохраняются.
Для обновления используйте резервную копию и последовательность удалить/установить.

```sh
hermes plugins disable hermes-learn
python -m hermes_learn uninstall --home /path/to/profile --dry-run
python -m hermes_learn uninstall --home /path/to/profile
python -m unittest discover -s tests -v
```

`pip install .` ставит CLI, но установка навыков/плагина требует полного checkout.
Журнал создаётся только по согласию и указанному .md пути; он не зашифрован и не
синхронизируется автоматически. Плагин работает с правами пользователя, не в sandbox.
[Безопасность](docs/security.md), [различия](docs/feature-parity.md),
[проверки](docs/verification.md), [авторство](ATTRIBUTION.md). MIT относится только
к оригинальным материалам этого проекта.
