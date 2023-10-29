# job-scraper
Python package for scraping job events

## Overview

This python package scrapes all the internships for an IT engineer from [外資就活ドットコム](https://gaishishukatsu.com/recruiting_info). Currently, only this website is supported, but I'll improve this package so that information in various websites can be scraped.

## Motivation

I'm searching for a job. However, I'm a Ph.D student and have to do research too. I don't want to spend much time on job hunting. In order to decrease time for job hunting, I have decided to automate job events check by web scraping.

## Prerequisites

This package needs WebDriver for Google Chrome.

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

  Python package for scraping job events

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

By `job-scraper company` command, you can scrape information about all the companies in a industry from [外資就活ドットコム](https://gaishishukatsu.com/company). You need to pass `--industry` option to the command. Available values can be checked from help as below.

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

If the command execution end, you'll see a output file in your current directory. You can change the location of it.
