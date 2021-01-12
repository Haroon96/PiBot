# PiBot

A Telegram bot for running and managing tasks on a Raspberry Pi. Mostly built for my use but you can modify the code to your liking.

## Features
- Runs common shell commands
- Automated subtitle downloading for torrents
- Automatic proxy management via site scraping (if Telegram is inaccessible in your location)
- Downloading audio from YouTube
- Remote code updating using `git pull`
- Modular design for further enhancements
- Independent configurations for easy integration

## Command List
- `mdl`: Download audio from YouTube and embed metadata using [gTagger](https://github.com/haroon96/gTagger)
- `vdl`: Download video from YouTube
- `rms`: Reboot MiniDLNA server
- `status`: Check the status of the bot
- `reboot`: Reboot the device
- `upd`: Update code (Pull from remote repo)
- `lms`: List the media available in media server directory
- `pbd`: Clear base directory
- `upx`: Fetch a new proxy
- `qbt`: Download torrents using qBittorrent

## Setting up and configuration
- Adjust the settings in `config.tmpl.json` for your Pi and rename it to `config.json`. Set `bot_token` to your bot's API token. Set `master_chat_id` to your primary chat that will receive uninitiated messages (e.g., torrent updates). 
- [Instructions here. Only follow instructions for receiving your Chat ID and API token.](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#telegram-setup)
- Use any torrent client. I use [qBittorrent](https://qbittorrent.org/) with RSS feeds setup for automated downloading. Set your client to run `torrent_module.py <path-to your-download>` when a torrent is finished downloading. It'll scan the download directory for video files and move them to your mediaserver location.
- If the path to the file contains `subs_download_directory`, it will also softcode subtitles into the video file before moving it to the server, after waiting for `subs_wait_period` seconds.
- Anybody can send a command to the bot. The bot only sends uninitiated messages to `master_chat_id`.
- Set the `use_proxy` flag if you want the bot to use a proxy. You can specify the `proxy_url` or let the bot find one itself using the `upx` command or just call the `update_proxy` method inside `proxy_manager.py`.
- `base_directory` serves as the root folder where the bot will operate. `media_server_directory` and `subs_download_directory` will be inside this folder.
- Additionally, use [gTagger](https://github.com/haroon96/gTagger.git) to automatically embed metadata to music downloaded from YouTube. Set `genius_api_token` to your [Genius.com API token](https://genius.com/developers). 
