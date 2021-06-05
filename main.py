from ebaysdk.finding import Connection as finding
import smtplib


'''
For listings that calculate shipping cost based on the buyer's location, the API does not
return a price. You can set a `default_shipping_price` for those cases.

`ignore` is a list of URLs that will not trigger an alert.

When `verbose` is True the script prints all filtered search results.
'''

search_terms = "breath of the wild nintendo switch"
target_price = 40.00
price_minimum = 30.00
default_shipping_price = 5.00
ignore = []
verbose = True

APP_ID = "__YourAppID__"

email_server = "smtp.gmail.com"
email_port = 587
from_address = "sender@email.com"
email_pass = "SenderPassword123"
to_address = "recipient@email.com"


# #################### # #################### # #################### # ####################


def email(msg):
    """Sends an email alert if target price is found or if the script encounters an error.

    :param msg: email body text
    :type msg: string
    """
    server = smtplib.SMTP(email_server, email_port)
    server.ehlo()
    server.starttls()
    server.login(from_address, email_pass)
    server.sendmail(from_address, to_address, f"Subject: **eBay Price Alert**\n{msg}")
    server.quit()
    return


def search():
    """Execute an API call and return a list of search results sorted by price.

    :rtype: list
    :return: sorted list of tuples
    """
    api = finding(appid=APP_ID, config_file=None, https=True)
    response = api.execute("findItemsByKeywords", {"keywords": search_terms})
    results = response.reply.searchResult.item

    output = {}

    for item in results:
        ignore_flag = False

        if item.country != "US":
            ignore_flag = True
        elif item.shippingInfo.shippingType == "FreePickup":
            ignore_flag = True
        elif item.listingInfo.listingType == "Auction":
            ignore_flag = True

        if not ignore_flag:
            title = item.title
            url = item.viewItemURL
            list_price = float(item.sellingStatus.currentPrice.value)
            if item.shippingInfo.shippingType in ["Free", "Flat", "FlatDomesticCalculatedInternational"]:
                shipping_price = float(item.shippingInfo.shippingServiceCost.value)
            else:
                shipping_price = default_shipping_price
            price = list_price + shipping_price
            if price >= price_minimum and url not in ignore:
                output.update({(title, url, list_price, shipping_price): price})

    return sorted(zip(output.values(), output.keys()))


if __name__ == "__main__":
    try:
        results_filtered = search()

        if verbose:
            for item in results_filtered:
                print(f"${item[0]:.2f} ... ({item[1][2]:.2f} + {item[1][3]:.2f})")
                print(item[1][0])
                print(item[1][1], end="\n\n")

        email_message = ""

        for item in results_filtered:
            if item[0] > target_price:
                break
            email_message += f"${item[0]:.2f} ... ({item[1][2]:.2f} + {item[1][3]:.2f})\n{item[1][0]}\n{item[1][1]}\n\n"

        if email_message:
            email(email_message)

    except Exception as e:
        email(f"Error --> {e}")
