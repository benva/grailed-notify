# Grailed Notify

A simple Python script that notifies you via email on deals on Grailed you would have otherwise missed. Select your favourite designers, along with the categories and sizing you're interested in, with a minimum and maximum price.

## Installation

### 1. Clone the repository

`git clone https://github.com/benva/grailed-notify.git`

### 2. Go to the directory

`cd grailed-notify`

### 3. Install the dependencies

`sudo pip install -r requirements.txt`

### 4. Tailor to your OS

Change the line `browser = webdriver.Chrome("./bin/chromedriver-mac")` in `grailednotify.py` to `"./bin/chromedriver-linux32"`, `"./bin/chromedriver-linux64"`, or `"./bin/chromedriver.exe"` depending on your OS.

## Getting Started

### 1. Edit the values to your specifications

Open `main.py` and edit `designers`, `categories`, `sizes`, `prices`, `address`, and `os` to match your needs. All values must be valid and the filters must exist on Grailed.

### 2. Run the script

`python main.py`

### 3. Enter your e-mail password

`Password for <someone@site.com>:` will show up in the terminal prompting you for your password. Your password is not saved anywhere, just used to sign in. If you have application-specific passwords set up, you must use that.

### 4. Wait

Alerts of new listings matching your specifications will be emailed to you as long as the script is running, just wait!

### 5. Ending the script

Make sure you are in the terminal and hit `Ctrl+C` to terminate the script.

## To-do

### Robustness

In general, could use a bit more robustness.

### E-mail preview

When sending emails, give a preview (designer, picture, item name, price) with the link.

### HTML Front-end

Implement a HTML page with all the filters that would replace `main.py`.
