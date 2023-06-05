# job-scraper
Python package for scraping job events

## Overview

This python package scrapes all the internships for an IT engineer from [外資就活ドットコム](https://gaishishukatsu.com/recruiting_info). Currently, only this website is supported, but I'll improve this package so that information in various websites can be scraped.

## Motivation

I'm searching for a job. However, I'm a Ph.D student and have to do research too. I don't want to spend much time on job hunting. In order to decrease time for job hunting, I have decided to automate job events check by web scraping.

## Prerequisites

This package needs WebDriver for Google Chrome. If you use Mac, you can install it by Homebrew.

```shell
$ brew install chromedriver
```

## Installation

```shell
$ cd <job-scraper's root>
$ pip install .
```

## Usage

You can display helpfull messages by executing the following command.

```shell
Usage: job-scraper [OPTIONS]

  Scrape job events from a website, https://gaishishukatsu.com/

Options:
  --output_filename TEXT  Path to output file.  [default: event_info.json]
  --help                  Show this message and exit.
```

### Scrape internship list

Run the following command.

```shell
$ job-scraper
```

If the command execution end, you'll see a file in your current directory. You can change the location of a output file.
