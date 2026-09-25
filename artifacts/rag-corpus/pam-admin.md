# PAM Administrative Guide.pdf

Source: `data/sources/PAM Administrative Guide.pdf` - 702 pages.

## [p1]

www.arconnet.com | Copyright © 2025

## [p2]

www.arconnet.com|Copyright © 2025 2
Disclaimer
The handbook of ARCON PAM solution is being published to guide stakeholders and users. If any of the
statements in this document are at variance or inconsistent, they shall be brought to the notice of ARCON
through the support team. Wherever appropriate, references have been made to facilitate a better
understanding of the PAM solution. ARCON team has made every effort to ensure that the information
contained in it was correct at the time of publishing.
Nothing in this document constitutes a guarantee, warranty, or license, expressed or implied. ARCON disclaims
all liability for all such guarantees, warranties, and licenses, including but not limited to: Fitness for a particular
purpose; merchantability; non-infringement of intellectual property or other rights of any third party or of
ARCON; indemnity; and all others. The reader is advised that third parties can have intellectual property rights
that can be relevant to this document and the technologies discussed herein, and is advised to seek the advice
of competent legal counsel, without obligation of ARCON.
Copyright Notice
Copyright © 2025 ARCON All rights reserved.
ARCON retains the right to make changes to this document at any time without notice. ARCON makes no
warranty for the use of this document and assumes no responsibility for any errors that can appear in the
document, nor does it make a commitment to update the information contained herein.
Trademarks
Other product and corporate names may be trademarks of other companies and are used only for explanation
and to the owners' benefit, without intent to infringe.

## [p3]

www.arconnet.com|Copyright © 2025 3
Table of Contents
1 Introduction to ARCON Privileged Access Management (PAM) ..............................................................................7
2 Why ARCON PAM is Important and Beneficial for Organizations...........................................................................8
3 Quick Start Guide..........................................................................................................................................................................9
3.1 Overview .......................................................................................................................................................................................9
3.2 Section 1: Admin Modules ......................................................................................................................................................9
3.2.1 1. Server Manager................................................................................................................................................................... 9
3.2.2 2. Session Monitoring ............................................................................................................................................................ 9
3.2.3 3. AD Bridging........................................................................................................................................................................... 9
3.2.4 4. Digital Vault / Password Vault ...................................................................................................................................... 9
3.2.5 5. Auto Onboarding..............................................................................................................................................................10
3.2.6 6. PAM Logs .............................................................................................................................................................................10
3.2.7 7. My Vault (Admin)..............................................................................................................................................................10
3.2.8 8. Spection................................................................................................................................................................................10
3.2.9 9. Settings .................................................................................................................................................................................10
3.2.10 10. IDAM (Identity Access Management) ...................................................................................................................11
3.2.11 11. User Access Governance ............................................................................................................................................11
3.2.12 12. Administrator Console ................................................................................................................................................11
3.2.13 13. My Vault Enterprise......................................................................................................................................................11
3.2.14 14. Access Control ................................................................................................................................................................11
3.2.15 15. User Discovery................................................................................................................................................................11
3.2.16 16. Reports...............................................................................................................................................................................12
3.3 Section 2: ACMO Modules .................................................................................................................................................. 12
3.3.1 1. Script Manager ..................................................................................................................................................................12
3.3.2 2. Dashboard ...........................................................................................................................................................................12
3.3.3 3. My Services .........................................................................................................................................................................12
3.3.4 4. My Preferences .................................................................................................................................................................12
3.3.5 5. Raise Request.....................................................................................................................................................................12
3.3.6 6. Pending Request ...............................................................................................................................................................13
3.3.7 7. Request Logs ......................................................................................................................................................................13
3.3.8 8. My Activity ..........................................................................................................................................................................13
3.3.9 Support......................................................................................................................................................................................13
4 Getting Started ........................................................................................................................................................................... 14
4.1 This Section Includes: ............................................................................................................................................................ 14

## [p4]

www.arconnet.com|Copyright © 2025 4
4.2 Login Management ................................................................................................................................................................. 14
4.2.1 Overview ..................................................................................................................................................................................14
4.2.2 ACMO Login............................................................................................................................................................................14
4.2.3 License Information .............................................................................................................................................................17
4.3 Administrator Access (Admin Access)............................................................................................................................ 19
4.3.1 Overview ..................................................................................................................................................................................19
4.3.1.1 This Section Includes: ....................................................................................................................................................... 19
4.3.2 Command Profiler.................................................................................................................................................................19
4.3.2.1 What is Command Profiler? ........................................................................................................................................... 19
4.3.2.2 Why is Command Profiler Important?....................................................................................................................... 19
4.3.2.3 Processes Management................................................................................................................................................... 20
4.3.2.4 Commands Management................................................................................................................................................ 44
4.3.3 Privilege Management ........................................................................................................................................................77
4.3.3.1 Assign or Revoke Privileges from Admin or Client Users .................................................................................. 77
4.3.3.2 Client Manager's Privileges ........................................................................................................................................... 79
4.3.3.3 Server's Privileges.............................................................................................................................................................. 96
4.3.3.4 Group Admin Privilege...................................................................................................................................................113
4.3.4 Password Vault ................................................................................................................................................................... 114
4.3.4.1 What is ARCON | Password Vault?...........................................................................................................................114
4.3.4.2 Why use ARCON | Password Vault?.........................................................................................................................115
4.3.4.3 What is Password Management in ARCON | Password Vault?.....................................................................115
4.3.4.4 Dashboard Password Vault..........................................................................................................................................115
4.3.4.5 Password Envelope .........................................................................................................................................................120
4.3.4.6 Auto Healing ......................................................................................................................................................................124
4.3.4.7 Password Policy In Password Vault..........................................................................................................................126
4.3.4.8 Password Connectors ....................................................................................................................................................131
4.3.4.9 Password Rotate ..............................................................................................................................................................137
4.3.4.10 Password Reconciliation In Password Vault.........................................................................................................142
4.3.4.11 Service Vault ......................................................................................................................................................................145
4.3.4.12 Password Logs...................................................................................................................................................................183
4.3.4.13 Downloads ..........................................................................................................................................................................187
4.3.5 Tool Management .............................................................................................................................................................. 191
4.3.5.1 What is Tool Management? .........................................................................................................................................191
4.3.5.2 Why is Tool Management Important? .....................................................................................................................191
4.3.5.3 Service Discovery.............................................................................................................................................................192

## [p5]

www.arconnet.com|Copyright © 2025 5
4.3.5.4 Windows Utility ................................................................................................................................................................193
4.3.5.5 Privilege User Discovery and Reconciliation ........................................................................................................196
4.3.5.6 Real-Time Session Monitoring....................................................................................................................................205
4.3.5.7 Import ...................................................................................................................................................................................208
4.3.6 Workflow Management .................................................................................................................................................. 224
4.3.6.1 What is workflow Management ? ..............................................................................................................................224
4.3.6.2 Workflow Logs ..................................................................................................................................................................224
4.3.7 Settings................................................................................................................................................................................... 233
4.3.7.1 LOB(s) ...................................................................................................................................................................................234
4.3.7.2 Group ....................................................................................................................................................................................246
4.3.7.3 User Settings......................................................................................................................................................................277
4.3.7.4 Service Setting...................................................................................................................................................................291
4.3.7.5 Password .............................................................................................................................................................................315
4.3.7.6 Alert & Notifications .......................................................................................................................................................355
4.3.7.7 Workflow.............................................................................................................................................................................373
4.3.7.8 Session ..................................................................................................................................................................................388
4.3.7.9 Domain .................................................................................................................................................................................393
4.3.7.10 Ticket.....................................................................................................................................................................................397
4.3.7.11 Logs ........................................................................................................................................................................................403
4.3.7.12 Network/Connection .....................................................................................................................................................436
4.3.7.13 API ..........................................................................................................................................................................................447
4.3.7.14 General .................................................................................................................................................................................459
4.3.7.15 My Vault...............................................................................................................................................................................479
4.3.7.16 Cloud .....................................................................................................................................................................................479
4.3.7.17 Configures...........................................................................................................................................................................483
4.3.7.18 PAM Plugin Configuration ...........................................................................................................................................493
4.3.8 Logs Management.............................................................................................................................................................. 496
4.3.8.1 Overview .............................................................................................................................................................................496
4.3.8.2 Service Logs........................................................................................................................................................................496
4.3.8.3 Process Logs.......................................................................................................................................................................499
4.3.8.4 MetaData/Text Logs.......................................................................................................................................................503
4.3.8.5 User Activity Log ..............................................................................................................................................................505
4.3.8.6 Command Logs..................................................................................................................................................................507
4.3.8.7 ARCON PAM Logs...........................................................................................................................................................511
4.3.8.8 User Access Logs ..............................................................................................................................................................517

## [p6]

www.arconnet.com|Copyright © 2025 6
4.3.8.9 User Validity Status.........................................................................................................................................................518
4.3.8.10 Service Password Status ...............................................................................................................................................520
4.3.8.11 Service Reference Logs..................................................................................................................................................522
4.3.8.12 Import Utility Logs ...........................................................................................................................................................523
4.3.8.13 Envelope Logs....................................................................................................................................................................525
4.3.9 Entity Management and Mapping ............................................................................................................................... 526
4.3.9.1 What is Entity Management and Mapping?...........................................................................................................526
4.3.9.2 Why is Entity Management Needed?.......................................................................................................................527
4.3.9.3 LOB ........................................................................................................................................................................................527
4.3.9.4 User........................................................................................................................................................................................529
4.3.9.5 Service ..................................................................................................................................................................................623
4.3.9.6 Revoke and Share.............................................................................................................................................................656
4.3.9.7 Groups ..................................................................................................................................................................................663
4.3.9.8 Mappings .............................................................................................................................................................................670
5 PAM Access and Dashboard............................................................................................................................................... 701

## [p7]

www.arconnet.com|Copyright © 2025 7
1 Introduction to ARCON Privileged Access Management (PAM)
In the age of digital transformation, cybersecurity threats are evolving rapidly, and the need to secure critical
infrastructure and sensitive data has become more urgent than ever. One of the most significant vulnerabilities
in any IT environment lies in privileged accounts  with elevated access rights that can substantially change
systems, applications, and data. Misuse of these accounts, intentional or accidental, can lead to severe data
breaches, operational disruptions, and compliance failures.
ARCON Privileged Access Management (PAM)  is a comprehensive cybersecurity solution designed to
proactively manage and secure privileged access across an organization’s IT landscape. ARCON PAM acts as a
secure gateway between users and critical systems by enabling granular access control, real-time monitoring,
and comprehensive auditing of all privileged sessions.
ARCON PAM is built to support complex IT environments, including on-premise, cloud, and hybrid
infrastructures. It ensures that only authorized users have the right level of access to perform their roles, and
only for the required duration. The platform incorporates advanced features such as password vaulting, role-
based access control, session recording, behavioral analytics, and risk-based authentication.

## [p8]

www.arconnet.com|Copyright © 2025 8
1.
2.
3.
4.
5.
6.
7.
2 Why ARCON PAM is Important and Beneficial for Organizations
Mitigates Insider and External Threats
Privileged accounts are a prime target for cyberattackers. ARCON PAM helps organizations
significantly reduce the risk of insider threats and external attacks by monitoring and controlling access
to sensitive systems in real time.
Enforces the Principle of Least Privilege (PoLP)
By granting users the minimum access required to perform their tasks, ARCON PAM helps reduce the
attack surface and prevent unauthorized actions within the IT environment.
Strengthens Compliance and Audit Readiness
ARCON PAM provides detailed audit trails, session recordings, and access logs, essential for meeting
regulatory requirements such as GDPR, HIPAA, SOX, and ISO 27001. This not only helps in compliance
but also improves transparency and accountability.
Enhances Operational Efficiency
The centralized management console and automated access workflows help IT teams manage user
access more efficiently while reducing administrative overhead.
Supports Digital Transformation
As organizations adopt cloud, DevOps, and remote work environments, ARCON PAM ensures that
privileged access is secured across diverse platforms, supporting seamless and secure digital operations.
Real-time Monitoring and Alerts
With real-time session monitoring and risk-based alerts, organizations can immediately detect unusual
or unauthorized activities and proactively mitigate potential threats.
Secure Third-Party Access
ARCON PAM also allows secure and controlled access for third-party vendors and contractors, ensuring
that external users can perform necessary tasks without compromising system security.
In conclusion, ARCON PAM is not just a security tool, but a strategic solution that enables organizations to
maintain control over their most sensitive IT assets. By minimizing risk, improving compliance posture, and
enhancing visibility, ARCON PAM is critical in building a resilient cybersecurity framework for modern
enterprises.

## [p9]

www.arconnet.com|Copyright © 2025 9
•
•
a.
b.
c.
d.
e.
f.
•
•
a.
b.
c.
d.
•
•
a.
b.
c.
d.
•
•
a.
3 Quick Start Guide
3.1 Overview
ARCON Privileged Access Management (PAM) provides a secure platform to manage privileged accounts,
sessions, and activities within an IT environment. This guide is a comprehensive introduction to both Admin and
ACMO functionalities, helping users and administrators understand and navigate the platform efficiently.
3.2 Section 1: Admin Modules
These modules are focused on configuring and maintaining secure access controls, system integrations, identity
lifecycle, and audit readiness.
3.2.1 1. Server Manager
Purpose: Register and maintain an inventory of target servers and devices.
Steps:
Navigate to Server Manager under Admin console.
Click Add Server.
Enter hostname/IP, OS type, connection type (SSH, RDP, etc.).
Configure credentials (manual, vaulted, or AD-based).
Assign to groups for access control and monitoring.
Test connectivity and save.
3.2.2 2. Session Monitoring
Purpose: Real-time monitoring and playback of privileged user sessions.
Steps:
Go to Session Monitoring > Live Sessions.
Monitor sessions using filters (user, server, time).
Click on a session to view playback.
Use Video Audit Trail for evidence and compliance.
3.2.3 3. AD Bridging
Purpose: Integrate Active Directory for user authentication and access management.
Steps:
Go to AD Bridging.
Add AD domain, enter credentials, and test connection.
Sync user groups and assign to ARCON roles.
Define policies for authentication and authorization.
3.2.4 4. Digital Vault / Password Vault
Purpose: Store, manage, and rotate passwords securely.
Steps:
Navigate to Password Vault.

## [p10]

www.arconnet.com|Copyright © 2025 10
b.
c.
d.
•
•
a.
b.
c.
d.
•
•
a.
b.
c.
•
•
a.
b.
c.
•
•
a.
b.
c.
•
•
a.
b.
c.
Add credentials manually or import.
Set rotation policies (interval, complexity, exceptions).
Apply access control rules for usage.
3.2.5 5. Auto Onboarding
Purpose: Automatically discover and register assets and users.
Steps:
Go to Auto Onboarding.
Schedule a discovery scan (IP range, directory).
Review discovered servers and users.
Assign them to policies and credential groups.
3.2.6 6. PAM Logs
Purpose: View detailed logs for operations, user actions, and system events.
Steps:
Access PAM Logs.
Filter by module, action, user, or date.
Export logs for auditing or compliance.
3.2.7 7. My Vault (Admin)
Purpose: Personal vault space for Admins to manage and view owned credentials.
Steps:
Go to My Vault.
Access or modify credentials.
View usage history and audit logs.
3.2.8 8. Spection
Purpose: Advanced policy-based access management engine.
Steps:
Define policies for usage (time, user, purpose).
Assign to systems or services.
Monitor compliance reports and policy hits.
3.2.9 9. Settings
Purpose: Global configuration for platform behaviors, alerts, and features.
Steps:
Navigate to Settings > General / Security / Notification.
Update system-wide policies.
Integrate with 3rd party tools (SIEM, ticketing systems).

## [p11]

www.arconnet.com|Copyright © 2025 11
•
•
a.
b.
c.
•
•
a.
b.
c.
•
•
•
•
a.
b.
•
•
a.
b.
c.
•
•
a.
b.
c.
3.2.10 10. IDAM (Identity Access Management)
Purpose: Manage the full lifecycle of user identities.
Steps:
Add/import users.
Define access roles and entitlements.
Automate provisioning/deprovisioning.
3.2.11 11. User Access Governance
Purpose: Periodic review and certification of access rights.
Steps:
Launch Access Review Campaign.
Define scope (users, groups, roles).
Review and take actions (approve, revoke, comment).
3.2.12 12. Administrator Console
Purpose: Centralized dashboard for administrative control.
Features:
License management.
Policy review.
Health monitoring and alerts.
3.2.13 13. My Vault Enterprise
Purpose: Organization-wide credential vaulting with RBAC controls.
Steps:
Organize credentials by departments.
Assign access to roles or teams.
3.2.14 14. Access Control
Purpose: Define access policies based on user, device, time, and justification.
Steps:
Create new policies.
Specify target systems, access method, timing constraints.
Assign to users or groups.
3.2.15 15. User Discovery
Purpose: Discover unmanaged user accounts across endpoints.
Steps:
Scan defined IP ranges or AD trees.
Identify orphaned or risky accounts.
Take actions (onboard/remove/flag).

## [p12]

www.arconnet.com|Copyright © 2025 12
•
•
a.
b.
c.
•
•
a.
b.
c.
d.
•
•
a.
b.
•
•
a.
b.
•
•
•
•
a.
b.
3.2.16 16. Reports
Purpose: Generate visual or tabular data for compliance, auditing, and review.
Steps:
Select report template (access log, activity, risk, etc.).
Customize filters.
Export to PDF/CSV or schedule automatic delivery.
3.3 Section 2: ACMO Modules
Modules for Access Control and Monitoring Operations (ACMO) to request, track, and audit their access.
3.3.1 1. Script Manager
Purpose: Securely run admin-approved scripts on target servers.
Steps:
Go to Script Manager.
Upload or write scripts in portal.
Tag with categories and assign to roles.
Execute with logging and approval.
3.3.2 2. Dashboard
Purpose: View system status, active requests, and user-specific insights.
Steps:
Customize widgets.
Pin frequently accessed resources.
3.3.3 3. My Services
Purpose: View services the user is entitled to access.
Steps:
Select a service (RDP, SSH, App).
Launch session directly or request if restricted.
3.3.4 4. My Preferences
Purpose: Personalize the user portal.
Options:
Language, notifications, interface theme, dashboard layout.
3.3.5 5. Raise Request
Purpose: Request access to privileged resources.
Steps:
Fill in system/service details.
Specify duration, justification, and urgency.

## [p13]

www.arconnet.com|Copyright © 2025 13
c.
•
•
a.
b.
•
•
a.
b.
•
•
•
•
Submit for workflow approval.
3.3.6 6. Pending Request
Purpose: Track approval process of access requests.
Steps:
Review current status (Pending, Approved, Rejected).
Cancel or modify request if needed.
3.3.7 7. Request Logs
Purpose: View history of raised requests.
Steps:
Filter by system, type, date.
Export for reporting.
3.3.8 8. My Activity
Purpose: User-centric activity dashboard.
Features:
View session start/end time, usage history.
Track request lifecycle.
3.3.9 Support
For configuration help or troubleshooting:
Refer to the official ARCON PAM documentation.
Contact your system administrator or security team.

## [p14]

www.arconnet.com|Copyright © 2025 14
•
•
•
•
•
•
•
1.
4 Getting Started
After logging into PAM, this section provides a comprehensive starting point for new users. It helps them
understand the essential features, navigate the interface with ease, and quickly become familiar with the core
functionalities needed to begin using the platform effectively.
4.1 This Section Includes:
Login Management
License Information
Key Features
Use Cases
PAM Access and Dashboard
4.2 Login Management
4.2.1 Overview
In computer security, logging in (or logging on or signing in or signing on) is the process by which an individual
gains access to a computer system or an application by identifying and authenticating themselves through user
credentials. The user credentials are basically the username and password, which are sometimes referred to as
a login, (or a logon, or a sign-in, or a sign-on). In addition, due to digital thefts and breaches, modern secure
systems often use a second authorization for extra security of their application. Hence, ARCON PAM uses this
second or dual-factor authorization for mobile OTP, SMS OTP, biometric devices, and hardware token
configuration.
This Section Includes:
ACMO Login
License Information
4.2.2 ACMO Login
Server Manager in Privileged Access Management (PAM) that controls elevated access permissions for
network users or systems, ensuring security through features like access request approvals, activity logging,
and policy enforcement.
Follow the below steps to log into Server Manager:
Enter the URL <http(s)://ip-address:port> in the address bar. The ARCON PAM Login screen is
displayed.

## [p15]

www.arconnet.com|Copyright © 2025 15
2.
3.
The ARCON PAM login screen contains the following fields:
Field Name Description
Username Enter the username.
Password Enter the password.
Domain Select the domain from the dropdown list.
Enter the credentials in the above fields and click on the login   button, viewed in the application.
The ARCON PAM Home screen is displayed. Click the Manager menu.

## [p16]

www.arconnet.com|Copyright © 2025 16
4.
5.
The My Apps screen is displayed. Click the Server Manager icon.
Click OK. The ARCON PAM Server Manager Home screen is displayed.
Client Users having Manager Menu Display privilege will only be able to view Manager menu in Client
Manager.

## [p17]

www.arconnet.com|Copyright © 2025 17
4.2.3 License Information
After successfully logging in to PAM, you can view the license information from the main user interface.
To do this, select License Details from the left navigation panel.
•
•
•
The error messages displayed for the login attempt failure by Users are as follows:
The User is Dormant error message is displayed, if User attempts to login into the application
exceeding the dormancy days configured in Application Configuration.
The User is Lockout error message is displayed, if User attempts to enter invalid password
more than configured lockout attempts configured in Application Configuration.
The User is Disabled error message is displayed, If user validity is expired or admin has
manually disabled the user

## [p18]

www.arconnet.com|Copyright © 2025 18
The License details screen is displayed.
Select Current License Details to view both the current license information and the count of unused licenses.
•
•
To view license information, a user must have the License Configuration privilege.
A warning message is displayed 30 days before the license expires.

## [p19]

www.arconnet.com|Copyright © 2025 19
•
•
•
•
•
•
•
•
•
•
•
•
•
•
4.3 Administrator Access (Admin Access)
4.3.1 Overview
ARCON | Privileged Access Management (PAM) offers robust controls to manage and monitor administrative
access to critical systems and applications. By enforcing strict access policies, it ensures that only authorized
administrators can access privileged accounts, systems, and infrastructure components—based on predefined
roles, workflows, and approval mechanisms.
4.3.1.1 This Section Includes:
Command Profiler
Privilege Management
Administrative Console
Password Vault
Access Control
Workflow Management
Settings
Logs Management
Tool Management
IDAM
Privileged User Discovery
Entity Management and Mapping
4.3.2 Command Profiler
4.3.2.1 What is Command Profiler?
Command Profiler is used to restrict or elevate processes or commands. You can assign commands with the
Critical With Approval property, wherein an email notification will be sent to the Approver for approval. Once
approved, the command will be allowed for execution. This feature is used by the Administrator who is
responsible for keeping track of unwanted or critical commands or processes that should/should not be
executed by the user on the server. Multiple profiles can be created for each service type.
4.3.2.2 Why is Command Profiler Important?
Command Profiler enhances security by restricting the execution of high-risk or sensitive commands, ensuring
they are only run with proper oversight. It helps prevent misuse, enforces accountability, and supports
compliance by allowing administrators to monitor, control, and approve critical actions in real-time across
various service environments.
4.3.2.2.1 Following are the two types of profiles created:
Blacklist: Blacklist is a method for adding processes or commands that are required to be blocked.
Elevate: Elevate is a method to allow the user to execute certain processes.

## [p20]

www.arconnet.com|Copyright © 2025 20
1.
2.
3.
4.
Also, new processes or commands can be added to the existing set of processes and commands. In addition, you
can modify and delete a command profiler. To Blacklist or Elevate the processes or commands for the service
type the Administrator has to check the checkbox beside the processes or commands listed.
4.3.2.3 Processes Management
4.3.2.3.1 What is Process Management?
This section helps you know about the TS Plugin service and how this service is used to blacklist and elevate
Windows processes in ARCON. This service is installed on servers having 2003, 2008, 2008 R2, and 2012 R2
Windows operating system. A process restricted to you will not be allowed for access whereas an elevated
process will be made available to perform any action. This plugin can also help you to capture process logs.
4.3.2.3.2 Why do we need Process Management?
The TS Plugin enhances security by preventing unauthorized or risky processes from being executed and
ensuring only approved actions are performed on critical systems. It also supports monitoring and forensic
analysis by capturing detailed logs of process-level activity, helping administrators enforce control and visibility
over privileged user behavior.
To manage processes, follow the below steps:
TS Plugin Installation
Create Profile
Assign TS Monitor Command To Service
Assign Profiles and Restrict or Elevate Processes
•
•
•
For Windows Services we can use blacklist and elevate as profile type whereas, for Linux
services, only blacklist profile type can be used.
The Administrator having Command Profiler  privilege will only be able to create, modify, or
delete multiple profiles. The Administrator can also create, delete commands or restrict
commands and processes available for the User.
All the restricted commands can be used once the administrator deleted the command profiler.
•
•
The Administrator having Change User Restricted Commands in Server's Privileges privilege
shall only be able to apply Blacklist and Elevate profiles.
You will be able to install TS Plugin only if you have Administrator level privileges.

## [p21]

www.arconnet.com|Copyright © 2025 21
4.3.2.3.3 Process Flow Diagram

## [p22]

www.arconnet.com|Copyright © 2025 22
•
4.3.2.3.4 TS Plugin Installation
4.3.2.3.4.1 Pre-requisites
ARCOS TS Plugin Setup.msi file on the server

## [p23]

www.arconnet.com|Copyright © 2025 23
•
•
1.
2.
3.
PAMAPI URL
WebDT Web Service
4.3.2.3.5 How to Install TS Plugin?
To install TS Plugin, proceed with the following steps:
Double-click on the setup file, the following screen is displayed.
Click Next.
Browse and select the folder for installation as shown in the preceding screen and click Next.

## [p24]

www.arconnet.com|Copyright © 2025 24
4.
5.
Confirm the installation and click Next. The installation process will start automatically.
The installation process is completed. Click Close. Once TS Plugin is installed on the server, you can
check that the service is running on services.msc console.

## [p25]

www.arconnet.com|Copyright © 2025 25
6.
7.
1.
2.
Go to Run (Windows + R) and enter services.msc.
Click OK to view the TS Plugin service running on the server.
4.3.2.3.6 How to Create Profiles?
This section helps you to create profiles and then assign processes to the profile. For example - we will create
two profiles Blacklist and Elevate.
To create Profiles, follow the below steps:
Click on the ARCON PAM link ( https://devint.arconnet.com:1302/).
Enter the Credentials and click on the Login button.

## [p26]

www.arconnet.com|Copyright © 2025 26
3.
4.
My Services screen is displayed:
Click on the Manager. My Apps screen is displayed:

## [p27]

www.arconnet.com|Copyright © 2025 27
5.
6.
7.
Click on Server Manager.
Click on Server Manager or Server Manager with AGW.
Navigate to, Manage > Command Profiler:
What is AGW?
Application Gateway Server (AGW) is a solution that controls all the entry points into your
environment. The AGW Server is placed in a secure environment and monitored at all times.
Remote sessions can be taken from the AGW Server to other applications and machines.

## [p28]

www.arconnet.com|Copyright © 2025 28
8.
9.
10.
11.
12.
The Command Profiler screen is displayed. Click on the Process tab:
Click on Create radio button.
Enter Profile Name, For example, Blacklist.
Select Profile Type as Blacklist.
Select Is Active checkbox, and then Click on Create. The following pop-up screen is displayed.

## [p29]

www.arconnet.com|Copyright © 2025 29
13.
14.
15.
16.
Click OK. The created profile is now listed in the grid view.
Select the Created Profile. List of default processes available for the profile:
Select the required processes to be assigned to the profile and click Apply Changes, to create a profile.
Similarly, create another Profile for Elevate.
4.3.2.3.7 How to Add New Process?
This section helps you to add processes to a profile.
To add a new process, use the following path:
Manage > Command Profiler:

## [p30]

www.arconnet.com|Copyright © 2025 30
1.
a.
b.
c.
d.
e.
2.
Follow the below steps:
Select the Processes tab and click Add New Process link. The Add Process window is displayed:
The Add Process contains the following fields:
Description
Command Name
Process Name
Process Title
Process Path
Enter the details and click on the Modify button, to add a process to the default list of processes.
4.3.2.3.8 How to Modify Details of Process?
This section helps you to modify the details of a process.
To modify the details of a process, use the following navigation path:

## [p31]

www.arconnet.com|Copyright © 2025 31
1.
2.
3.
Manage > Command Profiler:
Follow the below steps:
Select the Processes tab. The Profiles created in Command Profiler are displayed.
Select the required Profile Name. The processes belonging to the particular profile are displayed:
Double-click on the required process. The Modify Process pop-up screen is displayed:

## [p32]

www.arconnet.com|Copyright © 2025 32
4.
1.
Modify the required details and click Modify, to update the details.
4.3.2.3.9 How to Delete a Process?
This section helps you know how to delete a process.
To delete a Process, use the following path:
Manage > Command Profiler:
Follow the below steps:
Select the required Profile Name. The processes belonging to the particular profile are displayed in the
grid on the bottom pane:

## [p33]

www.arconnet.com|Copyright © 2025 33
2.
3.
4.
1.
Select the Profile. Click on the Delete button.
The following screen is displayed
Click on yes button to delete the Selected Command Profile.
4.3.2.3.10 How to Assign TS Monitor Command to Service?
This section helps you to assign TS Monitor Command to the service. Once the profile is created then it is
mandatory to assign ARCOS TS Monitor Command to a particular service. Processes shall only be restricted or
elevated only once the TS Monitor Command is assigned to a particular service.
To assign TS Monitor, select the required LOB mapped to the service:

## [p34]

www.arconnet.com|Copyright © 2025 34
2.
3.
Select Windows Server group if you are a Group Admin:
Go to Manage > Users and Services > Manage Commands:

## [p35]

www.arconnet.com|Copyright © 2025 35
4.
5.
Select Windows Admin User Group. You can view the list of User IDs assigned to the group:
Select the required USER ID (E.g. ARCOSADMIN) from the list of User IDs:

## [p36]

www.arconnet.com|Copyright © 2025 36
6.
7.
Select Windows RDP Service Type. A list of services is displayed:
Select Windows RDP Service. The configuration commands are displayed:

## [p37]

www.arconnet.com|Copyright © 2025 37
8.
1.
2.
Select ARCOS-TS Monitor  command and click Apply Command Changes  to apply the TS Monitor
command to the Windows service.
4.3.2.3.11 How to Assign Profiles and Restrict or Elevate Processes?
This section helps you to assign a profile to a User. In addition, you can restrict or elevate processes available
for a particular user. You can restrict or elevate processes under the Manage Processes tab. Restricting
processes will disallow the user from further usage of the processes.
To Assign Profiles and restrict or elevate processes, select the required LOB mapped to the service:
Select Windows Server group if you are a Group Admin:

## [p38]

www.arconnet.com|Copyright © 2025 38
3.
4.
Go to Manage → Users and Services → Manage Processes. The following screen is displayed:
Select or Enter Windows Admin User Group. You can view a list of User IDs mapped to the User Group.
To search a specific set of rows, enter keywords(space separated) in the search text field of the
user group, and service detail dropdown, and the relevant rows are fetched.

## [p39]

www.arconnet.com|Copyright © 2025 39
5.
6.
Select the required USER ID (E.g. ARCOSADMIN) from the list of User IDs:
Select Windows RDP Service. You can view the profiles created:

## [p40]

www.arconnet.com|Copyright © 2025 40
7.
8.
Select the profile Blacklist. On the right side, blacklisted processes are displayed:
Similarly, select Elevate Profile, and you can view the processes assigned to the profile:

## [p41]

www.arconnet.com|Copyright © 2025 41
9.
10.
11.
12.
Click Apply Profile Changes to restrict or elevate processes for a Windows service.
After restricting Processes, follow the below steps in the Client Manager
Select the LOB and select the Windows RDP option from the Service Type dropdown list:
Click on the service for which settings the changes are saved in the Manage Command tab.
Select the Terminal option to access the server:
If a process is assigned in both Blacklist and Elevate profiles, then that process will be
considered as Blacklisted as a rule.

## [p42]

www.arconnet.com|Copyright © 2025 42
13.
14.
1.
2.
3.
1.
On the selected Server, click Run from Start Menu.
Enter the Blacklisted Process name and click OK to execute the process. An error prompt for restricted
command will be displayed.
4.3.2.3.12 How to Elevate Process?
On Elevating Processes follow the below steps in Client Manager:
Select the LOB and select the Windows RDP option from the Service Type dropdown list.
Click on the service for which settings were saved in the Manage Command tab.
Select Terminal Tab to access the server.
On the Server follow the below steps
Select the ARCOS TS Monitor window:

## [p43]

www.arconnet.com|Copyright © 2025 43
2. In ARCOS TS Monitor select User from the drop-down:

## [p44]

www.arconnet.com|Copyright © 2025 44
3.
4.
5.
Select a process (E.g. Notepad).
Right-click and click Elevate Process option.
The selected process will be displayed (Elevated):
4.3.2.4 Commands Management
4.3.2.4.1 What are Commands Management?
The Commands Management helps you to restrict commands. In addition, the critical commands can also be
sent for approval based on the configuration done in the Workflow Approval Matrix. On authorizing, the User
will be able to execute the command. If the Approver has rejected the request, then the command will not be
allowed for execution. You can restrict commands or add critical commands for approval under Manage
Commands tab.
Restricting commands will disallow the user from further usage of the commands. Adding critical commands for
approval will disallow the user from executing critical commands until approved.
4.3.2.4.2 Why do we need Commands Management?
This feature provides granular control over command execution, helping prevent misuse or accidental
execution of high-risk commands. It strengthens security and compliance by enforcing an approval workflow,
ensuring that only authorized users can run sensitive commands, thereby reducing the risk of internal threats
or unauthorized system changes.

## [p45]

www.arconnet.com|Copyright © 2025 45
1.
2.
3.
To manage commands, follow the below steps:
Configure Workflow Approval Matrix
Create Command Profile
Assign Profile To User
4.3.2.4.3 Process Flow Diagram
•
•
The Administrator having Change User Restricted Commands privilege in Server's Privileges
shall only be able to configure restricted commands, add critical commands for approval and
apply Configuration Commands to User and Service mapping.
The Server Group Admin having Change User Restricted Command privilege in Group Admin
Privileges  shall only be able to configure restricted commands, add critical commands for
approval, and apply Configuration Commands to User and Service mapping.

## [p46]

www.arconnet.com|Copyright © 2025 46
4.3.2.4.4 Configure Workflow Approval Matrix
4.3.2.4.4.1 How to Configure Workflow Approval Matrix?
For certain critical commands, the Administrator must obtain approval before assigning them to users. To
configure the Critical Command Workflow, the Administrator should follow this path:
Settings > Workflow > Raise Request > User Request Approval Workflow > Add/Edit

## [p47]

www.arconnet.com|Copyright © 2025 47

## [p48]

www.arconnet.com|Copyright © 2025 48
The User Request Approval Workflow screen contains the following fields:
Field Name Description
Description Specify the name or details of the approval matrix to be created.
Request Type Select Critical Command as the type of request.
LOB/ Profile Select the LOB or profile.
Service Group Select the service group.
User Group Select the user group.
Approval Levels Select the number of approval levels to approve the request.
Between Specific
Time
Select the specific time with hours and days, to enable the matrix between the selected
time.
Specific Service IP
Address
Select and specify the service IP address to apply the created matrix to the specific IP
only.
Specific Privileged
Account
Select and specify the privileged account to apply the created matrix to the specific
privileged account only.
Specific User ID Select and specify the user ID to apply the created matrix to the specific user ID only.
Multiple service groups can be selected. A search option can be used to filter
the dropdown values.
Multiple user groups can be selected. A search option can be used to filter the
dropdown values.
It can be set to a maximum of 5 levels and a minimum of 1 level.
The IP refers to the destination server/service accessed via ARCON PAM.
The account refers to the destination server user account accessed via
ARCON PAM.
The user ID refers to the user’s login in ARCON PAM.

## [p49]

www.arconnet.com|Copyright © 2025 49
1.
2.
Field Name Description
Approvers Select the name of the approver to approve the request.
Send Email
Notification(s) To
Requester
Send an email notification to the User who has raised a request from CM.
Send SMS
Notification(s) To
Approver
Send an SMS notification to the approver.
Enabled Enable the matrix.
Follow the below steps:
Select Any  or Critical Command  in the Request Type dropdown list and enter or select the required
details.
Click Save, to create the Workflow Matrix for Critical Command.
4.3.2.4.5 Create Command Profile
4.3.2.4.5.1 What is Command Profile?
The profile of commands is a security feature implemented by administrators to limit the commands and
processes accessible to users, ensuring a controlled and safe environment. This measure helps prevent
potential misuse or unauthorized actions.
4.3.2.4.5.2 Why is Command Profile Important?
This feature helps maintain a controlled and secure environment  by minimizing the risk of unauthorized
actions or misuse. It enforces command-level restrictions to uphold compliance, protect critical systems, and
ensure that users only perform actions relevant to their roles.
•
•
For the User IDs to appear for selection in Dropbox, the Users in
ARCON PAM need to have email IDs configured in user settings.
Multiple approvers can be chosen at each level of approval.
For the mails, SMTP configuration under ARCON PAM has to be configured
prior and ARCOS Alert Service has to be running on ARCON PAM server.
For sending SMS notifications, it is mandatory to define the SMS Gateway
configuration before ARCON PAM.
You can create only one Critical Command workflow. This workflow is configured by default for All
LOB/Profile, All User Groups, and All Service Groups.
Administrators can also assign Windows configuration commands to user groups.

## [p50]

www.arconnet.com|Copyright © 2025 50
1.
2.
3.
4.3.2.4.5.3 How to Create Command Profiler?
To create a command profiler use the following path:
Server Manager > Manage > Command Profiler
Enter the name of the profile in the Profile Name text field:
If commands need to be restricted between periods, check box the Restrict Between Specific Date-
Time and select the dates and time in the available fields below.
Select the Is Active checkbox:
This time period can be scheduled by selecting the field of the Restrict Using Schedule Date-
Time.

## [p51]

www.arconnet.com|Copyright © 2025 51
4.
5.
6.
Click on the Create button:
A window pops up with the following message:
Command Profile Added Into List
Select the profile from the Profile Name list and select the required service type from the Service Types
dropdown. It displays the list of commands commonly used by particular servers:

## [p52]

www.arconnet.com|Copyright © 2025 52
7.
8.
Assign command properties to the commands displayed in the list.
The following are the command properties:
N: None <Displayed in Black Colour>
The command marked as None will allow the user to execute the command without any
restriction or approval process.
R: Restricted <Displayed in Maroon Colour>
The command marked as Restricted, will not allow the User to execute the command.
CWA: Critical With Approval <Displayed in Orange Colour>
The command marked as Critical With Approval will allow the User to execute the command only
after approval. An email notification will be sent to the Approver for approval or rejection. Once
approved, the User will be able to execute the command.
Click Apply Changes, to assign commands to the profile:

## [p53]

www.arconnet.com|Copyright © 2025 53
9.
10.
1.
2.
3.
A window pops up with the following message: Command Profile Updated
Click OK. The profile will be created.
4.3.2.4.6 Delete and Modify Command Profile
4.3.2.4.6.1 How to Delete and Modify Command Profile?
The created command profile can be deleted if it is no longer needed. Proceed with the following steps to delete
the command profile:
Select the name of the profile from the Profile Name list and click Delete:
A window pops up with the following message:
Are You Sure You Want To Delete The Selected Command Profile?
Click Yes. Another window pops up with the following message Command Profile Deleted From List.

## [p54]

www.arconnet.com|Copyright © 2025 54
1.
2.
3.
1.
4.3.2.4.6.2 Modify Details of Command Profile
If required, the details of already created command profiles can be modified. Proceed with the following steps
to modify:
Select the required name of the profile from the Profile Name grid list. The details are displayed in
the Profile Name and Profile Type fields.
Modify the required details and click Modify to update the details:
A window pops up with the following message: Command Profile Updated.
4.3.2.4.7 Create and Delete Commands
4.3.2.4.7.1 How to Create and Delete Command?
A command is a specific instruction executed on the Server to perform some kind of task or function. Proceed
with the following steps to create a new command.
Select the required Profile and Service Type from the Service Type dropdown:

## [p55]

www.arconnet.com|Copyright © 2025 55
2.
3.
4.
5.
1.
Click the Add New Command link.
A  Create New Command For <Service Type name> window pops up.
Enter the command in the Enter Command text field and then click OK.
A window pops up with the following message:
New Command For Selected Service Type Added.
4.3.2.4.7.2 Delete Command
If the command profile is no longer required then it can be deleted. To delete any created command profile
proceed with the following steps.
Select the required Profile and Service Type from the Service Type dropdown:
The character limit for Add New Command window is limited to 1000 characters for restricting or
blacklisting commands.

## [p56]

www.arconnet.com|Copyright © 2025 56
2.
3.
4.
5.
Click the Delete Command link:
A Delete Command for the App window will pop up on the screen:
Enter the existing data or command in the Enter Data text field and click OK.
A window pops up with the following message:
Command Deleted From Selected Service Type.
4.3.2.4.8 Assign Profile to User
The created command profile needs to be assigned to users or services.

## [p57]

www.arconnet.com|Copyright © 2025 57
1.
4.3.2.4.8.1 How to Assign Profile to User?
To assign a profile to a User use the following path:
Server Manager > Manage > Users and Services > Manage Commands
Follow the below steps:
Select/Enter the user group from the User Groups dropdown list on the left pane. A list of User ID(s) is
displayed.
To search a specific set of rows, enter keywords (space separated)
in the search text field of the user group, service type, command profile dropdown and the relevant
rows are fetched.

## [p58]

www.arconnet.com|Copyright © 2025 58
2.
3.
4.
Select the user ID from the User ID list, wherein it displays all the service details available for that
particular user ID:
Select the Service Type from the Service Type drop-down and then select Service Details from the list
of Service Details section.
You can view all the commands in the ARCON PAM Configuration Command(s)  and Service
Command(s) sections.

## [p59]

www.arconnet.com|Copyright © 2025 59
5.
6.
Select the commands from the Configuration Command(s) and Service Command(s) grid.
Click Apply Command Changes:

## [p60]

www.arconnet.com|Copyright © 2025 60
1.
2.
a.
b.
c.
d.
Follow below steps to restrict commands:
A window pops up with the following message:
Commands Restricted/ Applied Successfully For User
Click OK. The commands will be restricted for that particular user.
If you want to restrict only those commands that belong to the selected Command Profile, then
you need to select the Select only Restricted command that belongs to the profile checkbox.
If you want to select only those critical commands that belong to the selected Command Profile,
then you need to select the Select only Critical command that belongs to the profile checkbox.
If Profile Duration  is configured for the selected profile then from and to date and time will be
displayed:
To verify, whether the commands are restricted or approved for execution, open a session from
Client Manager and execute the command on the server. It will either allow you to execute the
command or an error prompt will be displayed for restricted commands.

## [p61]

www.arconnet.com|Copyright © 2025 61
e.
f.
g.
3.
4.
•
•
•
•
The CWA (Critical With Approval) command property is not applicable for SFTP Commands of
SSH Linux Service Type.
You can whitelist configuration commands for services of SSH Firewall, SSH Router, and SSH
Switch Service Type.
Redirect clipboard option can be disabled for individual users even if the clipboard option is
globally enabled.
Users can assign AWS Roles after selecting the AWS service type from the dropdown:
For further steps to assign command profiles to users or services refer to the Apply Command Profile in
the Settings section.
4.3.2.4.9 Command Line Access Control
4.3.2.4.9.1 What is Command Line Access Control?
Command Line Access Control is a security mechanism that allows administrators to control and manage user
access to specific commands or executables on a system. With command line access control, administrators can
set permissions and restrictions on commands that users can run, allowing them to prevent unauthorized
access and enforce compliance policies. This type of control is typically used in environments where multiple
users need access to the same system, such as in a corporate network, where it is important to prevent users
from running commands that could harm the system or other users.
4.3.2.4.9.2 Why is Command Line Access Control Needed?
It is needed to:
Prevent unauthorized access to sensitive system functions or tools.
Reduce the risk of accidental or malicious commands that could compromise system integrity.
Enforce compliance policies by ensuring users only perform permitted actions.
Enhance security  in shared environments like corporate networks, where multiple users access the
same systems.
4.3.2.4.9.3 Elevation of Privilege
What is Elevation of Privilege?

## [p62]

www.arconnet.com|Copyright © 2025 62
•
•
•
•
1.
An elevation of privilege threat is a dangerous attack aimed at obtaining privileged access to sensitive
resources, which can lead to unauthorized access to critical information or the compromise of an entire system.
This type of threat occurs when an attacker gains access to authorization permissions beyond those that were
initially granted, effectively elevating their level of privilege. For instance, an attacker with a privilege set of
read-only permissions may somehow manage to elevate their access to include read and write permissions,
thereby gaining access to data they were not supposed to access.
Why is Elevation of Privilege a Concern?
It is a concern because:
It can lead to unauthorized access to sensitive or critical system resources.
It undermines the principle of least privilege, a core tenet of secure system design.
It enables further attacks, such as data breaches, malware injection, or full system compromise.
It puts organizational integrity and compliance at risk, especially in regulated environments.
What is Configuration?
ARCON PAM offers a robust solution for privilege elevation by creating two services - a non-privilege account
and a privileged account. The privilege account is tied to the non-privilege account using the User Lock To
Console/Supporting Service feature through the Administrative Console. As a result, when direct access to a
privileged account is restricted, users will have to first log in to the non-privileged account before accessing the
privileged account. This approach ensures that privileged access is granted only to authorized users, thereby
preventing any potential elevation of privilege threats.
How to navigate Manage Services?
Navigate to Manage → Manage Services.
How to Access Services?
ARCON PAM provides a secure way of executing privileged commands by allowing users to switch to a
privileged account via its functionality, even if they are logged in with a non-privileged account service.

## [p63]

www.arconnet.com|Copyright © 2025 63
2.
3.
For instance, the user can connect to the non-privilege account service (e.g., 10.10.0.246 - anb) assigned
to their PAM user, and then switch to the privileged account to execute the required commands,
ensuring that all activities are logged and monitored for security purposes.
After clicking on the "Open Connection" button, the user is seamlessly connected to the non-privileged
account, as depicted in the screenshot below.
To elevate the session and switch to the enable mode, the user needs to send a command that elevates
the session. This can be done by selecting the "en" account from the "ARCON PAM Options" menu,
which can be found under "su Users".

## [p64]

www.arconnet.com|Copyright © 2025 64
4. With ARCON PAM's advanced password vault, the en account's username and password can be
automatically retrieved and used for secure Single Sign-On (SSO) in the background, without the need
for the user to manually enter any login credentials. This ensures that the elevation of privilege is
performed securely and efficiently, minimizing any potential security risks or delays.

## [p65]

www.arconnet.com|Copyright © 2025 65
5. In ARCON PAM, the user first logs in as a non-privileged account (ANB). When the user executes the
"su" command, the PAM solution takes over and provides the necessary credentials to elevate the user's
privileges. The user is then changed to a privileged account (en), as depicted in the screenshot below.

## [p66]

www.arconnet.com|Copyright © 2025 66
4.3.2.4.9.4 Command Restrictions
What are Command Restrictions?
In today's rapidly changing IT landscape, it is essential to maintain the security and compliance of critical
systems and data. One way to achieve this is through command-level access control, which allows
organizations to restrict or elevate certain commands for specific users or groups. However, managing
command-level access control can be complex, especially in large and complex organizations.
ARCON's Command Profiler (Blacklisting and Whitelisting feature) provides a comprehensive solution to
manage command-level access control effectively. With this feature, administrators can create command
profiles to restrict or elevate commands based on user roles, groups, or individual users. This allows
organizations to maintain a secure environment by preventing unauthorized access to sensitive commands or
data.
ARCON's Command Profiler also provides a centralized view of all user activities, enabling organizations to
monitor and detect any suspicious activities. This feature allows administrators to track user behavior, detect
any anomalies, and take appropriate action in real-time to prevent potential security breaches.
With ARCON's Command Profiler, organizations can streamline the process of managing command-level
access control and ensure that their critical systems and data are protected against unauthorized access or
malicious activities.
Why are Command Restrictions Needed?

## [p67]

www.arconnet.com|Copyright © 2025 67
1.
2.
ARCON PAM provides access control for command-line operations through SSH command white-listing or
black-listing. This can be achieved by creating a command profile which is used to restrict or elevate commands
as per the requirement. The Command Profiler feature helps organizations to ensure the security of their
critical systems by controlling and monitoring the commands executed by users.
How to Access Configuration?
In Server Manager → Manage → Manage Command/Services, Apply Command profiler for any user.
In ARCON PAM, the Command Profiler feature restricts users from executing commands that are blacklisted
or not whitelisted by the approver. As shown in the screenshot, certain critical commands like "alter user scott",
"create", and "usermaster" are restricted and cannot be executed by the user.
How to Access Service?
The user can take Single Sign On (SSO) to any *nix device using SSH Services via ARCON PAM. The User
can access the service from the My Services page, by clicking   against the assigned service,
In ARCON PAM a service type named "SSH Oracle SQLPlus" is used to connect to the DB server. An SQL
Session is therefore established.

## [p68]

www.arconnet.com|Copyright © 2025 68
3. In the present scenario, if the user attempts to execute the 'create' command, the ARCON Putty will
prevent the execution of the command as it has been restricted for the user.
4.3.2.4.9.5 Critical Command Execution With Approval
What is Critical Command Execution with Approval?
Critical With Approval property addresses the potential risk posed by unwanted or critical commands
executed by users on the server. Without proper controls in place, such actions can lead to security breaches,
data loss, system downtime, and other serious consequences. The Critical With Approval property provides an
additional layer of security and control by allowing administrators to review and approve critical commands
before they are executed, ensuring that only authorized actions are taken on the system.

## [p69]

www.arconnet.com|Copyright © 2025 69
Why it is Needed?
To keep track of critical commands or processes that may pose a risk to the server, administrators can assign
them with a "Critical With Approval" property. When a user tries to execute such a command, a notification
will be automatically sent to the assigned approver for approval. Only after the approval is granted, the
command will be executed. This powerful feature ensures that only authorized commands are executed on the
server, making it an essential tool for security-conscious administrators.
Configuration
what is Configuring Workflow ?
To ensure a controlled and secure environment, user requests from the CLI are subject to approval based on a
pre-configured workflow matrix. Only Administrators with the appropriate privileges for configuring the User
Request Approval Workflow  in the Server's Privileges settings can manage the approval levels and ensure a
smooth and efficient process.
How to Access Workflow?
To Navigate to the User Request Approval Workflow, use the following path:
Settings → Workflow → User Request Approval Workflow → Add/Edit
How to Assign a Command Profile ?

## [p70]

www.arconnet.com|Copyright © 2025 70
1.
In Server Manager →  Manage →  Manage Commands/Services, Apply the Command Profile for any given
user.
As seen in the following screenshot, the user will not be able to execute the append command and will need
approval from the admin.
How to Access Service?
The user can take Single Sign On (SSO) to any *nix device using SSH Services via ARCON PAM. The User
can then access the service from the My Services page, by clicking   against the assigned service.

## [p71]

www.arconnet.com|Copyright © 2025 71
2.
3.
In ARCON PAM a service type named "SSH Oracle SQLPlus" is used to connect to the DB server. An SQL
Session is therefore established.
When a user fires a command that has been marked as Critical With Approval, they will be prompted for
approval to execute the command. This prompt will be displayed if the user tries to execute a critical
command. For instance, when the user enters the "Append" command, as shown in the screenshot
below, they will be asked for approval before the command is executed.

## [p72]

www.arconnet.com|Copyright © 2025 72
4.
5.
In the event of a user being prompted for approval to execute a critical command after clicking "Yes," a
comment box will appear requiring the user to provide a reason for executing the command. Once the
user has entered the reason, they may submit the request by clicking the "Submit" button.
To ensure the security of critical commands, the ARCON Putty freezes the window for the user until the
command is approved. During this time, the window title changes to "Your approval is pending, please
wait..." as displayed in the screenshot, thereby ensuring that no unauthorized execution takes place
while the command is pending approval.

## [p73]

www.arconnet.com|Copyright © 2025 73
1.
2.
How to Approval the Process?
The approver will receive either an email notification or a notification on the dashboard to approve the
request, as depicted in the screenshot below.
When the approver receives an email or a critical command request notification, they can click on the
link provided to open the Approval-Critical Command  page, from where they can click on "View
Request".

## [p74]

www.arconnet.com|Copyright © 2025 74
3.
4.
 Upon clicking the View Request button, the approver is redirected to a page where they can thoroughly
inspect the information of the critical command that has been requested.
The approver has the option to enter comments and either approve or reject the request, as illustrated
in the screenshot below.

## [p75]

www.arconnet.com|Copyright © 2025 75
5.
1.
Upon successful approval of the critical command request by the approver, a message confirming the
approval is displayed on the screen, stating "Critical Command Request Has Been Approved
Successfully", as depicted in the below screenshot.
How to Execute Command ?
After the approver approves the request, the user will receive a notification that the request has been
accepted, and the command can be executed successfully by the ARCON wrapper for Putty
automatically.

## [p76]

www.arconnet.com|Copyright © 2025 76
2. In the screenshot below, it can be observed that the command is executed securely in the background.
Following are the Command Responses which are present in PAM Command Logs:
1. Critical Command Execution Is Confirmed- Response is fired when the end-user selects ‘yes’ on the prompt
asking whether to fire the command or not.
2. Critical Command Execution Not Confirmed  - Response is fired when the end-user selects ‘no’ on the
prompt asking whether to fire the command or not.
3. Restricted Command - Response is fired when the command is configured as Restricted.

## [p77]

www.arconnet.com|Copyright © 2025 77
•
•
•
•
4. Critical Command with Approval: Workflow Not Set - Response is fired when the CWA command is fired
but workflow has not been set.
5. Workflow Critical Command Execution confirmed- Response is fired if a CWA command is fired by the end-
user and he/she selects ‘yes’ on the prompt asking whether to fire the command or not
6. Workflow Critical Command Execution NOT confirmed- Response is fired if a CWA command is fired by the
end-user and he/she selects ‘no’ on the prompt asking whether to fire the command or not
7. Critical Command with Approval: Approved - Response is fired when the approver approves the raised
command request.
8. Critical Command with Approval: Rejected - Response is fired when the approver rejects the raised
command request.
4.3.3 Privilege Management
What is Privilege Management?
Privilege Management refers to the access or privileges assigned to an identity i.e. any user account that holds
special or additional permissions within the enterprise systems. It involves managing privileged individual
identities, their authentication, authorization, and privileges/permissions within or across system.
4.3.3.1 Assign or Revoke Privileges from Admin or Client Users
4.3.3.1.1 Overview
Privileges are special rights, advantage, or immunity granted or available only to a particular person or group. In
ARCON PAM, there are two type of Users such as Client Users and Admin Users. Client Users are those Users
who has access to only Client Manager whereas, Users who has access to both Client Manager and Server
Manager are Admin type of User.
The following options are available in Edit Privilege Settings:
ARCON PAM User Privileges
ARCON PAM Group Admin Privileges
4.3.3.1.1.1 ARCON PAM User Privileges
In order to have limit on the user’s accessibility, access rights to users are given in both Server Manager and
Client Manager. These access rights are basically the privileges given to the users.
Client Manager or Server Manager privileges are assigned to Admin or Client Type users:
Client Manager Privileges: API User Registration, ARCOS Applications, ARCOS Dashboard, ARCOS
Delegation, ARCOS File Vault, Client Manager Log, Manager LOB/Profile, PAM Menu, Password
Manager, Reports (Dashboard, Group Reports, LOB Reports, Logs, Performance Reports, Privilege
Reports, Security Reports, Service Reports, User Reports, Vault Reports), and Script Manager.
Server Manager Privileges: Application Password Change, Application Password Change – HP
SiteScope, ARCOS Configuration, Command Profiler, Log Viewer, Manage Group, Manage LOB/ Profile,
The Administrator having Admin Privileges will only be able to edit privilege settings assigned to
Users or Group Admin.

## [p78]

www.arconnet.com|Copyright © 2025 78
•
1.
2.
Manage Services, Manage Tab, Manage User, Password Manager and Tools Tab.
4.3.3.1.1.2 ARCON PAM Group Admin Privileges
The Administrator can create number of groups for users and services. Each group can have their own
Administrator. To manage these groups Group Admin privileges are assigned to the respective Group
Administrator.
Group Admin privileges such as Group Log Viewer, User Certification, Manage Services, and Manage
User Request are only assigned to Admin type of users.
To edit privileges:
To edit privileges use the following path:
Manage → Users and Services → Manage Users
Right click on the user name from the User Display Name grid list. The Edit Privileges option is
displayed.
Click the Edit Privileges option. The User Privileges Setting window is displayed.

## [p79]

www.arconnet.com|Copyright © 2025 79
3.
4.
Select the privileges from the list of User’s Available Privileges and click the <<Add button. The selected
privileges are displayed in the list of User’s Assigned Privileges.
Similarly, you can remove the assigned privileges by selecting the privileges from the list of User’s
Assigned Privileges and then click on the Remove>> button to remove the assigned privileges.
4.3.3.2 Client Manager's Privileges
What are Client Manager’s Privileges?
ARCON PAM Client Manager's Privileges are assigned to Client or Admin type of Users to grant special rights
for accessing reports, dashboards, logs, and other applications. Client Manager privileges include API User
Registration, ARCOS Applications, ARCOS Dashboard, ARCOS Delegation, ARCOS File Vault, Client Manager
Log, Manager LOB/Profile, PAM Menu,  Password Manager, Report - Dashboard, Report - Group Reports,
Report - LOB Reports, Report - Logs, Report - Performance Reports, Report - Privilege Reports, Report -
Security Reports, Report - Service Reports, Report - User Reports, Report - Vault Reports and Script Manager.
Following is the list of Client Manager Privileges:
You can follow the above steps to add or remove the available or assigned privileges
for ARCONPAMClientManager’s Privileges option and ARCON PAM Group Admin Privileges tab

## [p80]

www.arconnet.com|Copyright © 2025 80
ARCON PAM Client Manager Privileges Description Feature Navigation
API User
Registration
API User Registration Users with this privilege can register
Users to log into API hosted in the
Client's environment.
Manager >
Application Setting
ARCON PAM
Configuration
Client Manager
Privileges- View All
LOB
Users with this privilege can view ALL
LOB Options.
Reports
Settings > Scheduler
>Schedule Reports,
Reports >
Dashboard,
  Dashboard
ARCON PAM
Dashboard
Dashboard Users with this privilege can view
useful graphical information about the
various actions performed in ARCON
PAM and can view pinned reports.
Dashboard
ARCON PAM
Delegation
Delegation Users with this privilege can delegate
Service Access, Service Password, or
Service Ticket approval rights to another
User.
My Access >
Preferences >
Delegation
Client Manager
Log
View Server Access
Log
Users with this privilege can view details
of user activities on services.
Manager > Access
Logs
View Server Access
Log Details
Users with this privilege can view details
of activities performed by users on
services through a video log.
Manager > Access
Logs > Details
Manager LOB/
Profile
View Service Access
Logs With Details
Users with this privilege can view various
activities performed by users on services
through video log.
My Access > My
Activity
PAM Menu Manager Menu Display Client Users with this privilege can only
view the Manager menu in Client
Manager.
Manager
Report -
Dashboard

ARCOS PAM Live Users with this privilege can view the
number and details of Users logging into
the application, the servers accessed by
the Users, and critical and restricted
commands fired by the Users.
Reports > Dashboard
> ARCOS Live
Enterprise Password Users with this privilege can
view Password Rotation Frequency,
Password Policy Compliance Status,
Password Security Status, Password
Change Success- Failure Rate, and
Upcoming Password Review.
Reports > Dashboard
> Enterprise
Password

## [p81]

www.arconnet.com|Copyright © 2025 81
ARCON PAM Client Manager Privileges Description Feature Navigation
Live Server Sessions Users with this privilege can view the list
of live sessions taken through ARCON
PAM.
Reports > Dashboard
> Live Server
Sessions
User Access & Usage Users with this privilege can view the
number of times critical servers have
been accessed, displayed in a time-based
manner and service-type wise, and the
highly accessed servers.
Reports > Dashboard
> User Access &
Usage
Report - Group
Reports
Servers In Service
Group
Users with this privilege can view details
of all the servers created in a Server
Group, irrespective of the LOBs. The
details displayed in this report are based
on the server's IP Address.
Reports > Group
Reports > Servers In
Server Group
Service Group Report Users with this privilege can view all the
service groups created in ARCON PAM.
Reports > Group
Reports > Service
Group Report
Services In Service
Group
Users with this privilege can view details
of all the services created in a Server
Group, irrespective of the LOBs. The
details displayed in this report are based
on the server's Service Username.
Reports > Group
Reports > Services In
Server Group
User Group Report Users with this privilege can view all the
User Groups created in ARCON PAM.
Reports > Group
Reports > User
Group Report
Users In User Group Users with this privilege can view details
of all the Users created in a User Group
irrespective of the LOB’s.
Reports > Group
Reports > Users In
User Group
Report - LOB
Reports

Active Services Group
Wise Report
Users with this privilege can view active
services under a particular Service
Group.
Reports > LOB
Reports > Active
Services Group Wise
Report
Service Count Report Users with this privilege can view a
graphical representation of the LOB-wise
status of unique IP addresses and
services and the status of Services LOB-
wise.
Reports > LOB
Reports > Service
Count Report
Object Status Report Users with his privilege can view a
graphical representation of the LOB-wise
mapping of objects and the status of
Users and Services LOB-wise.
Reports > LOB
Reports > Object
Status Report

## [p82]

www.arconnet.com|Copyright © 2025 82
ARCON PAM Client Manager Privileges Description Feature Navigation
Active Services Report Users with this privilege can view details
of all servers LOB-wise active in ARCON
PAM.
Reports > LOB
Reports > Active
Services Report
Active Users Report Users with this privilege can view the
details of all Users LOB-wise active in
ARCON PAM.
Reports > LOB
Reports > Active
Users Report
Inactive Services
Report
Users with this privilege can view details
of all inactive servers in ARCON PAM.
Reports > LOB
Reports > Inactive
Services Report
LOB Details Report Users with this privilege can
view detailed descriptions of all the LOBs
created in ARCON PAM.
Reports > LOB
Reports > LOB
Details Report
Dormant Users Users with this privilege can view details
of all dormant users in ARCON PAM. Reports > LOB
Reports > Dormant
Users
Report - Logs Service Request
Workflow Logs
Users with this privilege can view details
of all the service access requests raised
by Users.
Reports > Logs
> Service Request
Workflow Logs
Ticket Request
Workflow Logs
Users with this privilege can view details
of all ticket requests raised by Users in
LOB.
Reports > Logs
> Ticket Request
Workflow Logs
Log Review Report Users with this privilege can view details
of all the Users who have accessed or
viewed the logs generated in ARCON
PAM.
Reports > Logs > Log
Review Report
Approval Delegation
Report
Users with this privilege can
view delegation logs passed to/by based
on any particular LOB.
Reports > Logs
> Approval
Delegation Report
Service Access Log Users with this privilege can view details
of all the services accessed by the Users.
Reports > Logs
> Service Access Log
Session Activity Log Users with this privilege can view why
the current User switched to another
User in an ongoing session.
Reports > Logs
> Session Activity
Log
User Access Review
Processes
Users with this privilege can view details
of User access review processes.
Reports > Logs >User
Access Review
Processes

## [p83]

www.arconnet.com|Copyright © 2025 83
ARCON PAM Client Manager Privileges Description Feature Navigation
Service Password
Request Workflow
Logs
Users with this privilege can view details
of all the service password requests
raised by Users.
Reports > Logs
> Service Password
Request Workflow
Logs
Day Wise Summary
Report
Users with this privilege can view the
date and time-wise count of activities
performed on the Server.
Reports > Logs > Day
Wise Summary
Report
Session Wise Summary
Report
Users with this privilege can view a
session-wise count of activities
performed on the Server along with
service details. It displays details such as
the count of image logs, critical
commands executed on the Server, and
restricted commands and restricted
processes attempted to execute on the
Server.
Reports > Logs
> Session Wise
Summary Report
My Vault Logs Users with this privilege will view the list
of all the activities performed in the File
Vault. It displays filename,  extension,
size, status, added by, added on, shared
on, shared with, File Available till,
Deleted by, Deleted on, and Recorded
on.
Reports > Logs > My
Vault Logs
SIEM Command Logs
Report
Users with this privilege will help you
view command logs fetched from the
SIEM service. The service displays logs of
commands executed on the Linux service.
Reports > Logs >
SIEM Command Logs
Report
APEM Logs Users with this privilege will help you
view logs of actions performed via the
APEM tool. Actions such as opening the
APEM application, reading a file, and
viewing a password are captured in
APEM logs.
Reports > Logs >
APEM Logs
Day Wise User Access
Summary Report
Users with this privilege will help you
determine the total number of users who
accessed the site in a single day.
Reports > Logs > Day
Wise User Access
Summary Report
Incident Management
Log
Users with this privilege can view the
status of the incident ID.
Reports > Logs
> Incident
Management Log
Outside ARCON PAM
Access Log
Users with this privilege will help view
the server information accessed by the
user outside the PAM, including its
access date and time.
Reports > Logs
> Outside ARCON
PAM Access Log

## [p84]

www.arconnet.com|Copyright © 2025 84
ARCON PAM Client Manager Privileges Description Feature Navigation
Service Access Log Day
Wise Report
Users with this privilege can view the list
of users who have accessed the services
for the session duration by selecting the
date.
Reports > Logs
> Service Access Log
Day Wise Report
Service Password
Status Log
Users with this privilege can view the
service password status, such as service
type, password age, password last
change, and password next change.
Reports > Logs
> Service Password
Status Log
SMS And Email Log Users with this privilege can view the
SMS and email logs.
Reports > Logs > SMS
And Email Log
User Access Log
Report
Users with this privilege can view the log
report of users who access the services.
Reports > Logs
> User Access Log
Report
User Access Review
Service Details
Users with this privilege can download
the user access review service details.
Because of the large size, the data view
option is not available.
Reports > Logs
> User Access
Review Service
Details
Service Access Log
Report
Users with this privilege can view the
Service Access log report.
Reports > Logs
>Session Log Report
Collaboration Report Users with this privilege can view the
details of collaborative sessions between
individuals or teams.
Reports > Logs >
Collaboration Report
Report -
Performance
Reports
New ARCON Desk
Insight Devices
Users with this privilege can view details
of desktops integrated into ARCON
PAM.
Reports >
Performance Reports
> New ARCON
DeskInsight Devices
MS SQL Connection
Report
Users with this privilege can view the
details of all the Users connected to the
MS SQL (Microsoft Sequel) instance on
the ARCON PAM database server.
Reports >
Performance Reports
> MS SQL
Connection Report
Report - Privilege
Reports
Client Manager
Privilege Report
Users with this privilege can view
the count of client manager privileges
and the privileges assigned to Users.
Reports > Privilege
Reports > Client
Manager Privilege
Report
Group Admin Privilege
Report
Users with this privilege can view
the count of group admin privileges and
the privileges assigned to Admin Users.
Reports > Privilege
Reports > Group
Admin Privilege
Report

## [p85]

www.arconnet.com|Copyright © 2025 85
ARCON PAM Client Manager Privileges Description Feature Navigation
Server Manager
Privilege Report
Users with this privilege can view
the count of server manager
privileges and the privileges assigned to
Admin Users.
Reports > Privilege
Reports > Server
Manager Privilege
Report
User & Service
Privileges - Windows
RDP
Users with this privilege can view the
count of command privileges and a list of
privileges assigned to Client or Admin
Users, mapped to the Windows RDP
(Remote Desktop Protocol) service type.
Reports > Privilege
Reports > User &
Service Privileges -
Windows RDP
Users and Service
Privileges
Users with this privilege can view the
number of Users and Service privileges
and their assigned privileges.
Reports > Privilege
Reports > Users &
Service Privileges
Report - Security
Reports

Critical Commands
Executed Report
Users with this privilege can view details
of all the critical commands executed on
servers.
Reports > Security
Reports > Critical
Commands Executed
Report
Restricted Commands
Attempted Reports
Users with this privilege can view details
of all the restricted commands the User
executes.
Reports > Security
Reports > Restricted
Commands Executed
Report
High Usage (in hrs)
Services Report
Users with this privilege can view the
count of services that are highly
accessed.
Reports > Security
Reports > High Usage
(in hrs) Services
Report
Invalid Login Attempts
Report
Users with this privilege can view the
count/number of invalid login attempts
made by the user.
Reports > Security
Reports > Invalid
Login Attempts
Report
Low Usage (in days)
Services Report
Users with this privilege can view the
count/number of servers that are
accessed rarely.
Reports > Security
Reports > Low Usage
(in days) Services
Report
Multiple Desktop
Logon Report
Users with this privilege can view details
of the desktop IP used by users to log in
to ARCON PAM.
Reports > Security
Reports > Multiple
Desktop Logon
Report
Multiple User Logon
Report
Users with this privilege can view the
details of users who have logged into
ARCON PAM from different IPs/
desktops.
Reports > Security
Reports > Multiple
User Logon Report

## [p86]

www.arconnet.com|Copyright © 2025 86
ARCON PAM Client Manager Privileges Description Feature Navigation
Network Segment
Wise Logon Report
Users with this privilege can view the
details of all the Users who have logged
into ARCON PAM through any network
device configured in Network Segments
in Settings Configuration.
Reports > Security
Reports > Network
Segment Wise Logon
Report
Service Accessed -
Multiple Times Report
Users with this privilege can view details
of services accessed multiple times by the
User.
Reports > Security
Reports > Service
Accessed - Multiple
Times Report
User Service Accessed
- Multiple Times
Report
Users with this privilege can view the
number of times they have accessed
services within the defined range.
Reports > Security
Reports > User
Service Accessed -
 Multiple Times
Report
Mobile OTP Auth
Status Report
Users with this privilege can view the
details of the User Mobile Auth Report.
Reports > Security
Reports > Mobile
OTP Auth Status
Report
Service Access off
Production Hrs Report
Users with this privilege can access the
Service Access off Production hours
Report.
Reports > Security
Reports > Service
Access off
Production Hrs
Report
Commands Executed
Report
Users with this privilege can access the
Report on Commands Executed.
Reports > Security
Reports > Commands
Executed Report
Blacklisted Processes
Attempted Report
Users with this privilege can access the
Report Attempted Blacklisted Processes.
Reports > Security
Reports > Blacklisted
Processes Attempted
Report
Report - Service
Reports

Multiple Service
Reference No. Report
Users with this privilege can view details
of the reference number provided by the
User before accessing any Service.
Reports > Service
Reports > Multiple
Service Reference
No. Report
Unique Services IP
Address Report
Users with this privilege can view details
of all the services with unique IP
addresses.
Reports > Service
Reports > Unique
Services IP Address
Report
Active Services Report Users with this privilege can view details
of services that are active in ARCON
PAM, irrespective of the LOBs.
Reports > Service
Reports > Active
Services Report

## [p87]

www.arconnet.com|Copyright © 2025 87
ARCON PAM Client Manager Privileges Description Feature Navigation
Service Accessed
Summary Report
Users with this privilege can view a
monthly summary report of all the
services they access.
Reports > Service
Reports > Service
Accessed Summary
Report.
Active Sessions Report Users with this privilege can view all the
active service sessions in ARCON PAM.
Reports > Service
Reports > Active
Sessions Report
Scheduled Password
Change Services
Users with this privilege can view details
of all the services scheduled for the
password change process.
Reports > Service
Reports > Scheduled
Password Change
Services
Service Accessed
Summary Days Wise
Report
Users with this privilege can view the
total number of services accessed daily.
Reports > Service
Reports > Service
Accessed Summary
Days Wise Report.
Password Envelope
never generated
Users with this privilege can view details
of Users who have printed password
envelopes and those who have verified
the process.
Reports > Service
Reports > Password
Envelope Print
Report
Service Dependency
Report
Users with this privilege can view details
of all the services that have dependent
services.
Reports > Service
Reports > Service
Dependency Report
Servers in Domain
Report
Users with this privilege can view
details of all the servers in a domain
irrespective of the LOBs. The details
displayed in this report are based on the
server's IP Address.
Reports > Service
Reports > Servers in
Domain
Services in Domain
Report
Users with this privilege can view
details of all the services in a domain
irrespective of the LOB. The details
displayed in this report are based on the
Service Username.
Reports > Service
Reports > Services in
Domain
Service Group wise
Service Type Report
Users with this privilege can view Service
Types of Services assigned to the Service
Group.
Reports > Service
Reports > Service
Group wise Service
Type Report
Service Creation
Deletion Summary
Report
Users with this privilege can view all the
created and deleted services.
Reports > Service
Reports > Service
Creation Deletion
Summary Report

## [p88]

www.arconnet.com|Copyright © 2025 88
ARCON PAM Client Manager Privileges Description Feature Navigation
Service Timeline
Report
Users with this privilege can view the
timelines of all the services.
Reports > Service
Reports > Service
Timeline Report
Service Creation
Deletion Details
Report
Users with this privilege can view all the
details of the created and deleted
services.
Reports > Service
Reports > Service
Creation Deletion
Details Report
Server Last Accessed
On
Users with this privilege can view the
records of servers that have not been
accessed for a number of days.
Reports > Service
Reports > Server Last
Accessed On
Service Audit Logs
Report
Users with this privilege can view all the
Service Audit Logs Report details.
Reports > Service
Reports > Service
Audit Logs Report
AGW Service Access
Report
Users with this privilege can view all the
details of the AGW Access Service
Report.
Reports > Service
Reports >AGW
Service Access
Report
Device Detailed report Users with this privilege can view all the
details of the Device Detailed Report.
Reports > Service
Reports >Device
Detailed report
Session Extension
Report - For Duration
Users with this privilege can view all the
Session Extended Report - For Duration
details.
Reports > Service
Reports >Session
Extension Report -
For Duration
Service Application
Report
Users with this privilege can view all the
details of the Service Application Report.
Reports > Service
Reports >Service
Application Report
Services assigned to
AGW Server
Users with this privilege can view all the
details of the Services assigned to AGW
Server.
Reports > Service
Reports >Services
assigned to AGW
Server
Password
Dependencies(Actions)
Users with this privilege can view all the
details of the Dependencies Password.
Reports > Service
Reports > Password
Dependencies(Action
s)
DMZ Gateway Report Users with this privilege can view all the
details of the DMZ Gateway Report.
Reports > Service
Reports >DMZ Gate
Report
Command Profile
Report
Users with this privilege can view all the
details of the Command Profile Report.
Reports > Service
Reports >Command
Profile Report

## [p89]

www.arconnet.com|Copyright © 2025 89
ARCON PAM Client Manager Privileges Description Feature Navigation
Lock to Console Report Users with this privilege can view all the
Lock to Console Report details.
Reports > Service
Reports > Lock to
Console Report
Password policy
Report
Users with this privilege can view all the
details of the Password Policy Report.
Reports > Service
Reports > Password
policy report
Password policy
report
Users with this privilege can view all the
details of the Password Policy Report.
Reports > Service
Reports > Password
policy report
Password expiry
report
Users with this privilege can view all the
details of the Password expiry Report.
Reports > Service
Reports > Password
policy report
Password expiry
report
Users with this privilege can view all the
details of the Password expiry Report.
Reports > Service
Reports > Password
policy report
Report - User
Reports

Idle Users Report Users with this privilege can view details
of all the users who are idle for the
selected LOB.
Reports > User
Reports > Idle Users
Report
User & Service
Mapping Report
Users with this privilege can view LOB-
wise User and Service mapping details.
Reports > User
Reports > User &
Service Mapping
Report
User Last Logon
Report
Users with this privilege can view the
User’s last login details into the ARCON
PAM application.
Reports > User
Reports > User Last
Logon Report
User Biometric Auth
Report
Users with this privilege can view details
of Users who have configured only
biometric authorization to make the login
process more secure.
Reports > User
Reports > User
Biometric Auth
Report
User Biometric Auth
Report - All LOB
Users with this privilege can view details
of users who have configured only the
biometric authorization, making the login
process more secure for all LOBs.
Reports > User
Reports > User
Biometric Auth
Report - All LOB
User Mobile OTP Auth
Report
Users with this privilege can view the
details of Users who have configured
mobile authorization, which makes the
login process more secure.
Reports > User
Reports > User
Mobile OTP Auth
Report
User Hardware Auth
Report
Users with this privilege can view details
of Users who have configured Hardware
Token authorization, making the login
process more secure.
Reports > User
Reports > User
Hardware Auth
Report

## [p90]

www.arconnet.com|Copyright © 2025 90
ARCON PAM Client Manager Privileges Description Feature Navigation
User SMS OTP Auth
Report
Users with this privilege can view details
of Users who have configured SMS OTP
authorization, making the login process
more secure.
Reports > User
Reports > User SMS
OTP Auth Report
Active Users Report Users with this privilege can view details
of all active users in ARCON PAM
irrespective of the LOB.
Reports > User
Reports > Active
Users Report
Inactive Users Report Users with this privilege can view the
details of all inactive users in ARCON
PAM, irrespective of the LOBs.
Reports > User
Reports > Inactive
Users Report
Dual Factor Auth
Configuration Report
Users with this privilege can view the
details of Users who have configured
dual-factor authorization to make the
login process more secure.
Reports > User
Reports > Dual
Factor Auth
Configuration Report
Locked Out User
Report
Users with this privilege can view details
of Users who have tried to log in using an
invalid password and exceeded the value
configured in lockout attempts in
Application Configuration (Settings
Configuration).
Reports > User
Reports > Locked
Out User Report
Dormant User Report Users with this privilege can view details
of Users who have not used their account
for the configured number of dormancy
days in Application Configuration
(Settings Configuration).
Reports > User
Reports > Dormant
User Report
Last Service Accessed
Report
Users with this privilege can view details
of the last service users accessed.
Reports > User
Reports > Last
Service Accessed
Report
Consolidated User &
Service Mapping
Report
Users with this privilege can view the
total number of services mapped to
users.
Reports > User
Reports
> Consolidated User
& Service Mapping
Report
User Dormant in next 5
day Report
Users with this privilege can view details
of Users whose accounts will be dormant
in the next 5 days.
Reports > User
Reports > User
Dormant in next 5
day Report
User Creation Deletion
Summary Report
Users with this privilege can view a
summary of user creation and deletion.
Reports > User
Reports > User
Creation Deletion
Summary Report

## [p91]

www.arconnet.com|Copyright © 2025 91
ARCON PAM Client Manager Privileges Description Feature Navigation
User Compliance
Report
Users with this privilege can view a User
Compliance Report.
Reports > User
Reports > User
Compliance Report
User Status  Report Users with this privilege can view the
different statuses of Users under the
User Status Report.
Reports > User
Reports > User
Status  Report
Endpoint Access
Control Configuration
Report
Users with this privilege can view a
Configuration of Endpoint Access
Control.
Reports > User
Reports > Endpoint
Access Control
Configuration Report
Report - Vault
Reports
Service Password
Envelope Print Status
Report
Users with this privilege can view details
of all the services for which the password
envelope has been generated.
Reports > Vault
Reports > Service
Password Envelope
Print Status Report
Restore Service
Password Option Used
Users with this privilege can view the list
of users who used the Restore Service
Password option.
Reports > Vault
Reports > Restore
Service Password
Option Used
Service Password Age
Report
Users with this privilege can view the age
of the service password, i.e., the number
of days the password has been active in
ARCON PAM.
Reports > Vault
Reports > Service
Password Age Report
Service Password
Change Failed (Server
Unavailable) Report
Users with this privilege can view details
of all the services whose password
change has failed due to server
downtime.
Reports > Vault
Reports > Service
Password Change
Failed (Server
Unavailable) Report
Service Password
Changed Status Report
Users with this privilege can view details
of all the services whose passwords have
been successfully changed since the
service was created.
Reports > Vault
Reports > Service
Password Changed
Status Report
Service Password
Expires In 5 Days
Report
Users with this privilege can view details
of those services whose passwords will
expire in 5 days.
Reports > Vault
Reports > Service
Password Expires In
5 Days Report
Service Password
Manually Changed
Report
Users with this privilege can view details
of all the services whose passwords are
changed manually.
Reports > Vault
Reports > Service
Password Manually
Changed Report

## [p92]

www.arconnet.com|Copyright © 2025 92
ARCON PAM Client Manager Privileges Description Feature Navigation
Service Password
Never Changed Report
- All LOB
Users with this privilege can view details
of all the services whose passwords are
never changed, either manually or
through the password change process.
Reports > Vault
Reports > Service
Password Never
Changed Report
Service Password
Check-Out Report
Users with this privilege can view details
of the Users requested to view the
service password for a desired number of
hours.
Reports > Vault
Reports > Service
Password Check Out
Report
Service Password
Changed Success-
Failed Report
Users with this privilege can view the
status of password changes for the
services.
Reports > Vault
Reports > Service
Password Changed
Success-Failed
Report
Service Password
Security Status
Users with this privilege can view details
of all the services whose passwords are
open or closed.
Reports > Vault
Reports > Service
Password Security
Status
Service Password
Vaulting Summary
Report
Users with this privilege can view the
LOB-wise summary of all the services
whose passwords have been changed.
Reports > Vault
Reports > Service
Password Vaulting
Summary Report
Current Password
Status Report
Users with this privilege can view the
current status of the service password
and other password change details.
Reports > Vault
Reports > Current
Password Status
Report
SPC not Configured
Report
Users with this privilege can view details
of services for whom SPC has not been
configured.
Reports > Vault
Reports > SPC not
Configured Report
SPC Success and Failed
Report
Users with this privilege can view details
of service password changes through the
SPC service.
Reports > Vault
Reports > SPC
Success and Failed
Report
Users Extracting
Password Envelope
Users with this privilege can view details
of Users who have printed Password
Envelopes.
Reports > Vault
Reports > Users
Extracting Password
Envelope
Service Reconcile
Status Report
Users with this privilege can view the
status of the reconciliation of assets.
Reports > Vault
Reports > Service
Reconcile Status
Report

## [p93]

www.arconnet.com|Copyright © 2025 93
ARCON PAM Client Manager Privileges Description Feature Navigation
Mobile OTP Auth
Status Report
Users with this privilege can view the
status of the mobile OTP configuration
process.
Reports > Vault
Reports > Mobile
OTP Auth Status
Report
Services Scheduled for
SPC
Users with this privilege can view details
of assets for which SPC has been
scheduled.
Reports > Vault
Reports > Services
Scheduled for SPC
Service Password
Never Changed Report
- All LOB
Users with this privilege can view details
of all the assets whose passwords have
never been changed, both manually or
through the password change process for
all LOBs.
Reports > Vault
Reports > Service
Password Never
Changed Report - All
LOB
Service Password
Changed Status Report
- All LOB
Users with this privilege can view details
of all the Assets whose passwords have
been successfully changed since the
Asset was created for all LOBs.
Reports > Vault
Reports > Service
Password Changed
Status Report - All
LOB
Maximum Password
Failed Attempts
Users with this privilege can view details
of Failed Attempts of Password.
Reports > Vault
Reports > Maximum
Password Failed
Attempts
Service details for SPC
- Max Failed Attempts
Users with this privilege can view details
of failed attempts in Service for SPC.
Reports > Vault
Reports > Service
details for SPC - Max
Failed Attempts
Service Password
Change  Consolidated
Report
Users with this privilege can view details
of the change in service password.
Reports > Vault
Reports > Service
Password Change
Consolidated  Report
Service Last Password
Failed Reason
Users with this privilege can view details
of Service Last Password Failed Reason.
Reports > Vault
Reports > Service
Last Password Failed
Reason
Allow Password
Change Report
Users with this privilege can view details
of Change Password.
Reports > Vault
Reports >Allow
Password Change
Report
Service Password
Viewed By
Administrator
Users with this privilege can view details
of the Service Password viewed by the
Administrator.
Reports > Vault
Reports > Service
Password Viewed By
Administrator

## [p94]

www.arconnet.com|Copyright © 2025 94
ARCON PAM Client Manager Privileges Description Feature Navigation
Service  Reached
Maximum  Failed
Attempts
Users with this privilege can view details
of Service Reached with Maximum Failed
Attempts.
Reports > Vault
Reports >Service
Reached Maximum
Failed Attempts
Service Password
Vaulting Status
Users with this privilege can view details
of Service Password Vaulting Status.
Reports > Vault
Reports >Service
Password Vaulting
Status
Service Consolidated
Vault Status Report
Users with this privilege can view details
of Service Consolidated Vault Status.
Reports > Vault
Reports >Service
Consolidated Vault
Status Report
Credentials Accessed
via APIs
Users with this privilege can view details
of Accessed Credentials via APIs.
Reports > Vault
Reports >Credentials
Accessed via APIs
Notifications Service Password
Change Scheduled
Users with this privilege will be notified
before the configured number of days in
Settings Service Password Change
Scheduled Days (number of days). For
example, if the configured value is set to
5, then the User will be notified 5 days
before the password expires.
Notifications
  Service Expiry Due Users with this privilege will be notified
before the configured number of days in
Settings Service Expiry Days (number of
days). For example, if the configured
value is set to 5, then the User will be
notified 5 days before service expiry.
Notifications
Script Manager Create New Script Users with this privilege can create a new
script.
Manager > Script
Manager > Add New
Script
Edit Script Users with this privilege can edit an
existing script.
Manager > Script
Manager > Edit Script
Run Script Users with this privilege can run a script. Manager > Script
Manager > Run Script
Schedule Script Users with this privilege can Schedule a
script.
Manager > Script
Manager > Schedule
Script
Delete Script Users with this privilege can delete a
script.
Manager >Script
Manager > Delete
Script

## [p95]

www.arconnet.com|Copyright © 2025 95
ARCON PAM Client Manager Privileges Description Feature Navigation
About Edit Contact Users with this privilege Edit/Add
contact details on the ACMO about page.
About
ACMO-Access
Type

ACMO CLI Users with this privilege can access
ACMO CLI

My Vault - ARCOS
Secret Service
Service Download Users with this privilege can Download
the Service
My Vault - ARCOS
Secret Service >
Service Download
Service Remove Users with this privilege can Remove the
Service.
My Vault - ARCOS
Secret Service >
Service Remove
Service Share Users with this privilege can Share the
Service.
My Vault - ARCOS
Secret Service >
Service Share
Service View Users with this privilege can View the
Service.
My Vault - ARCOS
Secret Service >
Service View
Service Edit Users with this privilege can Edit an
existing Service.
My Vault - ARCOS
Secret Service >
Service Edit
Service Create Users with this privilege can Create a
new Service.
My Vault - ARCOS
Secret Service >
Service Create
Secret Tab Users with this privilege can view the
Secret tab option.
My Vault - ARCOS
Secret Service >
Secret Tab
My Vault - Secret Type Users with this privilege can map the
visible type secrets while creating the
service.
My Vault - ARCOS
Secret Service > My
Vault - Secret Type
My Vault  - Secret
Group
Users with this privilege can map the
visible type group while creating the
secret group.
My Vault - ARCOS
Secret Service > My
Vault - Secret Group
Raise Request Allow Service
Password Request
Users with this privilege can Request a
Service Password.
Raise Request >
Allow Service
Password Request
Allow Offline Service
Request
Users with this privilege can Request the
Service Offline.
Raise Request >
Allow Offline Service
Request

## [p96]

www.arconnet.com|Copyright © 2025 96
4.3.3.3 Server's Privileges
What are Server’s Privileges?
ARCON PAM Server's privileges are assigned to admin users for - user  management, service management,
group management, password management, accessing logs, and other applications. Server privileges
include Application Password Change, Application Password Change - HP SiteScope, ARCOS Configuration,
Command Profiler, Log Viewer, Manage Group, Manage LOB / Profile, Manage Services, Manage Tab, Manage
User, and Password Manager.
Following is the list of Server Privileges:
ARCON PAM Server Privilege Description Feature Navigation
ARCON PAM
Applications
File Vault Users with this privilege can upload,
download, view, or delete files in the
vault.
Manager > My Apps >
My Vault
Session Monitoring Administrators with this privilege can
allow effective monitoring of user
activities during privileged account
sessions.
Manager > My Apps>
Session Monitoring
PAM Logs Administrators with this privilege can
audit trail details for the activities
performed in Server Manager. It
generates logs for all the activities
performed by the users while using the
application.
Manager >My Apps>
PAM Logs
ARCON Gateway Administrators with this Privilege can
do AGW Configuration
Manager > My Apps>
Settings> ARCON
Gateway
Spection Administrators with this privilege can
access the report builder that allows
searching and filtering capabilities to
derive a detailed compilation of all
activities.
Manager > My Apps>
Spection
Settings Administrators with this Privilege can
have more control over the program's
security functions and behavior,
enabling them to modify it to suit their
security requirements and preferences.
Manager >My Apps>
Settings
ARCON PAM Object
Counter
Administrators with this privilege can
view and monitor different entities in
ARCON PAM.
My Apps> Setting
> ARCON PAM Object
CounterTools
File Vault Admin Administrators with this privilege can
upload a file in various file formats.
Manager >My Apps>
My Vault

## [p97]

www.arconnet.com|Copyright © 2025 97
ARCON PAM Server Privilege Description Feature Navigation
User Access
Governance Manager
Administrators with this privilege can
give users access.
Manager > My
Apps>User Access
Governance
User Access
Governance Reviewer
Administrators with this privilege can
review the access of any users with
specific attributes. By configuring the
data, you can fetch the user for review.
Manager > User Access
Governance Reviewer
Administrative Console Administrators with this privilege can
empower administrators with the tools
and permissions needed to manage and
oversee the entire identity
management system.
Manager >My Apps >
Administrative Console
Password Manager Administrators with this privilege can
manage the password management.
Manager > My Apps>
Password Vault
MyVault Enterprise Administrators with this privilege can
offer MyVault service to all corporate
users. However, files and secrets can be
shared only among registered members
of that organization.
Manager > My Apps >
MyVault Enterprise
Digital Vault Administrators with this privilege can
create non-interactive vault users.
Manager >My Apps>
Digital Vault
IDAM(Infrastructure) Administrators with this privilege can
provide security and ease in configuring
Servers, provisioning, and de-
provisioning Servers.
Manager > My Apps>
IDAM
Auto-onboarding Administrators with this privilege can
access "Auto-Onboarding" under the
Manager tab.
Manager > My Apps >
Auto-Onboarding
ARCON PAM
Configuration
MAC/IP Filter Administrators with this privilege can
configure all the IP addresses, MAC
addresses, Processor IDs, and BIOS
Serial IDs that have been blocked or
allowed for desktop-level access.
Manager > My Apps>
Settings>User>
MAC/IPFilter
License Details Administrators with the License
Configuration privilege can view
license information and will receive a
warning message 30 days before the
license expires.
ACMO > MyAccess >
License Details

## [p98]

www.arconnet.com|Copyright © 2025 98
ARCON PAM Server Privilege Description Feature Navigation
Alert And Notification
Configurations
Administrators with this privilege
can configure alerts and Users who will
receive alert notifications.
Manager > My Apps>
Settings > Alert &
Notification
Configurations
Scheduler Master Administrators with this privilege
can configure a scheduler to send
reports and password envelopes
through email.
Manager > My Apps>
Settings > Scheduler
Master
Schedule Reports Administrators with this privilege can
configure reports to be sent through
email and saved on a preferred path.
Manager > My Apps>
Settings
>Scheduler> Schedule
Reports
Workflow Approval
Matrix
Administrators with this privilege can
configure approval levels for each
transaction or operation the
Administrator performs.
Manager > My Apps>
Settings >Admin
Activities > Workflow
Approval Matrix
User Request Approval
Workflow
Administrators with this privilege
can configure approval levels for the
user's request for service access,
service password, service ticket, and
critical command.
Manager > My Apps>
Settings >Raise Request
> User Request
Approval Workflow
Gateway Configurations Administrators with privileges will be
able to perform LOB to gateway
mapping.

Manager > My Apps>
Settings> Gateway
Configurations
Apply Password Setting Administrators with this privilege can
configure password settings and
schedule password changes at the
group level.
Manager > My Apps>
Settings> Apply
Password Settings
Apply Command Profile Administrators with this privilege can
manage profiles at the group level.
Manager > My Apps>
Settings> Apply
Command Profile
Service Classification Administrators with this privilege
can classify a service as critical, data, or
antivirus server.
Manager > My Apps>
Settings > Service
Modifications> Service
Classification
Service Critical
Commands
Administrators with this privilege
can define a critical command for a
service.
Manager > My Apps>
Settings >Service
Security > Service
Critical Commands

## [p99]

www.arconnet.com|Copyright © 2025 99
ARCON PAM Server Privilege Description Feature Navigation
ARCON PAM Server
Master
Administrators with this privilege
can add or modify servers such as
application, database, gateway, and DR
servers.
Manager > My Apps>
Settings
>General>Server
Master
Application
Configuration
Administrators with this privilege
can enable the Administrator to design
local user account policies and manage
the User's login according to the policy.
Manager > My Apps>
Settings > Time
Control> Application
Configuration
Domain Configuration Administrators with this configuration
privilege can configure different
domains.
Manager > My Apps>
Settings > Domain
Configuration
Server Reference / Call
Log
Administrators with this privilege can
enable a confirmation message box in
Client Manager that prompts for the
ticket number and the reason for
accessing a particular service.
Manager > My Apps>
Settings > Server
Reference / Call Log
Log Manager Service  Administrators with this privilege
can configure Log Manager Service
Settings.
Manager > My Apps>
Settings > Capture> Log
Manager Service
Service Reference
Template
Administrators with this privilege
can configure templates that prompt
Users before accessing the service from
the Client Manager.
Manager > My Apps>
Settings > Template
> Service Reference
Template
Advanced Utility Administrators with this privilege
can convert the Service Host Name and
Service Domain Name font to
uppercase.
Manager > My Apps>
Settings > Service
Modifications
> Advanced Utility
Hardware Token -
Radius Servers
Administrators with this privilege
can configure values to authenticate
the RSA portal.
Manager > My Apps>
Settings > 2FA> User
Door Access >
Hardware Token -
Radius Servers
Password Dictionary Administrators with this privilege can
configure default passwords.
Manager >My Apps>
Settings > Password
Change> Password
Dictionary
SMTP Configuration Administrators with this privilege can
configure settings for the SMTP Server
Manager > My Apps>
Settings > User> User
Security Menu > Mail
Servers> Add

## [p100]

www.arconnet.com|Copyright © 2025 100
ARCON PAM Server Privilege Description Feature Navigation
ARCON PAM Message
Board
Administrators with this privilege
can configure messages to be displayed
on pages after or before login.
Manager > My Apps>
Settings >Alert &
Notifications >
> ARCON PAM
Message Board
Dual Factor IP Range Administrators with this privilege can
define the range of IP Addresses to be
configured for the ‘Dual Factor type.’
Manager > My Apps>
Settings >2FA> Dual
Factor IP Range
SMS Gateway
Configuration
Administrators with this privilege can
configure SMS Gateway Server details.
Manager > My Apps>
Settings
>Configure> SMS
Gateway Configuration
Server Monitoring
System
Administrators with this privilege can
configure details to validate whether a
monitoring system already monitors
the service or the server.
Manager > My Apps>
Settings >API> Service
Creation Validator
>Server Monitoring
System
User Door Access
Authentication
Administrators with this privilege can
enable and configure values for the
application to authenticate or check the
user’s physical presence within the
premises.
Manager > My Apps>
Settings > Group>
> User Door Access
Authentication
Password Change
Defaults
Administrators with this privilege can
configure password change settings for
different operating systems and service
types, such as Windows, Linux, and
Oracle.
Manager > My Apps>
Settings >Password
Change > Password
Change Defaults
Voice Biometric
Authentication
Administrators with this privilege can
configure a web service for
authentication before logging into
Client Manager.
Manager > My Apps>
Settings >
Biometric> Voice
Biometric Configuration
ARCON PAM Staging
Log Server
Administrators with this privilege can
configure server details where logs will
be stored before they are transferred
to the Database Server.
Manager > My Apps>
Settings >Capture
> ARCON PAM Staging
Log Server
Web API Configuration Administrators with this privilege can
configure a number of configuration
types such as URL, description, method,
API ID, user name, and password.
Manager > My Apps>
Settings > API > Web
API Configuration

## [p101]

www.arconnet.com|Copyright © 2025 101
ARCON PAM Server Privilege Description Feature Navigation
Network Segments Administrators with this privilege can
configure a range of IP Addresses. The
Network Segment Wise Logon report
displays details based on this
configuration.
Manager > My Apps>
Manager> My
Apps>Settings >
Machine Control
> Network Segments
Global Configuration Administrators with this privilege can
configure critical configurations that
affect the application at the Global
level.
Manager > My
Apps>Settings
Schedule Password
Envelope
Administrators with this privilege can
configure password envelopes to be
sent through email.
Manager > My Apps>
Settings > Schedule
Password Envelope
LOB-wise Global
Configuration
Administrators with this privilege can
make global-level configurations from
settings.
Manager > My
Apps>Settings
ARCON PAM Server
Configuration
Administrators with this privilege
can configure server details, such as
UAT, production, and application
servers, displayed in About (Client
Manager).
Manager > My Apps>
Settings > ARCON PAM
Server Configuration
Web API Registration Administrators with this privilege can
configure machine details through
which the User can view the Service's
password.
Manager>My Apps>
Settings > API>
Registered Machines>
Web API Registration
API Reference Mapping Administrators with this privilege
can enable the ARCON API to notify
the Third Party API about service
password changes in ARCON PAM.
Manager > My Apps>
Settings >  API
Reference Mapping
Outside ARCON PAM
Access Configuration
Administrators with this privilege can
enable monitoring of Servers accessed
outside ARCON PAM and configure
actions such as sending alerts or
blocking access.
Manager > My Apps>
Settings > Outside
ARCON PAM Access
Configuration
Generic Scheduler
Settings
Administrators with this privilege can
configure critical configurations that
ARCON PAM Services and executable
files will use.
Manager > My Apps>
Settings > Generic
Scheduler Settings
Custom Commands
Configuration
Administrators with this privilege
can configure custom commands
required for password change.
Manager > My Apps>
Settings > Custom
Commands
Configuration

## [p102]

www.arconnet.com|Copyright © 2025 102
ARCON PAM Server Privilege Description Feature Navigation
LOB Wise Log Archival
Settings
Administrators with this privilege can
configure LOB-wise log Archival, which
ARCON PAM Services and executable
files will use.
Manager > My
Apps>Settings > Log >
LOB Wise Log Archival
Settings
Configure Holidays  Administrators with this privilege can
manage the holiday calendar by
configuring specific dates, including the
month, day, holiday name, and relevant
descriptions.
Manager >My Apps>
Settings > Workflow >
Configure Holidays
Configure Server tag
type
Administrators with this privilege can
configure details in Server Type
Configuration.
Manager > My
Apps>Settings >
Configure Server Tag
type
Alert Email Template  Administrators with this privilege can
configure email notifications to alert
users about activities performed within
ARCON PAM.
Manager > My Apps>
Settings > Alert &
Notifications > Alert
Email Template
Configure User Tags Administrators with this privilege can
configure and manage User Tags, which
control users' access to your site.
Manager > My Apps >
Settings > User
modifications >
Configure User Tags
Service Mandatory
Fields Configuration
Administrators with this privilege can
configure the details in the Service
mandatory field configurations.
Manager> My Apps >
Settings > Service
Modifications > Service
Mandatory Fields
Configuration
Allow Bulk Upload
Across LOB
Administrators with this privilege can
upload users across LOB using Import
Utility
Server Manager
>Tools> Import Utility
Navigation is Server
Manager > Tools >
Import Utility
Performance
Monitoring Utility
Administrators with this privilege can
access the users based on the server's
status.
Manager > Settings >
General Performance
Monitoring
Video Log Information Administrators with Video Log
Information Privileges can configure a
template displayed at the start of the
video logs.
Manager > My Apps>
Settings > > Capture >
Video Log Information
File Naming Template   Administrators with File Naming
Template Privileges can download a file
in a standardized format.
Manager > My
Apps>Settings > >
Image Quality > File
Naming Template

## [p103]

www.arconnet.com|Copyright © 2025 103
ARCON PAM Server Privilege Description Feature Navigation
Configure Enduser IP
Range
Administrators with this privilege can
configure the range of IP addresses.
Manager > My
Apps>Settings > AGW >
Configure EndUser IP
Range
Login Security -Settings Administrators with this privilege can
configure the settings of Login Security.
Manager>My Apps>
Settings > User> User
Security>Configure
Dormancy Period at
Group Level
Mail Servers Administrators with Mail server
privileges can configure settings for
SMTP and O365
Manager > My Apps>
Settings > User Security
>Mail Servers
Command
Profiler
Command Profiler Administrators with this privilege
can create, modify, or delete Elevate
and Blacklist profiles.
Server Manager >
Manage > Command
Profiler
Log Viewer View Command Log Administrators with this privilege can
view logs of the commands fired after
connecting to the server.
Server Manager >
Manage > Logs >
Command Logs
ARCON PAM Log Administrators with this privilege can
view details for the activities
performed in Server Manager.
Server Manager >
Manage > Logs
> ARCON PAM Logs
View User Access Log Administrators with this privilege can
view the login and logout details of
users who have accessed the ARCON
PAM application.
Server Manager >
Manage > Logs > User
Access Logs
View Service Access Log Administrators with this privilege can
view detailed logs of the services
accessed by the user in the ARCON
PAM application.
Server Manager >
Manage > Logs
> Service Logs
View User Validity
Status
Administrators with this privilege can
view details of all active users or those
who the Administrator has deactivated
to access the ARCON PAM application.
Server Manager >
Manage > Logs >  User
Validity Status
View Server Reference
Log
Administrators with this privilege can
view details of reference numbers used
by users before accessing services
through ARCON PAM.
Server Manager >
Manage > Logs
> Service Reference Log
View Process Log Administrators with this privilege can
view details of the processes executed
on Windows Server when a service is
accessed through ARCON PAM.
Server Manager >
Manage > Logs
> Process Logs

## [p104]

www.arconnet.com|Copyright © 2025 104
ARCON PAM Server Privilege Description Feature Navigation
View Service Password
Status Log
Administrators with this privilege can
view the service password status for
the services in ARCON PAM.
Server Manager >
Manage > Logs
> Service Password
Status
Download Video Log Administrators with this privilege can
download video logs of Command logs,
Process Logs, and Service Logs.
Server Manager >
Manage > Logs >
Process Logs (or
Command Logs or
Service Logs) > Video
Log
View Application Logs Administrators with this privilege can
view the error logs of the Client
Manager application.
Server Manager >
Manage > Application
Logs
Real-Time Session
Monitoring
Administrators with this privilege
can monitor real-time sessions.
Manager> My Apps>
Settings> Real-Time
Session Monitoring
User Activity Log Administrators with this privilege can
view SSM text and video logs.
Server Manager >
Manage > Logs > User
Activity Log
View Envelope Log Administrators with this privilege can
view the print password envelope logs.
Server Manager >
Manage > Logs >  View
Envelope Logs
View Import Utility Log Administrators with this privilege can
view the Import Utility Log.
Server Manager >
Manage > Logs >
Import Utility Logs
Service Password
Request Log
Administrators with this privilege can
view the Request Log of Service
Password.
Server Manager >
Manage > Logs >
Service Password
Request Logs
Metadata / Text Log Administrators with this privilege can
view the Metadata / Text Log.
Server Manager >
Manage > Logs >
Metadata/ Text Logs
User Status Log  Administrators with this privilege can
track the user status change at a
particular date and time.
Server Manager >
Manage > Logs >  User
Status Logs
Capture Key Stroke Administrators with this privilege can
capture the user's keystroke logs.
Server Manager >
Manage > Logs >
Capture Key Stroke
Logs

## [p105]

www.arconnet.com|Copyright © 2025 105
ARCON PAM Server Privilege Description Feature Navigation
Manage Group Add Group Administrators with this privilege can
create User and Server groups.
Server Manager >
Manage > User and
Services > Manage
Groups
Modify Group Administrators with this privilege can
modify User and Server groups.
Server Manager >
Manage > User and
Services > Manage
Groups
Drop Group Administrators with this privilege can
delete User and Server groups.
Server Manager >
Manage > User and
Services > Manage
Groups
Assign Service Group To
User Group
Administrators with this privilege can
perform User-to-service group
mapping.
Server Manager >
Manage > User and
Services > Map Group
Types
Revoke Service Group
From User Group
Administrators with this privilege can
revoke the User to Service group
mapping.
Server Manager >
Manage > User and
Services > Map Group
Types
Read Only Access Administrators with this privilege can
view details displayed under Manage
Groups, Manage Groups/Services, and
Manage Groups/Users.
Server Manager >
Manage > User and
Services > Manage
Groups (or Manage
Groups/Services or
Manage Groups/Users)
Manage LOB /
Profile
Add New LOB Administrators with this privilege can
create new LOBs and view all the LOBs
in the Select LOB/ Profile dropdown on
the Server Manager Home Page.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Manage LOB
Modify LOB Administrators with this privilege can
modify the existing LOB's name,
description, address, and Report
Header.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Manage LOB
Assign LOB To Service
Group
Administrators with this privilege can
map a Service Group to a particular
LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Service
Groups

## [p106]

www.arconnet.com|Copyright © 2025 106
ARCON PAM Server Privilege Description Feature Navigation
Revoke LOB From
Service Group
Administrators with this privilege can
remove service groups from a
particular LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Service
Groups
Assign LOB To User
Group
Administrators with this privilege can
map the User Group to LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / User Groups
Revoke LOB From User
Group
Administrators with this privilege can
remove user groups from a particular
LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / User Groups
Assign LOB To Service Administrators with this privilege can
map Services to a particular LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Services
Revoke LOB From
Service
Administrators with this privilege can
remove services from a particular LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Services
Assign LOB To User Administrators with this privilege can
map Users to a particular LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Users
Revoke LOB From User Administrators with this privilege can
remove users from a particular LOB.
Server Manager >
Manage > LOB/Profile
Master & Manager >
Map LOB / Users
Manage Services Add Service Administrators with this privilege can
create services.
Server Manager >
Manage > User and
Services > Manage
Services
Modify Service Administrators with this privilege can
modify services.
Server Manager >
Manage > User and
Services > Manage
Services
Drop Service Administrators with this privilege
can disable or delete services.
Server Manager >
Manage > User and
Services > Manage
Services

## [p107]

www.arconnet.com|Copyright © 2025 107
ARCON PAM Server Privilege Description Feature Navigation
Assign Service To
Service Group
Administrators with this privilege can
map services to a particular Service
Group.
Server Manager >
Manage > User and
Services > Map Groups/
Services
Revoke Service From
Service Group
Administrators with this privilege can
remove services mapped to the Service
Group.
Server Manager >
Manage > User and
Services > Map Groups/
Services
Assign Service To User Administrators with this privilege can
map Services to a particular User.
Server Manager >
Manage > User and
Services > Map Users/
Services
Revoke Service From
User
Administrators with this privilege can
remove Services from a particular User.
Server Manager >
Manage > User and
Services > Map Users/
Services
Windows Connection
Service
Administrators with this privilege can
add an ARCON PAM Windows service
to a service created in ARCON PAM.
Thus, if the password for a particular
service is changed with Password
Manager, the password of the
dependent service is also changed.
Manage > Password
Vault > Select service >
Prepost actions
Windows Connection
DCOM
Administrators with this privilege can
add the DCOM service to a service
created in ARCON PAM. If the
password for a particular service is
changed with Password Manager, then
the password of the DCOM service is
also changed.
Manage > Password
Vault > Select service >
Prepost actions
Windows Connection
Task
Administrators with this privilege can
add a Windows service to a service
created in ARCON PAM. If the
password for a particular service is
changed with Password Manager, then
the password of the dependent task is
also changed.
Manage > Password
Vault > Select service >
Prepost actions
Read Only Access Administrators with this privilege can
view details displayed under the
Manage Services and Map Groups/
Services tab.
Server Manager >
Manage > User and
Services > Manage
Services (or Manage
Groups/Services)

## [p108]

www.arconnet.com|Copyright © 2025 108
ARCON PAM Server Privilege Description Feature Navigation
Bulk /update Services Administrators with this privilege can
perform a bulk update of services
Server Manager
Manage → Users and
Services → Manage
Services
Change Service Root
Users to Users
Administrators with this privilege can
change the Service for Root Users to
Users.
Server Manager
Manage → Users and
Services →Change
Service Root Users to
Users
Manage Tab ARCON PAM Workflow
Tracker
Administrators with this privilege can
view workflow approval matrix logs,
user request approval overriding
workflow logs, and ticket request
workflow logs.
Server Manager >
Manage > ARCON PAM
Workflow Tracker
Manage User Add User Administrators with this privilege can
create Users.
Server Manager >
Manage > User and
Services > Manage
Users
Modify User Administrators with this privilege can
modify User details.
Server Manager >
Manage > User and
Services > Manage
Users
Drop User Administrators with this privilege can
disable a User.
Server Manager >
Manage > User and
Services > Manage
Users
Assign User Group Administrators with this privilege
can map Users to a particular User
Group.
Server Manager >
Manage > User and
Services > Map Groups/
Users
Revoke User Group Administrators with this privilege
can remove Users mapped to User
Groups.
Server Manager >
Manage > User and
Services > Map Groups/
Users
Admin Privileges Administrators with this privilege can
edit privileges.
Server Manager >
Manage > User and
Services > Manage
Users > Edit privileges
Approve User (Checker) Administrators with this privilege can
approve or reject newly created Users.
Server Manager >
Manage > Maker's
Checker

## [p109]

www.arconnet.com|Copyright © 2025 109
ARCON PAM Server Privilege Description Feature Navigation
Change User Restricted
Commands
Administrators with this privilege can
configure restricted commands, add
critical commands for approval, and
apply Configuration Commands,
Blacklist profiles, and Elevate profiles
to User and Service mapping.
Server Manager >
Manage > User and
Services > Manage
Commands
And
Server Manager >
Manage > User and
Services > Manage
Processes
Copy User Profile Administrators with this privilege can
copy entities such as LOB, User Group,
Services, Commands, or Processes
assigned to one User to another User.
Server Manager >
Manage > User and
Services > Manage
Users > Copy User
Profile
Read Only Access Administrators with this privilege can
view details displayed under the
Manage Users and Map Groups/Users
tab.
Server Manager >
Manage > User and
Services > Manage
Users (or Manage
Groups/Users)
Receive Alert On User
Creation By Maker
Administrators with this privilege and
the Approve User (Checker) privilege
will receive an alert when Maker
creates a new User.
Server Manager >
Manage > Maker's
Checker
Edit User Settings Administrators with this privilege shall
only be able to edit User settings.
Server Manager >
Manage > User and
Services > Manage
Users > Edit User
Settings
Copy Text Log Administrators with this privilege can
copy commands on the SSM monitoring
screen.
Server Manager >
Manager > Copy Text
Log
Password
Manager
Change Password Administrators with this privilege can
change the service password.
Manage > My Apps>
Password Vault >
Password Change
And
Manage > My Apps>
Password Vault >  User
and Services > Manage
Services > Change
Password Manually.

## [p110]

www.arconnet.com|Copyright © 2025 110
ARCON PAM Server Privilege Description Feature Navigation
View Server Password Administrators with this privilege can
view the service password.
Manage > My Apps >
Password Vault >  User
and Services > Manage
Services > View
Password
Generate Server
Password Envelope
Administrators with this privilege can
print password envelopes with
Envelope Status as Generated.
Manage > My Apps>
Password Vault >
Password Vault > Print
Password Envelope
Print Server Password
Envelope
Administrators with this privilege can
print password envelopes in PDF or
PIN Mailer format.
Manage > My Apps>
Password Vault > Print
Password Envelope >
Print Envelope(s)
Reprint Server
Password Envelope
Administrators with this privilege can
print password envelopes with
Envelope Status as Printed, First
Reprint, Second Reprint, Third
Reprint, Fourth Reprint, Fifth
Reprint, Sixth Reprint, Seventh
Reprint, Eighth Reprint, Ninth Reprint,
and Tenth Reprint.
Manage > My Apps>
Password Vault > Print
Password Envelope >
Print Envelope(s)
And
Manage > My Apps>
Password Vault > Print
Password Envelope >
Password Envelope(s)
For APEM Tool
Verify Reprint Server
Password Envelope
Administrators with this privilege will
be displayed as approvers in the drop-
down list to authenticate the password
printing process.
Manage > My Apps>
Password Vault > Print
Password Envelope >
Print Envelope(s)
And
Manage > My Apps>
Password Vault > Print
Password Envelope >
Password Envelope(s)
For APEM Tool
Change Password Policy Administrators with this privilege can
set constraints for a password policy.
Manage > My Apps>
Password Vault >
Password Policy Editor
Show Password Change
History
Administrators with this privilege
can view the detailed history of the
service's changed passwords.
Manage > My Apps>
Password Vault > User
and Services > Manage
Commands > Manage
Services > Show
Password Change
History

## [p111]

www.arconnet.com|Copyright © 2025 111
ARCON PAM Server Privilege Description Feature Navigation
Password Change
Process Approver
Administrators with this privilege can
authorize the password change
process.
Manage > My Apps>
Password Vault >
Password Change
Windows Connection
Password Dependency
Administrators with this privilege
can map all the different Windows
Services, Windows DCOM, and
Windows Tasks that depend on any
service of a particular server.
Manage > My Apps>
Password Vault > Select
service > Prepost
actions
Change Password
Manually
Administrators with this privilege can
manually change the service password.
Manage > My Apps>
Password Vault >
Manage Services >
Change Password
Manually.
Download Envelope
PDF
Administrators with this privilege can
download the Password Envelope in
the PDF Format.
Manage > My Apps>
Password Vault >
Envelope > Download
Envelope PDF
Download Envelope for
APEM
Administrators with this privilege can
download the Envelope for APEM
(ARCON Password Envelope Manager)
Manage > My Apps>
Password Vault >
Envelope > Download
Envelope for APEM
View Envelope for
PinMailer
Administrators with this privilege can
download the Envelope in mailer
format
Manage > My Apps>
Password Vault >
Envelope > Download
Envelope PDF
Password Reconciliation Administrators with this privilege can
reconcile the Password.
Manage > My Apps>
Password Vault >
Password
Reconciliation
Tools Tab Windows Utility Administrators with this privilege can
view the versions of the ARCON PAM
PWD service.
Manager> My Apps>
Settings > Windows
Utility
Import Administrators with this privilege can
import Users and Services into the
ARCON PAM database.
Server Manager > Tools
> Import
Privileged User
Discovery &
Reconciliation
Administrators with this privilege can
view Users created on the Server.
Server Manager > Tools
> Privileged User
Discovery &
Reconciliation
Service Discovery Administrators with this privilege can
view newly discovered services running
on the server.
Server Manager > Tools
> Service Discovery

## [p112]

www.arconnet.com|Copyright © 2025 112
ARCON PAM Server Privilege Description Feature Navigation
HSM Device
Configuration
HSM Device
Configuration
Administrators with this privilege can
configure HSM Devices in ARCON
PAM
Settings> HSM Device
Configuration
Manage
Services, ARCOS
Configuration
Modify Service Type Administrators with this privilege can
configure Manage Services in ARCON
PAM
Manager > Settings >
Manage Services
ARCOS Configuration
Manage Roles Read Only Access  Administrators with this privilege can
give Access to the Read Only User Role
in ARCON PAM.
Manager >
Administrative
Console>Manage >
UserRoles>Admin>Rea
d Only Access
Add Role Administrators with this privilege can
Add Roles in ARCON PAM
Manager >
Administrative
Console>Manage >
UserRoles>Admin >Add
Role
Modify Role Administrators with this privilege can
Modify Roles in ARCON PAM
Manager >
Administrative
Console>Manage >
UserRoles>Admin >
Modify Role
Manage Service
Group
Read Only Access Administrators with this privilege can
grant access to Read Only Users.
Server Manager
Manage → Users and
Services > Manage
Services ARCOS
Configuration.
Add Service Group Administrators with this privilege can
Add Service Group in ARCON PAM
Server Manager
Manage → Users and
Services > Manage
Services ARCOS
Configuration
Modify Service Group Administrators with this privilege can
modify the Service Group in ARCON
PAM
Server Manager
Manage → Users and
Services > Modify
Service Group
Drop Service Group Administrators with this privilege can
drop the Service Group in ARCON
PAM
Server Manager
Manage → Users and
Services >Drop Service
Group
Manage Tags Read Only Access Administrators with this privilege can
permit users to Read Only
Manager > My
Apps>Administrative
Console> Settings> Tag
management

## [p113]

www.arconnet.com|Copyright © 2025 113
ARCON PAM Server Privilege Description Feature Navigation
Add Tag Administrators with this privilege can
Add Tag in ARCON PAM
Manager > My
Apps>Administrative
Console> Settings> Tag
management
Modify Tag Administrators with this privilege can
modify the Tag in ARCON PAM
Manager > My
Apps>Administrative
Console> Settings> Tag
management
Drop Tag Administrators with this privilege can
drop Tag in ARCON PAM
Manager > My
Apps>Administrative
Console> Settings> Tag
management
4.3.3.4 Group Admin Privilege
What are Group Admin Privileges?
ARCON PAM Group Admin Privileges are assigned to Server Group Admins to grant special rights for
assigning services, viewing logs and reviewing User access. Group Admin privileges include Group Log Viewer,
Manage Services, and Manage User Request.
 Following is the list of Client Manager Privileges:
ARCON PAM Group Admin
Privileges Description Feature Navigation
Group Log
Viewer
View
Command Log
Group Admin having this privilege can view
Command Logs and Process Logs.
Server Manager >
Manage > Logs >
Command Logs
And
Server Manager >
Manage > Logs
> Process Logs
View Service
Access Log
Group Admin having this privilege can view Service
Logs.
Server Manager >
Manage > Logs
> Service Logs
One should also be assigned View Command
Log and View Process Log privileges under
Server's Privileges.
One should also be assigned View Service
Log privilege under Server's Privileges.

## [p114]

www.arconnet.com|Copyright © 2025 114
ARCON PAM Group Admin
Privileges Description Feature Navigation
Manage
Services
Assign Service
To User
Group Admin having this privilege can map Services
to a particular User.
Server Manager >
Manage > User and
Services > Map
Users/Services
And
Server Manager >
Manage > User and
Services > Group
Admin - Map
Services
Revoke Service
From User
Group Admin having this privilege
can remove Services from a particular User.
Server Manager >
Manage > User and
Services > Map
Users/Services
And
Server Manager >
Manage > User and
Services > Group
Admin - Map
Services
Change User
Restricted
Command
Group Admin having this privilege can configure
restricted commands, add critical commands for
approval, and apply Configuration Commands to
User and Service mapping.
Server Manager >
Manage > User and
Services > Manage
Commands
Manage User
Request
Service Access
Approver
Group Admin having this privilege can approve
Service Access Request.
Workflow Manager
And
Client Manager >
Server Manager >
Service Access
Request
4.3.4 Password Vault
4.3.4.1 What is ARCON | Password Vault?
ARCON | Password Vault is a centralized, secure solution designed to manage, store, and govern privileged
credentials across complex enterprise environments. It automates the lifecycle of passwords and other
sensitive credentials—such as SSH keys, access/secret keys, and certificates—used across disparate systems,
databases, web applications, SaaS platforms, and cloud environments. The module provides functionalities
including password policy configuration, automated and ad-hoc password rotation, reconciliation, credential
usage logging, and dependency management. Administrators can use a unified dashboard to monitor all
activities and enforce compliance-driven access controls.
The requested service access should be
assigned to the approver.

## [p115]

www.arconnet.com|Copyright © 2025 115
•
•
•
•
4.3.4.2 Why use ARCON | Password Vault?
Manual password management increases the risk of credential compromise, especially in large-scale IT
environments with thousands of privileged accounts. Cybercriminals, malicious insiders, and third parties
constantly target these credentials to gain unauthorized access. A single compromised privileged password can
cripple an organization’s security posture. ARCON | Password Vault mitigates these risks by automating
password generation, rotation, and storage, thereby eliminating the possibility of plaintext credential exposure.
It enables secure password management practices, simplifies compliance with regulatory standards, and
strengthens enterprise IT security through robust audit trails and policy enforcement mechanisms.
4.3.4.3 What is Password Management in ARCON | Password Vault?
Password Management in ARCON | Password Vault provides a comprehensive framework for securely
handling privileged credentials through a combination of manual, scheduled, view-triggered, and API-driven
mechanisms. It serves as an electronic vault backed by FIPS-compliant AES-256 encryption, ensuring
credentials remain secure and inaccessible to unauthorized entities. Administrators can configure password
policies, automate password rotations, enforce complexity requirements, and control user access—all from a
centralized interface. The module includes services like Manual Password Change (PCQ), Scheduled Password
Change (SPC), View-triggered Password Change, and Integrated Password Change, enabling organizations to
align with security policies and operational needs.
4.3.4.3.1 Why use Password Management in ARCON | Password Vault?
Managing privileged credentials manually across large and heterogeneous IT environments increases the risk
of mismanagement and potential breaches. ARCON | Password Vault automates password lifecycle processes
to reduce human error, eliminate plaintext exposure, and enforce strict security policies. By supporting various
rotation methods—manual for exceptions, scheduled for routine compliance, and API/view-based for dynamic
access—it ensures operational flexibility while maintaining security and audit readiness. The system also
enforces password complexity standards and usage controls, reducing the attack surface and aligning with
regulatory requirements.
4.3.4.3.2 How does ARCON Password Vault help to streamline the privileged password management process?
Enforce Strong Password Policy:  With the ability to generate strong and dynamic passwords,
administrators can ensure that the passwords created are not easily guessable, ultimately increasing
password security.
Customized password rules:  Administrators can enforce password creation rules such as length,
character use, and combinations based on the organization's password policy. This ensures that
passwords are not only strong, but are created in line with the company's security standards.
Compliance with IT security policy: Vault's password-creating parameters can be configured according
to an organization's IT security policy. This ensures that passwords are created in compliance with
security standards set by the organization.
Streamlined password management:  The engine enables administrators to change privileged
passwords/credentials in bulk at designated intervals, providing administrative efficiency and reducing
the risk of security breaches.
4.3.4.4 Dashboard Password Vault
Overview of the Password Vault Dashboard

## [p116]

www.arconnet.com|Copyright © 2025 116
The Password Vault Dashboard is an interactive interface within ARCON | Password Vault that visually
presents key credential-related metrics, password statuses, and user activities. It is designed with intuitive
widgets and graphical representations that offer a consolidated view of the privileged access environment.
Upon logging in, administrators can access the dashboard to monitor credential usage trends, review activities,
detect anomalies, and assess the current security posture—all in real time.
4.3.4.4.1 Once the user logs in to the Password Vault application, they can view the dashboard:
Refer to the respective sections to understand the widgets and charts.
4.3.4.4.2 Widgets
The widgets provide the exact count of open reviews and users under review as shown in the image below:
Refer to the following table to understand the widgets shown in the preceding screen:
Widget Name Description
Auto Rotation Disabled This widget displays the number of services on which, the password rotation is
disabled through PAM.
Passwords Expired This widget displays the number of passwords expired(i.e the credentials were
due for rotation but they haven’t been rotated)

## [p117]

www.arconnet.com|Copyright © 2025 117
•
•
•
•
Widget Name Description
Password Reconciliation
Failed
This widget displays the following values on the specified date window:
The numerator value displays the number of services on which, the
reconciliation process was successful.
The denominator value displays the total number of services on which,
the reconciliation was attempted.
*Reconciliation is the process of comparing the credentials in the PAM
repository and the target repository.
Open Password This widget displays the number of services for whom, the passwords were
opened/viewed/checked out in the specified date window.
Envelope(s) Not Printed This widget displays the number of envelopes, which were never printed on the
specified date window.
*Envelopes are made whenever a new service is onboarded in PAM or
whenever there is a credential rotation through PAM. Once envelopes are in
the generated state, they are available to be printed/checked out manually or
could be scheduled to be received in a shared drive/email. (helps in break-glass
scenarios)
4.3.4.4.3 Charts
In this section, the Administrator will be able to view the Password Vault activities in the form of charts. The
chart section includes the following:
Password Age: This chart displays the number of services categorized into different password age
buckets.
Top 5 Services With Max Password Failure: This widget displays the services with the highest number
of failed password attempts within the specified date range.

## [p118]

www.arconnet.com|Copyright © 2025 118
• Password Auto-Rotation:  This widget displays the distribution of the password rotation attempts
(success/failed) by various trigger points (Manual, SPC, VPC, IPC, etc). Here various microservices have
been built to do specific tasks, eg- the ARCON SPC service would be responsible for the scheduled
rotation of the credentials, and the ARCON VPC service would rotate the credentials that have been
checked out manually from the ARCON PAM Portal, ARCON IPC service would rotate the credentials
that have been checked out using the Vault APIs.

## [p119]

www.arconnet.com|Copyright © 2025 119
•
•
Envelope Printed Via: In this chart, the administrator can view the total number of envelopes printed via
different formats such as APEM, Pin Mailer, and PDF. Mouse hover anywhere on the chart to view the
exact count details. Refer to the legends to understand the color representation in the pie chart.
Top 5 Users Requesting Service Passwords: This chart shows the top 5 password requestors along with
their respective counts.
The Green color specifies the successful password change attempts whereas Red specifies the failed
password change attempts.

## [p120]

www.arconnet.com|Copyright © 2025 120
4.3.4.5 Password Envelope
4.3.4.5.1 What is a Password Envelope?
A Password Envelope in ARCON | Password Vault is a secure storage container that holds the most recent
credential of a service or privileged account. Whenever a new service is onboarded or an existing credential is
rotated—manually, automatically, or via API—a new envelope is generated to store the updated credential
securely within the vault. Each envelope is uniquely tied to the service it protects and is governed by access
control policies and encryption protocols to prevent unauthorized retrieval.
4.3.4.5.2 Why is the Password Envelope important?
Managing and tracking password changes without a structured system increases the risk of inconsistency,
unauthorized access, and credential leakage. The Password Envelope mechanism ensures that each credential
is stored separately, securely, and is traceable to a specific change event. This improves operational clarity,
enables detailed audit trails, and enhances accountability. By securely storing credentials in isolated envelopes,
ARCON | Password Vault minimizes the attack surface and ensures compliance with strict password
management and security regulations.
Navigation
To access the ARCON Password Envelopes, log in to the Password Vault application and click the Envelope
icon located in the left panel of the main page..
Select the service group from the Service Group dropdown and click on Go. The administrator can also select
multiple service groups using the checkbox. Based on the selected service groups, the envelope list will be
displayed:

## [p121]

www.arconnet.com|Copyright © 2025 121
Customize Columns ?
The customize columns are default columns where the user can add or remove the columns as per the
requirement.
To view Custom Columns, click on the + icon at the top right corner of the screen. Customize Columns popup
displays on the screen:
Refer to the below table to understand the data displayed in the Customize Columns screen.
Column Name Description
IP Address Enable to view the IP Address
User Name Enable to view the User Name
Service Type Enable to view the Service Type
Generated On Enable to view the date and time generated on

## [p122]

www.arconnet.com|Copyright © 2025 122
1.
2.
Column Name Description
Status Envelopes would be either be in the Generated state(i.e the credential of the
particular service has been rotated or it's a newly onboarded service or the
envelope has never been unsealed since rotation) or Printed State (if the envelope
is in the printed state that would imply that the credential has been unsealed or
viewed upon)
Credential Type Credential type can be password/ssh keys
Print Method Enable to view the method of printing (example: print via APEM tool, PDF, Pin
Mailer, etc.)
Generated By Enable to view by home the service is generated
Domain Enable to view the Domain
Instance Enable to view the Instance
Port Enable to view the port number
Host Enable to view the host address
4.3.4.5.3 Envelope Logs
What are Envelope Logs?
Envelope Logs capture all user actions performed within the Password Envelope. These logs provide valuable
insights for administrators by tracking activities related to envelopes, such as who printed the envelope, the
print method used, the date and time it was printed, and the print status.
4.3.4.5.3.1 Why are Envelope Logs important?
Envelope Logs are essential for tracking user actions within the Password Vault, ensuring accountability and
traceability of credential management activities. By logging every action taken on a Password Envelope,
administrators can identify any unauthorized or suspicious behavior, helping to prevent data breaches.
To view the logs, follow the below steps:
Click on Logs from the Action dropdown.
A popup of that particular service is displayed on the screen and the administrator can see the actions
performed by the user.

## [p123]

www.arconnet.com|Copyright © 2025 123
1.
2.
Refer to the following table to understand the grid data displayed in the preceding screen:
Column Name Description
Printed By Specifies the username of who printed the envelope
Print Method Specifies the format of the envelope printed
Printed On Specify the date and time of the envelope printed
Print Status Specifies the print status of the envelope
4.3.4.5.4 Filters
This section allows the administrator to filter the services. Follow the steps below to apply filters:
Click on the Filter icon at the top right side of the screen.
A Filters popup displays on the screen. Configure the data as required and click Apply.

## [p124]

www.arconnet.com|Copyright © 2025 124
Refer to the below table to understand the fields and data displayed on the Filters screen.
Field Name Description
Envelope Status Using the checkbox function, select the single/multiple envelope status
Generated By Check box the name by whom the envelope is generated from the drop down
Host Name Using the checkbox function, select the single/multiple host names from the
dropdown
IP Address Using the checkbox function, select the single/multiple IP addresses from the
dropdown
Service Type Using the checkbox function, select the single/multiple service types from the
dropdown
4.3.4.6 Auto Healing
4.3.4.6.1 What is the Auto Heal Feature?
The Auto Heal feature in ARCON | PAM automatically detects and corrects inconsistencies in privileged
account passwords, ensuring they are always accurate and up-to-date. This feature continuously monitors the
passwords of privileged accounts and performs automatic corrections when discrepancies are found. The Auto
Heal process ensures that passwords remain synchronized with the ARCON PAM Vault and are in compliance
with organizational security policies, reducing the need for manual intervention.

## [p125]

www.arconnet.com|Copyright © 2025 125
•
•
4.3.4.6.2 Why is the Auto Heal Feature important?
In complex IT environments, the risk of password inconsistencies—such as mismatches or outdated credentials
—can lead to unauthorized access and security breaches. The Auto Heal feature mitigates this risk by ensuring
that passwords are always in alignment with the organization's security policies. It enhances operational
efficiency by eliminating the need for manual password verification and updates, while also providing a higher
level of security by maintaining real-time password accuracy. This feature ultimately reduces the chances of
unauthorized access, improves compliance with regulatory standards, and strengthens the overall security of
privileged accounts.
4.3.4.6.3 Prerequisites
4.3.4.6.3.1 What are the prerequisites for using the Auto Heal feature?
To enable and perform the Auto Heal process in ARCON | PAM, the following prerequisite must be met:
An admin-equivalent account must be vaulted in the PAM system for the target device. This account is
used to perform password validation and correction activities during the auto-healing process.
Auto Heal must be configured at the service level. This can be done by navigating to:
Password Vault > Service Vault > Select a Service > Modify
4.3.4.6.4 Auto Heal – Configuration
4.3.4.6.4.1 What are the configuration settings required for Auto Heal?
Auto Heal settings in ARCON | PAM vary based on the Service Type. Administrators must configure root or
privileged accounts specific to the target system to enable auto-healing. The following configurations are
available:
•
•
•
Service Accounts having privileges to Change the Password of other users will only be used for
auto-healing of Passwords.
Auto-healing shall be applicable only for the following service types-
SSH Telnet
MS SQL EM - Local
MySQL QA
SSH LINUX
MS SQL QA
MS SQL EM - RDP
SSH Router
SSH Switch
SSH Firewall
SSH Unix
ORACLE QA
Auto-healing shall be attempted for all Password change Processes such as Manual, SPC, VPC,
IPC, and Reconciliation.

## [p126]

www.arconnet.com|Copyright © 2025 126
•
•
1.
2.
Configuration Description
1 Root Account For IP Service Type 7 & 16 (With Comma) Enter the username of all the privileged
user accounts( the accounts that have the
privilege of changing the password for
other users). If there are multiple user
names to be added, add them in a comma-
separated format.
2 Root account for MSSQL Database Users Password Auto Heal
3 Root account for Oracle Database Users Password Auto Heal
4 Root account for MySQL Database Users Password Auto Heal
4.3.4.6.5 Auto-Healing Process
4.3.4.6.5.1 What is the Auto-Healing process in ARCON | PAM?
The Auto-Healing process is triggered when a password operation fails or a discrepancy is detected. It
automatically initiates corrective actions to restore the correct credential state without manual intervention.
This applies to the following scenarios:
Password Change Failure during SPC (Scheduled Password Change), VPC (View Password Change),
IPC (Integrated Password Change), or Manual password update.
Reconciliation process detects a mismatch between stored and actual service credentials.
The following steps will be performed automatically by ARCON | PAM:
ARCON will automatically log in to a server for which the password has failed through the privileged
account which is configured and change the password of the actual Service
Password failure and auto-heal process logs can be viewed in the Logs.
4.3.4.7 Password Policy In Password Vault
4.3.4.7.1 What is the Password Policy in ARCON | PAM Password Vault?
The Password Policy feature enables authorized administrators to define and enforce organization-specific
rules for password complexity and structure. These policies determine the composition of passwords by setting
constraints such as:

## [p127]

www.arconnet.com|Copyright © 2025 127
•
•
•
•
•
•
•
•
1.
2.
3.
Inclusion of uppercase, lowercase, numeric, and special characters
Minimum and maximum password length
Specific character positioning rules
Restrictions on password reuse and age
These settings can be applied across servers and services managed within the Password Vault, ensuring that all
stored credentials adhere to consistent security standards.
4.3.4.7.2 Why is Password Policy important?
Weak or easily guessable passwords pose significant security risks. Without enforced policies, users may create
passwords vulnerable to brute-force attacks, dictionary attacks, or social engineering. A robust password
policy:
Ensures consistency in password strength across the enterprise
Reduces the likelihood of unauthorized access to privileged accounts
Supports compliance with internal governance and external regulations
Helps prevent data theft and security breaches caused by credential compromise
Enforcing password policies across all services and devices ensures enhanced protection of sensitive systems
and data.
Navigation:
To view the Password Policy section, navigate to: Manage > Password Vault > Policy.
4.3.4.7.3 How to Create Policy ?
Follow below steps to create Password Policy
To create a new policy, click on the + icon at the bottom right corner.
A Create Policy pop-up displays on the screen.
Admin can create their own custom password policy by configuring data in the Create Policy screen.

## [p128]

www.arconnet.com|Copyright © 2025 128

## [p129]

www.arconnet.com|Copyright © 2025 129
Refer to the table below to understand the data displayed in the Create Policy.
Field Name Description
Name Enter the Policy Name
Length Select the length for the password (Minimum 4 characters and maximum 100
characters)
Choose Characters
Upper Case Tick the checkbox to enable the use of uppercase characters in the password.
Lower Case Tick the checkbox to enable the use of lowercase characters in the password.
Digits Tick the checkbox to enable the use of Digits in the password.
Symbols Tick the checkbox to enable the use the Symbols in the password.
Constraints (The total characters should add up to the selected password length)
Minimum Character
Upper Case Set minimum uppercase characters in password
Lower Case Set minimum lowercase characters in password
Digits Set minimum numeric characters in password
Symbols Use symbolic characters in the password
Fixed Character
Upper Case Set fixed uppercase characters in the password
Lower Case Set fixed lowercase characters in the password
Digits Set fixed numeric characters in the password
The administrator can create policies to enforce specific password requirements, such as the inclusion
of uppercase and lowercase letters, digits, and symbols at the beginning, middle, or end of the
password, based on their specific needs.

## [p130]

www.arconnet.com|Copyright © 2025 130
4.
Field Name Description
Symbols Use fixed characters in the password
Advanced
Non-Repetitive Enable not to repeat the letters in the password
Ensure at least one symbol in
middle
Enable to ensure at least one symbol in the middle position
Other
Sample Password A sample password is generated, depending on the selected password policy
setting
Once all the required details are configured, click on Create. The password policy will be created and
listed on the All Policies page.
Customize Columns
Customize columns are default columns where the administrator can add or remove columns as per the
requirement.
To view Custom Columns, click the + icon at the top right corner of the screen. The Customize Columns popup
displays on the screen
Refer to the table below to understand the fields and data displayed in the Customize Columns screen.
Column Name Description
Policy Name Enable viewing the Policy Name

## [p131]

www.arconnet.com|Copyright © 2025 131
1.
2.
3.
Column Name Description
Number of services Enable to view the No. of services column
Last Modified Enable viewing the last modified date and time
4.3.4.7.4 How to Modify Policy?
The Modify Password Policy  function allows administrators to update existing password policies within the
Password Vault. This includes adjusting complexity rules, character requirements, password length, and other
parameters to ensure compliance with the organization's security standards.
Follow the steps below to modify the Password Policy:
To modify any existing policy, click the Modify button.
A Modify Policy side-over displays on the screen.
The administrator can modify the password by configuring the data in the Modify Policy screen.
4.3.4.8 Password Connectors
What is Password Connector Module?
The Password Connectors module is used to configure the commands required for custom password change
devices and applications. It removes the dependency on developers for creating database scripts for each
password change request. This is particularly useful for devices like routers, switches, and network devices,
where password changes need to be managed in a streamlined manner.
This column shows the count of number of
services that the policy has been attached to.
The Administrator, having Change Password Policy privilege in Admin Privilege, will only be able to
set/modify constraints for a password policy.

## [p132]

www.arconnet.com|Copyright © 2025 132
1.
2.
Why is it Important ?
Password Connectors allow administrators to easily define, arrange, and specify their own commands for the
password change process. This flexibility is crucial in scenarios where certain devices or applications have
unique requirements. For instance, banking applications with customized Linux OS might prompt for the
password multiple times during a change, or network devices may require delays due to slow connections. The
Password Connectors module addresses these challenges, ensuring smoother password change operations
without requiring constant developer intervention.
4.3.4.8.1 How Create Password Connector ?
To create a password connector, perform the following steps:
From the ARCON Password Vault, click on the Password Connector icon present in the left pane. The
Password Connector screen will be displayed where all the existing password connectors are listed:
Click on the Add New (+) icon, and the Create Password Connector window will appear:
The Administrator having Custom Command Configuration privilege will only be able to configure the
Password Connectors.

## [p133]

www.arconnet.com|Copyright © 2025 133
3.
a.
b.
c.
d.
e.
i.
ii.
iii.
f.
4.
1.
Specify the required inputs from the following fields:
Name: Specify the name of the password connector.
Description: Specify the description of the password connector.
Parameters:
Service Type: Select the service type from the dropdown.
Connection Type: Select the connection type. The available connections are:
SSH
Telnet
RPA
Do you want to enable this password connector?: Enable this toggle button to make the
respective password connector active.
Once, all the required fields are entered, click on Create. The password connector will be created and
listed in the Password Connector screen.
4.3.4.8.2 Configure Steps
Once the password connector is created, its steps need to be configured. These steps are nothing but a set of
commands that will be triggered sequentially whenever the respective password connector is in use for
password change.
Follow the below steps to configure steps in password connector:
From the Password Connector screen, click on the Action dropdown of the respective password
connector on which, the steps need to be configured:

## [p134]

www.arconnet.com|Copyright © 2025 134
2.
3.
4.
Click on Configure Steps.
Click the Add New (+) icon. The Add Step window appears:
Refer to the following table to understand the field-level details shown in the above screen:
Field Name Description
Command Name Specify the name of the command that would help in identification.
Command Specify the command to be executed during the password change process.
•
•
Admin can use tags by typing # which would prompt a list of
tags, for constructing a command.
Admin can also click on the document icon, which would
give information on tags and their usage.

## [p135]

www.arconnet.com|Copyright © 2025 135
Field Name Description
Command Condition Specify the command condition that needs to be checked during command
execution.
Command Response Specify the command response that needs to be captured during the
password change process.
Prompt Text Specify the prompt text that is shown during the password change process.
Password Prompt Enable this toggle button, If there is a password prompt during the
password change process.
Max Line Difference Specify the maximum line difference.
Wait Time Second(s) Specify the wait time in seconds. According to the timer interval set, the
password change process would wait for the response post executing the
command.
Active Enable the toggle button to make the respective step active.
5. Once All the required details are entered, click on Add. The step will be added to the respective password
connector.
6. Similarly, the administrator can configure more steps, which can be modified/deleted or dragged to
change the sequence. The sample screen is shown below:
4.3.4.8.3 Assign Services
Once the steps are configured in the password connector, the administrator must assign service(s) to it. Hence,
whenever the password change for the respective service is initiated, the password connector of that service
will be triggered.
To assign services to the password connector, perform the below steps:

## [p136]

www.arconnet.com|Copyright © 2025 136
1.
2.
3.
From the Password Connector screen, click on the Action dropdown of the respective password
connector on which, the service(s) need to be assigned:
Click on Assign Services. The Assign Services window appears:
Select the service group from the Service Group dropdown and click on Go. The administrator can select
multiple services using the checkbox. The services of that service group will be listed:

## [p137]

www.arconnet.com|Copyright © 2025 137
4.
1.
2.
Select the required services and click on Done. All the selected services will be assigned to the
respective password connector.
4.3.4.9 Password Rotate
4.3.4.9.1 What is Password Rotation in ARCON | Password Vault?
Password Rotation refers to the automated or manual process of regularly changing authentication credentials
—such as passwords, SSH keys, access keys, and secret keys—to limit their exposure and prevent unauthorized
access. Within ARCON | Password Vault, administrators can configure and enforce rotation policies based on
password type, usage, and criticality. The system supports both scheduled and event-driven password
rotations, ensuring that sensitive credentials are regularly updated in line with organizational security policies.
4.3.4.9.2 Why use Password Rotation in ARCON | Password Vault?
Static or outdated credentials significantly increase the risk of security breaches, especially in environments
with high volumes of privileged access. Frequent password rotation minimizes the window of opportunity for
attackers, limiting the impact of potential credential leaks. By automating the password rotation process,
ARCON | Password Vault eliminates the burden of manual updates, enforces consistency, and helps meet
compliance requirements. It ensures that critical credentials—especially those tied to privileged accounts—are
refreshed based on predefined intervals or trigger events, strengthening the overall security posture of the
enterprise.
According to the privilege(Change Password), after routing to the Password Vault application admin can
click on the Rotate icon from the left pane of the main page.
Select the service group from the Service Group dropdown and click on Go. The admin can also select
multiple service groups using the checkbox. Based on the selected service groups, the service list will be
displayed.

## [p138]

www.arconnet.com|Copyright © 2025 138
Customize Columns
The customize columns are default columns where the admin can add or remove the columns as per the
requirement. To view Custom Columns, click the +  icon at the top right corner of the screen. Customize
Columns popup displays on the screen.
Refer to the below table to understand the data displayed in the Customize Columns screen.
Column Name Description
IP Address Enable to view Service IP
Username Enable to view Username
Host Enable to view the Host address
Port Enable to view Port number
Service Type Enable to view Service Type

## [p139]

www.arconnet.com|Copyright © 2025 139
1.
2.
Column Name Description
Password Age (in days) Enable to view the age of password (in days)
Instance Enable to view Instance name
Last Password Change Enable to view the last password change(date and time)
Next Password Change Enable to view the next password change(date and time)
Domain Enable to view Domain
4.3.4.9.3 History
This section helps you to view the detailed history of the changed credentials for a selected service. It displays
details such as Service IP address, name of Privilege ID, name of the host, date & time on which the password is
changed, name of the user or service through which the password is changed, and status of the changed
password.
To View password history, follow the below steps:
Click on History as illustrated below.
A new page opens on the screen and displays the history of the password of that particular service.

## [p140]

www.arconnet.com|Copyright © 2025 140
3.
4.
As shown in the preceding screen, all the logs for the changed password of the selected service will be
displayed. Click on the View log icon of the desired log and the Log Details pop-up displays on the screen
showing all the log details:
By clicking on the Restore Password icon, the password will be restored according to the below options:

## [p141]

www.arconnet.com|Copyright © 2025 141
a.
b.
1.
2.
Before Password Change: In the event that the password change process is only performed on
the target server, choose the "Before Password Change" option from the radio button and
proceed to click on the "Restore Password" button to reinstate the previous password.
After Password Change: In the event that the password is changed exclusively in the ARCON
PAM Vault after the password change procedure, select the After Password Change radio button
and proceed to click the Restore Password button to restore the password.
4.3.4.9.4 Filters
This section helps the admin to filter the services. Follow the below steps to use filters:
Click on the Filter icon at the top right side of the screen. A Filters popup displays on the screen.
Configure the data as required and click Apply.
Restore password configuration helps the administrator during the troubleshooting phase in case of a
password failed attempt.

## [p142]

www.arconnet.com|Copyright © 2025 142
Refer to the below table to understand the fields and data displayed in the Filters screen.
Field Name Description
Host Name Using the checkbox function, select the single/multiple host names from the
dropdown
IP Address Using the checkbox function, select the single/multiple IP addresses from the
dropdown
Service Type Using the checkbox function, select the single/multiple service types from the
dropdown
Password Status Select the status of the password from the drop-down
Password Last Changed Date of Password Last Changed
Password Next Changed Date of Password Next Change
4.3.4.10 Password Reconciliation In Password Vault
What is Password Reconciliation In Password Vault ?
Password Reconciliation is the process of comparing credentials stored in the ARCON PAM repository with
those in the target system’s repository (e.g., Windows, *nix, databases). This process identifies discrepancies
between the two repositories. It is typically an ad-hoc function, allowing administrators to manually perform
the reconciliation and identify any inconsistencies or abnormalities. Additionally, if a service is marked for
reconciliation and auto-heal in the Password Vault under Service Vault > Modify service, microservices
(ARCON Recon and ARCON AH) handle the reconciliation and auto-heal processes automatically as batch
operations. Detailed logs are generated and can be accessed by the administrator in Password Vault > Logs and
in the reports.
Why is it important ?
Password Reconciliation ensures that credentials are synchronized between ARCON PAM and the target

## [p143]

www.arconnet.com|Copyright © 2025 143
systems, reducing the risk of mismatched or outdated credentials. By automating the process for services
marked for auto-heal, the system minimizes manual oversight, ensuring consistent and accurate credential
management. This automated approach, along with the availability of detailed logs and reports, enhances
operational efficiency, transparency, and security by quickly addressing discrepancies and healing them as
needed.
4.3.4.10.1 Reconcile Services
To initiate the reconciliation process for services, the administrator must access the ARCON Password Vault
application and navigate to the Reconcile  icon located in the left pane of the main page. Upon selecting this
icon, the Reconcile page will be displayed, showing a list of all previously attempted reconciliation procedures
for the available services.
Refer to the following table to understand the columns shown in the above screen:
Column Name Description
Service Displays the service name to be reconciled.
Created By Displays the username who initiated the reconciliation for the respective service.
Queue Date Displays the queue date and time on which, the reconciliation was initiated.
Reconcile Message Displays the message post-reconciliation process.
It can either display a success message or can specify the reason for the
reconciliation failure.
The Administrator having Password Reconciliation privilege in Admin Privileges will only be able to
compare entries in the ARCON PAM repository in the target system.

## [p144]

www.arconnet.com|Copyright © 2025 144
•
•
•
•
•
1.
2.
3.
Column Name Description
Reconcile Status Displays the status of the service reconciliation.
The green tick icon specifies that the reconciliation was completed.
The red cross icon specifies that the reconciliation process was failed.
The three dots (…) icon specifies that the reconciliation process is in progress.
Action The Action column contains the following actions that can be performed by the
administrator:
Reconcile
Remove
To reconcile services, perform the following steps:
From the Reconcile screen, click on the Add New (+) icon. The Service to Reconcile window will appear:
Select the service group from the Service Group dropdown and click on Go. The admin can also select
multiple service groups using the checkbox.
The following options can be configured in Settings:
User Name After Password: By enabling the "User Name After Password" feature, the password
microservice would enter the username after entering the password while constructing of
password change command. This feature is commonly used during password change processes
for certain *nix devices, simplifying the password management process.
Use Replace Keyword in Password Change (Oracle): The "Enable Use Replace Keyword in
Password Change (Oracle)" feature allows the usage of the Replace keyword during the
password change process for Oracle databases. This functionality is particularly useful for
ensuring secure password management in Oracle environments.
Use Gateway Server (ARCON PAM – Firewall): Enable Use Gateway Server (ARCON PAM
Firewall), to route the password change process through the gateway server.

## [p145]

www.arconnet.com|Copyright © 2025 145
4. Once all the required services and configurations are taken, click on Add to Queue. The reconciliation
process will be initiated for the specified services.
4.3.4.11 Service Vault
4.3.4.11.1 What is Service Vault in ARCON | Password Vault?
The Service Vault provides PAM administrators with centralized access to all password-related configurations
and actions for individual services. Through this interface, administrators can request to view service
passwords, modify password settings, review password change history, configure pre- and post-actions for
application-to-application (app-to-app) password management, and manage credential dependencies by
defining parent-child relationships between services. The Service Vault enables secure, efficient, and
controlled management of passwords and their associated operations within the enterprise IT environment.
4.3.4.11.2 Why use Service Vault in ARCON | Password Vault?
Managing service credentials at scale requires visibility, control, and the ability to adapt to dynamic operational
needs. The Service Vault simplifies this by offering a single pane of glass for viewing, updating, and auditing
password-related activities. It allows administrators to efficiently manage password lifecycles, automate app-
to-app credential handling, and enforce dependency-based password propagation—reducing manual effort and
risk of error. With features like password view requests, configuration modifications, and detailed change logs,
the Service Vault strengthens operational accountability and ensures compliance with security policies.
Select the service group from the Service Group dropdown and click on Go. The admin can also select multiple
service groups using the checkbox. The envelope list will be displayed based on the selected service groups.
Customize Columns
The customize columns are default columns where the admin can add or remove the columns as per the
requirement. To view Custom Columns, click the +  icon at the top right corner of the screen. Customize
Columns pop-up displays on the screen.

## [p146]

www.arconnet.com|Copyright © 2025 146
1.
Refer to the below table to understand the data displayed in the Customize Columns screen.
Column Name Description
IP Address Enable to view the IP address of the service.
Username Enable to view the Username of the service.
Host Name Enable to view the Host address of the service.
Service Type Enable to view the Service Type of the service.
Port Enable to view the Port number of the service.
Last Password Changed Enable to view the Last Password Change (date and time) of the service.
Password Option Enable to view the password option of the service.
Next Password Change Enable to view the next password change(date and time) of the service.
Instance Enable to view the Instance of the service.
Domain Name Enable to view the Domain Name of the service.
4.3.4.11.3 View Password
To view the password of any particular service, follow the below steps:
From the Service Vault screen, click on View Password of the desired Service from the action column
dropdown.

## [p147]

www.arconnet.com|Copyright © 2025 147
2.
3.
A View Password pop-up displays on the screen and configures the data as per the requirement.
Configure the data in the Authorize section in the View Password screen and click Authorize & View.

## [p148]

www.arconnet.com|Copyright © 2025 148
Refer to the below table to understand the fields and data displayed in the View Password screen.
Field Name Description
Request
View Historical Password Enable the toggle button to view the password history.
Description Enter Description.
Open for Hour Number of hours until which, the password should be kept open.
Open Till Date Date until which, the password should be kept open.
User(Requester) Select User from the dropdown.
Password Enter the credentials of the selected user.
Authorize
Authorizing User Select the User
Password Enter the credential of the selected user
Verification Code Enter the Captcha
4.3.4.11.4 Modify Password
To modify the password of any particular service, follow the below steps:
Reason for viewing password (min 20 characters)
A password will be sent to the requesters’ PAM mailbox

## [p149]

www.arconnet.com|Copyright © 2025 149
1.
2.
3.
Click on the Modify button from the Action dropdown for the desired Service.
A Modify Service Vault pop-up displays on the screen.
To Configure data in the Modify Service Vault screen, refer to the following table:
Field Name Description
Configuration
Rotate Enable the rotation of the password of a service
Auto Rotate Enable to Auto Rotate the password of a service
Auto Heal Enable to Auto Heal the password of a service
Rotate on Session Disconnection Enable to rotate password once the Session Disconnected from the
PAM
Policy Select the Password Policy of a service

## [p150]

www.arconnet.com|Copyright © 2025 150
1.
2.
Field Name Description
Custom Connector Select Custom Connector
Min Password age Specify the minimum age of the password
Max Password age Specify the maximum age of the password
Raise Password Request If enabled then the user/admin can raise password requests for the
particular service
Reconciliation If enabled then the service would be picked up for the reconciliation
process
3. Once all the required details are updated, click on Modify. The configurations will be modified for the
respective service.
4.3.4.11.5 Password History
This section helps you to view the detailed history of the changed passwords for a selected service. It displays
details such as Service IP address, name of Privilege ID(username), hostname, service type, date & time on
which the password is changed, name of the user or service through which the password is changed, and status
of the changed password.
To view password history, follow the below steps:
Click on History from the Action dropdown for the desired Service.
A new page opens on the screen and displays the history of the password of that particular service.

## [p151]

www.arconnet.com|Copyright © 2025 151
3.
4.
As shown in the preceding screen, all the logs for a changed password of the selected service will be
displayed. Click on the View logs  icon of the desired log and the Log Details  pop-up displays on the
screen showing all the log details:
By clicking on the Restore Password icon, the password will be restored according to the below options:

## [p152]

www.arconnet.com|Copyright © 2025 152
a.
b.
1.
Before Password Change: If the password is changed only on the Target Server after the
password change process, then select  the Before Password Change radio button and click the
Restore Password button, to restore the password.
After Password Change: If the password is changed only in ARCON PAM Vault after the
password change process, then select the After Password Change  radio button and click the
Restore Password button, to restore the password.
4.3.4.11.6 Pre-Post Actions
This section helps the admin to configure the set of actions to be performed before and after the password
change process (App to App Password Change).
We need to eliminate the risks caused by password changes in the files which are located at multiple places.
Generally, to change the password of a file existing on a different server, the administrator will have to access
that file and manually change the password. This manual process involves manually going to that server,
opening the file, and changing the password. This is quite a time-consuming task and involves a lot of risks. The
privileged user-ids, which are hardcoded carry a high degree of risk of being compromised as these user-ids and
passwords are known to be in clear text in various files on the application servers or are known to the support
team as insert this in the application configuration files during any application implementation. Also, this
creates administrative overhead as any change in such passwords has to be replicated in the applications as
well as the operating system or databases as the case may be. There are several cases wherein these passwords
are in services that need to be restarted again on updation.
Pre-requisites - Install ARCON PAM Windows Vaulting Service on the Windows Servers where the application
is installed. Port number 45045 is required to be opened from ARCOS SGS (Secured Gateway Server) to
respective Windows Servers. Powershell must be installed on the target Windows Servers
To configure the pre-post password change actions, follow the below steps:
Click on Pre-Post Action from the Action dropdown for the desired Service.

## [p153]

www.arconnet.com|Copyright © 2025 153
2.
3.
The Pre-Post action screen appears.
As shown in the preceding screen, the admin can drag and drop any of the password change actions to
Pre or Post action panels and configure the steps accordingly. As a reference, the following screen
displays if the admin wants to add the Execute Command action in the Pre-Action panel:

## [p154]

www.arconnet.com|Copyright © 2025 154
4.
5.
As shown above, the admin will have to specify the action details such as command description, source
server, command name, etc. The action details will differ based on the selection of the change action.
Once all the required action details are entered, click Create. The action will be added accordingly. The
admin can add multiple actions and can also drag and drop the configured action to reorder the
sequence:
4.3.4.11.6.1
Action Type Parameters
The action Type parameter is an important parameter that defines 4 major types of ways in which ARCON
PAM can further cause password change in the required dependent servers. To configure this parameter, the
following is a list of instances and scenarios that ARCON PAM can induce the passwords for.
Inducing passwords through Microsoft Windows-based services, APIs, Powershell, and VB scripting scripts:

## [p155]

www.arconnet.com|Copyright © 2025 155
Category  Device/OEM
OEM Service/
Feature Type
(If applicable)
Operation Type Version/ Type
ARCON PAM
Post Password
Action/
Navigation Type
OS Microsoft
Windows
Server File Transfer
from Server to
Server
2008, 2012 R2 Action Type-
Transfer File
OS Microsoft
Windows
Active Directory
Domain Account
Domain Account
Password
Change
Dependency
2008, 2012 R2 Password
Dependency
Type-Change
Password-
Update Service
Password Only
OS Microsoft
Windows
Configuration Auto Logon 2008, 2012 R2 Action Type-
Execute
Command
OS Microsoft
Windows
System Center
Operation
Manager
(SCOM)
Password
Change
Dependency
2008, 2012 R2 Action Type-
Update Through
API
OS Microsoft
Windows
Server Network Cluster
Failover Process
2008, 2012 R2 Action Type-
Update Through
API
OS Microsoft
Windows
SharePoint SharePoint
Domain Account
Password
Change
2008, 2012 R2 Password
Dependency
Type-Change
Password-
Update Service
Password Only
OS Microsoft
Windows
SharePoint SharePoint Local
Account
Password
Change
2008, 2012 R2 Action Type-
Update
Password In File
OS Microsoft
Windows
Server Scheduled Tasks 2008, 2012 R2 Windows
Password
Dependency
OS Microsoft
Windows
Server COM, DCOM 2008, 2012 R2 Windows
Password
Dependency
OS SSH Linux Configuration Auto Logon Ubuntu Action Type-
Execute
Command

## [p156]

www.arconnet.com|Copyright © 2025 156
•
•
•
•
•
•
•
•
•
•
•
•
•
Category  Device/OEM
OEM Service/
Feature Type
(If applicable)
Operation Type Version/ Type
ARCON PAM
Post Password
Action/
Navigation Type
Database Microsoft
Windows
SQL Server Dependent
Database
Password
Change
2008, 2012 Action Type-
Update Through
Registry(DSN)
Database Microsoft
Windows
SQL Server
Auditing
Dependent
Database
Password
Change
2008, 2012 Action Type-
Update Through
Registry(DSN)
Web/
Application
Server
Oracle
WebLogic
WebLogic
Application
Server
Dependent
Server Password
Change
11g, 12c Action Type-
Update
Password In File
Web/
Application
Server
Apache Tomcat Tomcat
Application
Server
Dependent
Server Password
Change
7.0, 8.5 Action Type-
Update
Password In File
Web/
Application
Server
Microsoft
Windows
Internet
Information
Service
Anonymous,
Application Pool
Password
Change
2008, 2012 R2 Action Type-
Execute
Command
Driver- based Microsoft JDBC driver Dependent
Server Password
Change
6.0 Action Type-
Update Through
Registry
Driver- based Microsoft ODBC driver Dependent
Server Password
Change
13.1 Action Type-
Update Through
Registry
Other actions available for the App-to-App password management process-
Execute a BOT process
Execute a command
Execute a PowerShell command
Map a linked server
Map network drive (with credentials)
Send email
Perform action(like start, shutdown) Oracle DB
Start / Stop IIS Website
Start / Stop Windows services
Transfer file
Update password in file/files
Update the password in IIS App pool
Update through API

## [p157]

www.arconnet.com|Copyright © 2025 157
•
•
•
1.
2.
3.
4.
5.
Update password for Windows service
Windows COM+ devices(eg- DCOM,SCOM)
Windows task scheduler
& many more...
Some of the App to App Password management Use Cases -:
4.3.4.11.7 Use-cases
Use-cases - Fulfilled
Service Accounts
For a service instance that logs
on with a user account, rather
than the LocalSystem account,
the Service Control Manager
(SCM) on the host computer
stores the account password,
which it uses to log on to the
service when the service starts.
As with any user account, you
must change the password
periodically to maintain security.
Stop Services on the Application Server
Stops the service running on the Application Server using the Service
Name.
Start Services on the Application Server
Starts the service running on the Application Server using the Service
Name.
Update the Password in Service Accounts
When you change the password on a service account, it is required that the
password stored by the Service Control Manager must also be updated.
Database Accounts
Generally, in order to provide
your connection information to a
particular Database account, a
connection string is used.
Change the Password of the Database
Changing the password of a Database user using a database query.
Make Changes to ODBC Drivers
Updating the new password of the database user used in the connection
string of the ODBC Driver. A manual restart of the ODBC Driver is
required.
Credentials in Web.config files
There are a number of important
settings that can be stored in the
configuration file. Some of the
most frequently used
configurations, stored
conveniently inside Web.config
file are:
Database connections
Caching settings
Session States
Error Handling
Security
Update the Password in Web.config
Update the new password of the database user in the connection string
web setting
Update a string in configuration files using the keyword
Update the new password in a particular string inside the config files with a
specific keyword.
For example, cred=”pass@123” (a string in the config file) then by
mentioning “cred” as the keyword, the new password will be updated in the
place of “pass@123”.

## [p158]

www.arconnet.com|Copyright © 2025 158
Use-cases - Fulfilled
Update the password in the Batch file
This will update the password in the file (batch file) and execute the same.
For example, assuming the CP.bat file contains the following command.
sc config "TEST Plugin" password=%1
echo success
0Select the Execute Commands option from the Action Types dropdown
and mention the file path and the password tag following it in the Source
File section. “C:\CP.bat <AUSRNP>”
Website Accounts
In order to ensure the security
isolation of Websites in a shared
hosting environment, using a
dedicated user account as an
identity for the application pool is
recommended.
Restart the Website in IIS
Stop and Start the Website in IIS using the Website name.
Update the Password in Application Pools
Update the new password for the account associated with the Application
Pool Identity in the Application Pools.
Execute Commands with the
new password
Execute PowerShell Commands
Perform advanced tasks to be performed on the server with the updated
password using the <AUSRNP> tag wherever required.
Following is the list of tags that can be used in the command.
Tag Description
<AIPADD> IP Address of the service
<AHSTNM> Host Name of the service
<ADOMNM> Domain Name of the service
<ADBINS> DB Instance of the service
<AUSRID> User ID of the service
<AUROP> User Original Password of the service
<AUSRNP> User New Password of the service
<EQ> This will be replaced with an equal sign =
<DQ> This will be replaced with the double quote “
<SQ> This will be replaced with a single quote '
<CBO> This will be replaced with Open curly braces {
<CBC> This will be replaced with Closed curly braces }

## [p159]

www.arconnet.com|Copyright © 2025 159
Use-cases - Fulfilled
<NEWLINE> This will be replaced with \r\n
Network Drive User Accounts
Applications use Drive maps to
simply associate a single drive
letter to files and folders that
reside on file servers.
Reconnect Network Drive
To save a mapped drive in the user's settings and attempt to restore it at
each subsequent login, reconnecting to the Network Drive is necessary.
Otherwise, the drive is mapped, but not saved in the user's settings.
Reconnect Network Drive with User Credentials
To implement a drive mapping using the credentials of the privileged
account.
File Transfer Transfer Files from Linux to Windows & Citrix Servers
Copy files from the source server to the destination server. This can be
done on SSH Linux and Windows RDP.
Notify Admins Send Email
This function will trigger a mail as per configuration. This can be done to
trigger a mail pre or post-password change as per requirement. We can
also encrypt the password in the mail before sending it.
Use-cases - Under Development
Update password using User
Interface
Execute utility to prompt for Password
Update UI of Management Consoles
Update the Passwords in UI-based .exe locations

## [p160]

www.arconnet.com|Copyright © 2025 160
1.
Using BOT Process
Enter the BOT Path and BOT Parameters to enable RPA BOT to perform
password changes using RPA.
Encrypted Credentials Execute commands to decrypt-update-encrypt .config files
Execute a utility to encrypt a new password in a string
Use Encrypted Passwords to update files
Others Update Password for COM+ Components
Make Changes in Regedit
Update the Password in Linux Management consoles
4.3.4.11.8 Sample Applications
4.3.4.11.8.1 Microsoft SharePoint
Assuming the Microsoft SharePoint is installed on server 10.10.4.17. Moreover, the Microsoft SharePoint
service is running under the user “anbglobaldc\soumya.das1”. When the password rotation triggers due to
Scheduled Password Change Service the password will be rotated on the Microsoft Active Directory Server. In
order to update this password in the Service Account Post password change action must be configured.
To configure pre or post password change actions use the following path:
In Password Vault →  Vault, select the ARCON PAM Domain Service under which the Microsoft
SharePoint is running.

## [p161]

www.arconnet.com|Copyright © 2025 161
2.
a.
Explore further options by clicking on the downward-pointing arrow  located adjacent to the View
Password feature, and then opt for Pre-Post Actions to access additional functionality.
The system administrator will proceed to select and drag the appropriate password change
action that needs to be executed in the pre-post actions section. In this particular scenario, the
chosen action is the Execute PowerShell Command. 0

## [p162]

www.arconnet.com|Copyright © 2025 162
3.
4.
i. Provide a description for the selected action to ensure clarity and specificity.
ii. Provide the command necessary to achieve the service account password updation as required.
iii. To activate the action, 'Turn On' the toggle for 'Do you want to enable this action?'.
iv. After ensuring all details are correctly entered, click on the 'UPDATE' button to execute the
action.
#####Powershell Script Starts#####
Stop-SPService -Identity “Microsoft Sharepoint Foundation“ ##Stop the
Microsoft Sharepoint Service
$m = Get-SPManagedAccount -Identity “ANBGLOBALDC\Pratap.Patil“
Set-SPManagedAccount -Identity  $m -NewPassword <AUSRNP> -ConfirmPassword
<AUSRNP> ## Update the password
Start-SPService -Identity “Microsoft Sharepoint Foundation“  ##Start the
Microsoft Sharepoint Service
#####Powershell Script Ends#####
Post Password change action has been successfully configured.
Stop Website - Select the Stop IIS Website from the Drag Password Change Action panel. Provide the
Website Name of the service that should be stopped.

## [p163]

www.arconnet.com|Copyright © 2025 163
5.
6.
Update password in file - Select the Update Password in File from the Drag Password Change Action
panel. Provide the File Path of the file that should be updated.
Start Website  - Select the Start IIS Website  from the Action Type  dropdown. Provide the Website
Name of the website that should get started.

## [p164]

www.arconnet.com|Copyright © 2025 164
7. On the following screen, you can see all the pre-actions and post-actions configured for this service.
4.3.4.11.8.2 Swift
To maintain the security and integrity of your business data, it is essential to keep your Swift application
updated with the latest passwords. With ARCON's Pre-Post Password Change Actions, you can easily update
your Domain account password on the AD server and Swift service simultaneously, without any hassle.
Additionally, our platform provides the flexibility to configure the re-mapping of network drives on the servers,
ensuring that your file storage is always mapped correctly. By automating these critical actions, you can
minimize the risk of unauthorized access and protect your business from potential security breaches.

## [p165]

www.arconnet.com|Copyright © 2025 165
1.
2.
3.
Stop Service - Select the Stop Windows Service from the Drag Password Change Action panel. Provide
the Service Name of the service that should get stopped.
Update Service Account Password  - Select the Update Windows Service Logon User Password  from
the Drag Password Change Action panel. Provide the Server Name.
Start Service  - Select the Start Windows Service  from the Drag Password Change Action  panel.
Provide the Service Name of the service that should get started.

## [p166]

www.arconnet.com|Copyright © 2025 166
4.
5.
Reconnect Network Drive  - Select the Map Network Drive  from the Drag Password Change Action
panel. Provide the Network Path and Network Drive to map it to.
On the following screen, you can see all the pre-actions and post-actions configured for this service.

## [p167]

www.arconnet.com|Copyright © 2025 167
1.
2.
3.
4.3.4.11.8.3 Huawei Local Maintenance Terminal - RPA Bot Process
RPA bot will fetch all the information about the password change process steps (JSON File) from the
ARCON PAM Database via API.
Once the RPA bot is ready with all the prerequisites, it will launch the application/browser on the
server. As soon as the application is launched, the RPA bot starts taking screenshots of the screen.0
RPA bot will log in using the credentials fetched from ARCON PAM Vault.

## [p168]

www.arconnet.com|Copyright © 2025 168
4.
5.
RPA bot will compare the screenshot with the information configured in the JSON file fetched. It will
then locate the different parameters' coordinates on the screen and fill the values in the respective field.
RPA bot will execute password change. RPA bot will fetch the old password and password policy from
the ARCON PAM Vault using the ARCON PAM Vault API.

## [p169]

www.arconnet.com|Copyright © 2025 169
6.
7.
Log out of the system 0
It will reconcile that the password change is successful by re-authenticating with the application using
the same RPA process. In case, it is unsuccessful it must roll back and notify the Admin accordingly.
Log Generation
Records every step of the password change process. Text logs of the process must be visible in the server
manager. For example, Connected to RPA bot, Performing RPA, RPA successful, and others.  At what step the
error occurs must be recorded.

## [p170]

www.arconnet.com|Copyright © 2025 170
•
•
•
•
1.
4.3.4.11.8.4 WSB2BAutomation
In order to ensure seamless and secure access to our business-critical data, it is essential to update the
passwords for SQL and Oracle databases used in our application. This not only involves updating the password
on the database server but also requires us to modify the web.config file to reflect the new password in clear
text. Additionally, we need to update the DSN settings of the respective application servers to ensure
uninterrupted connectivity to the databases. By taking these necessary steps, we can safeguard our sensitive
data and maintain the reliability of our application.
4.3.4.11.9 Other Applications
Automated Teller Machine (ATM)
SailPoint
Sonicwall Firewalls
Okta
4.3.4.11.10 Dependency
Dependency helps to create a parent-child relationship, which helps the administrator in the Password
management process such that if the credential of the parent service is rotated then on similar lines the
credentials for the child services should also be managed according to the dependency types like Change
Password - Process With New Password, Change Password - Process With Same Password, Change Password -
Update Service Password Only.
To configure a dependency for any service, perform the following steps:
Click on Dependency from the Action dropdown for the desired Service.

## [p171]

www.arconnet.com|Copyright © 2025 171
2.
3.
The Dependency screen for the respective service will be displayed where all the dependent services of
the selected service (parent) will be listed. Admin can also view the Service that the selected service is
dependent upon:
To add new child services, click on the Add New Service icon. The Add Service pop-up will be displayed:

## [p172]

www.arconnet.com|Copyright © 2025 172
4.
a.
b.
c.
1.
Select the services that need to be added and select the password dependency type from the dropdown.
There are three options available:
Change Password - Process With New Password: It will change the password of the depending
service with the different(new) password of the parent service.
Change Password - Process With Same Password: It will change the password of the depending
service with the same password of the parent service.
Change Password - Update Service Password Only: It will update the password of the depending
service with the same password of the parent service only in the ARCON PAM vault.
Here in options -: a,b- the credential at the target device is also propagated according to the definitions of the
options.
4.3.4.11.11 Change Password Manually
There can be use cases where the administrator might want to handle the Password Change Process manually
for some servers. So after changing the password manually on the target server, to maintain the sync with
Vault, the admin might need to change the password manually on Vault as well.
So the Manual Password Change allows the admin to update the password in the ARCON PAM vault(manually)
or copy the password of an existing identity from the Vault.
Perform the below steps to change a password manually for any identity:
From the Service Vault screen, go to the respective asset tab.
•
•
The Change Password - No of User(s) Authentication configuration must be enabled from the
global configuration to modify passwords.
Users having the Change Password privilege can modify passwords.

## [p173]

www.arconnet.com|Copyright © 2025 173
2.
3.
a.
i.
The Change Password Manually panel will be displayed on the screen.
There are two ways to change the password manually, such as Update Vault and Copy from the Vault:
Update Vault
Select the Update Vault radio button to change the password with a new password.

## [p174]

www.arconnet.com|Copyright © 2025 174
ii. Enter a new password and re-enter the same password to confirm the password in
respective fields.

## [p175]

www.arconnet.com|Copyright © 2025 175
iii. Enable the “Do you want to vault with the new password immediately “ toggle if you want
to apply this password immediately. (The password change microservice would be
responsible for connecting to the target device and rotating the known credentials as per
the Password Policy configured and vault the same in the highly secure ARCON PAM
vault. The use case of providing this feature; after Manual password Change, is because
the Passwords on Target and Vault are now in Sync and ready to be rotated as ARCON
PAM Password Policy).

## [p176]

www.arconnet.com|Copyright © 2025 176
iv. Click on the Change button.

## [p177]

www.arconnet.com|Copyright © 2025 177
v.
b.
i.
A popup displays on the screen stating “Do you want to change password manually?“
Click Yes.
Copy from the Vault
Select the Copy from the Vault radio button to copy the password for any identity:

## [p178]

www.arconnet.com|Copyright © 2025 178
ii. From the Search Type drop-down, select Identities with the same Domain Name & User
Name or Identities with the same IP address. (This functionality would ease out the
administrator's role in filtering out identities/accounts).

## [p179]

www.arconnet.com|Copyright © 2025 179
iii. Select any identity from the Identity drop-down.

## [p180]

www.arconnet.com|Copyright © 2025 180
iv. Click Change. The password will be changed.
Refer to the table below to understand the fields:
Field Name Description
Update Vault
New Password Enter a new password.
Confirm Password Re-enter the same password for confirmation.
Copy from the Vault
Search Type Select the type of search required for filtering the identities.
Identity Select the identity from the drop-down list.
The configuration Max Hours For Service Password Duration  in the global settings enables the
customization of the maximum duration for asset password expiry. Once this duration is reached, the
asset password will expire.

## [p181]

www.arconnet.com|Copyright © 2025 181
1.
2.
4.3.4.11.12 Filters
This section helps the admin to filter the services. Follow the below steps to use filters:
Click on the Filter icon at the top right side of the screen. A Filters popup is displayed on the screen.
Configure the data as required and click Apply. Refer to the below table to understand the fields and
data displayed in the Filters screen.
Field Name Description
Password Option Using the checkbox function, select the single/multiple password options from
the dropdown.(for eg whether the credential was stored based on single/split
custody)
Host Name Multi-select the hostnames to filter the data
Service IP Multi-select the IP Addresses to filter the data
Service Type Multi-select the service type to filter the data
The Only Server Group Admin Can Perform Password Change-Is Enabled configuration enables
administrators to limit the password change privileges to the group admin only.
Users having the Password Change Process Approver Policy privilege can approve password change
requests.

## [p182]

www.arconnet.com|Copyright © 2025 182
1.
2.
3.
4.
Field Name Description
Password Last Changed Date of Password Last Changed
Password Next Changed Date of Password Next Changed
4.3.4.11.13 Bulk Service Vault Modification
The bulk modification is a new enhancement that allows the administrator user to modify multiple service
vaults at the same time. The updated values will be reflected to the selected services. To check the updated
values, the user can open the modify option in the Action field, the modification window will pop up.
Proceed with the following steps to bulk modify the service vaults,
Navigate to Password Valult > Service Vault.
Click the dropdown field of service group and select. The list of services from the selected service group
will be listed in table format below.
Select the multiple services. The Modify option will display below the export option.
Click Modify. The modify screen will pop up as below.
The Service Group dropdown allows the user to select the service group which belongs to the
respected LOB.

## [p183]

www.arconnet.com|Copyright © 2025 183
5.
6.
To understand the field-level description, refer to the following table:
Field Name Description
Rotate Enable the Rotate toggle to allow password rotation for the services.
Min Password age Enter the minimum age of the password. The password age is the number of
days the password of the services will be active in the ARCON PAM.
Max Password age Enter the maximum age of the password. The password age is the number of
days the password of the services. will be active in the ARCON PAM.
Raise Password Request If enabled then the user/admin can raise password requests for the particular
service.
Reconciliation If enabled then respected services would be picked up for the reconciliation
process.
Click Modify. The pop-up screen will display to ask the confirmation before updating the modification.
Click Yes. The configuration is now modified for the selected services.
4.3.4.12 Password Logs
What is Password Logs
The Password Log tracks details for all services whose credentials have been rotated. These credentials can
include passwords for various devices (Windows, *nix, databases), web applications, SSH keys, access keys,
secret keys, and more. The log provides critical information such as the Queue ID, the timestamp when the log
was generated, the count of services affected by the password change process, and the initiator of the rotation
(whether it's the administrator or a password change microservice like SPC, VPC, IPC, Recon, or ARCONAH).

## [p184]

www.arconnet.com|Copyright © 2025 184
1.
The administrator can view detailed logs for each queue ID, including the type of service, the host name, the
date and time the password rotation was initiated, and the status of the rotation process.
Why is it important ?
The Password Log serves as a comprehensive audit trail for password rotation activities, ensuring transparency
and accountability in the credential management process. By capturing detailed logs for each password change
event, administrators can easily track and verify which services have undergone changes, identify any issues
during the rotation, and review the status of the process. This feature enhances security by providing full
visibility into credential updates and helps in troubleshooting any discrepancies in the password change
process.
The administrator can select ‘from date’ and ‘to date’ as per the requirement.
Click anywhere on the Queue ID  grid and all the service details of that particular Queue ID are
displayed.
The details can be fetched for a maximum of up to 90 days (3 months) and a minimum of two days in
the past from the current date. By default, the current date is selected in the From and To date fields.

## [p185]

www.arconnet.com|Copyright © 2025 185
2.
3.
To view log details of any service, click anywhere on the Service grid. A Log Description Popup displays
on the screen and shows detailed logs of that service.
Click Refresh to refresh the screen.

## [p186]

www.arconnet.com|Copyright © 2025 186
4.
1.
Click Export to export the logs.
4.3.4.12.1 Filters
This section helps the admin to filter the services. Follow the below steps to use filters:
Click the Filter icon at the top right side of the screen. A Filters popup displays on the screen.

## [p187]

www.arconnet.com|Copyright © 2025 187
2. Configure the data as required and click Apply. Refer to the below table to understand the fields and
data displayed in the Filters screen.
Filed Name Description
Service Group Using the checkbox function, select the single/multiple service group from the
dropdown
Rotation Initiated
By
Select the name of the admin who initiated the rotation of the password from the
dropdown list
Credential Type Select the credential type as Password or SSH Key from the dropdown
Rotation Status Select the rotation status filter as failed or success from the dropdown
4.3.4.13 Downloads
The Downloads page in the Password Vault Application provides privileged users with secure access to
downloadable log files and password envelopes. This feature is designed to help administrators and authorized
personnel efficiently track activity logs, manage file exports, and access historical data as needed.
The Downloads section displays a list of password envelopes generated within the system. Users with the
appropriate permissions can download these password envelopes directly from this section. Each download is
monitored, and logs are maintained.
The "Download" option is available based on user privileges given under Server Manager -> User
Privileges -> Download Schedule Password Envelope

## [p188]

www.arconnet.com|Copyright © 2025 188
1.
Refer to the table below to understand the columns in Downloads:
Column Name Description
LOB Name It displays the Line of Business (LOB) or application area
associated with the exported file.
File Name It displays the name of the exported log file. It typically
includes the LOB name and timestamp
File Path It displays the file system path where the log file is stored on
the server or local drive.
Printed On It displays the date and time when the file was generated or
printed.
Printed By It displays the username or system account that generated or
printed the file.
4.3.4.13.1 Download Envelope
Follow these steps to download the envelope:
Click the Download button from the action dropdown as illustrated below.

## [p189]

www.arconnet.com|Copyright © 2025 189
2.
1.
2.
The password envelope will be downloaded to the local device.
4.3.4.13.2 View Logs
The View Logs  option on the Downloads screen allows users to view detailed audit logs related to each
downloaded file.
Follow these steps to view the logs:
Click the Log button from the dropdown as illustrated below.
The logs for the selected LOB are displayed.

## [p190]

www.arconnet.com|Copyright © 2025 190
Customize Columns
Customize columns are default columns where the administrator can add or remove columns as per the
requirement.
To view Custom Columns, click the + icon at the top right corner of the screen.
Click Refresh to refresh the page.

## [p191]

www.arconnet.com|Copyright © 2025 191
•
•
•
•
•
•
•
•
•
Click Export to export the data in CSV format.
4.3.5 Tool Management
4.3.5.1 What is Tool Management?
The Tool Management feature in Server Manager offers a comprehensive suite of tools designed for managing
tasks such as real-time session monitoring, application password changes, and user privilege discovery. The
following tools are included:
Real Time Session Monitoring
Windows Utility
Import
Privilege User Discovery and Reconciliation
Service Discovery
4.3.5.2 Why is Tool Management Important?
Tool Management plays a crucial role in maintaining operational efficiency and security. The tools help in:
Real-Time Monitoring: Tracking live sessions and ensuring secure access control.
Password Management: Automating password changes and ensuring compliance with security policies.
User Discovery: Identifying privilege users and reconciling user data to prevent unauthorized access.
Service Discovery: Monitoring services to ensure proper functionality and integrity.

## [p192]

www.arconnet.com|Copyright © 2025 192
1.
4.3.5.3 Service Discovery
4.3.5.3.1 What is Service Discovery?
The Service Discovery  feature allows you to view and manage all newly discovered services running on the
server. This functionality helps administrators identify active services and ensure that all relevant services are
correctly monitored for security and performance.
To enable this feature, ensure that the ARCON DeskInsight Master service  is installed on the Database
Server. You must configure device details in the ARCONDeskInsightMaster.ini  file, which is located in the
folder on the Domain/Application Server where the service has been installed.
To view discovered services use the following path:
ACMO → Server Manager → Tools → Service Discovery
Select the required Protocol Type, Group, and then click the Search button.
2. Server list appears. Right-click the server and click the Search Service Discovery  option to get the
discovered Services.
3. The Service Discovery processing screen appears and then the Service list appears.
•
•
Configure the toggle value of Auto Discovery in  Manage Service is Enabled to view the
Discovered Services.
Win Vaulting Service must be installed & running on the Target Windows Server.

## [p193]

www.arconnet.com|Copyright © 2025 193
4.3.5.4 Windows Utility
4.3.5.4.1 What is Windows Utility?
The Windows Utility  tool is used to monitor the ARCON PAM PWD service  on Windows servers. It checks
whether the password change service is installed and running on the servers configured for password changes
through ARCON PAM. If all the servers are equipped with a password change service and there is a need to
check whether the password change service is installed or not, you can run this utility to validate This utility
specifically applies to Windows connections only.
It does not initiate password changes but simply validates the presence of the password change service on each
server.
To navigate to Windows Utility, use the following path:
Tools → Windows Utility
The Administrator having Windows Utility privilege in Server's Privilege will only be able to view the
version of the service.

## [p194]

www.arconnet.com|Copyright © 2025 194
• Click Check Service Version. The status of the log are displayed on the right panel and the services that
are connected will display the version on the left panel

## [p195]

www.arconnet.com|Copyright © 2025 195
•
•
If the user does not want to gather version information for all services, click on the required service and
click the Delete button on the keyboard or right-click on the service and click Delete or user can select
and drag using the mouse and click delete to remove from the list. Similarly, the user can check the
version for a single service by right-clicking on it and clicking the Check Service Version option.
Status for final output screen:
Output Status displaying Service Version describes that ARCON PAM PWD service is installed
on a server and its version details are captured.
Output Status displaying A Connection Attempt Failed describes that the connectivity to the
destination server is not possible or has some issue reaching the server.
The Export Version button exports version details in Excel format and the Export Log button exports
log details in text format.
•
•
The password change port number 45045 is displayed in the text box against the ARCON PAM
Windows Password Change Service Port.
You can check the WinPWD Services version via gateway by selecting the Use Gateway Server
(ARCON PAM - Firewall) checkbox.

## [p196]

www.arconnet.com|Copyright © 2025 196
•
•
•
•
•
•
•
•
•
•
4.3.5.5 Privilege User Discovery and Reconciliation
4.3.5.5.1 Privilege User Discovery and Reconciliation
4.3.5.5.1.1 What is Privilege User Discovery and Reconciliation?
The Privilege User Discovery and Reconciliation feature is designed to identify and evaluate user accounts on
target systems during the initial resource deployment phase. This process allows ARCON PAM to quickly load
account information from systems such as Linux, Windows, and databases.
Discovery  identifies existing user accounts but does not automatically add them to ARCON PAM or
trigger workflows.
Once an input account is matched (correlated) with an existing ARCON PAM user, the system uses it to
discover other accounts on the same server.
Reconciliation compares ARCON PAM’s internal account index with the actual accounts present on the
resource, enabling further analysis.
Key reconciliation capabilities include:
Detecting new accounts
Correlating accounts with existing ARCON PAM users
Identifying unassociated accounts
The Users Auto–Discovery component facilitates automatic discovery of server-level users across supported
platforms such as Linux, Windows, and databases.
4.3.5.5.1.2 Why is Privilege User Discovery and Reconciliation Important?
This feature is critical for:
Initial Onboarding: Simplifying the integration of new systems by quickly identifying user accounts.
Accuracy and Audit Readiness: Ensuring that the account information within ARCON PAM accurately
reflects what exists on the target systems.
Security and Compliance: Detecting unauthorized or unmanaged accounts that may pose security risks.
Operational Efficiency: Automating the discovery process reduces manual effort and ensures
consistent visibility across the infrastructure.
To configure Auto Discovery, use the following path:
Manage → Users and Services → Manage Services
The Administrator, having Privileged User Discovery & Reconciliation privilege in the Server's
Privilege will only be able to view Users created on the Server.

## [p197]

www.arconnet.com|Copyright © 2025 197
1.
2.
Follow the steps below to configure Auto Discovery:
Select the type of service, such as SSH Linux or Windows RDP, from the Service Type dropdown list and
click the Refresh button. The services are displayed in the grid.
Right-click on the service and choose the Modify Service Parameters option.
Users can change or update specific service details by selecting a field from the Available Services
window. For example, if the "IP Detail" field is selected, clicking on the corresponding cell will make it
editable, allowing users to modify the value directly.

## [p198]

www.arconnet.com|Copyright © 2025 198
3.
4.
Click the Modify Service Parameters option. The Manage Services – Modify Parameters window pops
up.
Select the Enable checkbox beside the Auto Discovery field and click the Modify button to auto-
discover all the users.
To validate the process, use the following path:
Tools → Privileged User Discovery & Reconciliation

## [p199]

www.arconnet.com|Copyright © 2025 199
1.
a.
b.
c.
d.
e.
f.
g.
h.
2.
Follow the steps below to validate the process:
Select the type of protocol from the Protocol Type dropdown list. The following protocol types are
displayed in the drop-down list:
Database-DB2
Database-MSSQL
Database-Oracle
Desktop-Windows
Server-Unix-SSH
Server-Windows
SSH Router
Telnet Router
Select the service group from the Select Group drop-down list and click Search. The services that have
been enabled for Auto-Discovery will be displayed.
To search for a particular service, enter the required details in the Search filter field.

## [p200]

www.arconnet.com|Copyright © 2025 200
3.
a.
b.
Right-click on the Service,
Select the Start User Discovery option to discover users for the selected service.
Select Start User Discovery using the Sudo Privilege option when the sudo command is required.
If you do not want to discover users for all services, select the service which you want to
delete and click Delete button on the keyboard or right click on service and
select Remove From List option.

## [p201]

www.arconnet.com|Copyright © 2025 201
4.
5.
•
Click the Start User Discovery option. A window pops up with the following message
ARCON PAM Validation Process Completed.
Click OK to view the list of all the users belonging to the particular server
Auto Discovery for particular Service Types:
The auto-discovery for particular service types are as follows:
For SSH-Based Services: You need to have a “root” account in ARCON PAM to fetch the details.
•
•
•
•
The port number for Windows RDP-based services is 45045.
The Export Log button saves or downloads the generated logs in .csv format.
Start User Discovery button allows you to discover all the users in a sequence on all the target
servers.
Use Gateway Server (ARCON PAM – Firewall) to route you to a service through a gateway
server.

## [p202]

www.arconnet.com|Copyright © 2025 202
•
•
•
For Windows-Based Services: For Windows servers, you need to install the “ARCOS win PWD service”
and port”45045” should be open from the ARCON PAM secured server.
For Databases: MS SQL / SQL QA, for MS-SQL users, auto-discovery, the SQL user should have
“sysadmin” rights.
SSH Oracle SQL Plus: You need to have “Oracle” user access.
Schedule User Discovery
The PAM admin can schedule the Privilege User Discovery using the scheduling option.

## [p203]

www.arconnet.com|Copyright © 2025 203
1.
2.
To schedule the privileged user Discovery, use the following steps:
A schedule option is provided to schedule the "Privilege User Discovery.
After clicking on the Schedule option, A Service can either be searched for or uploaded for privileged
user discovery.

The Schedule Privilege User Discovery screen contains the following fields
Field Name Description
Create (radio
button)
Create a new Privilege User Discovery scheduler.

## [p204]

www.arconnet.com|Copyright © 2025 204
a.
i.
ii.
iii.
iv.
v.
vi.
b.
Modify
(radio
button)
Modify details of an existing Privilege User Discovery scheduler.
Search
Services
A Section Search Services will be displayed on selecting this radio button.
Select the type of protocol from Protocol Type drop down list.The
following protocol types are displayed in the drop down list:
Database-DB2
Database-MSSQL
Database-Oracle
Desktop-Windows
Server-Unix-SSH
Server-Windows
Select the service group from Select Group drop down list and
click Search. The services which have been enabled for Auto Discovery
will be displayed.
Browse File Browse File to Upload Services section will be displayed on selecting this radio button.
Steps to upload a file.
Click Download file template and save the file to a preferred location on to
your local machine.
Open the saved template and enter the required details and save the file.
Copy all the file content in to .txt file and save it.
On the Schedule Privilege User Discovery screen, Browse the .txt file
Click Validate.
Scheduler
Parameters
Enter a description for the specific scheduler
Port No. This field will be displayed automatically
Use Gateway
Server
Select this radio button to (ARCON PAM – Firewall) routes you to a service through a
gateway server.
Is Active Select this radio button to enable the scheduler to start processing.

## [p205]

www.arconnet.com|Copyright © 2025 205
3.
4.
5.
•
Download/
Email Report
Select this radio button to download/ email the user discovery report.
Shared Drive: Select this radio button to share the report on a shared
drive
Email: Select this radio button to share the report via email, enter the
email address in the field provided.
Both: Select this option to receive the files through email and in shared
path.
Shared Folder path: Enter the shared folder path/ email id where the file
are to be placed/shared.
Email
Parameters
User Email
ID
Specify the email id of the user to whom the email is to be sent.
Email
Subject
Specify the subject for the email.
Email Body Specify the description for the mail.
ARCON Privilege User Discovery Windows Service will therefore start user discovery as per the
selected scheduler.
The discovered data can be viewed and exported.
The data can also be sent by email or shared path, which is to be provided while scheduling the privileged
user discovery.
4.3.5.6 Real-Time Session Monitoring
4.3.5.6.1 What is Real-Time Session Monitoring?
Administrative users require privileged account access in their day-to-day roles to maintain systems, perform
upgrades, and troubleshoot issues. However, these users can also misuse their privileges to gain unauthorized
access to sensitive information or cause damage to the IT environment. To deter the misuse of privileges by
authorized users, as well as detect malicious activity, organizations should proactively record and monitor all
privileged session activity.
Real-Time Session Monitoring monitors the live feed of a session. ARCON|PAM Real Time Session Monitoring
feature enables monitoring, suspending, and terminating activities. You can quickly freeze, unfreeze or log out
of the session to minimize any potential damage. It increases the control over the user's activity.
0Pre-requisites for RTSM configuring in different VLAN
Ports to be opened- They belong in the range of 12000-13000 which are unidirectional.
The Administrator having Real Time Session Monitoring  privilege will be able to monitor real-time
sessions.

## [p206]

www.arconnet.com|Copyright © 2025 206
• Communication
Source: End Machine of ADMIN who wants to see the session
Destination: Target Machine of the PAM user who is initiating the session
To monitor real-time sessions:
To monitor real-time sessions, use the following path:
Tools → Real Time Session Monitoring
By default, you can view all the live sessions in the grid. If you want to view live session of a particular
user, then enter the User ID or Service IP Address and click View Live Session to view the live session
of a particular user.

## [p207]

www.arconnet.com|Copyright © 2025 207
1.
2.
Right-click on the session and choose the View Live Session option.
Click the View Live Session option. The live session screen is displayed.

## [p208]

www.arconnet.com|Copyright © 2025 208
•
•
4.3.5.7 Import
What is Import Utility?
Import Utility allows bulk import of users and services into ARCON PAM database. ARCON PAM provides
templates for defining data related to users and services for uploading through Import Utility. Import Utility
reads data from the .txt file and imports it into ARCON PAM.
The Import Utility provides following options:
Import Server Connections
Update Server Connections
•
•
•
The Administrator has the privilege to Freeze, Unfreeze, or log out of the session.
Freeze Session: It allows to freeze of the session being used by the user.
The User shall specify the reason while freezing any session.
Unfreeze Session: It allows to unfreeze the frozen session being used by the user.
Logout Session: It allows to log out of the session being used by the user.
The User shall specify the reason while logging out of any session.
The Administrator having Import privilege in Server's Privilege will only be able to import Users and
Services in ARCON PAM database.

## [p209]

www.arconnet.com|Copyright © 2025 209
•
•
•
•
•
•
•
1.
2.
3.
Import Windows Services
Change DMZ Gateway
Import Users
User Server Mapping
Import User Groups
Import Service Groups
Import User Group Server Group
The following path is used to import users and services:
Tools → Import
4.3.5.7.1 Update Server Connections
4.3.5.7.1.1 What is Update Server Connections?
Update Server Connections  is used to update the details of existing services configured in ARCON PAM. It
allows modification of attributes such as Username, IP Address, Hostname, Domain Name, Service Type, and
Description. The changes made are reflected under the Manage Services screen.
A predefined MS Excel template for gathering data is provided.
The process for Updating Services is as follows:
The sheet Update_Server_Connections is used for Updating Services.
Enter Original Service details under Service Type_ORI, IP Address_ORI / Host Name_ORI, and User
Name_ORI  columns. Using these parameters, the service is recognized by ARCON PAM.
<DNC> tag stands for “Do Not Change”. Enter revised details only under those columns in which the
respective parameters of the service need to be changed. For columns where there no change is
required enter <DNC> tag. The cells with <DNC> tag will not change the value of the respective
parameters of the service.
Description of column headers are as follows:
Field Name Description
*Service Type_ORI Enter Service Type ID referring to Masters sheet.
*IP Address_ORI / Host
Name_ORI
Enter original IP Address / HostName of service to be updated.

## [p210]

www.arconnet.com|Copyright © 2025 210
4.
5.
6.
Field Name Description
*User Name_ORI Enter original User Name of service to be updated.
Domain Name_ORI Enter Original Domain Name details in this field or keep it blank. This is
optional field.
Instance_ORI Enter Original Instance details in this field or keep it blank. This is
optional field.
Host Name Enter new Host Name for Service or enter <DNC> in this field.
IP Address Enter new IP Address for Service or enter <DNC> in this field.
Domain Name Enter new Domain Name for Service or enter <DNC> in this field.
Service Type Enter Service Type for Service or enter <DNC> in this field.
Service Options Enter Service Options (True or False) for Service or enter <DNC> in this
field.
Instance Enter new Instance for Service or enter <DNC> in this field.
Port No Enter new Port no. for Service or enter <DNC> in this field.
User Name Enter new User Name for Service or enter <DNC> in this field.
Password Enter new Password for Service or enter <DNC> in this field.
Valid Till Date Enter new Valid Till Date for Service or enter <DNC> in this field.
Description 1 Enter new Description 1 (OS Version) for Service or enter <DNC> in this
field.
Description 2 Enter new Description 2 (Server Description) for Service or enter
<DNC> in this field.
Description 3 Enter new Description 3 (Location of Server) for Service or enter
<DNC> in this field.
Parameter Enter Tags for Service or enter <DNC> in this field.
The details entered in the Template should not contain space or special characters.
Copy the details from Master Sheet to Notepad and save it to .txt format.
The text file is then used to import the desired data into ARCON PAM.
Import Text file into ARCON PAM follow below steps:

## [p211]

www.arconnet.com|Copyright © 2025 211
1.
2.
3.
4.
5.
Login to Server Manager → Tools → Import → Select Update Server Connections tab → Click Browse
→ Select the location of the .txt file.
Click the Read File button. A window pops up with the following message:
Read File Process Completed
Click OK. The details are displayed in the grid.
Click the Validate button to validate whether the imported service exists in ARCON PAM or not. A
window pops up with the following message:
Validation Process Completed.
Click the OK button. The status is updated to Validated.

## [p212]

www.arconnet.com|Copyright © 2025 212
6.
7.
Click the Import button. A window pops up with the following message:
Import To Database Process Completed.
Click OK. The status is updated to Update Success.

## [p213]

www.arconnet.com|Copyright © 2025 213
8.
1.
The updated service will be displayed on the Manage Services screen.
4.3.5.7.2 Import Server Connections
4.3.5.7.2.1 What is Import Server Connections?
The Import Server Connections  tab is used to import new services  into ARCON PAM. Once imported and
assigned to the required Line of Business (LOB), these services appear under the Manage Services section in
Server Manager.Process for Importing Users :
Login to Server Manager → Tools → Import →Import Server connection tab is opened.
If toggle value for Bulk Update Server Password in Settings is Enabled, then you can update the
password of Services whereas if the value is Disabled, then you cannot update the password of
Services.  Bulk update excel supports across LOBs using bulk Import Utility in a single excel upload.

## [p214]

www.arconnet.com|Copyright © 2025 214
2.
a.
b.
c.
d.
e.
3.
4.
5.
Now, the data should be imported in the .txt format in the following manner.
Click Download Template Button.
The Admin user has to enter the desired data into a predefined Excel template.
The data entered in the Excel template should be left-aligned.
The data from the Excel template is copied to the text file.
The text file is then used to import the desired data into ARCON PAM.
Select the Browse tab →  browse for the .txt file →  click the Read File button. This will read all the
service details from the .txt file and is displayed in the grid.
Verify the details and click the Import button. The service is imported into the ARCON PAM database.
Check the status in the first column, it shows Import Success.

## [p215]

www.arconnet.com|Copyright © 2025 215
6.
Map the imported services to a particular LOB and you will view the services under the Manage
Services tab.
4.3.5.7.3 Import Windows Services
4.3.5.7.3.1 What is Import Windows Services?
Import Windows Services  allows bulk import of multiple Windows Services that are dependent on specific
privileged accounts and are integrated into ARCON PAM. This utility eliminates the need to manually add each
Windows Service individually under the Windows Connection Password Dependency  section, streamlining
the setup process.
A predefined MS Excel template for gathering data is provided.
•
•
Once a service is successfully imported, you need to then map the service to a particular LOB. In some
cases, wherein an Administrator having Settings privileges has configured the value for the LOB Wise
Service Management - Is Enabled option, where
LOB Wise Service Management - Is Enabled toggle value is Enabled, then it states that when a
service is imported, it will directly map the service to the selected LOB from the Select LOB/
Profile drop-down list, once it is imported.
LOB Wise Service Management - Is Enabled toggle value is  Disabled, then it states that the
service imported needs to be mapped to a particular LOB in LOB/Profile Master & Manager.
By default, the value is Disabled.

## [p216]

www.arconnet.com|Copyright © 2025 216
1.
2.
3.
The description of column headers are as follows:
Field Name Description
IP Address Enter the IP Address of the Existing Service.
Username Enter the Username of the Existing Service.
Windows Service Name Enter Windows Service Name.
Process for Importing Windows Service are as follows:
For Windows Service Name, login to the Server where the service is installed.
Go to “Services.msc”. Select the service, right-click on select Properties.
Enter the Service Name displayed in properties under the WindowsServiceName column in Template.

## [p217]

www.arconnet.com|Copyright © 2025 217
4.
5.
6.
The details entered in the Template should not contain space or special characters.
Copy the details from Master Sheet to Notepad and save the file to .txt format.
The text file is then used to import the desired data into ARCON PAM.
Follow below steps to Import Text File into ARCON PAM:

## [p218]

www.arconnet.com|Copyright © 2025 218
1.
2.
3.
Login to Server Manager → Tools → Import → Select Import Windows Services tab → Click Browse →
Select the location of .txt file.
Click Read File button. A window pops up with the following message:
Read File Process Completed
Click OK. The details are displayed in the grid.

## [p219]

www.arconnet.com|Copyright © 2025 219
4.
5.
6.
Click the Import button. A window pops up with the following message:
Import To Database Process Completed
Click OK. The status is updated to Import Success.
The imported service will be displayed for the entered IP Address in the Windows Connection
Password Dependency screen in the Manage menu.

## [p220]

www.arconnet.com|Copyright © 2025 220
4.3.5.7.4 Change DMZ Gateway
What is Change DMZ Gateway ?
Secure Gateway Server (SGS) acts as a PAM Firewall, as any connection initiated by end-user through PAM is
routed through SGS. ARCON|PAM Secured Gateway Server (SGS) runs proprietary components to securely
manage all traffic directly from a user machine to the target devices. Native clients can be used for multiple
active sessions for all Unix/Linux target systems. If any server is isolated in a separate network zone such as
DMZ server, which is not reachable through SGS configured for a specific LOB in ARCON PAM then the
‘Change DMZ Gateway’ option provides a way to take an exception or change SGS for these isolated servers
from where the communication is enabled for connecting to it. To configure multiple such SGS for multiple
isolated servers integrated in ARCON PAM in bulk, Change DMZ Gateway is used.
A predefined MS-Excel template for gathering data is provided.

## [p221]

www.arconnet.com|Copyright © 2025 221
1.
2.
3.
1.
The description of column headers are as follows:
Field Name Description
Service Type Enter Service Type ID of service referring Master Sheet
Server IP Address Enter Server IP Address of service to be added in DMZ zone
Process to configure SGS for multiple Servers are as follows:
The details entered in the template should not contain space or special characters.
Copy the details from Master Sheet to notepad and save it to .txt format.
The text file is then used to import the desired data into ARCON PAM.
Import Text file into ARCON PAM:
Login to Server Manager → Tools → Import →  Select Change DMZ Gateway  tab →  Click Browse →
Select the location of .txt file.

## [p222]

www.arconnet.com|Copyright © 2025 222
2.
3.
4.
Select DMZ Server from Use DMZ Gateway dropdown.
Click Read File button. A window pops up with the following message:
Read File Process Completed
Click OK. The details are displayed in the grid.

## [p223]

www.arconnet.com|Copyright © 2025 223
5.
6.
1.
2.
Click Import button. A window pops up with the following message:
Import to Database Process Completed
Click OK. The status is updated to Import Success.
To view the configured DMZ Gateway:
Login to Server Manager → Manage → Users and Services → Manage Services
Select the service for which DMZ Gateway was changed. Right-click and choose Modify Service
Parameters option.

## [p224]

www.arconnet.com|Copyright © 2025 224
3. The selected DMZ Gateway will be displayed in Use DMZ Gateway drop-down list.
4.3.6 Workflow Management
4.3.6.1 What is workflow Management ?
The Workflow Management feature in ARCON | PAM provides a centralized mechanism to track and manage
various user-initiated requests and approval workflows. Through the Workflow Tracker, administrators can
monitor detailed logs of activities such as service access requests, service password requests, and ticket-based
requests. This functionality ensures end-to-end visibility and accountability in the approval process, helping
maintain control and auditability over privileged access workflows.
Why is it important?
Effective workflow management is critical to maintaining secure and compliant privileged access in an
enterprise environment. By tracking user-initiated requests—such as service access, password retrieval, and
ticket approvals—ARCON | PAM ensures that every privileged action is authorized, documented, and
auditable. This reduces the risk of unauthorized access, supports regulatory compliance, and strengthens
overall IT governance by enforcing approval hierarchies and monitoring user activity throughout the workflow
lifecycle.
4.3.6.2 Workflow Logs
4.3.6.2.1 What:
The Workflow Logs  section in ARCON | PAM's Workflow Tracker provides detailed records of transactions
related to privileged access workflows. It captures logs for activities such as user creation, service creation,
service access requests, ticket submissions, and service password requests. Additionally, it displays the
complete approval trail for each request. Access to these logs is restricted to administrators who have been
assigned the Workflow Tracker privilege under Server Privileges. The section includes distinct logs for
different workflows, offering a granular view of each transaction type.

## [p225]

www.arconnet.com|Copyright © 2025 225
•
•
•
•
•
Workflow log types include:
Workflow Tracker
User Service Request Workflow Tracker
Service Password Request Workflow Tracker
Ticket Request Workflow Tracker
Critical Command Workflow Tracker
4.3.6.2.2 Why is it important?
Workflow logs serve as an essential audit mechanism within ARCON | PAM, offering complete visibility into
privileged access workflows and approval hierarchies. They help administrators trace actions, verify
compliance with internal policies, and investigate anomalies or unauthorized activities. By maintaining a
comprehensive record of user requests and associated approvals, Workflow Logs support accountability,
enforce access governance, and facilitate security audits across critical infrastructure environments.
4.3.6.2.3 View Workflow Approval Matrix Logs
What is View Workflow Approval Matrix Logs ?
The View Workflow Approval Matrix Logs section in ARCOS Workflow Tracker provides a detailed overview
of approval matrices associated with various transactions, such as user and service creation. This section
displays critical data including the workflow ID, object type, operation type, configured approval levels,
approval status, last approved level, name of the requester, and the request initiation timestamp. It helps
monitor and audit multi-level approval workflows configured in ARCON | PAM.
To view logs of workflow use the following path:
Manager → Server Manager →Manage → Workflow Tracker
Users can view the logs generated in the Workflow Tracker, as shown in the screen below.
The Administrator having ARCON PAM Workflow Tracker privilege under the Server's Privileges
shall only be able to view workflow approval matrix logs, user service request workflow logs, ticket
request workflow logs, and service password request workflow logs.
•
•
If the value for LOB Wise Workflow Tracker – Is Enabled in Settings is set to:
Disabled: The Service Access Request, Ticket Request, and Service Password Request logs are
filtered based on the selected LOB from the LOB/Profile dropdown list.
Enabled: The Service Access Request, Ticket Request, and Service Password Request logs are
filtered for all the LOBs. By default, the value is set to All in the LOB/Profile dropdown list.

## [p226]

www.arconnet.com|Copyright © 2025 226
Refer to the table below for detailed information
Field Description
Workflow ID Unique identifier assigned to each workflow transaction
Object Type Type of object involved in the workflow
Operation Type Type of operation performed (e.g., Create, Modify, Delete)
Approval Levels Number of approval stages configured in the workflow
Approval Status Current status of the workflow approval (e.g., Pending, Approved, Rejected)
Last Approved Level Most recent level of the workflow that received approval
Requester Name Name of the user who initiated the workflow request
Request Initiation Time Date and time when the workflow request was initiated
4.3.6.2.4 View User Service Request Workflow Logs
What is View User Service Request Workflow Logs ?
The View User Service Request Workflow Logs  section allows you to view detailed logs of user service
requests raised within ARCON | PAM. This feature provides a comprehensive overview of the service requests,
including key details such as the Line of Business (LOB), User ID, IP address, request description, type of access
requested, and the specific service involved. It enables filtering of logs based on selected criteria, allowing you
to access relevant information quickly and efficiently..
To view logs of User service request workflow use the following path:
Manager  → Server Manager  → Manage → Workflow Tracker → User Service Request Workflow Tracker

## [p227]

www.arconnet.com|Copyright © 2025 227
1.
To View the User service request workflow details follow below Steps
Enter the required fields in the filter section.
Refer to the table below for detailed information about the filter options.
Field Name Description
From Select the start date to filter logs.
To Select the end date to filter logs.
LOB/ Profile Select the LOB.
User ID Specify the User ID, to filter the logs based on the particular User ID.

## [p228]

www.arconnet.com|Copyright © 2025 228
2.
Field Name Description
IP Address Specify the IP address.
Click View the details of the user service requests raised by users are displayed in the grid.
4.3.6.2.5 View Service Password Request Workflow Logs
What is View Service Password Request Workflow Logs ?
The View Service Password Request Workflow Logs section enables users to access detailed logs of service
password requests raised by users. This feature allows filtering based on selected criteria such as Line of
Business (LOB), User ID, and IP address. The logs provide comprehensive information, including the name of
the LOB, User ID, request details, service type, IP address, username, database instance, and password access
details. Additional data such as approval levels, approvers, password open duration, and final approval status
are also displayed, offering full visibility into the password request workflow.
To view logs of service password request workflow use the following path:
Manager →  Server Manager →  Manage →  Workflow Tracker →  Service Password Request Workflow
Tracker

## [p229]

www.arconnet.com|Copyright © 2025 229
1.
To View the View Service Password Request Workflow Logs follow below Steps
Enter the required fields in the filter section.
Refer to the table below for detailed information about the filter options.
Field Name Description
From Select the start date to filter logs.
To Select the end date to filter logs.
LOB/ Profile Select the LOB
User ID Specify the User ID, to filter the logs based on the particular User ID.
IP Address Specify the IP address.

## [p230]

www.arconnet.com|Copyright © 2025 230
2. Click View the details of the service password requests raised by Users are displayed in the grid.
4.3.6.2.6 View Ticket Request Workflow Logs
What is View Ticket Request Workflow Logs ?
The View Ticket Request Workflow Logs  section provides visibility into the ticket requests raised by users
within ARCON | PAM. Users can filter the logs based on Line of Business (LOB) and User ID to narrow down the
results. The logs display essential information such as the LOB name, ticket ID, ticket number, ticket type,
activity type, associated server group, server domain name, and server port number, enabling efficient tracking
and auditing of ticket-based workflows.To view logs of ticket request workflow:
To view logs of ticket request workflow use the following path:
Manager → Server Manager → Manage → Workflow Tracker → Ticket Request Workflow Tracker

## [p231]

www.arconnet.com|Copyright © 2025 231
1.
2.
To View the Ticket Request Workflow Tracker follow below Steps
Enter the required fields in the filter section.
Refer to the table below for detailed information about the filter options.
Field Name Description
From Select the start date to filter logs.
To Select the end date to filter logs.
LOB/ Profile Select the LOB.
User ID Specify the User ID, to filter the logs based on the particular user ID.
Click View the details of the user service requests raised by users are displayed in the grid.

## [p232]

www.arconnet.com|Copyright © 2025 232
4.3.6.2.7 View Critical Command Workflow Logs
What is View Critical Command Request Workflow Logs ?
The View Critical Command Request Workflow Logs  section displays detailed records of critical command
execution requests raised by users. The logs can be filtered based on a specified date range (From date and To
date) to narrow down search results. Key information includes the requester's name, request timestamp,
command details, session ID, approver’s name and comments, current and final request status, approval
timestamp, current approval level, and the total number of configured approvals. This section helps track and
audit the usage of sensitive commands within ARCON | PAM.
To view logs of ticket request workflow use the following path:
Manager → Server Manager → Manage → Workflow Tracker → Critical Command Workflow Tracker

## [p233]

www.arconnet.com|Copyright © 2025 233
1.
2.
To View the Critical Command Workflow Tracker follow below Steps:
Enter the required fields in the filter section.
Refer to the table below for detailed information about the filter options.
Field Name Description
From Select the start date to filter logs.
To Select the end date to filter logs.
Click View the details of the user service requests raised by users are displayed in the grid.
4.3.7 Settings
What is Settings?
Settings is a prebuilt system with standard specifications that mainly consists of preset configurations. In
ARCON PAM, the Settings feature gives administrators control over the security functions and behavior of the
application, allowing them to customize it according to their specific security requirements and preferences.
This module, previously part of the server manager, has now been independently moved to the web interface. It
also supports a multilingual feature that displays settings in various languages including French, German,
Arabic, Spanish, Japanese, and Korean.
Why is Settings Important?
Settings enables administrators to tailor the ARCON PAM application to meet organizational security
standards and operational preferences. By providing centralized and flexible control over application behavior.

## [p234]

www.arconnet.com|Copyright © 2025 234
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
To Navigate to Settings use the following path:
Manager → Settings
ARCON PAM Settings help you to know about the configurations in detail. This section includes the following
configuration topics:
LOB
Group
User
Service
Password
Alerts and Notification
Workflow
Session
Domain
Ticket
Log
Network/Connection
API
General
My Vault
Cloud
Configure
4.3.7.1 LOB(s)
What are LOBs?
Companies can standardize processes and procedures for a particular LOB (line of business) across all areas
where the organization operates by using LOB-wise configuration. The admin user can perform the
configuration of LOB. This section provides a configuration that can be applied at the LOB level. The purpose of
creating LOBs is to facilitate focused decision-making, improve operational efficiency and performance, and
enable more effective management.
4.3.7.1.1 Gateway Configurations
4.3.7.1.1.1 Gateway Servers Details
Gateway Servers are Secure Gateway Servers (SGS) for the ARCON applications. If the Gateway Server is
configured in the ARCON application, the connection is invoked from the User’s workstation to SGS and then
from SGS to the target server/devices for SSO or password change on the target device. If the Gateway server
is not configured, then the connection is established directly from the User's machine to the Target Device. The
connection from the User workstation to the secured gateway server is established through an AES 256-bit
with an encrypted tunnel on a secured port, making the connection secure.
To change the language of Settings select the User Profile icon and select the language.

## [p235]

www.arconnet.com|Copyright © 2025 235
1.
2.
3.
To navigate, use the following path:
Settings > LOB > Gateway Configurations > Gateway Server Details
Go to the Gateway Server Details screen:
For adding a new Gateway server select the Add button:
Click Save after adding the details:
The Administrator having Gateway Server privileges in the Server’s Privileges will only be able to
configure the Gateway server.

## [p236]

www.arconnet.com|Copyright © 2025 236
4.
•
•
•

The Gateway Server screen contains the following fields:
Field Name Description
IP Address Enter the IP address of the Gateway Server.
Port No Enter the port number.
User Name Enter the user name of the Gateway Server.
Password Enter the password of the Gateway Server
Gateway Key Enter key for identification of service. The default value is ARCOS.
Use Gateway For Database In the ARCON application, the session recording is sent from the user’s
workstation to the database in the following three ways:
Directly to Database (PVSL - Password Vault Session Logging)
on a set port
Via Application Server to PVSL using port 443
Via Secure Gateway Server (SGS) to PVSL using port 22 – for
enabling this ‘Use Gateway for Database’ is checked.
Enabled  Enable the configuration.
It is enabled when the database is on the other side of the
Firewall and is accessed from a local machine that is inside the
boundary of the firewall.
The status is active for Gateway Server once enabled. If
disabled the server will not be used in the LOB to which it is
mapped.

## [p237]

www.arconnet.com|Copyright © 2025 237
5.
6.
1.
2.
The export button will export all the Gateway server details in the form .xlsx format. The Copy button
will copy all the details of the table.
To delete any record, click Delete or right-click on any record and click Delete:
To add Virtual IP in the Gateway servers, perform these steps below:
Right-click on the required Gateway server from the grid and select Set Gateway Servers - Virtual IP's:
The Gateway Servers - Virtual IP's screen displayed:

## [p238]

www.arconnet.com|Copyright © 2025 238
The Gateway Server screen contains the following fields:
Field Name Description
Remote IP Specify the remote IP address

Server IP Specify the server IP address
Server Port Specify the server port number
Enabled Select the checkbox to enable virtual IP for the Gateway server
4.3.7.1.1.2 Gateway Assign Details
The user can configure the Gateway server to the LOB and because of that all the servers which are part of that
particular LOB will be connected/routed via this Gateway server. The user can configure only a single Gateway
server to the particular LOB. If the administrator user configures the already assigned Gateway server to a new
LOB then the pop-up screen will be displayed with the error message. The Gateway server can be removed
from the LOB to assign it to another LOB.
This section helps you to map different LOBs to a particular Gateway Server.
This field also allows you to add text
The Administrator having LOB / Profile Default Configuration privilege in the Server’s Privileges will
only be able to do configurations under LOB / Profile Default  Configuration.

## [p239]

www.arconnet.com|Copyright © 2025 239
1.
2.
3.
4.
5.
6.
Proceed with the following steps to configure:
Navigate to, Settings > LOB > Gateway Configurations > Gateway Assign Details and select LOB profile
from the dropdown field:
Select the LOB from the LOB/Profile  drop-down and the VPN server from the Gateway Server  drop-
down list.
Click Assign. A window pops up with the following message:
Gateway Server Assigned To LOB/ Profile
Click OK. Now the LOB is mapped to the particular VPN Server.
To remove the gateway server from LOB, select the desired row and click Remove Gateway server from
LOB Profile. Also, you can right-click on the row and select Remove Gateway server from LOB Profile:
Users can click Export to export all the gateway(s) details in the .xlsx format or click the Copy button to
copy the details:

## [p240]

www.arconnet.com|Copyright © 2025 240
1.
4.3.7.1.2 Web Gateway Configurations
What are Web Gateway Servers?
Web Gateway Servers are used for brokering access to securely access web applications from ARCON PAM. If
the Web Gateway Server is configured in the ARCON application, the connection is invoked from the User’s
workstation and then from the Web Gateway to the Web application. If the Web Gateway server is not
configured, the connection is established directly from the User's machine to the target web application. The
connection from the User workstation to the secured web gateway server is established through an encrypted
tunnel on a secured port, making the connection secure.
To navigate, use the following path:
Settings > LOB > Gateway Configurations > Web Gateway Configuration
Go to the Web Gateway Configuration screen:
Only the Administrator with Web Gateway Server privileges in the Server’s Privileges can configure
the Web Gateway server.

## [p241]

www.arconnet.com|Copyright © 2025 241
2.
3.
For adding a new Web Gateway server select the Add button:
Click Save after adding the details:
The Add/Edit screen contains the following fields:
Field Name Description
IP Address Enter the IP address of the Web Gateway Server.
Port No Enter the port number.
Lob/Profile Enter the LOB name of the Web Gateway Server.

## [p242]

www.arconnet.com|Copyright © 2025 242
4.
5.
6.
Field Name Description
Enabled  Enable the configuration.
The export button will export all the Web Gateway server details in the form .xlsx format. The Copy
button will copy all the details of the table:
To delete any record, click Delete or right-click on any record and click Delete:
Click Edit to edit the record:
Once enabled, the Web Gateway Server's status is active. If
disabled, the server will not be used in the LOB to which it is
mapped.

## [p243]

www.arconnet.com|Copyright © 2025 243
4.3.7.1.3 Service Configuration
What is Service Configuration?
Service configuration in the ARCON PAM program refers to the process of customizing different settings and
parameters of services to ensure their security and optimal performance. A variety of settings, including access
control policies, authentication and authorization procedures, encryption protocols, logging, and other
security-related factors are included in the service configuration.
Service configuration is essential to protecting it from different cyber risks such as malware assaults, illegal
access, data leaks, and other security issues. It assists in making sure that the service runs safely and effectively
and that the system is set up to guard against, recognize, and address security threats.
To navigate, use the following path:
Settings > LOB > Service Configuration
The Service Configuration screen contains the following fields:
Field Name Description
LOB - Share All Users This configuration enables/disables the sharing of users between
LOBs.
Remove From User Group If User
Removed From LOB/Profile - Is
Enabled
This configuration enables/disables the removal of User Group
Mapping if the User is removed from LOB.
Disable If the Toggle value is 'Disabled', and the user is removed from LOB
then User Group mapping for that particular LOB will be retained.
Enable If the Toggle value is 'Enabled', and the user is removed from LOB
then User Group mapping for that particular LOB will be removed.

## [p244]

www.arconnet.com|Copyright © 2025 244
Field Name Description
Remove Service Mapping If User
Removed From LOB/Profile - Is
Enabled
This configuration enables/disables the removal of Service Mapping
if the User is removed from LOB.
Disable If the Toggle value is 'Disabled', and the user is removed from LOB
then service mapping for that LOB will be retained from the
backend.
Enable If the Toggle value is 'Enabled', and the user is removed from LOB
then service mapping for that particular LOB will be removed.
Send alert to User (Hours) before
Service access time expires
This configuration sends an email notification to the User prior to
the number of hours set here stating that his time-based or one-time
service access is going to expire.
Valid Values The range is from 0-100 hours.
By default value is 0. If '0' is set then no email will be sent.
Configure Shift start time for
monitoring Services
This Configuration sets the start time value. It means any service
that is critically high and is accessed before this time will be
captured in the Service Access Off Production Hrs Report in ACMO.
Valid Values Enter the start time and date.
Configure Shift end time for
monitoring Services
This Configuration sets the end-time value. It means any service that
is critically high and is accessed after this time will be captured in the
Service Access Off Production Hrs Report in ACMO.
Valid Values Enter the end time and date.
Auto Revoking of User-Service
Mapping if not accessed for days
This configuration revokes the user's services based on the number
of days configured in this configuration.
Valid Values Enter the number of days after which the service will be revoked.
Auto Revoking of User-Service
Mapping if not accessed for days (Lob-
wise)
This configuration revokes the services of the user LOB Wise.
Disable If the Toggle value is 'Disabled', then the  number of days cannot be
configured under LOB Wise Global configuration

## [p245]

www.arconnet.com|Copyright © 2025 245
Field Name Description
Enable If the Toggle value is 'Enabled', configure the number of days of Auto
Revoking of User-Service Mapping LOB Wise under LOB Wise
Global configuration.
Its value ranges from 0-999.
Allow Service Access Request For All
Services In LOB
This configuration enables/disables the users to raise service access
requests for all the services available in a particular LOB.
Disable If the Toggle value is ‘Disabled', then the users can’t raise a service
access request for all the services available in a particular LOB.
Enable If the Toggle value is 'Enabled', then the users can raise a service
access request for all the services available in a particular LOB.
4.3.7.1.4 LOB Wise Global Configuration
What is LOB Wise Global Configuration?
LOB Wise Global Configuration helps to configure any applicable settings that will be applied to each aspect
available in that LOB. Companies can standardize processes and procedures for a certain line of business across
all areas where the organization operates by using LOB-wise global configuration. This promotes operational
uniformity, legal compliance, and adherence to the overarching business goal.
The LOB Wise Global Configuration screen helps in setting the configuration at a LOB level. The following
settings can be configured directly at the LOB level:
Field Name Description
Auto Revoke User-Service Mapping if not
accessed for days (LOB-wise)
This configuration revokes the user's services (LOB Wise) after
the number of days set here.

## [p246]

www.arconnet.com|Copyright © 2025 246
Field Name Description
Automate User and Service Mapping when
server added in ServerGroup- Is Enabled
Service that is newly added to the Service Group which is itself
mapped to a User Group will get assigned to all the Users
present in the User Groups.
Enable If the Toggle value is 'Enabled', then the Service that is newly
added to a Service Group which is itself mapped to the User
Group will get assigned to all the Users present in the User
Groups.
Disable If the Toggle value is 'Disabled', then the Service that is newly
added to a Service Group which is itself mapped to the User
Group will not get assigned to all the Users present in the User
Groups.
Automate User and Service Mapping
When user added in UserGroup - Is
Enabled
Users that are newly added to the User Groups which is itself
mapped to a Service Group will be assigned to all the Services
present in the Service Groups.
Enable If the Toggle value is 'Enabled', then the Users that are newly
added to the User Groups which is itself mapped to a Service
Group will be assigned to all the Services present in the Service
Groups.
Disable If the Toggle value is 'Disabled', then the Users that are newly
added to the User Groups which is itself mapped to a Service
Group will not be assigned to all the Services present in the
Service Groups.
Windows RDP - Allow Clipboard To All This configuration enables/disables Clipboard by default for all
the Windows RDP sessions taken through ARCON PAM.
Enable If the Toggle value is 'Enabled', then the clipboard will be
activated for all the Windows RDP sessions taken through
ARCON PAM.
Disable If the Toggle value is 'Disabled', then the clipboard will not work
for all the Windows RDP sessions taken through ARCON PAM.
4.3.7.2 Group
What are Group Settings?
Group level settings refer to a set of security parameters applied to a specific user group. These settings include
access control rules, authentication and authorization procedures, and other security measures. An admin can
define and centrally manage these settings for different user groups.
Why are Group Settings Important?
Group settings allow the enforcement of security policies tailored to each user group’s needs while maintaining

## [p247]

www.arconnet.com|Copyright © 2025 247
•
•
•
•
•
•
•
1.
consistency and compliance with enterprise security standards. This setup provides flexibility and
customization for groups with varying security requirements across the organization.
This section includes the following topics:
Apply Password Settings
Apply Command Profile
2FA
USER DOOR ACCESS
BIOMETRIC
Machine Control
ACMO
Alerts
Mapping
4.3.7.2.1 Apply Password Settings
What are Apply Password Settings?
Apply Password Settings helps you to configure the settings for passwords or can define a policy that will be
applied at the group level. You can configure the minimum or maximum age of the password and also schedule
the password change process at the group level.
To navigate, use the following path:
Settings → Group
Select Apply Password Settings.
The Administrator having LOB / Profile Default Configuration privilege in the Server’s Privileges will
only be able to do configurations under LOB / Profile Default  Configuration.

## [p248]

www.arconnet.com|Copyright © 2025 248
2. Select the LOB from the LOB/Profile dropdown list displayed in the grid.

## [p249]

www.arconnet.com|Copyright © 2025 249
3. Select the checkbox from the Service Group Name list. Select a type of service from the Service
Type list which displays the count of services.

## [p250]

www.arconnet.com|Copyright © 2025 250
4. Enable Allow to set automated change passwords for that particular service type. It will also allow you
to set the password policy and you can also set auto-discovery, criticality level, and service classification
for the password change process.
Refer to the table below to understand the fields:
Field Name Description
Allow Password
Change
To enable the password change process.
Min Password Age Select minimum days for the scheduled password change process.
By default, the Allow Password Change the checkbox is selected. If you
uncheck it, all the fields are disabled and you cannot change the password
for the selected service both manually and automatically.
Password of Service will not be changed before the defined minimum days.
Eg.: If you configure Minimum Password Age as 3; then the password
change process cannot be performed before 3 days.

## [p251]

www.arconnet.com|Copyright © 2025 251
•
•
•
•
Field Name Description
Max Password Age Select maximum days for the scheduled password change process.
Use Global Password
Policy
Select to enable the global policy configured for the password change process.
Password Policy Select the password policy.
Allow Scheduled
Password Change
Select to enable/configure the scheduled password change process.
Allow (Checkbox) Enable Allow to set automated change passwords for that particular service type
Auto Discovery To enable Auto Discovery
Critical Level Enable the Critical level and select from the dropdown to assign the critical level.
Low
Medium
High
Service Classification Enable Service Classification and select from the dropdown to assign the service
classification.
Critical
4.3.7.2.2 Apply Command Profile
What is Command Profile Settings?
Command Profile helps you to assign a command profile to the services mapped under a particular user group.
Restricting commands will disallow the user from further usage of the commands. The profile of commands is
used to restrict any process or commands for the user by the administrator to maintain a safe environment.
The password change process will be scheduled automatically depending on
the selected max password age field.
By default, Default Profile is selected. You can create your own password
policy, save it, and select it in this field.
By enabling this checkbox the password change process for the selected
service will be scheduled according to the selected min and max password
age and selected password policy or the global password policy.
If Automatically Apply Password Policy When Service is added in Server Group Configuration is
enabled, then Password Policy will be applied to Services newly mapped in Server Group whereas if it
is set to disabled, then Password Policy will not be applied to Services newly mapped in Server Group.

## [p252]

www.arconnet.com|Copyright © 2025 252
1.
2.
To navigate, use the following path: Settings > Group:
Select Apply Command Profile:
Select the LOB from the LOB/Profile dropdown list. Select the user group from the list of User Groups in
the grid:
The Administrator having LOB / Profile Default Configuration privilege in Server’s Privileges will only
be able to do configurations under LOB / Profile Default  Configuration.

## [p253]

www.arconnet.com|Copyright © 2025 253
3.
4.
The service types displayed belong to that particular user group:
Select the profile from the Command Profile dropdown list:

## [p254]

www.arconnet.com|Copyright © 2025 254
5.
6.
Select None option the as shown below, so that the existing mapping of the command profile to the
selected User Group will be removed.
Click on the Confirm Changes button:

## [p255]

www.arconnet.com|Copyright © 2025 255
7.
8.
9.
A window pops up displaying the following message:
Are you sure you want to apply LOB/profile – command Policy to selected user group(s)?
Click Yes:
Another window pops up will be displayed with the following message:
LOB/Profile – Command Policy Applied Successfully
No Of Users Affected: (Total Number)

## [p256]

www.arconnet.com|Copyright © 2025 256
1.
2.
3.
4.
4.3.7.2.3 2FA
4.3.7.2.3.1 Dual Factor IP Range
In Dual Factor IP Range, you can define the range of IP Addresses to be configured for the ‘Dual Factor type’.
Once configured, ARCON PAM will prompt for the second authentication to the End User only if the User is
from the configured IP range.
To navigate, use the following path:
Settings > Group > 2FA
Select Dual Factor IP Range under 2FA:
Select the Enable (Dual factor will be applicable only for mentioned IP addresses) checkbox. A window
pops up with the following message: Confirm Changes?
Click Yes. The fields are enabled to configure the IP range.
Select the Add button to add a new Dual Factor:
The Administrator having Dual Factor IP Range privileges in the Server’s Privileges will only be able to
configure values for Dual Factor IP Range.

## [p257]

www.arconnet.com|Copyright © 2025 257
5.
The Dual Factor IP Range screen contains the following fields:
Field Name Description
Description Enter the description for the dual-factor IP range.
From IP Enter the IP address to set the start range for dual-factor.
To IP Enter the IP address to set the end range for dual-factor.
Type Select the type of authentication.
Enabled Click to enable the configuration.
For Editing the details of the existing Dual Factor IP Range, click on the existing Dual Factor IP
Range and select the Edit button at the top and make the required changes. Also, you can right-click on
the domain and select Edit.
The user is authenticated on the login screen of Client Manager, once the dual factor IP range is
configured.

## [p258]

www.arconnet.com|Copyright © 2025 258
6.
7.
For Deleting the existing Dual Factor IP Range, click on the existing Dual Factor IP Range and select the
Delete the button at the top and make the required changes. Also, you can right-click on the domain and
select Delete.
The Export button will export all the Dual Factor IP Range details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.2.3.2 CISCO Duo MFA
To ensure strong authentication mechanisms, ARCON PAM enables users to set up a security
configuration with a multi-layered validation process. Among many integrations, ARCON integrates with
CISCO Duo Authentication as well. So once Cisco Duo Authentication is configured for users, it would be used
for that particular user during the login process to the ARCON PAM portal.
To navigate, use the following path:
Settings > Group > 2FA > Cisco Duo MFA
Field Name Description
Client ID This field displays the client ID for the particular Cisco Duo MFA.
API host of Cisco duo This field displays the host API details for the particular Cisco Duo
MFA.
Created By This field displays the administrator name who has added the
particular Cisco Duo MFA.
Created On This field displays the date and time the particular Cisco Duo MFA was
added.

## [p259]

www.arconnet.com|Copyright © 2025 259
Field Name Description
RIght-Top corner buttons Add: The Add button helps to add a new Cisco Duo MFA.
Edit: The Add button helps to edit details of an existing Cisco Duo MFA.
Delete: The Add button helps to delete an existing Cisco Duo MFA.
Export: The Add button helps to export the existing Cisco Duo MFA.
Copy: The Add button helps to copy the existing Cisco Duo MFA
details.
4.3.7.2.3.3 2FA Configurations
To navigate, use the following path:
Settings → Group → 2FA
Field Name Description
User Door Access Authentication -
Error Message
Allows to configure the Message to be displayed by ARCON PAM
when User Door Access Authentication fails.
Valid Values If the Toggle value is 'Enabled', then it enables the Restoration of the
last Password based on the password history.
Biometric Device This configuration sets which Biometric device is to be enabled for
Biometric Authentication.
Valid Values The valid values are Morpho, Precision, 3M Cogent/Gemalto,
eikonTouch, Global space
SMS OTP -  Enforce Self
Registration for all Users
This configuration will allow administrators to enable/disable SMS
OTP.
Disable If the Toggle value is 'Disabled', then SMS OTP-Enforce Self
Registration will be disabled for All Users.
Enable If the Toggle value is 'Enabled', then SMS OTP-Enforce Self
Registration will be enabled for All Users.
Mobile OTP - Enforce Self
Registration for all Users
This configuration will allow administrators to enable/disable Mobile
OTP - Enforce Self Registration.
SMS OTP -Enforce Self Registration for All Users and Mobile
OTP -Enforce Self Registration for All Users cannot be
enabled at the same time.

## [p260]

www.arconnet.com|Copyright © 2025 260
1.
2.
3.
Field Name Description
Disable If the Toggle value is 'Disabled', then Mobile OTP-Enforce Self
Registration will be disabled for All Users.
Enable If the Toggle value is 'Enabled', then Mobile OTP-Enforce Self
Registration will be enabled for All Users.
SMS OTP Mobile No Duplication
Validation - Is Enable
This configuration enables Validation for Duplicate Mobile No.
Entries on Creation/Modification of Users in Manage Users.
Disable  If the Toggle value is 'Disabled', then Validation of Duplicate Mobile
No. is disabled
Enable  If the Toggle value is 'Enabled', then  Validation of Duplicate Mobile No.
is enabled.
Unlock SSH Linux User Account and
Change Password
For locked services, 3 options have been added to the dropdown.
Do not change the locked user password (Value = 0)
Unlock the user and change the password (Value = 1)
Unlock the user, change the password, and lock the user again
(Value = 2)
Set SMS OTP (Dual Factor
Authentication) value
This configuration enforces SMS OTP as Dual Factor Authentication
for all the users currently present in ARCON PAM.
Allow Duplicate Mobile OTP
(Unique ID)
This configuration allows the duplicate Mobile OTP for the same
Unique ID for Authentication.
Enable Dual Factor on My Services This configuration enables/disables dual-factor authentication for
service access while taking the single sign-on services.
SMS OTP -Enforce Self Registration for All Users and Mobile
OTP -Enforce Self Registration for All Users cannot be
enabled at the same time.
There will be an error pop-up message as 'Mobile No. Not Valid.
It Has Been Already Used For Some Other User.' with another
pop-up as 'Error In Updating Selected User' on the addition of
duplicate entries of Mobile Number.

## [p261]

www.arconnet.com|Copyright © 2025 261
1.
Field Name Description
Enable Mobile OTP Registration on
Multiple Instances
This configuration enables/disables Mobile OTP on multiple instances
with the same user.
Disable Hardware Token - for All
User
This configuration enables/disables Hardware tokens OTP for all
users.
Disable If the Toggle value is 'Disabled', then this feature is disabled.
Enable If the Toggle value is 'Enabled', then this feature is enabled.
4.3.7.2.3.4 User Door Access
What is User Door Access Authentication?
The User Door Access Authentication mechanism is used when the user wants the application to authenticate
or check the User’s physical presence within the premise. This can be done by communicating with the Door
Access Management System to check if the User has swiped the door to check in the premise, this information
can be monitored by ARCON PAM to get the status of the user and only then allow to login into the application.
For such communication with Door Access Management, a framework is available in ARCON PAM.
To navigate, use the following path:
Settings → Group → 2FA → USER DOOR ACCESS
Select User Door Access Authentication under USER DOOR ACCESS.
If Mobile OTP is disabled in the first instance it will be disabled
in the following instances too.
The Administrator having User Door Access Authentication privileges in Server’s Privileges will only
be able to configure values for User Door Access Authentication.

## [p262]

www.arconnet.com|Copyright © 2025 262
2.
3.
Click Enable. A User Door Access Authentication window pops up with the following message.
Confirm Changes?0
Click Yes. The fields are enabled to configure user door access authentication.
The User Door Access Authentication screen displays the following fields:
Field Name Description
Service Select the service. Predefined service types are available in ARCON PAM.
To add a service in Service drop-down, right-click the service from manage
services and select add it to DMZ supported services. Only supported services
will be available in the drop-down list.
The User Door Access Authentication section has eight different parameters.
Based on the selected service, these parameters get utilized.
Example: In the Service list, select the service. Based on this, from the Service list,
a database is selected on the User Door Access Authentication screen. ARCON
PAM will now connect to the Info Bridge.

## [p263]

www.arconnet.com|Copyright © 2025 263
4.
Field Name Description
Services ARCON PAM will pass the details of the server, to the Info Bridge. Info Bridge will
fire the query provided in the Parameter field to the database selected in the
Service list and check whether User 1 has checked in or not. ARCON PAM knows
the type of database, the type of connectivity needs to be established. If there is a
web service, configure a web service parameter and it will customize the Info
Bridge accordingly so that it can connect to any type of access card system or
door access system.
URL It is an Info Bridge. This is one of the web services in the Info Bridge.
Example: One application using the Microsoft SQL database has created a view.
This is a temporary table where ARCON PAM can query data. User 1 tries to
access ARCON PAM from the office but he has not swiped his card at the main
entrance. Now, according to the swipe mechanism User 1 has not entered the
office. When User 1 tries to access ARCON PAM, it will communicate with the
Info Bridge. ARCON PAM will check whether User 1 has swiped his card in or not.
When it communicates with the Info Bridge, Info Bridge will take the details such
as server details to the database. ARCON PAM will directly query the database
whether User 1 has checked in or not. If User 1 has checked in, ARCON PAM will
allow him to log in.
Enter the details and click Confirm Changes button to configure the details.
User Door Access Configuration
To navigate, use the following path:
Settings → Group → 2FA → USER DOOR ACCESS0
Field Name Description
RADIUS Server
Connection Timeout
This configuration sets the time for Radius Server Connection Timeout.
If the user selects the default RADIUS Server Connection Timeout value to 5000,
it refers to 5 seconds/minute.
Valid Values The valid range is 1-100000.
Hardware Token-Radius Servers
What are Hardware Token-Radius Servers?
The RADIUS servers are used for the authentication of the RSA portal. RADIUS is a protocol similar to LDAP,
DCPIP, and RDP protocol. Similarly, RADIUS is a kind of protocol that helps to communicate with another
server. When you want to enable the Hardware / Software Tokens which works on the RADIUS protocol as the
second factor of authentication in ARCON PAM, then the configuration of the RADIUS server is done here.
To navigate, use the following path:
Settings → Group → 2FA → USER DOOR ACCESS0
The Administrator having Hardware Token – RADIUS Servers privilege in Server’s Privileges will only
be able to configure values for Hardware Token – Radius Servers.

## [p264]

www.arconnet.com|Copyright © 2025 264
1.
2.
Select Hardware Token – Radius Servers under USER DOOR ACCESS:
Select Add to add a new token:
Refer to the following table to understand the field-level description shown in the above screen:

## [p265]

www.arconnet.com|Copyright © 2025 265
3.
4.
5.
Field Name Description
Server Priority Select the server priority.
Radius Server Enter the radius server.
Shared Key Enter the shared key.
Server Port (UDP) Enter the server port (UDP) number.
Domain Select the Domain name.
Radius User Authentication Enable Radius User Authentication for User Authentication
Radius 2FA Enable Radius 2FA for 2FA
Domain with User Enables all the users within the domain
Enabled Enable the server in ARCON PAM.
Enter the details and click Save button to configure the radius server details.
For editing the details of the existing Hardware Token- Radius servers, click on the existing row and
select the Edit button at the top and make the required changes. Also, you can right-click on the row and
select Edit:
For deleting the existing Hardware Token- Radius servers, click on the existing row and select the
Delete button at the top and make the required changes. Also, you can right-click on the row and select
Delete.
The priority up to three servers can be configured if those
many servers are available in the environment as part of HA
(High Availability).

## [p266]

www.arconnet.com|Copyright © 2025 266
6.
1.
The Export button will export all the  Hardware Token- Radius servers details in the form .xlsx format.
The Copy button will copy all the details of the table.
4.3.7.2.3.5 Biometric
What is Biometric Setting?
Biometric Configuration is a dual-factor authentication supported by ARCON PAM. It is performed by using
the biometric data (voice/fingerprint) of the user. ARCON PAM acts as a strategic entry and identity
management system for managing several system-based users.
Voice Biometric Configuration
Voice Biometric Authentication is a type of Dual Factor Authentication that uses Web Service for
authenticating users before logging into Client Manager. The predefined web service authentication is
configured, which will authenticate the user through his voice and decide whether to allow the user to log in or
not.
To navigate, use the following path:
Settings → Group → 2FA → BIOMETRIC
Select Voice Bio Metric Configuration under BIOMETRIC:
The Administrator having Voice Biometric Authentication privileges in Server’s Privileges will only be
able to configure values for Voice Bio Metric Configuration.

## [p267]

www.arconnet.com|Copyright © 2025 267
2.
•
•
•
•
3.
4.
Check the Enable checkbox.
The fields are enabled to configure voice biometric authentication:
Field Name Description
Authentication URL It is in the predefined .xml format.
Success Flag Configure the success flag. The valid values are:
True
False
Error Flag Configure the error flag. The valid values are:
True
False
Authorization Username Authorized user name used to access the specified URL.
Authorization Password Password used to access the specified URL.
Request Timeout (in min) Select the session timeout in minutes.
Few fields are customizable according to requirements. The ARCON PAM User Tag, ARCON PAM Use
Mobile No. Tag and ARCON PAM Message Tag can be configured with user details, user mobile number
and message to be sent.
Enter the details and click Confirm Changes to configure the details.
Biometric Configurations

## [p268]

www.arconnet.com|Copyright © 2025 268
•
•
To navigate, use the following path:
Settings → Group → 2FA → BIOMETRIC
Field Name Description
Biometric – Finger Print - Mode This configuration sets mode of Finger Print in Biometric Authentication.
Valid Values The two modes are:
Desktop: In this mode, every ARCON PAM User should have an
individual bio-metric device configured to their respective
workstation, hence first the user login to the ARCON PAM portal
with their respective credentials and then the biometric
authentication is prompted.
Centralized: In this mode, the biometric device should be
configured on a centralized location and every user will be
authenticated with the centralized bio-metric device first and then
are allowed to login to ARCON PAM Portal.
Biometric – Finger Print - Mode -
Centralized Valid For (Minutes)
This configuration sets time in minutes for the validity of Finger Print in
Centralized Mode for Biometric Authentication.
Valid Values The range is from 1-480.
If the value is Zero every time the user will have to identify through the
bio-metric fingerprint.
Biometric Finger Print
Authenticator Link On ACMO
Login Page - Is Enabled
This configuration enables/disables Biometric Finger Print Authenticator
Link on CM Login Page.
Biometric-Finger Print- Minimum
Match Score (Percentage)
This configuration sets the percentage of minimum match score of Finger
Print in Biometric Authentication.
Valid Values The range is 0-100.
4.3.7.2.4 Machine Control
4.3.7.2.4.1 Network Segments
Network Segments configuration is used to pull Network Segment Wise Logon Report from Client Manager.
The range of IP Addresses is set under a Network Segment. The report will display details based on the
configuration. The Network Segment Wise Logon report displays the details of the User who has logged into
the application by any network device with the User’s IP address and desktop details.

## [p269]

www.arconnet.com|Copyright © 2025 269
1.
2.
To navigate, use the following path:
Settings → Group → Machine Control
Select Network Segments under Machine Control:
Select the Add button to add a new Network segment:
Network segment fields are described below:
Field Name Description
Description Enter the description for network segment.
From IP Enter the IP address, from where the network range starts.
To IP Enter the IP address, where the network range ends.
Enabled To enable the configuration.
The Administrator having Network Segments privileges in Server’s Privileges will only be able to
configure values for Network Segments.

## [p270]

www.arconnet.com|Copyright © 2025 270
3.
4.
5.
6.
Enter the details and click the Save button to create a new network segment.
For editing the details of the existing Network Segment, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the domain and select Edit.
For deleting the existing Network Segment, click on the existing row and select the Delete button at the
top and make the required changes. Also, you can right-click on the domain and select Delete.
The Export button will export all the Network Segment details in the form .xlsx format. The Copy button
will copy all the details of the table.
4.3.7.2.4.2 Machine Controls Global Configurations
To navigate, use the following path:
Settings → Group → Machine Control
Field Name Description
Desktop Level Access Control -
MAC/IP Filter
This configuration sets whether Desktop Level Access will block devices
from connecting to ARCON PAM or not.

## [p271]

www.arconnet.com|Copyright © 2025 271
•
•
•
Field Name Description
Valid Values The range is from 0-2
If the value is set to ‘0’, it refers to everything is allowed. It means all
the devices are allowed to connect to ARCON PAM. The menu is
not visible because no configuration is required.
If the value is set to ‘1’, it refers to Block Only value. It means the
listed workstations are blocked and rest are allowed to connect to
ARCON PAM.
If the value is set to ‘2’, it refers to Allow Defined Only. It means only
the defined Workstations are allowed to connect to ARCON PAM.
Common Temp Parent Folder
For ARCOS ActiveX
This configuration sets the name of Common Temp Parent Folder for
ActiveX.
Valid Values Set the name of Common Temp Parent Folder for ActiveX. By default value
is ‘ARCON PAM’.
Access On Hold (By Default) In
User Access Review - Is Enabled
This configuration sets whether old reviews kept on hold will be
displayed under CM > Server Manager > Reviews > User Access.
Disable If Toggle value is 'Disabled', then recently added to Hold list reviews will be
displayed under CM > Server Manager > Reviews > User Access > Access
On Hold tab.
Enable If Toggle value is 'Enabled', then old reviews kept on Hold will be displayed
under CM > Server Manager > Reviews > User Access > Access On Hold
tab.
4.3.7.2.5 ACMO
This section helps the administrator to configure a few security settings for ACMO at the group level which
means the same ACMO settings will be applicable at the group level.
To navigate, use the following path:
Settings → Group → ACMO
Field Name Description
ACMO Session Timeout
(Minutes)
This configuration sets the time in minutes which is considered to log out the
user if the ACMO session is idle for that duration.
Valid Values  The range is from 1-9999.

## [p272]

www.arconnet.com|Copyright © 2025 272
Field Name Description
Sort All Filter Data In
ACMO Connections - Is
Enabled
This configuration sets whether service details displayed in the grid view under
My Services (Client Manager > My Access > My Services) should be sorted or
not. By default, ARCON PAM only sorts by the IP address.
Disable If the Toggle value is 'Disabled', it displays data sorted by IP address.
Enable If the Toggle value is 'Enabled', under Server Manager > Settings > Service >
Security > Service Critical Command > Configure a command and tick Ask User
Confirmation (Before Execution). Execute this critical command on the server. A
confirmation message will be displayed.
ARCOS Security Token
Validation In ACMO - Is
Enabled
This configuration will enable or disable ARCON PAM Security Token Validation
in Client Manager.
Service Access All LOB - Is
Enabled
This configuration enables/disables the All LOBs option in the LOB drop-down
list in My Services (Client Manager).
Disable If the Toggle value is 'Disabled', it displays Services LOB-wise.
Enable If the Toggle value is 'Enabled', it displays the All LOBs option. Enable this
configuration to show services for a particular IP Address or Hostname from all
LOBs.
Hide ACMO My Services
Page Table Column (Case
sensitive)
This configuration hides the selected column from ACMO -> My Services.
Valid Values Select the column name: Service Type, Host Name, Host IP, Username, Domain,
Instance
ACMO Enable Agentless
Login
This configuration will enable the agentless login option in ACMO.
Domain Validation for
ACMO (WindowsOS only)
This configuration sets restrictions for accessing PAM ACMO based on their
domain and workgroup.
Valid Values Allow both Domain and Workgroup machines, Allow only Domain machines, and
Allow only domains which have been listed.

## [p273]

www.arconnet.com|Copyright © 2025 273
Field Name Description
Domain validation failed
message for ACMO
(WindowsOS only)
Set a customized message for domain validation.
For example- If my Domain validation for ACMO (WindowsOS only) is - Allow
only Domain Machines and a workgroup user tries to access it then the login is
failed, and the message set on Domain validation failed message for ACMO
(WindowsOS only) appears on the ACMO user screen.
Valid Values Enter the text message to be displayed on ACMO when the validation fails.
Dashboard-Critical
Commands Fired Daywise
This configuration will display data in ACMO→ Dashboard → Critical
Commands fired.
Disable If the Toggle value is 'Disabled', it will display 30 days records in critical
command fired.
Enable If the Toggle value is 'Enabled', it will display a 1-day record in critical command
fired.
Disable Domain Field for
Login
This configuration will disable to login field on the login page.
Disable If the Toggle value is 'Disabled', the domain field will be accessible on the login
page.
Enable If the Toggle value is 'Enabled', the domain field will be disabled on the login
page.
Multi Access This config enables the user to take multiple connections. All the services
assigned to the user can be accessed at once.
Disable If the Toggle value is ‘Disabled', the user can’t access multiple services.
Enable If the Toggle value is 'Enabled', the user can access multiple services.
Enable Multi Access
Button
This configuration will enable or disable the Multi Access Button option.
Disable If the Toggle value is ‘Disabled', the user can’t see the Enable Multi Connections
button on the ACMO screen. The user can access multiple services by clicking
each service’s Open button.
Enable If the Toggle value is ‘Enabled', the user can see the Enable Multi Connections
button on the ACMO screen and can access multiple services with one click.

## [p274]

www.arconnet.com|Copyright © 2025 274
Field Name Description
Enable Hash Value
Comparison
This configuration will enable or disable the hash value comparison.
Disable If the Toggle value is ‘Disabled', the connector shall not undertake a comparison
between the file on the local machine and the server file that the user intends to
download. In the event that a file with an identical name is present on the local
machine, the connector shall prohibit the download of the file from the server.
Enable If the Toggle value is ‘Enabled', the connector shall undertake a comparison
between the file located on the local machine and the file on the server that the
user intends to download. In the event that a file with an identical name is
present on the local machine, the user may proceed to update the file name in
order to download the file from the server.
Display My Vault APEM
button
This configuration will enable or disable the display of the Secure With Vault
APEM button on the My Vault > Service creation screen.
Disable If the Toggle value is ‘Disabled', the user can’t see the Secure With Vault APEM
button on the My Vault > Service creation screen.
Enable If the Toggle value is ‘Enabled', the user can see the Secure With Vault APEM
button on the My Vault > Service creation screen.
ACMO Custom Logout  This configuration sets the ACMO Custom Logout.
Incident Management
Admin Users
In this configuration, the administrator needs to select one or more admin users
from the dropdown who will review the raised incidents.
Password Complexity Of
API Users
This configuration is used to set the password policy for API User passwords.
Disable If the Toggle value is 'Disabled', the password policy will not be applicable for
the API user passwords.
Enable If the Toggle value is 'Enabled', the password policy will apply to the API user
passwords.
4.3.7.2.6 Alerts
What are Alerts?
Alert preferences allow administrators to configure to get notifications or alerts when a particular event takes
place. The type of alert you receive, how frequently you receive it, and how you receive it can all be customized
using these parameters, which can vary depending on the device or application.

## [p275]

www.arconnet.com|Copyright © 2025 275
•
•
•
Alert settings can be a helpful method to be updated on significant events or updates, but if they are not
correctly controlled, they can also become overpowering. In order to guarantee that you are only receiving
notifications that are important, it is crucial to routinely evaluate the alert settings and make any necessary
adjustments.
To navigate, use the following path:
Settings → Group→Alerts(?)
Field Name Description
Send Alert To All Checkers
When Maker Creates New
User
This configuration sets whether the alert will be sent to all Checkers when
Maker creates a new User.
Valid Values The range is 0-2.
If the ‘0’ value is set then the alert will not be sent to any Administrator,
but the request will be displayed in the Maker’s Checker screen of
Admins having Approve User (Checker) privilege.
If the ‘1’ value is set then the alert will be sent to Administrators having
to Receive Alert On User Creation By Maker and Approve User
(Checker) privilege.
If the ‘2’ value is set then the alert will be sent to Administrators
having Approve User (Checker) privilege.
User Dormancy Alert -
Schedule Days
This configuration sets the number of days for the alert to be sent to the User
prior to his ID being added in the Dormant User list.
Eg: If the value is configured as 4, the User will be notified 4 days before the day
his ID will be added to the Dormant User List.
Valid Values The range is from 1-5.
Dormant User Alert This configuration sets whether the alert is sent to the User that he will be added
to Dormant User list.
Disable If the Toggle value is 'Disabled', then an alert will not be sent to the User.
Enable If the Toggle value is 'Enabled', then an alert will be sent to the User.
4.3.7.2.7 MFA
What are MFA Settings?
The Dormant User Alert configuration should be enabled for this
configuration.

## [p276]

www.arconnet.com|Copyright © 2025 276
1.
2.
Multifactor authentication (MFA) enhances security by requiring users to provide two or more verification
methods before accessing an ARCON application. MFA is crucial in cybersecurity for several reasons, including
improved security, prevention of unauthorized access, reduction of fraud and data breaches, regulatory
compliance, protection against identity theft, and blocking automated attacks.
In the Settings module, the end-user can configure the MFA settings.
To navigate, use the following path:
Settings → Group → MFA
Proceed with the following steps:
Click and open the Login Security Configurations. The following screen will display:
Refer to the table below to understand the fields:
Field Name Description
PCI-DSS standards for MFA
Enabled
Enabling this toggle allows MFA to comply with PCI-DSS.
Enable AutoUnlock on Lockout This toggle will automatically unlock the lockout user profile after the
configured Lockout time.
Lockout Minutes Enter the Lockout Minutes. The lockout user will automatically be unlocked
after the configured lockout minutes.
Invalid Login Attempts
Threshold for Local Users
Enter the threshold value for Invalid Login Attempts for the local User. If
the limit is exceeded, the user will be locked out.
Invalid Login Attempts
Threshold for Domain Users
Enter the threshold value of Invalid Login Attempts for the Domain User.
The user will lock out after the limit is exceeded.
OTP Expiration Time (In
Minutes)
Configure the time in minutes for OTP expiration.
Maximum OTP Resend
Attempts Threshold
Enter the threshold value for maximum OTP resend attempts.
Click Confirm Changes to save the configuration.
4.3.7.2.8 Mapping - Settings
What are Mapping Settings?
The Mapping section helps the administrators configure a few settings at the user group and service group
level. The act of connecting a user or user group to a service or service group is referred to as mapping. Data

## [p277]

www.arconnet.com|Copyright © 2025 277
misuse or illegal access points might be found by mapping access controls and permissions. This can aid in wise
resource allocation and the prioritization of security measures.
To navigate, use the following path:
Settings > Group > Mapping
Field Name Description
Automate UserGroup And
ServerGroup Mapping (AD
OnBoarding) - Is Enabled
This configuration enables/disables the mapping of the User Group with the
Server Group once they are scanned from Active Directory. If the User Group is
mapped to the respective Server Group then only named and vault Services will
be created for the Users present in the User Group.
Disable If the Toggle value is 'Disabled', the User Group will not be mapped with the
Server Group after fetching from Active Directory.
Enable If the Toggle value is 'Enabled', the User Group will be mapped with the Server
Group once fetched from Active Directory.
Automate User and
Service Mapping When
user added in UserGroup -
Is Enabled
Whenever a new User is created, a User Group will be assigned to that
respective User. The Services of Service Groups that are mapped to the assigned
User Group will be auto-mapped to the created User.
Disable If the Toggle value is 'Disabled', the services will not be automatically mapped to
the newly created user. The administrator may need to map services with users
manually.
Enable If the Toggle value is 'Enabled', the services will be automatically mapped to the
newly created user.
Automate User and
Service Mapping when
server added in
ServerGroup- Is Enabled
Whenever a new Service is created, a Service Group will be assigned to that
respective Service. The Users of the User Groups that are mapped to the
assigned Service Group will be auto-mapped to the created Service.
Disable If the Toggle value is 'Disabled', the users will not be automatically mapped to
the newly created service. The administrator may need to map services with
users manually.
Enable If the Toggle value is 'Enabled', the users will automatically mapped to the newly
created service.
4.3.7.3 User Settings
What are User Settings?
User settings are the adaptable choices that let the administrator tailor a configuration to their unique
requirements and preferences. It's crucial to remember that improper user settings can make the system open
to assaults.

## [p278]

www.arconnet.com|Copyright © 2025 278
1.
2.
4.3.7.3.1 Mac or IP Filter
This section helps you to define or view all the IP addresses, MAC addresses, Processor IDs, and BIOS Serial IDs
which has been blocked or allowed for desktop-level access.
To navigate, use the following path:
Settings → User0
Select Mac/IP Filter:0
Select the Add button to add a new Mac/IP Filter:
•
•
The Desktop Level Access Control - MAC/IP Filter Configuration sets whether Desktop Level
Access will block devices from connecting to ARCON PAM or not.
If value 0  is configured, it refers to everything being allowed and all the devices are
allowed to connect to ARCON PAM. The MAC/IP Filter option will not be visible under
the Tools menu as no configuration is required.
If value 1 is configured, it refers to the Block Only value. It means the workstations listed
in MAC/IP Filter option will be blocked and the rest are allowed to connect to ARCON
PAM.
If value 2 is configured, it refers to Allow Defined Only. It means only the workstations
listed in MAC/IP Filter option are allowed to connect to ARCON PAM.
The Administrator having IP / MAC Filter privileges in Server’s Privileges will only be able to
configure values in IP/MAC Filter.

## [p279]

www.arconnet.com|Copyright © 2025 279
•
•
•
•
3.
4.
The Mac/IP filter screen contains the following fields:0
Field Name Description
Filter Type Select the type of filter.
The valid values are:
IP Address
MAC Address
Processor ID
BIOS Serial ID
Detail Specify the detail based on the filter type.
Enabled (checkbox) Enable the configuration.
Click Get Last 10 Days Login Details, to view the last 10 days' login details in the application.
Click on Save to save all the changes and the Mac/IP Filter has been set. A window pops up with the
following message:

## [p280]

www.arconnet.com|Copyright © 2025 280
5.
6.
7.
8.
For editing the details of the existing Mac/IP Filter, click on the existing row and select the Edit button at
the top and make the required changes.
To enable or disable the selected row, right-click on the selected row and click on the Active or Inactive
option:
For deleting the existing Mac/IP Filter, click on the existing row and select the Delete button at the top
and make the required changes.
The Export button will export all the Mac/IP Filter details in the form .xlsx format. The Copy button will
copy all the details of the table.

## [p281]

www.arconnet.com|Copyright © 2025 281
4.3.7.3.2 User Security
4.3.7.3.2.1 Configure Dormancy Period at Group Level
This section helps the administrator to configure dormancy days Lob-wise and group-wise. Users can set the
value of the dormancy period to 366 days under the section of Account Threshold Values. Previously, the
dormancy period was limited to 99 days but now it is increased the limit to 366 days (1 Year).
To navigate to login security, use the following path:
Settings→ User Security → Configure Dormancy Period at Group Level
The Configure Dormancy Period at Group Level screen contains the following fields:
Field Name Description
LOB/Profile Select LOB/Profile from the dropdown
Show Entries Select the number of entries from the dropdown
Select All Tick the check box to configure LOB-wise configuration
User Group Name Specify the name of the user group
No. of Users Count Specify the total number of users count
Dormancy Day(s) Specify the total number of dormancy days
LOB Assigned By Specify the name by whom the LOB was assigned
LOB Assigned On Specify the date when the LOB was assigned
Account Threshold Values
Dormancy Day(s) Select the dormancy days from the dropdown
Dormancy days can be set for users as per group/LOB and for other users globally applicable
dormancy days will apply where Admin can configure Dormancy days at User Group Level.

## [p282]

www.arconnet.com|Copyright © 2025 282
1.
2.
3.
Click Confirm Changes to save the configured details.
4.3.7.3.2.2 Mail Servers
Mail server is an application that are responsible for sending receiving and storage of emails.
To add any new server configuration, click on Add button as shown in the preceding screen.
Mail Server Configuration page is displayed. From this page user can configure mail server.
Enter the senders the email id in Mail From field.
SMTP Setting
The Email Configuration to send Alerts and Notifications to users is done using SMTP Configuration.
ARCON PAM provides alerts for New User Approved, New Service Created, Command executed on SSH,
Invalid Login Attempt, ARCOS Logs, Service Password Manually Changed, Process started on Windows,
Process title on Windows, and, Failed SMS OTP Authentication.

## [p283]

www.arconnet.com|Copyright © 2025 283
Refer to the below table to under stand the field and data present in SMTP Setting:
Field Name Description
User Name Enter the username for the mail ID mentioned in Mail From field
(if applicable as per SMTP Configuration).
SMTP Server Enter server DNS / IP of SMTP server.
Password Enter the password for the mail ID mentioned in Mail From (if
applicable as per SMTP Configuration).
Security Select the security of SMTP server.
SMTP Method Methods are used for auth supported by mail server.
Smtp port Enter port number of SMTP server.
Certificate Enter/Select the certificate details.
Timeout(s) Duration of receiving mail in milliseconds.
Sign Message Select to send the message digitally signed, to verify the identity
as the sender.
Encrypt Message Select to send message in encrypted format.
Proxy Settings

## [p284]

www.arconnet.com|Copyright © 2025 284
Field Name Description
Proxy Type Select the type of proxy server.
User Name Enter the username of proxy server.
Proxy Port Enter the port number of proxy server.
Password Enter the password of proxy server.
Proxy Server Enter the proxy server details.
Method Select the method based on the selected type in the Proxy
Type field.
Domain Enter the domain of proxy server.
IMAP Setting
If IMAP Settings are enabled, the approvers can reply to the mail received on raising a request by the user.
Refer to the below table to under stand the field and data present in IMAP Setting:
Field Name Description
User Name (Email) Enter the username for the mail ID mentioned in Mail From
field.
IMAP Server URL Enter the email of IMAP server.
Password Enter the password for the mail ID mentioned in Mail From.
Port Enter port number of IMAP server.
Proxy Settings
Proxy Type Select the type of proxy server.

## [p285]

www.arconnet.com|Copyright © 2025 285
Field Name Description
User Name Enter the username of proxy server.
Proxy Port Enter the port number of proxy server.
Password Enter the password of proxy server.
Proxy Server Enter the proxy server details.
Method Select the method based on the selected type in the Proxy
Type field.
Domain Enter the domain of proxy server.
EWS Setting
exchange web services is an API that allows users to manage emails.
Refer to the below table to under stand the field and data present in EWS Setting
Field Name Description
User Name (Email) Enter the username for the mail ID mentioned in Mail From
EWS Server URL Enter the URL of EWS Server.
Password Enter the password for the mail ID mentioned in Mail From
Port Enter port number of EWS server.
Proxy Settings
Proxy Type Select the type of proxy server from the dropdown
User Name Enter the username of proxy server.

## [p286]

www.arconnet.com|Copyright © 2025 286
Field Name Description
Proxy Port Enter the port number of proxy server.
Password Enter the password of proxy server.
Proxy Server Enter the proxy server details.
Method Select the method based on the selected type in the Proxy
Type field.
Domain Enter the domain of proxy server.
O 365 Settings
Through hosted Exchange Server versions, Office 365 offers service plans that offer email and social
networking services to the users.
Refer to the below table to understand the field and data present in O 365 Setting:
Field Name Description
Client Secret A password or a public/private key pair that your app uses to
authenticate with the Microsoft identity platform.
Client ID The directory tenant that you want to request permission
from. The value can be in GUID or a friendly name format. If
you don't know which tenant the user belongs to and you want
to let them sign in with any tenant, use common.
Tenant ID The application ID that the Azure app registration
portal assigned when you registered your app.
MS Teams
MS Teams configuration is used to integrate with PAM to Hook the web URL with it.
Select the details and click Confirm Changes button. The Clear All Configuration button allows to reset the
details i.e. clear the data from the fields

## [p287]

www.arconnet.com|Copyright © 2025 287
For Editing the details of the existing mail server, click on the existing row and select the Edit button at the top
and make the required changes. Also, you can right-click on the row and select Edit.
For Deleting the existing mail server, click on the existing row and select the Delete button at the top and make
the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the mail servers details in the form .xlsx format. The Copy button will copy all
the details of the table.
Assigned Mail Server(s)
In this configuration, the administrator can assign the configured mail servers to a particular LOB. To do the
same, follow the below steps:

## [p288]

www.arconnet.com|Copyright © 2025 288
1.
2.
3.
4.
5.
6.
Follow the path: Settings > User > User Security > Assigned Mail Server(s)
Enable the Enable LOB Wise toggle.
From the LOB/Profile dropdown, select the required LOB to which, the mail servers need to be mapped.
From the Mail Server dropdown, select the Mail server to which, the selected LOB needs to be mapped.
Click on Assign. The selected mail server will be mapped to the specified LOB.
The Export  button will export all the mapped mail servers details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.3.2.3 User Security - Other Configurations
Field Name Description
Instance Is Checked By Default This configuration enables/disables the availability of the Instance option
in the grid view in CM > Connections.
4.3.7.3.3 User Modification
What are User Modification Settings?
The User Modification settings describe the configuration choices and preferences that the administrator can
make to alter the users' validity, functionality, and appearance in the ARCON PAM application.
To navigate, use the following path:
Settings → User→ User Modification:

## [p289]

www.arconnet.com|Copyright © 2025 289
Field Name Description
Allow User Enabling Once
Disabled - Is Enabled
This configuration enables/disables User Enabling Once Disabled.
Disable If the Toggle value is ‘Disabled', the disabled users can’t be enabled.
Enable If the Toggle value is 'Enabled', the disabled users can be enabled in the
future.
Editable Display Name For
Domain User - Is Enabled
This configuration sets permission to edit the display name of users
integrated into ARCON PAM with Domain validation.
Disable If the Toggle value is ‘Disabled', the domain user can’t edit the display
name.
Enable If the Toggle value is 'Enabled', the domain user can edit the display name.
User Display Name Properties In
LDAP (Separated With ~)
This configuration sets User Properties separated by ~, which will allow
the application to fetch configured values from AD (LDAP) and display
them in the User Display Name field. This is applicable only to Domain
Users.
Valid Values displayName
User Valid Till Date The user will be valid for the specified number of days.
Valid Values If the minimum value is 0 (default value), the date will be displayed as 2058
(the default ARCON PAM Date). If the maximum value is set to specified
days, the user will be valid for the specified number of days.
Display username along with
userId on all Mapping screen
This configuration will display the User Display name along with the User
ID (Example-If user ID is John.D and the User Display name is John David,
then it should be seen as:
John.D (John David) under the following screens:
ACMO-> Manage -> Server Manager
Map Group/Users
Map Users/Services
Manage Commands
Manage Processes
GroupAdmin - Map Services
Disable If the Toggle value is 'Disabled', only the User ID is visible on all the screens
mentioned above.

## [p290]

www.arconnet.com|Copyright © 2025 290
1.
2.
3.
4.
Field Name Description
Enable If the Toggle value is 'Enabled', the User ID( User Display name) is visible
on all the screens mentioned above.
4.3.7.3.3.1 Configure User Tags
The Configure User Tags are the critical configurations given to the ARCON PAM Services. User Tags give
control over what users of your site have access to. Admin can arrange users into these groups by assigning
them the appropriate tag.
To navigate, use the following path:
Settings > User > User Modifications > Configure User Tags0
Select Configure User Tag under User Modifications.
Enter the details, and make sure that the template name must be unique.
Description Field 1 Name: Enter the name of the Description Field. This entered value will be the field
name displayed in Manage Users. Display an information icon with the following message - “This is a
dropdown field".
Enter the name of the Description Field. This entered value will be the field name displayed in Manage
Users. Enter comma-separated to display in the dropdown. Display an information icon
with the following message - “Enter comma-separated values. Admin can import values from LDAP”.
To configure the values Administrator should be assigned Configure User Tags privileges from the
Administrator under Server’s Privileges.

## [p291]

www.arconnet.com|Copyright © 2025 291
5.
6.
7.
•
•
•
•
•
Description Field 1 Value: Enter comma-separated to display in the dropdown.
Similarly, Description Field 2 Name will be similar to Description Field 1 Name, and Description Field 2
Value will be similar to Description Field 1 Value.
Description Field 3 and 4 will be text fields.
4.3.7.4 Service Setting
What are Service Settings?
Service settings refer to the configuration options and parameters that control how the program interacts with
other system services, such as network protocols, operating system features, and other software applications.
Why are Service Settings Important?
Service settings have a big impact on how secure a system is overall. The confidentiality and integrity of
sensitive data can be guaranteed by properly configured service settings, which also assist prevent
unauthorized access and reduce the impact of malware or other security concerns. On the other hand,
improperly configured service settings might make a system more open to attack, jeopardize its security
measures, and reveal private data.
This section includes the following topics:
Security
SSH
Windows
Request
Service Modifications
4.3.7.4.1 Security setting
4.3.7.4.1.1 Service Critical Command
Critical Commands are commands which are defined as highly critical for use. These commands when executed
will have a crucial impact on the target server or on the resources associated with it. When an attempt is made
to execute a critical command, it will prompt confirmation for executing the command.
This section helps you to define a critical command for a service. In addition, you can modify or delete an
existing defined critical command.
LDAP Value is a checkbox. If this value is selected, “Description Field 1 Value” field will be disabled and
a text box beside this checkbox will be enabled along with the LDAP Path text field.
Click on the checkbox will enable this field. If not then the checkbox will not be enabled.
If Description Field Name is kept blank then it will be displayed as Description Field 1 (2/3/4)
in Manage Users screen.

## [p292]

www.arconnet.com|Copyright © 2025 292
1.
2.
To navigate, use the following path:
Settings → Service → Service Security
Select the Service Critical Commands under Security.
Select the Add button to add a new service critical command:
The Service Critical Commands screen contains the following fields:
The Administrator having Service Critical Commands privilege in Server’s Privileges will only be able
to define a critical command for a service.

## [p293]

www.arconnet.com|Copyright © 2025 293
3.
4.
Field Name Description
Service Type Select the type of service.
Command Define a command.
Command Description Specify the command description.
Remark Specify the remark.
Ask User Confirmation (Before Execution) Indicates that the user will be asked for confirmation before
executing the command.
Enabled Enables the configuration.
Delete button Click Delete, to delete the selected critical command from
ARCON PAM.
Click on Save to save all the changes and the service critical command has been set. A window pops up
with the following message:
For editing, the details of the existing service critical command, click on the existing row and select the
Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.

## [p294]

www.arconnet.com|Copyright © 2025 294
5.
6.
For deleting the existing service critical command, click on the existing row and select the Delete button
at the top and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the service critical command details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.4.1.2 Service Security Configurations
Service Security Configurations refer to security procedures that are applied to the services to minimize
unneeded cyber vulnerabilities.
To navigate, use the following path:
Settings → Service → Service Security:

## [p295]

www.arconnet.com|Copyright © 2025 295
Field Name Description
Service Critical
Commands
This helps the administrator to define a critical command for a service. Refer to the
Service Critical Commands section for more details.
Restricted Command
Error Message
This configuration sets the Message that should be displayed by ARCON PAM
when an attempt is made to execute any Restricted Command.
Valid Values Contact ARCON PAM Administrator To Get Access to the Restricted Command.
Resolve IP Address
Before Connecting (If
Direct Access) - Is
Enabled
This configuration enables/disables resolving of IP Address before Connecting to
target server if Direct Access (this is applied only in an environment without
secured).
Toolbar In App
Attachmate Reflection -
Is Enabled
This configuration will allow users to access the SFTP connection of the App
Attachmate Reflection application. By default ARCON PAM disables the toolbar.
Remove Sign On Menu
In App PLSQL Developer
Oracle - Is Enabled
This configuration will allow users to remove LogOn menu from PLSQL
Developer Oracle Application. By default ARCON PAM enables the LogOn menu.

## [p296]

www.arconnet.com|Copyright © 2025 296
1.
Field Name Description
ARCON PAM MultiTab
Option
This configuration enables/disables Users to open multiple Windows RDP and SSH
Linux connections in multiple tabs (single window).
Disable If Toggle value is 'Disabled', then multiple connections can be opened but in
different windows.
Enable If Toggle value is 'Enabled', then MultiTab option will be displayed before
establishing Windows RDP connection and SSH MultiTab option will be displayed
before establishing the SSH Linux connection.
Oracle Virtual RAC IPs It will display the list of the IPs for the Oracle Virtual RAC.
Valid Values The value ranges from 1-999.
Service Health Status It will display the health status of the services being monitored
Disable If Toggle value is 'Disabled', then this feature is disabled.
Enable If Toggle value is 'Enabled', then this feature is enabled.
Days For Server Last
Accessed On
It will display the list of idle servers for the configured value or more for Server
Last Accessed Report. Example: If the configured value is 10, the server Last
Accessed Report will display all the servers that were idle for 10 days.
Valid Values The value ranges from 1-999.
4.3.7.4.1.3 Outside ARCON PAM Access Configuration
ARCON PAM monitors Servers that are accessed from outside ARCON PAM. You can configure actions such
as sending alert to configured users or blocking access to the Server from outside ARCON PAM.
Pre-requisite: ARCOS TSPlugin service should be installed on the server, for monitoring users trying to access
the server.
To navigate, use the following path:
Settings → Service → Service Security0
Select Outside ARCON PAM Access Configuration under Security:
The Administrator having Outside ARCON PAM Access Configuration privileges in Server’s
Privileges will only be able to configure action to be performed under Outside ARCON PAM Access
Configuration.

## [p297]

www.arconnet.com|Copyright © 2025 297
•
•
•
•
2.
The Outside ARCON PAM Access Configuration screen contains the following fields:
Field Name Description
Action Select the action to be taken.
The valid values are:
No Action: Perform no action on access.
Email Notification: Send email notification to Users, necessary to be
intimated during access.
Block: Block access to server
Email Notification & Block: Send email notification to Users and
block access to server.
Notify To Select the Users to send email notification.
Email ID should be configured in Edit User Settings under Manage Users to
list Users in Notify To selection list.
Select the required details and click Save. The following success message will be displayed:0

## [p298]

www.arconnet.com|Copyright © 2025 298
3. Click OK. The details will be saved and configured action will be performed when the server is accessed
outside ARCON PAM.
4.3.7.4.2 SSH
For secure remote access to a computer or server, the SSH (Secure Shell) protocol is utilized. SSH service
settings are a collection of configuration options and parameters that can be used to manage and regulate the
operation of the SSH server software.
To navigate, use the following path:
Settings → Service→ SSH:

## [p299]

www.arconnet.com|Copyright © 2025 299

## [p300]

www.arconnet.com|Copyright © 2025 300
Refer to the below table to understand the data present in SSH:
Field Name Description
Use SFTP Privileges This configuration sets whether SFTP Privileges should be allowed to all
users or not.
Disable If Toggle value is 'Disabled', then this privilege is by default given to all
users.
Enable If Toggle value is 'Enabled', then Admin ID needs to give this privilege for
an individual user under the Server Manager > Manage Commands tab.
ARCOS Default SSH Terminal This configuration sets which SSh Terminal to be used. There are two
different SSh terminal interchangeably used with different sets of
functions being delivered.
Valid Values It can be either 1 or 2.
Value ‘1’ – With this value SSh terminal will have all the standard
functionality of a PuTTY client but no function key mapping.
Value ‘2’ – With this value SSh terminal will have function key mapping
along with standard functionality of a PuTTY client.
SYSADM Account For Root User 7
& 16 (With Comma)
This configuration sets SYSADM Account for Root User 7 & 16 (IP - 7 for
SSH Linux and IP- 16 for DMZ SSH Linux). SYSADM is required to login to
switch to Root. Multiple values are separated by Comma.
Valid Values  The valid strings are arcon, sysadm, sysadmin, netadmin.
Root Account For IP Service Type
7 & 16 (With Comma)
This configuration sets Root Account for IP Service Type 7 & 16 (IP - 7 for
SSH Linux and IP- 16 for DMZ SSH Linux). Multiple values are separated
by Comma. These accounts are used for changing password.
Valid Values The Valid strings are arcon,root,test.
Domain Validation For SSH Based
Connections - Is Enabled
This configuration enables/disables Domain Validation for SSH Based
Connections.
Service Critical Commands - Ask
User Confirmation (Before
Execution) - Is Enabled
This configuration enables/disables the working of Ask User
Confirmation (Before Execution) option of Service Critical Command.
Disable If Toggle value is 'Disabled', then the steps below are carried out then
confirmation message will not be displayed.

## [p301]

www.arconnet.com|Copyright © 2025 301
Field Name Description
Enable If Toggle value is 'Enabled', and under Server Manager >Settings >
Service >Security > Service Critical Command > Configure a command
and tick Ask User Confirmation (Before Execution). Execute this critical
command on the server. A confirmation message will be displayed.
ARCOS SSH Terminal (2) SSH
Authentication Methods Type
This configuration will set SSH Authentication Method for ARCON PAM
SSH type 2 Terminal (“suse”).
Valid Values Select from the dropdown where the values are 0,1,2,15.
ARCOS Switch User Reason
Popup Box
This configuration when enabled will raise a popup box when a switch
user attempt is made during a service session. User needs to enter the
reason for switching to another user in the popup box and click on submit
button. This will effect the configured Service Type.
Valid Values Select from the dropdown where the values are SSH, TELNET, SQLPLUS.
ARCOS SFTP Latest Ciphers Is
Enabled
This configuration will enable/disable the latest ciphers.
Valid Values It ranges from 5-99.
ARCOS Putty WebService CLURL This configuration is used to configure web API URL for ARCON PAM
API. This API can be used in PAM Client Multi-type Utility for RDP and
SSH Linux Connections.
Valid Values Configure web API URL for ARCON API URL
Execute Network Command With
Credential
This configuration is used to configure commands for which you
want ARCON PAM to enter credentials on Server before executing
commands.
Valid Values The Configuration Value shall be Command_Name. Multiple commands
can be configured separated by a comma. Eg: sudo, passwd.
Enforce Login to EN Account  This configuration enables/disables Network Device services (Telnet
Router, Telnet Switch, SSH Router, SSH Switch, SSH Telnet) to switch to
configuration mode.
Disable If Toggle value is 'Disabled', then User needs to access service and then
switch to EN service.

## [p302]

www.arconnet.com|Copyright © 2025 302
Field Name Description
Enable If Toggle value is 'Enabled', then User is switched to configuration mode.
Stop SSHOracleSqlplus Auto
Login
This configuration sets whether the Database list will be displayed to
User when SSH Oracle SQL Plus connection is established from Client
Manager.
Disable If Toggle value is 'Disabled', Service will connect to the default Database.
Enable If Toggle value is 'Enabled', you have multiple database on the Server and
you want to login into a particular DB.
Enable/Disable Copy Paste in
Putty
This Configuration restricts the Copy Paste option in putty.
Valid Values The valid values are Enable Copy Paste everywhere, Enable Copy Paste
only in Putty window, Disable Copy Paste everywhere.
Enable Copy Paste everywhere- This Configuration allows copy-paste
functionality inside putty session window as well as outside putty eg- in
notepad.
Enable Copy Paste only in Putty window- This configuration allows
copy-paste functionality only inside putty session window.
Disable Copy Paste everywhere- This configuration disables copy-paste
functionality everywhere i.e both inside and outside putty.
Disable copy to all option in
ARCOSPutty
This configuration restricts the Copy to all option in ARCOSputty.
Disable If the Toggle value is 'Disabled', the users can access copy to all option
everywhere.
Enable If the Toggle value is 'Enabled', the users cannot access copy to all option
from ARCOSputty.
SSH Capture Process ID  This configuration will capture the process ID.
Disable  If the Toggle value is 'Disabled', the process ID will not be captured
Enable  If the Toggle value is 'Enabled', the process ID will be captured.
SSH New Command Log Web
Method
This configuration will enables/disables the new command log web
method.

## [p303]

www.arconnet.com|Copyright © 2025 303
Field Name Description
 SSH File Size If the user wants to specify the size(kb) of the logs in the SSH Log File size
section, the out put of the log will be of the same size.
SSH file path Once the user specify the server location in that SSH log file section, the
logs will start moving from client location to specified location from the
global settings.
Enable SSH Reconnect option This configuration is used to reconnect the accessed Linux services from
putty in case of service stops working due to crash or network issues.
Apply all SFTP controls to SSH
Linux services
By enabling this toggle, users are allowed to automatically configure each
SSH Linux service.
4.3.7.4.3 Windows
What are Windows Settings?
The Windows settings refer to the numerous configuration settings and parameters that can be used to
administer and regulate the actions of the ARCON PAM application while it is running as a Windows service. To
guarantee that the cyber security application is operating securely and effectively, as well as to prevent any
unexpected effects or vulnerabilities, it is crucial to configure Windows service settings properly.
To navigate, use the following path:
Settings → Service→ Windows:
 The maximum log file size is 500kb.

## [p304]

www.arconnet.com|Copyright © 2025 304
Field Name Description
Show VNC Button This configuration shows/hides the VNC button on RDP Service Type.
Windows RDP - Use Console
Privileges
This configuration enables/disables the Console Privileges button for
Windows RDP.
Disable If Toggle value is 'Disabled', then this privilege is by default given to all
users.
Enable If Toggle value is 'Enabled', then Admin ID needs to assign this privilege
for individual users under the Server Manager > Manage Commands tab.
Windows RDP - Allow Clipboard
To All
This configuration enables/disables Clipboard by default for Windows
RDP session taken through ARCON PAM.
Windows App Option For
Windows RDP - Is Enabled
This configuration enables/disables display of Windows App option
before accessing Windows RDP service in CM > Connections > Select
Windows RDP option from Service Type drop-down > Click Open.
Process Level Restriction - Is
Enabled
This configuration enables/disables process restriction on Windows
Server.

## [p305]

www.arconnet.com|Copyright © 2025 305
Field Name Description
Disable If Toggle value is 'Disabled', then processes will not be restricted. Also
‘Manage Processes’ tab will not be available under Server Manager >
User and Services and ‘Process Logs’ will not be available under View
Logs.
Enable If Toggle value is 'Enabled', then processes will be restricted on Windows
Server.
ARCOS TS Monitor Keep Alive
Max Value
This configuration sets the number of attempts to connect to the ARCOS
TS Monitor plug-in on Server for the Session taken through ARCON
PAM. If ARCOS TS Monitor plug-in is not connected in these attempts
then the session is terminated.
Valid Values It ranges from 1-99
ARCOS TS Monitor Connection
Timeout (Seconds)
This configuration is a timeout value for RDP Terminal to determine
whether ARCON PAM TS Monitor has started on target server (if
configured for particular RDP session).
Valid Values It ranges from 30-999
Allow RDP Connection Without
TS-Monitor
This configuration enables/disables session termination if ARCOS
TSPlugin service is not installed on Server but ARCOS TS-Monitor is
enabled for User and Service mapping under Manage Commands(Server
Manager).
Disable If Toggle value is 'Disabled', then the session will be terminated.
Windows Terminal Option For
Windows RDP - Is Enabled
This configuration enables/disables display of Terminal option before
accessing Windows RDP service in CM > Connections > Select Windows
RDP option from Service Type drop down > Click Open.
Disable X-RDP Reconnect Option  This configuration will disable the X-RDP Reconnect Option.
RDP Timeout This configuration enables/disables a global session time out for
Windows RDP services.
Values Specify the session timeout value in minutes.
4.3.7.4.4 Request
What are Request Settings?

## [p306]

www.arconnet.com|Copyright © 2025 306
The Request settings in the ARCON PAM application are typically used by administrators to configure requests
to access the services. This is to guarantee that security measures are applied consistently and successfully,
particular people or teams are typically allocated to specific security tasks in an organization.
To navigate, use the following path:
Settings → Service→ Request:
Field Name Description
Time Based Request Service
Access - Is Enabled
This configuration sets availability for Time Based Service Access Request
under CM > Connections > Raise Request > Service Access > Access Type
drop-down.
Hide Configuration Command for
Service Request
This configuration will hide/display the configuration command field on
the Service Access Request form (Client Manager > My Access > Raise
Request > Service Access).
Disable If the toggle is set to "Disabled", then it will display the Configuration
Command field
Enable If the toggle is set to "Enabled", then it will hide the Configuration
Command field on the Service Access Request form.
ARCOS Service Password - Is
Enabled
It enables/disables Service Password requests.
Disable If the toggle is set to "Disabled", then users won't be able to raise a service
password request.

## [p307]

www.arconnet.com|Copyright © 2025 307
Field Name Description
Enable If the toggle is set to "Enabled",(default value) then the users shall be able
to raise a service password request.
ARCOS Service Access - Is
Enabled
This configuration will enable or disable the Service Access option under
Raise Request (My Access > Raise Request) in the Client Manager
Access Duration For Service
Access Request(in days)
The users can raise a service access request for a specified number of
days.
Valid Values It ranges from 1-90 days.
The minimum value is 1 (default value), and the users shall be able to raise
a service access request only for a day. The maximum value is 90, the
users shall be able to raise a service access request for 90 days.
Permanent Request Service
Access - Is Enabled
This configuration enables/disables the users to raise a permanent service
access request.
Disable If the toggle is set to "Disabled", then the users won't be able to raise a
permanent service access request.
Enable If the toggle is set to "Enabled", then the users shall be able to raise a
permanent service access request.
Time Based Service
Access Request From Server
Manager - Is Enabled
This configuration enables/disables the pop-up which asks for Service
level access, whether, One Time, Time Based, or Permanent under Server
Manager > Manager> Manage User/Service.
Disable If the toggle is set to "Disabled", then users won't be able to see the popup
on selecting the service.
Enable If the toggle is set to "Enabled", then users will be able to see the popup on
selecting the service.
One Time Service Access
Request- Is Enabled
This configuration sets availability for One Time  Service Access Request
under CM > Connections > Raise Request > Service Access > Access Type
drop-down.
Disable If the toggle is set to "Disabled", then the users won't be able to raise one
time service access request.
Enable If the toggle is set to "Enabled", then the users shall be able to raise one
time service access request.

## [p308]

www.arconnet.com|Copyright © 2025 308
1.
Field Name Description
Enable Offline Access This configuration allows the users who work onsite and are not
connected to PAM to take offline sessions.
Disable If the toggle is set to "Disabled", Offline Access Feature will be disabled
globally and the user will neither be able to request offline service access
nor can take offline access to any service.
Enable If the toggle is set to "Enabled", the Offline Access feature will be enabled
globally. For example, the user can request offline service access in
ACMO/Multitab, user can take offline access to service through Multitab.
Select Service Types For Offline
Access
The administrator need to select the one or more service types from the
dropdown that can be requested for offline access. Check box “Select All”
to select or deselect all the service types at a time.
4.3.7.4.5 Service Modification
4.3.7.4.5.1 Service Mandatory Field Configuration
The Service mandatory field configurations set the mandatory configurations which help an organization in
reviewing and auditing. ARCON has few proprietary mandatory configurations, however, the admins too can
set their own mandatory configurations. These settings are reflected with an asterisk mark while creating/
modifying the service, or using the quick search functionality to find a service and then modify it, or when the
user uses bulk update, all under the Manager Service Section. It is also reflected while importing server
connections under the import section and while setting service details in ARCON PAM API.
To navigate, use the following path:
Settings → Service →  Service Modifications
Select Service Mandatory Field Configuration under Service Modifications:
This configuration is enabled only when the Enable Offline
Access configuration is enabled.
The Administrator having Service Mandatory Fields Configuration privilege in Server’s Privileges will
only be able to configure details in Service mandatory field configurations.

## [p309]

www.arconnet.com|Copyright © 2025 309
2. Configurations enabled here are set as mandatory fields in the Administrative Console.
4.3.7.4.5.2 Advanced Utility
What is Advanced Utility?
Advanced Utility is used to convert the font of the Service Host Name and Service Domain Name to uppercase.
This setting feature is used to standardize the naming format and to increase the user experience. Usually while
writing hostname, service domain, and username people used to write in their own style, but each organization
has a standard naming format. This setting helps to get it standardized.
To navigate, use the following path:
The Administrator having Advanced Utility privileges in Server’s Privileges will only be able to convert
the font.

## [p310]

www.arconnet.com|Copyright © 2025 310
1.
2.
Settings → Service → Modification:0
Select Advanced Utility under Modification:
The Advance Utility screen contains the following buttons:0
Field Name  Description
Convert All Service Host Name to Uppercase  It converts the font of all service hostname to uppercase.
Convert All Service Domain Name To Uppercase It converts the font of all service domain name to
uppercase.
Convert First Letter of Server User Name To
Uppercase
It converts the font of the first letter of Server username to
uppercase.
A window pops up with the following message:
4.3.7.4.5.3 Service Classifications
What are Service Classifications?

## [p311]

www.arconnet.com|Copyright © 2025 311
1.
2.
3.
Service Classification defines the classification for a service such as critical, data, or antivirus server. In
addition, you can modify the existing defined classification. Once the classification is defined, you can apply the
classification while modifying the parameters of a service.
To navigate, use the following path:
Settings → Service → Service Modifications0
Select Service Classification under Service Modifications:
Select the Add button to add a new service classification.
The Service Classification screen contains the following fields:
Field Name  Description
Service Classification Specify the name for a service classification.
Description Specify the description for a service classification.
Click on Save to save all the changes and the service critical command has been set. A window pops up
with the following message:
The Administrator having Service Classification privilege in Server’s Privileges will only be able to
configure under Service Classification.

## [p312]

www.arconnet.com|Copyright © 2025 312
4.
5.
6.
For editing, the details of the existing service classification, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.0
For deleting the existing service classification, click on the existing row and select the Delete button at
the top and make the required changes. Also, you can right-click on the row and select Delete.0
The Export button will export all the service critical command details in the form .xlsx format. The Copy
button will copy all the details of the table.

## [p313]

www.arconnet.com|Copyright © 2025 313
7.
a.
i.
ii.
iii.
iv.
b.
i.
ii.
iii.
iv.
v.
vi.
You can apply this service classification to service (s).
Apply to a single Service:
To apply Service Classification to a single service, use the following path:
Server Manager → Manage → Users and Services → Manage Services
Select a service.
Right-click and select Modify Service Parameters.
Select Service Classification from the dropdown.
Click Modify. The selected Service Classification will be applied to the Service.
Apply to a group of Services:
To apply Service Classification to services, use the following path:
Server Manager → Tools → Settings → Groups→ Apply Password Settings
Select the LOB or profile from the LOB/ Profile dropdown list. A list of service groups is
displayed in the grid.
Select the checkbox from the Service Group Name list. It displays the count of services for
that particular group under the Service Type grid.
Select a type of service from the Service Type list. This will enable you to set automated
change passwords for that particular service type.
To apply service classification, select Allow  checkbox against the Service Classification
drop-down. The drop-down will be enabled.
Select the required service classification.
Click Confirm Changes  button. Service Classification will be applied to services under
selected Service Group and Service Type.
4.3.7.4.5.4 Service Modifications Configurations
The process of customizing and modifying a service's settings to improve its efficiency and efficacy in defending
the system against security threats is known as service modification configuration in the ARCON PAM
program. An essential component of cyber security is service modification configuration, which enables users
to enhance the efficiency and efficacy of their security software and safeguard their systems and data from
potential security risks.
To navigate, use the following path:
Settings → Service → Modification:
Field Name Description
Description 1 New Name This configuration sets the new name for Description 1.
Valid Values It sets the value for Description 1.
Description 2 New Name This configuration sets the new name for Description 2.
Valid Values It sets the value for Description 2.

## [p314]

www.arconnet.com|Copyright © 2025 314
•
•
•
Field Name Description
Description 3 New Name This configuration sets the new name for Description 3.
Valid Values It sets the value for Description 3.
Description 1 - Is Editable This configuration enables/disables Description 1.
Description 2 - Is Editable This configuration enables/disables Description 2.
Description 3 - Is Editable This configuration enables/disables Description 3.
Confirmation Box For
Mapping Operations In
ARCOS Server Manager -
Is Enabled
This configuration sets whether the Confirmation box should be displayed when
mapping Operations are performed in Server Manager between entities.
Allow Permanently Service
Deletion - Is Enabled
This configuration enables/disables permanent service deletion from ARCON
PAM database including, the logs, mapping, and so on. It deletes everything
except the audit trail.
Service Display
Configuration
This configuration sets which Service details are to be displayed in following
fields:
Service (CM > My Access > Raise Request > Service Access)
Service (CM > My Access > Raise Request > Service Password)
Service / IP Address (CM > My Access > Raise Request > Ticket)
Valid Values IPADDRESS,USERNAME,DOMAIN,DBINSTANCE,HOSTNAME,USERDISPLAY
NAME,USERDESCRIPTION
Service Creation - Force
Host Name check from DB
This configuration is explained below.
Disable If Toggle value is 'Disabled', while creating a service the combination of service
type and IP address, and the Host Name is different then it will display a prompt
Yes/No. If yes, the service will be created, and If No, the service will not be
created.

## [p315]

www.arconnet.com|Copyright © 2025 315
•
•
•
•
•
•
•
•
•
Field Name Description
Enable If  Toggle value is 'Enabled', while creating a service it ensures that the
combination of service type and IP address, the Host Name has to be the same
every time for the service to be created. It will not create a service if the
hostname is different.
Service Expiry Days If the value is set to 5 an alert notification shall be sent 5 days before the service
expiry and so on. An alert notification shall be displayed in ACMO notifications
before the Service Validity expires (before the days configured) so that the
Administrators can extend the validity period of the service if required. Users
with the Privilege Service Expiry Due will only be able to view this notification.
Valid Values It ranges from 5-99 days.
JIT Service Access Request When you enable the JIT Service Access Request toggle, a dropdown field will
appear under ACMO → My Access → Raise Request → Service Access Request,
where you can select the JIT Provisioning Service option.
4.3.7.5 Password
What are Password Settings?
Password settings are an important aspect of the ARCON PAM application that helps to protect sensitive
information and prevent unauthorized access.
Why are Password Settings Important?
The password settings are designed to make it more difficult for attackers to gain access to sensitive
information, and to provide an additional layer of protection against cyber threats.
This section includes the following topics:
HSM configuration
Generic Scheduler Setting
Password Dashboard
View Password
Password Change
Reconciliation
Fail Safe (Envelope)
Debug Mode
Miscellaneous
4.3.7.5.1 HSM Configuration
What is HSM Configuration?
The Hardware Secure Module (HSM) feature is used to verify sensitive data by provisioning encryption and
decryption. This feature can be enabled for a service. ARCON PAM will use HSM for verifying details. The
Administrator is responsible for modifying a service that can enable this feature.
To navigate, use the following path:

## [p316]

www.arconnet.com|Copyright © 2025 316
1.
2.
Settings → Password
Select HSM Configuration under Password:
Select the Add button to add a new Hardware Secure Module:
The Hardware Secure Module Configuration screen contains the following fields:
Field Name Description
Device Type Select the device type from the dropdown.
Device Name Enter the HSM device name.
IP Address Enter the IP Address of HSM.
Port Enter the port number.

## [p317]

www.arconnet.com|Copyright © 2025 317
3.
4.
5.
6.
Field Name Description
Label/Key Enter the Key
Slot Number Enter the slot number
Password Enter the password.
Enter the details and click the Save button to create a new Hardware Secure Module Configuration.
For editing, the details of the existing Hardware Secure Module Configuration, click on the existing row
and select the Edit button at the top and make the required changes. Also, you can right-click on the row
and select Edit.0
For deleting the existing Hardware Secure Module Configuration, click on the existing row and select
the Delete button at the top and make the required changes. Also, you can right-click on the row and
select Delete.
The Export button will export all the Hardware Secure Module Configuration details in the form .xlsx
format. The Copy button will copy all the details of the table.
•
•
You need to enable Precision Biometric for fingerprint authentication over API from the back
end.
The Precision Authentication API URL will be provided by the Client. Enter this URL in the
URL text field and configure details in Web API Configuration window.

## [p318]

www.arconnet.com|Copyright © 2025 318
1.
2.
3.
4.
5.
6.
7.
1.
4.3.7.5.2 Generic Scheduler Settings
What are Generic Scheduler Settings?
The Generic Scheduler Settings are the critical configurations given to the ARCON PAM Services and
executable files. In this configuration, the Settings Values are configured. The executable files such as ARCOS
Generic Scheduler, ARCOS Provisioning Scheduler, and so on, consider these settings for running the files.
ARCON PAM Services such as ARCOS Alert Service, ARCOS Log Manager Service, and so on, consider these
settings for running the services.
Assign Generic Scheduler Setting
To assign these privileges follow the below steps:
Open Server Manager.
On the menu bar, click Manage > Users and Services > Manage Users.
On the Users Type, select admin from the dropdown list. All admin users will be displayed.
Select the user present in the User Display Name column.
Right-click on the admin user to whom you want to give the Generic Scheduler Setting privileges and
select Edit Privileges. User Privileges Settings windows open.
Note: Make sure that the Server Privileges radio button is selected as we are assigning these privileges
to the Admin users.
On the User’s Available Privileges frame, select the Default Configuration  and Generic Scheduler
Setting and click the << Add button.
The Default Configuration and Generic Scheduler Setting privileges will be added on the User’s
Assigned Privileges frame.
Configure Generic Scheduler Settings
To configure Generic Scheduler Settings follow the below steps:
To navigate, use the following path:
Settings → Password
Select Generic Scheduler Setting under Password:
To configure the values Administrator should be assigned Default Configuration and Generic
Scheduler Setting privileges from the Administrator under Server’s Privileges.

## [p319]

www.arconnet.com|Copyright © 2025 319
2.
3.
4.
5.
6.
Select the Add button to configure a new Generic Scheduler Settings.
Enter the name of settings, the value of settings, and description in the Settings Name, Settings Value,
and Description text field respectively.
Select the Enabled checkbox to enable this setting.
Enter the details and click Save to create a new Generic Scheduler Settings.
For editing, the details of the existing Generic Scheduler Settings, click on the existing row and select the
Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.

## [p320]

www.arconnet.com|Copyright © 2025 320
7.
8.
For deleting the existing Generic Scheduler Settings, click on the existing row and select the Delete
button at the top and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the Generic Scheduler Settings details in the form .xlsx format. The
Copy button will copy all the details of the table.
The settings given in the below table are used by executable files and services. Following is the
categorization:
Provisioning Scheduler: This is used for LAM.
ARCOS Generic Scheduler: This is responsible for transferring the data from ARCON PAM DB to
the Data warehouse DB via ARCON PAM API. This is used in Data Warehouse.
ARCONPAMVaultApp: This service is responsible for the reconciliation of each service present
in ARCON PAM Services.
The settings name along with its usage and default settings value are as follows:
Sr. No. Settings Name Settings Value Description Usage
1. ProvisioningApiUrl http://IP/arcos/ This value is used for calling External
API for User creation on Target
Server.
Used
for Provisioning
Scheduler

## [p321]

www.arconnet.com|Copyright © 2025 321
•
Sr. No. Settings Name Settings Value Description Usage
2. ProvisioningProces
s
Off This value is used to check whether
Provisioning Process exists on the
server or not.
Used
for Provisioning
Scheduler
3. BatchSize 10000 This value indicates the batch size of
data that will be sent from Scheduler
to the ARCON API.
Used for ARCOS
Generic Scheduler
4. LowMemory 30 -This value is used to determine,
whether Parallel processing should
be initiated or not.
If the Actual CPU usage is
lower than this specified
value then Parallel Processing
should be initiated.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp
5. LowCpu 30 -This value is used to determine,
whether Parallel processing should
be initiated or not.
-If the Actual CPU usage is lower
than this specified value then
Parallel Processing should be
initiated.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp
6. ApplicationName GenericScheduler This value indicates the name of the
application.
Used for ARCOS
Generic Scheduler
7. TimerInterval 6000 This value indicates the Timer to be
triggered after the specified value.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp
8. HighCpu 90 -The value indicates the high limit of
CPU usage.
-If CPU usage is below the specified
level, then only processing will start.
Increment the value if the scheduler
is not running.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp

## [p322]

www.arconnet.com|Copyright © 2025 322
Sr. No. Settings Name Settings Value Description Usage
9. ParallelProcessing N -This value indicates whether
Parallel Processing should start or
not.
-Irrespective of low usage, if the
value is N, then parallel processing
won't start.
-Possible value for this setting is Y or
N.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp
10. SiteName Site Name (Eg.
Site1)
This value indicates the site name
used in Data Warehouse.
Used for ARCOS
Generic Scheduler
11. DWHAPIUrl http://IP:Port/api/ This value indicates the URL of API
for dumping data into the Data
Warehouse Database.
Used for ARCOS
Generic Scheduler
12. OffPeakTime NightTime This value indicates the time other
than peak time.
Possible values for this setting are
NightTime, DayTime and Both.
Used for ARCOS
Generic Scheduler
13. DecryptDataLimit 50000 This value indicates the decryption
limit used for Data Warehouse
Application for decrypting data at a
single time.
Used for ARCOS
Generic Scheduler
14. DatawareHousePr
ocess
On This value indicates whether Data
Warehouse Process exists on the
Server.
Used for ARCOS
Generic Scheduler
15. HighMemory 90 This value indicates the Timer to be
triggered after the specified value.
Used for Provisionin
g Scheduler, ARCOS
Generic Scheduler
and
ARCONPAMVaultA
pp
16. StartTime 9:00:00 -This value indicates the start time of
the service password change
password.
-Enter the value in 24-hour format.
Used for
ARCONPAMVaultA
pp
17. EndTime 22:00:00 -This value indicates the end time of
the service password change
process.
-Enter the value in 24-hour format.
Used for
ARCONPAMVaultA
pp
18. PasswordChangePr
ocess
On This value is used for turning On /
Off password change process.
Used for
ARCONPAMVaultA
pp

## [p323]

www.arconnet.com|Copyright © 2025 323
Sr. No. Settings Name Settings Value Description Usage
19. MaxPasswordAgeR
ange
10 -This value indicates the number of
hours to be considered by password
change vault service.
-The password of the service will get
changed before the specified
number of hours of the password
expiry. Eg. the Password of the
service will be changed 10 hours
before the password expiry time.
-The default value for this setting is
10.
Used for
ARCONPAMVaultA
pp
20. MonthCount 2 This value indicates the number of
months for fetching data.
Used for ARCOS
Generic Scheduler
21. IsRunIncrementalD
ata
0 This value indicates whether to run
increment data instead of checking
firstrun. The value '0' stands for 'No'
and '1' stands for 'Yes'.
Used for ARCOS
Generic Scheduler
22. TillDate 05/01/2018 This value indicates up to which back
date data should be pushed to DWH.
Used for ARCOS
Generic Scheduler
23. MaxDegreeOfParal
lelism
1000 This value indicates the number of
parallel threads running at a time.
More numbers might increase the
CPU percentage of the Server.
Used for
ARCONPAMVaultA
pp
24. TelnetTimeout 0 This value is used for telnet the
server for connectivity. The value is
in milliseconds.
Used for
ARCONPAMVaultA
pp
25. BatchSizeForRecon
ciliation
50 This value indicates the batch size
used for reconciliation of services
parallelly.
Used for
ARCONPAMVaultA
pp
26. SamlSPEntityId Entity Id (Eg.
99a5d86d17d241
b3b732bfa6a0054
e1b)
This value is the SAML Entity Id
This is considered only for
DWH Log tables.
If the batch size is increased
then check for the Out Of
Memory exception.

## [p324]

www.arconnet.com|Copyright © 2025 324
Sr. No. Settings Name Settings Value Description Usage
27. EntityName ARCON PAM
Reporting
This is the name of the application
28. EntityCode PAMRP This is the code name of the
reporting portal
29. CertificateName IISExpressDev.pfx This is the certificate used for SAML
Authentication
30. CertificatePass Key (Eg.
uOo2a5MH2uKyz
hAUX8TVhQ==)
This key is associated with the value
mentioned in CertificateName. It is
used as a key for the certificate
mentioned.
31. ConsumerServiceU
rl
http://IP:Port/
ReportView/
Index2
This is Reporting Portals URL, which
is hosted separately, need to update
the IP and port of ReportingPortal,
the rest of the URL will be the same.
32. TargetUrl http://IP:Port/ This URL is of Reporting Portal,
update the IP Address and Port
33. AssertionEncryptio
n
true This value represents whether the
rpUser, rpPass and API Url are in
ARCOS encrypted format or not. If
True then mentioned values are in
ARCOS Encrypted format. API URL
is in Base64 Encoding.
34. rpUser ARCOS Encrypted
Value
(Eg.
3Ez6M30ys7gLnz
HPQR7/H1qB5lh/
6QYa6h7YeOwpL
TU=)
This value represents the ARCOS
Encrypted Value of API User.
35. rpPass ARCOS Encrypted
Value
(Eg.TGARyg8RmiE
c5Ixe+x0XEkue7C
9CcUVrpuUZkmQ
1s0U=)
This value represents the ARCOS
Encrypted Value of API Users
password.
36. APIUrl Base64 encoding
Value
(Eg.
aHR0cDovL2xvY2
FsaG9zdDoxMjQ3
Lw==)
This value is the Base64 encoding of
API Url.

## [p325]

www.arconnet.com|Copyright © 2025 325
4.3.7.5.3 View Password
What is View Password?
It is frequently important to view the service passwords for security reasons. The password display time can be
limited by the administrator. The parameters to let or prohibit numerous users from working on a particular
Service can be defined by the Administrators. The see password setting also assists administrators in enabling/
disabling user password change requests for services that depend on other services.
To maintain the security and secrecy of user passwords, it's critical to adhere to best practices for password
management.
This section helps you with configurations to view passwords.
To navigate, use the following path:
Settings → Password→ View Password
Field Name Description
View Password - No of
Authentication Users
This configuration sets the number of users to be enabled to authenticate
on the View Password window under Server Manager > Manage Services >
Select a service > Right-click and select View Password.
Valid Values It is either 1 or 2.
Allow Password Request Of
Dependent Services - Is Enabled
This configuration enables/disables users to request passwords for
services that are dependent on other services for password change.
Disable If the Toggle value is 'Disabled', then the user can request a password for
only the parent service.
Enable If the Toggle value is 'Enabled', then the user can request a password for
both parent and dependent services.
Allow Multiple Users to Request
to open Service Password
This will allow the Administrators to define the settings to allow/deny
multiple users to work on a particular Service.
Disable If the Toggle value is 'Disabled', it will not allow multiple users to open an
already requested/opened Service Password.
Enable If the Toggle value is 'Enabled', it will allow multiple users to open an
already requested/opened Service Password.
Set Min-Max Range for Service
Password Duration (Hours)
This configuration sets the maximum hours to be displayed in the Open for
Hours drop-down under Service Password Request (Client Manager).
Minimum Range: 1-24
Maximum Range: 2-96

## [p326]

www.arconnet.com|Copyright © 2025 326
1.
Field Name Description
Display the Vault Password
button
This configuration displays the Vault password button under ACMO →
Mailbox.
Disable If the Toggle value is 'Disabled', the Vault Password button is not visible
in the ACMO→Mailbox.
Enable If the Toggle value is 'Enabled', the Vault Password button is visible in the
ACMO→Mailbox.
Auto clear closed passwords
from Mail Box older than days
This Configuration clears the closed password from Mailbox post the
configured days.
4.3.7.5.4 Password Change
4.3.7.5.4.1 Password Dictionary
The password dictionary is the repository of default passwords. In ARCON PAM, a set of default passwords are
added that are used in the Password Dictionary of the organization.
To navigate, use the following path:
Settings → Password → Password Change0
Select Password Dictionary under Password Change:
The Administrator having Password Dictionary privileges in Server’s Privileges will only be able to
configure the password dictionary.

## [p327]

www.arconnet.com|Copyright © 2025 327
2.
3.
4.
5.
Select the Add button to add a new default password:
The Password Dictionary screen contains the following fields:
Field Name Description
Description Enter the description for the password
Password Enter the default password.
Enter the details and click the Save button to create a default password.
For editing, the details of the existing password dictionary, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.0
For deleting the existing password dictionary, click on the existing row and select the Delete button at
the top and make the required changes. Also, you can right-click on the row and select Delete.0

## [p328]

www.arconnet.com|Copyright © 2025 328
6.
1.
The Export button will export all the password dictionary details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.5.4.2 Password Change Defaults
Password Change Defaults is a default setting of password change for different operating systems and service
types such as Windows, Linux, and Oracle.
To navigate, use the following path:
Settings → Password → Password Change0
Select Password Change Defaults under Password Change:
The Password Change Defaults screen contains the following fields:
Field Name Description
Username After Password Enable User Name After Password, to use username after password while
configuring password.
The Administrator having Password Change Defaults privileges in Server’s Privileges will only be able
to configure values for Password Change Defaults.

## [p329]

www.arconnet.com|Copyright © 2025 329
•
•
2.
1.
Field Name Description
Use Replace Keyword in
Password Change (Oracle)
Enable Use Replace keyword in Password Change (Oracle), to use Replace
keyword in the Password change process.
Use Gateway Server (ARCON
PAM – Firewall)
Enable Use Gateway Server (ARCON PAM Firewall), to route the password
change process through the gateway server.
ARCON PAM Windows
Password Change Service
Port
Enable ARCON PAM Windows Password Change Service Port, when you
require port for windows password change process.
The default value is 45045.
Use Central Password
Change Service (CPCS Client)
Enable the Central Password Change Service (CPCS Client), to initiate the
password change process through a centralized domain server (ARCON PAM
Server).
Note:
WinPwd  service needs to be installed on the centralized server, to
initiate the password change process.
To configure multiple centralized servers, select Multiple CPCS Clients
checkbox and click on Configure  link, this will initiate the password
change process through multiple domain servers.
RPA Password Change Server To configure the automation of any password change process, click on
Configure link. The pop-up window of the robotic automation process
configuration will open on the screen. Fill in the required details and click on
Save.
Use “suse” For UNIX
Password Change
Enable “suse” for UNIX Password Change, to change the password through
suse putty.
Hide Password Changing Log
Window (Beta)
Enable Hide Password Changing Log window (Beta), to disable the password
log details window in Password Change Log screen.
Select the details and click Confirm Changes to save the configuration details.
Configure Multiple CPCS Clients
To configure multiple centralized servers, select the Multiple CPCS Clients  checkbox and click on
Configure link, this will initiate the password change process through multiple domain servers.

## [p330]

www.arconnet.com|Copyright © 2025 330
2. Click Configure and the following screen is displayed:
The Central Password Change Service Configuration screen contains the following fields:

## [p331]

www.arconnet.com|Copyright © 2025 331
•
•
•
•
•
•
•
•
3.
4.
Field Name Description
Domain Name Enter Domain Name
Server IP Enter the IP Address of Server
Server Port Enter Port Number of Server
Server Type Select the type of Server. The valid values are:
ARCOSWinPasswordChangeService
CiscoACSPasswordChangeService
CiscoISEPasswordChange Service
ForcePointPasswordChangeService
AD Auth URL Enter AD Auth URL
Protocol Port Enter Protocol Port number
Domain Extension Enter Domain Extension
Admin Username Enter Admin Username
Admin Password Enter Admin Password
Enabled Enables the configuration
Based on the Server Type, the details are to be entered:
ARCOSWinPasswordChangeService:  Enter the Domain Name, IP Address, and Port Number of the
server, where ARCOSWinPasswordChangeService (service provided by ARCON Team) is installed.
CiscoACSPasswordChangeService: Enter the Domain Name, IP Address, and Port Number of the
server, where CiscoACSPasswordChangeService (API provided by Third Party Client) is installed.
CiscoISEPasswordChange Service: Enter the Domain Name, IP Address, and Port Number of the server,
where CiscoISEPasswordChange Service (API provided by Third Party Client) is installed.
ForcePointPasswordChangeService:  Enter the Domain Name, IP Address, and Port Number of the
server, where ForcePointPasswordChangeService (API provided by Third Party Client) is installed.
The Export button will export all the password dictionary details in the form .xlsx format. The Copy
button will copy all the details of the table.
To delete record, select any record from the grid and Delete option is displayed on the screen a shown
below.

## [p332]

www.arconnet.com|Copyright © 2025 332
5.
1.
Click Delete to delete the record.
4.3.7.5.4.3 Custom Command Configuration
What is Custom Command Configuration?
Custom Command Configuration is used to configure commands required for password change. This will
remove the dependency on developers to create a database script for every password change commands
request which is required to change the password of the router, switch, and network devices.
 To navigate, use the following path:
Settings → Password → Password Change
Select Custom Command Configuration under Password Change:
The Administrator having Custom command Configuration privileges in Server’s Privileges will only
be able to configure custom commands.

## [p333]

www.arconnet.com|Copyright © 2025 333
2.
•
•
•
3.
To add a command, the following options are present, enter the details and click add command:
Refer the below fields to understand the fields and its description:
 Field Name Description
Command Name Enter name for command
Service Type  Select the service
Parameter  Enter the parameters
Description Enter the description
Enabled Enable the command
Service Connection Type Select the Service Connection Type:
SSH
Telnet
Robotic Process Automation (RPA)
The Custom Command Configuration popup screen will open on clicking Add command,

## [p334]

www.arconnet.com|Copyright © 2025 334
4.
It contains the following fields:
 Field Name Description
Command Name Enter name for command
Command Enter Command
Command Condition NA
Command Response NA
Is Password Prompt NA
Prompt Test NA
Wait For Seconds Duration to execute the command
Enabled  Enable command for execution
Enter the details and click Add Command, to add custom commands. The Custom Command
Configuration popup is displayed:

## [p335]

www.arconnet.com|Copyright © 2025 335
5.
6.
Enter the command details and click Save. A window pops up displaying the following message:
Click OK. The commands are displayed in the Custom Command Configuration grid.

## [p336]

www.arconnet.com|Copyright © 2025 336
7.
8.
Click Save. A window pops up with the following message: New Custom Command Configuration added
Successfully.
The Export button will export all the custom command configuration details in the form .xlsx format. The
Copy button will copy all the details of the table.
4.3.7.5.4.4 Password change Configurations
What are Password Change Configurations?
Password change configuration describes the options and parameters that administrators have at their
disposal to set the password change rules in the ARCON PAM application. User accounts can be made more
secure and the chance of unwanted access can be decreased with the aid of properly configured password
change settings.
To navigate, use the following path:
Settings → Password → Password Change
Field Name Description
Default Password Age For
New Service
This configuration sets the default Password Age for a new service created.
Valid Values It ranges from 0-100.
Password Manager - Group
Authorization (Request
Email Approval) - Is Enabled
This configuration enables/disables Password Manager - Group Authorization.
Disable If the Toggle value is 'Disabled', then it disables Password Manager - Group
Authorization.
•
•
The commands are executed in the order in which they are added for password change.
Therefore, commands shall be added in a proper sequence.
Multiple commands shall be added using Add Command button.

## [p337]

www.arconnet.com|Copyright © 2025 337
Field Name Description
Enable If the Toggle value is 'Enabled', then it enables Password Manager - Group
Authorization.
Change Password - No of
User(s) Authentication
This configuration sets the number of users either 1 or 2 to authenticate
before the password of service is changed under Server Manager > Manage >
Password Manager.
Valid Values  It is either 1 or 2.
Supported Service Types For
Password Change Services
This configuration triggers the Service Password Change for specified Service
Ids.
Valid Values Enter comma-separated service IDs to start Service Password change.
Eg:1,7
In the above example, SPC will trigger password change only for Service Type
ID 1 & 7.
Maximum Failed Attempts
For Password Change
Services
This configuration will exclude the service from changing the password by SPC
Service if the maximum password change failed attempt is reached.
Valid Values It ranges from 3-9.
Allow Dependency From
Across LOB Is Enabled
This will allow services across LOB to be added for Service Password
dependencies.
Disable If the Toggle value is 'Disabled', then it will not allow Services across LOB to be
added for Service Password dependencies.
Enable If the Toggle value is 'Enabled', then it will allow Services across LOB to be
added for Service Password dependencies.
Only Server Group Admin
Can Perform Password
Change-Is Enabled
This configuration enables/disables service password change rights to Server
Group Administrators.
Note:
To know more about Password Change privileges refer Manually change the
password for single or multiple services topics from Password Management
section.
Disable If the Toggle value is 'Disabled', then Administrators having required privileges
can change the password of a service.

## [p338]

www.arconnet.com|Copyright © 2025 338
Field Name Description
Enabled If the Toggle value is 'Enabled', then only Server Group Admins can change the
password of service manually for single (Manage > User and Services >
Manage Services) or multiple services (Manage > Password Manager >
Password Change). Administrators should be assigned Change
Password privilege under ARCON PAM Group Admin Privileges along
with other privileges required for changing the password of the service.
Failure Interval (In Hours)
For Password Change
Services
The password change can be attempted after the specified hours.
Valid Values It ranges from 1-999. The default value is 1.
Service Password change
scheduled days
If the value is set to 5 an alert notification shall be sent 5 days before the
service expiry and so on. An alert notification shall be displayed in ACMO
notifications before the Service Password change. Users with the
Privilege Service Password Change Scheduled will only be able to view this
notification.
Valid Values It ranges from 5-99.
To Unlock and Forced Log
Off User Before Password
Change
This configuration enables/disables the ability to unlock or force log off a user
before the password is changed.
Disable If the Toggle value is 'Disabled', then it will not unlock or force log off a user
before the password is changed.
Enable If the Toggle value is 'Enabled', then it will allow unlocking or force log off a
user before the password is changed.
Switch SSH key management
to .pem format (default
is .ppk)
This configuration when enabled allows switching SSH key management
from .ppk to .pem format.
Disable If the Toggle value is 'Disabled', then it will not switch the SSH key
management from .ppk to .pem format.
Enable If the Toggle value is 'Enabled', then it will allow switching SSH key
management from .ppk to .pem format.

## [p339]

www.arconnet.com|Copyright © 2025 339
4.3.7.5.5 Reconciliation
What is Reconciliation?
Password reconciliation is the process of comparing passwords saved in one system or application with
passwords maintained in other systems or directories for user accounts.
Why is Reconciliation Important?
The security of user accounts and the restriction of access to just authorized users can both be improved with
proper password reconciliation. It is used to check that all user passwords are current and synced across all
apps and systems, as well as to spot any discrepancies or mistakes in password storage. This is crucial to
preserve the security and integrity of user accounts and prevent unwanted access to confidential data.
To navigate, use the following path:
Settings → Password → Reconciliation
Field Name Description
Application Password
Change (ASM) - Is
Enabled
This configuration enables or disables Application Password Change – HP
SiteScope.
Disable If the toggle value is 'Disabled', then it disables Application Password Change-HP
SiteScope.
Enable If the toggle value is 'Enabled', then it enables the Application Password Change-
HP SiteScope.
Root account for MSSQL
Database Users
Passwords Auto Heal
This configuration sets the ROOT accounts for Auto healing
Note- For Auto Healing ROOT Account is required.
Valid Values In this, we add comma separated root usernames.
Eg: If we have MSSQL Service as below
1. 10.10.0.180@user1
2. 10.10.0.280@user1
3. 10.10.0.180@user2
As there are 2 Server IPs mentioned above which will have 2 different root
accounts as follows
10.10.0.180@root, 10.10.0.180@admin
Then you have to configure it as shown below:
root, admin
Note: If 2 Servers have the same root username then add username only once.
Example: root, root is wrong only add root
Root account for Oracle
Database Users
Passwords Auto Heal
This configuration sets the SYS accounts for Auto healing.
Note- For Auto Healing SYS Account is required.

## [p340]

www.arconnet.com|Copyright © 2025 340
1.
2.
3.
Field Name Description
Valid Values In this, we add comma separated sys usernames.
Eg: If we have Oracle Service as below:
1. 10.10.0.180@user1
2. 10.10.0.280@user1
3. 10.10.0.180@user2
As there are 2 Server IPs mentioned above which will have 2 different sys
accounts as follows.
10.10.0.180@sys, 10.10.0.180@admin
Then you have to configure it as shown below:
sys, admin
Note: If 2 Servers have the same sys username then add username only once.
Example: sys, sys is wrong only add sys.
Root account for MySQL
Database Users
Password Auto Heal
This configuration sets the ROOT accounts for Auto healing.
Note- For Auto Healing ROOT Account is required.
In this, we add comma separated root usernames.
Eg: If we have MSSQL Service as below:
10.10.0.180@user1
10.10.0.280@user1
10.10.0.180@user2
As there are 2 Server IPs mentioned above which will have 2 different root
accounts as follows:
10.10.0.180@root, 10.10.0.180@admin
Then you have to configure it as shown below:
root
Note: If 2 Servers have the same root username then add username only once.
Example: root, root is wrong only add root.
4.3.7.5.6 Fail Safe(Envelope)
What is Password Fail Safe Setting?
Password fail-safe is a vital security feature that ensures authorized users can still access their accounts in the
case of a forgotten password or other problem while also helping to prevent unwanted access to user accounts.
To offer a thorough defense against cyber attacks, it is frequently used in conjunction with other security
measures, such as multi-factor authentication.
To navigate, use the following path:
Settings → Password→ Fail Safe(Envelope)

## [p341]

www.arconnet.com|Copyright © 2025 341
Field Name Description
Pin Mailer - Auto
Generate Password For
PDF - Is Enabled
This configuration enables/disables sending passwords to User's Mailbox who has
printed Password for service. This password is used to open PDF files generated by
the user from Server Manager > Manage > Password Manager > Print Password
Envelope > Select Printing Type.
Disable If Toggle value is 'Disabled', then the user needs to enter the password manually
while generating PDF. User needs to use this password to open the PDF file.
Enable If  Toggle value is 'Enabled', then ARCON PAM will Auto-Generate password to
password protect the generated PDF file. The user needs to use this password sent
to his Mailbox to open the PDF file.
Schedule Password
Envelope - Is Enabled
This configuration sets availability of Schedule Password Envelope under
Settings→ Logs→ Scheduler→ Schedule Password Envelope
Disable If Toggle value is 'Disabled', then this option is not available.
Enable If  Toggle value is 'Enabled', then this option is available.
Password Envelope
Protected File
This configuration enables/disables sending password envelope through email or
printing it in .zip format. This file can be decrypted by APEM Tool.
Disable If Toggle value is 'Disabled', the configured password envelope will be sent in .txt
format.
Enable If  Toggle value is 'Enabled', the configured password envelope will be sent in .zip
format.
4.3.7.5.7 Debug Mode
What is Password Debug Mode Setting?
The password debug mode enables system administrators to alter password-related functionality, such as
password changing, storage, and verification, and to inspect any output or logs produced as a result. Identifying
potential security flaws or troubleshooting password management issues will benefit from this.
To navigate, use the following path:
Settings → Password→ Debug Mode
•
•
Print password envelope from ARCON PAM Server Manager >
Manage > Password Manager > Print Password Envelope > Print
Password For APEM Tool.
Password envelope is sent through email when you schedule it
from ARCON PAM Server Manager > Settings > Logs > Scheduler
> Schedule Password Envelope.

## [p342]

www.arconnet.com|Copyright © 2025 342
Field Name Description
ARCOS Password Change
Log In Debug Mode - Is
Enabled
This configuration enables/disables ARCOS Password Change Log in debug mode.
Disable If the Toggle value is 'Disabled', then it disables ARCOS Password Change Log in
debug mode.
Enable If the Toggle value is 'Enabled', then it enables ARCOS Password Change Log in
debug mode.
ARCOS Password Change
Log File Path In Debug
Mode
This configuration is used to specify the file path for the password change log
generated in debug mode. The log file generated is saved at that location under
the DebugLogs folder.
Valid Values  The default value is C;\ and can browse to any drive of the client machine.
4.3.7.5.8 Miscellaneous
What is Password Miscellaneous Setting?
The password miscellaneous feature is a crucial part that helps to guarantee the security and integrity of user
accounts and critical data. It aids in configuring the settings for password storage, password recovery,
password validation, password modification, and many other password-related things.
To navigate, use the following path:
Settings → Password→ Miscellaneous
Field Name Description
Auto Detect Dependent Service
With Common Domain Name and
User Name (For Update Service
Password Only) - Is Enabled
This configuration will enable or disable, auto-detection of dependent
services based on the common Domain Name and User Name of Service
and will update the service password after successfully changing the
password of the same user account.
ARCOSAPI (Password Retrieval)
Requestor Validation - Is Enabled
This configuration when enabled will validate the user(requestor) for
viewing the password of the services.
The first step will be the registration of the User(Requestor) through the
ARCON PAM Web API Registration option in Server Manager.
The second step will be enabling this configuration to validate the
requestor.
The final step will be viewing the password of the services that have been
registered for the User.
Bulk Update Server Password This configuration enables/disables updating the Password of Services
under the Import > Update Server Connections option.

## [p343]

www.arconnet.com|Copyright © 2025 343
Field Name Description
Disable If the Toggle value is 'Disabled', then you cannot update the Password of
Services under Import.
Enable If the Toggle value is 'Enabled', then you can update the Password of
Services under Import.
Automatically Apply Password
Policy When Service is added in
Server Group
This configuration sets whether the Password Policy is applied
to Services newly mapped in the Service Group.
Password policy is applied to Services of a particular Service Type in
a Server Group under LOB/Profile - Default Configuration > LOB/Profile
– Password Policy.
Disable If the Toggle value is 'Disabled', the Password Policy is not applied
to Services newly mapped in the Server Group.
Enable If the Toggle value is 'Enabled', the Password Policy is applied
to Services newly mapped in the Server Group.
Enable Robotic Automation
Process
This configuration enables/disables the Robotic Automation.
Admin account for password
change (windows)
The mentioned ID used in this field will be used in the password change
process.
Store passwords in Split Custody This configuration enables/disables to store privilege identities password
in split custody in ARCON PAM.
Idle session timeout(in minutes)
for Password Vault module
Configure time in minutes for idle session timeout for Password Vault
module
Consider live session for
password change (Database)
when enabled, postpones password changes if there is an ongoing
database session via PAM until the next scheduled change date, and
when disabled, does not verify ongoing database sessions during the
password change process.
4.3.7.5.8.1 ARCON PAM Plugin
Overview
The new ARCON PAM Plugin supports all major browsers, Mozilla Firefox V55 & above, and Google Chrome
V69 & above on Windows for browser independency. To use ARCON PAM application on all browsers, user
shall install ARCON PAM Plugin on his/her system.

## [p344]

www.arconnet.com|Copyright © 2025 344
1.
2.
3.
4.
ARCON PAM Plugin Installation
Access PAM Portal with Given URL (e.g: https://internal.arconpam.com/frmLoginACMO.aspx )
Click on Downloadable option.
Click on first option in windows section and download ARCON PAM Plugin as shown below
Find the downloaded ARCON PAM Plugin Setup.msi file.

## [p345]

www.arconnet.com|Copyright © 2025 345
5.
6.
Double-click on ARCON PAM Plugin Setup.msi file. The ARCON PAM Plugin screen is displayed.
Click Next. Browse and Select the required folder.

## [p346]

www.arconnet.com|Copyright © 2025 346
7.
8.
Click Next. The installer is ready to install ARCON PAM Plugin on your computer.
Click Next to start the installation.

## [p347]

www.arconnet.com|Copyright © 2025 347
9.
10.
11.
1.
2.
ARCON PAM Plugin is being installed.
ARCON PAM Plugin has been successfully installed.
Once the Plugin is installed on the system, User will he able to launch ARCON PAM URL from all the
major browsers.
Temp Folder Permission
ARCON PAM Plugin Temp Permission - Chrome
Goto C:\Program Files (x86).
Right-click on ARCON Solution folder and go to properties.

## [p348]

www.arconnet.com|Copyright © 2025 348
3.
4.
Click on the Security tab and click on Edit.
Click on Add button.

## [p349]

www.arconnet.com|Copyright © 2025 349
5. Type Everyone In the search box and click on Check Names then click OK.

## [p350]

www.arconnet.com|Copyright © 2025 350
6.
7.
Click the Security Tab, select Everyone in the Group or user names:, and then click the Edit… button.
The Permission for ARCON PAM screen is displayed.

## [p351]

www.arconnet.com|Copyright © 2025 351
8. Select all the Allow check-boxes, click the Apply button, and then click the OK button.

## [p352]

www.arconnet.com|Copyright © 2025 352
1.
The user have the complete access to the ARCON PAM Temp.
ARCON PAM
To login into PAM, enter credentials and click on the login button highlighted.

## [p353]

www.arconnet.com|Copyright © 2025 353
2.
3.
4.
After login, you’ll see this page. For choosing LOB of your choice, click on the drop down menu and
choose your respective LOB.
For choosing Service Type, click on the drop down menu and you’ll find all the assigned Service Type for
the user which is logged in.
For easier search process, just type ‘IP Address or Host Name’ of the service to filter out or you can even
Search with the search option.

## [p354]

www.arconnet.com|Copyright © 2025 354
5.
6.
If you tick on the ‘All Services’ box, you’ll see all the services all together.
If you click on the ‘My Favourite’ star button, you can mark your service as a favourite service, for easier
access whenever required.

## [p355]

www.arconnet.com|Copyright © 2025 355
7. By clicking this button, you can access the required service.
4.3.7.6 Alert & Notifications
What are Alerts and Notifications?
The Alerts and Notification feature in ARCON PAM provides alert notifications via email for various activities
performed within the platform. These include alerts for actions such as New User Approved, New Service
Created, New User Added in the group, Command executed on SSH, Invalid Login Attempt, ARCOS Logs,
Service Password Manually Changed, Process started on Windows, Process title on Windows, Critical
Service(s) accessed in Service Group, Failed SMS OTP Authentication, Successful login and logout alert,
Password reset failure, and Failed User Door Access Authentication.
Why need Alerts and Notifications?
Alerts and Notifications enables real-time monitoring of critical actions, helping administrators stay informed
about user activities and system events. By receiving timely alerts, administrators can respond quickly to

## [p356]

www.arconnet.com|Copyright © 2025 356
•
•
•
•
•
suspicious or unauthorized actions, thereby enhancing the overall security and integrity of the ARCON PAM
environment.
The following two modules come under Alert and Notification
Alert and Notification Configuration
Alert Email Template
Custom Email Alert
ARCON PAM Message Board
Configure
Pre Requisite for Alert & Notification
Alert service should be installed and configured in ARCON PAM to receive alerts on email. Alert Service is
installed and configured in ARCON PAM Application or Database Server (EPAM) for sending notifications to
users.
Primarily, before starting Alert configuration, you need to install ARCOS Alert Service  on the application or
database server.
Process Flow Diagram
Following is the process flow diagram for receiving Alerts and Notifications.
•
•
The Administrator having Alert And Notification Configuration  privilege will be able to
configure alerts and Users who will receive an alert notification.
It is mandatory to configure SMTP details in ARCON PAM in order to receive an alert
notification.

## [p357]

www.arconnet.com|Copyright © 2025 357
4.3.7.6.1 Alert & Notification Configuration
What are Alerts and Notifications?

## [p358]

www.arconnet.com|Copyright © 2025 358
1.
2.
Alert and notification configuration is a feature that allows administrators to set up alerts and notifications for
specific events or activities that may indicate a potential security issue. The process to configure a new Alert
and Notification Configuration is explained below.
To navigate, use the following path:
Settings → Alert & Notifications0
Select Alert and Notification Configuration:
Select the Add button to add a new Alert and Notification configuration:
The Administrator having Alert and Notification Configuration privileges in Server’s Privileges will
only be able to configure Alerts and notification.

## [p359]

www.arconnet.com|Copyright © 2025 359
3. From here, we can configure the following Alerts/Notification-
New User Approved: Notification for the recently approved new user in ARCON PAM.
New Service Created: Notification for every new service created in ARCON PAM.
User Added In Group: Notification for every new user added to the group.

## [p360]

www.arconnet.com|Copyright © 2025 360
Command executed on SSH: Notification for command executed on SSH-based service
(command needs to be defined).
Invalid Login Attempt: Notification for every invalid attempt to log in to the application.
ARCOS Logs: Notification for logs viewed.
Service Password Manually Changed: Notification for every service whose password is manually
changed.
Process Started On Windows: Notification for the process started on Windows.
Process Title On Windows: Notification for process title on Windows.
Critical Service(s) Accessed In Service Group: Notification for critical services accessed in the
service group.
Failed SMS OTP Authentication: Notification for failed SMS OTP authentication.
Failed User Door Access Authentication: Notification for failed user door access authentication.
Successful Login Alert: Notification for every successful login.
Successful logout Alert: Notification for every successful logout.
Password Reset Failure: Notification for every Password Reset Failure.
Critical Command Executed on Server: Notification for critical commands executed on the
server.
RDPDB Image Counter Alert: Notification when the RDPDB image count exceeds the threshold
value in the specified time interval.
Service Revoked from User: Notification for revoking of service.
Service Password Expiry Reminder: Notification when the service password is going to expire.
Services Accessed from User Group: Notification when any user from that User Group accesses
the service assigned to them.
The Alerts and Configuration screen contains the following fields:
Field Name Description
Alert/ Notification Select the type of alert or notification.
Mode Select the type of mode used for notification i.e. email.
Object Type Select the type of object.
Operation Select the type of operation.
Service Type Select the type of service.
LOB/ Profile Select the LOB/ profile.
This field is enabled if you select the Alert/ Notification
as ARCOS Logs.
This field is enabled if you select the Alert/ Notification
as ARCOS Logs.

## [p361]

www.arconnet.com|Copyright © 2025 361
Field Name Description
User Group Select the group name of the user.
Service Group Select the service group.
Users Select the name of the user.
Services Select the name of the service.
Command Define the command in SSH.
Threshold Set the threshold value for the alert.
Interval (in min) Set the alert interval in minutes.
Days Prior Set the days prior to which the user will receive the alert
This field is enabled if you select the Alert/ Notification
as User Added In Group.
This field is enabled if you select the Alert/ Notification
as Critical Service(s) Accessed In Service Group and
Password Reset Failure.
This field is enabled if you select the Alert/ Notification
as Command Executed On SSH, Process Started On
Windows, and Process Title On Windows.
This field is enabled if you select the Alert/ Notification
as Command Executed On SSH, Process Started On
Windows, and Process Title On Windows.
This field is enabled if you select the Alert/ Notification
as Service Password Expiry.

## [p362]

www.arconnet.com|Copyright © 2025 362
•
•
4.
Field Name Description
Schedule type Select the schedule type.
Run Once- If the password of the service is going to expire
on 6th of April at 4:00 pm and the Days prior is 5 and
scheduler is Run Once, then the alert will be sent once on
1st April at 4:00 pm.
Daily- If the password of the service is going to expire
on 6th of April at 4:00 pm and the Days prior is 5 and
scheduler is Daily, then the alert will be sent from 1st
April at 4:00 pm till the time the password is not changed;
keeping a difference of 24 hours.
Alert Send To User Select the name of the user to whom the alert has to be sent.
After selecting the user from the Alert Send To User dropdown
list, it will display the mail ID of the respective user in the text
field beside the Alert Send To User dropdown.
Enabled  To enable the alerts.
Between specific time Set the time and date between which alert and notification shall
be received.
Send Alert to Group Admin To send Alert to the Group Admin.
Click on Save to configure Alert and Notification.
This field is enabled if you select the Alert/ Notification
as Service Password Expiry.
For the users to appear in the Alert Send To User list,
their e-mail ID must be configured.
This field is enabled if you select the Alert/ Notification
as New Service Created, Command Executed on
SSH, Service Password Manually Changed, Password
Reset Failure, Service Password Expiry Reminder,
Critical Service(s) Accessed In Service Group, and
Critical Command Executed on Server.
Start the ARCOS Alert Service in services.msc for getting e-mail alerts.

## [p363]

www.arconnet.com|Copyright © 2025 363
5.
6.
7.
For editing, the details of the existing Alert and Notification configuration, click on the existing row and
select the Edit button at the top and make the required changes. Also, you can right-click on the row and
select Edit.
For deleting the existing Alert and Notification configuration, click on the existing row and select the
Delete button at the top and make the required changes. Also, you can right-click on the row and select
Delete.
The Export button will export all the Alert and Notification configuration details in the form .xlsx format.
The Copy button will copy all the details of the table.
4.3.7.6.2 Alert Email Template
What is Alert Email Template?
Alert Email Template feature provides users to notify by email for activities performed in ARCON PAM. The
email template contains basic details about the requests. This feature has a Business Email ID and Business
Mobile Number field in the Manage Users screen. When a new user is created, an email is sent to the user on a
configured email ID.
To navigate, use the following path:
Settings → Alert & Notifications
The Administrator having Alert Email Template privileges in Server’s Privileges will only be able to do
configurations under Alert Email Template.

## [p364]

www.arconnet.com|Copyright © 2025 364
1.
2.
Select Alert Email Template:
Select the Add button to add a new Alert Email Template.
The Alert Email Template screen contains the following fields:
Field Name Description
LOB User has access to make LOB specific templates. Configurations in ARCON
PAM that include LOBs will be sent using this template.
User can select LOB from the dropdown. User can also select
more than one LOB for the template.

## [p365]

www.arconnet.com|Copyright © 2025 365
•
•
•
•
3.
4.
5.
Field Name Description
Request Type User has to select a module for which the template is been created.
Whenever this module is configured in Server Manager then Email is sent to
the respective receiver (Approver/Requestor/End-User/Executor)
User can select below actions under Request Type:
Service Password Request
Service Access
Service Ticket
Critical With Approval
Recipient Type Select Recipient Type:
Approver
The approver is the one who will decide to accept or reject the request based
on the information provided in the email.
Requestor
The requestor is one who requests for accessing a particular entity.
Name Assign a unique name to this template.
Body The user can enter a customized message. This message will be delivered to
the respective receiver.
The body contains features to edit and style the message. From left to right
the icons specification are as follows:
Bold, Italic, Underline, Strike Out Text, Colour Text, Colour Background,
Fonts, Text Size, Left Align Right Align, Adjust, Center Align, Bullets,
Numbered Bullets, Indent, and Dedent.
After updating all the required details, click Save so that the template is created in the Alert Email
Template.
For editing, the details of the existing Alert Email Template, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.
For deleting the existing Alert Email Template, click on the existing row and select the Delete button at
the top and make the required changes. Also, you can right-click on the row and select Delete.

## [p366]

www.arconnet.com|Copyright © 2025 366
6.
1.
2.
The Export button will export all the Alert Email Template details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.6.3 Custom Email Alert
By configuring Custom Email Alert, The administrator can configure email and notifications and can send to the
defined LOB/Profile/User Group/Service Group/Specific USer at a scheduled time.
At the scheduled time, the configured Custom Email Alert is picked up and sends an email according to the
subject and body configured.
To configure the Custom EmailAlert, follow the below path:
Settings > Alerts & Notifications > Custom Email Alert
Click on Add. The following screen is displayed:

## [p367]

www.arconnet.com|Copyright © 2025 367
Refer to the following table to understand the field-level details shown in the preceding screen:
Field Name Description
Name Enter the name of the Email Alert.
LOB/Profile Select the LOB/Profile from the dropdown for which, the alert needs
to be configured.
User Group Based on the selected LOB/Profile, select the User group for which,
the alert needs to be configured.
Service Group Select the Service Group from the dropdown.
Alert Send to User Select the users to which, the alert needs to be sent.
Alert Send to Email IDs Specify the Email IDs of the users on which, the alert needs to be sent
if applicable.

## [p368]

www.arconnet.com|Copyright © 2025 368
3.
4.
a.
b.
5.
1.
Field Name Description
Enabled Tick the checkbox to keep the configured alert active.
Send Alert To Service Group Admin Tick the checkbox if the alert needs to be sent out to the Service
Group Admin as well.
Scheduler Select the required scheduler from the dropdown based on which, the
alert will be sent.
Email Subject Specify the subject of the alert.
Enter Body Enter the message of the respective alert that needs to be sent.
Once all the required fields are entered, click on Save. The alert will be configured and listed in the grid.
To edit/delete the existing alert,
Right-click on the respective alert and click on Edit/Delete.
Select the respective alert and click on the Edit/Delete button located at the top-right corner.
The Export button will export all the Custom Alert Email details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.6.4 ARCON PAM Message Board
ARCON PAM Message Board allows, to configure messages to be displayed on pages after or before login.
To navigate, use the following path:
Settings → Alert & Notifications0
Select ARCON PAM Message Board:
The Administrator having ARCOS Message Board privileges in Server’s Privileges will only be able to
do configuration under the message board.

## [p369]

www.arconnet.com|Copyright © 2025 369
2.
The ARCON PAM Message Board screen contains the following fields:
Field Name Description
Display On Login Page-Popup Window Enable checkbox to receive the message that will be displayed on
Login Page after login.
Display On All Pages After Login Enable checkbox to receive the message that will be displayed on
all pages after login.
Message Settings
Message Enter the message in the Message text field.
Font Size Set the font size of the message.
Between specific time Set the time and date between which message shall be received.
Select the details and click Confirm Changes button to configure the details. The following message
appears:0
The maximum text length of ARCON PAM Message
Board is 1500 characters.

## [p370]

www.arconnet.com|Copyright © 2025 370
1.
4.3.7.6.5 Configure
4.3.7.6.5.1 SMS Gateway Configuration
ARCON SMS gateway server details are used when the notification is sent to approvers for service, ticket, and
password requests. ARCON PAM provides Dual Factor Authentication when the user logs in to Client
Manager. SMS OTP is one of the methods wherein the User receives OTP on the registered mobile number.
OTP is the second factor of authentication.
The SMS gateway configuration allows receiving alerts or notification messages via SMS on the configured
Mobile devices in the following way.
To navigate, use the following path:
Settings → Alert & Notifications → Configure0
Select SMS gateway configuration under Configure.
The Administrator having SMS Gateway Configuration privileges in Server’s Privileges will only be
able to configure values for SMS Gateway Configuration.

## [p371]

www.arconnet.com|Copyright © 2025 371
The SMS Gateway Configuration screen contains the following fields:
Field Name  Description
Enable (checkbox) To enable the configuration.
Enable Binding (checkbox) To enable binding. If it is checked/enabled, it will use the SMPP Gateway
to send OTP to the user.
SMS Gateway URL Define the main URL for SMS gateway.
Success Flag Defines the success flag. It can either be 1, 0, or success depending on the
gateway. It can also be different characters or variables.
Error Flag Defines the error flag. It can either be Error or Invalid Entry. This field is
variable depending on the gateway.
SMS OTP Length Set the Length of the OTP. The valid values are from 2 to 9.
Gateway Username  Enter the gateway Username
Gateway Password Enter the gateway Password
Gateway Sender ID Enter the Gateway Sender ID
Binding IP Enter the Binding IP (Will be accessible if the Enable Binding option is
enabled).
Binding Port  Enter the Binding port (Will be accessible if the Enable Binding option is
enabled).

## [p372]

www.arconnet.com|Copyright © 2025 372
2.
Field Name  Description
SMS OTP Template Set the template message to be displayed.
Username Tag The Tag used in the URL will be replaced by the Gateway’s Username,
which is configured under ‘SMS Gateway Configuration’.
Password Tag The Tag used in the URL will be replaced by the Gateway’s Password,
which is configured under ‘SMS Gateway Configuration’.
Mobile No Tag The Tag used in the URL will be replaced by the User’s Mobile Number,
which is configured in User’s Security Setting under ‘Manage User’.
Message Tag The Tag used in the URL will be replaced by the SMS OTP Template, which
is configured in ‘SMS Gateway Configuration’.
Sender ID Tag The Tag used in the URL will be replaced by the Gateway’s Sender ID,
which is configured in ‘SMS Gateway Configuration’.
SMS OTP Tag Used in configuring OTP Message under SMS OTP Template, which will be
replaced by the randomly generated OTP.
Select the details and Click Confirm Changes button to configure the settings.
4.3.7.6.5.2 Configurations
To navigate, use the following path:
Settings → Alert & Notifications → Configure
Field Name Description
Alert Service Email/SMS Failed Attempts This configuration sets the number of times Alert Service shall
attempt to send an alert on Email or SMS.
Valid Values It ranges from 1-10.
Send Password of ARCOSAUTH Users in
Email Notification
This configuration will send the URL, password, and other
guidelines for the first-time login users in ARCOSAUTH Domain
over an email.
Disable If the Toggle value is 'Disabled', then the first time ARCOSAUTH
user will not receive an email with URL, Password, and
guidelines.
Enable If the Toggle value is 'Enabled', then then the first time
ARCOSAUTH user will receive an email with URL, Password,
and guidelines.
Show My Tags in My Access Page  This configuration will display the My Tags option in My Access
page.

## [p373]

www.arconnet.com|Copyright © 2025 373
•
•
•
1.
Field Name Description
Disable If the Toggle value is 'Disabled', then the My tags option will not
be displayed in My Access page.
Enable If the Toggle value is 'Enabled', then the My tags option will be
displayed in My Access page.
Use append mode for Hardware Token This configuration will enable the use of append mode for the
hardware token
4.3.7.7 Workflow
What is Workflow?
Workflow in ARCON PAM is an approval process where one or more Admins are required to approve changes
or transactions made within the platform. This includes approvals for actions involving users, services, user
groups, and service groups. To enable this process, configuration must be done in the Workflow Approval
Matrix. Additionally, when users raise requests for service access, service passwords, tickets, or to execute
critical commands on a server, these requests can also go through an approval process by configuring the User
Request Approval Workflow.
Why need Workflow?
The Workflow feature is essential for ensuring controlled and secure execution of actions within ARCON PAM.
It enforces a layer of oversight and accountability by requiring administrative approval for critical operations.
This helps prevent unauthorized changes, enhances compliance, and ensures that only verified and approved
activities take place in the system.
The following two sections come under the workflow module
Configure Holidays
Raise Request
Admin Activities
4.3.7.7.1 Configure Holiday
This section monitors the performance of ARCON PAM servers. Using this feature an organization can define a
list of Holidays by selecting a Month, Date, and describing the holiday by adding the Name of the Holiday.
To navigate, use the following path:
Settings → Workflow
Select Configure Holiday:
The Administrator having Configure Holiday privilege in Server’s Privileges will only be able to do
configurations under Configure holiday screen.

## [p374]

www.arconnet.com|Copyright © 2025 374
2.
3.
Select the Add button to add a new Configure Holiday:
The Configure Holiday screen contains the following fields:
Field Name Description
Holiday Name Specify the Holiday Name.
Holiday Date Select the Holiday date.
Enabled If selected, then the command profile will be applicable only between the time range.
If left unselected, then the commands profile will be applicable for the complete day.
Enter the details and click Save, new holiday Is created in Configure Holiday.
Holidays will have a validity of one year and need to be defined manually each
year.
For Example:
Scenario 1: The defined holidays will only by-pass the time and not the days
(Monday to Friday) which are configured. So, if a public holiday falls on a
Saturday or Sunday, the end user will have full access as stated in Scenario 2.
Scenario 2: This configuration has to be set from 12:00 AM to 5:00 PM in
order to restrict commands. So starting 5:00 PM and the next day, being a
working day, restrictions will start from 8:00 AM as defined in Scenario 1.

## [p375]

www.arconnet.com|Copyright © 2025 375
4.
5.
6.
For editing, the details of the existing Configure Holiday, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.
For deleting the existing Configure Holiday, click on the existing row and select the Delete button at the
top and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the Configure Holiday details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.7.2 Raise Request
The raise request procedure is a crucial step because it enables administrators to ask for specific security-
related actions or policies to be implemented in order to safeguard sensitive data and systems. Organizations
can maintain a strong security posture by adhering to a defined protocol for raising requests, ensuring that
security-related activities are evaluated and approved in a consistent and transparent manner.
To navigate, use the following path:
Settings → Workflow → Raise Request0
Field Name Description
Reference Details Mandate while
raising Service Access Request- Is
Enable
This configuration helps in setting the reference parameters that will be
visible on the ACMO→ Raise Request→ Service Access Request screen.
Disable If the Toggle value is 'Disabled', then the Reference type and Reference
Detail fields will not be visible in Settings.

## [p376]

www.arconnet.com|Copyright © 2025 376
•
•
•
•
•
•
•
•
1.
Field Name Description
Enable If the Toggle value is 'Enabled', then the User can set the Reference type
and Reference Details fields in Settings, which will reflect on ACMO→
Raise Request→ Service Access Request screen.
Reference Type Enter reference type
Reference Details Enter reference details
Allow Raising Password Request
For All Services In Group
The toggle allows users to raise Service Password Requests for all
services in a Service Group, including both assigned and unassigned
services.
Disabled If the setting is off (default behavior), services will be displayed based on:
Line of Business (LOB)
Group mapping
User-service assignment
Enabled If the setting is on, services will be displayed based on:
Selected LOB
User and Service Group mapping (assigned and unassigned)
The user should be mapped to the User Group
Service to Service Group mapping
The user group and service group mapping.
4.3.7.7.2.1 User Request Approval Workflow
This section helps you to configure approval levels for the request raised by the User for service access, service
password, service ticket, and critical command. The request raised by Users from the Client Manager shall be
sent for approval based on the approval levels configured in the workflow matrix. Therefore, it provides a
definite audit trail and proper flow of events, which are required to be monitored closely.
To navigate, use the following path:
Settings → Workflow → Raise Request
Select User Request Approval workflow under Raise Request:
When this configuration is updated, an entry will be logged in
the Audit Logs under the "Modified" operation type, capturing
both the old and new values. If alerting is enabled for Audit Log
changes, an alert will be triggered when this setting is modified.
The Administrator having User Request Approval Workflow privileges in the Server’s Privileges will
only be able to configure user request approval Workflow

## [p377]

www.arconnet.com|Copyright © 2025 377
2. Select the Add button to raise a new request:

## [p378]

www.arconnet.com|Copyright © 2025 378
•
•
•
•
•
•
•
•
The User Request Approval workflow contains the following fields:
Field Name Description
Description Specify the name or details of the approval matrix to be created.
Request type Select the type of request to be raised:
Service Password: It raises a request to view the password of a
particular service.
Service Access: It raises a request to access a particular service.
Service Ticket: It raises a ticket request which states the requested
services.
Critical Command: It raises a request to fire a critical command.
Script Execution: It raises a request to execute a script.
Access type Select the Access type:
Permanent: It raises Permanent and full access request of the service
to the user.
One time: It raises a One-time request for the service to the user.
Time Based: It raises requests based on a specified duration of time by
the user.

## [p379]

www.arconnet.com|Copyright © 2025 379
Field Name Description
Priority Configure Priority Levels for Workflow. Based on the priority configured, the
Workflow would be applied.
For Example, if User 1 raises a Service Access Request, now User 1 belongs to
both Group 1 and Group 2, mapped to Workflow 1 and Workflow 2
respectively. However, since the priority that is set for Workflow 2 is higher,
the highest priority level workflow would be applied.
LOB/ Profile Select the LOB/Profile.
Service Group Select the Service group from the drop-down.
User Group Select the user group from the drop-down.
Approval Levels Select the number of approval levels to approve the request.
If LOB Wise Workflow Configuration - Is Enabled Configuration is
enabled in Settings, then only LOB/Profile will be displayed in the
LOB/Profile drop-down list. Whereas, if it is disabled, then the All
LOB option will be displayed along with LOBs in the drop-down list.
Multiple service groups can be selected. A search option can be used
to filter the dropdown values.
Multiple user groups can be selected. A search option can be used to
filter the dropdown values.
•
•
It can be set to a maximum of 5 users and a minimum of 0
users.
0 Approval Level can be configured only for Service Password
and Service Access Requests. If the Approval level is
configured to 0, then it is mandatory to specify an email ID for
notification. For any service password and service access
request by the User, a service details notification will be sent
to the configured email ID.
Enter the email ID in the Notify Email Only for 0
Approval Level text box.

## [p380]

www.arconnet.com|Copyright © 2025 380
Field Name Description
Ad hoc approver If the Request type is Service access and the approval level is more than 0,
the ad hoc approver checkbox will be visible. Clicking this checkbox ad hoc
approval list is populated at the bottom where the admin can set Ad hoc
approvers. The purpose of this configuration is that approvers can simply
forward the service access request if they are not sure if they have approved
or rejected the request on ACMO.
Between Specific time Select the specific time with hours and days, to enable the workflow matrix
between the selected time.
Specific Service IP address Select and specify the service IP address to apply the created matrix to the
specific IP only.
Specific Privileged Account Select and specify the service IP address to apply the created matrix to the
specific IP only.
Specific User ID Select and specify the user ID to apply the created matrix to the specific user
ID only.
Approvers Search and select the approvers for the workflow.
Send SMS notification to
Approver
Enabling the checkbox SMS is sent to the approver for the request.
Show password on request
window
Enable the checkbox to see the password on the request window
Send Email Notification(s) to
Requester
Enable the checkbox to get an email notification for the raised request.
Enabled Enable the matrix.
The Ad hoc approvers configured here by the Admin will be visible
under ACMO to the approvers when they select the Forward option.
The IP refers to the destination server/service accessed via ARCON
PAM.
The account refers to the destination server user account accessed
via ARCON PAM.
The user ID refers to the user’s login in ARCON PAM.
For the mails, SMTP configuration under ARCON PAM has to be
configured prior and ARCOS Alert Service has to be running on
ARCON PAM server.

## [p381]

www.arconnet.com|Copyright © 2025 381
3.
4.
5.
6.
7.
Click on Save to save all the changes and the user request approval workflow has been set.
For editing, the details of the existing approval workflow, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.
To delete the existing request approval workflow, click on the existing row, select the Delete button at
the top, and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the user request approval workflow details in the form .xlsx format.
The Copy button will copy all the details of the table.
4.3.7.7.3 Admin Activities
4.3.7.7.3.1 Workflow Approval Matrix
This section helps you to configure approval levels for each transaction or operation performed by the
Administrator. The transactions between Users, services, User group, and service group shall be sent for
approval based on the approval levels configured in the workflow matrix. Therefore, it provides a definite audit
trail and proper flow of events, which are required to be monitored closely.
To navigate, use the following path:
The Administrator having ARCOS Workflow Approval Matrix privilege in the Server’s Privileges will
only be able to configure the workflow approval matrix.

## [p382]

www.arconnet.com|Copyright © 2025 382
1.
2.
Settings → Workflow → Admin Activities
Select Workflow Approval Matrix under Admin Activities.
Select the Add button to create a new matrix:

## [p383]

www.arconnet.com|Copyright © 2025 383
The Approval Matrix screen contains the following fields:

## [p384]

www.arconnet.com|Copyright © 2025 384
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
Field Name Description
Object Type Select the type of object. The valid values are:
User Transactions: Used for the creation, deletion, and modification of
Users.
Service Transactions: Used for the creation, deletion, and
modification of Services.
Transaction Between User and User Group: To map User(s) with their
respective User Groups.
Transaction Between Service and Service Group: To add or remove
services to/from their respective Server Group.
Transaction between User And Service: To assign or revoke Services
to/from Users.
Transaction Between User Group And Service: To map or remove
User Group to/from Service Group and vice versa.
Video Log: Used to view the historical video logs.
Operation Type Select the type of operation. The valid values are:
Created
Modified
Deleted
Assigned
Revoked
View
LOB/ Profile Select the LOB/Profile.
Service Group Select the service group.
User Group Select the user group.
Description Specify the description for the selected object type.
Approver Levels Select the levels of approval for the selected object type.
The valid values are:
You can select up to 5 levels of approval.

## [p385]

www.arconnet.com|Copyright © 2025 385
3.
4.
5.
Field Name Description
Enabled Enable the configuration for approval.
Between Specific Time To set the specific time for approval.
Approvers Search and select the approvers for the workflow.
Click on Save to save all the changes.
For editing, the details of the existing workflow matrix, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the row and select Edit.
For deleting the existing workflow matrix, click on the existing row, select the Delete button at the top
and make the required changes. Also, you can right-click on the row and select Delete.

## [p386]

www.arconnet.com|Copyright © 2025 386
6.
1.
2.
The Export button will export all the workflow approval matrix details in the form .xlsx format. The Copy
button will copy all the details of the table.
Approve/Reject new users created
On raising a request by the user, the approvers will get the following mail in their inbox.
To approve/reject a request, the approver can reply to the above mail received in their inbox.
The approvers will have to reply with the content #Approve# or #Reject# to approve/reject the request.
Once the workflow is created as per the Workflow Approval Matrix, the request is sent to the
approver(s) through email for approval.

## [p387]

www.arconnet.com|Copyright © 2025 387
4.3.7.7.3.2 Admin Activities Global Configurations
To navigate, use the following path:
Settings → Workflow → Admin Activities
Field Name Description
User Request Approval Workflow - Is
Enabled
This configuration sets the availability of the User Request
Approval Workflow option.
Disabled If the Toggle value is 'Disabled', this option will not be available for
configuration.
Enabled If the Toggle value is 'Enabled', this option will be available for
workflow configuration.
CAPTCHA Validation In ACMO Service
Access And Password Request - Is
Enabled
This configuration enables/disables Captcha Validation in CM
while raising Service Access and Password View Request.
Minimum Length of Comment Field
While Rejecting Any Workflow
This configuration sets the minimum length of characters under
the comment field which is mandatory to be entered by Admin ID
while rejecting Service Access, View Password requests, or any
Workflow.
Valid Values It ranges from 0-99.
Minimum Length of Comment Field
While Approving Any Workflow
This configuration sets the minimum length of characters under
the comment field which is mandatory to be entered by Admin ID
while rejecting Service Access, View Password requests, or any
Workflow.
Valid Values  It ranges from 0-99.
LOB Wise Workflow Tracker - Is Enabled This configuration sets whether Workflow details should be
displayed LOB wise or for all.
Disable If the Toggle value is 'Disabled', then the “All” option will be
available in LOB/Profile drop-down.
Enable If the Toggle value is 'Enabled', then only LOBs will be available for
selection in the LOB/Profile drop-down in Server Manager >
Manage > Workflow Tracker > User Service Request Workflow
Tracker tab.

## [p388]

www.arconnet.com|Copyright © 2025 388
1.
Field Name Description
Critical With Approval (Minutes) This configuration sets the time in minutes post which critical
command execution request would auto terminate when the
defined duration is expired.
When the user tries to execute a critical command on the Server
accessed from CM > Connections, a count down for the approval
process is displayed. That count downtime is defined in this
configuration
Valid Values  It ranges from 5-30.
4.3.7.8 Session
4.3.7.8.1 Time Control
What is Application Configuration?
Application Configuration on the web enables the Administrator to design local and domain user account
policies. The password policy and account threshold values configured are applicable to users created in
ARCON PAM. The user’s login can be managed according to the policy designed here. This configuration helps
to set the session time out for the Target Server session, define session log time to capture images, set the
password policy for the local users, and set the accessibility control for User’s ids hence this resides under the
Session tab.
To navigate, use the following path:
Settings → Session → Time Control
Select the Application Configuration under Time Control:
The Administrator having Application Configuration privilege in Server’s Privileges will only be able to
configure values.

## [p389]

www.arconnet.com|Copyright © 2025 389
The Application Configuration screen contains the following buttons:
Field Name Description
Session Lock Out
(Minutes)
It is a Global Session Lockout time in minutes. If the value is set to 30 minutes and a
user’s RDP session remains idle for 30 minutes, it will get locked.
Log Enable Enables the video log globally. ARCON PAM checks for every 250 milliseconds for
the new screen. If it is set to 1000 milliseconds, it will check for a new screen after
every 1 second.
Note: By default, Log is enabled.
Session Log Time Select the time interval in minutes to capture images of the Target Server session.
Local User Account Policy:
Select the password policy for the ARCON PAM Local Users.
Password Length Set the length of the password.
Lower Case Characters Select the number of lower case characters in the password.
Numeric Characters Select the number of numeric characters in the password.

## [p390]

www.arconnet.com|Copyright © 2025 390
Enforce password
Change After Day(s)
Users can apply similar policies as used in their Organization’s Active Directory.
Set the number of days after which the password should be changed.
Upper Case Characters Select the number of upper case characters in the password.
Symbol Characters Select the set number of symbol characters in the password.
Enforce Password
History
The value set in this field applies that Users cannot use the same password for the
next time. If the value in this field is set to 6, the user cannot use the passwords for
the next 6 times. Every time a new password should be used for the defined
number of times.
Password Dictionary
Check
Select this value for ARCON PAM to check Password Dictionary while changing
the password of Local User or creating new local User in ARCON PAM.
Password Equal
Username Check
Select this option if you do not want to set the same username and password.
Character Allowance (ACMO-Login Form)
Special Characters
Allowed in Username
Field
Enter the character which will be allowed in the Username.
Special Characters
Allowed in Password
Field
Enter the character which will be allowed in the Password.
Account Threshold values
Sets accessibility control for all active User IDs in ARCON PAM. The Admin ID can set the maximum
number of days an account will be in an enable state, set lockout attempts, and reset lockout time.
Dormancy Days(s) A User ID is added to the Dormancy Days list if the user does not login to ARCON
PAM for the configured number of days.
Example: If the dormancy period is set to 30 days and a user did not log into the
application during this period, then ARCON PAM will become dormant to that user
and the user will be added in the dormant list under Manage Users. The Users in
Dormant List are not allowed to login until the Administrator does not change
Account Status to Active for that user.
Lockout Attempt(s) The value set in Lockout Attempts is considered to Lock local User ID’s in ARCON
PAM.
Example: If Lockout Attempts is set as 3 and User makes 3 Invalid Attempts to login
into Client Manager Online; then his ID gets locked and it is added to Lockout Users
List under Manage Users. Such users will not be able to Login into ARCON PAM
even with the correct password.
The period of dormancy days have increased up to 366 days (1 Year).
Users can set dormancy days up to 366 days.

## [p391]

www.arconnet.com|Copyright © 2025 391
2.
Lockout Attempt(s) for
Domain Users
The value set in Lockout Attempts for Domain Users is considered to Lock domain
User ID’s in ARCON PAM.
Example: If Lockout Attempts for Domain Users is set as 3 and User makes 3
Invalid Attempts to login into Client Manager Online; then his ID gets locked and it
is added to Lockout Users List under Manage Users. Such domain users will not be
able to Login into ARCON PAM even with the correct password.
Reset Lockout Minute(s) The value set in Reset Lockout Minutes is considered to Reset Locked User IDs in
ARCON PAM.
Example: If the value in Reset Lockout Minute(s) field is set as 15, after 15 Minutes
User ID will be unlocked. This user can then login to ARCON PAM.
If the value in this field is set to zero, ARCON PAM will not reset locked users. In
this case, the Administrator of ARCON PAM needs to change Account Status to
Active for that user under Manage Users.
Select/Enter the details and click Confirm Changes to enable the configuration.
4.3.7.8.2 Time Control Configuration
To navigate, use the following path:
Settings → Session → Time Control
Field Name Description
Max Session(s) Per User
(0 Is Unlimited)
This configuration sets the maximum number of CM sessions that can be taken by a
User ID at a time.
Valid Values The valid range is 0-999.
Min Time Wait For New
User Session - If Exceeds
This configuration sets the minimum time to wait before initiating a new CM
session when other than zero value is defined in Max Session(s) Per User (0 Is
Unlimited) configuration.
If value defined in Max Session(s) Per User (0 Is Unlimited) is ‘1’ and user logs in
into CM and without logging out closes the browser, then he cannot log in to CM
with same User ID from another system until the time defined in Min Time Wait
For New User Session - If Exceeds has expired.
Valid Values It ranges from 0-999.
AWM Session Timeout
(Minutes)
This configuration sets the time in minutes for Workflow Manager Session
Timeout. The Workflow Manager will log out if keep idle for the configured number
of minute
Note: The Workflow Manager link is sent to Approver's email for approving/
rejecting requests such as service access, service password, user transaction, and
so on.
Valid Values It ranges from 0-9999.

## [p392]

www.arconnet.com|Copyright © 2025 392
Field Name Description
Max Hours For Service
Session Duration
This configuration sets the time in hours to be made available for selection while
raising a request for Service Access.
Valid Values It ranges from 0-999.
Auto Terminate Session
If Session Duration
Expired (Minutes)
This configuration sets time in minutes post which Session would auto terminate
when defined duration in service access request has expired.
When a Time Based or One Time session is accessed from My Services (Client
Manager > My Access > My Services) and defined duration in request has expired, a
window is displayed for requesting session extension. This window is displayed for
a defined time which displays as a count down. The maximum minutes to be
displayed as count down are configured in this configuration.
Valid Values It ranges from 0-999.
Maximum Number of
Service Session(s) Per
User (0 is Unlimited)
This configuration enables/disables the feature of defining the maximum number
of connections a user can create at global level.
4.3.7.8.3 UI Control
We also need to set the UI features for capturing the sessions.
To navigate, use the following path:
Settings → Session → UI Control
Field Name Description
ARCOS Window Min
Width
This configuration sets minimum Width of ARCON PAM window.
Valid Values It ranges from 600-800.
ARCOS Window Min
Height
This configuration sets minimum Height of ARCON PAM window.
Valid Values It ranges from 450-600.
Terminate Session
Button On Unlock
Session - Is Enabled
This configuration enables/disables the display of “Terminate Session” button on
the Unlock Session window.

## [p393]

www.arconnet.com|Copyright © 2025 393
1.
Field Name Description
Client Session Window
Title Order
This configuration will allow users to rearrange name in the title bar for service
session.
Valid Values One can mention at least these fields IP Address, User, Service Type and a
maximum of IP Address, User, Hostname, DBInstance, Service Type
Disable Snipping Tool -
Is Enable
This configuration enables/disables Snipping Tool on the Windows RDP connection
established from Client Manager.
Disable If Toggle value is 'Disabled', then enable the snipping tool on Server.
Enable If Toggle value is 'Enabled', then it disables the snipping tool on Server.
Launch Putty FullScreen
Mode - Is Enabled
This configuration sets whether putty will open in full screen or minimized mode
when you connect from Client Manager.
Note: This configuration is applicable to SSH Linux services with <PTY> tag in the
Parameter field (field 4).
Disable If Toggle value is 'Disabled', then putty will be opened in minimized mode.
Enable If Toggle value is 'Enabled', then putty will be opened in full screen.
4.3.7.9 Domain
What is Domain Configuration?
Domain Configuration allows configuring different domains. A particular domain will only be visible on the login
screen if it is active. The configured domain can be disabled. To disable all the logins for a particular domain, the
configuration has to be disabled. Once the configuration is disabled, users will not be allowed to log in to
ARCON PAM. User authentication is done by validating details in the domain server. ARCON PAM can also
authenticate users using multiple domain servers.
To navigate, use the following path:
Settings → Domain → Configure
Select Domain Configuration and the following screen is displayed:
The Administrator having Domain Configuration privileges in Server’s Privileges will only be able to
configure values for the domain.

## [p394]

www.arconnet.com|Copyright © 2025 394
2. For adding a new domain select the Add button:
The Domain configuration screen contains the following fields:
Field Name  Description
Protocol Type Select authentication type as ARCOSAUTH, LDAP, LDAP SSL, Azure AD
OAuth, or SAML Auth as available in the dropdown list.

## [p395]

www.arconnet.com|Copyright © 2025 395
3.
4.
Field Name  Description
Domain Server Enter the Domain Server IP Address. If there are multiple AD accounts in
an organization, use ~ to separate multiple IP addresses.
Domain Name  Enter the Domain Name.
Domain Extension Enter the extension of Domain.
Protocol String In LDAP, the LDAP string can be configured. If the LDAP string is enabled,
ARCON PAM will use the configured Protocol String, such as Domain
Server, Domain Name and Domain Extension to communicate the Domain
Server.
Organizational Unit Enter the name of the Organization Unit to which it shall belong.
Account Type Select the type of account for which the domain is configured i.e Privileged
account or Login account
Client ID Enter the Application (client) ID generated from the Microsoft Azure
account.
Tenant Info Enter the Directory (tenant) ID generated from the Microsoft Azure
account
Redirect URI Enter the same URI mentioned in the Redirect URIs section of the
Microsoft Azure account
Enabled  Enable the configuration.
Enter the details and click Save, a domain is configured in Domain Configuration.
For editing the details of the existing Domain, click on the existing domain and select the Edit button at
the top and make the required changes. Also, you can right-click on the domain and select Edit.
Register ARCON PAM application in Microsoft Azure, to
generate Client ID, Tenant Info, and Redirect URL
When the Protocol Type is selected as “LDAP” the Protocol String field is enabled to enter text, and
when the Protocol Type  is selected as “LDAP SSL” then the Protocol String field is disabled
streamlining the configuration process and reducing the chance of errors.

## [p396]

www.arconnet.com|Copyright © 2025 396
5.
6.
7.
For deleting the existing Domain, click on the existing domain and select the Delete button at the top
and make the required changes. Also, you can right-click on the domain and select Delete.
Right-click the domain and click Set Domain User Details. The Cross Domain Authorization dialog box
appears.
The Domain configuration screen contains the following fields:
Cross Domain authorization is set when users have to be created belonging to ARCOS domain, with
some credentials to authenticate with another domain. The user using for Cross-Domain
Authentication should be a part of the domain and should not have a password expiry. It is
recommended to be a service account.

## [p397]

www.arconnet.com|Copyright © 2025 397
8.
9.
•
•
The Cross Domain Authorization dialog box appears:
Field Name Description
User ID Enter the User ID.
Password  Enter the Password.
Domain Name Enter the Domain Name.
The User ID and Password are to be entered once. When validating a user or creating a new user of that
particular domain, it will not prompt for the password.
The Export button will export all the template details in the form .xlsx format. The Copy button will copy
all the details of the table.
4.3.7.10 Ticket
This section includes the following topics:
Service Reference Template
Service Type
4.3.7.10.1 Service Reference Template
What is Service Reference Template?
Service Reference Template is used to configure templates. Once the service reference template is configured,
the user will be asked for the reference to access any service, such as Ticket Number, DC Governance Case ID,
Tech flow Case ID, or Form Case ID. The template can be modified as per the admin’s requirement. The DC, TF,
and FC are the prefixes defined by the admin and will be displayed in Audit Trails to identify the type of

## [p398]

www.arconnet.com|Copyright © 2025 398
1.
2.
3.
reference details the log refers to. You can also define predefined templates based on their service types. The
details captured while accessing any service are displayed in ‘Service Logs’ as a part of a comprehensive audit
trail to correlate with the integrated CMS/TS Tool.
To navigate, use the following path:
Settings → Ticket → Template0
Select Service Reference Template under Template. The following screen is displayed.
Select the required options from the left pane and click Confirm Changes. The selected options will be
displayed while accessing the Service.0
Select the LOB/Profile from the LOB/Profile drop-down list and select Is Enabled? Checkbox to enable
the Service Reference Template.
Below is the detailed description of fields under LOB/Profile Configuration:
Field Name Description
Validation If ‘Validation?’ is enabled, ARCON PAM will send the UserID and Reference Ticket Number to
the CMS/TS for validation. On successful validation, it will further give access to the target
server or display the appropriate message sent by the CMS/TS.
IP Address If ‘IP Address?’ is enabled, ARCON PAM sends the UserID, Reference Ticket No. & Requested
Server IP Address to the CMS/TS for validation. On successful validation, it further gives
access to the target server or displays the appropriate message sent by the CMS/TS.
The Administrator with Service Reference Template privileges in the Server’s Privileges can
only configure templates.

## [p399]

www.arconnet.com|Copyright © 2025 399
4.
5.
6.
Field Name Description
Allow Max
Attempts
If the attempts are set to a particular value, the end-user can use the Reference Ticket Number
only for the number of times it is set.
Reference
Method
(URL)
Enter the URL (Web Service Call) so ARCON PAM can communicate with CMS/TS.
Click Confirm Changes to save settings.
Example:
When the administrator enables this validation and the user tries to access any Service, ARCON PAM
sends the User ID, the Ticket / Reference Details entered by the user, and the IP Address of the Server
being accessed to the Change Management System / Ticketing System by calling the Reference URL
configured above. If validation is successful, the user receives access to the server. If unsuccessful, an
appropriate Error Message from the Change Management System will be populated to the end-user.
Click Predefined Template to configure the templates Service Type wise.
The following screen is displayed when you click Predefined Template. It displays the list of existing
Predefined templates.
You need to select the Option Other checkbox and click Confirm Template. The details configured in
the predefined template option will be displayed in the Option Other field when you access the Service
from Client Manager.

## [p400]

www.arconnet.com|Copyright © 2025 400
7.
8.
To add a new template, select the service type, add the Template Description, and select the Enabled
option. Click Save to add the template or Clear to clear all the details.
Below is the detailed description of fields under Service Reference Predefined Templates:
Field Name Description
Service Type Select the Service Type.
Template Description Enter the template description.
Enabled  Select the checkbox to enable visibility of this template.
To edit the details of the existing predefined templates, click the existing ones and then click the Update
button at the top and make the required changes. Also, you can right-click on the row and select Edit.

## [p401]

www.arconnet.com|Copyright © 2025 401
9.
10.
Select the predefined templates and then click the Delete button at the top to delete the predefined
templates. Also, you can right-click on the row and click Delete.
The Close button closes the page and returns to the former page.

## [p402]

www.arconnet.com|Copyright © 2025 402
11.
12.
1.
2.
Click the Export button to export all the server template details in the form .xlsx format.
Click the Copy button to copy all the table details.
4.3.7.10.2 Service Type
4.3.7.10.2.1 Server Reference / Call log
The Server Reference / Call Log feature on the web enables a confirmation message box, which prompts the
user to enter the ticket number and the reason for accessing a particular service in Client Manager.
To navigate, use the following path:
Settings → Ticket → Service Type
Click on the Server Reference/Call Log under Service Type:
Right-Click on the required Service Type then click the Ask Before Accessing Server option.
The Administrator having  Server Reference / Call Log privileges in Server’s Privileges will only be able
to enable confirmation message box.

## [p403]

www.arconnet.com|Copyright © 2025 403
3.
4.
5.
The Ask Server Reference / Call Log? column status will change from No to Yes.0
Click the Export button to export all the Service Reference or Call Log details in .xlsx format.
Click the Copy button to copy all the details of the table.
4.3.7.11 Logs
What are Logs?
Logs capture all the activities performed in ARCON PAM with detailed information. It provides an audit trail for
transactions performed in Server Manager. It also provides detailed information about services accessed
through ARCON PAM.
This section includes the following topics:

## [p404]

www.arconnet.com|Copyright © 2025 404
•
•
•
•
•
LOB Wise Log Archival Settings
Image Quality
Capture
Archival Service
Scheduler
To navigate, use the following path:
Settings → Log
Field Name Description
Reference Detail Required For
Audit Trail - Is Enabled
This configuration enables/disables prompting Admin User to enter
reference details for transactions performed in Advanced Configuration
and User and Service Management.
Disable If Toggle value is 'Disabled', then ARCON PAM will not prompt Admin
User for reference details against which the change is being performed.
Enable If Toggle value is 'Enabled',  then ARCON PAM will prompt Admin User
for reference details against which the change is being performed.
Enable Video Log This configuration enables/disables video logs for all service types under
Settings → Log → Capture→ Modify Service type→ Enable/Disable
service parameter field.
Disable If Toggle value is 'Disabled', then video logs for all service types are
disabled.
Enable If Toggle value is 'Enabled', then video logs for all service types are
enabled.
Enable Text Log This configuration enables/disables text logs for all service types under
Settings → Log → Capture→ Modify Service type→ Enable/Disable
service parameter field.
Disable If Toggle value is 'Disabled', then text logs for all service types are
disabled.
Enable If Toggle value is 'Enabled',  then text logs for all service types are
enabled.
4.3.7.11.1 LOB Wise Log Archival Settings
LOB Wise Log Archival Settings will enable users to store the video logs LOB-wise. The videos can be stored on
a shared folder or on Web Dav.
The Administrator having LOB Wise Log Archival Setting privilege in Server’s Privileges will only be
able to configure details in LOB Wise Log Archival Setting section.

## [p405]

www.arconnet.com|Copyright © 2025 405
1.
2.
To navigate, use the following path:
Settings → Log
Select LOB Wise Log Archival Settings.
Click the Add button to add a new LOB Wise Log Archival Setting:
The LOB Wise Log Archival Settings screen contains the following fields:
Field Name Description
LOB Profile Select the LOB for which the Log staging settings are to be set.
Log Viewer Web Enable Log Viewer Web to enter the Log Web URL.

## [p406]

www.arconnet.com|Copyright © 2025 406
•
•
3.
4.
5.
Field Name Description
Log Web URL This is the URL of the log web viewer play website hosted on IIS. This URL
will allow you to play videos.
Archival Video Storage  Select the storage
Shared Folder
Web Dav
Web Dav URL This is the URL of ARCOS UserAccessLogViewer Website hosted on IIS.
This URL is used to store video.
The URL should be in the following format:
IP Address:Port/ARCOSLogManagerServiceLog_Archived
User Name Enter a user name of the server where user access log viewer is hosted
Password Enter the password of the above user name
Domain Enter the Domain.
Shared Folder Path Enter the path of the Shared folder.
Enter the details and click the Save button to create a new LOB Wise Log Archival Setting.
For editing, the details of the existing LOB Wise Log Archival Setting, click on the existing row and select
the Edit button at the top and make the required changes. Also, you can right-click on the row and click
Edit.
For deleting the existing LOB Wise Log Archival Setting, click on the existing row and click the Delete
button at the top and make the required changes. Also, you can right-click on the row and click Delete.

## [p407]

www.arconnet.com|Copyright © 2025 407
6.
7.
Click the Export button to export all the LOB Wise Log Archival Setting details in the form .xlsx format.
Click the Copy button to copy all the details of the table.
4.3.7.11.2 Image Quality
The entire video is a compilation of images captured in the session established by the administrator. The image
quality defines the quality of the images which will be captured. The quality is configurable and the size of a
video session is determined by the quality of the image which is selected. This section helps you with Image
Quality configurations in video logs.
To navigate, use the following path:
Settings → Logs → Image Quality
Field Name Description
ARCOS Video Log Image
Config - Is Enabled
This configuration enables/disables ARCON PAM Video Log Image
Configuration.
ARCOS Video Log Image
Width
This configuration sets Width of Image in Video Log.
Valid Values  The valid range is 0-1920.
ARCOS Video Log Image
Height
This configuration sets the Height of Image in Video Log.
Valid Values The valid range is 0-1080.
If StagingLogServer is True, then images are picked from the path configured in URL field of Staging
Log Server in Server Manager and archived videos are stored in the path configured for Web Dav URL
of LOB Wise Log Archival Settings in Server Manager.

## [p408]

www.arconnet.com|Copyright © 2025 408
Field Name Description
ARCOS Video Log Image
Compression - Is Enabled
This configuration enables/disables ARCON PAM Video Log Image
Compression
Disable If Toggle value is 'Disabled', then it disables ARCON PAM Video Log Image
Compression.
Enable If  Toggle value is 'Enabled', then it enables ARCON PAM Video Log Image
Compression.
ARCOS Video Log Image
Quality
This configuration sets the Quality of Image in ARCON PAM Video Log in
percentage. e.g. 50% compression
Valid Values The valid range is 0-100.
ARCOSSIEMConnectorService
- ARCOS Event ID From SIEM
This configuration sets the ARCON PAM Event ID that is defined in ARCON
PAM SIEM Connector Service.
Valid Values Failed Login Attempts: This Event ID represents the invalid logon attempts
in ARCON PAM.
Service Access: This Event ID represents the individual servers accessed by
any ARCON PAM user.
Service Command This Event ID represents the command and informs you
about the particular command that is fired in the session.
Password View: This Event ID contains the information about the level of
user who has requested and approved the password, time of the password
request, device for which the password request is sent, and so on.
Password Change: This Event ID is a password change service. It consists of
information about the password that is printed on the server.
Service Password Envelope Print: This Event ID consists of the information
about the envelope printing and password printing. There are 10 levels of
printing status.
ARCOS Log: This Event ID represents the all generic ARCON PAM logs
(They are Object type and Operation Type).
4.3.7.11.2.1 File Naming Template
What is File Naming Template?
Organizations usually have tons of files, and if the filenames are not consistent then searching and retrieving
the file becomes an uphill task. Thus we have a File Naming Template which sets the standardized format for
the files once they are downloaded. This naming convention ensures that the team and collaborators can
discover, manage, and access the file easily as and when needed. The order of selection of these configurations
forms a template. The configurations under this template include User Id, User Name, Machine details, Service
Type, Service IP, Service hostname, Service User Name, Service DB Instance, Service Port Number, Connection

## [p409]

www.arconnet.com|Copyright © 2025 409
1.
2.
•
•
•
type, Description 1, Description 2, Description 3, Service Group, User Group, LOB,  Task/Incident number,
Task/Incident Description, and Log fileName.
To navigate, use the following path:
Settings → Log → Image Quality
Select File Naming Template under Image Quality.
Select the Add button to create a new template:
The File Naming Template contains the following fields:
Field Name Description
Module Name Select the module for which the template should be set
Video Logs
Password Envelope
PDF From Logs

## [p410]

www.arconnet.com|Copyright © 2025 410
3.
4.
5.
1.
Field Name Description
File Name Format Select the configurations one by one, the naming template is formed.
Example- If the admin wants the filename of the logs to be in accordance with the
date format (yyyy-mm-dd) followed the UserId and LOB. The checkboxes are
selected in this way- Year, followed by Month, Day, DateTime, UserID, LOB.
Check box Enable the checkbox to use the same file name format for the archived video logs
on server
Click on Save to save all the changes and the File Naming Template has been set.
For editing, the details of the existing template click on the existing row and select the Edit button at the
top and make the required changes. Also, you can right-click on the row and select Edit. Similarly, for
deleting the existing template, click on the existing row and select the Delete button at the top and make
the required changes. Also, you can right-click on the row and select Delete.
The Export button will export the File Naming Template details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.11.3 Capture
What is Log Manager Service?
Log Manager Service configuration allows ARCON PAM to capture images during session recording for any
GUI-based access taken by the User. The images are transferred to Database Server on a real-time basis. This is
a one-time configuration wherein the width and height of the image, and path of the storage server to retain
logs are configured as per the company’s policy.
To navigate, use the following path:
Settings → Logs → Capture
Select the Log Manager Service under Capture.
This checkbox is only applicable for the Video Logs.
The Administrator having Default Configuration and Log Manager Service privileges in Server’s
Privileges will only be able to configure Log Manager Service.

## [p411]

www.arconnet.com|Copyright © 2025 411
•
•
•
2.
The Log Manager Service screen contains the following fields:
Field Name Description
Default Image Size Select the resolution to maintain the quality of images.
Parent Backup Path Enter the path of the backup folder, to store the recorded session images.
Backup Folder Specify the name of the backup folder in which the logs of recorded session
images are stored.
Service Interval Once the interval is set to 1 or 2 or more minute(s) the ‘ARCOS Log Manager
Service’ will connect the DB after that interval and empty the database and
save the images in the ‘Backup Folder’.
No of Images At One Time Select the number of images you want ARCON PAM to process at one time by
Log Manager Service.
Log Images Type Select the type for log images. The valid values are:
Colored
Black and White
Gray Scaled
Log web URL field Specify the IP Address and Port of User Access Log Viewer hosted on the
Server.
Enable Encryption checkbox If you enable the Enable Encryption checkbox, the images are stored in an
encrypted format.
Click Confirm Changes button to configure the details.

## [p412]

www.arconnet.com|Copyright © 2025 412
1.
4.3.7.11.3.1 Video Log Information Configuration
What is Video Log information Configuration?
Video Log Information Configuration is a form of a template that is displayed at the start of the video logs. This
template also appears when at the start when Images are played through Server Manager and Access Logs
or when Images are downloaded from the Server Manager, or when archived videos are played or downloaded
from Administrative Console. Apart from that, this template is also used when we export videos in Word
format from the server manager.
The configurations in this template include details such as User Id, User Name, Machine details, Service Type,
Service IP, Service hostname, Service User Name, Service DB Instance, Service Port Number, Connection type,
Description 1, Description 2, Description 3, Service Group, User Group, LOB,  Task/Incident number, Task/
Incident Description, and Log fileName. On enabling these toggle configurations, this information can be seen
on the first screen of the video logs.
To navigate, use the following path:
Settings → Log → Capture
Select Video Log Information Configuration under Capture:

## [p413]

www.arconnet.com|Copyright © 2025 413
2. Enabled configurations will be seen on the first screen of video logs.
4.3.7.11.3.2 ARCON PAM Staging Log Server
Staging Log Server is used to store logs before they are transferred to Database Server. Logs are compressed
and stored on this Server.

## [p414]

www.arconnet.com|Copyright © 2025 414
1.
2.
3.
In a few organizations, the size of logs generated per day is higher and users accessing ARCON PAM are of
greater volume. The bandwidth falls short for transferring logs to Database Server. In such a scenario, Log
Staging Server is used to store logs. These logs are then transferred to Database Server in the configured time
interval. The status of the logs can be monitored by hosting on the URL.
To navigate, use the following path:
Settings → Logs → Capture0
Select the ARCON PAM Staging Log server under Capture.
Select Enable (ARCON PAM Staging Log Server only for mentioned IP addresses) checkbox to enable
the configuration:
Select the Add button to add a new Staging Log Server.
The Administrator having ARCOS Staging Log Server privileges in Server’s Privileges will only be able
to configure values for Staging Log Server.

## [p415]

www.arconnet.com|Copyright © 2025 415
4.
5.
6.
The Staging Log Server screen contains the following fields:
Field Name Description
Description Enter the description.
From IP Enter the start IP address of the server from where log staging will start.
To IP Enter the end IP address of the server, where the log staging will end.
URL Enter the URL of the hosted Log Staging Server.
Enabled  To enable the configuration.
Enter the details and click Save to create a new Staging Log Server.
For editing, the details of the existing ARCON PAM Staging Log Server, click on the existing row and
select the Edit button at the top and make the required changes. Also, you can right-click on the row and
select Edit. Similarly, for deleting the existing ARCON PAM Staging Log Server, click on the existing row
and select the Delete button at the top and make the required changes. Also, you can right-click on the
row and select Delete.
The Export button will export all the ARCON PAM Staging Log Server details in the form .xlsx format.
The Copy button will copy all the details of the table.

## [p416]

www.arconnet.com|Copyright © 2025 416
1.
4.3.7.11.3.3 Modify Service Type
What is Modify Service Type?
Modify Service type allows the administrator to enable and disable the service types in ARCON PAM, Client
Manager  The disabled services will not be visible in ARCON PAM or CM. Administrators can also customize
the list of service types to be listed under Command Profiler.
To navigate, use the following path:
Settings → Log → Capture
Select Modify Service Type under Capture.
•
•
It is the basic configuration for the Staging Server. When logging in from the IP range, 0.0.0.0 to
192.168.0.237, ARCON PAM captures the local IP address, MAC address, processor ID, and
BIOS cell number. So, on that particular IP address, ARCON PAM will decide which server to
use as a Local Staging Server or Local Log Collector.
The From IP field refers to the local IP that is a laptop IP or desktop IP. If there is an IP range, as
in “From IP and To IP”, it will use the gateway server specified in the URL field. To configure
another gateway server, one can configure same server in another range or configure multiple
range on the multiple gateway servers. Every gateway server will need to have the sync service
installed.
The Administrator having Modify Service Type privilege shall only be able to select service types to be
displayed in ARCON PAM or CM.

## [p417]

www.arconnet.com|Copyright © 2025 417
2.
a.
b.
The toggle configurations can be set to:
Activate/Inactivate a particular service
Enable/Disable Video logs for services
c. Enable/Disable Text logs for services
3. Only the enabled services will be visible in ARCON PAM and CM.
4.3.7.11.3.4 Capture Configurations
This section explains the various parameters which can be configured for session monitoring and audit trails.
The toggle button would enable/disable the configuration.
To navigate, use the following path:
Settings → Logs → Capture
Field Name Description
ARCON Desk Insight Video
Log - Is Enabled For All
This configuration enables/disables ARCON Desk Insight Video Log globally for
all the services of Workstation being integrated into ARCON PAM.
ARCOSRDPDB SQL
Connect Timeout
This configuration sets the time in seconds for setting up the ‘timeout’ threshold
when connecting ARCOSRDPDB for sending logs.
Valid Values The valid range is 1-20.
Video Log Threading For
RDP - Is Enabled
This configuration enables/disables multithreading of Video Logs for RDP. This
can be useful if connectivity is weak with ARCON PAM Server.
Capture Window
Activated/Inactivated
State - Is Enabled
This configuration enables/disables Capturing of logs when Window in Active /
Inactive State once the session of target Server/device is taken through ARCON
PAM.
Note: The selected window is active. If you click somewhere else, the window is
inactive i.e. grayed
The Enable Video Log configuration should be enabled to enable video logs for all the service types.
The Enable Text Log configuration should be enabled to enable text logs for all the service types.
All the service types that are not checked in this list will not be visible in ARCON PAM and CM.

## [p418]

www.arconnet.com|Copyright © 2025 418
Field Name Description
Capture Window
Minimized / Maximized
State - Is Enabled
This configuration enables/disables capturing of Window in Minimized /
Maximized State.
Max Duration(in days) For
Log Generation
This configuration sets the value for viewing logs. Users can view logs as per the
configured days. This configured value is applicable to all logs except Service
Password Status logs.
Valid Values The valid range is 1-180.
By default, the value is 90 days.
Disable Video Logs by
Server Group
This configuration will allow to disable video logs for Server Groups.
Disable If the Toggle value is 'Disabled', the checkbox for Disable video logs will not be
displayed under the Section of Manage Groups.
Enable If the Toggle value is 'Enabled', the checkbox for Disable video logs will be
displayed under the Section of Manage Groups.
ARCON QA Video Log
Enable
This configuration enables/disables video logs for all QA connectors.
Use RDPDB For Image Log This configuration enables/disables the saving of pictures in the RDP database.
Disable If the Toggle value is 'Disabled', then images will be saved directly into a folder.
Enable If the Toggle value is 'Enabled', then images will be saved in the RDP Database.
Enable SSM Used to enable Session Monitoring for Connectors.
Command capture format
for clipboard data in
Command logs.
This configuration enables/disables the Command capture format for clipboard
data in Command logs
Use WebDT for Web API
Image Capture
This configuration enables/disables the Use of WebDT for Web API Image
Capture.

## [p419]

www.arconnet.com|Copyright © 2025 419
•
•
•
Field Name Description
New Image encryption
(Applicable in case of NO
RDPDB Database)
Select an encryption type from the dropdown, which will be used while sending
an image through the API.
Valid Value The valid values are below:
Old encryption-  Image Encoding
New encryption- AES 256 Encryption
New Encryption with Tamperproof
Enable Image Integrity Enable the toggle to ensure the authenticity of images processed by WebDT. If
an image is tampered with, the server detects it and responds appropriately.
Image Log Failure
Frequency
This is the time window within which you are monitoring the failures. For
instance, if you set this to 2 minutes, the system will check for failures within
each 2-minute interval.
Image Log Failure Count This is the threshold of failed image captures you allow within the specified time
window. If you set this to 10, the system will count the number of failed
attempts to capture images.
4.3.7.11.4 Archival Service
This section helps you with configurations in Archival Services of logs.
To navigate, use the following path:
Settings → Logs → Archival Service
Field Name Description
ARCOS Log Archiver Service - Is
Enabled
This configuration enables/disables the Log Archiving Operation (start/
stop).
ARCOS Log Archiver Service - Is
Delete Service Log (If Archive
Success)
This configuration enables/disables the deletion of Archived Logs from the
Server.
ARCOS Log Archiver Service -
Archive Older Than Hours
Configuration sets the number of hours for which the logs will be retained.
Logs prior to set hours will be archived into video logs (with higher
compression).
Valid Values It ranges from 0-99999.
Recommended Value: 3 hours.

## [p420]

www.arconnet.com|Copyright © 2025 420
•
•
•
1.
2.
Field Name Description
Rule Based Video Archival Enables or Disables Rule Based Video Archival.
Once the Rule based configuration is enabled, you cannot revert back the
configuration.
4.3.7.11.5 Scheduler
What is Scheduler?
A scheduler is a program that arranges and executes operations in a specific sequence and time frame, based on
a predefined objective. It ensures that planned activities are carried out according to schedule, organizing each
operation in the required order with the necessary time allocation. Schedulers are typically implemented to
enable multiple users to efficiently share system resources or to maintain a certain quality of service.
Why need Scheduler?
The scheduler helps monitor performance and ensures timely execution of tasks. It also facilitates the
generation of necessary reports based on scheduled activities, enabling better resource management and
operational efficiency across the system.
This section includes the following topics:
Scheduler Master
Schedule Password Envelope
Schedule Reports and Logs
4.3.7.11.5.1 Schedule Master
This section helps you to configure a scheduler master. The Administrator can define multiple schedulers as per
the requirement. The appropriate name for the scheduler, duration, and span details are provided while
defining a scheduler. In addition, you can modify the details of a configured scheduler.
To navigate, use the following path:
Settings →Logs→ Scheduler
Select Scheduler Master under Scheduler:
Select the Add button to add a new Scheduler Master:
The Administrator having Scheduler Master privilege will only be able to configure a scheduler.

## [p421]

www.arconnet.com|Copyright © 2025 421
The Scheduler Master Configure screen contains the following fields:
Field Name Description
Name Enter the name of the scheduler.
Description Enter a short description for the scheduler.
Time Zone Select the time zone from the dropdown list.

## [p422]

www.arconnet.com|Copyright © 2025 422
•
•
•
•
3.
4.
Field Name Description
Start Date Select the date and time for the scheduler to start processing.
Expire Date Select the end time for the scheduler to stop processing.
Schedule Type Used to select the schedule type for the scheduler. The valid values are:
Run only once: Enables the scheduler to run only once.
Daily: Enables the scheduler to run on a daily basis.
Weekly: Enables the scheduler to run on a weekly basis.
Monthly: Enables the scheduler to run on a monthly basis.
Run Only On (Daily) Select the number of days in a Week required for a scheduler to run, to fetch
reports or password envelope
Run Only On (Weekly) Select a day in a Week required for a scheduler to run, to fetch reports or
password envelope.
Run Only On (Monthly) Select the number of days in months required for a scheduler to run, to fetch
reports or password envelope.
Run Only Between These
Times
Select time to enable the scheduler to run on a timely basis.
Run Only Between These
Times on holidays
Select time to enable the scheduler to run on a timely basis on holidays.
Enabled  Enable the scheduler to start processing.
Enter the details and click Save button to create a new scheduler master.
For editing, the details of the existing scheduler master, click on the existing row and select the Edit
button at the top and make the required changes. Also, you can right-click on the domain and select Edit.
Similarly, for deleting the existing scheduler master, click on the existing row and select the Delete
button at the top and make the required changes. Also, you can right-click on the domain and select
Delete.
When set, the expire Time field will stop sending emails of the
Scheduled Password Envelope and Scheduled Reports to the user/
admin after the set period.
This field is enabled if you select the Schedule Type as Daily.
This field is enabled if you select the Schedule Type as Weekly.
This field is enabled if you select the Schedule Type as Monthly.

## [p423]

www.arconnet.com|Copyright © 2025 423
5. The Export button will export all the scheduler master details in the form .xlsx format. The Copy button
will copy all the details of the table.
4.3.7.11.5.2 Scheduler Configurations
To navigate, use the following path:
Settings → Logs → Scheduler
Field Name Description
Show ServiceType, Service
Group & UserID Filters In
ACMO.ViewAccessLogs
This configuration enables/disables the availability of Service Type, Service
Group, and UserID filters for selection in the CM > View Access Logs tab.
Disable If the toggle value is 'Disabled', then it disables the availability of these
options.
Enable If the toggle value is 'Enabled', then it enables the availability of these
options.
Exclude Inactive Or Disabled
Users From Reports - Is
Enabled
This configuration sets whether Inactive and Disabled Users are to be
excluded from Idle Users and User Last Logon reports.
•
•
You can filter details displayed in the grid view by entering the required value in the respective
column filter displayed above the header.
To generate a Unique Password Envelope for similar Domain ID's, the Envelope By Domain
IDs configuration should be enabled. This configuration is used to generate and send a unique
password envelope for similar Domain IDs based on the scheduled time in Schedule Master.

## [p424]

www.arconnet.com|Copyright © 2025 424
•
•
1.
Field Name Description
Service ID for Dashboard
Widget
Based on this configuration, a list of Service details accessed by the User is
displayed in the Services Currently Being Accessed widget (Client Manager
> Dashboard > Services Currently Being Accessed > More Info):
The list will be displayed based on the following two scenarios:
If you configure a value as a service type ID in this configuration, then
details of services accessed from Client Manager with the configured
service type ID will be displayed.
If you do not configure any value in this configuration, then details of
all services accessed from the Client Manager will be displayed.
Valid Values Service type ID
Generate Envelope By Domain
IDs
This configuration is used to generate and send a unique password envelope
for similar Domain IDs based on the scheduled time in the Schedule Master.
4.3.7.11.5.3 Schedule Password Envelopes
What are Scheduled Password Envelopes?
A password Envelope is an envelope that stores the password of the service in an encrypted format which will
help the password to be secure. This section helps you to configure the scheduler for a password envelope. The
password envelope scheduler once configured, will help the User to receive passwords in encrypted format as
envelope emails to their configured email IDs.
To navigate, use the following path:
Settings → Logs → Scheduler
Select Schedule Password Envelope under Scheduler.
•
•
•
The Administrator having Scheduler Master and Schedule Password Envelope privileges
in Server’s Privileges will only be able to configure the scheduler for password envelope.
Once the scheduler is configured in Scheduler Master, you need to then schedule a password
envelope.
To generate a Unique Password Envelope for similar Domain ID's, the Envelope By Domain
IDs configuration should be enabled. This configuration is used to generate and send a unique
password envelope for similar Domain IDs based on the scheduled time in Schedule Master.

## [p425]

www.arconnet.com|Copyright © 2025 425
2. Select the Add button to add a new Password Envelope:

## [p426]

www.arconnet.com|Copyright © 2025 426
The Schedule Password Envelope screen contains the following fields:
Field Name Description
Description Specify a short description for the specific scheduler.
LOB/Profile Select the LOB. On selecting LOB, the Service Group Details are displayed in
the grid. On selecting Service Group, the Service Types are displayed.
Enabled  Enable the scheduler to start processing.
Scheduler Select the scheduler.
Envelope Password Specify the envelope password.
The schedulers configured under Scheduler Master will be available
for selection.
You can enter a minimum of 12 character password.

## [p427]

www.arconnet.com|Copyright © 2025 427
•
•
•
•
•
3.
4.
Field Name Description
Send Newly Created
Envelope(s) Instantaneously
Indicates that when a new connection password is changed, the password
envelope of that connection will be mailed to their configured email IDs.
File Location
File Location (Select) Select the radio button and accordingly enter the details of the path to the
folder.
Shared
Email
Both
Shared Folder Path Enter the path of the shared folder to save the file.
Email Parameters
Email Parameters Select the radio button:
Send Complete Password to the Admin: The password envelope is sent
to the owner whose email Id is configured below.
Send Individual Envelopes to Respective Owners: For services with
split passwords, envelopes are sent to individual owners.
User Email IDs Specify the email id of the user to whom the email has to be sent.
Email Subject Specify the subject for the email.
Email Body Specify the description for the mail
Enter the details and click the Save button to create a new Schedule Password Envelope.
For editing the details of the existing Schedule Password Envelope, click on the existing row and select
the Edit button at the top and make the required changes. Also, you can right-click on the domain and
select Edit.Similarly, for deleting the existing Schedule Password Envelope, click on the existing row and
select the Delete button at the top and make the required changes. Also, you can right-click on the
domain and select Delete.
For Instantaneous Password Envelope, the email Subject in Schedule
Password Envelope should contain IP Address and Username of
Service. Any alert notification sent via email for Instantaneous
Password Envelope will have<IP, Username>which will help the
Administrator to identify the envelope is for which service based on
the subject Line i.e, <IP, Username>.
Multiple Email IDs can be added separated by semi-colon or comma.

## [p428]

www.arconnet.com|Copyright © 2025 428
5.
1.
The Export button will export all the Schedule Password Envelope details in the form .xlsx format. The
Copy button will copy all the details of the table.
4.3.7.11.5.4 Schedule Reports and Logs
What are Schedule Reports and Logs?
This section helps you to schedule various types of reports and logs. It will help the User to receive generated
reports through email on the scheduled date/time intervals. A Schedule Report is based on the configured
Scheduler master. So prior to scheduling reports, it is mandatory to configure Scheduler Master.
To navigate, use the following path:
Settings → Logs → Scheduler
Select Schedule Reports and Logs under Scheduler:
•
•
•
You can save the password envelope in a shared drive.
You can filter details displayed in the grid view by entering the required value in the respective
column filter displayed above the header.
If the Password Envelope Protected File configuration is enabled, then the password envelope
will be sent in .zip format whereas if it is disabled then it will be sent in .txt format.
•
•
The Administrator having Scheduler Master and Schedule Reports privileges in Server’s
Privileges will only be able to configure scheduler for reports.
Once the scheduler is configured in Scheduler Master, you need to then schedule reports.

## [p429]

www.arconnet.com|Copyright © 2025 429
2. Select the Report radio button. Then select the Add button to add a new Schedule Report:

## [p430]

www.arconnet.com|Copyright © 2025 430
The Schedule Reports screen contains the following fields:
Field Name Description
Report Category Select the category of the report.

## [p431]

www.arconnet.com|Copyright © 2025 431
Field Name Description
Report Name Displays the list of reports.
Schedule Type
LOB/Profile Select the LOB.
From Date Select the start date to fetch reports.
To Date Select the end date for the reports to be fetched.
User Group Select the user group.
Service Group Select the service group.
User ID Enter the user ID.
Server IP Enter the server IP.
Service Type Select the type of service.
The data in this field is auto-populated based on the Report
Category selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.

## [p432]

www.arconnet.com|Copyright © 2025 432
3.
4.
5.
1.
Field Name Description
Scheduler Select the corresponding scheduler master.
Is Active Enable the scheduler.
File Location
Save Report File Select to save the scheduled report.
Application Server Folder Path Enter the path of the application server to save the file.
Email Parameters
User Email ID Specify the email id of the user to whom the email is to be sent.
Email Subject Specify the subject for the email.
Email Body Specify the description for the mail.
Enter the details and click Save button. A window pops up with the following message: New Report
Scheduled
For editing the details of the existing scheduled report, click on the existing row and select the Edit
button at the top and make the required changes. Similarly, for deleting the existing scheduled
report, click on the existing row and select the Delete button at the top and make the required changes.
The Export button will export all the scheduled report details in the form .xlsx format. The Copy button
will copy all the details of the table.
To schedule logs uses the following path:
Settings → Logs → Scheduler
Select Schedule Reports and logs under Scheduler.
•
•
•
You can filter details displayed in the grid view by entering the required value in respective
column filter displayed above header.
The file naming convention for reports where the LOB  filter is enabled will be Report
name_LOB name_Timestamp.
The reports configured using Weekly  Schedule Type will be received on configured
day containing the last seven days data.

## [p433]

www.arconnet.com|Copyright © 2025 433
2. Select the Log radio button. Then select the Add button to add a new Schedule Report.

## [p434]

www.arconnet.com|Copyright © 2025 434
The Schedule Reports screen contains the following fields:

## [p435]

www.arconnet.com|Copyright © 2025 435
Field Name Description
Log Category Select the category of the Log.
Schedule Type
LOB/Profile Select the LOB.
From Date Select the start date to fetch reports.
To Date Select the end date for the reports to be fetched.
User Group Select the user group.
Filter By Select the filter
Filter Value Specify the filter value if required
Object Type Select the object type from the dropdown
Operation Type Select the operation type from the dropdown
Service Group Select the service group.
User ID Enter the user ID.
Server IP Enter the server IP.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.
This field is enabled or disabled on the Master Report selected.

## [p436]

www.arconnet.com|Copyright © 2025 436
3.
4.
5.
Field Name Description
Service Type Select the type of service.
Scheduler Select the corresponding scheduler master.
Enabled Enable the scheduler.
File Location
Save Report File Select to save the scheduled report.
Application Server Folder Path Enter the path of the application server to save the file.
Email Parameters
User Email ID Specify the email id of the user to whom the email is to be sent.
Email Subject Specify the subject for the email.
Email Body Specify the description for the mail.
Enter the details and click Save button. A window pops up with the following message: New Log
Scheduled
For editing the details of the existing scheduled log, click on the existing row and select the Edit button
at the top and make the required changes. Similarly, for deleting the existing scheduled log, click on the
existing row and select the Delete button at the top and make the required changes.
The Export button will export all the scheduled log details in the form .xlsx format. The Copy button will
copy all the details of the table.
4.3.7.12 Network/Connection
4.3.7.12.1 Gateway
The Gateway component allows different types of sessions to be brokered from the administrator/user
machines to the target devices. There are two types of Gateway i.e. Secure Gateway and Application Gateway.
This section allows administrators to configure the gateway depending on the type of defined architecture.
This field is enabled or disabled on the Master Report selected.
•
•
•
You can filter details displayed in the grid view by entering the required value in respective
column filter displayed above header.
The file naming convention for reports where the LOB filter is enabled will be Log name_LOB
name_Timestamp.
The reports configured using Weekly  Schedule Type will be received on configured
day containing the last seven days data.

## [p437]

www.arconnet.com|Copyright © 2025 437
1.
2.
4.3.7.12.2 VPN Servers
VPN Servers are Secure Gateway Server (SGS) for ARCON PAM. If VPN Server is configured in ARCON PAM,
the connection is invoked from User’s workstation to SGS and then from SGS to the target server/devices for
SSO or password change on the target device. If the VPN server is not configured, then the connection is
established directly from the User's machine to the Target Device. The connection from the User workstation
to the secured gateway server is established through an AES 256-bit with an encrypted tunnel on a secured
port, making the connection more secure. In the case of an organization, when there is a Firewall in use, a port
needs to be opened from a particular local machine to a remote machine (it may be any server) which is on the
other side of the Firewall for communication. In this case, there should be a VPN Server whose credentials are
stored in an ARCON PAM Server.
To navigate, use the following path:
Settings → Network/Connection → Gateway
Select VPN Servers service under Gateway.
For adding a new VPN server select the Add button. Click Save after adding the details.
The Administrator having VPN Server privileges in Server’s Privileges will only be able to configure
the VPN server.

## [p438]

www.arconnet.com|Copyright © 2025 438
•
•
•
The VPN Server screen contains the following fields:
Field Name Description
IP Address Enter the IP address of the VPN Server.
Port No Enter the port number.
User Name Enter the user name of the VPN Server.
Password Enter the password of VPN Server
VPN Key Enter key for identification of service. The default value is ARCOS.
Use VPN For Database In ARCON PAM the session recording is sent from user’s workstation
to database in the following three ways:
Directly to Database (PVSL - Password Vault Session Logging)
on a set port
Via Application Server (EPAM - Enterprise Privileged Account
Management) to PVSL using port 443
Via Secure Gateway Server (SGS) to PVSL using port 22 – for
enabling this ‘Use VPN for Database’ is checked.
It is enabled when the database is on the other side of the
Firewall and is accessed from a local machine that is inside the
boundary of the firewall.

## [p439]

www.arconnet.com|Copyright © 2025 439
3.
4.
1.
2.
Field Name Description
Enabled  Enable the configuration.
The Export button will export all the VPN server details in the form .xlsx format. The Copy button will
copy all the details of the table.
To delete any record, click Delete button or right click on any record and click delete.
To add Virtual IP in the VPN servers, perform these steps below:
Right-click on the required VPN server from the grid and select Set VPN Servers - Virtual IP's:
The VPN Servers - Virtual IP's screen displayed:
The status is active for VPN Server once enabled. If disabled
the server will not be used in LOB to which it is mapped.

## [p440]

www.arconnet.com|Copyright © 2025 440
3.
1.
2.
The VPN Server screen contains the following fields:
Field Name Description
Remote IP Specify the remote IP address
Server IP Specify the server IP address
Server Port Specify the server port number
Enabled Select the checkbox to enable virtual IP for the VPN server
Click on the Save button.
To update the Virtual IP in the VPN servers, perform these steps below:
Right-click on the required VPN server from the grid and select Set VPN Servers - Virtual IP's.
The VPN Servers - Virtual IP's screen displayed. Click on the existing details that you need to update:
This field also allows you to add text

## [p441]

www.arconnet.com|Copyright © 2025 441
3. Update the required details in the existing fields, then click on the Update button.
4.3.7.12.3 Gateway Configurations
To navigate, use the following path:
Settings → Network/Connection → Gateway
Field Name Description
ARCON VPN Client Version This configuration sets the Version of internal VPN.
There are multiple versions of internal VPN’s, one of which can be used to
connect to destination servers. Depending on the architecture, User selects
the appropriate VPN type.
Valid Values It ranges from 1-4.
VPN For ARCON Desk Insight
(RDP) - Is Enabled
This configuration enables/disables VPN for ARCON Desk Insight (RDP).
Disable If Toggle value is 'Disabled', then it disables VPN for ARCON Desk Insight
(RDP).
Enable If Toggle value is 'Enabled', then it enables VPN for ARCON Desk Insight
(RDP).

## [p442]

www.arconnet.com|Copyright © 2025 442
•
•
Field Name Description
ARCON VPN Client Version
(For SSH, Telnet)
This configuration sets the Version of internal VPN for SSH and Telnet
based services.
Multiple versions of internal VPN’s can be used to connect to SSH
destination servers. Depending on the architecture, user selects the
appropriate VPN type.
Valid Values  It ranges from 1-4.
ARCON VPN Client Version
(For SFTP, FTP)
This configuration sets the Version of internal VPN for SFTP and FTP only.
There are multiple versions of internal VPN’s, one of which can be used to
connect to destination servers for SFTP and FTP for Linux. Depending on the
architecture user selects the appropriate VPN type.
Valid Values It ranges from 1-4.
ARCOS Compro Secure
Gateway Is Enable
This configuration helps you to enable/disable SHA-2 enabled gateways.
Secure Gateway supports following Ciphers:
Key Exchange Method
diffie-hellman-group-exchange-sha256
diffie-hellman-group-exchange-sha1
diffie-hellman-group14-sha1
diffie-hellman-group1-sha1
Message Authentication Code (MAC) algorithms:
hmac-md5
hmac-md5-96
hmac-sha1
hmac-sha1-96
hmac-sha2-256
hmac-sha2-256-96
hmac-sha2-512
hmac-sha2-512-96
hmac-ripemd160
hmac-ripemd160@openssh.com
Disable If Toggle value is 'Disabled', then it disables SHA-2 enabled gateways.
Enabled If Toggle value is 'Enabled', then it enables SHA-2 enabled gateways.

## [p443]

www.arconnet.com|Copyright © 2025 443
1.
2.
4.3.7.12.4 AGW
Application Gateway server (AGW) is a solution that controls all the entry points into your environment. With
AGW, one can allow taking remote sessions to one particular machine (AGW Server) that is placed in a very
controlled environment and is monitored from the AGW Server.
4.3.7.12.4.1 Configure Enduser IP Range
This Enduser IP Range configuration allows the selected end users to connect to the target server at the User
level. Since the connection is set at the User level, any services mapped with that particular User ID will know
how the connection will take place i.e. via AGW, Gateway, or Direct.
To navigate, use the following path:
Settings → Network/Connection → AGW
Select Configure Enduser IP Range under AGW:0
Select the Add button to configure a new Enduser IP range:

## [p444]

www.arconnet.com|Copyright © 2025 444
•
•
3.
4.
The Configure Enduser IP range screen contains the following fields:
Field Name Description
Access Via The User is routed via
Gateway
AGW
From IP Enter starting IP address to configure Enduser IP range.
To IP Enter ending IP address to configure Enduser IP range.
Enabled  Click to enable the configuration.
Enter the details and click Save to Configure Enduser IP range.
For Editing, the details of the existing Configure Enduser IP range, Click on the existing row and select
the Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.

## [p445]

www.arconnet.com|Copyright © 2025 445
5.
6.
For Deleting the existing Configure Enduser IP range, Click on the existing row and select the Delete
button at the top and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the Configure Enduser IP range details in the form .xlsx format. The
Copy button will copy all the details of the table.
4.3.7.12.4.2 AGW Configuration
To navigate, use the following path:
Settings → Network/Connection →AGW0

## [p446]

www.arconnet.com|Copyright © 2025 446
Field Name Description
Use AGW for Open Connection This configuration enables/disables the option of AGW.
Disable If Toggle value is 'Disabled', then the AGW icon will not be
displayed in ACMO (under My Services) and users won't be able to
access service sessions in ACMO through AGW.
Enable If Toggle value is 'Enabled', then the AGW icon will be displayed
next to the open connection icon in ACMO (under My Services) and
users can take service sessions via AGW.
Use AGW to open Server manager This configuration enables/disables the configuration to open
ARCON PAM Server Manager on a specific AGW Server where
only PAM Admin activities can be performed.
Disable If Toggle value is 'Disabled', then Server Manager cannot be
launched on AGW.
Enable If Toggle value is 'Enabled', then it will map the AGW servers to
ARCON PAM Server Manager.
Use User's AGW pin to connect to AGW This configuration enables/ disables connection to the AGW server
through PAM Username.
Disable If Toggle value is 'Disabled', hen it will connect by username which
is configured in AGW configuration
Enable If Toggle value is 'Enabled', then it will connect to the AGW server
using the PAM user name.
Enable AGW Multiple Instance in one
connection
This configuration enables/disables the AGW multiple instance in
one connection
Record all Windows in AGW This configuration will enable or disable the option to record all
windows in AGW.
AGW Time Between Sign Off and New
Connection
This configuration enable or disable the AGW time between Sign
off and New Connection

## [p447]

www.arconnet.com|Copyright © 2025 447
•
•
•
•
1.
4.3.7.13 API
In ARCON PAM, there is a Web API collection. Instead of creating the same configuration again and again, a
repository of configurations is created. In the repository of configuration, one can configure a number of
configuration types such as URL, description, method, API ID, user name, and password.
This section includes the following topics:
API Configure
3rd Party API Notifier
Service Creation Validator
Registered Machines
4.3.7.13.1 API Configure
4.3.7.13.1.1 Web API Configuration
SNA API and ID1 are the identification (ID) of API. In ARCON PAM, there is a standardization. The
standardization describes how ARCON PAM will communicate with the target device or target system, in what
format it will communicate, and the number of parameters. These factors are already defined. When
performing the implementation, it becomes a challenge because the alternate system may not have the same
parameter configuration. The alternate system may also not have the flexibility to configure the parameters as
per the ARCON PAM requirements. However, they will have a standardization of the parameters. To overcome
this challenge, we have created the API configuration.
To navigate, use the following path:
Settings → API → Configure00
Select Web API Configuration under the API Configure.0
The Administrator having Web API Configuration privileges in the Server’s Privileges will only be able
to configure details in Web API Configuration.

## [p448]

www.arconnet.com|Copyright © 2025 448
2. Select the Add button to add a new Web API:0

## [p449]

www.arconnet.com|Copyright © 2025 449
The Web API Configuration screen contains the following fields:

## [p450]

www.arconnet.com|Copyright © 2025 450
Field Name Description
Header Authorization  Enable the toggle button to authenticate web API not only through Request
Body but also through Authorization in Request Header.
URL Enter the URL of the Web IP.
Token Authentication URL Enter the URL for token authentication.
Offline Token Validation Enter comma separated email ID for offline token validation.
Request Body Enter XML Data. The XML data can be imported by clicking on
button.
Description Enter the description of Web API.
Content Type Displays the predefined content type of Web API.
Method Enter the method of Web API.
Accept Displays the predefined response value of Web API.
API ID Enter the application programming interface ID.
SOAP Action
User Name Enter the username of the web IP page.
Password Enter the password of the web API page.
Enabled  To enable the configuration.
Response Parameters
Success Tag Define a tag for successful API calling.
Success Text This text will be displayed on a successful API call.
Error Tag Define a tag for the API call failure.
Error Text This text will be displayed on an API call failure.
If the toggle is on, username and password fields will be sent in the
API request header and if the toggle is off, username and password
fields will be sent in the request body.
Check box to enter the URL for token authentication
Check box to enter the offline token validation

## [p451]

www.arconnet.com|Copyright © 2025 451
3.
4.
5.
Field Name Description
Custom Validation
Parameter Name Enter the name of the parameter.
Parameter Type Select the dropdown value of the Parameter Type as Less Than, Greater
Than, Equals, Less Than Equals, and Greater Than Equals.
Validation Operation Select the dropdown value of the Validation Operation.
Validation Against Enter the value of validation against.
Enable Proxy
Proxy URL Enter the proxy server URL.
User Name Enter the username of the proxy server.
Password Enter the password for the proxy server.
Enabled  To enable the configurationa
Enter the details and click Save to create a new Web API.
To edit the details of the existing Web API Configuration, click on the existing row, select the Edit button
at the top, and then make the required changes. Also, you can right-click on the row and select Edit:
To delete the existing Web API Configuration, click on the existing row, select the Delete button at the
top, and then make the required changes. Also, you can right-click on the row and select Delete.

## [p452]

www.arconnet.com|Copyright © 2025 452
6.
7.
8.
The Export button will export all the Web API Configuration details in the form .xlsx format. The Copy
button will copy all the details of the table.
Enter the URL in the ARCON API URL text field.
Select the configuration type from the TLS Configuration For SMS Web API drop-down list.

## [p453]

www.arconnet.com|Copyright © 2025 453
1.
4.3.7.13.2 3rd Party API Notifier
4.3.7.13.2.1 API Reference Mapping
This section explains how ARCON PAM notifies Third Party API when the password of a service is changed in
the application. An Administrator having access to API Reference Mapping configuration can enable ARCON
API to notify Third Party API about the service password change. You need to configure Third Party API details
in Web API configuration and give its reference in API Reference Mapping. The URL of ARCON API should be
configured in ARCON API URL under Global Configuration.
To navigate, use the following path:
Settings → API → 3rd Party API Notifier
Select API Reference Mapping under 3rd Party API Notifier:
The API Reference Mapping screen contains the following fields:
Field Name Description
Enable Select to Enable API Reference Mapping
API Reference Tag Enter same value followed by <WAPI> tag which you have entered in API ID
field under Web API screen.
Param 1 Value Not Applicable
Param 2 Value Not Applicable
•
•
You need to enable Precision Biometric for fingerprint authentication over API from the back
end.
The Precision Authentication API URL will be provided by the Client. Enter this URL in the
URL text field and configure details in the Web API Configuration screen.
The Administrator having API Reference Mapping privileges in Server’s Privileges will only be able to
configure API Reference Mapping.

## [p454]

www.arconnet.com|Copyright © 2025 454
2.
•
•
•
1.
2.
Field Name Description
Param 3 Value Not Applicable
Param 4 Value Not Applicable
Enter the details and click Confirm Changes button to configure the detail.
4.3.7.13.3 Service Creation Validator
4.3.7.13.3.1 Server Monitoring System
The server monitoring system is configured to validate whether the service or the server is already monitored
by some monitoring system. If it is not, ARCON PAM will not allow the server to get integrated for the user to
access it. Further to explain this, the user can perform checks to make sure that any Server when goes online in
the network has been passed through all the necessary hygiene checks, security checks, etc. The status of the
same may be available with various systems such as:
Monitoring System: It is responsible to monitor the server health status.
SIEM System: It is responsible to check for any vulnerabilities left open which may attack the system or
any hardening checks, configuration missed, or real-time analysis.
Anti-Virus System: It is responsible to check if the server is updated with the latest signature of Anti-
virus and is fully protected from viruses or similar attacks.
To all of these systems, ARCON PAM has a framework available to get integrated with these systems, to check
for the respective status of a server, and then allow a server or system to be integrated in the application for
any User to access it.
To navigate, use the following path:
Settings → API → Service Creation Validator
Select the Server Monitoring system under Service Creation Validator. Select the Enable checkbox.
A window pops up with the following message:
Configure the URL of ARCON API in ARCON API URL  in Global Configuration. This API will notify
Third Party API when the password of a service is changed in ARCON PAM.
The Administrator having Server Monitoring System privileges in Server’s Privileges will only be able
to configure values for Server Monitoning System.

## [p455]

www.arconnet.com|Copyright © 2025 455
3.
4.
1.
Click Yes. The Server Monitoring System fields are enabled.
The Server Monitoring System screen displays the following fields:
Field Name Description
Validation URL Enter the URL of web service (Web API).
This URL has the web service parameters required to validate the service which is
created in ARCON PAM. It sends the details to web service and based on the
response, it will allow or deny the creation of a new service post validation with
the monitoring system.
In the Validation URL, enter the URL of the API with the corresponding tags.
There are URL’s based on Java, some of the web services are .Net based web
services. They can be configured as if the format is same. But if web service is Java
or JSP based, they need certain parameters to be enabled in .Net. If it is Java
based, certain parameters need to be enabled, else the communication fails.
<Java> is the tag to be configured in the web service configuration.
Is Validate LOB/Profile Indicates if the user wants to validate using LOB/Profile.
Is Validate Service Type Indicates if the user wants to validate service type.
Is Validate Service User
Name
Indicates if the user wants to validate service user name
Select the details and click Confirm Changes button to configure the details.
4.3.7.13.4 Registered Machines
4.3.7.13.4.1 Web API Registration
Web API Registration helps you to register the user’s machine IP address, where the user can view the
password from the registered machine or laptop.
To navigate, use the following path:
Settings → API → Registered Machines0
Select Web API Registration under Registered Machines:
The Administrator having ARCON PAM Web API Registration privileges in Server’s Privileges will
only be able to configure the Web API registration details

## [p456]

www.arconnet.com|Copyright © 2025 456
2. Select the Add button to register a new Web API.
The Web API Registration screen contains the following fields:
Field Name Description
Description Specify the description for registration.
Requestor IP Specify the IP address of the requestor.
Requestor MAC Specify the MAC address of the requestor.

## [p457]

www.arconnet.com|Copyright © 2025 457
3.
4.
5.
6.
1.
Field Name Description
LOB Select LOB.
Service Type Select the type of service.
Enabled  Tick the checkbox to enable the configuration.
Select Services  The list of services are displayed in the Select Services grid, once you select
the service type from the Service Type dropdown list
Enter the details and click the Save button to create a new Web API.
To edit the details of an existing Web API Registration, either click on the desired row and select the
Edit button at the top, or simply right-click on the row and choose Edit from the context menu.
To delete an existing Web API Registration, select the desired row and click the Delete button at the
top, or right-click on the row and choose Delete from the context menu.
The Export button will export all the Web API Registration details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.13.4.2 Bulk Import
This feature allows administrators to efficiently register multiple user machine IP addresses at once, saving
time and reducing manual effort.
Follow these steps to perform bulk import:
Click Import as illustrated below.

## [p458]

www.arconnet.com|Copyright © 2025 458
2.
3.
The Import File screen is displayed. Click Download the Template to download the Excel file.
Complete all the required fields in the downloaded template and save the file to your local device.
Refer to the table below to understand the fields:
Field Name Description
Description A short note or label describing the purpose or identity of the
entry.
Requestor_IP Enter the IP address of the requesting machine that needs to be
registered.
Requestor_MAC Enter the MAC address of the requesting device.

## [p459]

www.arconnet.com|Copyright © 2025 459
4.
•
•
•
Field Name Description
LOB Enter the business unit or department the requestor belongs to.
Service_Group Enter the service group of the device.
Service_Types Enter the service type of the device.
Services Enter the specific service names or IDs for the user.
Enabled Indicates whether the entry is active
Click the Browse button to upload the file.
4.3.7.14 General
The General  menu allows administrators to configure essential settings that influence decision-making and
enable changes to the user interface, personalization options, and startup behavior.
To navigate, use the following path:
Settings → General
Field Name Description
ARCOS Server Manager Login
Mode
This configuration sets whether the User ID and Password are required to
be entered when an Admin User logs in to Server Manager.
Valid Values The valid range is 0-2.
If the ‘0’ value is set, then the system will prompt for both User ID
and Password.
If the ‘1’ value is set, then the system will prompt only for the
Password.
If the ‘2’ value is set, then the system considers this as Single Sign-
On, that is, the Admin can log into Server Manager directly, as here
the Portal Authentication will be used to validate the User.
•
•
•
•
If the ARCOSAPI(Password Retrieval)RequestorValidator – Is Enabled configuration is
disabled, then the user can view the password of the service from any machine.
If the ARCOSAPI(Password Retrieval)RequestorValidator – Is Enabled configuration is
enabled, then the user can view the password of the service from only the registered machine.
For API Restriction to work, the configuration ARCOSAPI(Password
Retrieval)RequestorValidator should be enabled. It works only if both the Requestor Machine
and API Server are in the same VLAN/Subnet.
On enabling this configuration, it will restrict all API Access and will allow only those API
Requests for which the IP address and MAC address are registered in the API registration.

## [p460]

www.arconnet.com|Copyright © 2025 460
Field Name Description
ARCOS Server Master - Is
Enabled
This configuration sets the availability of Server Master under Server
Manager > Settings  > Logs > Scheduler
Show List Of Newly Discovered
Devices In Server Manager - Is
Enabled
This configuration will enable or disable the Discovered Devices option in
Server Manager.
Cisco ISE HTTP Protocol for
Certificate Validation
This configuration sets protocols for Cisco ISE configuration.
Valid Values SSL3, TLS, TLS1.1, TLS1.2
Environment Information This configuration enables users to display environment information (e.g.,
Production/UAT) in Server Manager and Client Manager.
Valid Values Production/UAT.
Enable SSH File Encryption This configuration will enable or disable the encryption of the SSH text file,
which is generated in SSH output to a file.
SSH Output to File This configuration will enable/disable the SSH output in the file.
Disable If the Toggle value is 'Disabled', then this feature is disabled.
Enable If the Toggle value is 'Enabled', then the file is saved based on the config
value in ./api/Command/WriteCommandDataToDatabase.
SSH Output Log This configuration will enable/disable the SSH output to log.
Disable If the Toggle value is 'Disabled', then this feature is disabled.
Enable If the Toggle value is 'Enabled', then CLI output for the executed
commands over Putty will be captured in the Server manager→ Manage
Menu →  Logs → Service Logs.
Server for Datawatch This configuration sets the server for Datawatch.
Valid values Server IP

## [p461]

www.arconnet.com|Copyright © 2025 461
Field Name Description
Force Client Manager Splash
Screen to be Always on Top
This configuration enables or disables the feature for the client manager
splash screen to be always on top.
Enable Custom Columns in
Reports
This configuration allows you to enable or disable the column
customization while exporting any report.
IsCapture Data This configuration enables or disables the Is Capture Data option.
Enable Browser Protocol to
Open Connection
This setting is typically used in VDI-based systems (where multiple users
would come on a single box to browse the PAM solution to connect to
target devices).
Enable If this setting is enabled, the user would connect to the target device, and
the PAM client (connector) would launch in their profile.
Get all connection related
configs at once - Is Enabled
By enabling this configuration, the Administrator can get all connection
details through one API call.
Frequency in Minutes to check
logout punch Is ON?
This will check if the logout punch should be off at a specific time. The
default time is 10 minutes.
Frequency in Minutes to check If
Logout Punch API calls are OFF?
This will check dynamically if API calling(toggle) is OFF. The default time is
15 minutes.
Frequency in Minutes For
sending session activity details
captured by logout punch
This will update the remaining JSON if there is anything left. The default
time is 60 minutes.
Close All API calls for logout
punch?
This enables/disables sending logout punch data to PAM.
Disable If the Toggle value is 'Disabled', it will allow sending logout punch data to
PAM.

## [p462]

www.arconnet.com|Copyright © 2025 462
1.
2.
3.
4.
Field Name Description
Enable If the Toggle value is 'Disabled', it will stop sending logout punch data to
PAM.
Send session activity data in
Offline hours?
This enables/disables sending session activity data in offline hours to PAM.
Disable If the Toggle value is 'Disabled', it will stop sending session activity data in
offline hours to PAM.
Enable If the Toggle value is 'Disabled', it will allow sending session activity data in
offline hours to PAM.
Disable ARCON PAM Plugin
Security
This setting is typically used to encrypt or decrypt the data passing from
the ACMO to the plugin (connector).
Disable If the Toggle value is 'Disabled', the data passing from the ACMO to the
plugin will be encrypted.
Enable If the Toggle value is 'Enabled', the data passing from the ACMO to the
plugin will not be encrypted.
Restrict SFTP File Transfer The Restrict SFTP File Transfer setting controls whether users can perform
SFTP (Secure File Transfer Protocol) operations during their SSH-based
Linux sessions.
Disable If the Toggle value is 'Disabled', Users cannot upload or download files
using SFTP during their Linux SSH sessions.
Enable If the Toggle value is 'Enabled', Users can perform file transfers using SFTP
over SSH connections.
Enable BlockInput The Enable BlockInput feature is used to prevent user interaction, such as
keyboard or mouse input, during the login process, especially when the
session is being launched via a web browser.
Disable If the Toggle value is 'Disabled', Users can interact with the session even
while the login process is ongoing.
Enable If the Toggle value is 'Enabled', all user inputs are blocked during the login
process, preventing any interference until the login is fully completed.
Allow pasting password on login
screen
When enabled, users will be able to paste passwords into the password
field while logging in on the following screens:
ACMO Login screen
Server Manager login screen
Server Manager login screen (when resumed after idle timeout)
Connector session login screen (when locked due to idle timeout)

## [p463]

www.arconnet.com|Copyright © 2025 463
1.
2.
3.
Field Name Description
New Image Capture Mechanism The New Image Capture Mechanism enables an updated method for
capturing images or video from the login page during session initiation.
Disable If the toggle is set to ‘Disabled’, video capture from the login page will not
be allowed.
Enable If the Toggle value is 'Enabled', it allows the video capture from the login
page.
4.3.7.14.1 ARCON PAM Server Configuration
ARCON PAM Server Configuration helps you to configure Server details like UAT, Production, Application, etc.
These details will be displayed in About (Client Manager).
To navigate, use the following path:
Settings → General
Select the ARCON PAM Server Configuration.
Enter server details in the Server Description text field.0
Click Confirm Changes  to save the configuration. The following message will be displayed: ARCON
PAM Server Configuration Value Updated Successfully.
The Administrator having ARCOS Server Configuration privileges in Server’s Privileges will only be
able to configure server details.

## [p464]

www.arconnet.com|Copyright © 2025 464
1.
2.
4.3.7.14.2 Server Master
This section monitors the performance of ARCON PAM servers. In addition, it allows adding or modifying
servers such as application servers, database servers, gateway servers, and DR servers.
To navigate, use the following path:
Settings → General
Select Server Master.
Select the Add button to add a new Server Master:
The Administrator having ARCOS Server Master privilege in Server’s Privileges will only be able to
configure details in Server Master.

## [p465]

www.arconnet.com|Copyright © 2025 465
The Server Master screen contains the following fields:
Field Name Description
Description Specify the type of server such as application server, or database server.
Host Name Specify the hostname of the server.
IP Address Specify the IP address of the server.

## [p466]

www.arconnet.com|Copyright © 2025 466
Field Name Description
Type Select the type of server. The valid values are:
Production
Production – HA
Disaster Recovery
Disaster Recovery - HA
Component Type Select the type of component (sub type server). The valid values are:
Application Server
Vault Server
Gateway (VPN) Server
Base OS Displays the base OS used.
Instance Specify the instance.(if applicable)
Port Specify the standard port number.
Domain Name Specify the domain name.
User Name Specify the username.
Password Specify the password.
Confirm Password Re-enter the password and confirm.
Parameter 1 Specify the parameter. (if applicable)
Parameter 2 Specify the parameter. (if applicable)
Critical Error Alert
(checkbox)
Enable the Email ID, Email Subject, and Email Body text field.
Email ID Specify the email ID of the user.
Email Subject Specify the subject title for the email.
The data in this field is auto populated, if you select the Component
Type as Vault Server.
The data in this field is auto populated, if you select the Component
Type as Vault Server.
The data in this field is auto populated, if you select the Component
Type as Vault Server.

## [p467]

www.arconnet.com|Copyright © 2025 467
3.
4.
5.
6.
Field Name Description
Email Body Specify the description for the email.
Enabled  (checkbox) Enable the configuration in ARCON PAM.
Enter the details and click Save to create a new Server Master. A window pops up with the following
message: New ARCOS Server Created
For Editing, the details of the existing Server Master click on the existing row and select the Edit button
at the top and make the required changes. Also, you can right-click on the row and select Edit:0
For Deleting the existing Server Master click on the existing row and select the Delete button at the top
and make the required changes. Also, you can right-click on the row and select Delete.0
The Export button will export all the Server Master details in the form .xlsx format. The Copy button will
copy all the details of the table.
•
•
•
The win PWD service.exe should be installed on ARCON PAM Servers which is Windows-
based.
Port 45045 should be opened from Database Server to all windows based servers (i.e. App and
DB servers).
Port 22 (SSH) should be opened from Database Server to all UNIX based servers (i.e. Secured
servers).

## [p468]

www.arconnet.com|Copyright © 2025 468
4.3.7.14.3 Server Type Configuration
What is Server Type Configuration?
In Server Type Configuration users can define the separation of the production and non-production servers in
different colors. Production servers will be visible in a different color in ACMO and non-production servers in
other colors. User can identify which is the production server and which are non-production servers
before performing any activity.
• PerformIT service should be installed and running on the Application or Database server of
ARCON PAM.

## [p469]

www.arconnet.com|Copyright © 2025 469
1.
2.
3.
1.
2.
ACMO Screen
Admin can access Global Configuration to add values such as IP Address, Hostname, etc. all values
which we currently display in ACMO → My Access → My Services.
Based on admin selection, only those will be displayed in the User's Client Manager.
The user will have the option to set his preference which will be saved for his login.
To navigate, use the following path:
Settings → General
Select Server Type Configuration.
Select the add button to add a new Server Type Configuration.
The Administrator having Configure Server Tag type privilege in Server’s Privileges will only be able
to configure details in Server Type Configuration.
If Server Type is not created in the server type Configuration setting, it displays “Not Configured”
under the Server Type column in ACMO and if Server Type is configured in settings, then it displays
Tag color and Tag Value.

## [p470]

www.arconnet.com|Copyright © 2025 470
3.
4.
The Server Type Configuration screen contains the following fields:
Field Name Description
Tag Name Enter the server type name as the tag value to identify production/nonproduction
servers when attached to the service.
Color Choose colors for the respective tag value (server type).
Click on the three dots button, a palette is opened and which will show a list of
basic colors with a name to select. Basic colors to be shown are as
follows:
None - In case of admin wishes to disable this tag. Similar message to
display while deleting the tag as mentioned below.
BLACK #000000 RGB(0, 0, 0)
RED #FF0000 RGB(255, 0, 0)
MAROON #800000 RGB(128, 0, 0)
YELLOW #FFFF00 RGB(255, 255, 0)
OLIVE #808000 RGB(128, 128, 0)
LIME #00FF00 RGB(0, 255, 0)
GREEN #008000 RGB(0, 128, 0)
AQUA #00FFFF RGB(0, 255, 255)
TEAL #008080 RGB(0, 128, 128)
BLUE #0000FF RGB(0, 0, 255)
NAVY #000080 RGB(0, 0, 128)
PURPLE #800080 RGB(128, 0, 128))
Enter the details and click Save to create a new tag in Server Type Configuration.
For Editing, the details of the existing Server Type Configuration, click on the existing row and select
the Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.
Make sure that no two tag values have the same colors.

## [p471]

www.arconnet.com|Copyright © 2025 471
5.
6.
For Deleting the existing Server Type Configuration, click on the existing row and select the Delete
button at the top and make the required changes. Also, you can right-click on the row and select Delete.
The Export button will export all the Server Type Configuration details in the form .xlsx format. The
Copy button will copy all the details of the table.
4.3.7.14.4 Object Counter
What is Object Counter?
This section helps you to view or monitor different entities. It helps to view the count of the objects integrated
in ARCON PAM such as the count of services, server group, user group, profile, details of password change,
command log, and captured images in the ARCOSRDPDB database. In addition, it displays the count of all the
active and inactive objects integrated with ARCON PAM.
To view Object Counter:
To view the object counter use the following path:
General→ ARCOS Object Counter
The Administrator having ARCON PAM Object Counter privilege in Server's Privilege will only be
able to view and monitor different entities in ARCON PAM.

## [p472]

www.arconnet.com|Copyright © 2025 472
On refreshing, you can see the detailed screen.
4.3.7.14.5 Performance Monitoring
What is Performance Monitoring?
The Performance Monitoring feature provides users with the status of the server being accessed. The
functionality will show whether the server is up and running or not. The Performance Monitoring page will
display the IP Address, the current status, and the last updated Date and Time.

## [p473]

www.arconnet.com|Copyright © 2025 473
1.
2.
3.
To navigate, use the following path:
Settings → General
Select Performance Monitoring.
The Performance Monitoring Report will display the IP Address, The Current status of the User IP, and
the last updated status.
The Export button will export all the Performance Monitoring details in the form .xlsx format. The Copy
button will copy all the details of the table.
4.3.7.14.6 LOB Wise
LOB Wise, any defaults enabled under this section will ensure that any new configuration will be reflected and
assigned as per a particular LOB. For example, real-time session monitoring has to be manually enabled for
each LOB.
To navigate, use the following path:
Settings → General → LOB Wise
Field Name Description
LOB Wise User Management -
Is Enabled
This configuration enables/disables LOB Wise User Management.
Disable If Toggle value is 'Disabled', then all users will be displayed under Server
Manager > Manage Users and Server Manager > Manage > Maker’s
Checker irrespective of the selected LOB.
Enable If  Toggle value is 'Enabled', then users assigned to selected LOB will be
displayed under Server Manager > Manage Users and Server Manager >
Manage > Maker’s Checker.
The Administrator having Performance Monitoring Utility privileges in Server’s Privileges will only be
able to do configurations under Performance Monitoring.

## [p474]

www.arconnet.com|Copyright © 2025 474
Field Name Description
LOB Wise Workflow
Configuration - Is Enabled
This configuration sets whether Workflow should be configured LOB wise
or for all.
Disable If Toggle value is 'Disabled', then the “All” option will be available in LOB/
Profile drop-down.
Enable If  Toggle value is 'Enabled', then only LOB names will be available for
selection in  LOB/Profile drop-down in Server Manager > Settings
>Workflow >Raise Request > User Request Approval Workflow. Also
configured workflows will be displayed LOB wise.
LOB Wise Master And Manager
- Is Enabled
This configuration sets whether all or only LOBs assigned to logged in
user will be displayed under LOB Wise Master and Manager > Map LOB
tabs.
Disable then all LOBs will be available in the drop-down for selection.
Enable If  Toggle value is 'Enabled' (and “Add New LOB” privilege is not assigned)
then only those LOBs will be available in the drop-down which is assigned
to the user.
LOB Wise Real Time Session
Monitoring - Is Enabled
This configuration sets whether live sessions under Server Manager >
Tools > Real Time Session Monitoring should be displayed for all LOBs or
LOB Wise.
Disable If Toggle value is 'Disabled',  live sessions of all LOBs will be displayed.
Enable If  Toggle value is 'Enabled', then live sessions of single LOB will be
displayed.
LOB Wise Service Management
- Is Enabled
This configuration enables/disables LOB Wise Service Management.
Disable If Toggle value is 'Disabled', then Admin ID should assign newly created
service to required LOB under Server Manager > Manage > LOB/Profile
Master & Manager.
Enable If  Toggle value is 'Enabled', then newly created service will be directly
assigned to the selected LOB in Server Manager > Select LOB/Profile.

## [p475]

www.arconnet.com|Copyright © 2025 475
Field Name Description
LOB Wise Authorize Users This configuration sets whether Users will be displayed LOB wise in
Authorising User 1 and Authorising User 2 drop-down under Print
Password Envelope (SM > Manage > Password Manager) while
authorizing the password printing process for APEM Tool.
Note:
The LOB selected in Select LOB/Profile dropdown on the Server Manager
home screen will be considered while listing Users.
Disable If Toggle value is 'Disabled', then User from all LOBs will be listed.
Enable If  Toggle value is 'Enabled', then Users will be listed LOB wise.
4.3.7.14.7 Ticket.
This section explains the configuration of the inbuilt ticketing system within PAM, which can be used for
references under multiple service sessions by administrators.
To navigate, use the following path:
Settings → General → Ticket
Field Name Description
ARCOS Ticketing System - Is
Enabled
The users can enable or disable the ARCON ticketing system.
Disable If the Toggle value is ‘Disabled', the user can’t use the ARCON ticketing
system to raise tickets in the PAM application.
Enable If the Toggle value is 'Enabled', the user can use the ARCON ticketing
system to raise tickets in the PAM application.
Access Duration For Ticket
Access Request(in days)
The users can raise a service access request for the ticket within a
specified number of days.
Valid Values It ranges from 1-45 days.
The minimum value is 1 (default value), and the users shall be able to raise a
service access request only for a day. The maximum value is 45, the users
shall be able to raise a service access request for 45 days.
Max Hours For Ticket Session
Duration(in hours)
This configuration sets the maximum number of hours to be displayed in
the Expected Duration dropdown under Ticket Request (Client Manager >
My Access > Raise Request > Ticket Request).
Valid Values It ranges from 0-999. If the value '0' is selected then, the Expected Duration
dropdown will be displayed as blank.

## [p476]

www.arconnet.com|Copyright © 2025 476
4.3.7.14.8 Real Time Session Monitoring
What is Real Time Session Monitoring?
Real-Time Session Monitoring monitors the live feed of a session. ARCON|PAM Real Time Session Monitoring
feature enables monitoring, suspending, and terminating activities. You can quickly freeze, unfreeze or log out
the session to minimize any potential damage. It increases the control over the user's activity.
This section describes a couple of configurations that enable/disable different activities of Real-Time Session
Monitoring.
To navigate, use the following path:
Settings → General → Real-Time Session Monitoring
Field Name Description
Real Time Session Monitoring -
Is Enabled
This configuration sets availability of Real Time Session Monitoring under
Server Manager > Tools.
Disable If Toggle value is 'Disabled', then this option is not available.
Enable If  Toggle value is 'Enabled', then the option is available to view live sessions
accessed through ARCON PAM.
Real Time Session Monitoring
With Freeze / Unfreeze Session
- Is Enabled
This configuration sets the availability of Freeze and Unfreeze Session
options on Real Time Session Monitoring window when the live session is
accessed.
Disable If Toggle value is 'Disabled', then these options are not available.
Enable If  Toggle value is 'Enabled', then options are available.
4.3.7.14.9 Privileged User Discovery and Reconciliation
The Privilege User Discovery process is designed to be used when a resource is being deployed for the first
time or to run regular reconciliation as part of governance or compliance. The Privilege User Discovery process
allows the Administrator to quickly determine all the privileged accounts on the system and determine whether
the privileged identities are not present in PAM and provides a means to onboard them quickly. This
functionality can either be enabled or disabled using the following configuration:
To navigate, use the following path:
Settings → General → Privileged User Discovery and Reconciliation
Field Name Description
Privileged User Discovery &
Reconciliation - Is Enabled
This configuration sets the availability of Privileged User Discovery &
Reconciliation under Server Manager > Tools.
Disable If Toggle value is 'Disabled', then this option is not available.
Enable If  Toggle value is 'Enabled', then the option is available to discover users on
servers.

## [p477]

www.arconnet.com|Copyright © 2025 477
4.3.7.14.10 Maker Checker
The Maker-Checker setting ensures every user added by an administrator will have to be "checked" and
approved by another administrator user.
To navigate, use the following path:
Settings → General → Maker Checker
Field Name Description
User Maker Checker - Is
Enabled
This configuration enables the approval process of User creation using
Maker's Checker option. Every user added by an administrator will have to
be "checked" and approved by another administrator user.
Disable If Toggle value is 'Disabled',  then a new User will be created without the
approval process.
Enable If  Toggle value is 'Enabled', then a new User creation process will be
approved using Maker's Checker option.
4.3.7.14.11 Log Staging Server
To navigate, use the following path:
Settings → General → Log Staging Server
Field Name Description
ARCOS Staging Log Server - Is
Enabled
It enables or disables the ARCOS Staging Server.
Disable If Toggle value is 'Disabled', then it disables ARCOS Staging Server.
Enable If Toggle value is 'Enabled', then it enables ARCOS Staging Server.
4.3.7.14.12 Database
To navigate, use the following path:
Settings → General → Database
Field Name Description
Use ARCOS Web Service DT
For Database (Server Manager)
- Is Enabled
This configuration enables/disables routing of Server Manager connecting
to the Database server for sending audit logs from the Application Server.
Disable If the Toggle value is 'Disabled', then this feature disables routing.
Enable If the Toggle value is 'Enabled', then this feature enables routing.
If this value is enabled, no Direct port for the Database is required from the
Local system.

## [p478]

www.arconnet.com|Copyright © 2025 478
Field Name Description
Use ARCOS Web Service DT
For Database (Script Manager)
- Is Enabled
This configuration enables/disables routing of Script Manager connecting
to the Database server for sending audit logs from the Application Server.
Disable If the Toggle value is 'Disabled', then this feature disables routing.
Enable If the Toggle value is 'Enabled', then this feature enables routing.
If this value is enabled, no Direct port for the Database is required from the
Local system.
Use ARCOS Web Service DT
For Database (ARCOS Clients)
- Is Enabled
This configuration enables/disables the routing of Video Logs to the
ARCON PAM Database server from the Application Server.
Disable If the Toggle value is 'Disabled', then this feature disables routing.
Enable If the Toggle value is 'Enabled', then this feature enables routing.
If this value is enabled, no Direct port for the Database is required from the
Local system.
New Timer Update Mechanism
- Is Enabled
The available resources and the specific requirements of the video logs
determine the use of the timer update mechanism. When selecting a timer
update mechanism, the most important thing to consider is the accuracy of
the session duration tracking.
This configuration enables/disables the Timer Update Mechanism that
notices the resource's ideal time to provide the accuracy of the session
duration of the resource.
Disable If the Toggle value is 'Disabled', this feature disables the timer update
mechanism. The application will not notice the ideal time for the resources.
Enable If the Toggle value is 'Enabled', this feature enables the timer update
mechanism.
If this toggle is enabled, then the application will notice the ideal time for the
resources to provide the exact session duration.

New Timer Update
Mechanism(OFFLINE) - Is
Enabled
The most important thing to consider is the accuracy of the session
duration tracking while selecting a timer update mechanism (offline).
This configuration enables/disables the Timer Update Mechanism
(OFFLINE) that notices the offline connector’s ideal time to provide the
accuracy of the session duration of the resource.

## [p479]

www.arconnet.com|Copyright © 2025 479
Field Name Description
Disable If the Toggle value is 'Disabled', this feature disables the timer update
mechanism (offline). The application will not notice the ideal time for the
resources using offline connectors.
Enable If the Toggle value is 'Enabled', this feature enables the timer update
mechanism (offline).
If this toggle is enabled, then the application will notice the ideal time for the
resources using offline connectors to provide the exact session duration.
4.3.7.15 My Vault
4.3.7.15.1 File(s)
This section helps you with configurations to view passwords.
To navigate, use the following path:
Settings → My Vault → Files(s)
Field Name Description
Allowed File types for upload  This configuration, if blank will allow you to upload all file formats to My
Vault; if file formats are added only these added file formats will be
allowed to upload to My Vault.
Valid Values jpg, gif, png, txt, pdf are supported.
Upload all files to file vault This configuration sets the location for uploaded files in the file vault.
Disable If the toggle value is 'Disabled', then it uploads small files(file size less than
10MB) to the database and large files(file size greater than 10 MB) to file
server.
Enable If the toggle value is 'Enabled', then it uploads all the files to the file server.
4.3.7.16 Cloud
The section explains the various parameters that can be configured for achieving password rotation or
connections on various cloud platforms such as AWS and Azure. The cloud platforms added would require API
and credentials to authenticate. The cloud section lets the administrator configure these based on the below
parameters:
To navigate, use the following path:
Settings → Cloud
Click on Cloud Credential Configuration under Cloud. The following screen will be displayed:

## [p480]

www.arconnet.com|Copyright © 2025 480
1.
To configure cloud credentials in AWS:
To add new account credentials for AWS, click on Add button located at the top right corner of the
Amazon Web Services section. The following screen will be displayed:
Refer to the following table to understand the field-level details shown in the preceding screen:
Field Name Description
AWS Account ID  Specify the AWS account ID.

## [p481]

www.arconnet.com|Copyright © 2025 481
2.
3.
4.
1.
Field Name Description
AWS Policy Select the AWS policy from the dropdown.
AWS Access Key Specifythe AWS access key.
AWS Secret Key Specify the AWS secret key.
Description Enter the AWS account description.
Once all the required details are entered, click on Save. The AWS account will then be added to the
existing list.
For editing, the details of the existing AWS account credentials, click on the existing row and select the
Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.Similarly, for deleting the existing AWS account credentials, click on the existing row and select the
Delete button at the top. Also, you can right-click on the row and select Delete.
The Export button will export all the AWS account details in the form .xlsx format. The Copy button will
copy all the details of the table.
To configure cloud credentials in Azure:
To add new account credentials for Azure, click on Add button located at the top right corner of the
Microsoft Azure section. The following screen will be displayed:

## [p482]

www.arconnet.com|Copyright © 2025 482
2.
3.
Refer to the following table to understand the field-level details shown in the preceding screen:
Field Name Description
Azure Tenant ID Specify the Azure tenant ID.
Azure Role Select the Azure role from the dropdown.
Azure Subscription ID Specify the Azure subscription ID.
Azure Client ID Specify the Azure client ID.
Azure Client Secret Specify Azure client secret key.
Description Enter the Azure account description.
Once all the required details are entered, click on Save. The Azure account will then be added to the
existing list.
For editing, the details of the existing Azure account credentials, click on the existing row and selectthe
Edit button at the top and make the required changes. Also, you can right-click on the row and select
Edit.Similarly, for deleting the existing Azure account credentials, click on the existing row and select the
Delete button at the top. Also, you can right-click on the row and select Delete.

## [p483]

www.arconnet.com|Copyright © 2025 483
4. The Export button will export all the Azure account details in the form .xlsx format. The Copy button will
copy all the details of the table.
4.3.7.17 Configures
This section provides an overview of the various customizable parameters for the image and video log setup. It
covers the configuration options for different fields related to the session and settings for cloud storage
integration and management. These options allow users to tailor the logging process to their specific needs,
ensuring optimal performance and storage efficiency.
4.3.7.17.1 Image Log Configuration
What is Image Log Configuration?
The Image Log Configuration feature allows the user to customize the parameters associated with the image
logs that are to be recorded. These parameters include the Image Log Type, Image Log Quality, Watermarking,
Network Bandwidth Dependent Adaptive Image Quality, and Folder Structure. Consequently, the captured
images will bear the imprint determined by the user-defined values.
To navigate, use the following path:
Settings > Configure > Image Log Configuration
The following screen will be displayed:

## [p484]

www.arconnet.com|Copyright © 2025 484
Refer to the table below to understand the fields and data present in the image Log Configuration:
Field Description Default
Value
Image Log Type Select a color option from the drop-down value. Options are Colored, Black White,
and Gray Scaled)
Colored
Image Log
Quality
The quality of the image is based on the value set between 1-100,1 being the
lowest image quality and 100 being the highest. Select an image quality value from
the drop-down values.
Watermarking This toggle button enables/disables the standard ARCON footer to the video
captured during the session.
On
Network
Bandwidth
Dependent
Adaptive Image
Quality
This toggle button enables/disables the adaptive image quality of the network
bandwidth, basically adjusting image quality with a particular FPS.
On
Folder Structure Four checkboxes to set a folder structure such as LOB, YEAR, MONTH, and DAY.
As a value is checked, the corresponding entry appears in the below textbox. For
eg: if LOB is checked, <LOB>\ is added. Next, if YEAR is checked, then <YEAR>\ is
appended making the entire entry <LOB>\<YEAR>\
For Month - <MONTH>\, for Day - <DAY\
<LOB>\
4.3.7.17.1.1 Session Orchestrator Video Log
What is Session Orchestrator Video Log?
The Session Orchestrator Configuration allows the user to customize the values for various session-related
fields. These fields include the IP Address, TCP Port Number, WSS Port Number, Retry API Count, Working
The settings will be initialized for every value for which a Default Value should exist.

## [p485]

www.arconnet.com|Copyright © 2025 485
URL (API), Storage Folder Path, and Active status. Consequently, the video logs generated for the sessions will
reflect the specific details configured by the user in the Session Orchestrator.
To navigate, use the following path:
Settings →  Configure →  Image Log Configuration and Video Log Setup →  Session Orchestrator Video Log
Enable:
The following screen will be displayed:
Refer to the table below to understand the columns that are present in the Session Orchestrator Video Enable:
Column Name Description
Session Orchestrator Video Log Enable This configuration will enable/disable the Session
Orchestrator configurations.
Real Time Session Monitoring This configuration will enable/disable to view live sessions
accessed through ARCON PAM.
LOB Profile It allows the selection of the Line of Business (LOB)
associated with the session orchestrator, aiding in session
categorization based on organizational units or regions.
IP Address It displays the IP address of the configured Video Log Server,
facilitating communication between the session orchestrator
and the Video Log Server.
TCP Port Number It displays the port number utilized for communication in
Remote Desktop Protocol (RDP) sessions, enabling
interaction between the session orchestrator and the RDP
server.
The default port number is 8085

## [p486]

www.arconnet.com|Copyright © 2025 486
1.
Column Name Description
WSS Port Number It displays the port number utilized for secure communication
in Remote Desktop Protocol (RDP) sessions, which is used
when secure communication is necessary between the
session orchestrator and the RDP server.
Retry API Count It displays the number of attempts made to call the Video Log
API to retrieve video logs from a designated path, ensuring
reliable retrieval by allowing multiple attempts in case of
failure.
Working URL(API) It displays the URL utilized for accessing video logs,
facilitating efficient retrieval from the Video Log Server by
the session orchestrator.
Storage folder Path It displays the file path where video logs are stored, specifying
the server location where video logs are stored for future
access and reference.
Enabled It displays whether the Session Orchestrator Video is
enabled. It will display "YES" if enabled, or "NO" if not
enabled.
LOB Profile It displays the LOB profile selected from the dropdown list.
Storage Folder Type It displays the path where the videos are stored.
Add/Edit Session Orchestrator Video Log
Follow the below steps to add or edit the Session Orchestrator Video Log:
Click Add as illustrated below.
The default port number is 8086
Multiple RDPS Servers can be added for a selected LOB.

## [p487]

www.arconnet.com|Copyright © 2025 487
2. The Add/Edit popup screen will be displayed. Enter the required details and click Save.
Refer to the table below to understand the fields and data present in the Add/Edit screen:
Fields Description Default
Value
Enable This configuration will enable/disable the Session Orchestrator configurations. NA
LOB Profile Select a LOB profile from the drop-down values. NA

## [p488]

www.arconnet.com|Copyright © 2025 488
1.
Fields Description Default
Value
Session Orchestrator Setting
IP Address Enter the IP address for the instance. NA
TCP PORT Enter the IP TCP port number for the instance. NA
WSS PORT Enter the WSS port number for the instance. NA
Retry API Count Enter the number of times an API request is retried after a failure. NA
Storage Folder
Type
Enter the folder storage such as cloud or local etc.
Connector Configuration
Retry Interval Enter the retry count for RDPS API failures. 3
Session
Orchestrator
Retry Count
Enter the Connector Retry count for RDPS Connectivity failure. It can be with a
step counter of 1 increment/ decrement.
Working
API(URL)
Enter the Video log API URL which is hosted to get video on UI from the given
path.
NA
Storage Folder
Path
Enter the path where the videos will be stored. NA
Add/ Edit When a LOB is selected for which, an existing entry has not been made, then a
new entry is added for that LOB. API and Folder path are compulsory fields and
cannot be kept empty while adding.
When a LOB for which an entry exists is selected and the pre-filled values are
changed, the same entry will be edited while clicking this button. API and
Folder paths both are compulsory fields and cannot be empty while editing.
-
NA
After ARCON|PAM Administrator has configured the required configuration in Settings. Logs will be captured
Using RTSM.
Delete Session Orchestrator Video Log
To delete the Session Orchestrator Video Log, follow these steps:
Select any record from the grid and the Delete button is enabled.

## [p489]

www.arconnet.com|Copyright © 2025 489
2. Click Delete to delete the record.
4.3.7.17.1.2 Delta Image Capture Video Log
What is Delta Image Capture Video Log?
Delta Image Capture Video Log optimizes session logging by capturing only screen changes, reducing storage
usage, and supporting all connector types. Integrated with the Session Orchestrator, it ensures efficient video
logging, collaboration, and real-time session monitoring (RTSM). This allows users to view, store, and upload
delta images to local or cloud storage, including shared paths.
To navigate, use the following path:
Configure → Image Log Configuration and Video Log Setup →  Delta Image Capture Video Log Enable, and
the following screen is displayed.

## [p490]

www.arconnet.com|Copyright © 2025 490
1.
Refer to the table below to understand the columns that are present in the Delta Image Capture Video Log
Enable:
Column Name Description
LOB Profile It allows the selection of the Line of Business (LOB) associated
with the Delta Image Capture, aiding in session categorization
based on organizational units or regions
Working URL (API) It displays the API URL where the video logs are captured.
Storage Folder Path It displays the Path where the logs are stored.
Enabled It displays whether the Delta Image video Capture is enabled. It
will display "YES" if enabled, or "NO" if not enabled.
LOB Profile It displays the LOB profile selected from the dropdown list.
Storage Folder Path It displays the path where the videos are stored.
Add/Edit Delta Image Capture Video Log
Follow the below steps to add or edit the Delta Image Capture Video Log:
Click Add as illustrated below.

## [p491]

www.arconnet.com|Copyright © 2025 491
2. The Add/Edit screen will be displayed. Enter the required details and click Save.
Refer to the table below to understand the fields and data present in the Add/Edit screen:
Field Name Description
Enable This configuration will enable/disable the Delta Image Capture
Video Log.
LOB Profile Select a LOB profile from the drop-down values
Working URL(API) Enter the Video log API URL which is hosted to get video on UI
from the given path.

## [p492]

www.arconnet.com|Copyright © 2025 492
Field Name Description
Storage Folder Path Enter the path where the videos will be stored.
Storage Folder Type Enter the folder storage such as cloud or local from the dropdown
list.
4.3.7.17.2 Cloud Storage Configuration
The Cloud Storage Configuration allows the user to store RDPS Video logs on Cloud Storage (for example, S3/
Azure/GCP). The RDPS will be able to transmit video logs and images to the S3/Azure/GCP bucket.
To navigate, use the following path:
Settings > Configure > Cloud Storage Configuration
The following screen will be displayed:
Refer to the table below to understand the columns that are present on the Cloud Storage Configuration
screen:
Column Name Description
Cloud Storage Type It displays type of the Cloud Storage Configuration.
Cloud Storage Username It displays the username for the configuration.
Cloud Storage Region It displays the region of the configuration.
Cloud Storage Process ID It displays the process ID of the configuration.
IsActive It displays the Cloud Storage Configuration status whether it
is active or not.
Created By It displays the name of the user who has added the
configuration.
Created On It displays the date and time the particular configuration was
added.
4.3.7.17.2.1 Add/Edit Cloud Storage Configuration
Follow the below steps to add or edit a Cloud Storage Configuration:

## [p493]

www.arconnet.com|Copyright © 2025 493
1.
2.
Click on Add:
The Add/Edit popup screen will be displayed. Enter the required details and click on Confirm Changes:
4.3.7.18 PAM Plugin Configuration
An Auto-update PAM Plugin automates the PAM plugin update process. Previously, end users had to update to
the latest version of the PAM plugin manually. With this enhancement, the update process is now automated,
and the PAM plugin will be automatically updated when the end user accesses the ACMO URL.
4.3.7.18.1 Test PAM Plugin Release
This section helps to bulk upload users. Admins can click on "Download Sample Template" to download a bulk
sheet.

## [p494]

www.arconnet.com|Copyright © 2025 494
•
•
•
•
The bulk upload sheet consists of two columns: "Hostname_IPAddress" and "Entity Type."
In the "Hostname_IPAddress" column, the admin will enter the hostname or IP address.
In the "Entity Type" column, the admin will specify the corresponding entity type for which they want to
push the latest PAM plugin for testing purposes.
Click the Download Records to view the uploaded records.
4.3.7.18.2 Full PAM Plugin Release
Admins can enable the "Enable the PAM Plugin Update" toggle.
If enabled, the PAM plugin will automatically upgrade on all machines where the auto-upgrade PAM
plugin executable is available.
If disabled, the PAM plugin upgrade will occur only on the machines listed under Test PAM Plugin
Release.

## [p495]

www.arconnet.com|Copyright © 2025 495
4.3.7.18.3 Auto Update Logs
The Auto-update Logs  section provides administrators with a log of automatic updates applied to the PAM
plugin. The Auto-update Logs screen includes the From Date Time  and End Date Time  fields, allowing
administrators to filter logs within a specific time range. Additionally, it features a Select Status dropdown with
three options: Success, Fail, and In Process, enabling users to filter logs based on the status of the auto-update
process.
Refer to the table below to understand the columns present in Auto Update Logs:
Column Name Description
Host Name The name of the system where the PAM update was attempted.
Previous PAM Version The PAM version installed before the update
Updated PAM Version The target PAM version after the update.
Status The result of the update process.
Log Details Additional information or errors regarding the update process.
Performed On The date and time when the update attempt was made.

## [p496]

www.arconnet.com|Copyright © 2025 496
•
•
•
•
•
•
•
•
•
4.3.8 Logs Management
4.3.8.1 Overview
Logs capture all the activities performed in ARCON PAM with detailed information. It provides an audit trail for
transactions performed in Server Manager. It also provides detailed information on services accessed through
ARCON PAM. The Administrator can view them using the View Logs option.
4.3.8.1.1 This section includes the following topics:
Service Logs
Process Logs
Command Logs
User Access Logs
Service Password Status
User Activity Log
Envelope Logs
Import Utility Logs
MetaData/Text Logs
4.3.8.2 Service Logs
4.3.8.2.1 What are Service Logs?
Service logs help you to generate detailed logs of the services accessed by the user in the ARCON PAM
application. It displays details such as User ID, User Machine ID, Connection details, Service Reference
Number, other details, log-in and logout details of the service, session Log ID, the reason for accessing the
session, and logout status (reason for session termination). Users can export these logs to desired location if
required.
4.3.8.2.2 How to Generate Service Logs?
To generate service logs use the following path:
Manage → Logs → Service Logs
The Administrator, who is assigned privileges listed in Log Viewer in Server’s Privileges, can view logs.
•
•
The Administrator having View Service Log privilege in Server’s Privileges will only be able to
view Service logs. In addition, Administrator should have Download Video Log privilege, to
download video logs.
The Server Group Admin having View Command Log privilege in Group Admin Privileges, will
only be able to view Service Logs.

## [p497]

www.arconnet.com|Copyright © 2025 497
1.
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
Service Group Select the service group from the dropdown list.
User Group Select the user group from the dropdown list.
User ID Specify the user ID, to filter the logs.
IP Address Specify the IP address, to filter the logs.
Below are the steps to generate logs:
Select the fields and click on the View Log button. The logs are generated based on the selected filters.
The logs are filtered based on the user ID.
The logs are filtered based on the IP address.

## [p498]

www.arconnet.com|Copyright © 2025 498
2.
3.
4.
5.
6.
7.
Select the Check/Uncheck All checkbox to select/deselect all the details in grid view.
Select the checkboxes besides the service details, right click and select Export To PDF option, to export
logs to word document.
Select the checkboxes besides the service details, right click and select Download Video Log(s) option,
to download multiple video logs.
Right click on the selected service detail and choose Show Details option, to view video log.
Select the checkboxes besides the service details, right click and select Export To PDF (CLI) option, to
export logs to word document.
Click Show Details option. The Service Log Viewer screen is displayed.

## [p499]

www.arconnet.com|Copyright © 2025 499
8. View the video log.
4.3.8.3 Process Logs
4.3.8.3.1 What are Process Logs?
Process Logs helps you to view details of the processes executed on Windows Server when a service is
accessed through ARCON PAM. The processes executed on Windows Server are only viewed in Process Logs.
It displays details such as ID of the user who has logged in application, machine’s IP [MAC address], type of
service, service description, log type, timestamp, name of the process, and process title executed on server. The
generated logs can be exported to .xls format.
•
•
•
•
•
To export logs into .xls format, click on Export Data button, which is present in the bottom of
the screen.
Click Previous Log Set, to view set of previous logs.
Click Next Log Set, to view next set of logs.
Click Next Set of Log, to view particular set of logs. Select the particular set from the Next Set
of Log dropdown list.
Select the number of records from No of Records/Set dropdown list, wherein it will display
those many records in the grid

## [p500]

www.arconnet.com|Copyright © 2025 500
•
•
•
•
If type of the log is displayed as:
Activated: Session is active.
Inactivated: Session is closed.
Minimized: Session is minimized by user.
Maximized: Session is maximized by user.
4.3.8.3.2 How to generate process logs?
To generate process logs use the following path:
Manage → Logs → Process Logs
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, till when you want to generate logs.
•
•
The Administrator having View Process Log privilege in Server’s Privileges will only be able to
view Process logs. In addition, the Administrator should have Download Video Log privilege, to
download video logs.
The Server Group Admin having View Command Log privilege in Group Admin Privileges, will
only be able to view Process Logs.

## [p501]

www.arconnet.com|Copyright © 2025 501
•
•
•
•
•
1.
Field Name Description
Filter By Select the type of filter.
The valid values are:
User Name
User IP (MAC) Address
Server IP Address
Process Name
Process Title
Filter Value Specify the value, to filter the logs.
Follow below steps to generate process logs:
Select/Enter the fields and click on View Log button. The logs are generated based on the selected
filters.

## [p502]

www.arconnet.com|Copyright © 2025 502
2.
3.
4.
Right click on the windows service and choose Show Session Log option, to view video log.
Click Show Session Log option. The Log Viewer screen is displayed.
View the video log.
To export logs into .xls format, click on Export Data button, which is present in the
bottom of the screen.
Click Previous Log Set, to view set of previous logs.
Click Next Log Set, to view next set of logs.

## [p503]

www.arconnet.com|Copyright © 2025 503
4.3.8.4 MetaData/Text Logs
4.3.8.4.1 What are Meta Data/Text Logs?
The Metadata Log displays text logs generated from the video logs with the help of OCR (Optical Character
Recognition) technology. It extracts the textual metadata about the session. This log allows the administrator
to search for critical activity without viewing the complete video log. It displays the details such as User ID,
User Display Name, Service Type, Service Description, Application Name, Server Host, User Session Log ID,
MetaData/Text, Command Response, Command Logged in, Command Logged out, and a few more details of
the log.
4.3.8.4.2 How to generate Meta Data/Text Logs Logs?
To generate import service logs, use the following path:
ACMO → Server Manager → Manage → Logs → Meta Data/Text Logs
Click Next Set of Log, to view particular set of logs. Select the particular set from
the Next Set of Log dropdown list.
Select the number of records from No of Records/Set dropdown list, wherein it will
display those many records in the grid.
To capture the metadata log, you must enable the video log from the setting for that service type.
1.
2.
3.
4.
We support metadata logs for the following four connectors only:
SSMS for MS SQL
Toad for Oracle
SQL Navigator for Oracle
PL/SQL Developer for Oracle

## [p504]

www.arconnet.com|Copyright © 2025 504
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate
logs.
Filter By Select the required option.
Filter Value Specify the filter value, to filter the logs.
User ID Specify the user ID, to filter the logs.
Server IP Specify the IP address, to filter the logs.
Session ID Specify the session ID, to filter the logs.
Service User Name Specify the service username, to filter the logs.
The logs are filtered based on the user ID.
The logs are filtered based on the IP address.
The logs are filtered based on the session id.
The logs are filtered based on the username.

## [p505]

www.arconnet.com|Copyright © 2025 505
1.
2.
Follow the below steps to Access MetaData/Text Logs
Select/Enter the fields and click the View Log button. The logs are generated based on the selected
filters.
Click on the Show Details / Show Details All option to view more details.
4.3.8.5 User Activity Log
4.3.8.5.1 What is User Activity Log?
User Activity Log displays text and video logs for Session Monitoring (SM). The user activities such as creation,
modification, or deletion of files and User activities are captured under these logs.
These logs display details such as the name of the User, machine details of the User, IP Address of configured
Server, the application started on the Server, the action performed on the Server, session ID, and the date and
time details of the activity performed on Server.
4.3.8.5.2 How to generate User Activity Log in ACMO?
To generate User Activity Log use the following path:
ACMO → Server Manager → Logs → User Activity Log
The Administrator having User Activity Log privilege in Server’s Privileges will only be able to view
User Activity Log under Logs (ACMO> Manager > Session Monitoring > User Activity Logs)

## [p506]

www.arconnet.com|Copyright © 2025 506
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate
logs.
Filter By Select the required option.
Session ID Specify the session ID, to filter the logs.
Service User Name Specify the service username, to filter the logs.
User ID Specify the user ID, to filter the logs.
Service / Server IP Specify the IP address, to filter the logs.
Below are the steps:
The logs are filtered based on the session id.
The logs are filtered based on the username.
The logs are filtered based on the user ID.
The logs are filtered based on the IP address.

## [p507]

www.arconnet.com|Copyright © 2025 507
1.
2.
3.
Select/Enter the fields and click the View Log button. The logs are generated based on the selected
filters.
The user can view either Session Monitoring logs. By selecting Session Monitoring, the following screen
will appear.
By right-clicking on the record, the Show Session Log option will be displayed. By clicking on the same,
the Log Viewer screen will be displayed to view the video log.
4.3.8.6 Command Logs
4.3.8.6.1 What are Command Logs?
This section helps you to view the logs of the commands fired after connecting to the server. It displays details
such as User ID of the User who has logged in ARCON PAM, User Display Name, User Machine’s IP [MAC
address], type of Service, Service Description, Session Log ID, Command fired, Command Response, Command
Logged in and out timestamp. The generated logs can be exported to .xls format.
The mouse click activities performed by User on the Server are highlighted in red when you view
video logs.
•
•
•
The Administrator having View Command Log privilege in Server’s Privilege will only be able to
view Command logs. In addition, the Administrator should have Download Video Log privilege,
to download video logs.
The Server Group Admin having View Command Log privilege in Group Admin Privileges, will
only be able to view Command Logs.
To generate video logs for SSH services (Firewall, Switch, LINUX, Telnet etc.), configure the
value for SSH Video Log - Is Enabled For All as 1 in Global Configuration. The storage capacity
shall be maximum on the Server, where logs are generated.

## [p508]

www.arconnet.com|Copyright © 2025 508
•
•
•
•
•
•
•
4.3.8.6.2 How to generate Command Logs?
To generate command logs use the following path:
Manage → Logs → Command Logs
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
Filter By Select the type of filter.
The valid values are:
User Name
Server IP Address
User IP (MAC) Address
Command Fired
Command Response
User Groups
Service Groups
Filter Value Specify the value, to filter the logs.
Below are the steps:

## [p509]

www.arconnet.com|Copyright © 2025 509
1.
1.
Select/Enter the fields and click the View Log button. The logs are generated based on the selected
filters.
To view video of command logs:
Right-click on the command log, to view the video log. A Show Session Log option is displayed.

## [p510]

www.arconnet.com|Copyright © 2025 510
2. Click Show Session Log option. A window pops up.
3. Click View Video Log button. The Log Viewer screen is displayed.
4. View the video log.
You can view Video Logs for a selected set of commands. In Command Log Viewer screen, select the
required command, and click View Video Log button. The video will start from the selected command
till the end of the session.

## [p511]

www.arconnet.com|Copyright © 2025 511
4.3.8.7 ARCON PAM Logs
4.3.8.7.1 What are PAM Logs?
ARCON PAM Logs provides audit trail details for the activities performed in Server Manager. It generates logs
for all the activities performed by the users while using the application. The logs can be filtered based on the
type of object such as Group Transactions, User and Services Transactions, Transactions between User/User
Group, Service/Service Group, User/Service, User Group/Service Group, and User/Restrict Commands based
on the date. In addition, the logs can also be filtered based on the type of operations such as Created, Modified,
Deleted, Assigned, Revoked, Checker Approved, and Checker Not Approved. It displays details such as the
User ID of the User, type of object, type of operation, transaction for, old value, new value, and time stamp. The
generated logs can be exported to .xls format.
4.3.8.7.2 How to generate ARCON PAM Logs?
To generate ARCON PAM logs use the following path:
Manage → Logs → ARCON PAM Logs
•
•
•
The Administrator having View Command Log privilege in Server’s Privilege will only be able to
view Command logs. In addition, the Administrator should have Download Video Log privilege,
to download video logs.
The Server Group Admin having View Command Log privilege in Group Admin Privileges, will
only be able to view Command Logs.
To generate video logs for SSH services (Firewall, Switch, LINUX, Telnet etc.), configure the
value for SSH Video Log - Is Enabled For All as 1 in Global Configuration. The storage capacity
shall be maximum on the Server, where logs are generated.
•
•
•
The Administrator having View ARCOS Log privilege in the Server’s Privileges will only be able
to view ARCON PAM logs.
When Server is added to ServerGroup through workflow and the Global Configuration for
bulk mapping is enabled then ARCON PAM Logs for transaction between User and Service will
be generated.
Administrators having PAM Logs privilege can view ARCON PAM Logs in ACMO under the
Manager tab (My Apps)

## [p512]

www.arconnet.com|Copyright © 2025 512
1.
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
Object Type Select the type of object from the dropdown list.
Operation Select the type of operation from the dropdown list.
User ID Specify the user ID, to filter the logs.
Below are the steps:
Select the fields and click on the View Log button. The logs are generated based on the selected filters.
The logs are filtered based on the user ID.

## [p513]

www.arconnet.com|Copyright © 2025 513
2.
3.
4.
Right-click on the log. A Show Log Details and Show Audit Logs options are displayed.
The following are the two options:
Show Log Details: Displays details of the log selected.
Show Audit Details: Displays details of all the actions performed.
Click the Show Log Details option. The log details screen is displayed.
Click Show Audit Logs option. The audit details screen is displayed.

## [p514]

www.arconnet.com|Copyright © 2025 514
5. View the audit log details.
4.3.8.7.3 Reference Detail for Audit Trail
You can enable reference details for transactions performed in Advanced Configuration and User and Service
Management. These details help you to track references for transactions performed in ARCON PAM under
ARCON PAM Logs.
A Configuration Reference Details  window is prompted to the User when he performs any transaction in
ARCON PAM. You need to select the type of reference and enter its details. These details will be displayed in
ARCON PAM Logs along with the transaction details.
•
•
•
•
•
•
To export logs into .xls format, click on the Export Data button, which is present at the bottom
of the screen.
Click Previous Log Set, to view a set of previous logs.
Click Next Log Set, to view the next set of logs.
Click Next Set of Logs, to view a particular set of logs. Select the particular set from the Next
Set of Log dropdown list.
Select the number of records from the No of Records/Set dropdown list, wherein it will display
those many records in the grid.
ARCON PAM Logs can be viewed only for a maximum of 180 days at a time.
The configuration value for Reference Detail Required For Audit Trail - Is Enabled  under Global
Configuration  should be 1  for ARCON PAM to prompt Configuration Reference Details  window to
Administrator.

## [p515]

www.arconnet.com|Copyright © 2025 515
1.
2.
3.
4.
4.3.8.7.4 Configure reference details in ARCON PAM Logs
To configure reference details, use the following path:
Tools → Advanced Configuration → Default Configuration → Menu → Global Configuration
Select Reference Detail Required For Audit Trail - Is Enabled Configuration. Update this value as 1.
Now perform any transaction in Advanced Configuration or User and Service Management.
Example: Consider modifying User details under  Manage Users. Select a User, edit details under the
Create/Modify User  screen, and click Modify. The Configuration Reference Details  window will be
prompted.
Select the Reference Type  as New Ticket, Existing Ticket, or Other. Enter details in the Reference
Details text field.
Click OK. The transaction will be completed and transaction details along with reference details will be
captured in ARCON PAM Logs.

## [p516]

www.arconnet.com|Copyright © 2025 516
1.
2.
3.
4.
4.3.8.7.5 How to view the details?
To view details in ARCON PAM Logs, use the following path:
Manage → Logs → ARCON PAM Logs
Select or enter details in filters and click View Log.
Right-click on the log for which you had performed the transaction. A Show Log Details and Show Audit
Logs options are displayed.
Click the Show Log Details option. The log details screen is displayed.
Click the Show Audit Logs option. The audit details screen is displayed.

## [p517]

www.arconnet.com|Copyright © 2025 517
5. View the reference details displayed under Reference Type  and Reference Details  in the ARCOS Log
Details window.
4.3.8.8 User Access Logs
4.3.8.8.1 What are User Access Logs?
User Access Logs help you to generate the login and logout details of the user who has accessed the ARCON
PAM application. It displays details such as User ID details, IP Address, Logged in and out time, and type of user.
4.3.8.8.2 How to generate User Access Logs?
To generate User Access Logs use the following path:
Manage → Logs → User Access Logs
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
User ID Specify the user ID, to filter the logs.
Below are the Steps:
The Administrator having View User Access Log privilege in the Server’s Privileges will only be able to
view User Access logs.
The logs are filtered based on the user ID.

## [p518]

www.arconnet.com|Copyright © 2025 518
1. Select the fields and click the View Log button. The logs are generated based on the selected filters.
4.3.8.9 User Validity Status
4.3.8.9.1 What is User Validity Status?
User Validity Status helps you to generate details of all the users who are active or the ones who are
deactivated by the Administrator to access the ARCON PAM application. This helps the Administrator to
visually perceive all the details of the users. It gives the total time [in hours, days, forth nights, and years] the
user is active and the time he has been deactivated to access the application. It displays details such as User ID,
domain name, type of user, valid date and time with hours, days, forth nights, and years to access the
application and status of the user.
4.3.8.9.2 How to generate User Validity Status?
To generate User Validity Status use the following path:
Manage → Logs → User Validity Status
•
•
•
•
•
To export logs into .xls format, click on the Export Data button, which is present at the bottom
of the screen.
Click Previous Log Set, to view a set of previous logs.
Click Next Log Set, to view the next set of logs.
Click Next Set of Logs, to view a particular set of logs. Select the particular set from the Next
Set of Log dropdown list.
Select the number of records from the No of Records/Set dropdown list, wherein it will display
those many records in the grid.
The Administrator having View User Validity Status privilege in the Server’s Privileges will only be
able to view User Validity Status logs.

## [p519]

www.arconnet.com|Copyright © 2025 519
1.
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
User ID Specify the user ID, to filter the logs.
Show all deactivated Users (checkbox) Filter the logs of all the deactivated (inactive) users.
Below are the steps:
Select/Enter the fields and click the View Log button. The logs are generated based on the selected
filters.
The logs are filtered based on the user ID.

## [p520]

www.arconnet.com|Copyright © 2025 520
4.3.8.10 Service Password Status
4.3.8.10.1 What is Service Password Status?
Service Password Status Logs helps you to view the details of the service password status for the services in
ARCON PAM. It displays details such as the age of the password, last modified date of the password, the next
date to change the password, and the status of the password. In addition, if the status of the password is Open
then it also displays the details such as the date and time on which the password is opened, the days from when
the password is active, the name of the user who has viewed the password, and the type of the service.
4.3.8.10.2 How to generate Service Password Status log?
To generate the service password status log use the following path:
Manage → Logs → Service Password Status
The Filter screen contains the following fields:
•
•
•
•
•
•
Select Show all deactivated Users and click the View Log button to display inactive users.
To export logs into .xls format, click on the Export Data button, which is present at the bottom
of the screen.
Click Previous Log Set, to view a set of previous logs.
Click Next Log Set, to view the next set of logs.
Click Next Set of Logs, to view a particular set of logs. Select the particular set from the Next
Set of Log dropdown list.
Select the number of records from the No of Records/Set dropdown list, wherein it will display
those many records in the grid.
The Administrator having View Service Password Status Log privilege in the Server’s Privileges will
only be able to view Service Password Status logs.

## [p521]

www.arconnet.com|Copyright © 2025 521
1.
Field Name Description
Select Service
Group
Select Service Group
Service Type Select the Service Type
All Parts of Service Specify a keyword to search the available service type.
For example,
To search for a service type like WINDOWS RDP, specify the keyword as WIN, RDP or
NDO.
Follow the below steps:
Select the fields and click the View Log button. The logs are generated based on the selected filters.
To filter logs for a specific service group, select Select Service Group checkbox.
To filter logs for a specific service type, select Service Type checkbox.
If you want to filter details of all the services then you need to select All Parts of
Service checkbox. By default, All Parts of Service  checkbox is selected.
•
•
•
To export logs into .xls format, click on Export Data button, which is present in the bottom of
the screen.
Click Previous Log Set, to view set of previous logs.
Click Next Log Set, to view next set of logs.

## [p522]

www.arconnet.com|Copyright © 2025 522
4.3.8.11 Service Reference Logs
4.3.8.11.1 What are Service Reference Logs?
Service Reference Logs help you to generate details of reference numbers used before accessing services by
Users through ARCON PAM. It displays details of the User such as the ID of the User, machine IP, the type of
connection, service reference number, and the login–logout details of the service used.
4.3.8.11.2 How to generate Service Reference Logs?
To generate Service Reference Logs use the following path:
Manage → Logs → Service Reference Logs
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate logs.
User ID Specify the user ID, to filter the logs.
•
•
Click Next Set of Log, to view particular set of logs. Select the particular set from the Next Set
of Log dropdown list.
Select the number of records from No of Records/Set dropdown list, wherein it will display
those many records in the grid.
The Administrator having View Server Reference Log privilege in Server’s Privileges will only be able
to view Service Reference logs.
The logs are filtered based on the user ID.

## [p523]

www.arconnet.com|Copyright © 2025 523
1.
Field Name Description
Service Reference Number Specify the service reference number, to filter the logs.
Follow the below steps:
Select the fields and click on the View Log button. The logs are generated based on the selected filters.
4.3.8.12 Import Utility Logs
4.3.8.12.1 What are Import Utility Logs?
The Import Utility Logs helps to generate the detailed logs of the imported services in the ARCON PAM
Application. It displays the details such as Service IP Address, Service Hostname, Service Domain, Service
Instance, Service Port, Service Username, Service type, Import Log Message, Created by and Created on.
4.3.8.12.2 How to generate Import Utility Logs?
To generate Import Utility Logs use the following path:
The logs are filtered based on the reference number of a service.
•
•
•
•
•
To export logs into .xls format, click on the Export Data button, which is present in the bottom
of the screen.
Click Previous Log Set, to view a set of previous logs.
Click Next Log Set, to view the next set of logs.
Click Next Set of Logs, to viewa particular set of logs. Select the particular set from the Next Set
of Log dropdown list.
Select the number of records from the No of Records/Set dropdown list, wherein it will display
those many records in the grid.

## [p524]

www.arconnet.com|Copyright © 2025 524
1.
ACMO → Server Manager → Logs → Import Utility Logs
The Filter screen contains the following fields:
Field Name Description
From Select the start date, to generate logs.
To Select the end date, until when you want to generate
logs.
Filter By Select the required option.
Follow the below Steps:
Select the fields and click on the View Log button. The logs get generated based on the selected filters.

## [p525]

www.arconnet.com|Copyright © 2025 525
4.3.8.13 Envelope Logs
4.3.8.13.1 What are Envelope Logs?
The Envelope Logs helps you to generate detailed logs of the password generated for the authorized users. It
displays details such as the User ID, User Display Name, Service IP, Host Name, Domain Name, User Name, 1st
Authenticate User, 2nd Authenticated User, Envelope Status, and Timestamp.
4.3.8.13.2 How to generate the Envelope Logs?
To generate the envelope logs use the following path:
ACMO → Server Manager → Logs → Envelope Logs
The filter screen contains the following fields:
Field Name Description
From Select the start date, to generate the logs.
To Select the end date, until when you want to generate
the logs.
Service Type Select the service type from the dropdown list.
•
•
•
•
Click Previous Log Set, to view set of previous logs.
Click Next Log Set, to view next set of logs.
Click Next Set of Log, to view particular set of logs. Select the particular set from the Next Set
of Log dropdown list.
Select the number of records from the No Of Records/ Set dropdown list, wherein it will
display those many records in the grid.

## [p526]

www.arconnet.com|Copyright © 2025 526
1.
Field Name Description
Service / Server IP Specify the Service IP, to filter the logs
Follow the below steps:
Select/Enter the fields and click on the View Log button. The logs get generated based on the selected
filters.
4.3.9 Entity Management and Mapping
4.3.9.1 What is Entity Management and Mapping?
In ARCON PAM, the users are mainly the Administrators. These users use various kinds of services to access
privileged accounts. Hence, it offers a wide range of services and supports privileges to make the privileged
account secure and meet compliance regulations for these accounts. The various services created help to
implement, maintain, support, and control privileged identities with ease. Users can request access to these
services, which are to be approved by the Admin/Approver. The Administrator is responsible for managing
users. The users can be created, disabled, and modified through the User Management module. It includes
features such as Manage Users, Map Groups/Users, and Map Users/Services for managing and mapping users
and services. In addition, you can configure user groups to access various services, through group mapping.
•
•
•
•
Click Previous Log Set, to view set of previous logs.
Click Next Log Set, to view next set of logs.
Click Next Set of Log, to view particular set of logs. Select the particular set from the Next Set
of Log dropdown list.
Select the number of records from No Of Records/Set dropdown list, wherein it will display
those many records in the grid.

## [p527]

www.arconnet.com|Copyright © 2025 527
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
4.3.9.2 Why is Entity Management Needed?
Privileged access must be tightly controlled to prevent misuse and ensure security.
Mapping users to specific services ensures that only authorized individuals can access sensitive
resources.
Approval workflows for service access reinforce compliance and accountability.
Efficient management of user roles and groups simplifies administration in large environments.
It supports regulatory compliance by enforcing role-based access and access request governance.
This section includes the following topics:
LOB
User
Service
Groups
Mappings
Revoke and Share
4.3.9.3 LOB
4.3.9.3.1 What is LOB (Line of Business)?
Line of Business (LOB) is a general classification of operations used by the organization. A business describes
the set of products or services that are grouped under one department or team, based on factors planned by
the organization. ARCON PAM helps to segregate different users and services. For example, a company may
have a dedicated team working independently which can be segregated as a part of LOB. Therefore, different
users and services are segregated under one particular department/LOB. The LOB concept is true to support
multi-tenancy. LOB becomes a root for all the entities (Users, Services, User Group, and Server Group) when
integrated with ARCON PAM. These entities are then mapped to their respective LOBs.
4.3.9.3.2 Why is LOB (Line of Business) Needed?
It supports multi-tenancy, enabling different teams or departments to operate independently within a
shared PAM environment.
It improves organizational clarity by logically grouping users and services under their respective
business units.
It enhances access control by allowing policies, roles, and permissions to be scoped within a specific
LOB.
It simplifies administration and compliance, as entities can be managed and audited based on
departmental boundaries.
It scales well for large enterprises, where multiple business units require segregation of privileges and
resources.
The Administrator who is assigned privileges listed in Manage LOB/Profile in Server’s Privileges can
perform respective action in LOB/Profile Master & Manager.

## [p528]

www.arconnet.com|Copyright © 2025 528
•
1.
This Section includes the following topics:
Create LOB
4.3.9.3.3 Create LOB
This section explains the steps to create or modify details of LOB (Line Of Business). The Administrators
having the Add New LOB privilege shall only be able to create or modify details of a LOB.
4.3.9.3.3.1 How to Create a LOB?
To create a line of business use the following path:
Manage → LOB/Profile Master and Manager → Manage LOB
Click the Manage LOB tab. The Create/Modify LOB screen is displayed.
The Create/ Modify LOB screen contains the following fields:
Field Name Description
Create Select to create LOB.
Administrators, who have been assigned the Add New LOB privilege will be able to create new LOB
and view all the LOB’s in Select LOB/ Profile dropdown in Server Manager Home Page whereas
Administrators, who have not been assigned Add New LOB privilege will be able to view only those
LOB’s which are mapped to them.

## [p529]

www.arconnet.com|Copyright © 2025 529
2.
3.
Field Name Description
Modify Select to modify details of an existing LOB.
LOB Name Specify the name for LOB. The LOB name should be unique.
Short Name Specify a short name for LOB. The field is mandatory since the LOB short name
is used in Archival Service to fetch the recorded history videos. The LOB's short
name should be unique. The Short Name field is not editable in the LOB
modification screen.
Description Specify the description for LOB.
Address Specify the address of the LOB.
Report Header Specify the header name for the LOB report.
Is Active Enables the LOB once it is created.
Click Create. A window pops up with the following message, "New LOB Created".
Click OK. A new line of business is created.
4.3.9.4 User
4.3.9.4.1 What is a User?
A User is an entity that has the authority to use an application. Users shall be of two types, Client User and
Admin User. The Client type of User shall be responsible only for checking reports and accessing services. The
Client User will not have admin privileges to perform any admin activity in Server Manager whereas the Admin
User shall be able to perform all the activities in ARCON PAM.
•
•
Administrators having Modify LOB  privilege in Server’s
Privileges will only be able modify the LOB name, description,
address, and Report Header of the existing LOB.
To modify the details of the LOB, select the required LOB from
the grid on the left pane. The LOB details are displayed
under Create/Modify LOB pane on the right side. The Short
Name field is not editable in the LOB modification
screen. Modify the required details and click Modify, to update
the details.

## [p530]

www.arconnet.com|Copyright © 2025 530
•
•
•
•
•
•
•
•
•
•
1.
While Logging into ARCON PAM, the Admin/Client type of User shall select the respective domains (AD
Domain/ Local Domain) for authentication. The Users authenticated from Active Directory shall be called
Domain Users whereas, the Users authenticated from local Domain are known as Local User.
Domain User: A domain User is a User whose username and password are stored on a domain controller
rather than the computer through which the User is logging into. When you log in as a domain User, the
computer asks the domain controller what privileges are assigned to you. When the computer receives
an appropriate response from the domain controller, it logs you in with the permissions and restrictions.
Local User: A local User is one whose username and encrypted password are stored on the computer
itself. When you log in as a local User, the computer checks its own list of Users and its own password file
to see if you are allowed to log into the standalone computer.
4.3.9.4.2 Why is User Important?
It ensures access control by clearly defining user privileges based on their roles (Admin vs. Client).
Domain-based authentication provides centralized user management, making it easier for organizations
to control access and enforce policies.
Local authentication offers a fallback or isolated access option, useful in environments where domain
services are not available or for standalone deployments.
The separation between Client and Admin roles enhances security and accountability, reducing the risk
of privilege misuse or unauthorized changes.
4.3.9.4.2.1 This section includes the following topics:
User Creation Approval Process
Modify details of User
User Access Control
User Creation Approval Process
4.3.9.4.3 User Profile
This section helps you to copy the user profile of a particular User to another User. You can copy entities such
as LOB, User Group, Services, Commands, or Processes.
4.3.9.4.3.1 How to Copy the User Profile?
To copy the user profile use the following path:
Manage → Users and Services → Manage Users
Right click on the User name from the User Display Name list. A multiple-options list is popped up.
The Administrators having Read Only Access privilege (under Manage User) can view details
displayed under Manage Users and Map Groups/Users tab.
The Administrator having Copy User Profile privilege shall only be able to copy a user profile from one
User to another User.

## [p531]

www.arconnet.com|Copyright © 2025 531
2.
3.
4.
5.
Click the Copy User Profile option.
Now select another user to copy the User Profile.
Right click on the User name from the User Display Name list. A multiple-options list is popped up.
Click the Paste User Profile option. A confirmation box is displayed with the following message.
Do You Want To Perform this Operation?

## [p532]

www.arconnet.com|Copyright © 2025 532
6.
7.
a.
b.
c.
d.
e.
Click the Yes button. The following Copy Paste User Profile screen is displayed.
Select the required check box against the options. The following entities can be selected on the Copy
Paste User Profile screen.
Copy LOB
Copy User Group
Copy Services
Copy Commands
Copy Process

## [p533]

www.arconnet.com|Copyright © 2025 533
f.
g.
h.
8.
9.
10.
Copy ACMO Privileges
Copy ASM Privileges
Copy Group Admin Privileges
Select the required options and click the Submit button.
The following success message will be displayed.
User Profile Copied Successfully...
Click the OK button. The selected options will be copied to the User.
4.3.9.4.4 User Creation Approval Process
4.3.9.4.4.1 What is User Creation Approval Process?
A User is an entity that has the authority to use an application. There are two types of users: Client Users and
Admin Users. When logging into ARCON PAM, the Admin/Client type of User selects the respective domains
(AD Domain/ Local Domain) for authentication. Users authenticated from Active Directory are called Domain
Users, whereas Users authenticated from the local Domain are known as Local Users.
User Creation Process
The process of User Creation and Approving this process is given below.
Click the Cancel button to close the window
•
•
•
The Administrator having Add User privilege will be able to create a User.
The Domain User created must be present in the Active Directory. The User is then
authenticated using Active Directory while logging into the application.
If User Maker Checker-Is Enabled is enabled in Settings, then the User created will be sent for
approval to the Checker, whereas if Disabled, then the User will be directly created in ARCON
PAM without the approval process.

## [p534]

www.arconnet.com|Copyright © 2025 534
1.
4.3.9.4.4.2 How to Create Domain or Local User?
Domain and Local Users are created from Manage Users.
The following steps are used to create a Domain or Local User:
To create a User, use the following path:
Server Manager → Manage → Users and Services → Manage Users
2. The Create/Modify User screen contains the following fields:0
Field Name Description
Create (radio button) Select to create a new User.
Modify (radio button) Select to modify details of an existing active User.
•
•
For Domain Users, you need to enter the User ID in the User ID text field, select the Domain
Name from the Domain Name dropdown list, and then click the […] icon beside the User
Display Name text field to fetch the details of the User from the Active Directory.
To search a specific set of rows, enter keywords (space separated) on the column's header, and
the relevant rows are pulled out.
To modify the details of the User, select the required User from the grid
on the left pane. The User details are displayed under the Create/
Modify User pane on the right side. Modify the required details and
click the Modify button, to update the User details.

## [p535]

www.arconnet.com|Copyright © 2025 535
•
•
Field Name Description
User Display Name Specify the name of the User.
User ID Specify the ID of the User.
Domain Name Select the local domain or Active Directory (AD) domain from the dropdown list.
Password Specify the password.
Confirm Password Re-enter the password to confirm that the entered password matches the
previous password entered.
User Type Select the type of the User. The valid values are:
Client
Admin
Email ID  Specify the Business Email ID.
Mobile No Specify the Business Mobile Number.
For Domain User, the data in this field is auto-populated, once you enter
the User ID select the Domain Name from the dropdown list and then
click the […] icon beside the User Display Name text field.
•
•
For Domain Users,
The data in this field is auto-populated, once you enter the User
ID select the Domain Name from the dropdown list and then
click the icon beside the User Display Name text field.
The […]  icon verifies the domain name from the AD and if it
successfully verifies the domain name, it fetches and displays the
name in the User Display Name field. If the verification fails, then
an error message “Server was unable to process request….. No
Users Found on Domain With Specified User Name” is
displayed.
For Domain Users, The data in this field is auto-populated, once you
enter the User ID select the Domain Name from the dropdown list and
then click the icon beside the User Display Name text field.
Email IDs which is starting with "_" (Underscore) can be added. For Ex -
_John_sn@mail.com.

## [p536]

www.arconnet.com|Copyright © 2025 536
Field Name Description
Valid Till Date Select the end date. This is the date from which the User will be inactive to access
the application.
Department
**Customized field
Select the Department of the User from the dropdown.
Blood Group
**Customized Field
Select the Blood Group of the User from the dropdown.
Country
**Customized Field
Specify the name of the country the user belongs to.
State
**Customized Field
Specify the name of the state in the country the user belongs to.
This field is enabled, once you select the Enable checkbox.
•
•
This field name and the values in the dropdown are bespoke and
can be set according to an organization's needs.
This can be set in Configure User Tag in Settings.
•
•
This field name and the values in the dropdown are bespoke and
can be set according to an organization's needs.
This can be set in Configure User Tag in Settings.
•
•
The field name is bespoke and can be set according to an
organization's needs.
This can be set in Configure User Tag in Settings.
•
•
The field name is bespoke and can be set according to an
organization's needs.
This can be set in Configure User Tag in Settings.

## [p537]

www.arconnet.com|Copyright © 2025 537
Field Name Description
Drop Button Click Drop, to disable the User in ARCON PAM.
3. Enter or select the details and click Create to initiate the User creation process.
4.3.9.4.4.3 User Approving Process
Approving new Users can be done through Maker Checker or ARCOS Workflow Approval Matrix.
Approving User through Maker Checker
Maker-Checker is one of the central principles of authorization in ARCON PAM. The maker-checker concept
means that for each request sent by the User/Administrator, there shall be at least two individuals or two levels
of authority to complete the User Creation process. A maker is an individual who shall create a user and the
checker is an individual who shall be involved in confirming/authorizing the user created by the maker.
•
•
Administrators having Drop User privilege will be able to disable
a User.
To drop a User, select the required User from the grid on the left
pane. The User details are displayed under the Create/Modify
User pane on the right side. View the details and click Drop, to
disable the User.
•
•
If the User Maker Checker configuration is enabled in Settings, then the User will be displayed
in Administrator's Maker’s Checker. Whereas, if this configuration is not enabled, then ARCON
PAM will check whether User Transaction (Object Type) for Creation (Operation Type) is
enabled in the ARCOS Workflow Approval Matrix. If it is enabled, then an Approval Email will
be sent to the configured User's email ID.
If User Maker Checker configuration is enabled in Settings and User Transaction for Creation
is enabled in  ARCOS Workflow Approval Matrix, then User approval will be through the
Maker Checker process.
•
•
The Administrator having Approve User (Checker) privilege will only be able to approve or
reject newly created Users.
The Send Alert To All Checker When Maker Creates New User configuration
under Settings sets whether an alert will be sent to all Checkers when Maker creates a new
User
If the toggle value is disabled then the alert will not be sent to any Administrator, but the
request will be displayed in Maker’s Checker screen of Admins having Approve User
(Checker) privilege.
If the toggle value is enabled then the alert will be sent to Administrators having Receive
Alert On User Creation By Maker and Approve User (Checker) privilege.

## [p538]

www.arconnet.com|Copyright © 2025 538
1.
2.
3.
4.
5.
1.
4.3.9.4.4.4 How to Approve User from Maker’s Checker?
Follow these steps to Approve User from Maker's Checker:
To approve a domain or local User use the following path:
Server Manager → Manage → Maker’s Checker
Click the Maker’s Checker sub-menu. The User Maker’s Checker screen is displayed.
To approve the User created, select the checkbox in the User Display Name column.
Click the Approve New User link. A window pops up with the following message:
Selected Users Have Been Checked Successfully.
Click OK. The User created is approved successfully.
4.3.9.4.4.5 How to Approve User from Approval Link?
ARCOS Workflow Matrix helps you to configure approval levels for transactions performed in ARCON PAM.
You should configure User Transaction of Creation Operation Type to send email notification to approvers for
approving new created User.
The following steps are used to Configure Workflow and Approve request:
To navigate to the ARCOS Workflow Approval Matrix, use the following path:
Server Manager → Tools → Advanced Configuration → ARCOS Workflow Approval Matrix
•
•
To reject the request raised by Maker, click the Do not Approve New User button.
Once the request is approved or rejected by the Checker/Approver, an alert notification is sent
to the User. The notification is only sent to the User who is configured to receive notifications
in Alert and Notification Configuration. For more information, refer Alert and Notification
Configuration section from Tool Management.

## [p539]

www.arconnet.com|Copyright © 2025 539
•
•
•
•
•
•
The Approval Matrix screen contains the following fields:
Field Name Description
Object Type Select the type of object. The valid values are:
User Transactions: Used for creation, deletion, modification of User's.
Service Transactions: Used for creation, deletion, modification of Services.
Transaction Between User and User Group: To map User(s) with their
respective User Groups.
Transaction Between Service and Service Group:To add or remove
services to/from their respective Server Group.
Transaction between User And Service: To assign or revoke Services to/
from User's.
Transaction Between User Group And Service:To map or remove User
Group to/from Service Group and vice versa.

## [p540]

www.arconnet.com|Copyright © 2025 540
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
1.
Field Name Description
Operation Type Select the type of operation. The valid values are:
Created
Modified
Deleted
Assigned
Revoked
CheckerApproved
CheckerNotApproved
Accessed
Viewed
Shared
Un-Shared
Approver Levels Select the levels of approval for the selected object type.
The valid values are:
Is Active Enable the configuration for approval.
LOB/ Profile Select the LOB/Profile.
Service Group Select the service group.
User Group Select the user group.
Description Specify the description for the selected object type.
Between Specific Time To set the specific time for approval.
Approvers Select the name of the approver to approve the request.
Follow the below steps
Select/Enter the fields and click Create to create Workflow.
You can select up to 5 levels of approval.
For the User ID’s to appear for selection in the drop box, the Users in
ARCON PAM needs to have email ID’s configured in user settings.

## [p541]

www.arconnet.com|Copyright © 2025 541
2.
a.
b.
c.
When a User is created under the Manage Users tab, an approval email will be sent to the Approver.
Example: Below is an example of the User creation approval process through the Workflow Matrix.
User 'Jack' is created under the Manage Users tab.
The approval link is sent to the Approver configured in the ARCOS Workflow Approval Matrix.
To approve/reject a request using the link, click on the Click here to Approve / Reject link sent on
email. The following login screen will be displayed.
To approve/reject a request, the approver can click link given in email or can reply to the
above mail received in their inbox. The approvers will have to reply with the
content #Approve# or #Reject# to approve/reject the request.

## [p542]

www.arconnet.com|Copyright © 2025 542
d.
e.
f.
Login into the ARCON PAM Workflow web console. The following details are displayed for
approval.
Enter comments and click Approve Transaction to approve the User creation process.
A similar email will be sent to all Approvers. The User will be created when all approves the
transaction.
Click Reject Transaction to reject User Creation.
Once a User is successfully created, you need to then map the user to a particular LOB. In some cases,
wherein an Administrator having Settings privileges has configured the value for LOB Wise User
Management option, where

## [p543]

www.arconnet.com|Copyright © 2025 543
•
•
•
•
4.3.9.4.4.6 Process Flow Diagram
Following is the process flow diagram of the User Creation Approval Process.
4.3.9.4.5 User Access Control
4.3.9.4.5.1 What is User Access Control?
Access control is a security technique that can be used to regulate who can view or use resources in a
computing environment. Access control systems perform authorization identification, authentication, access
approval, and accountability of entities through login credentials including passwords, personal identification
numbers (PINs), biometric scans, and physical or electronic keys.
User Access Control is a security feature, which helps to prevent unauthorized changes to your computer.
These changes can be initiated by applications, viruses, or other users. User Access Control module makes sure
that these changes are made only with approval from the Administrator. This section allows to enable the user
login period, disable the user login, session lockout, endpoint-based access, and to enable or disable the dual
authorization factor for user(s).
4.3.9.4.5.2 Why is User Access Control Important?
It protects systems and data from unauthorized access, reducing the risk of breaches or misuse.
It ensures that only verified and authorized users can make system-level changes, helping prevent
malware or insider threats.
It enforces organizational security policies, like restricting access by time or location.
It improves operational security, by adding layered defense mechanisms like dual-factor authentication
and endpoint validation.
•
•
LOB Wise User Management - Is Enabled toggle value is set to Disabled, it states that when a
user is created, it will directly map the user to the selected LOB in the Select LOB/
Profile dropdown list, once it is created.
LOB Wise User Management - Is Enabled toggle value is set to Enabled, it states that the user
created needs to be mapped to a particular LOB in LOB/Profile Master & Manager.
By default, the toggle value is Enabled.
The Administrator having Edit User Settings privilege shall only be able to edit User settings.

## [p544]

www.arconnet.com|Copyright © 2025 544
1.
2.
3.
4.3.9.4.5.3 How to Access Manage Users?
To navigate, use the following path:
Manage → Users and Services → Manage Users
Select a User and right-click on the record. A dropdown list is displayed.
Click the Edit User Settings option.
The User Settings screen is displayed.

## [p545]

www.arconnet.com|Copyright © 2025 545
4.
a.
b.
c.
The User Settings screen contains the following tabs:
Security Setting
Access Control Setting
Endpoint-Based Access Setting
4.3.9.4.5.4 Access Control Setting
What is Access Control Setting?
Access control is a security technique that can be used to regulate who can view or use resources in a
computing environment. Access control systems perform authorization, identification, authentication, access
approval, and accountability of entities through login credentials including passwords, personal identification
numbers (PINs), biometric scans, and physical or electronic keys.
Access Control Setting helps to enable or disable the user logon period. In addition, it allows to decrease or
increase the session lock-out time, disable lockout attempts (Devoid Security), enable/disable user logon
access, and enable endpoint-based access for user(s).

## [p546]

www.arconnet.com|Copyright © 2025 546
The Access Control Setting tab contains the following fields:
Field Name Description
Enable Logon
Period
Enable the number of days and hours for the selected user to access the application.
Use Global Session
Lock Out
Decrease or increase the session lock out time in minutes for the selected user.
Devoid Security Disable lockout attempts for the selected user.
Disable Logon Disable the logon access for the selected user.
Enable Endpoint
Based Access
Enable the endpoint based access, which allows access to the application through the
specified desktop or laptop only.
Restrict Clipboard
through AGW
Enable or Disable the user from using the Copy-Paste Option through AGW.
•
•
If a user tries to login into ARCON PAM application after the set logon
period is expired, then the user will receive an error message displaying
“Invalid User Name OR Password”.
Once the logon period is selected, click Allow Logon, to enable the logon
period and click Disable Logon to disable the logon period.
By default, Use Global Session Lock Out is enabled.
If Enable Endpoint Based Access checkbox is selected, then you need to enter
the IP or MAC address, Processor or BIOS Serial ID details of the laptop or
desktop in the Endpoint Based Access Setting tab.

## [p547]

www.arconnet.com|Copyright © 2025 547
1.
2.
Follow the below steps to configure Access Control:
Select the required access control settings and click Confirm Changes button. A window pops up with
the following message:
Access Control Setting Successfully Configured.
Click OK to configure the access control settings for the selected user.
4.3.9.4.5.5 Endpoint Based Access Setting
What is Endpoint Based Access Setting?
Endpoint Based Access Setting is an approach that helps to identify and manage the user’s computer to gain
access to the network. This involves the Administrator restricting certain access to the user to maintain and
comply with the organization's policies and standards. ARCON PAM binds the user(s) login to a particular
system’s IP address, MAC Address, Process ID, or BIOS Serial ID of a desktop or laptop. Hence, the users will be
able to log into only those endpoint machines to which it is bound to.
How to Add/Edit Endpoint Based Access Setting?
The Add/ Edit frame contains the following fields:

## [p548]

www.arconnet.com|Copyright © 2025 548
•
•
•
•
1.
2.
3.
1.
Field Name Description
Filter Type Select the type for endpoint configuration.
The valid values are:
IP Address
MAC Address
Processor ID
BIOS Serial ID
Detail Specify the details based on the selected type of endpoint configuration.
Is Active
(checkbox)
Enable the configuration for desktop or laptop who’s details are specified.
Follow the below steps:
Click Add. A window pops up with the following message:
Endpoint Filter Added Successfully.
Click OK. The Endpoint Based Access setting for the specified desktop or laptop is added successfully.
Click Get Last 10 Days Login Details, to view the last 10 days login details of the User.
4.3.9.4.5.6 Security Settings
User Security Settings is a dual authentication process, wherein the user is authorized twice in ARCON PAM,
after which the user can get access to the application, making it more secure.
How to Edit Security Settings?
To edit user settings use the following path:
Manage → Users and Services → Manage Users
Right-click on the User Name from the User Display Name list. A multiple-options list is popped up.

## [p549]

www.arconnet.com|Copyright © 2025 549
2. Click the Edit User Settings option. The User Settings screen is displayed.

## [p550]

www.arconnet.com|Copyright © 2025 550
1.
2.
3.
Configure TOTP Authentication
What is TOTP Authentication?
Time-based One-time Password (TOTP) Authentication is a robust multi-factor authentication type that adds a
formidable layer of protection to your account. It works on a simple premise where the login tokens are formed
by mixing a secret key with the current time interval to generate the OTP. So, it is necessary that the system
times are synchronized. The generated OTP is validated by the server within the time frame, a successful
validation will be given to access ARCON PAM. If the validation is unsuccessful, a connection to ARCON PAM
will not be established. TOTP authentication has an edge over others as it works without an internet
connection and does not rely on cell phone coverage and roaming. Moreover, it offers users the flexibility to
choose from a range of authentication applications like Google Authenticator, Microsoft Authenticator,
Symantec VIP Authenticator, etc.
Pre-requisites
Access to smartphones that are capable of generating OTP. A smartphone is required because the users will
have to download the TOTP generator app. Some of these apps are as follows:
Google Authenticator
Microsoft Authenticator
Symantec VIP Authenticator
All of these authenticators work similarly, so the configuration and operation will be demonstrated using one
example.
Let us consider Microsoft Authenticator.
Download and install the Microsoft Authenticator App from the Google Play Store on your mobile to configure
mobile TOTP dual-factor authentication.

## [p551]

www.arconnet.com|Copyright © 2025 551
1.
2.
How to Enable Dual Factor Authentication - TOTP?
To enable TOTP dual-factor authentication perform the following steps on server manager for the following
path :
Manage → Users and Services → Manage Users
Select the user for whom the TOTP Based authentication should be displayed during login from ACMO.
Right click on the User name from the User Display Name list. A multiple options list is popped up.

## [p552]

www.arconnet.com|Copyright © 2025 552
3.
4.
Click on Edit User Settings menu this will show a new window for User setting.
Click on the Dual Authorization Factor Type drop-down list this will populate list. At the end of the list,
TOTP Authenticator list entry should be displayed.

## [p553]

www.arconnet.com|Copyright © 2025 553
5. Download Microsoft Authenticator in your android phone. After downloading this application, open it,
and scan the QR code. After scanning the new account gets added in your QR code application and
respective time-based OTP is generated in your mobile application.

## [p554]

www.arconnet.com|Copyright © 2025 554
6.
7.
Enter this OTP in the textbox and click on the validate and save button after successful validation.
Select on Enable Dual Factor Type checkbox. It enables the Confirm Status button.

## [p555]

www.arconnet.com|Copyright © 2025 555
8.
9.
10.
11.
1.
2.
Enforce Self Registration button displays the Account Details.
If you select Enforce Self Registration then the following popup appears. Clicking on the Confirm
Changes button a confirmation dialog box appears with a yes/no option. Click on yes to save the
settings.
After Enforcing Self Registration TOTP Authenticator. Click on Ok button
The Self Registration Enforced is displayed in the Account Details.
How to Post TOTP Configuration?
Go to the ACMO Login page. Enter the credentials in the ARCON PAM Login screen and click Login,
The TOTP Validator pop-up is displayed.
Enter the generated OTP from the configured Microsoft Authenticator application.
•
•
Only Admins have access to Enforce Self Registration.
The enforce self registration the end user to register when accessing the first time post this
MFA is applied by scanning the QR code and entering Secret Key. This reduces the
Administrator overhead as the admin now needs to only enable the MFA and not perform any
validation from the Server Manager module.

## [p556]

www.arconnet.com|Copyright © 2025 556
3.
4.
5.
Users for whom the Enforce Self Registration was enabled, the Account Name  and Secret Key are
visible after the user name and password are entered,
Scan the QR code and enter the TOTP which is generated in the Microsoft Authenticator application.
Successful authentication will direct you to the landing page.
If your OTP is correct but the password is wrong then the following message “Invalid User
Name Or Password” is displayed and the user remains on the same page.

## [p557]

www.arconnet.com|Copyright © 2025 557
•
•
•
•
•
1.
Configure Mobile OTP
What is Dual-Factor Authentication with Mobile OTP?
Static passwords for authentication have quite a few security drawbacks such as passwords can be guessed,
forgotten, written down and stolen, eavesdropped or deliberately being told to other people. A better, more
secure way of authentication is called "dual-factor" based on one-time passwords. Mobile one-time password
(OTP) configuration is one of the dual-factor authentication. Mobile users use it by implementing the
application on mobile, in order to log into ARCON PAM securely.
Why is Dual-Factor Authentication via Mobile OTP Important?
Static passwords are vulnerable to theft, sharing, or guessing, making them a weak form of
authentication.
2FA significantly enhances security by adding a second layer of verification.
Mobile OTPs are dynamic and expire quickly, making them resistant to reuse and harder for attackers to
exploit.
It reduces the risk of unauthorized access, even if a user's password is compromised.
It helps meet compliance requirements for secure authentication in privileged access environments.
Pre-requisite
Download and install the ARCON  App from the Google Play Store to configure mobile OTP dual factor
authentication.

## [p558]

www.arconnet.com|Copyright © 2025 558
2. Enter a Passcode for first login attempt and re-enter passcode to confirm on your mobile device.

## [p559]

www.arconnet.com|Copyright © 2025 559
3.
a.
b.
c.
d.
1.
The above screen will be displayed on re-entering the password, the screen will have the following
details
Unique ID : To be entered in server manager
Validation key: To be entered in Server Manager
Validation code : Encrypted format
Validation Password:
How to Enable Dual Factor Authentication - Mobile OTP?
To enable dual factor authentication Mobile OTP use the following path on server manager:
Manage → Users and Services → Manage Users
Right-click on the User name from the User Display Name list. A multiple-options list is popped up.

## [p560]

www.arconnet.com|Copyright © 2025 560
2.
3.
4.
Click Edit User Settings option. The User Settings screen is displayed.
Select the Dual Authorization Factor Type as Mobile OTP  and click the Enable Dual Factor Type
checkbox.
Enter the Unique ID displayed on the App (explained in pre-requisite Step 3a)  in the Unique ID text
field.

## [p561]

www.arconnet.com|Copyright © 2025 561
5.
6.
7.
8.
Click Validate Unique ID link to validate the Unique ID number.
If Unique ID is not valid, then it displays an error message Unique ID Invalid.
On successful validation, the Validation Key filed under Phone Validation will be enabled.
Enter the Validation Key displayed on the mobile screen (explained in pre-requisite Step 3b) .

## [p562]

www.arconnet.com|Copyright © 2025 562
To enter new validation key, click on New Validation Key button.

## [p563]

www.arconnet.com|Copyright © 2025 563
9.
10.
11.
Click Generate Validation Password button. The validation password is displayed in the Validation
Password text field.
Enter the Validation Password displayed on the Server Manager in the Validation password field of the
ARCOS Authenticator mobile app.
Click Validate Phone button.

## [p564]

www.arconnet.com|Copyright © 2025 564
12.
13.
On successful validation of the phone, the validate Code filed that was earlier in encrypted format will
be displayed now.
Enter the Validation code displayed on the Mobile app in the Validation code filed on the Server
Manager.

## [p565]

www.arconnet.com|Copyright © 2025 565
14.
15.
1.
2.
Click Validate Code button. A window pops up.
Click OK button. The mobile OTP is successfully configured.
Post Mobile OTP Configuration
Enter the credentials in ARCON PAM Login screen and click on Login button, the Mobile OTP
Validator pop up is displayed with PIN/Challenge.
User needs to enter the OTP. The OTP is generated in ARCOS OTP App.

## [p566]

www.arconnet.com|Copyright © 2025 566
3.
4.
The Pin/Challenge displayed in Mobile OTP Validator screen is entered in the Enter Challenge textfield
in the ARCOS OTP App.
Click Generate OTP button to generate the OTP and enter the OTP in Mobile OTP Validator screen.

## [p567]

www.arconnet.com|Copyright © 2025 567
5.
6.
1.
Click on the Validate OTP button.
The user is allowed to successfully login to the application.
Configure Email Address
This section explains the steps to configure email address for the User. It helps the User to receive alert mails
for the activities performed in ARCON PAM. For example, alert mails for Workflow Approval, Scheduled
Reports, Scheduled Password Envelope, Service Access Request, Service Password Request, or Ticket Request.
How to Configure Email Address?
To configure your Email Address use the following path:
Manage → Users and Services → Manage Users
Right-click on the user name from the User Display Name grid list. The Edit User Settings option is
displayed.
User needs to enter the OTP within 60 seconds for the given challenge or else the Pin/
Challenge will change.

## [p568]

www.arconnet.com|Copyright © 2025 568
2. Click the Edit User Settings option. The User Settings window is displayed.

## [p569]

www.arconnet.com|Copyright © 2025 569
3.
1.
In the Security Setting tab, enter the email address of the user in the Email ID text field and click
Confirm Changes to configure the email address for the User.
Configure Email OTP
What is Email OTP based Dual Factor-Authentication?
Dual-factor authentication makes the environment safer and more reliable. It helps to handle passwords
securely so authentication will only be available to authenticated people. Dual factor authentication means that
during login the user has to provide two secure information such as the user password and the one-time
password you receive in the Email. Email OTP is one of the methods, wherein ARCON PAM users receive OTP
on registered email addresses.
How to Configure Email OTP?
To configure Email OTP, follow the below steps:
Right-click on the user. A multiple-options list is popped up.
For Domain User, if email address is configured for the user on the domain server, then click more
options menu (Three Dots) to fetch the emailaddress from the domain user.

## [p570]

www.arconnet.com|Copyright © 2025 570
2. Click on the Edit User Settings option. The User Settings screen is displayed.

## [p571]

www.arconnet.com|Copyright © 2025 571
3.
4.
5.
Select the Dual Authorization Factor Type as Email OTP from the drop-down list and then click on
the Enable Dual Factor Type checkbox.
Enter your email address in the Email ID text field and click the Confirm Status link. A window pops up
with the following message will be displayed:
Click the Yes button, to confirm the changes. The following message will be displayed on the screen.
Post Email OTP Configuration
Users will be locked out if wrong password is entered after the defined attempts.

## [p572]

www.arconnet.com|Copyright © 2025 572
1.
2.
1.
Enter the credentials in the ARCON PAM Login screen and click Login, the SMS and Email OTP
Validator pop-up is displayed.
Enter the OTP received via Email and click Validate OTP, to validate and log into the ARCON PAM
application.
Configure Biometric Device
What is Biometric Device Configuration?
Biometric Device Configuration is a dual-factor authentication supported by ARCON PAM. It is performed by
using the biometric data (fingerprint) of the user. ARCON PAM acts as a strategic entry and identity
management system for managing several system-based users. It supports leading biometric devices such as
3M Cogent, Morpho, and Precision.
How to Configure Biometric Device?
To configure the biometric device, you need to follow the below steps:
You need to install the driver of BIO Metrics in your local computer.
Resend OTP: Click on Resend OTP, if OTP is not received via Email for a long duration.
If the value in Biometric – Finger Print – Minimum Match Score (Percentage) is set between 0 to 100
in Settings, then the score of the fingerprint should be matched to the configured value while logging
into the application.

## [p573]

www.arconnet.com|Copyright © 2025 573
2.
3.
4.
5.
Install in local computer and then connect the device with local computer.
You need to check whether the device manager is installed in Computer Management.
Check if the green light is displayed in the device.
Now configure the Biometric device on Server Manager for the individual user.

## [p574]

www.arconnet.com|Copyright © 2025 574
6. Right-click on the selected user. A multiple options list is popped up.

## [p575]

www.arconnet.com|Copyright © 2025 575
7.
8.
9.
Click on the Edit User Settings option. The User Settings screen is displayed.
Select the Dual  Authorization Factor Type as Biometric – Finger Print and then select the Enable Dual
Factor Type checkbox.
Click Confirm Status link. A window pops up.

## [p576]

www.arconnet.com|Copyright © 2025 576
10.
11.
Click Yes button. Another window pops up.
Click OK button to enable the settings of dual-factor biometric fingerprint in ARCON PAM while logging
into the application.

## [p577]

www.arconnet.com|Copyright © 2025 577
12.
13.
Select the finger position to be traced from Finger Position dropdown list and click Scan Finger
Print button. A Biometric – Finger Print Scanner a window pops up.
Place the finger on the Biometric device and click Start Scan button, to scan the fingerprint. The
fingerprint is traced on the Biometric – Finger Print Scanner screen.

## [p578]

www.arconnet.com|Copyright © 2025 578
14.
15.
1.
2.
Click OK button. The fingerprint is displayed in the Scanner.
Click Confirm Changes button to save or enable the configuration.
Post-Biometric Device Configuration
Enter the credentials in ARCON PAM Login screen and click Login, the Biometric Finger Print Validator
pop up is displayed.
Within a few seconds, the ARCON PAM Biometric Finger Print Authenticator pop up is displayed.
Test Finger Print the button is used to test the score of the fingerprint and if the score does not match
with the configured value then an error message is displayed Finger Print Does Not Match. Try Again.

## [p579]

www.arconnet.com|Copyright © 2025 579
3.
4.
Place the finger on the Biometric device. The fingerprint is traced on the Biometric – Finger Print screen
as shown below.
The fingerprint is authenticated and User will be able to successfully login into ARCON PAM application.

## [p580]

www.arconnet.com|Copyright © 2025 580
5. If the traced fingerprint does not match, then you will view the following error message displayed in the
below screen.
1.
2.
3.
Configure Biometric - Finger Print - Mode - Centralized Valid For (Minutes) in Settings, to
configure time in minutes for the validity of Finger Print.
If the value is Zero every time the user will have to identify through the biometric fingerprint.
If the value is 1 or above (minutes), it will bypass the biometric fingerprint for the defined time
period after the first login.
1.
2.
The following Settings can be configured to customize the requirements.
Biometric - Finger Print - Minimum Match Score (Percentage)  - This configuration will allow
setting, the percentage of minimum match score of Finger Print in Biometric Authentication.
The minimum value is 0% and the maximum value is 100%
Biometric - Finger Print - Mode - This configuration sets the mode of Finger Print in Biometric
Authentication.
a. Desktop: In this mode, every ARCON PAM User should have an individual bio-metric device
configured to their respective workstation, hence first the user login to the ARCON PAM portal
with their respective credentials and then the biometric authentication is prompted.

## [p581]

www.arconnet.com|Copyright © 2025 581
1.
Morpho Biometric Device Installation
The steps for Morpho Biometric Device Installation are as follows:
Double click on the Morpho.exe.
3.
b. Centralized: In this mode, the biometric device should be configured on a centralized location
and every User will be authenticated with the centralized bio-metric device first and then are
allowed to login into ARCON PAM Portal.
Biometric - Finger Print - Mode - Centralized Valid For (Minutes) - This configuration sets the
time in minutes for the validity of Finger Print in Centralized Mode for Biometric
Authentication. The minimum value is 1 minute and the maximum value is 480 minutes.
4. Biometric Devices - This configuration enables to set the type of biometric device that will be
used. The value 1 is for Morpho, 2 for Precision, 3 for 3Mcognet/Gemalto, 4 for eikon Touch. 5
for Globalspace
5. Biometric Finger Print Authenticator Link On ACMO Login Page - Is Enabled  -This
configuration enables/disables Biometric Finger Print Authenticator Link on CM Login Page.
Value '1' enables this link and '0' value disables it.

## [p582]

www.arconnet.com|Copyright © 2025 582
2.
3.
Click Next. Browse and select the required folder or location for installation.
Click Next. The installer is ready to install the program on your com

## [p583]

www.arconnet.com|Copyright © 2025 583
4. Click Install to start the installation.

## [p584]

www.arconnet.com|Copyright © 2025 584
5. The driver is being installed.

## [p585]

www.arconnet.com|Copyright © 2025 585
6.
7.
Click Finish, once the driver has been successfully installed, you need to check whether the driver is
installed in the device manager.
Check if a green light is displayed in the device. Now configure the Biometric device on Server Manager
for individual user.

## [p586]

www.arconnet.com|Copyright © 2025 586
Configure Hardware Token
What is Hardware Token Authentication?
A Hardware token is a security token which may be a physical device that an authorized User of computer
services is given, to ease authentication. It may be a small hardware device that the owner carries to authorize
access to a network service. In ARCON PAM, RADIUS servers are used for authentication of a RSA portal.
RADIUS is a protocol similar to LDAP, DCPIP, and RDP protocol. Similarly, RADIUS is a kind of protocol that
helps to communicate with another server.
How to Configure Hardware Token via RADIUS Server?
To configure values for Hardware Token RADIUS Server, use the following path:
Tools → Advanced Configuration → Hardware Token – Radius Server
The Hardware Token – RADIUS Servers contains the following fields:
Field Name Description
Create (radio button) Configure new radius server details.
Modify (radio button) Modify or update the radius server details.
Server Priority Select the server priority.
Radius Server Enter the IP address of the RADIUS Server.
Shared Key Enter the shared key of the RADIUS Server.
•
•
The Administrator having Hardware Token – RADIUS Server privileges in Server’s Privileges,
will only be able to enable or configure values for Hardware Token.
You need to configure values for Hardware Token RADIUS Server and Dual Factor IP
Range, before enabling Hardware Tokens which work on RADIUS protocol as a second factor of
authentication.
The server priority  can be configured up to three
servers, if those many servers are available in the
environment as part of HA (High Availability).

## [p587]

www.arconnet.com|Copyright © 2025 587
•
•
Field Name Description
Server Port (UDP) Enter the port (UDP) number of the RADIUS Server.
Domain Select the domain name of the RADIUS Server.
Radius User Authentication (checkbox) If enabled will check whether the user is in ActiveDirectory of
the RADIUS Server.
Radius 2FA Enables Dual Factor Authentication. ARCON PAM supports two
types of tokens, which are as follows:
Hardware Token: A random token is generated when you
press the key in the Hardware Device, which is entered in
2FA prompt while logging into ARCON PAM. The token
entered is authenticated with the RADIUS Server. Once
authenticated, the User will be able to login into the
application.
Software Token: A RADIUS Windows application
available with the User on his/her local machine contains
a random token, which is entered in 2FA prompt while
logging into ARCON PAM. The token entered is
authenticated with the RADIUS Server. Once
authenticated, the User will be able to login into the
application.
Domain with User  Select Domain with User checkbox, if multiple domains are
configured on RADIUS Server. The User has to specify Domain
Name with User Name while 2FA authentication.
Is Active To enable the configuration in ARCON PAM.
Select or Enter the details and click on Create button to configure the RADIUS Server.
Dual Factor IP Range Configuration:
Dual Factor IP Range helps you to define the range of IP Addresses to be configured for the ‘Dual Factor type’.
Once configured, ARCON PAM will prompt for the second-factor authentication to the End User only if the
user is from the configured IP range.
If Radius User Authentication is enabled, by
default  Radius 2FA will be enabled due to which while
logging into the application, the user will be
authenticated twice once for ADauthentication and
then through Dual FactorAuthentication.
The Administrator having Default Configuration and Dual Factor IP Range privileges in ARCON PAM
Server’s Privileges, will only be able to configure values for Dual Factor IP Range.

## [p588]

www.arconnet.com|Copyright © 2025 588
1.
2.
3.
Select the Enable (Dual factor will be applicable only for mentioned IP addresses) checkbox.
A window pops up with the following message:
Confirm Changes?
Click Yes. The fields are enabled to configure dual factor IP range.
The Dual Factor IP Range screen contains the following fields:
Field Name Description
Create (radio button) Create (radio button)
Modify (radio button) To modify or update an existing dual factor IP range.
Description Enter description for the dual factor IP range.
To modify details of dual factor IP range, select the
required dual factor IP range from the grid on the left
pane. The details are displayed on the right side. Modify
the required details and click Modify button, to update
the IP address of the machines.

## [p589]

www.arconnet.com|Copyright © 2025 589
1.
Field Name Description
From IP Enter IP address to set the start range for dual factor.
To IP Enter IP address to set the end range for dual factor.
Type Select the type of dual factor authentication.
Is Active Click to enable the configuration in ARCON PAM.
Delete Click Delete, to delete the configured dual factor IP Range.
4. Select/ Enter the details and click on the Create button to define a dual factor IP range.
Enable Hardware Token Configuration:
To enable the configuration for Hardware Token use the following path:
Manage → Users and Services → Manage Users → Right click on the User → Edit User Settings option.
Select the Dual  Authorization Factor Type as Hardware Token and then select the Enable Dual Factor
Type checkbox.
To delete a dual factor IP range, select the required
dual factor IP range from the grid on the left pane. The
details are displayed on the right side. View the details
and click Delete button, to delete the details.
•
•
The user is authenticated on login screen of ARCON PAM Client Manager, once the dual factor
IP range is configured.
Once both the values for Hardware Token RADIUS Server and Dual Factor IP Range are
configured, you need to enable the configuration for Hardware Token in User Settings screen.

## [p590]

www.arconnet.com|Copyright © 2025 590
2.
3.
4.
1.
2.
Click Confirm Status link. A window pops up.
Click Yes button. Another window pops up.
Click OK button. The Dual Factor Hardware Token is enabled for the selected User.
Post Hardware Token Configuration
Enter the credentials in ARCON PAM Login screen and click Login, the Hardware Token - Validator pop
up is displayed.
Enter OTP received via Email and click Validate, to validate and login into ARCON PAM application.
Configure Voice Biometric
What is Voice Biometric Authentication?

## [p591]

www.arconnet.com|Copyright © 2025 591
1.
2.
•
•
Voice Biometric Authentication is a type of dual-factor authentication that uses Web Service to authenticate
users before logging into Client Manager. The predefined web service authentication is configured, which will
authenticate the user through his voice and decide whether to allow the user to log in or not.
How to Configure Voice Biometric Authentication?
To Navigate use the following path:
Settings → Group → 2FA → Voice Bio Metric Configuration
Select Voice Bio Metric Configuration
To Enable select the checkbox. The fields are enabled to configure voice biometric authentication.
The Voice Biometric Authentication screen displays the following fields:
Field Name Description
Authentication URL It is in the predefined .xml format.
Success Flag Configure success flag. The valid values are:
True
False
•
•
The Administrator having Default Configuration and Voice Biometric
Authentication privileges in Server’s Privileges will only be able to configure values for Voice
Bio Metric Configuration.
You need to configure values for Voice Biometric Authentication and Dual Factor IP
Range, before enabling Vioce Biomatric Authentication as a second factor of authentication.

## [p592]

www.arconnet.com|Copyright © 2025 592
•
•
3.
4.
1.
Field Name Description
Error Flag Configure error flag. The valid values are:
True
False
Authorization Username Authorized user name used to access the specified URL.
Authorization Password Password used to access the specified URL.
Request Time(In Min) Select the session timeout in minutes.
Few fields are customizable according to requirement. The ARCON PAM User Tag, ARCON PAM User
Mobile No. Tag and ARCON PAM Message Tag can be configured with user details, user mobile number
and message to be sent.
Select/Enter the details and click Confirm Changes to configure the details.
Dual Factor IP Range Configuration:
Dual Factor IP Range helps you to define the range of IP Address to be configured for the ‘Dual Factor type’.
Once configured, ARCON PAM will prompt for the second factor authentication to the End User only if the
User is from the configured IP range.
The Administrator having Default Configuration and Dual Factor IP Range privileges in ARCON PAM Server’s
Privileges, will only be able to configure values for Dual Factor IP Range.
How to Configure Dual Factor IP Range?
To Navigate use the following path:
Settings → Group → 2FA → Dual Factor IP Range
To Enable select (Dual factor will be applicable only for mentioned IP addresses) checkbox.

## [p593]

www.arconnet.com|Copyright © 2025 593
2.
3.
4.
5.
Select the Enable (Dual factor will be applicable only for mentioned IP addresses) checkbox. A window
pops up with the following message: Confirm Changes?
Click Yes. The fields are enabled to configure the IP range.
Click on the Add button  to add a New Dual Factor.
The Dual Factor IP Range screen contains the following fields:
Field Name Description
Description Enter the description for the dual-factor IP range.
From IP Enter IP address to set the start range fordual-factor.
To IP Enter IP address to set the end range for dual-factor.
Type Select the type of authentication.
Is Active Click to enable the configuration.
For Editing  the details of the existing Dual Factor IP Range. Click on the existing Dual Factor IP
Range and select the Edit button at the top and make the required changes. Also, you can right-click on
the domain and select Edit.
The user is authenticated on login screen of Client Manager, once the dual factor IP range is
configured.

## [p594]

www.arconnet.com|Copyright © 2025 594
6.
7.
1.
For Deleting  the existing Dual Factor IP Range. Click on the existing Dual Factor IP Range and select
the Delete button at the top and make the required changes. Also, you can right-click on the domain and
select Delete.
The Export  button  will export all the Dual Factor IP Range details in the form .xlsx format. The
Copy button  will copy all the details of the table.
Configure SMS OTP
What is SMS OTP Dual-Factor Authentication?
Dual-factor authentication makes the environment safer and more reliable. It helps to handle passwords
securely so authentication will only be available to authenticated people. Dual factor authentication means that
during login the user has to provide two secure information such as his password and one time password he
receives in SMS on his mobile phone. SMS OTP is one of the methods, wherein ARCON PAM users receive OTP
on registered mobile numbers.
How to Configure SMS OTP?
To Navigate use the following path:
To configure SMS OTP, follow the below steps:
Right-click on the user. A multiple-options list is popped up.

## [p595]

www.arconnet.com|Copyright © 2025 595
2.
3.
Click on the Edit User Settings option. The User Settings screen is displayed.
Select the Dual Authorization Factor Type as SMS OTP from the dropdown list and then click on
the Enable Dual Factor Type checkbox.

## [p596]

www.arconnet.com|Copyright © 2025 596
4.
5.
Click Confirm Status link then enter the 10 digit mobile number in Mobile No text field and
click Confirm Changes button. A window pops up with the following message:
Do You Want To Change Dual Factor – SMS OTP Setting For Selected User?
Click Yes button, to confirm the changes.
Post SMS OTP Configuration
Users will be locked out if wrong password is entered after the defined attempts. Settings for SMS and
Email OTP logout attempt has been added to set a minimum and maximum value to consider for user
lockout.

## [p597]

www.arconnet.com|Copyright © 2025 597
1.
2.
1.
2.
3.
4.
Enter the credentials in ARCON PAM Login screen and click Login, the SMS and Email OTP
Validator pop up is displayed.
Enter OTP received via SMS and click Validate OTP, to validate and login into ARCON PAM application.
Passwordless Authentication
What is Passwordless Authentication?
A drive towards complete automation is envisaged. With the evolving technology, the organization's security
should be stronger than ever before and at the same time ensure higher security standards. A new
authentication has been introduced which frees the User from remembering passwords while logging into their
systems.
ARCON PAM features a Passwordless authentication strategy where the Users can seamlessly log on to the
application by just using MFA of their choice. The login details of the user are validated against the domain.
Successful Validation lands the user on the Dual factor Authentication page if the admin has set one, else lands
the user directly to the target page.
To achieve passwordless authentication, it is recommended to enable Multifactor Authentication for the user
as an additional security step.
We have the following Multifactor solutions integrated with the ARCON PAM Solution:
Leading Biometric  devices such as 3M Cogent(Gemalto), Morpho, Precision, eikonTouch, and
Globalspace.
Standard Protocols based Authentication e.g. LDAP, RADIUS, OAUTH2.
Email and SMS-based OTP.
TOTP-based authenticators like Symantec VIP Access, Google Authenticator, and Microsoft
Authenticator.
Resend OTp: Click Resend OTP, if OTP is not received via SMS for a long duration

## [p598]

www.arconnet.com|Copyright © 2025 598
5.
6.
1.
2.
ARCON | PAM has its own built Mobile OTP App called ARCON AUTHENTICATOR.
The solution integrates with Facial recognition  solutions, as well as, has an in-built ARCON facial
recognition module.
ARCON | PAM also gives the flexibility to a user to select the dual-factor he wants to when logging into the
ARCON | PAM solution.
How to Configure?
Go to the path: Local Drive:\ARCON
Solutions\ARCOSClientManagerOnline\PAMNextGen\DomainAuth folder.
It should contain urls.ini, and inside that it should contain the below entry:
~/frmConnection.aspx
To support other Multi-Factor Authentications, refer to Configurations under Security Settings.

## [p599]

www.arconnet.com|Copyright © 2025 599
3.
4.
Right-click on the DomainAuth folder > Properties > Security Tab > Add a User > "IIS_IUSRS" with full
rights (read, write, execute).
Open IIS and look for "Authentication" under the PAM-hosted website.

## [p600]

www.arconnet.com|Copyright © 2025 600
5.
a.
b.
6.
7.
8.
Go to Sites > ARCOSClientManagerOnline > DomainAuth > Double Click > Authentication
Anonymous Logon - Set it as Disabled
Windows Authentication - Set it as Enabled
Restart IIS service.
In applicationHost.config file; under the "Authentication" section group , set <section
name="anonymousAuthentication" overrideModeDefault="Allow"/>
In web.config file, put the following code :-

## [p601]

www.arconnet.com|Copyright © 2025 601
1.
2.
<location path="ARCOSWebAPI"> // Location of the folder where the webdt file is
located.
<system.webServer>
<security>
<authentication>
<anonymousAuthentication enabled="true" />
</authentication>
</security>
</system.webServer>
</location>
Internet Options Configuration (Server)
Go to Internet Options > Security > Custom Level button.
Under User Authentication > Logon > select radio button "Automatically logon with current username
and password".

## [p602]

www.arconnet.com|Copyright © 2025 602
1.
Internet Options Configuration (End-user machine)
Go to Internet Options > Security.

## [p603]

www.arconnet.com|Copyright © 2025 603
2. Select Local Intranet > Sites

## [p604]

www.arconnet.com|Copyright © 2025 604
3.
4.
5.
6.
7.
1.
Add ARCON PAM URL to Add this website to the Zone option and click Add.
Click Close
Now go to Custom level > User Authentication >  Logon > Automatic logon with username and
password.
Click Ok and then Click Apply
Restart the machine.
How to Access PAM?
Once all the configuration for Passwordless Authentication is achieved, the end-user can log in to a Windows
Domain Authenticated machine and open the PAM web application in the browser. When the URL is accessed,
the Passwordless Authentication feature would automatically pick up the Authentication for the logged-in
Domain User and provide only with the Multifactor Authentication. For example, if Mobile OTP(ARCON
Authenticator), the below would be the process.
Follow the below steps:
Enter the URL with the DOMAINAUTH extension.

## [p605]

www.arconnet.com|Copyright © 2025 605
2.
3.
If Multifactor Authentication is enabled, the user will be asked for input to validate.
After successful Multifactor Authentication validation, the user will be successfully logged into ARCON
PAM Client Manager Online.

## [p606]

www.arconnet.com|Copyright © 2025 606
Domain Validation
Along with a seamless Passwordless authentication, ARCON PAM also provides additional security to control
access for allowed domains in an organization.
This can be achieved by enabling the following 3 configurations, using centralized PAM Settings. To navigate,
use the following path:
Settings → Group → ACMO
Field Name Description
Domain
Validation for
ACMO
( WindowsOS
only)
This configuration sets restrictions for accessing PAM ACMO based on their domain and
workgroup.
Valid Values Allow both Domain and Workgroup machines, Allow only Domain machines, Allow only
domain which have been listed.
Domain
validation failed
message for
ACMO
(WindowsOS
only)
Set a customized message for domain validation.
For example- If my Domain validation for ACMO (WindowsOS only) is - Allow only
Domain Machines, and a workgroup user tries to access it then the login is failed, and the
message set on Domain validation failed message for ACMO (WindowsOS only) appears
on the ACMO user screen.
Valid Values Enter the text message to be displayed on ACMO when the validation fails.

## [p607]

www.arconnet.com|Copyright © 2025 607
1.
2.
Field Name Description
Custom Domain
Validation
names (Windows
OS only)
We write the Comma-separated domain names, which verify the user's presence against
that domain.
Valid Values Enter the Domain names
Note: - To enable Custom Domain Validationnames (WindowsOS only), the Domain
validation for ACMO (WindowsOS only) value needs to set to Allow only domain which
have been listed.
Follow the below steps:
Domain Validation for ACMO (Windows OS only)
Domain validation failed message for ACMO (Windows OS only)

## [p608]

www.arconnet.com|Copyright © 2025 608
3.
4.
Custom Domain Validation names (WindowsOS only)
If an unauthorized domain login happens, the custom defined message would be displayed.

## [p609]

www.arconnet.com|Copyright © 2025 609
1.
Configure Face Recognition
Face Recognition Configuration is a dual-factor authentication supported by ARCON PAM. It is performed by
using the facial information captured from the webcam of the user's machine.
How to Configure Facial Information?
To configure face recognition, you need to follow the below steps:
To Navigate, follow the below path:
Server Manager > Manage Users
You need to configure the facial information on the Server Manager for the individual users.

## [p610]

www.arconnet.com|Copyright © 2025 610
2.
3.
4.
5.
Right-click on the selected user. A multiple-options list is popped up.
Click on the Edit User Settings option. The User Settings screen is displayed.
Select the Dual  Authorization Factor Type as Face Recognition and then select the Enable Dual Factor
Type checkbox.
Click the OK button to enable the settings of dual-factor facial recognition in ARCON PAM while logging
into the application.

## [p611]

www.arconnet.com|Copyright © 2025 611
1.
Post-Face Registration Configuration
Enter the credentials in the ARCON PAM Login screen and click Login, the Facial Recognition Validator
pop-up is displayed.

## [p612]

www.arconnet.com|Copyright © 2025 612
2.
3.
4.
5.
Within a few seconds, the ARCON PAM Facial Recognition Registration pop-up is displayed.
Place your face in front of the camera so that we can start scanning.
The facial data is authenticated from the database and Users will be able to successfully login into the
ARCON PAM application.
If the facial data does not match, then you will not be able to log into the ARCON PAM application.

## [p613]

www.arconnet.com|Copyright © 2025 613
1.
2.
3.
4.
Configure FIDO2 Authentication
What is FIDO2 Authenticator?
FIDO2 Authenticator is a modern, hardware-based authentication method that supports dual-factor
authentication without the need for traditional passwords. It allows users to securely access systems and
services using a physical security key, such as a USB or biometric device, instead of remembering or entering
credentials.
How to Configure FIDO2 Authenticator?
To navigate, use the following path:
To configure the FIDO2 authenticator, follow the steps below:
You need to configure the FIDO2 authenticator on the Server Manager for the individual users.
Right-click on the selected user. A multiple-option list pops up.
Click on the Edit User Settings option. The User Settings screen is displayed.
Select the Dual  Authorization Factor Type as FIDO Authentication.

## [p614]

www.arconnet.com|Copyright © 2025 614
5.  Select the Enable Dual Factor Type checkbox.

## [p615]

www.arconnet.com|Copyright © 2025 615
6. Click Confirm Status to enable the settings of FIDO Authentication in ARCON PAM while logging into
the application.

## [p616]

www.arconnet.com|Copyright © 2025 616
1.
Post-FIDO Authentication Configuration
Enter your credentials on the ARCON PAM login screen and click Login. The FIDO Authenticator pop-
up will then appear. Click FIDO Authentication.

## [p617]

www.arconnet.com|Copyright © 2025 617
2.
3.
Click Register.
Click Ok to set up the security key.

## [p618]

www.arconnet.com|Copyright © 2025 618
4.
5.
Place your finger on the FIDO device to complete authentication.
You need to create a PIN for the security key. Enter the new security key pin and confirm the security
key pin. Click Ok.

## [p619]

www.arconnet.com|Copyright © 2025 619
1.
2.
Log in to PAM With FIDO Authenticator
When a user logs into PAM, the Dual Factor Authentication pop-up is displayed, and click FIDO
Authentication.
The below Login screen is displayed, and click Login.

## [p620]

www.arconnet.com|Copyright © 2025 620
3.
2.
The screen below is displayed, and select Windows Hello or external security key as illustrated below.
Enter the security and click OK.

## [p621]

www.arconnet.com|Copyright © 2025 621
3.
1.
Touch the FIDO device with your finger to complete authentication, after which the user will be
successfully logged into PAM.
4.3.9.4.6 Modify details of User
This section helps you to modify the details of a particular user. You can modify the details of a particular user
using the Create/ Modify User screen.
4.3.9.4.6.1 How to Modify the details of a User?
To modify the details of a User use the following path:
Manage → Users and Services → Manage Users
Click the Manage Users sub-menu. The Create/Modify User screen is displayed.
The Administrator having Modify User privilege shall only be able to modify User details.

## [p622]

www.arconnet.com|Copyright © 2025 622
2.
3.
4.
5.
Select the LOB and type of User from the Select LOB/Profile and User Type dropdown list respectively.
A list of active Users are displayed in the grid.
Select the User from the grid. The details are populated in the Create/Modify User fields.
Modify the required changes in the existing fields and click Modify. A window pops up with the following
message:
Selected User Updated.
Click OK. The details of the User are modified.
You can modify details of Active Users, Disabled Users, Lockout Users, and Dormant Users of a
particular LOB by selecting the icons besides the User Type dropdown.

## [p623]

www.arconnet.com|Copyright © 2025 623
•
•
•
•
•
•
•
•
•
•
•
•
4.3.9.5 Service
4.3.9.5.1 What are Services?
A service is an instance of a server. In ARCON PAM, the routers, firewalls, switches, and databases are some of
the services created to connect to the target server. These services need to be mapped to users. The users
mapped to the services will have the privilege to connect to the target server using these services.
For example, Suppose there are four users Admin, Client, TEST, and UAT on a Windows server. Each user may
have a unique requirement for service to be performed on the server. Hence, the Administrator will create
services for each of the users. These services are then grouped and mapped to each of the users which helps the
Administrator to manage the services which are mapped to the user. Thereby, also helping the Administrator in
user wise audit trail performed in ARCON PAM.
4.3.9.5.2 Why are Services Important?
They define and control user access to specific components of the infrastructure, supporting the
principle of least privilege.
They allow precise role-based access management, where each user only interacts with the services
they are authorized for.
They enable better auditing and traceability, as actions can be logged and reviewed on a per-user, per-
service basis.
They simplify service administration, making it easier for administrators to manage user access across
multiple systems.
4.3.9.5.2.1 This Section includes the following Topics:
Service Classification
Create a Service
Define a Critical Command for a Service
Add Services in DMZ Supporting Server
Bulk Update
Service Quick Search
Copy Service Details
Modify Service Parameters
4.3.9.5.3 Service Classification
Service Classification defines the classification for a service such as critical, data, or antivirus server. In
addition, you can modify the existing defined classification. Once the classification is defined, you can apply the
classification while modifying the parameters of a service.
The Administrators having Read Only Access privilege (under Manage Services) can view details
displayed under Manage Services and Map Groups/Services tab.
The Administrator having Service Classification privilege in Server’s Privileges will only be able to
configure under Service Classification.

## [p624]

www.arconnet.com|Copyright © 2025 624
1.
2.
3.
a.
i.
4.3.9.5.3.1 How to define service classification?
To define service classification, follow the below path:
Tools → Advanced Configuration → Service Classification
The Service Classification screen contains the following fields:
Field
Name Description
Create Select to create a service classification.
Modify Select to modify details of service classification.
Service
Classifica
tion
Specify the name for a service classification.
Descripti
on
Specify the description for a service classification.
Follow the below steps:
Enter the details and click Create button. A window pops up with the following message:
New Service Classification Created.
Click OK. The new service classification is created.
You can apply this service classification to service (s).
Apply to a single Service:
To apply Service Classification to single service, use the following path:
Server Manager → Manage → Users and Services → Manage Services
Select a service.
To modify details of service classification, select the required service classification from
the grid on the left pane. The details are displayed on the right side. Modify the required
details and click Modify button, to update the service classification details

## [p625]

www.arconnet.com|Copyright © 2025 625
ii.
iii.
iv.
b.
i.
ii.
iii.
iv.
v.
vi.
Right click and select Modify Service Parameters.
Select Service Classification from drop down.
Click Modify. The selected Service Classification will be applied to Service.
Apply to a group of Services:
To apply Service Classification to services, use the following path:
Server Manager → Tools → Advanced Configuration → LOB / Profile Default Configuration →
LOB / Profile - Password Policy
Select the LOB or profile from the LOB/ Profile dropdown list. A list of service groups are
displayed in the grid.
Select the checkbox from the Service Group Name list. It displays the count of services for
that particular group under Service Type grid.
Select a type of service from the Service Type list. This will enable you to set automated
change passwords for that particular service type.
To apply service classification, select Allow checkbox against Service Classification drop
down. The drop down will be enabled.
Select the required service classification.
Click Confirm Changes  button. Service Classification will be applied to services under
selected Service Group and Service Type.
4.3.9.5.4 Create a Service
This section explains the steps to create services. The Administrators are responsible for managing services. In
addition, the details of the services created shall also be modified or deleted.
4.3.9.5.4.1 How to Create a Service?
To create a service use the following path:
Manage → Users and Services → Manage Services
The Administrator having Add Service privilege will only be able to create services.

## [p626]

www.arconnet.com|Copyright © 2025 626
1. Click the Manage Services sub-menu. The Create/Modify Services screen is displayed.
To search a specific set of rows, enter keywords (space separated) on the column's header, and the
relevant rows are pulled out.

## [p627]

www.arconnet.com|Copyright © 2025 627

## [p628]

www.arconnet.com|Copyright © 2025 628
•
•
The Create/ Modify Services screen contains the following fields:
Field Name Description
Create (radio button) Select to create a service.
Modify (radio button) Select to modify details of an existing service.
Service Type Select the type of service from the drop-down list.
Host Name Specify the hostname of the Server.
IP Address Specify the IP address of the Server.
Domain Name Specify the domain name of the Server.
Service Options Use Credentials: This field is enabled if you select the Service Type as MS SQL EM
– RDP, to login to the server using the RDP credentials.
Dynamic Port: Dynamic port can be enabled while connecting to MS SQL QA
Service.
While creating a service, if Administrator selects the Dymanic Port option, it is
mandatory to pass the instance name of the server and user lock to console
(supporting service) to connect to server. Therefore, the Administrator should
enter the details in Instance field  and select the User Lock To Console or
Supporting Service from the dropdown.
Instance: Enter the Instance name of the server to be connected.
User Lock To Console or Supporting Service: Select the required
supporting service having SQL Administrator rights.
This editor does not support displaying this content: panel
Server Type Select the type of Server.
User Display Name Specify the User Display Name.
User Description Specify the User Description.
•
•
The Administrator having Modify Service privilege will only be
able to modify services.
To modify details of Service, select the required Service from the
grid on the left pane. The Service details are displayed under
Create/Modify Services pane on the right side. Modify the
required details and click Modify, to update the Service details.

## [p629]

www.arconnet.com|Copyright © 2025 629
•
•
•
•
Field Name Description
Instance Specify the instance name of the Server (if applicable).
Port Displays the port number.
User Name Specify the username.
IAM ARN Each and every AWS Service can be uniquely identified with IAM ARN Text
specified here.
AWS Credentials   Upload the CSV file that contains the Access Key and the Secret Key.
Password Options Single Custody- In this option, the Admin(Owner1 himself) assigns the
password for the service and the service is created.
Split Custody- In this option there are two owners of the
password. Owner1 is the Admin himself who wants to create the service
with his (first/second half) of the password and fills in the name of the
second owner who will enter the other half of the password. The service
will be created only when both the owners enter their part of passwords.
This editor does not support displaying this content: panel
Password Part First half- Select the checkbox to enter the first part of the password in the
password field.
Second half- Select the checkbox to enter the second part of the password
in the password field.
This editor does not support displaying this content: panel
The data in this field is auto-populated based on the Service
Type selected.
This field will be visible for AWS Service Type.
•
•
Both the keys will be stored in the database.
This field will be visible for AWS Service Type

## [p630]

www.arconnet.com|Copyright © 2025 630
Field Name Description
Password Specify the password for the server.
Confirm Password Re-enter the password and confirm.
Other Owner Select the second owner's name who will enter the other half of the password and
create the service.
Valid Till Date Select the end date. This is the date from which the service will be inactive for the
user.
Use Customized
Connector
Used to select the customized connector.
User Lock To Console/
Supporting Service
Used for SSH Linux services to login to root and allow change of passwords.
Allow Password Change  To enable the password change process.
Allow Password Request If the checkbox is enabled, then Users can raise a password request for that
particular service.
Description 1 Specify the required description 1 (OS Version) for Service (if required).
Description 2 Specify the required description 2 (Server Description) for Service (if required).
Description 3 Specify the required description 3 (Location of Server) for Service (if required).
Parameter Specify the parameter of Service (if applicable).
This field is enabled, when you select the Enable checkbox.
By default the checkbox is Enabled.
•
•
Refer configurations tag documents/or click Config tags
Description for more details.
ARCON supports multi sessions for SSH services. Multisession is
configured in Server Manager→  Manage Service→  Select the
service→ Add <MUTISESSION>tag in the parameter field.

## [p631]

www.arconnet.com|Copyright © 2025 631
•
•
Field Name Description
Enable Application
Mapping
Select this checkbox to have multiple connector options when taking the
connection for the created service.
Active Applications It lists all the applications selected from the Application Name dropdown.
Application Name  Select the application names from the dropdown which should be available when
taking the connection for the created service.
Description 1 Specify the required description 1 (OS Version) for Service (if required).
Description 2 Specify the required description 2 (Server Description) for Service (if required).
Description 3 Specify the required description 3 (Location of Server) for Service (if required).
Parameter Specify the parameter of Service (if applicable).
Is Active It enables all the applications set under Enable Application Mapping.
Config Tags Description Click link to view configuration tags.
Drop button Used to disable or delete the service from ARCON PAM. Click Drop, A pop up is
displayed with two options:
Disable Service: Used to disable the service in ARCON PAM.
Permanently Delete Service: Used to permanently delete the service from
ARCON PAM.
Follow the below steps:
•
•
•
•
•
•
•
•
•
•
This can be enabled only for the following service types
App Xshell
App SecureCRT
App MobaXterm
App WinSCP
App FileZilla
App BMT
App BSCLOGCOL
App 3 HIT Tool
App Win fiol
Putty
The Administrator having Drop Service privilege will only be able to
disable or delete services.

## [p632]

www.arconnet.com|Copyright © 2025 632
1.
2.
Click Create. A window pops up with the following message:
New Server Instance Created
Click OK. A new service is created for the user.
The new service created is displayed in Manage Services grid, once you have mapped it under a
particular LOB.
On the topmost corner of the Create / Modify Service Page, Click the down arrow key and the following options
will be displayed.
Options Description
Paste Service
Details
Directly paste the service details (the service details should already be copied to the
clipboard)
Resolve Hostname It will fetch for Hostname for a similar IP in the Database and automatically take up  the
hostname if there is an existing service in the same combination
Resolve IP Address It will fetch for IP Address for a similar Hostname in the Database and automatically take
up  the IP Address if there is an existing service in the same combination
On creating Linux services, a pop-up window is displayed to confirm whether the password has
to be vaulted.
Once a service is successfully created, you need to then map the service to a particular LOB. In
some cases, wherein an administrator having Settings privileges has configured the value for
the LOB Wise Service Management - Is Enabled option, where
LOB Wise Service Management - Is Enabled toggle value is set to Enabled, then it states
that when a service is created, it will directly map the service to the selected LOB
from Select LOB/Profile dropdown list, once it is created.
LOB Wise Service Management - Is Enabled toggle value is set to Disabled, then it
states that the service created needs to be mapped to a particular LOB in LOB/Profile
Master & Manager.
While creating service and manually changing password of any existing service, a prompt will be
displayed stating:
Do you want to Vault With New Password Immediately?
On User's confirmation, a new password will be generated by ARCON PAM. The new generated
password will be vaulted in ARCON PAM and updated on Target Device.
To enable Password Change through Gateway Server, enable Use Gateway Server
(ARCON PAM - Firewall) from Password Change Defaults (Default Configuration).

## [p633]

www.arconnet.com|Copyright © 2025 633
1.
2.
3.
4.
•
•
•
•
Options Description
Resolve Hostname
to DB
It will fetch for Hostname for a similar IP in the Database and automatically take up  the
hostname if there is an existing service in the same combination
4.3.9.5.4.2 App X-RDP
X-RDP service users can remotely connect to Windows Desktop and access files, applications, and other
network resources. If an X-RDP service type is assigned to the user(s), when the user(s) select the LOB and X-
RDP Service type all the services will be listed.
Follow the below steps:
To start RDP on the second screen, configure   ARCOSAppExeTerminal_Config.ini in the ACM folder:
ShowOnSecondaryMonitor should be set to 1, If the value is set to 0, it will open on the same screen.
App X-RDP can be launched either directly or via Remote Desktop Plus too. For launching it with RDP
Plus, tag <RDPPLUS> should be mentioned in field 4. otherwise it will launch directly.
The port must be changed to 3389 while configuring App X-RDP in Server Manager.
4.3.9.5.4.3 ARCON DBeaver QA Connector
What is DBeaver Integration?
ARCON has extended the database integration by integrating DBeaver DBMS (Community Edition) which is a
universal database management tool. With DBeaver you are able to create analytical reports based on records
from different data storages, export information in an appropriate format. For advanced database users
DBeaver suggests a powerful SQL-editor, plenty of administration features, abilities of data and schema
migration, monitoring database connection sessions, and a lot more. Out-of-the box DBeaver supports more
than 80 databases, but currently ARCON has tested the integration with MSSQL and Oracle.
This document will guide you through the steps involved in the deployment for the ARCON Privileged Access
Management (PAM) DBeaver QA Connector.  The following steps are to be followed for the successful
deployment of ARCON PAM Datawarehouse in your environment.
Pre-requisites
Before configuring the ARCON PAM DBeaver QA Connector, you should read the ARCON PAM connector
Pre-requisite document to ensure that your environments meets the minimum installation requirement for the
ARCON PAM product.
End-user machine should have access to below web components
ACMO (PAM Portal)
ARCON PAM API
PAM Version: U10
Java 8 (32/64 bit based on system) should be installed on the system to run DBeaver https://
www.java.com/en/download/manual.jsp
Configuration:
Oracle QA Service:  Create a Oracle QA service and Parameter 4 of service needs to be
<dbeaverqa><ORACLE>

## [p634]

www.arconnet.com|Copyright © 2025 634
•
•
•
•
•
•
•
•
1.
2.
3.
4.
5.
6.
•
•
•
•
•
MSSQL QA Service:  Create an MSSQL QA Service and Parameter 4 of service needs to be
<dbeaverqa><MSSQL>
Features:
The following are the features of the DBeaver QA Connector:
Single Sign On
Command Restrictions
Critical With Approval
Alerts for Critical Commands
Session Recording
Command logs
Video Logs
Session Monitoring
Behavior Analytics
Issues Resolved:
The Following issues are resolved with DBeaver QA Connector:
Multiple Instances.
Block popups for daily tips, Sample Database.
Block Driver Download and set driver paths.
Fixed command logging for multiple times execution of the same query.
API Slowness.
Restrict Dbeaver UI’s editing options
4.3.9.5.4.4 App Corona Workbench
Corona is a Banking Tool that smart streams solutions for effectively reconciling the following:
Nostro accounts
Securities messages (settlements, statements of holdings, statements of transactions, and corporate
actions)
Forex, money market, derivative, and commodity confirmations
Intra-day messages
Cards-based transaction messages
It also includes the calculation module Corona Quantum which allows you to calculate positions for
configurable periods by processing data from Corona Cards, Corona Cash, or external data sources. It also
enables you to generate all types of Intraday Liquidity Reports according to the regulatory requirements of the
Basel III agreement. Corona delivers complete transaction management and control and integrates a powerful
module for the detection of exceptions, enabling institutions to reduce operational risk and cost through
continual process improvement.
Pre-Requisites:

## [p635]

www.arconnet.com|Copyright © 2025 635
•
•
•
•
1.
2.
3.
4.
5.
a.
b.
c.
d.
Before configuring the ARCON PAM Corona Workbench Connector, you should read the ARCON PAM
connector Pre-requisite document to ensure that your environment meets the minimum installation
requirement for the ARCON PAM product.
The end-user machine should have access to the web component mentioned below
ACMO (PAM Portal)
PAM Version: U10
Exe Path: The end user should have the Corona application installed on the system (for eg. : C:\Program
Files (x86)\CoronaCS\7.8\ftms.exe)
Propertyfilepath: Folder hierarchy should be present at the end-user %APPDATA% \SmartStream
Technologies\Corona\7.8
Configuration:
Open Server Manager from ACMO.
 Navigate Manage → Users and Services → Manage Services.
In the Manage Service screen, you can create the service type as App Corona Workbench by entering
the Host Name, IP and Domain Name, and Port in the respective fields of the service.
Corona Database details need to be updated in the instance field of service
In the Parameter field,
Property File Path <DATA><CONFIGPATH>%APPDATA%\SmartStream
Technologies\Corona\7.8\Logon Profiles.ini</CONFIGPATH></DATA>
Check for deputyship use <deputyshipon>
Uncheck for deputyship use <deputyshipoff>
The default tile is "Logon to Corona 7.8" for Corona workbench. If the title is changed then
include the title in the following format <DATA><lwh>New title</lwh</DATA>.

## [p636]

www.arconnet.com|Copyright © 2025 636
6.
7.
•
•
•
The path of this application should be copied and entered under the local path in My Preferences in
ACMO.
Now, we can simply connect to the service from ACMO.
Features:
The following features of ARCON PAM are supported by the App Corona Workbench Connector.
Single Sign-On
Session Recording
SSM
4.3.9.5.5 Define a Critical Command for a Service
4.3.9.5.5.1 What are Critical Commands?
Critical Commands are commands that are defined as highly critical for use. These commands when executed
will have a crucial impact on the target server or the resources associated with it. When an attempt is made to
execute a critical command, it will prompt for confirmation for executing the command.
4.3.9.5.5.2 How to define Critical Commands?
This section helps you to define a critical command for a service. In addition, you can modify or delete an
existing defined critical command.
To define a critical command, use the following path:
Tools → Advanced Configuration → Service Critical Commands
The Administrator having Service Critical Commands privilege in Server’s Privileges will only be able
to define a critical command for a service.

## [p637]

www.arconnet.com|Copyright © 2025 637
1.
2.
The Service Critical Commands screen contains the following fields:
Field Name Description
Create Create a critical command for a service.
Modify Modify an existing critical command defined for a service.
Service Type Select the type of service.
Command Define a command.
Command
Description
Specify command description.
Remark Specify the remark.
Ask User
Confirmation
(Before
Execution)
Indicates that the user will be asked for confirmation before executing the command.
Is Active Enables the configuration.
Delete button Click Delete, to delete the selected critical command from ARCON PAM.
Follow the below steps:
Select/Enter the details and click Create. A window pops up with the following message:
New Service Critical Commands Created.
Click OK. The new critical command is defined.
To modify a critical command, select the required command from the grid on the left
pane. The Command details are displayed on the right side. Modify the required
details and click Modify button, to update the Command details.

## [p638]

www.arconnet.com|Copyright © 2025 638
1.
2.
3.
4.
4.3.9.5.6 Add Services in DMZ Supporting Server
4.3.9.5.6.1 What is DMZ or Demilitarized Zone?
A DMZ or Demilitarized Zone is a secure server that adds layer of security to a network and acts as a buffer
between a local area network (LAN) and a less secure network which is the Internet. In computer security, a
DMZ is a physical or logical subnetwork that contains and exposes an organization's external-facing services to
an untrusted network, usually a larger network such as the Internet. Therefore, as a DMZ segment a network,
security controls can be tuned specifically for each segment. This section helps you to add services to the DMZ
Server.
4.3.9.5.6.2 How to Add Services in the DMZ Supporting Server?
To add a service in the DMZ Supporting Server, use the following path:
Manage → Users and Services → Manage Services
Right-click on a service whose ports are open to DMZ Servers.
Choose Add To DMZ Supporting Server List option from the list. A window pops up with the following
message:
Are You Sure You Want To Add The Selected Service To Supporting Service(s) For DMZ Server List?
Click Yes. Another window pops up with the following message:
Selected Services Has Been Added To Supporting Services For DMZ Servers List.
Click OK. The service is added to DMZ Server List.
•
•
To modify an existing defined command, select the command from the grid and modify the
required changes and then click Modify to modify the changes.
To delete an existing command, select the critical command from the grid and click Delete to
delete the details

## [p639]

www.arconnet.com|Copyright © 2025 639
1.
4.3.9.5.6.3 How to view the added services in DMZ Zone?
To view the added services in DMZ Zone follow the below steps:
Click Supporting DMZ icon. The Supporting Services For DMZ Servers window pops up.

## [p640]

www.arconnet.com|Copyright © 2025 640
2.
1.
View the added services and click Close.
4.3.9.5.7 Bulk Update
This section explains the steps to bulk update and delete services. The Administrators are responsible for
updating and deleting services.
4.3.9.5.7.1 How to Bulk Update or Delete Service?
To Bulk Update or Delete Services, use the following path:
Manage → Users and Services → Manage Services
Select the particular LOB for which the Bulk Update or Delete has to be performed.

## [p641]

www.arconnet.com|Copyright © 2025 641
2.
3.
4.
Click the Bulk Update option, the following window will be displayed.
Select the Service Type from the dropdown for which you want to do a bulk update or delete and click
Refresh.
It will list all the services under the selected service type, and select the services for which you want to
do a bulk update or delete.

## [p642]

www.arconnet.com|Copyright © 2025 642
5.
6.
7.
8.
Select the checkboxes on the Bulk Update Services form on the right side.
Enter the changes that you want to make on the form and click Update to do a Bulk update of the
selected services.
For Example: If you want to change the port number for all the selected services, enter the new port
number on the form and click update to bulk update the port number for all the selected services.
For Bulk Delete the above steps 1-4 should be followed.
Click the Drop button to delete the services, the following two options will be displayed.
If Service Windows Process Elevation  checkbox is configured to Yes,  then it will allow to
elevate processes for selected services in bulk. In other words, it allows Users to elevate
processes assigned to services.

## [p643]

www.arconnet.com|Copyright © 2025 643
a.
b.
1.
Disable Service:  Click this button to delete the service temporarily, the service will be listed
under disabled services on the Managed Services page
Permanently Delete Service: Click this button to permanently delete all the selected services.
4.3.9.5.8 Service Quick Search
This section explains the steps to search for a service. The Administrator who knows details of the service such
as IP Address, Hostname, name of Domain, user name of service, or type of service can search for a service
using the Quick Search option.
4.3.9.5.8.1 How to search for a service using Quick Search?
To search for a service using Quick Search, use the following path:
Manage → Users and Services → Manage Services
Click the Quick Search   icon.

## [p644]

www.arconnet.com|Copyright © 2025 644
2. The Services - Quick Search window pops up.

## [p645]

www.arconnet.com|Copyright © 2025 645
3.
4.
5.
6.
7.
8.
You can enter part of Service in All Parts of Service  field and click Search  button. Details will be
displayed in grid view.
Click Export button to export the service details.
Click Select All link to select details displayed in grid view.
Click Select Column link to select columns to be displayed.
Select the required Column Name and click OK.
Service details will be displayed in selected columns.

## [p646]

www.arconnet.com|Copyright © 2025 646
1.
2.
3.
4.
5.
6.
4.3.9.5.9 Copy Service Details
This section explains the steps to copy the details of one service to another. You can copy all details displayed in
the Create/Modify Services screen under Manage Services.
4.3.9.5.9.1 How to Copy Details of Service?
To copy details of Service, use the following path:
Manage → Users and Services → Manage Services
Right click on the Connections from the Available Services list. A multiple options list is popped up.
Click Copy Service Details option.
The following success message will be displayed.
Service Details Copied To Clipboard
Click OK. The service details displayed in Create/Modify Services screen are copied to clipboard.
Select   icon displayed in top left under Create/Modify Services screen.
A multiple options list is popped up. Click the Paste Service Details option.

## [p647]

www.arconnet.com|Copyright © 2025 647
7.
8.
1.
Service Details will be copied in fields.
Edit required details and click Create button to create new Service.
4.3.9.5.10 Modify Service Parameters
This section helps you to schedule password change process for a particular service.
4.3.9.5.10.1 How to Schedule password change process for a service?
To schedule password change process for a particular service use the following path:
Manage → Users and Services → Manage Services
The services available in the grid are displayed based on the LOB and service type selected from
the Select LOB/Profile drop-down list (in the home screen Server Manager) and Service Type drop-
down list respectively. Click Refresh button after selecting the LOB and Service Type.

## [p648]

www.arconnet.com|Copyright © 2025 648
2.
3.
Right-click on the service for which you want to schedule the password change process and
choose Modify Service Parameters option.
The Manage Services - Modify Parameters screen is displayed.
The Manage Services – Modify Parameters screen displays the following fields:

## [p649]

www.arconnet.com|Copyright © 2025 649
•
•
•
•
•
•
•
•
•
•
•
Field Name Description
Service Type -
Version
Select the service type version from the dropdown list.
Change
Password on
Session
Disconnection
The password of the service changes after the session is closed from the PAM.
On enabling the checkbox, the following popup window comes up- Enabling this option
might affect existing sessions or immediate reconnection of the same service.?
Allow Auto heal To enable auto-healing for the service.
Auto healing is supported by the following service types-
SSH Telnet
MS SQL EM - Local
MySQL QA
SSH LINUX
MS SQL QA
MS SQL EM - RDP
SSH Router
SSH Switch
SSH Firewall
SSH Unix
ORACLE QA
•
•
Commands are displayed in the dropdown list based on the selected
Service Type.
The commands configured under Custom Commands Configuration
screen is displayed in this dropdown.
The password change will happen for only those services which are configured
in ARCOSSPC- Supported Service Tyes in Settings.
For SSH Telnet service En Account must be there in the Server Manager.

## [p650]

www.arconnet.com|Copyright © 2025 650
•
•
•
•
•
•
•
•
•
•
Field Name Description
Allow
Reconciliation
To enable reconciliation for the service.
Reconciliation is supported by the following service types-
SSH Telnet
MS SQL EM - Local
MySQL QA
SSH LINUX
MS SQL QA
MS SQL EM - RDP
SSH Router
SSH Switch
SSH Unix
ORACLE QA
Min Password
Age
Select minimum days for the scheduled password change process.
Max Password
Age
Select maximum days for the scheduled password change process.
Use Global
Password Policy
Select to enable the global policy configured for the password change process.
Password Policy Select the password policy.
Allow Scheduled
Password
Change
Select to enable/configure the scheduled password change process.
Auto Discovery Select this check box to enable Auto-Discovery of users on a particular server.
Password of Service will not be changed before the defined minimum days.
Eg.: If you configure Minimum Password Age as 3; then the password change
process cannot be performed before 3 days.
The password change process will be scheduled automatically depending on the
selected max password age field.
By default, Default Profile is selected. You can create your own password policy,
save it and select it in this field.
By enabling this checkbox the password change process for the selected service
will be scheduled according to the selected min and max password age and
selected password policy or the global password policy.

## [p651]

www.arconnet.com|Copyright © 2025 651
1.
Field Name Description
Criticality Level Select the criticality level of the service.
Service
Classification
Select the Service Classification.
Service Configuration
To Add the Service Configuration details, Click Add on the top right side.
This criticality level shall be considered while displaying reports.
•
•
The value displayed here is the value that is configured in Settings →
Service → Service Modifications → Service Classification.
This classification level shall be considered while displaying reports.

## [p652]

www.arconnet.com|Copyright © 2025 652
2.
a.
b.
c.
d.
e.
f.
3.
Select the checkboxes to configure that particular configuartion for the service.
Session Lock Out Time (in Minutes): This option will set the duration after which an idle session
should be locked out. Specify the time after which the session will be locked out if idle.
Disable Video Log:  This configuration will check whether the images are to be captured during
the session or not.  If the value is 1, then it will not capture images. If the value is 0, then it will
capture images.
Enable Text Log: This configuration will check whether the text logs are to be captured or not for
a service. If the value is 1, then it will capture the text logs. If the value is 0, then it will not capture
the text logs.
Enable SSM Log: This configuration will check whether the session monitoring logs are to be
captured or not for a service. If the value is 1, then it will capture the session monitoring logs. If
the value is 0, then it will not capture the session monitoring logs.
Use Service for Windows Process Elevation: This configuration will check whether the service
can be used for Windows Process Elevation. If the value is 1, use the service for Windows Process
Elevation. If the value is 0, then it will not use the service for Windows Process Elevation.
Use Service for Remote Assist Elevation: This configuration will check whether the service can
be used for Remote Assist Elevation. If the value is 1, use the service for Remote Assist Elevation.
If the value is 0, then it will not use the service for Remote Assist Elevation.
Click Add. The added configuration shall be displayed under service configuration, modify the value as
per requirement

## [p653]

www.arconnet.com|Copyright © 2025 653
4. Click Modify, parameter updated screen shall be displayed
4.3.9.5.10.2 Windows Process Elevation
Follow the below steps for windows process elevation:

## [p654]

www.arconnet.com|Copyright © 2025 654
1.
2.
3.
Right-click on the service for which you want to use for Windows Process Elevation and choose Modify
Service Parameters option.
The Manage Services - Modify Parameters screen is displayed.
Now add the Process Elevation Service Configuration details, Click Add on the top right side, a new
window shall be displayed.

## [p655]

www.arconnet.com|Copyright © 2025 655
4.
Select Use Service for Windows Process Elevation and click Add

## [p656]

www.arconnet.com|Copyright © 2025 656
5.
6.
7.
The added configuration shall be displayed under service configuration as follows:
By default, the value shall be 0, to enable Process Elevation modify the value to 1 and click Modify.
Parameter updated screen shall be displayed on successful modifying the parameters.
4.3.9.6 Revoke and Share
4.3.9.6.1 What is Revoke and Share?
ARCON PAM supports remove and share feature wherein an Administrator can remove users, user group,
services, and server group from a particular LOB. An Administrator can use Remove function, when he does not
want to allow any authorization to the users to access any services. In addition, an Administrator can share

## [p657]

www.arconnet.com|Copyright © 2025 657
•
•
•
•
•
•
•
1.
users between LOB’s. A Share function is used, when a user is part of two different LOB’s and he needs
authorization to access the services belonging to those LOB’s.
4.3.9.6.2 Why is Revoke and Share Needed?
The Remove  function ensures security and access control by revoking authorizations for users who
should no longer access certain services.
The Share  function allows flexibility by enabling users to have authorized access to services across
multiple LOBs, which is essential for users working in cross-functional roles or projects.
This section includes the following topics:
Remove Users from LOB
Remove User Groups from LOB
Remove Services from LOB
Remove Service Groups from LOB
Share Users between LOB's
4.3.9.6.3 Remove Users from LOB
This section helps you to remove users from a particular LOB. You can remove users from a particular LOB
using Map LOB/Users screen.
4.3.9.6.3.1 How to remove Users from a Particular LOB?
To remove users from a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Users
Select the required LOB. A list of Users mapped to the LOB are displayed.
The Administrator having Revoke LOB From User privilege will only be able to revoke user from LOB.

## [p658]

www.arconnet.com|Copyright © 2025 658
2.
3.
4.
1.
2.
Right click on the selected user. A Remove User From LOB option is popped up.
Click Remove User From LOB. A window pops up with the following message:
User(s) Removed From LOB
Click OK. The selected user is removed from the LOB.
4.3.9.6.4 Remove User Groups from LOB
This section helps you to remove user groups from a particular LOB. You can revoke user groups from a
particular LOB using the Map LOB/User Groups screen.
To remove user groups from a particular LOB:
To remove user groups from a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/User Groups
Select required LOB. A list of User Groups are displayed.
Right click on the selected user group. A Remove User Group From LOB option is popped up.
The Administrator having Revoke LOB From User Group privilege will only be able to revoke user
group from a particular LOB.

## [p659]

www.arconnet.com|Copyright © 2025 659
3.
4.
1.
2.
Click Remove User Group From LOB. A window pops up with the following message:
User Group Removed From LOB
Click OK. The selected user group is removed from the LOB.
4.3.9.6.5 Remove Services from LOB
This section helps you to remove services from a particular LOB. You can revoke services from a particular LOB
using the Map LOB/Services screen.
4.3.9.6.5.1 How to remove services from a particular LOB?
To remove services from a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Services
Select required LOB. A list of services are displayed.
Select the service and click on the  icon to select the entire row.
The Administrator having Revoke LOB From Service privilege will only be able to revoke services
from a particular LOB.

## [p660]

www.arconnet.com|Copyright © 2025 660
3.
4.
5.
Right click on the selected service. A Remove Service From LOB option is popped up.
Click Remove Service From LOB. A window pops up with the following message:
Services(s) Removed From LOB
Click OK. The selected service is removed from the LOB.

## [p661]

www.arconnet.com|Copyright © 2025 661
1.
2.
3.
4.
4.3.9.6.6 Remove Service Groups from LOB
This section helps you to remove service groups from a particular LOB. You can revoke service groups from a
particular LOB using the Map LOB/Service Group screen.
4.3.9.6.6.1 How to Remove Service Groups from a Particular LOB?
To remove service groups from a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Services
Select the required LOB. A list of Service Groups are displayed.
Right click on the selected service group. A Remove Service Group From LOB option is popped up.
Click Remove Service Group From LOB. A window pops up with the following message:
Service Group Removed From LOB
Click OK. The selected service group is removed from the LOB.
The Administrator having Revoke LOB From Service Group privilege will only be able to revoke
service group from a particular LOB.

## [p662]

www.arconnet.com|Copyright © 2025 662
4.3.9.6.7 Share Users between LOB's
This section helps you to share users from one LOB to another LOB. Therefore, a user is able to access servers
in multiple LOB(s).
4.3.9.6.7.1 How to share users between LOB(s)?
To share users between LOB(s) use the following path:
Manage → LOB/Profile Master and Manager → LOB Shared Users

## [p663]

www.arconnet.com|Copyright © 2025 663
1.
2.
3.
4.
Select the LOB from the Select LOB dropdown list.
Select the LOB from the Shared For LOB/Profile dropdown list, where a user has to be shared.
Click Add User button. The Select From List screen is displayed.
Select the username and double-click on the  icon. A window pops up with the following message:
New User Added To Shared User List
4.3.9.7 Groups
4.3.9.7.1 What are Groups?
A Group is a collection of users or servers. The Users created are grouped, such as Admin Users, Network
Users, etc. Similarly, Server Groups are created grouped according to the service provided on the server. For
example, users accessing Windows are grouped as Windows Admin, and Linux as Linux Admin. Similarly,
services are grouped as Windows Services, Linux Services, etc.

## [p664]

www.arconnet.com|Copyright © 2025 664
•
•
•
•
•
•
•
•
1.
For effective inventory management, services and users have been mapped. Therefore, to reduce the
complications, we segregate them into two broad categories:
User Group (based on users)
Server Group (based on services)
4.3.9.7.2 Why are Groups Important?
They simplify inventory and access management by organizing users and services into structured,
manageable units.
They reduce administrative complexity in large environments by allowing bulk policy application and
access mapping.
They support scalability, making it easier to onboard new users or services without reconfiguring
individual permissions.
4.3.9.7.2.1 This section includes the following topics:
Create User and Server Group
Modify details of User or Server Group
Manage Group Utility
4.3.9.7.3 Modify details of User or Server Group
You can modify the details of a particular user or server group using the Create/ Modify Group screen.
4.3.9.7.3.1 How to modify the details of a User Group/ Server Group?
To modify details of a user/server group, use the following path:
Manage → Users and Services → Manage Groups
Click the Manage Groups sub-menu. The Manage Groups screen is displayed.
The Administrators having Read Only Access privilege (under Manage Group) can view details
displayed under Manage Groups, Manage Groups/Services and Manage Groups/Users.
The Administrator, having Modify Group privilege, shall only be able to modify User or Server Group
details.

## [p665]

www.arconnet.com|Copyright © 2025 665
2.
3.
4.
5.
1.
Select the LOB and type of group from the Select LOB/Profile and Group Type dropdown lists,
respectively. A list of user or server groups are displayed in the grid.
Select a group name from the list of groups under the Manage Groups grid. The details are populated in
the Create/Modify Group fields.
Modify the required changes in the existing fields and click Modify. A window pops up with the following
message:
Selected Group Updated.
Click OK. The details of the group are modified.
4.3.9.7.4 Create User and Server Group
4.3.9.7.4.1 What is a Group?
A group is a collection of users or servers. For a user to access a service, the user has to be part of at least one
User Group, and the user group has to be part of at least one Server Group. This section helps you to create
groups such as User or Server Group. In addition, you can modify the details of the User or Server Group.
4.3.9.7.4.2 How to Create Groups?
To create groups, use the following path:
Manage → Users and Services → Manage Groups
Click the Manage Groups sub-menu. The Create/Modify Group screen is displayed.
The Administrator, having the Add Group privilege, shall only be able to create a User or Server
Group.

## [p666]

www.arconnet.com|Copyright © 2025 666
The Create/ Modify screen contains the following fields:
Field Name Description
Create (radio button) Select to create a group.
Modify (radio
button)
Select to modify the details of an existing group.
To search a specific set of rows, enter keywords (space-separated) on the column's header, and the
relevant rows are pulled out.
To modify details of the Group, select the required User or Server Group from
the grid on the left pane. The Group details are displayed under the Create/
Modify Group pane on the right side. Modify the required details and click the
Modify button to update the Group details.

## [p667]

www.arconnet.com|Copyright © 2025 667
•
•
Field Name Description
Group Type Displays the type of group.
The valid values are:
User Group
Server Group
Group Name Specify the group name for users or services.
Group Description Specify the description for the group.
Drop button Click Drop to delete the group from ARCON PAM.
Disable Video Logs Select this Checkbox to Disable Video Logs for any particular Server Group.
2. Enter the fields and click Create. A window pops up with the following message:
New Group Created
3. Click OK. A new user or service group is created.
4.3.9.7.5 Manage Group Utility
4.3.9.7.5.1 What is the Manage Group Utility?
Manage Group Utility is used to transfer server connections from one Server Group to another Server Group.
Suppose there are two server groups, for example, Server Group 1 and Server Group 2. The Server Group 1 is
The data in this field is auto-populated once you select the Group
Type under the Manage Groups section.
•
•
The Administrator, having Drop Group privilege, shall only be able to
delete a User or Server Group.
To drop a Group, select the required User or Server Group from the
grid on the left pane. The Group details are displayed under the Create/
Modify Group pane on the right side. View the details and click Drop, to
delete the Group from ARCON PAM
This field is displayed if the Disable Video Logs by Server Group toggle value
in Settings is enabled.
•
•
The new group created is displayed under the Manage Groups grid, once you have mapped it
under a particular LOB.
Similarly, follow the above steps to create a Server Group by selecting Group Type as Server
Group.

## [p668]

www.arconnet.com|Copyright © 2025 668
1.
2.
3.
mapped to User Group 1. However, through Manage Group Utility, the connections from Server Group 1 is
completely removed and transferred to Server Group 2. Then the User Group 1 will have all the connections of
Server Group 2.
4.3.9.7.5.2 How to Manage Groups?
To transfer server connections, use the following path:
Manage → Users and Services → Manage Groups
Click the Manage Groups sub-menu. The Create/Modify Group screen is displayed.
Select LOB from the Select LOB/Profile dropdown list and then click on the Manage Group Utility
icon. The Manage Group – Utility screen is displayed.
Select the Server Group option from the Group Type dropdown list. A list of services are displayed in
the grid.

## [p669]

www.arconnet.com|Copyright © 2025 669
4.
5.
6.
In the Transfer Groups panel, select the server from the Select Group Transfer To dropdown list to
which the connection is to be transferred.
Select the server group from the list on the left pane and right-click on the selected server group.
Click Add To Transfer Queue. The selected server group is added to the Group list in the Transfer
Groups grid.

## [p670]

www.arconnet.com|Copyright © 2025 670
7.
8.
•
•
•
•
Click the Transfer Groups button to transfer the connections from one server group to another. A
window pops up with the following message:
Group Transfer Process Completed
Click OK. The connection is transferred to the server group.
4.3.9.8 Mappings
4.3.9.8.1 What is Mapping?
Mapping is the process, wherein the created entities such as LOB’s, Users, Services, User Groups, and Server
Groups are mapped with each other in order to establish connection to the server. It is performed for effective
management of entities in ARCON PAM.
4.3.9.8.2 Why is Mapping Needed?
It establishes the necessary relationships between users and the resources they need to access.
It allows for granular access control, ensuring that only authorized users can connect to specific services
or servers.
It streamlines management by organizing entities into logical groups, which simplifies policy
enforcement and auditing.
4.3.9.8.2.1 This section includes the following topics:
Map Users to LOB
You cannot transfer the connections to the same server group. For example, if you select Network
Admin as the server group, then you cannot transfer the connections to the same Network Admin
group.

## [p671]

www.arconnet.com|Copyright © 2025 671
•
•
•
•
•
•
•
•
•
1.
Map Services to LOB
Map User Group to LOB
Map Service Group to LOB
Map Users to User Group
Map Services to Server Group
Map Server Group to User Group
Map Services to a User
Map Service to Multiple Users
Automatically Map User to Service and Vice Versa
4.3.9.8.3 Map Users to LOB
This section helps you to map Users to a particular LOB. You can map Users to a particular LOB using the Map
LOB/Users screen.
4.3.9.8.3.1 How to Map Users to a Particular LOB?
To map users to a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Users
Select the LOB from Select LOB field and click Add button.
•
•
The Administrator having Assign LOB To User privilege will only be able to map User to a
particular LOB.
If toggle value for LOB - Share All Users in Settings is Enabled, then the Users can be mapped
to multiple LOB.

## [p672]

www.arconnet.com|Copyright © 2025 672
2.
3.
4.
The Selection List screen is displayed, then select the checkbox from the list and click Add button.
A window pops up with the following message:
New User(s) Added To LOB
Click OK. The users are mapped to the particular LOB.
4.3.9.8.3.2 User LOB/Profile Management
You can map a User to multiple LOBs using User LOB/Profile Management option under Manage Users tab.
4.3.9.8.3.3 How to Map User to LOB?
To map User to LOB use the following path:
Manage → Users and Services → Manage Users
The toggle value for LOB - Share All Users in Settings should be Enabled, to map User to multiple
LOBs using User LOB/Profile Management option.

## [p673]

www.arconnet.com|Copyright © 2025 673
1.
2.
3.
Right-click on the User name from the User Display Name list. A multiple options list is popped up.
Click User LOB/Profile Management option. The LOB / Profile Management screen is displayed.
Click Add New. The Selection List screen is displayed, then select the LOB and double-click on the
icon.

## [p674]

www.arconnet.com|Copyright © 2025 674
4. The selected LOB is displayed in LOB / Profile Management screen.
To search a specific set of rows, enter keywords (space separated) on the column's header, and
the relevant rows are pulled out

## [p675]

www.arconnet.com|Copyright © 2025 675
5.
6.
To remove User to LOB mapping, select the LOB, right-click and select Remove.
The selected LOB will be removed from LOB / Profile Management screen.
4.3.9.8.4 Map User Group to LOB
This section helps you to map User Group to LOB. You can map User Group to a particular LOB using the Map
LOB/User Groups screen.
4.3.9.8.4.1 How to Map User Groups to a Particular LOB?
To map user groups to a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/User Groups
The Administrator having Assign LOB To User Group privilege will only be able to map User Group to
a particular LOB.

## [p676]

www.arconnet.com|Copyright © 2025 676
1.
2.
3.
4.
Select the LOB from the Select LOB dropdown list and click on Add User Groups button.
The Selection List screen is displayed, then select the group name and double-click on the  icon.
A window pops up with the following message:
New User Group Added To LOB
Click OK. The selected user group is mapped to a particular LOB.
4.3.9.8.5 Map Users to User Group
This section helps you to map Users to a particular User Group. Users can access the services belonging to a
particular User Group, only when the services are mapped to the Users of that User Group.
The Administrator having Assign User Group privilege will only be able to map Users to a particular
User Group.

## [p677]

www.arconnet.com|Copyright © 2025 677
1.
2.
3.
4.3.9.8.5.1 How to Map Users to User Group?
To map Users to a particular User Group use the following path:
Manage → Users and Services → Map Groups/Users
Click Map Groups/Users sub menu. The Group Users screen is displayed.
Select LOB and the user group from the Select LOB/Profile and User Group dropdown list respectively.
Select the group name from the Not In Group dropdown list, wherein it displays all those users, which
are not present in the selected user group.
To search a specific set of rows, enter keywords(space separated) in the search text field of user
group dropdown and the relevant rows are fetched

## [p678]

www.arconnet.com|Copyright © 2025 678
4.
5.
1.
Select the user from the Users Not in Selected Group grid list and click on << Add button. The selected
user is added on the left hand side, in User in Selected Group list.
Similarly, you can remove users from the particular user group by selecting the user from the list
of Users in Selected Group and then click on the Remove >> button.
4.3.9.8.5.2 User Group Management
You can map a User to multiple User Groups using User Group Management option under Manage Users tab.
4.3.9.8.5.3 How to Map User to User Group?
To map User to User Group use the following path:
Manage → Users and Services → Manage Users
Right-click on the User name from the User Display Name list. A multiple options list is popped
up. Click User Group Management option.
Select the User Not In Any Group checkbox, to display the list of all the users which are
mapped to a particular LOB but are not present in any user group.
To search a specific set of rows, enter keywords (space separated) on the column's
header, and the relevant rows are pulled out.
The Administrator having Revoke User Group privilege will only be able to remove Users
mapped to User Group.

## [p679]

www.arconnet.com|Copyright © 2025 679
2.
3.
The Group Management screen is displayed. It displays the list of User groups already mapped to the
User.
Click Add New Group to map a new User Group to the User. A pop up comes up- Do you want to
perform this operation? Select Yes.
To search a specific set of rows, enter keywords (space separated) on the column's header, and
the relevant rows are pulled out

## [p680]

www.arconnet.com|Copyright © 2025 680
4. The Selection List screen is displayed, select the Server Groups checkbox to which the Service should be
mapped and select Add.
On clicking Add the User group is mapped to the User either directly or goes under approval to
higher level admins depending on the workflow.

## [p681]

www.arconnet.com|Copyright © 2025 681
5.
6.
The selected User Group is displayed in Group Management screen.
To remove User Group from the User, select the User Group, right-click and select Remove From Group
or select the checkbox beside the User Groups and select remove.

## [p682]

www.arconnet.com|Copyright © 2025 682
7.
1.
The selected User Group will be removed from Group Management screen.
4.3.9.8.6 Map Services to LOB
This section helps you to map Services to a particular LOB. You can map Services to a particular LOB using
the Map LOB/Services screen.
4.3.9.8.6.1 How to Map a service to a particular LOB?
To map a service to a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Services
Select the LOB from the Select LOB dropdown list and click on the Add Service button.
On clicking Remove, the User group is revoked from the User either directly or goes under
approval to higher level admins depending on the workflow.
The Administrator having Assign LOB To Service privilege will only be able to map Services to LOB.

## [p683]

www.arconnet.com|Copyright © 2025 683
2.
3.
4.
The Selection List screen is displayed and then select the checkbox and click on Add button.
A window pops up with the following message:
New Service(s) Added To LOB
Click OK. The new service is added to LOB.
4.3.9.8.7 Map Service Group to LOB
This section helps you to map Service Group to a particular LOB. You can map Service Group to a particular
LOB using the Map LOB/Service Groups screen.
4.3.9.8.7.1 How to Map Service Group to a particular LOB?
To map a service group to a particular LOB use the following path:
Manage → LOB/Profile Master and Manager → Map LOB/Service Groups
The Administrator having Assign LOB To Service Group privilege will only be able to map Service
Group to a particular LOB.

## [p684]

www.arconnet.com|Copyright © 2025 684
1.
2.
3.
4.
Select the LOB from the Select LOB drop down list and click the Add Service Groups button.
The Select From List screen is displayed, then select the service group and double click   icon.
A window pops up with the following message:
New Service Group Added To LOB
Click OK. The Service Group is mapped to LOB.
4.3.9.8.8 Map Services to Server Group
This section helps you to map Services to a particular Server Group. You can map Services to a particular Server
Group using the Map Groups/Services screen.
The Administrator having Assign Service To Service Group privilege will only be able to map services
to a particular Service Group.

## [p685]

www.arconnet.com|Copyright © 2025 685
1.
2.
3.
4.
4.3.9.8.8.1 How to Map Services to Server Group?
To map services to a server group use the following path:
Manage → Users and Services → Map Groups/Services
Click Map Groups/Services sub menu. The Groups Services screen is displayed.
On the left pane, select/enter the server group from the Server Group dropdown list respectively and
click on Refresh button, to view the services belonging to the selected server group.
Select the Server Type from the server type dropdown list.
On the right pane, select the server group from the Server Group dropdown list and select the services
which are to be added to the selected server group.
To search a specific set of rows, enter keywords(space separated) in the search text field of
service group dropdown and the relevant rows are fetched.

## [p686]

www.arconnet.com|Copyright © 2025 686
5. Select the services from the Connections Not Available in Group list and click on << Add button. The
connection is added to the selected server group on the left pane.
Click Not In Group button, to view services which are not present in the selected server
group.
Click In Group button, to view services which are present in the selected server group.
Select Services Not in any Group checkbox, to view services which are mapped to a
particular LOB but not present in any server groups.
To search a specific set of rows, enter keywords (space separated) on the column's
header, and the relevant rows are pulled out.

## [p687]

www.arconnet.com|Copyright © 2025 687
6.
1.
Similarly, you can remove a service from a particular server group by selecting the service from
the Connections Available in Group list and then click on the Remove >> button.
4.3.9.8.8.2 Group Management
You can map service to multiple Server Groups using Group Management option under Manage Service tab.
4.3.9.8.8.3 How to Map Server to Server Group?
To map User to User Group use the following path:
Manage → Users and Services → Manage Service
Right-click on the User name from the User Display Name list. A multiple options list is popped
up. Click Group Management option.
The Administrator having Revoke Service From Service Group  privilege will only be able to
remove Services mapped to Service Group.

## [p688]

www.arconnet.com|Copyright © 2025 688
2.
3.
The Group Management screen is displayed. It displays the list of Server groups already mapped to the
service.
Click Add New Group to map a new Server Group to the Service. A pop up comes up- Do you want to
perform this operation? Select Yes.
To search a specific set of rows, enter keywords (space separated) on the column's header, and
the relevant rows are pulled out

## [p689]

www.arconnet.com|Copyright © 2025 689
4. The Selection List screen is displayed, select the User Groups checkbox to which the User should be
mapped and select Add.
On clicking Add the User group is mapped to the User either directly or goes under approval to
higher level admins depending on the workflow.

## [p690]

www.arconnet.com|Copyright © 2025 690
5.
6.
The selected User Group is displayed in Group Management screen.
To remove the Server Group from the Server, select the Server Group, right-click and select Remove
From Group or select the checkbox beside the Server Group and select remove.

## [p691]

www.arconnet.com|Copyright © 2025 691
7.
1.
The selected Server Group will be removed from Group Management screen.
4.3.9.8.9 Map Server Group to User Group
This section helps you to map Server Groups to User Groups. You can map Server Groups to User Groups using
the Map Group Types screen.
4.3.9.8.9.1 How to Map Server Group to User Group?
To map server group to user group use the following path:
Manage → Users and Services → Map Group Types
Follow the below steps:
Select/Enter the user group from the User Groups dropdown list. The left pane displays all the server
groups, which are already mapped with the user group, and the right pane displays all the server groups
which are not yet mapped with the selected user group.
On clicking Remove, the Server group is revoked from the Server either directly or goes under
approval to higher level admins depending on the workflow.
The Administrator having Assign Service Group To User Group privilege will only be able to perform
group mapping.
To search a specific set of rows, enter keywords(space separated) in the search text field
of user group and service group dropdown and the relevant rows are fetched.
To search a specific set of rows, enter keywords (space separated) on the column's
header, and the relevant rows are pulled out.

## [p692]

www.arconnet.com|Copyright © 2025 692
2.
3.
Select the server group from the right pane and click << Add button. The server group is assigned to the
user group on the left pane.
Similarly, you can remove a server group assigned to a user group by selecting the server group from
the Server Group list on the left pane and then click the Remove >> button.
4.3.9.8.10 Map Services to a User
This section helps you to map Services to a particular User. The connections to the users are established in Map
Users / Services screen. The Services are assigned to a User, based on the Services available in the User Group
and the User shall be part of the User Group.
This will assign all the services of the selected server group to the selected user group.
The Administrator having Revoke Service Group From User Group privilege will only be able to
revoke group mapping.

## [p693]

www.arconnet.com|Copyright © 2025 693
1.
2.
4.3.9.8.10.1 How to Map Services to Users?
To map services to users use the following path:
Manage → Users and Services → Map Users/ Services
Select the user group from the User Groups dropdown list on the left pane. A list of User ID(s) are
displayed.
Select the user ID from the User ID list, wherein it displays all the service details available for that
particular user ID.
•
•
The Administrator having Assign Service To User privilege in Server's Privileges will only be
able to map Services to a particular User.
If the Admin is Server Group Admin, then he should be assigned Assign Service To
User privilege in Group Admin Privileges to map Services to a particular User.
To search a specific set of rows, enter keywords (space separated) on the column's header, and
the relevant rows are pulled out.

## [p694]

www.arconnet.com|Copyright © 2025 694
3.
4.
5.
6.
Select the services from the Service Details list under Available Services section. On selection of the
service, a popup appears requesting to select the access type(Time-based/one-time/permanent) of
service for that user.
Click Add >> button. The services are now assigned to that particular user.
You can view the services assigned to the user in the Service Details list under Assigned
Services section.
Similarly, you can remove Services mapped to a particular User by selecting the user from the list of
services in Assigned Services section and then click the Remove >> button.
The popup will appear only if Time Based Service Access Request From Server Manager - Is
Enabled in Settings.

## [p695]

www.arconnet.com|Copyright © 2025 695
1.
2.
4.3.9.8.11 Map Service to Multiple Users
This section helps you to map Services to single or multiple Users. In addition, it also allows to restrict
commands for a particular User.
4.3.9.8.11.1 How to Map Services to Multiple Users?
To map services to multiple users use the following path:
Manage → User and Services → Group Admin – Map Services
Select required Service Group Admin from the dropdown list in the menu bar.
A window pops up with message: Server Group Selected For Administration: Server Group Name
The Administrator having Revoke Service From User privilege in Server's Privileges will
only be able to remove Services mapped to a User.
If the Admin is Server Group Admin, then he should be assigned Revoke Service From
User privilege in Group Admin Privileges will only be able to remove Services mapped to
a User.
The Administrator having Assign Service To User privilege in Group Admin privileges will only be able
to map Services to multiple Users.

## [p696]

www.arconnet.com|Copyright © 2025 696
3.
4.
5.
Navigate through tabs to view the group name under Group Admin – Map Services text field.
Click Refresh button. The services available in the server group and the service group assigned to user
are displayed in the Connections Available in Group grid and Service Group Assigned To User text field
respectively.
Select the service in Connections Available in Group grid. It displays a list of users to whom the services
are not assigned and assigned in the Service Not Assigned grid and Service Assigned grid respectively.

## [p697]

www.arconnet.com|Copyright © 2025 697
6.
7.
8.
Select the user ID from the Services Not Assigned grid and click Assign >> button. The selected user ID
is displayed in the Service Assigned grid.
Similarly, you can revoke a user to whom a services are assigned by selecting the user from the Service
Assigned grid and then click the << Revoke button.
Select the User ID from the Service Assigned grid and then click Show Commands button. A list of
commands assigned to the user are displayed in the Show Commands list.
The Administrator having Revoke Service From User privilege in Group Admin privileges will
only be able to remove Services mapped to multiple Users.

## [p698]

www.arconnet.com|Copyright © 2025 698
9.
10.
Select the commands checkbox and click the (Apply Changes) Restrict Commands button to restrict the
commands.
A window pops up with message: Commands Restricted/ Applied Successfully For User.
4.3.9.8.12 Automatically Map User to Service and Vice Versa
The Automatically Map User to Server and vice-versa feature allows Administrator to automatically map Users
to Services or Services to User which are mapped to their respective Groups. This feature can be applied at
global level or LOB wise. To automate the feature at global level, the Administrator has to enable the
configurations present in Settings.

## [p699]

www.arconnet.com|Copyright © 2025 699
•
•
•
1.
2.
3.
4.
5.
6.
7.
Pre-requisites:
The User Group should be present in the domain.
The Server Group should be present in the domain.
It is mandatory for the Administrator to map the User Group to the Server Group in the domain.
4.3.9.8.12.1 Automatically Assign Users to all Services
The Administrator has to enable the Settings to automatically assign all services to newly added Users in User
Group. If the Settings value is Disabled and you add a User to User Group, then services are not assigned to the
User. When the Settings value is configured as Enabled and you add a User to User group, the services are
automatically assigned to this User. Whereas, services will not be assigned to Users who were added to User
group before the Settings value was enabled.
To automatically map User to Services, follow the below steps:
Click Manager → Settings, Settings window opens.
Search for Automate User and Service Mapping When user added in UserGroup – Is Enabled. You can
Disable or Enable the feature using the toggle button in Settings.
Enable the toggle value and the settings Value will be updated Successfully.
The Settings to automate the user and service mapping when the user is added to User Group is
configured successfully.
Click Manage → Users and Services → Map Group/Users.
Map User to User Group.
On mapping the User to User Group, as the Settings for automation is Enabled the User is automatically
assigned the Services present in the mapped Server Group.
4.3.9.8.12.2 Automatically Assign Services to All Users
The Administrator has to enable the Settings to automatically assign all Users to newly added Services in
Server Group. If the Settings value is Diabled and you add a Service to Server Group, then Users are not
assigned to the Service. When the Settings  value is configured as Enabled and you add a Service to Server
group, the Users are automatically assigned to this Service. Whereas, Users will not be assigned to Services
which were added to Server group before the Settings value was enabled.
•
•
It is mandatory to map the User Group to Server Group before starting the automation of Users
to Services or Services to Users
To configure Settings, the Administrator should have Default Configuration
and Settings privileges under Server's Privileges.
For more information refer Map User to User Group.
• It is mandatory to map the User Group to Server Group before starting the automation of Users
to Services or Services to Users

## [p700]

www.arconnet.com|Copyright © 2025 700
1.
2.
3.
4.
5.
6.
7.
To automatically assign Service to the Users, follow the below steps:
Click Manager → Settings, Settings window opens.
Search for Automate User and Service Mapping When server added in ServerGroup – Is Enabled. You
can Disable or Enable the feature using the toggle button in Settings.
Enable the toggle value and the settings Value will be updated Successfully.
The Settings to automate the user and service mapping when the user is added to User Group is
configured successfully.
Click Manage → Users and Services → Map Group/Services.
Map Service/s to Server Group.
On mapping the Services to Server Group, as the Settings or automation is Enabled the Service/s is
automatically assigned to the User present in the mapped User Group.
• To configure Settings, the Administrator should have Default Configuration
and Settings privileges under Server's Privileges.
For more information refer Map Services to Server Group

## [p701]

www.arconnet.com|Copyright © 2025 701
5 PAM Access and Dashboard

## [p702]

No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any
means such as electronic, mechanical, photocopying, recording, or otherwise without permission.
1.
2.
3.
4.
5.
•
•
POC (Point of Contact) & Support Information
The product is developed and maintained by ARCON TechSolutions Private Limited. We at ARCON are continuously
thriving to develop and deliver the best quality products. Being our valued customer, we would like to know your
feedback, suggestions, and ideas for improvements with regard to our products and services. You can always reach
out to us through the below ways of communication:
Web
https://arconnet.com/
Sales Contact
You can directly contact us with sales-related topics at the email address sales@arconnet.com, or leave us your
contact information, and we will call you back.
Support Contact
To access ARCON Support Centre (ASC), Sign in with your account.
Remote support is available 24*7.
ARCON Support System is available only for registered users with a valid support package.
ARCON Support Centre (ASC): https://support.arconnet.com/
Central Support E-mail Address: arcos.support@arconnet.com
Support hotline:
Global: +91 8080005577 (For ARCON PAM Support Press 1)
UAE: 800035703628 (Press 1)
