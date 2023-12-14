# job-scraper

CLI application for scraping information about Japanese companies.

## Overview

This app scrapes information about companies (e.g. available internship and basic information about companies) posted on [外資就活ドットコム](https://gaishishukatsu.com/). Currently, only this website is supported.

## Motivation

I'm searching for a job. However, I'm a Ph.D student and have to do research too. I don't have much time for job hunting. In order to find companies good for me efficiently, I have decided to automate information gathering by web scraping.

## Prerequisites

This app needs Google Chrome.

### Windows

Here, I suppose you are using WSL(Windows Subsystem for Linux).

1. Install Google Chrome for Linux on WSL.

```shell
$ sudo apt update
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
# If dependency error is raised, run the following command
$ sudo apt --fix-broken install

# Check whether installation succeeds or not
$ google-chrome-stable --version
$ rm -f google-chrome-stable_current_amd64.deb
```

2. Install a Windows X-server, e.g. `VcXsrv`.

## Installation

```shell
$ cd job-scraper
$ pip install .
```

## Usage

You can display helpfull messages by executing the following command.

```shell
$ job-scraper --help
Usage: job-scraper [OPTIONS] COMMAND [ARGS]...

  Python package for scraping information about Japanese companies

Options:
  --help  Show this message and exit.

Commands:
  company  Scrape company information from a website,...
  intern   Scrape job events from a website, https://gaishishukatsu.com/
```

You can also display help for each subcommand.

```shell
$ job-scraper company --help
```

### Scrape company list

By `job-scraper company` command, you can scrape information about companies in a specified industry posted on [外資就活ドットコム](https://gaishishukatsu.com/company). You need to pass `--industry` option to the command. Available values can be viewed from help as below.

```shell
$ job-scraper company --help
Usage: job-scraper company [OPTIONS]

  Scrape company information from a website, https://gaishishukatsu.com/

Options:
  --industry [consultant|gaishi_finance|nikkei_finance|gaishi_maker_service|trading|civil_servant|it_service|nikkei_maker|media|construction]
                                  Industry which you are interested in.
                                  [required]
  --output_filename TEXT          Path to output file.  [default:
                                  company_info.csv]
  --login / --no-login            Whether to login to the website or not.
  --gui / --no-gui                Whether to display a browser or not.
  --help                          Show this message and exit.
```

For example, you can parse information about all the consulting companies.

```shell
$ job-scraper company --industry consultant
```

### Scrape internship list

Run the following command.

```shell
$ job-scraper intern
```

If the command execution ends, you'll see an output file in your current directory. You can change the location of it.
