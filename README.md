# active-forks

> Find the active github forks of a project

_NOTE: Looking for maintainer(s) to keep this project going_

While I want to be able to spend some time on this, I've had a lot of changes in life in general
and thus can not spend as much time on this repo. If you are interested in taking over to maintain
this project, please file an issue.

This project allows you to find the most active forks of a repository.

[Find Active Fork](https://techgaun.github.io/active-forks/index.html)

## GitHub Forks PDF Report Generator

Generate a comprehensive PDF report of all your GitHub forks with detailed information including stars, last update date, language, and more.

### Prerequisites

- Python 3.6+
- GitHub account

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

**Basic Usage (without authentication):**
```bash
python generate_forks_pdf.py
```

**With GitHub Token (recommended for higher rate limits):**

On Linux/macOS:
```bash
export GITHUB_TOKEN=your_github_token_here
python generate_forks_pdf.py
```

On Windows (Command Prompt):
```cmd
set GITHUB_TOKEN=your_github_token_here
python generate_forks_pdf.py
```

### Output

The script generates a PDF file named `forks_report.pdf` containing:

- **Summary Table:** Repository names, descriptions, stars, language, and last updated dates
- **Detailed List:** Full URLs, descriptions, star count, fork count, open issues, language, created date, and last updated date/time

### Customization

Edit `generate_forks_pdf.py` to:

- **Change username:** Modify `USERNAME = 'EeveeVictoria'` (line 108)
- **Change output filename:** Modify `OUTPUT_FILE = 'forks_report.pdf'` (line 109)

## As Bookmarklet

If you would like to use this tool as a bookmarklet,
you can do so by saving the following javascript code as the bookmarklet.
Since Github doesn't allow javascript in its markdown, you can add it manually.
Hit `Ctrl+D` to create a new bookmark and paste the javascript below into the URL
or "Location" entry (you may have to click "More" to see the URL field).
Any time you're on a Github repo you can click the bookmarklet
and it'll bring up the Active Forks of that repo.

```javascript
javascript:(function(){if(window.location.hostname.match(/github.com+/)){var%20a=window.location.pathname.split('/',3);if(a.length==3){var%20b=encodeURIComponent(a[1]+'/'+a[2]);window.open('https:[...]
```

![Active Forks in Action](screenshot.png "Active Forks in Action")

## Licensing

This repository is available under either [the Apache License version 2.0](LICENSE) or (at your option) [the European Union Public License version 1.2](LICENSE-ALT).

`SPDX-License-Identifier: Apache-2.0 OR EUPL-1.2`
