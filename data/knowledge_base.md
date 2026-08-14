# Digiplus IT Support - Standard Operating Procedures (SOPs)

## 1. Network & VPN Issues
- **Hotel/Public Wi-Fi**: Users experiencing VPN drops on public Wi-Fi should be advised to lower their MTU size or use TCP mode on the VPN client. 
- **Account Lockouts**: If a user is locked out of Active Directory, they must be verified via manager approval before unlocking.

## 2. Hardware Requests
- **Printers (Zebra)**: Zebra label printers must be added manually via IP address (10.x.x.x). Drivers are pre-installed on the network share `\\digiplus-fs\drivers`.
- **Laptops & Peripherals**: Missing webcams or Bluetooth devices usually require a BIOS update or reseating the physical cable if the device manager does not detect them at all.

## 3. General Security
- **Suspicious Emails/Spam**: Never click links. Isolate the affected inbox, run a malware scan, and report the sender domain to the security team for blacklisting.
- **VIP Accounts**: Any ticket submitted by C-level executives (CEO, CFO, CTO) must be escalated to a Senior Engineer immediately and requires a phone call follow-up.
