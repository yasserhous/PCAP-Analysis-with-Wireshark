# Wireshark_Tutorial
For this lab, The focus will be on understanding the indicators of infection of windows client through pcap analysis using wireshark. We will be following the malware traffic analysis exercise from malware-traffic-analysis.net , and answering the questions. the exercise will be solving is the following: https://malware-traffic-analysis.net/2025/01/22/index.html.

#Background povided:
You work as an analyst at a Security Operation Center (SOC). Someone contacts your team to report a coworker has downloaded a suspicious file after searching for Google Authenticator. The caller provides some information similar to social media posts at:

https://www.linkedin.com/posts/unit42_2025-01-22-wednesday-a-malicious-ad-led-activity-7288213662329192450-ky3V/
https://x.com/Unit42_Intel/status/1882448037030584611
Based on the caller's initial information, you confirm there was an infection.  You retrieve a packet capture (pcap) of the associated traffic.  Reviewing the traffic, you find several indicators matching details from a Github page referenced in the above social media posts.  After confirming an infection happened, you begin writing an incident report.


#Tasks

For this exercise, answer the following questions for your incident report:

What is the IP address of the infected Windows client?
What is the mac address of the infected Windows client?
What is the host name of the infected Windows client?
What is the user account name from the infected Windows client?
What is the likely domain name for the fake Google Authenticator page?
What are the IP addresses used for C2 servers for this infection?

# Step 1: Download the post infection pcap file provided by the exercise
## Step 1.1: For the filw password, you can review the following page: https://malware-traffic-analysis.net/about.html


# Step 2: setup file sharing between the host machine and the virtual machine
## Step 2.2: spinning up a quick python server on the host machine
1. open command prompt from the location of the file you want to share with VM
2. 2.run the following python command: python -m http.server 8080
3. From your VM, run the following command on the terminal: wget http://192.168.56.1:8080/yourfile.txt

# Step 3: Setup your Wireshark display
1. Remove the packet No column, and change the time display format column to represent the date and time of day


![Step 3 malware analysis - Made with Clipchamp](https://github.com/user-attachments/assets/350cabbb-bd8c-444b-b8c2-c63f05bdab5b)


sources:
https://malware-traffic-analysis.net/2025/01/22/index.html
https://www.youtube.com/watch?v=3t1BNAavrlQ&t=11s
