# Pokemon TCG matchup-maker / backend

This script is built to combine matchup data from rk9labs.com to the decklist data from LimitlessTCG.com. The aim is to build a tool that allows easy way to see how certain matchups are statistically.

**Current version is very experimental and in-progress.**

## Build and run

Requires Python 3.7 and virtualenv.

You also need to [install Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) and [install geckodriver](https://github.com/mozilla/geckodriver/releases) matching your operating system and make sure it is in PATH. We're using Firefox as our browser with Selenium to access Limitless's page that is loaded via Javascript.

```
$ pip3.7 install -r requirements.txt
$ python main.py <rk9_labs_id> <limitless_tcg_id>
```

`<rk9_labs_id>` refers to the alpha numeric code in the url (https://player.rk9labs.com/pairings/D04B1A60 => D04B1A60) and `<limitless_tcg_id>` refers to the tournament id in Limitless url (http://limitlesstcg.com/tournaments/?id=116 => 116).

## LICENSE

Copyright 2018 Juha-Matti Santala

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.