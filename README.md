# Teledax Api

## [ Check Official Repo + Web Version ](https://github.com/odysseusmax/tg-index)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](.) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

[![](https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png)](https://play.google.com/store/apps/details?id=com.tele.dax)

## Deploy Guide

- **Clone to local machine.**

```bash
$ git clone https://github.com/odysseusmax/tg-index.git
$ cd tg-index
```

- **Create and activate virtual environment.**

```bash
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

- **Install dependencies.**

```bash
$ pip3 install -U -r requirements.txt
```

- **Environment Variables.**

| Variable Name               | Value                                                                                                                                                          |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `API_ID` (required)         | Telegram api_id obtained from https://my.telegram.org/apps.                                                                                                    |
| `API_HASH` (required)       | Telegram api_hash obtained from https://my.telegram.org/apps.                                                                                                  |
| `INDEX_SETTINGS` (required) | See the below description.                                                                                                                                     |
| `SESSION_STRING` (required) | String obtained by running `$ python3 app/generate_session_string.py`. (Login with the telegram account which is a participant of the given channel (or chat). |
| `PRIVATEKEY` (required) | your Password to access Your api |

| `PORT` (optional)           | Port on which app should listen to, defaults to 8080.                                                                                                          |
| `HOST` (optional)           | Host name on which app should listen to, defaults to 0.0.0.0.                                                                                                  |
| `DEBUG` (optional)          | Give some value to set logging level to debug, info by default.                                                                                                |

- **Setting value for `INDEX_SETTINGS`**

This is the general format, change the values of corresponding fields as your requirements.

```
{
    "index_all": true,
    "index_private":false,
    "index_group": false,
    "index_channel": true,
    "exclude_chats": [],
    "include_chats": [],
}
```

> - `index_all` - Whether to consider all the chats associated with the telegram account. Value should either be `true` or `false`.
> - `index_private` - Whether to index private chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> - `index_group` - Whether to index group chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> - `index_channel` - Whether to index channels. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> - `exclude_chats` - An array/list of chat id's that should be ignored for indexing. Only considered if `index_all` is set to `true`.
> - `include_chats` - An array/list of chat id's to index. Only considered if `index_all` is set to `false`.

- **Run app.**

```bash
$ python3 -m app
```

- **Other quick methods.**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/aryanvikash/teledaxApi/tree/master) [![Run on Repl.it](https://repl.it/badge/github/aryanvikash/teledaxApi)](https://repl.it/github/aryanvikash/teledaxApi)

## Contributions

Contributions are welcome.

## Credit ❤️

original repo is created by [@odysseusmax](https://tx.me/odysseusmax).

## License

Code released under [The GNU General Public License](LICENSE).
