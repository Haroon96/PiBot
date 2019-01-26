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
- `ytdl`: Download audio from Youtube
- `rms`: Reboot MiniDLNA server
- `status`: Check the status of the bot
- `reboot`: Reboot the device
- `upd`: Update code (Pull from remote repo)
- `lms`: List the media available in media server directory
- `pbd`: Clear base directory
- `upx`: Fetch a new proxy
- `qbt`: Download torrents using qBittorrent
