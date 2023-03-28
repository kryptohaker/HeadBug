import http.client
import json
import sys
from http.cookies import SimpleCookie

banner = '''
###############################################################
#                                                             #
#              HeadBug - Web Header Security Checker          #
#                                                             #
#                 Created by: Kryptohaker                     #
#                                                             #
###############################################################
'''
print(banner)

def load_recommendations(folder):
    recommendations = []
    for file in folder.glob("*.json"):
        with open(file) as f:
            recommendations.append(json.load(f))
    return recommendations

def check_headers(headers, recommendations):
    issues = []
    for recommendation in recommendations:
        header = recommendation["header"]
        if header not in headers:
            issues.append(recommendation["missing_message"])
        else:
            check_func = eval(recommendation["check"])
            header_issues = check_func(headers[header])
            issues.extend(header_issues)
    return issues

def check_cookies(headers, cookie_recommendations):
    issues = []
    for header, value in headers:
        if header.lower() == 'set-cookie':
            cookie = SimpleCookie()
            cookie.load(value)
            for morsel in cookie.values():
                for recommendation in cookie_recommendations:
                    check_func = eval(recommendation["check"])
                    if check_func(morsel):
                        issues.append(recommendation["message"].format(cookie_name=morsel.key))
    return issues

def custom_request(host, path, custom_headers={}):
    for connection_class in [http.client.HTTPConnection, http.client.HTTPSConnection]:
        try:
            conn = connection_class(host)
            conn.request("GET", path, headers=custom_headers)
            response = conn.getresponse()
            return response.getheaders()
        except Exception:
            pass
    raise Exception("Failed to connect to the target using both HTTP and HTTPS")

def main():
    if len(sys.argv) < 2:
        print("Usage: python headbug.py target_url [custom_headers.json]")
        return

    target_url = sys.argv[1]
    custom_headers = {}
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            custom_headers = json.load(f)

    from urllib.parse import urlparse
    url_parts = urlparse(target_url)
    host, path = url_parts.netloc, url_parts.path

    from pathlib import Path
    folder = Path("recommendations")
    recommendations = load_recommendations(folder)

    try:
        headers = custom_request(host, path, custom_headers)
    except Exception as e:
        print(e)
        return

    issues = check_headers(dict(headers), recommendations)

    cookie_folder = Path("cookie_recommendations")
    cookie_recommendations = load_recommendations(cookie_folder)
    cookie_issues = check_cookies(headers, cookie_recommendations)
    issues.extend(cookie_issues)

    if issues:
        print("Security issues found:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("No security issues found.")

if __name__ == "__main__":
    main()
