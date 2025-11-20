Welcome to the Cadbury Chocolate Hunter repository! Here you'll find a script designed to track down those elusive Cadbury chocolate giveaways before they slip through your fingers faster than a piece of Dairy Milk on a hot day.

Overview
This Python script uses web scraping techniques to check if the Cadbury promotional URLs from starfreebies.co.uk are still live or if they've redirected to the dreaded "missed-out" page. If a URL hasn't hit the "missed-out" status, it opens the page in your default web browser, ready for you to claim your chocolatey treasure.

Features
Automatic URL Checking: The script checks a list of URLs periodically.
Redirect Detection: Identifies whether the URL has redirected to a "missed-out" page or not.
Browser Integration: Automatically opens valid URLs in your web browser for immediate access. 

Usage
To start your Cadbury quest, simply run the script:

bash
python3 cadbury_hunter.py

The script will continuously check the URLs every minute. Here's what happens:

If a URL does not redirect to "missed-out", it will open in your web browser.
If a URL has already been claimed or there's an error, it will log this in the console.

Code Explanation
URL List: A predefined list of URLs pointing to Cadbury chocolate promotions.
check_redirect Function: Uses requests to perform HEAD requests, checking if the URL has been redirected to a "missed-out" page or if it's still active.
Main Loop: Runs indefinitely, checking each URL in the list every 60 seconds, printing status, and opening valid URLs.

python
# Example URL check
def check_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
        # ... rest of the function
    except requests.RequestException as e:
        return False, str(e)

Contributing
Feel free to fork this repository and submit pull requests if you:

Find a new promotional URL for Cadbury chocolates.
Enhance the script's efficiency or error handling.
Add features like notifications via email or push notifications.

Disclaimer
This script is for educational and fun purposes. Use at your own risk.
Please ensure you're not violating any terms of service of starfreebies.co.uk or similar sites when using this tool.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Acknowledgments
Thanks to starfreebies.co.uk for the chocolate promotions.
To the creators of requests library for making HTTP requests in Python a breeze.

Happy hunting for those Cadbury bars! Remember, in the grand scheme of things, life might be absurd, but there's always room for chocolate.
