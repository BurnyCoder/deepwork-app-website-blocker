import time
import os
import sys
import signal
from threading import Thread, Event
from datetime import datetime as dt

# Path to the hosts file
hosts_path = "/etc/hosts"
# # IP address to redirect to (localhost)
# redirect = "127.0.0.1"
# # List of websites to block
# website_list = [
#     "www.facebook.com",
#     "facebook.com",
#     "www.discord.com",
#     "discord.com",
#     "x.com",
#     "www.x.com",
#     "twitter.com",
#     "www.twitter.com",
#     "reddit.com",
#     "www.reddit.com",
#     "boards.4chan.org",
#     "www.4chan.org",
#     "news.ycombinator.com",
#     "www.ycombinator.com",
#     "ycombinator.com",
#     "www.ycombinator.com",
#     "linkedin.com",
#     "www.linkedin.com"
#
# ]

# twitter_website_list = [
#     "x.com",
#     "twitter.com"
# ]

blocked_etc_host_file_content = """
127.0.0.1  localhost
127.0.1.1  burny-ThinkPad-A485

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
127.0.0.1 www.facebook.com
127.0.0.1 facebook.com
127.0.0.1 www.discord.com
127.0.0.1 discord.com
127.0.0.1 reddit.com
127.0.0.1 www.reddit.com
127.0.0.1 boards.4chan.org
127.0.0.1 www.4chan.org
127.0.0.1 news.ycombinator.com
127.0.0.1 www.ycombinator.com
127.0.0.1 ycombinator.com
127.0.0.1 www.ycombinator.com
127.0.0.1 linkedin.com
127.0.0.1 www.linkedin.com
127.0.0.1 lesswrong.com
127.0.0.1 www.lesswrong.com
127.0.0.1 alignmentforum.org
127.0.0.1 www.alignmentforum.org
127.0.0.1 bsky.app
127.0.0.1 www.bsky.app
0.0.0.0 www.x.com
0.0.0.0 x.com
0.0.0.0 www.twitter.com
0.0.0.0 www.twittter.com
0.0.0.0 www.twttr.com
0.0.0.0 www.twitter.fr
0.0.0.0 www.twitter.jp
0.0.0.0 www.twitter.rs
0.0.0.0 www.twitter.uz
0.0.0.0 twitter.biz
0.0.0.0 twitter.dk
0.0.0.0 twitter.events
0.0.0.0 twitter.ie
0.0.0.0 twitter.je
0.0.0.0 twitter.mobi
0.0.0.0 twitter.nu
0.0.0.0 twitter.pro
0.0.0.0 twitter.su
0.0.0.0 twitter.vn
0.0.0.0 twitter.com
0.0.0.0 *.twitter.com
0.0.0.0 twitter.gd
0.0.0.0 twitter.im
0.0.0.0 twitter.hk
0.0.0.0 twitter.jp
0.0.0.0 twitter.ch
0.0.0.0 twitter.pt
0.0.0.0 twitter.rs
0.0.0.0 www.twitter.com.br
0.0.0.0 twitter.ae
0.0.0.0 twitter.eus
0.0.0.0 twitter.hk
0.0.0.0 ns1.p34.dynect.net
0.0.0.0 ns2.p34.dynect.net
0.0.0.0 ns3.p34.dynect.net
0.0.0.0 ns4.p34.dynect.net
0.0.0.0 d01-01.ns.twtrdns.net
0.0.0.0 d01-02.ns.twtrdns.net
0.0.0.0 a.r06.twtrdns.net
0.0.0.0 b.r06.twtrdns.net
0.0.0.0 c.r06.twtrdns.net
0.0.0.0 d.r06.twtrdns.net
0.0.0.0 api-34-0-0.twitter.com
0.0.0.0 api-47-0-0.twitter.com
0.0.0.0 cheddar.twitter.com
0.0.0.0 goldenglobes.twitter.com
0.0.0.0 mx003.twitter.com
0.0.0.0 pop-api.twitter.com
0.0.0.0 spring-chicken-an.twitter.com
0.0.0.0 spruce-goose-ae.twitter.com
0.0.0.0 takeflight.twitter.com
0.0.0.0 www2.twitter.com
0.0.0.0 m.twitter.com
0.0.0.0 mobile.twitter.com
0.0.0.0 api.twitter.com
"""
# +"""
# 127.0.0.1 cs.wikipedia.org
# 127.0.0.1 www.cs.wikipedia.org
# 127.0.0.1 en.wikipedia.org
# 127.0.0.1 www.en.wikipedia.org
# 127.0.0.1 wikipedia.org
# 127.0.0.1 www.wikipedia.org
# """

unblocked_etc_host_file_content = """
127.0.0.1  localhost
127.0.1.1  burny-ThinkPad-A485

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
"""

app_list = [
    "telegram-desktop"
]

stop_event = Event()

def on():

    #for website in twitter_website_list:
        #with open("/etc/squid/squid.conf", "a") as squid_conf:
            #squid_conf.write("acl block_" + website.replace(".", "_") + " dstdomain ." + website + "\n")
            #squid_conf.write("http_access deny block_" + website.replace(".", "_") + "\n")
    
    #    os.system("sudo iptables -I OUTPUT -m string --string \"" + website + "\" --algo bm -j REJECT")
    #    os.system("sudo iptables -I FORWARD -m string --string \"" + website + "\" --algo bm -j REJECT")
    print("Opening the hosts file to block websites.")
    with open(hosts_path, 'w') as file:
        file.write(blocked_etc_host_file_content)
        
        # content = file.read()
        # for website in website_list:
        #     if website not in content:
        #         #print(f"Blocking {website}")
        #         # Redirect the website to localhost
        #         file.write(redirect + " " + website + "\n")
        
        
                
    print("Entering loop to kill specified applications.")
    while not stop_event.is_set():
        for app in app_list:
            os.system(f"pkill -f {app}")
        time.sleep(2)
    print("Exiting blocking loop.")

def off():
    
    #with open("/etc/squid/squid.conf", "w") as squid_conf:
        #squid_conf.write("")

    #for website in twitter_website_list:
    #    os.system("sudo iptables -D OUTPUT -m string --string \"" + website + "\" --algo bm -j REJECT")
    #    os.system("sudo iptables -D FORWARD -m string --string \"" + website + "\" --algo bm -j REJECT")


    print("Opening the hosts file to unblock websites.")
    with open(hosts_path, 'w') as file:
        file.write(unblocked_etc_host_file_content)
        
        # content = file.readlines()
        # file.seek(0)
        # for line in content:
        #     if not any(website in line for website in website_list):
        #         #print(f"Unblocking {line}")  
        #         file.write(line)
        # # Truncate the file to remove the remaining lines
        # file.truncate()
        
    print("Websites unblocked.")

def listen_for_commands():
    while True:
        command = input("Enter command (on/off): \n").lower()
        if "on" in command:
            if not stop_event.is_set():
                print("Blocking mode is already on.")
            else:
                stop_event.clear()
                print("Turning on blocking mode.")
                t = Thread(target=on)
                t.start()
        elif "off" in command:
            if stop_event.is_set():
                print("Blocking mode is already off.")
            else:
                print("Please type the following commitment to continue:\nI agree that im not going to procrastinate in the middle of cool deep work session and ruin it that way")
                commitment = "i agree that im not going to procrastinate in the middle of cool deep work session and ruin it that way"
                user_input = input("Type here: \n")
                if commitment in user_input.lower() :
                    print("Commitment acknowledged. Proceeding with the session.")
                    print("Turning off blocking mode.")
                    stop_event.set()
                    off()
                else:
                    print("Commitment not acknowledged. Exiting.")
                    return
        else:
            print("Unknown command. Please enter 'on' or 'off'.")

if __name__ == "__main__":
    stop_event.clear()
    print("Turning on blocking mode.")
    t = Thread(target=on)
    t.start()
    print("Starting command listener. Type 'on' or 'off' to control the blocking mode.")
    listen_for_commands()