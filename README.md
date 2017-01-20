# Grailed Notify

A simple Python script that notifies you via email on deals on Grailed you would have otherwise missed. Select your favourite designers, along with the categories and sizing you're interested in, with an optional minimum and maximum price.

## Installation

### 1. Clone the repository

`git clone https://github.com/benva/grailed-notify.git`

### 2. Go to the directory

`cd grailed-notify`

### 3. Install the dependencies

`sudo pip install -r requirements.txt`

## Getting Started

### 1. Edit the values to your specifications

Open `main.py` and edit `designers`, `categories`, `sizes`, `prices`, and `address` to match your needs. All values must be valid and the filters must exist on Grailed.

### 2. Run the script

`python main.py`

### 3. Enter your e-mail password

`Password for <grailed-notify@gmail.com>:` will show up prompting you for your password. Your password is not saved anywhere, just used to sign in. If you have application-specific passwords set up, you must use that.

### 4. Wait

Alerts of new listings matching your specifications will be emailed to you as long as the script is running, just wait!
