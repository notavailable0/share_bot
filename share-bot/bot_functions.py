import requests

def check_for_active_apk(package_name):

    url = 'https://play.google.com/store/apps/details?id=' + str(package_name)
    html_response = requests.get(url).text
    print(html_response)

    if """We're sorry, the requested URL was not found on this server.""" in html_response:
        return '404'
    else:
        return '000'

