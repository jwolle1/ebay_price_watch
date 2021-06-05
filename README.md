This script uses the eBay Finding API to search listings and alert the user via email when a target price is reached. It interfaces with the API using the [_ebaysdk_](https://github.com/timotheus/ebaysdk-python) library.

The script filters auction, local pickup, and non-US listings. It includes the ability to set a price minimum and to ignore specific URLs.

You'll need an [eBay developer account](https://developer.ebay.com/products/developer) to use the script. Set your `APP_ID` at the top of `main.py` before running. I usually run this script as a cron job. Remember to respect eBay API rate limits.

You'll also need an email address capable of sending email with _smtplib_ from the Python standard library. `email_server` address and `email_port` number will vary depending on the email service. Sometimes services will require you to verify your identity before sending messages.

---

**To use:**

1. The only required dependency outside the standard library is _ebaysdk_. To install it run `pip3 install ebaysdk`.
2. Set desired options at the top of `main.py` and run.

---

_Note: Never store your login credentials as plain text. Please store them in an encrypted format and import as needed._
