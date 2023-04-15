import urllib.request as rq

def good_ke_jian_request(url):
    html = rq.urlopen(url)
    return html.read()


if __name__ == "__main__":
    url = "http://goodkejian.com/mulu/sxrj.htm"
    html = good_ke_jian_request(url)
    print(html)
