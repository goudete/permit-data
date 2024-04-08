import requests
from bs4 import BeautifulSoup
import urllib


def find_business_website(business_name):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "__Secure-ENID=13.SE=O-jjp_A24-ab4Cr5Z0FqVxI5fq3BpIcoAfsggbOxtZWUn4AJsVrQznneMoPf8u-6PWarZSOuXkSHLi1ZK27ScFUwCQoCgRZv-jmPDozEJCQFir6jABWDgfmgBD5G2vXDcKSRXtM2mNpE9BMRTMSn-0FUNdERzCwoXbTst9dDFsGSLVRQRuKQMSDsWcw0r_e_-uS4FaYoOebadt5DnNX3o6Axj2SMfUG7SIyf2jS1DJYNPC4onixCOYcPxDWuNmCQnY5hcXBHnzVSle0; SEARCH_SAMESITE=CgQItZoB; S=billing-ui-v3=bYAYXKz3PGT8i8zGG2eSHuZxullx1ijK:billing-ui-v3-efe=bYAYXKz3PGT8i8zGG2eSHuZxullx1ijK; SID=g.a000iQhJDpilyByWRw996anpzyYa3Nx4Aa-9veDczS1WO_hlyE9WjhrBM1aoPiYs01EVaR_5BgACgYKAYsSAQASFQHGX2MiGh_mmTUS37sifJj6Fo-aPBoVAUF8yKpR-v0XvVnScNFgpqVm-BpG0076; __Secur...(line too long; chars omitted)",
        "dnt": "1",
        "referer": "https://www.google.com/",
        "sec-ch-ua": '"Chromium";v="123", "Not:A-Brand";v="8"',
        "sec-ch-ua-arch": '"arm"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"123.0.6312.106"',
        "sec-ch-ua-full-version-list": '"Chromium";v="123.0.6312.106", "Not:A-Brand";v="8.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"macOS"',
        "sec-ch-ua-platform-version": '"14.3.0"',
        "sec-ch-ua-wow64": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "x-client-data": "CPHqygE=",
    }

    query = urllib.parse.quote_plus(business_name)
    try:
        response = requests.get(
            f"https://www.google.com/search?q={query}&sca_esv=0e087ecb039725ea&ei=wvgSZqGfJIzm5NoPjbKDKA&ved=0ahUKEwihiJ3i77CFAxUMM1kFHQ3ZAAUQ4dUDCBA&uact=5&oq={query}&gs_lp=Egxnd3Mtd2l6LXNlcnAiFUpDQyBDT05TVFJVQ1RJT04gQ09SUDIKEAAYRxjWBBiwAzIKEAAYRxjWBBiwAzIKEAAYRxjWBBiwAzIKEAAYRxjWBBiwA0jlBFAAWABwAXgBkAEAmAEAoAEAqgEAuAEDyAEAmAIBoAIPmAMAiAYBkAYEkgcBMaAHAA&sclient=gws-wiz-serp",
            headers=headers,
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with the specific jsname attribute
        a_tags = soup.find_all("a", attrs={"jsname": "UWckNb"})

        # Extract the href attribute value from each tag
        urls = [a["href"] for a in a_tags if a and a.has_attr("href")]

        return urls
    except Exception as e:
        print(f"Request failed for {business_name}:", e)
        return []
