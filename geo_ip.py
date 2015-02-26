"""
Extract Geo location for an IP address using the Telize Rest Service
Pulls information from a firewall log ufw.log
Requires Python 3
"""
import sys
import json
from urllib import request


def main(ipaddr, num):
    """
    Function calls the Rest API provided by Telize
    """

    json_out = json.load(request.urlopen("http://www.telize.com/geoip/" + ipaddr))
    try:
        return "Ip - {0:>10} - {1:30} Count - {2:>3}\n ".format(
            ipaddr, json_out['country'], num)
    except:
        return ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1], 0)
    else:
        with open("./ufw_max.log", "r") as f, open("results.txt", "w") as outfile:
            ips = f.readlines()
            for i in ips:
                outfile.write(main(i.split()[1], i.split()[0]))
