# Client Manager Guide.pdf

Source: `data/sources/Client Manager Guide.pdf` - 399 pages.

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
1 Client Manager Guide .................................................................................................................................................................5
1.1 Introduction .................................................................................................................................................................................5
1.2 Basic Terminology for ARCON | PAM ...............................................................................................................................5
1.3 Logging In to ARCON | PAM..................................................................................................................................................6
1.3.1 Overview .................................................................................................................................................................................... 6
1.3.2 Pre-requisites ........................................................................................................................................................................... 6
1.3.3 How to Log in to ARCON | PAM........................................................................................................................................ 8
1.3.3.1 Login with ARCON | PAM Authentication.................................................................................................................. 8
1.3.3.2 Login with SAML Authentication................................................................................................................................. 10
1.3.3.3 Login with Microsoft Authentication......................................................................................................................... 11
1.3.3.4 Login with ADFS (Active Directory Federation Service) Authentication.................................................... 12
1.3.4 Dual/Multi Factor Authentication .................................................................................................................................13
1.3.4.1 Overview ............................................................................................................................................................................... 13
1.3.4.2 TOTP Authenticator ......................................................................................................................................................... 14
1.3.4.3 ARCON Authenticator Mobile App OTP.................................................................................................................. 15
1.3.4.4 SMS OTP................................................................................................................................................................................ 17
1.3.4.5 Email OTP.............................................................................................................................................................................. 19
1.3.4.6 Hardware Token................................................................................................................................................................. 20
1.3.4.7 Biometric - Finger Print ................................................................................................................................................... 21
1.3.4.8 Voice Biometric................................................................................................................................................................... 23
1.3.4.9 Facial Recognition.............................................................................................................................................................. 23
1.3.4.10 FIDO2 Authenticator ....................................................................................................................................................... 24
1.3.5 Enforce Self Registration (ESR) .......................................................................................................................................28
1.4 ARCON PAM Help and Learning Center....................................................................................................................... 28
1.4.1 Overview ..................................................................................................................................................................................28
1.4.2 ARCON Learning Center ...................................................................................................................................................32
1.5 Menu Bars .................................................................................................................................................................................. 34
1.5.1 Top Menu..................................................................................................................................................................................34
1.5.2 Left Side - Header Menu Bar ............................................................................................................................................35
1.5.3 Right Side - Icons ...................................................................................................................................................................35
1.5.4 Side Menu.................................................................................................................................................................................36
1.5.5 Top Menu Bar .........................................................................................................................................................................37
1.5.5.1 My Access.............................................................................................................................................................................. 38

## [p4]

www.arconnet.com|Copyright © 2025 4
1.5.5.2 Manager ................................................................................................................................................................................. 46
1.5.5.3 Reports .................................................................................................................................................................................126
1.5.5.4 Dashboard...........................................................................................................................................................................342
1.5.5.5 About.....................................................................................................................................................................................359
1.5.6 Side Menu Bar ..................................................................................................................................................................... 361
1.5.6.1 Side Menu............................................................................................................................................................................361
1.5.6.2 RaiseRequest .....................................................................................................................................................................362
1.5.6.3 Pending Requests.............................................................................................................................................................388
1.5.6.4 Request Logs ......................................................................................................................................................................394
1.5.6.5 My Service...........................................................................................................................................................................397
1.6 About The Client Manager Guide.................................................................................................................................. 397
1.6.1 Related Documents........................................................................................................................................................... 397
1.6.2 Acronyms............................................................................................................................................................................... 397
1.6.3 POC (Points of Contact) & Support Information................................................................................................... 398

## [p5]

www.arconnet.com|Copyright © 2025 5
•
•
•
•
•
1.
2.
1 Client Manager Guide
1.1 Introduction
The ARCON | PAM Client Manager Online (ACMO), also known as Client Manager (CM), is a web console used
by Client users to access target operating systems, databases, and networking devices. This web console
supports multi-domain authentication, multi-factor authentication, multi-tenancy, and target connectors. The
CM provides a single console to users accessing different devices, OSes, or databases from a single location.
Through the Client Manager, a user can access services, raise requests, and view logs and reports.
ARCON PAM Client Manager grants power to get control over the following:
Remote control security for essential endpoints
Obtain complete access to all privileged accounts
Control access requests and permissions precisely
Track and examine privileged user activity
Ensure security adherence
This guide provides the detailed usage and benefits of each functionality available in the Client Manager, with
illustrations for easy understanding of the material. Please refer below for an index of the sections explained in
this guide.
1.2 Basic Terminology for ARCON | PAM
Some basic terminology used in this guide are mentioned below.
Entity Meaning
LOB An LOB or Line of Business is a group or family of
products or services managed by a specific team or
department in the organizational hierarchy. It is
defined differently in different organizations
depending on their size, number of users, number of
services, regions of operation, and other factors.
Users, services, and groups are organized by LOB.
User  User(s) refer to the human identities in an
organization. There are two types of users defined on
the privileges they have:
Administrative users - These are privileged
users who can control what standard users
have access to.
Standard users - These users have a limited set
of privileges and can only perform permitted
activities on the network.

## [p6]

www.arconnet.com|Copyright © 2025 6
•
•
Entity Meaning
Service  Services are the endpoints in an organization that help
in implementing, maintaining, supporting, and
controlling privileged identities. They can be OSes,
databases, or networking devices such as routers,
firewalls, switches, etc. Examples - SSH Linux, MS SQL.
User Group A User Group is a collection of users. These groups are
formed based on the nature of work, team,
department, etc.
Service Group A Service Group is a collection of services. These
groups are formed based on factors like server
locations (MUM DEV SERVER, DEL APP SERVER,
etc.), internal teams (WIN TEAM SERVERS, LINUX
TEAM SERVERS, etc.), or OSes (WIN SERVERS, AIX
SERVERS, LINUX SERVERS, etc.).
Command A Command is an instruction that causes a computer
or a server to perform one of its basic functions.
Session A Session is a specific instance of a user accessing a
service through ARCON | PAM.
Process A Process is an instance of a program running on a
computer.
1.3 Logging In to ARCON | PAM
1.3.1 Overview
Logging refers to the procedure by which a user establishes their identity and authenticity using credentials to
obtain access to ARCON | PAM. The user credentials are username and password. We also utilize second-
factor or dual-factor authentication solutions such as the ARCON authenticator, hardware token, OTP, and
biometric devices for increased protection in your applications due to digital thefts and breaches.
This section explains how to log in to the Client Manager application. It outlines various login options, accessing
the Learning Center, Dual-Factor Authentication, Multi-Factor Authentication, SAML, (ADFS) Active Directory
Federation Service authentication, Microsoft Authorization, and Enforce Self-Registration (ESR).
1.3.2 Pre-requisites
ARCON | PAM must be installed and configured.
You can log in through Google Chrome, Mozilla Firefox, and Microsoft Edge only if the ARCON | PAM
Plugin is installed and configured.
Before ARCON | PAM can be accessed through a web browser, an Implementation Engineer (IE) must install
and configure it. Upon successful configuration and access of the ARCON | PAM application, the ARCON | PAM
(Privileged Access Management) login page will appear.

## [p7]

www.arconnet.com|Copyright © 2025 7
The following table explains the fields displayed on the ARCON | PAM Login screen:
Field Name/Icon Description
Username Enter the username that was given to you by the
administrator. This could be your name or employee
ID.
Password To log in for the first time, enter the password that the
administrator provided to you. The password must
then be reset.
Domain Select the domain from the drop-down list. The
Domain field on the login screen appears only when
the Administrator enables it in Global Configuration.
A particular domain will only be visible on the login
screen if it is active.

## [p8]

www.arconnet.com|Copyright © 2025 8
1.
2.
3.
•
•
•
•
1.
Field Name/Icon Description
Downloadable Icon The downloadable icon helps you to download and
configure the latest ARCON | PAM plugin. This icon
will only be enabled if the latest ARCON | PAM plugin
is not installed.
Click on the downloadable icon to open the
ARCON | PAM Help Center screen.
Download the ARCON | PAM Plugin.
You can get the User Guides and Video
Learning from this screen.
Biometric Authentication Icon The Biometric Authentication icon helps you to do
dual-factor authentication through biometric data
such as your fingerprints. It will be enabled only when
the administrator enables it in Global Configuration.
Login Icon The login icon helps you log in to the PAM application.
The login icon will be enabled if the most recent PAM
plugin is installed and configured. Otherwise, the login
icon will be disabled and the downloadable icon will
prompt you to download the latest PAM Plugin from
the server.
1.3.3 How to Log in to ARCON | PAM
Multiple login options are supported by the ARCON | PAM to enhance user experience. Users can access
numerous service providers by simply signing in once. As a result, the authentication procedure can go more
quickly, and the user does not need to remember numerous login credentials for every application.
ARCON supports many ways to access the ARCON | PAM, and you can do it in one of the following ways:
Login with ARCON | PAM Authentication
Login with SAML Authentication
Login with Microsoft Authentication
Login with ADFS (Active Directory Federation Service) Authentication
1.3.3.1 Login with ARCON | PAM Authentication
The Client user can log in to the ARCON | PAM by using the ARCON | PAM authentication feature. In this, the
Client user needs to enter the PAM credentials provided by the administrator and then reset the password, if
login for the first time.
Follow the steps given below to log in with ARCON | PAM authentication:
Once the login screen appears, enter the PAM username and password credentials.

## [p9]

www.arconnet.com|Copyright © 2025 9
2. Select the domain name from the drop-down and click the Login arrow.

## [p10]

www.arconnet.com|Copyright © 2025 10
2. A password change prompt appears when you log in for the first time. Please change your password toa
new one that is known only to you.
1.3.3.2 Login with SAML Authentication
Security Assertion Markup Language 2.0 (SAML) is an open standard for exchanging identity and security
information with applications and service providers. SAML is used as a Single Sign-on (SSO) to sign in to all of
your ARCON | PAM applications by using a single set of credentials.
Click on the Login with SAML button to log in with SAML authentication:
The Domain field on the login screen appears only when the Administrator enables it in Global
Configuration.
The ARCON | PAM application will prompt for multi/dual-factor authentication if configured by the
Administrator in the Server Manager. Refer to Dual/Multi-Factor Authentication for more information.
The Login with SAML button appears on the login screen only when the administrator enables it in
Global Configuration.

## [p11]

www.arconnet.com|Copyright © 2025 11
1.3.3.3 Login with Microsoft Authentication
Microsoft Azure is a cloud computing service operated by Microsoft for application management via Microsoft-
managed data centers. Login with Microsoft will help users log in to the ACMO application based on the Azure
Active Directory through OAuth.
Click on the Login with Microsoft button to log in with Microsoft authentication
The Login with Microsoft button appears on the login screen only when the administrator enables it in
Global Configuration.

## [p12]

www.arconnet.com|Copyright © 2025 12
1.3.3.4 Login with ADFS (Active Directory Federation Service) Authentication
1.3.3.4.1 Overview
ARCON PAM, a leading solution in the PAM domain, incorporates Active Directory Federation Service (ADFS)
Authentication to fortify its authentication mechanisms and streamline access control.
ADFS Authentication in ARCON PAM enables organizations to leverage their existing Active Directory
infrastructure to authenticate users accessing privileged resources. By integrating with ADFS, ARCON PAM
facilitates seamless single sign-on (SSO) experiences, allowing users to access privileged accounts and
resources with their familiar Active Directory credentials.
At its core, ADFS Authentication in ARCON PAM employs industry-standard protocols such as SAML (Security
Assertion Markup Language) to establish trust between the identity provider (ADFS) and the PAM solution.
This ensures secure authentication and authorization of users, reducing the risk of unauthorized access and
insider threats.
With ADFS Authentication, ARCON PAM empowers organizations to enforce strong authentication policies,
including multi-factor authentication (MFA) and conditional access, to ensure only authorized users gain access
to privileged accounts and sensitive data. Furthermore, ADFS integration enhances interoperability, allowing
seamless integration with other Microsoft ecosystem components and third-party applications.
In this introduction, we'll explore the capabilities of ADFS Authentication in ARCON PAM, highlighting its role
in bolstering authentication security, enhancing user experience, and enabling organizations to achieve
comprehensive privileged access management.

## [p13]

www.arconnet.com|Copyright © 2025 13
• Click on the Login with ADFS button to log in with ADFS authentication
1.3.4 Dual/Multi Factor Authentication
1.3.4.1 Overview
Corporate network environments are typically large, with many points of access that can potentially be
exploited to gain unauthorized entrance to the network, and to the resources and data within that network.
User accessing the target machines with typical username and static passwords presents a single-factor
authentication. Such a process for authentication has quite a few security drawbacks as passwords can be
guessed, forgotten, written down and stolen, eavesdropped on, or deliberately told to other people.
In order to prevent such unauthorized access to the target machine, ARCON | PAM uses a defense-in-depth
strategy whereby the system as a whole is protected by using multiple layers of defense that seek to ensure the
protection individually of each of its components. This technique is commonly known as multi-factor
authentication (MFA).
ARCON | PAM provides a multi-factor authentication (MFA), where the users authenticate themselves with
more than a single factor. That is, along with something a user knows, like a password, an MFA solution will also
require that the user have something that is distinctly theirs, unique to them such as SMS, Fingerprint, OTP, etc.
Hence, the user will have multiple options for authentication when they log in. With a password plus a unique
identifier, the system receives two layers or factors of proof that you are who you say you are.
The Login with ADFS  button appears on the login screen only when the administrator enables it in
Global Configuration.

## [p14]

www.arconnet.com|Copyright © 2025 14
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
The MFA configurations are set by administrators in the Administrative Console. ARCON | PAM supports the
following multi-factor authentications:
TOTP Authenticator
ARCON Authenticator App OTP
SMS OTP
Email OTP
Hardware Token
Biometric-Finger Print
Voice Biometric
Facial Recognition
FIDO2 Authenticator
1.3.4.2 TOTP Authenticator
What is TOTP Authenticator?
TOTP stands for Time-based One-Time Passwords and is a common form of two-factor authentication (2FA).
Unique numeric passwords are generated with a standardized algorithm that uses the current time as input.
The time-based passwords are available offline and provide user-friendly, increased account security when
used as a second factor.
Users, who must have an authenticator app downloaded on their device (such as Google Authenticator,
Microsoft Authenticator, Symantec VIP Authenticator, etc.), are asked to input the unique passcode within a
certain period of time, usually 30 seconds, as evidence of their identity.
To enable Dual Authentication, the TOTP Authenticator must be configured by an Administrator in
the Administrative Console. If the TOTP Validator is configured, a pop-up will appear after entering the login
credentials. Post entering the valid TOTP, the user will be able to log in to ARCON PAM.
1.3.4.2.1 Logging in using TOTP Authenticator
Let us consider the example of Microsoft Authenticator.
Download and install the Microsoft Authenticator App from the Google Play Store on your mobile to configure
mobile TOTP dual-factor authentication.
TOTP Authenticator - Self-Registration
Once Enforce Self Registration for TOTP has been configured for a particular user, the following screen
will be displayed on the screen after ACMO login.
The TOTP - Self Registration needs to be set up only once.

## [p15]

www.arconnet.com|Copyright © 2025 15
2.
3.
1.
2.
After downloading the Microsoft Authenticator  application, open it and scan the QR code. After
scanning, the new account will be added to your QR code application and a time-based OTP will be
generated in your mobile application.
Enter the OTP in the TOTP Self Registration screen and click the Save & Validate button. Once the OTP
is successfully validated, it will redirect you to the ACMO page.
Post TOTP Configuration
Enter the credentials on the ARCON | PAM Login screen and click the Login icon. The TOTP
Validator pop-up will be displayed.
Enter the OTP generated from the Microsoft Authenticator  application in the TOTP Validator screen
and click the Validate OTP button. You will now be allowed to successfully log in to the application.
1.3.4.3 ARCON Authenticator Mobile App OTP
1.3.4.3.1 Overview
A one-time password (OTP) can be obtained on your mobile phone through the ARCON Authenticator mobile
app to securely log into ARCON | PAM. One-time Passwords or OTP are considered a secure way of dual-factor
authentication. Mobile one-time password (OTP) configuration is one of the dual-factor authentications. It is
used by mobile users implementing the mobile application to securely log into ARCON | PAM. The users must

## [p16]

www.arconnet.com|Copyright © 2025 16
1.
2.
download and install the ARCON Authenticator App from the Google Play Store or Apple App Store to their
mobile device to configure mobile OTP dual-factor authentication.
Installing the ARCON Authenticator Application from the Google Play Store or Apple App Store
Download and install the ARCON Authenticator application from the Google Play Store or Apple Store
on your mobile:
Set a Passcode for the first login attempt and re-enter the passcode to confirm:
1.3.4.3.2 ARCON | PAM Mobile App OTP Self-Registration
On the Server Manager, configure Mobile OTP for a particular user.
The following table explains the fields displayed on the ARCON | PAM Mobile OTP - Self Registration screen:
Field Name Description
Unique ID Enter the unique number generated on the ARCON
Authenticator application in the Unique ID field on the desktop. Click the
Validate Unique ID button on the desktop.
Validation Key Generate Validation Password button appears on the desktop. Enter the
validation key on the desktop, which is generated from the ARCON
Authenticator application installed on your mobile. Click the Generate
Validation Password button on the desktop.
The ARCON | PAM Mobile OTP - Self Registration needs to be set up only once.

## [p17]

www.arconnet.com|Copyright © 2025 17
1.
2.
3.
4.
5.
Field Name Description
Validation Password The Validation Password will appear on the desktop. Enter this password
in the Validation Password field and tap on the Validate Phone button
on your mobile. A validation code will be generated on your mobile
device.
Validation Code Enter the validation code generated from your mobile device into the
respective field on the desktop.
Once you enter the validation code in the field, and click the Validate Code button, a message Mobile OTP Self
Registration Successfully completed will be displayed.
1.3.4.3.3 Post Mobile App OTP Configuration
Enter the credentials in the ARCON | PAM Login screen and click the Login icon. The Mobile OTP
Validator pop-up will be displayed with the PIN/Challenge.
Enter the Pin/Challenge in the Enter Challenge text field in the ARCON Authenticator app.
Tap the Generate OTP button to generate the OTP.
Enter the OTP generated by the ARCON Authenticator application in the Mobile OTP Validator screen
on your desktop.
Click on Validate OTP:
1.3.4.4 SMS OTP
What is SMS OTP?
Ensure to enter the Instance Name in the ARCON
Authenticator application before tapping the Validate Phone
button.
You must enter the OTP within 60 seconds for each instance, or the Pin/Challenge will change.

## [p18]

www.arconnet.com|Copyright © 2025 18
1.
2.
3.
4.
1.
2.
SMS OTP is a short message containing a one-time auto-generated password that is sent to the registered
mobile phone number of the user who has initiated the login request. This technology is perhaps the most
popular mechanism used by companies around the world to make sure that the login request has been
generated by an authorized person.
Multifactor authentication can also be completed via SMS OTP, whereby ARCON | PAM users receive an OTP
on their registered mobile number.
1.3.4.4.1 ARCON | PAM SMS OTP - Self-Registration
Perform the following steps to authenticate login using the SMS OTP method:
Once Enforce Self Registration (ESR) for SMS OTP has been configured for a particular user, the following
screen will be displayed on the screen after login.
Enter a valid mobile number with a country code in the text box.
Click on the Validate Mobile No button. The Validate Code button will appear.
You will receive a code via SMS on your registered mobile number. Enter the code in the Validate Code
text box.
1.3.4.4.1.1 Post SMS OTP Configuration
Enter the credentials in the ARCON | PAM Login screen and click Login. The SMS and Email OTP
Validator pop-up will be displayed.
Enter the OTP received via SMS and click the Validate OTP button to log in.
The SMS OTP - Self Registration needs to be set up only once.

## [p19]

www.arconnet.com|Copyright © 2025 19
1.
1.3.4.5 Email OTP
What is Email OTP?
The Email OTP method enables you to authenticate using the one-time password (OTP) that is sent to the
registered email address.
Multi-factor authentication can also be completed via Email OTP, whereby ARCON | PAM users receive an
OTP on their registered email address. By entering the OTP, the user will be able to log in to ARCON | PAM.
Perform the following steps to authenticate login using Email OTP:
Enter the credentials in the ARCON | PAM Login screen and click the Login icon. The SMS and Email
OTP Validator pop-up will appear.
If you do not receive the OTP via SMS for a long duration, click Resend OTP to try again.

## [p20]

www.arconnet.com|Copyright © 2025 20
1.
2. Enter the OTP received via Email and click the Validate OTP  button to log into the ARCON | PAM
application.
1.3.4.6 Hardware Token
What is hardware Token?
A Hardware Token is a security token that may be a physical device that an authorized user of computer
services is given to ease authentication. It may be a small hardware device that the owner carries to allow
access to a network service. In ARCON | PAM, RADIUS servers are used to authenticate an RSA portal.
RADIUS is a protocol that helps to communicate with another server, similar to LDAP, DCPIP, and RDP
protocols.
Perform the following steps to authenticate login using the Hardware Token:
Enter the credentials in the ARCON | PAM Login screen and click the Login icon. The Hardware Token -
Validator pop-up will be displayed.
If you do not get the OTP via Email for a long time, click on the Resend OTP button to try again.

## [p21]

www.arconnet.com|Copyright © 2025 21
2.
1.
Enter OTP received via Email and click on the Validate  button to login into the ARCON | PAM
application.
1.3.4.7 Biometric - Finger Print
What is Biometric Finger Print?
Biometric Device Configuration is a dual-factor authentication supported by ARCON | PAM. It is performed by
using the user’s biometric data (fingerprint). ARCON | PAM acts as a strategic entry and identity management
system for managing several system-based users. It supports leading biometric devices such as 3M Cogent,
Morpho, and Precision.
Perform the following steps to authenticate login using the Biometric fingerprint Validator:
Enter your credentials in the ARCON | PAM Login screen and click on the Login button.

## [p22]

www.arconnet.com|Copyright © 2025 22
2.
3.
Within a few seconds, the ARCON | PAM Biometric fingerprint Authenticator pop-up will be displayed
Place your finger on the Biometric device. The fingerprint will be traced on the Biometric – Finger
Print screen as shown below:

## [p23]

www.arconnet.com|Copyright © 2025 23
4.
5.
The fingerprint will be authenticated, and the user will be able to successfully log in to the ARCON |
PAM application.
If the traced fingerprint does not match, an error message will be displayed on the screen.
1.3.4.8 Voice Biometric
What is Voice Biometric?
Voice Biometric Authentication is a two-factor authentication method that employs web services to verify user
identities for Client Manager login. Voice biometrics is a convenient and secure method of authentication. It is
more difficult to forge a voiceprint than other biometric identifiers, such as fingerprints or facial scans.
Additionally, voice biometrics is a non-invasive method that does not require any physical contact. The pre-
configured web service authentication mechanism validates a user's voice and determines whether to grant
access.
1.3.4.9 Facial Recognition
What is Facial Recognition?
A facial recognition system is a technology capable of matching a human face from a digital image or a video
frame against a database of faces, typically employed to authenticate users through ID verification services,
and works by pinpointing and measuring facial features from a given image.
ARCON | PAM supports multi-factor authentication through Facial Recognition. This is performed by using the
webcam of the user's machine.

## [p24]

www.arconnet.com|Copyright © 2025 24
1.
2.
3.
4.
5.
Perform the following steps to authenticate login using Facial Recognition:
Enter your credentials in the ARCON | PAM Login screen and click on the Login button. The Facial
Recognition Validator pop-up will be displayed as below:
Within a few seconds, the ARCON | PAM Facial Recognition Registration pop-up will appear:
Place your face in front of the camera so that it can start scanning.
The facial data will be authenticated from the database and you will be able to successfully log in to the
ARCON | PAM application.
If the facial data does not match, the log-in attempt will be rejected.
1.3.4.10 FIDO2 Authenticator
1.3.4.10.1 What is FIDO2 Authenticator?
FIDO2 Authenticator is a modern, hardware-based authentication method that supports dual-factor
authentication without the need for traditional passwords. It allows users to securely access systems and

## [p25]

www.arconnet.com|Copyright © 2025 25
1.
2.
3.
services using a physical security key, such as a USB or biometric device, instead of remembering or entering
credentials.
1.3.4.10.1.1 ARCON | PAM FIDO2 - Self-Registration
Perform the following steps to authenticate login using the FIDO2 authentication method:
After logging in to any application, the self-registration screen will be displayed, where the user must
select the FIDO authentication from the drop-down list. Users will be prompted with FIDO2 multi-
factor authentication, and the screen below will be displayed.
Click the Security Key option.
The Add Your Security Key Screen is displayed. Click Continue.

## [p26]

www.arconnet.com|Copyright © 2025 26
4.
5.
After clicking Continue, the subsequent screen appears, displaying the security key.
This screen is asking you to verify your identity using a physical Security Key. To proceed, plug the key
into your device’s USB port (or use a cable), and if your key has a button or metallic sensor, tap it to
confirm.

## [p27]

www.arconnet.com|Copyright © 2025 27
6. The following screen is displayed, and enter a name for your Security Key. If you have multiple keys, you
can use the alias name to easily identify the correct one. Click "Continue" to save your changes.

## [p28]

www.arconnet.com|Copyright © 2025 28
7.
8.
This screen provides a recovery code, which you should save in a secure place. It acts as a backup to
access your account if you lose your device. Click Copy Code  to save it, then select Continue  to
complete the setup.
Upon successful authentication, the user is granted access to the application
1.3.5 Enforce Self Registration (ESR)
What is Enforce Self Registration?
Self-registration for the Dual Factor Authentication can be executed by the user only when the ESR is enabled
by the Administrator for a particular authentication. Enforce Self Registration (ESR) is a requirement within the
ARCON application that obligates users to register themselves in the system. This process is essential for
enabling dual-factor authentication, which adds an extra layer of security by requiring two forms of verification
for user access.
1.4 ARCON PAM Help and Learning Center
1.4.1 Overview
The ARCON PAM Help Center and Learning Center help you to find all the downloadable, user guides, system
requirement information, and a series of short videos to help you get a better grasp of the ARCON PAM
application. The ARCON PAM Help Center window appears when you click the downloadable icon on the
ARCON | PAM login screen. ARCON | PAM provides fast, easy-to-use applications that work seamlessly with
Ubuntu, Linux, MacOS, and Windows environments. Before you download, you can check if PAM supports your
operating system and if you have all the other system requirements.

## [p29]

www.arconnet.com|Copyright © 2025 29
The following table explains the fields displayed for the Windows environment:
Field Name Description
Download Application Icon
Arcon PAM Plugin ARCON PAM Plugin supports all major browsers:
Internet Explorer v10 & above, Mozilla Firefox V55 &
above, and Google Chrome V69 & above on Windows
for browser independency. To use the ARCON PAM
application on all browsers, you should install the
ARCON PAM Plugin on your system.
Thick Client Thick client is a form of client-server architecture. It is
a networked computer system where the majority of
the resources are deployed locally rather than being
spread across a network.
MultiTab PAM MultiTab is a desktop-based application that
enables you to access multiple PAM services in a
single window. Currently, MultiTab supports SSH and
RDP types of services.
Multiple service sessions are opened in a tabbed
manner, which makes it easier for you to toggle
between services and control all your sessions
centrally from a single window.
Connector Files (MultiTab) ARCON PAM connectors integrate native and third-
party applications. These connectors use a Single-
Sign-On (SSO) feature to connect to the remote
machines.

## [p30]

www.arconnet.com|Copyright © 2025 30
Field Name Description
TOTP Authenticator Time-based One-time Passwords (TOTP)
Authentication is a robust multi-factor authentication
type that adds a formidable layer of protection to
your account. It works on a simple premise where the
login tokens are formed by mixing a secret key with
the current time interval to generate the OTP. So, it is
necessary that the system times are
synchronized. The generated OTP is validated by the
server within the time frame. A successful validation
will give access to ARCON PAM.
Datawatch ARCON PAM Datawatch proves to be a unique
approach in enforcing measures that can restrict
threats emerging from database management
systems. It is a tool that is well capable of detecting
and reporting fraudulent, unauthorized, or other
unwanted activities with minimum disruption to user
operations and productivity. It is designed to smartly
monitor activities by selecting database transactions
and reporting any suspicious activity. This in turn
helps system administrators to take strict and
corrective actions against the reported activities and
make appropriate enhancements to protect sensitive
data.
System Requirement Icon
Windows 7/8/8.1/10 Make sure that you are using Windows 7/8/8.1/10
environments for the ARCON PAM product.
User Guide Icon
ARCON PAM Plugin This helps you to find the ARCON PAM Plugin
installation and configuration guide.
Thick Client This helps you to find the Thick Client installation and
configuration guide.
Video Learning Icon
ARCON Learning Center This helps you access the ARCON Learning Center
window. Refer to the ARCON Learning Center for more
information.
The following table explains the fields displayed for the Mac OS environment:

## [p31]

www.arconnet.com|Copyright © 2025 31
Field Name Description
Download Application Icon
MAC OS This helps you download the ARCON PAM MAC
package.
System Requirement Icon
OSX 10.11: EI Capitan, Mac OS 10.12: Sierra, Mac OS
10.13: High Sierra, and Mac OS 10.13: Mojave
Ensure that the ARCON PAM product is being used in
any one of these environments.
User Guide Icon
MAC OS This helps you to find the installation and
configuration guide for MAC.
The following table explains the fields displayed for the UNIX OS environment:
Field Name Description
Download Application Icon
ARCON PAM Ubuntu 16.04.03 LTS This helps you to download the ARCON PAM Ubuntu
16.04.03 LTS.
ARCON PAM Ubuntu 16.04 LTS This helps you to download the ARCON PAM Ubuntu
16.04 LTS.
ARCON PAM Ubuntu 20.04 LTS armh This helps you to download the ARCON PAM Ubuntu
20.04 LTS armh.
ARCON PAM Red Hat 7.5 This helps you to download the ARCON PAM Red Hat
7.5.
System Requirement Icon
Ubuntu 16.04.03 LTS, Ubuntu 18.04 LTS, Ubuntu
20.04 LTS armh, and Red Hat Enterprise Linux 7.5
Ensure that the ARCON PAM product is being used in
any one of these environments.
User Guide Icon
ARCON PAM Ubuntu This helps you to find the installation and
configuration guide for ARCON PAM Ubuntu.

## [p32]

www.arconnet.com|Copyright © 2025 32
Field Name Description
ARCON PAM Red Hat This helps you to find the installation and
configuration guide for ARCON PAM Red Hat.
The following table explains the fields displayed for the Browser Plugin environment:
Field Name Description
Download Application Icon
Browser Plugin The ARCON Browser Plugin is a browser-
independent extension available for all platforms that
provides a point solution for shielding all of the
classified secrets and confidential assets for your
organization in a single location.
With the Browser Plugin, users can automatically sign
in to a range of applications that are offered by
ARCON PAM without entering the credentials
manually or even remembering them each time they
access the applications directly from any browser
available on their desktop.
1.4.2 ARCON Learning Center
ARCON has created a series of short videos to help you get a better grasp of PAM functionalities. The Learning
Center window appears for users logging into ARCON | PAM for the first time. The ARCON Learning Center
offers video tutorials on various components, as shown on the screen below:

## [p33]

www.arconnet.com|Copyright © 2025 33
1.
2.
3.
 Perform the following steps to access the ARCON Learning Center:
Click the download icon on the PAM login screen:
When the ARCON | PAM Help Center appears, click on the Video Learning icon to launch the ARCON
Learning Center:
Once logged into the PAM application, you may access the Learning Center as shown on the screen
below:

## [p34]

www.arconnet.com|Copyright © 2025 34
•
•
1.5 Menu Bars
A graphical control element that has drop-down menus is known as a menu bar. The menu bar's function is to
provide a common container for window or application-specific menus that provide access to interacting with
the PAM application.
There are two main menus on the ACMO interface:
Top Menu
Side Menu.
1.5.1 Top Menu
The Top Menu consists of Navigation options on the top left and some icons on the top right side:
When users log in for the first time, the My Access  pop-up window appears as shown in the image
below. To watch more videos, click on the ARCON Learning Center.

## [p35]

www.arconnet.com|Copyright © 2025 35
1.5.2 Left Side - Header Menu Bar
Refer to the following table to understand the functionality of the headers on the top left side of the menu bar:
Headers Functionality
My Access This brings the user to the Homepage (My Services).
Manager This will display discrete applications offered by ARCON | PAM.
Users can view only those applications whose privileges are
assigned to them by Administrators.
Reports Access the diverse range of reports offered by ARCON | PAM.
Dashboard Access a high-level overview of what's going on in the application
through the dashboard.
About Access data about displays the version, release date, and the type of
server of ARCON | PAM.
1.5.3 Right Side - Icons
Refer to the following table to understand the functionality of icons on the top right side of the menu bar:
Icon Name Functionality
Figure1: (On the top left side)
Collapsed Menu When clicked, this expands the left pane of the ACMO
interface.
The Manager option in the top-header menu appears only
when an Administrator enables it in the Settings.

## [p36]

www.arconnet.com|Copyright © 2025 36
1.
2.
3.
4.
5.
Icon Name Functionality
Environment
Information
Displays the current version of ARCON | PAM. Set and
configured in Settings by an Administrator.
Language Lets users select the language of their choice from a
dropdown menu. Currently, ACMO supports English,
Japanese, Arabic, and French. It is set by default to
English.
Display Messages The Message Board is a source of communication of all
important security messages for users. Administrators
set the content and placement of the messages, which
can be seen by hovering over the Bulb icon.
Mailbox The Mailbox contains all incoming raised requests. All
messages received in your Mailbox are specifically
associated with and generated by ARCON | PAM.
Notifications Notifications are timely reminders for pending
activities in ARCON | PAM. Clicking on a notification
will redirect the user to the action page for that
particular request.
Profile The ARCON | PAM Profile icon displays the name of the
user signed in. Click on the profile name to perform the
following tasks:
To view session duration in the date-time format
of the current and previous session.
To change the password of the logged-in
account.
To log out from the application.
To clear the cache congregated in the plugin
folder.
To visit ARCON Learning Center, where users
can watch videos to understand and implement
the basic functionalities of PAM.
1.5.4 Side Menu
The Side Menu contains icons with different functionalities.
Icon Name Functionality
My Services This is the primary page of ACMO where an end user
can see services assigned to them and connect to
servers.

## [p37]

www.arconnet.com|Copyright © 2025 37
•
•
•
Icon Name Functionality
Preferences This helps the user to view the integrated third party
application’s exe path. User can also update the path of
the application. The user can view the last updated date
and delegate the approval authority to another user for
a particular amount of time.
Raise Request This is where an end user can raise a request for
elevation of privileges for access to additional
resources.
Pending Requests This allows the user to view pending requests.
Request Logs This allows the user to access logs that track
information of all requests raised in a particular time
frame.
My Activity The My Activity section allows users to view their
activity in the form of video logs.
1.5.5 Top Menu Bar
This is an index of the navigation headers (left side) on the Top Menu bar:
My Access / My Services (Homepage): This is the default page of the ACMO interface. It shows the list
of services assigned to the end user with which, they can connect to target servers and mark services as
favorites. It contains the following UI components:
My Services - Terminology
Filters
My Tags
Display Favourite Services
My Services Grid
Connecting to Target Machines
Session Extension
Manager: The Manager tab displays discrete applications offered by ARCON | PAM. Users can view only
these applications if the required privileges are assigned to them by Administrators.
Reports: Privileged Access Management (PAM) reports are crucial for security and compliance by
tracking user actions, monitoring access permissions, identifying risks, enforcing security policies, and
controlling privileged access effectively.
Report Builder Functionalities
How to Generate a Report?
Exported Reports

## [p38]

www.arconnet.com|Copyright © 2025 38
•
•
Dashboard Reports
Group Reports
LOB Reports
Logs Report
Performance Reports
Privilege Reports
Security Reports
Service Reports
User Reports
Vault Reports
Dashboard: The Dashboard centralizes important information for ARCON | PAM in the form of cards
and graphs.
About: The About section provides details about the ARCON | PAM Client Manager, which includes its
version, release date, and server description.
1.5.5.1 My Access
1.5.5.1.1 What is My Access?
The target service is a virtual non-physical machine where the user can perform the activities inside it by
accessing through the ACON PAM. This targeted service can be Windows RDP, MS SQL, SSH Linux, etc.
After logging in successfully to ARCON | PAM, the user will redirect to the My Services page and it will appear
as shown below:
All the mapped target services lists will appear on this page and by clicking on connect action button the user
will connect to the target services just in time by using a single sign-on.
The user can use the LOB, Service Type, IP Address/Host Name, and Tags filters to find the required target
service from the available list. Also, the user can mark the target service as a favorite and those will appear in
the My Favourite list to avoid the use of available filters.

## [p39]

www.arconnet.com|Copyright © 2025 39
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
1.5.5.1.2 Why is My Access Needed?
The My Services module streamlines how users discover, access, and manage target systems within the PAM
environment.
It simplifies privileged access management by:
Providing centralized access to all mapped services in one place
Enhancing efficiency with advanced filters and favorites
Reducing login complexity through single sign-on capabilities
Improving user experience with a clear, intuitive UI and structured service categorization
Supporting operational continuity through features like session extension
1.5.5.1.2.1 In this section of the guide, you will learn about the following UI components:
My Services - Terminology
Filters
My Tags
Display Favourite Services
My Services Grid
Connecting to Target Machines
Session Extension
1.5.5.1.3 My Services - Terminology
On the My Services page, the following symbols appear, helping to find and connect to target services more
quickly. See the table below to understand the symbol and what it means:
Symbol Description
By using this Quick Search option, the user can search for target services by entering the
information about them. When searching, all matching results are now displayed in the
scroll bar
This Tag symbol enables you to add services to an existing tag.
This Access Type symbol indicates the service type as Permanent. This type of service can
be accessed permanently by the user.
This Access Type symbol indicates the service type as Time-Based. This type of service can
be accessed only for a particular period by the user.
This Access Type symbol indicates the service type as one-time. This type of service can be
accessed only once by the user.
This symbol indicates the PAM service has been marked as a favorite. This type of service
will appear after clicking on My Favourite.

## [p40]

www.arconnet.com|Copyright © 2025 40
•
•
•
Symbol Description
This symbol indicates the PAM service is not marked as a favorite. The selected service is
not in the My Favorite list of the user. To add, the user can click on this symbol.
Connect
(default)
This symbol helps to connect the PAM services by using SSO. The user will connect just in
time without putting in any credentials. If this icon is showing in blue color, it means the
password of the PAM service matches the password that is stored in the vault.
Cannot Connect
If the connect symbol appears in red color, then it means password reconciliation has failed.
The password of the PAM server does not match the password stored in the vault. The user
can not connect to this type of service.
Can Connect
If the connect symbol appears in green color, then it means password reconciliation is done
successfully. The password of the PAM service matches the password stored in the vault.
Can Connect
If the connect symbol appears in gray, then it indicates that password reconciliation never
happened. By clicking on it, the user can connect to PAM services.
1.5.5.1.4 Filters
1.5.5.1.4.1 What are Filters?
Using keywords, field selections, functionality, and categories, filters let you narrow down long lists of choices
to just those that are pertinent. Quick commands can be used, for instance, to filter just specific text or
comments. Filters help to find the required PAM Service based on certain parameters. Users must select the
filter to search for sessions.
Three filters can be selected as shown following:
LOB: This filter is used to search the PAM services based on the assigned LOB name.
Service Type: This filter is used to search the PAM services based on the service type.
IP Address / Host Name: This filter is used to search the PAM services based on the IP address or
hostname.
Single sign-on (SSO) is a session and user authentication service that permits a
user to use one set of login credentials.

## [p41]

www.arconnet.com|Copyright © 2025 41
•
•
Also, the user can create tags to filter and search the group of PAM services. Refer to, My Tags  for more
information.
1.5.5.1.4.2 All Services
While selecting the All Services checkbox, the user will see all of the assigned PAM services from the assigned
LOB. If the user has filtered some sessions but suddenly wants to see all the services, then this checkbox can be
used.
1.5.5.1.5 My Tags
1.5.5.1.5.1 What are My Tags?
Using tags makes your service searchable, which is the first and most obvious advantage. You can locate your
service by looking up the tag or tags you used. It is beneficial if you are seeking service in a particular
department and are unsure of where to begin your search. Tags help to group some services for easy
identification and sorting. Users can create and assign tags to services at their discretion. The user can able to
sort through their list of services.
There are two ways to add services in the tag as below:
Addition of services while creating a new tag
Addition of tags to services by clicking the tag symbol in the available grid

## [p42]

www.arconnet.com|Copyright © 2025 42
1.
2.
3.
4.
1.
2.
1.5.5.1.5.2 How to create a Tag?
Perform the following steps to create a new tag:
Click on the :plus: icon.
Enter a name for the tag.
To create a nested tag, click the Nest under Tag checkbox and select the tag from the dropdown.
Click on Save.
1.5.5.1.5.3 How to Assign Tags to Services?
The user can add new tags to the PAM Services. Also, a new tag can be nested into the other existing tag.
Perform the following steps to assign tags to services:
Select the service from the My Services grid.
Click on the :t: icon.
The user can not nest the same tag under multiple existing tags.
The user can not nest the same tag under multiple existing tags.

## [p43]

www.arconnet.com|Copyright © 2025 43
3.
1.
2.
3.
Select the required tag. The service will be added to the tag.
1.5.5.1.6 Display Favourite Services
1.5.5.1.6.1 What is Favourtie Feature?
The admin can assign multiple PAM services to the user. From all PAM services if the user wants to find or filter
any particular service in the fastest way in future, then the user can mark those services as favourites by
clicking on the Star available in the grid. In a situation where you frequently use a few services, you can mark all
of the frequently used services on the ARCON PAM program as favourites. These services will be prominently
displayed in the service to facilitate easy access.
All those favourites marked PAM Services can be displayed after clicking on the  My Favourites  option as
shown on the below screen:
1.5.5.1.6.2 How to Mark Services as Favourites?
Perform the following steps to mark a service as your favourite:
Select the intended filters to display the PAM services.
Click on the star icon next to the service that you want to mark as your favourite.
Click on My Favourites to display the favourite services list, which will now include the marked service.
1.5.5.1.7 My Services Grid
1.5.5.1.7.1 What are Grids in My Services?
Grids can be used for a variety of tasks, including organizing and aligning your service list. They actually are
much more than just a few lines on a page; they organize, direct, and shape the service list display so that you
can get the intended outcome. On the My Services page, the user can see all the assigned PAM services below
the available filters in grid columns as shown in the below screen:

## [p44]

www.arconnet.com|Copyright © 2025 44
1.5.5.1.7.2 Columns Description
The columns show the description that can be customized by the admin in the global configuration.
See the following table for a description of grid columns:
Column Name Description
Service Type This column shows the type of services. It can be windows RDP, Linux root, SQL,
router device, or any web application, etc.
Host Name This column shows the hostname of the PAM service.
Host IP This column shows the IP of the host PAM service.
Username This column shows the username of that PAM service.
Domain This column shows the domain name of that PAM services.
Instance This column shows the instance of the services.
Server Type This column shows the name of the tag if the service is added to any tag.
Description 1
Description 2
Description 3
This description column shows the information about the service which was
mentioned while creating it.
•
Users can see the columns that are not ticked/selected by the Administrator as the following
configuration in Settings.
Hide ACMO My Services Page Table Column (Case-sensitive)
This column names can be changed by admin in global configuration.

## [p45]

www.arconnet.com|Copyright © 2025 45
1.
2.
3.
Column Name Description
Symbol In Grid In grid, there are four symbols are available to tag the service, access type
identification, favourite mark and connect. Refer the My Services - Terminology for
more information.
1.5.5.1.8 Connecting to Target Machines
1.5.5.1.8.1 What is Connecting to Target Services/Machines?
To connect the target services or machines which has been assigned by the admin, the user can navigate to the
My Services page. By using filters, tags, quick search or my favourite list users can find the required service or
machine. ARCON PAM uses a Single Sign-On authentication process while connecting to the target services or
machine because it enables user to authenticate and connect using just one set of credentials.
Before clicking on connect icon check its color. The connection icon for all services appears in blue unless the
Service Health Status  configuration is enabled in the global configuration. In that case, the following
connection icons appear:
Connection Icon Color Description
Red Single Sign-on is not possible because the password is not matched with the
password which is saved in vault or have not reconciled yet.
Green Single Sign-on is possible and the password is reconciled or the password is
matched with the password which is saved in vault.
Grey Single Sign-on is possible but password reconciliation never happened.
1.5.5.1.8.2 How to connect the target Services/ Machine?
Perform the following steps to connect to the target machine:
Navigate to My Services page.
Select the intended Filters to display the services in the grid.
Click on the connection icon to initiate Single Sign-on.

## [p46]

www.arconnet.com|Copyright © 2025 46
1.
a.
b.
2.
3.
4.
5.
6.
•
•
•
•
1.5.5.1.9 Session Extension
1.5.5.1.9.1 What is Session Extension?
Consider a scenario in which the user has access to the target server on a time-based / one-time basis. The user
is currently connected to the target server and their connection is due to end in a few minutes. If the user has
not finished their task and wants to continue their current session, they can request an extension.
1.5.5.1.9.2 How to Request a Session Extension?
Perform the following steps to request a session extension:
Once the session duration expires, a dialog box appears on the screen with two options:
Extend Session
Terminate Session
Click on the Extend Session button.
Enter a brief note to the approver explaining the purpose of the extension request.
Enter the time period for which the extension is required in hours and minutes.
Click on Raise Request.
The request will be sent to the approvers defined in the workflow.
1.5.5.2 Manager
1.5.5.2.1 What is Manager Tab?
The Manager tab in ARCON | PAM serves as a centralized hub for users to access various applications. This
streamlined single-page interface enhances user experience by providing easy navigation. Access to these
applications is controlled by permissions set by Administrators, ensuring that users only view and utilize the
tools they are authorized for, which helps maintain security and compliance This streamlined approach
enhances usability while maintaining security and control over sensitive resources.
1.5.5.2.2 Why is Manager Tab Needed?
Simplifying navigation through a unified interface for accessing various applications
Improving user productivity by consolidating tools in one accessible location
Enforcing security and compliance through role-based access controls
Reducing interface clutter and preventing unauthorized access to sensitive resources
•
•
The user receives an alert notification before the service expires. For alert notifications, an
Administrator must enable the Time Control configuration in Settings.
Once the session duration has expired, the session will terminate automatically. For auto-
termination of a session, the Administrator must define the time set (in minutes) in Settings.
•
Users can see this tab only if they have the following permission(s):
Manager Menu Display

## [p47]

www.arconnet.com|Copyright © 2025 47
1.
2.
1.5.5.2.3 Script Manager
1.5.5.2.3.1 What is Script Manager?
The Script Manager  helps the user to run a script and monitor multiple servers simultaneously. After an end
user creates the scripts in Script Manager, PAM retrieves the credentials stored in the Vault using API,
connects to the end target device using the credentials, and executes the script.
A Script Manager user must be assigned appropriate privileges such as the rights to create a new script, edit an
existing script, and run the script through ARCON | PAM on the required destination database server. The
scripts can be configured to run sequentially and thereby perform pre- and post-task actions for any
automation job. A Robotic Process Automation framework can be used to run bots on end devices. The user can
also schedule scripts to be executed at a specified time.
1.5.5.2.3.2 How to Launch the Script Manager?
Follow these steps to launch the script manager:
Click on the Manager tab.
When the My Apps page opens, click on the Script Manager icon.
•
•
A Script Manager user must have the following privileges:
Create New Script privilege to add new script.
Edit Script privilege to edit an existing script.
Run Script privilege to run a script.
Particular Service Type should also be assigned to the user.

## [p48]

www.arconnet.com|Copyright © 2025 48
3.
1.
ARCON | PAM Script Manager opens in a new window. There are two tabs in this window: Auto Script
Runner and Script Manager Log.
1.5.5.2.3.3 How to Run the Scanner?
Perform the following steps to run the scanner:
Select the LOB/Profile and Service Type from the drop-down list. All the servers for the selected service
type will be listed on the left-hand side pane.

## [p49]

www.arconnet.com|Copyright © 2025 49
2.
3.
1.
Right-click the server and choose Add Servers to Script Manager’s Queue. The selected servers will be
added to the top middle pane with the status displayed as Added to Queue.
To remove the server from the queue, right-click and choose Remove Server to Script Manager’s
Queue in the server queue list.
1.5.5.2.3.4 How to Add a Script?
Follow these steps to add a script:
Follow the below steps to add a script to the selected server:
On the bottom middle pane, click on the Add New Script :addscript: icon to add a new script:
•
•
•
The range of server status in the Queue is as follows:
Added to Queue: This indicates that the server is successfully added to the queue.
Running Script: This indicates that the script is running on the server.
Success: This indicates that the script is executed successfully on the server.

## [p50]

www.arconnet.com|Copyright © 2025 50
2.
3.
4.
5.
6.
7.
The edit Script window will open. Enter the name of the script in the Script Name field.
In the editor space, enter or copy-paste the script to run it on the selected server.
Click on the Save & Close button to add the script on the left bottom pane or click Cancel to revoke it.
Select the script from the left bottom pane and select the check box from the options on the top right of
this window.
Click the Run Script button to execute the script on selected servers. The details of the executed script
will be displayed on the right pane.
Click the Save As button to save the log to a local drive.
Users can view only those scripts which are created by themselves.
•
•
•
•
The following check boxes will be displayed:
Show Logs in Single Window: This check box is selected by default. By default, all the output of
the servers will be displayed in a single window. If this checkbox is de-selected, the output of
different servers will be displayed in different tabs.
Include Column Headers in Log: Select this checkbox to include column headers in the log.
Include Script in Log: Select this checkbox to include the script in the log.
Save Logs Locally: Select this check box to save the logs on a local drive.

## [p51]

www.arconnet.com|Copyright © 2025 51
1.
2.
3.
1.5.5.2.3.5 How to Edit a Script?
Follow the below steps to edit the script in the selected server:
On the middle bottom pane, click the Edit Script icon to edit an existing script. The edit Script window
will open.
In the editor space, make changes to the script to run on the selected server.
Click Save & Close to save the changes to the script or click Cancel to revoke it.

## [p52]

www.arconnet.com|Copyright © 2025 52
1.
2.
1.5.5.2.3.6 How to Delete a Script?
Follow the below steps to edit the script in the selected server:
On the middle bottom pane, click the Delete Script icon.
A popup stating Script Deleted Successfully is displayed as shown below:
1.5.5.2.3.7 How to view Version History?
Script Version History will show the version history of a specific script run on the selected server.
Follow the steps below to view the version history of a script:
•
•
The script name cannot be changed while editing the script.
The edited version of the script would appear as V1, V2, V3, etc. under the original script name.
Please be sure to choose the correct version of the script as, by default, the original script will
be run.

## [p53]

www.arconnet.com|Copyright © 2025 53
1.
2.
1.
On the bottom center pane, click the Show Version History :version_history: icon to view details of an
existing script.
The Script Version History window will open. It will display details such as Script Name, Script Version,
Created/Modified By, and Created/Modified On.
1.5.5.2.3.8 How to View the Script Manager Log?
The Script Manager Log tab will display the script log executed by a user on the Script Manager.
Follow the steps below to view the details of the log:
Select the service type. A list of all the scripts run for the selected service type will be displayed with the
fields Log Id, Script Executed By, and Script Executed On (Date and Time).

## [p54]

www.arconnet.com|Copyright © 2025 54
2. To view the details of the logged data, double-click on the specific row. The Script Manager Logged Data
Viewer window will open. This window will give a detailed description of the script on the selected
servers.

## [p55]

www.arconnet.com|Copyright © 2025 55
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
1.5.5.2.4 Approval Request
Users are obliged to have approval from Administrators to perform certain activities. This is where all the
requests are accumulated for approvals.
Requests can be Approved/Rejected for the following:
Service Access
Service Password
Ticket
Critical Command
Service Transactions
User Transactions
User Group and Service Group
Video Log
Split Password
1.5.5.2.4.1 Service Access
What is Service Access Request Workflow?
When a user requests access to a service, the request is submitted to the Administrators designated in the User
Request Approval Workflow in approval settings. These approvers can review, approve, reject, revoke, or
forward the requests.
If the request is Approved by the first approver, it goes to higher-level approvers as configured in the
workflow. Service Access is granted only when the last approver approves the request.
If the request is Rejected by the first approver, it does not go to higher approvers.
The request can be Forwarded only if ad-hoc approvers are set in the User Request Approval Workflow
in Settings. The action performed by that Administrator is the final one. It will not be sent to higher-ups
for approval.
The request can be Revoked in the service access request once it is approved.
How to Change Request Access Type?

## [p56]

www.arconnet.com|Copyright © 2025 56
1.
2.
Approvers can also change the request's access type. For example, if a user submits a permanent service access
request but the approver determines that it is a one-time labor request after reading the description, they can
change the request from permanent to one-time and approve it. Higher-level approvers can see all the request
changes made by approvers on their approval page.
How to Approve a Request?
Follow these steps to approve a request:
Navigate to the Manager → Approval Requests → Service Access.
Select Service Access. The Approvals - Service Access Request screen will appear.
Refer to the following table to understand the data displayed in each column:
Column Description
Transaction ID A unique ID assigned to the particular service access
request.
Requested By The name of the user who raised the service access
request.
Requested On Date/time at which the request was raised.
You may use the Check/Uncheck All button to bulk Approve or Reject all service access requests.

## [p57]

www.arconnet.com|Copyright © 2025 57
•
•
•
•
•
Description Text entered by the user to give a summary of the
request to the approver.
Access Type Displays the type of access requested:
Permanent
Time-Based
One-Time
Service The server for which the request has been raised
Current Status The current approval level of the request.
Pending With The name of the approver with whom the approval is
pending.
View Request Details of the request (click to view).
Requestor Details
Requestor The name of the user who raised the request.
Reference Type
** Customized field
Reference type of the request, if entered by the user
while raising the request.
Reference Details
** Customized field
Reference details of the request, if entered by the user
while raising the request.
Service Details
Service Type The server type for which the request has been raised
Requested Service Displays the services for which the request has been
raised.
Select the services that you want to Approve/
Reject.
The services that are not selected will remain on
the pending approval list.
Command Profile Select the Command Profile to restrict commands.
The active profiles for the selected Service type will be
displayed in the drop-down list.
Comments Enter any comments.

## [p58]

www.arconnet.com|Copyright © 2025 58
•
•
•
View Command Click this link to view commands configured for the
selected command profile.
Configuration Commands The configuration commands are selected by the User
while raising the request.
Description Summary of the request entered by the user.
Access Details
Access Type The type of access requested by the user.
Permanent
Time-Based
One-Time
Access Duration The dates between which the user requires server access.
Session Duration The period during which the user requires access to the
server is between the dates provided in the access
duration.

## [p59]

www.arconnet.com|Copyright © 2025 59
1.
View Request Changed at Levels The level-wise change of the request by the approver.
Change Request To change the access type of the request. The drop-down
displays the remaining access types to which it can be
changed.
Per Session Duration The amount of time in hours and minutes a user can
access the service in a session.
Description Enter the description for the change in the request.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the administrator before
approving, rejecting, or forwarding the request.
Bulk Access Approval
This section allows approvers to apply Command Profiles when performing bulk approvals of Service Access
Requests. To enable the use of Command Profiles, approvers must first select a Service Type before approving
multiple requests.
Follow these steps for bulk approval:
Select the service type from the Service Type dropdown.

## [p60]

www.arconnet.com|Copyright © 2025 60
2.
3.
4.
5.
1.
Select multiple services and click Approve as illustrated below.
The Bulk Approve Request screen is displayed.
Select the command profile from the dropdown list.
Enter the approval comment in the field and click Submit.
Approval of Services Access Requests
If no Service Type is selected, all available services will be displayed. When multiple services are selected
and the "Approve" button is clicked, the "Command Profile" option will not be shown. This is because the
selection may include third-party services that do not support Command Profiles, or a mix of service
types (e.g., Windows, SSH), making it incompatible with a single Command Profile selection.
Only the Command Profiles relevant to the selected Service Type will appear in the Command Profile
dropdown.

## [p61]

www.arconnet.com|Copyright © 2025 61
2.
3.
1.
2.
The Bulk Approve Request screen is displayed.
Enter the approval comment in the field and click Submit.
Rejection of Services Access Requests
Follow these steps to reject the service access request:
Check box the single or multiple services as illustrated below and click Reject.
The Rejection Reason screen is displayed.

## [p62]

www.arconnet.com|Copyright © 2025 62
3.
•
•
1.
2.
Enter a valid reason to reject the service access request and click Submit.
1.5.5.2.4.2 Service Password
What is Password Access Request Workflow?
When a user requests a password for any service from ACMO, the request is submitted to the Administrators
designated in the User Request Approval Workflow in approval settings. These approvers can go over the
requests and approve or reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow. The
password of the service can be viewed only when the last approver approves the request. Once the
password is viewed, it remains an Open Password until the password of that service has changed.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
Follow the steps below to approve a Service Password Request:
Navigate to the Manager → Approval Requests → Service Password.
Select Service Password. The Approvals - Service Password Request screen will appear.

## [p63]

www.arconnet.com|Copyright © 2025 63
Refer to the following table to understand the data displayed under each column:
Fields Description
Request ID Unique ID associated with each password request.
Transaction ID A unique ID associated with each transaction.
Requested By The name of the user who raised the service password
request.
Requested On Date/time at which the request was raised.
Description Text entered by the user to give a summary of the
request to the approver.
Requested Till Date/time till which the user should be able to see the
password of that service.
Service The server for which the request has been raised.
Current Status The current approval level of the request.
Is View Now Shows whether the “view now” checkbox was selected by
the user at the time of raising the request.
Requestor Details
Requestor The name of the user who raised the request.
Service Details
Service Type The server type for which the request has been raised.

## [p64]

www.arconnet.com|Copyright © 2025 64
•
•
4.
Requested Service Displays the services for which the request has been
raised.
Select the services that you want to Approve/
Reject.
The services that are not selected will remain on
the pending approval list.
Description Summary of the request entered by the user.
Access Details
View On Date/time from which the user can view the password of
the service.
To Be Accessed Till Date/time till which the user can view the password of
the service.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request.
Click on View Request.

## [p65]

www.arconnet.com|Copyright © 2025 65
1.
Rejection of Service Password Requests
Follow these steps to reject the service password request:
Check box the single or multiple services as illustrated below and click Reject.

## [p66]

www.arconnet.com|Copyright © 2025 66
2.
3.
•
•
1.
The Rejection Reason screen is displayed.
Enter a valid reason to reject the service access request and click Submit.
1.5.5.2.4.3 Ticket Requests
What is the Ticket-Based Access Request Workflow?
When a user raises a ticket request from ACMO, the request is submitted to the Administrators designated in
the User Request Approval Workflow in approval settings. These approvers can go over the requests and
approve or reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow. The
user needs to enter the ticket number to access that service.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
Follow these steps to approve a ticket request:
Navigate to the Manager → Approval Requests → Ticket.

## [p67]

www.arconnet.com|Copyright © 2025 67
2.
•
•
Select Ticket. The Approvals - Ticket Request screen will appear.
Refer to the following table to understand the data displayed under each column:
Fields Description
Ticket Number A unique ticket number associated with the ticket.
Service Group The name of the service group to which the service
belongs.
Service The name of the service for which the request is raised.
Ticket Type The ticket type of the request:
PE - Planned Event: Any periodical process of
raising a ticket or pre-planned cyclic procedure for
ticket raising.
CR - Change Request: Any request raised to make
any change in the service.

## [p68]

www.arconnet.com|Copyright © 2025 68
•
•
•
•
Activity Type The following activity types are available:
SA - Service Affecting: The proposed activity
affects the service as a whole.
NSA - Non-Service Affecting: The proposed
activity will have no effect on/make changes to the
service.
Requested By The name of the user who raised the ticket.
Executor The user who uses the ticket to access the service.
Start Time Date/time from which the ticket is valid.
End Time Date/time till which the ticket is valid.
Current Status The current approval level of the request.
Pending With The name of the approver with whom the approval is
pending.
View Details Details of the request (click to view).
Requestor Details
Requestor The name of the user who raised the request.
Executor The user who uses the ticket to access the service.
Service Details
LOB Name of the LOB to which the server belongs
Service Group Name of the service group to which the target server
belongs.
Service/ IP Address The IP address of the target server.
Ticket Details
Ticket Number A unique ticket number associated with the ticket.
Ticket Type The ticket type of the request.
PE - Planned Event
CR - Change Request
Users are populated based on the selected
service assigned to them.

## [p69]

www.arconnet.com|Copyright © 2025 69
•
•
•
•
•
•
•
•
1.
Activity Type The activity type:
SA (Service Affecting)
NSA (Non Service Affecting)
Description Summary of the request entered by the user.
Start Time Date/time from which the ticket is valid.
End Time Date/time till which the ticket is valid.
Expected Duration Time period to access the service.
Location Location of service.
Impact The impact this ticket has:
Low
Medium
High
Critical
Impact Location Impact location of the ticket.
Attachment 1 Attachment(s) attached by user.
Attachment 2 Attachment(s) attached by user.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the administrator before approving
or rejecting the request.
1.5.5.2.4.4 Critical Commands
ARCON | PAM provides Administrators with the capability to specifically define the commands that require
approval from approvers before execution. These commands are defined as critical with approval (CWA). This
implies that commands will run only when the approvers specified in the User Request Approval Workflow in
Settings have given their approval.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
Follow these steps to approve a request:
Navigate to the Manager → Approval Requests → Critical Commands.

## [p70]

www.arconnet.com|Copyright © 2025 70
2. Select Critical Command. The Approvals - Critical Command screen will appear.
Refer to the following table to understand the data displayed under each column:
Column Name Description
Transaction ID A unique ID associated with each transaction.
Requested By The name of the user who wants to fire the critical
command.
Requested On Date/time at which the command was typed.
Command The command that the user wants to fire.
Description Text entered by the user to give a summary of the
request to the approver.
Session ID Unique Session ID associated with each session.
Current Status Present status of the request.
View Request Details of the request (click to view).
Requestor Details
Requestor The name of the user who raised the request.

## [p71]

www.arconnet.com|Copyright © 2025 71
4.
5.
•
•
Command Details
Requested Command The command that the user wants to fire.
Description Description of the command.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request.
Click View Details. The following Approve - Critical Command Request screen will be displayed:
Enter comments and click the Approve button to approve the request or the Reject button to reject the
request.
1.5.5.2.4.5 Service Transactions
What is Service Transactions Approval Workflow?
Administrators who have the required privileges can create, modify, or delete a service in ARCON | PAM. To
keep an eye on this process, Administrators can create and set higher-level approvers who can monitor any
service transactions in the ARCOS Workflow Approval Matrix in Settings. These approvers can go over the
requests and approve or reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow.
If the first approver rejects the request, it does not go to higher approvers.

## [p72]

www.arconnet.com|Copyright © 2025 72
1.
2.
•
•
•
How to Approve a Request?
To approve the Service Transaction Request, follow the steps below:
Navigate to the Manager → Approval Requests → Service Transactions.
Select Service Transaction. The Approvals - Service Transaction screen will appear.
Refer to the following table to understand the data displayed under each column:
Column Name Description
Transaction ID A unique ID associated with each transaction.
Operation Action performed at service level:
Create - Creation of service
Modify - Modification of service
Delete - Deletion of service
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the target server IP.
Current Level The current approval level of the request.

## [p73]

www.arconnet.com|Copyright © 2025 73
•
•
•
4.
Last Level The last approval level of the request.
View Request Details of the request (click to view).
Transaction Details
Transaction By Name of the Administrator performing the operation.
Object type Set to Service Transaction by default.
Operation Type Name of the operation performed at service level:
Create - Creation of service
Modify - Modification of service
Delete - Deletion of service
Transaction Details Details of the transaction.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request.
Click View Request.

## [p74]

www.arconnet.com|Copyright © 2025 74
5.
•
•
1.
Click the Approve button to approve the request or the Reject button to reject the request.
1.5.5.2.4.6 User Transactions
What is the User Management Approval Workflow?
ARCON | PAM provides Administrators with the capability to create, modify, or delete users. To keep an eye on
this process, Administrators can create and set higher-level approvers who can monitor any user transactions
in the ARCOS Workflow Approval Matrix in Settings. These approvers can go over the requests and approve or
reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
Follow the steps below to approve a User Transactional Request:
Navigate to the Manager → Approval Requests → User Transactions.

## [p75]

www.arconnet.com|Copyright © 2025 75
2.
•
•
•
Select User Transactions. The Approvals - User Transactions screen will appear.
Refer to the following table to understand the data displayed under each column:
Column Name Description
Transaction ID A unique ID associated with each transaction.
Operation Action performed at user level:
Create - Creation of user.
Modify - Modification of user.
Delete - Deletion of user.
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the activity performed by the user.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
View Request Details of the request (click to view).

## [p76]

www.arconnet.com|Copyright © 2025 76
•
•
•
4.
5.
Transaction Details
Transaction By Name of the Administrator performing the operation.
Object type Set to Service Transaction by default.
Operation Type Name of the operation performed at service level
Create - Creation of user.
Modify - Modification of user.
Delete - Deletion of user.
Transaction Details Details of the transaction.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request.
Click View Request.
Click the Approve button to approve the request or the Reject button to reject the request.

## [p77]

www.arconnet.com|Copyright © 2025 77
•
•
1.
2.
1.5.5.2.4.7 User Groups & Service Groups
What is the User Group & Server Group Assignment Workflow?
Administrators who have the required privileges can assign or remove user groups to/from the server groups.
To keep an eye on this process, Administrators can create and set higher-level approvers who can monitor any
user group-server group transactions in the ARCOS Workflow Approval Matrix in Settings. These approvers
can go over the requests and approve or reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
To approve the User Group-Service Group Transaction Request, follow the steps below:
Navigate to the Manager → Approval Requests → User Groups And Service Groups.
Select User Group and Service Group Transactions. The Approvals - User Group and Service Group
Transactions screen will appear.
Refer to the following table to understand the data displayed under each column:
Column Name Description
Transaction ID A unique ID associated with each transaction.

## [p78]

www.arconnet.com|Copyright © 2025 78
•
•
•
•
4.
Operation Action performed at the user level:
Assigned - Assign server group to user group.
Revoked - Revoke server group from the user
group.
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the activity performed by the user.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
View Request Details of the request (click to view).
Transaction Details
Transaction By Name of the Administrator performing the operation.
Object type Set to Transaction between User Group and Server
Group by default.
Operation Type Name of the operation performed at service level:
Assigned - Assign server group to user group
Revoked - Revoke server group from the user
group
Transaction Details Details of the transaction.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request
Click View Request.

## [p79]

www.arconnet.com|Copyright © 2025 79
5.
•
•
1.
Click the Approve button to approve the request or the Reject button to reject the request.
1.5.5.2.4.8 Video Logs
What is the Video Log Access Approval Workflow?
Video logs are important for security purposes. Therefore, access to them is controlled and secured in ARCON |
PAM. Administrators can create and set higher-level approvers who can approve requests to view video logs in
the ARCOS Workflow Approval Matrix in Settings. These approvers can go over the requests and approve or
reject them.
If the first approver approves the request, it goes to higher-level approvers as set in the workflow.
If the first approver rejects the request, it does not go to higher approvers.
How to Approve a Request?
To approve the Video Log View Approval, follow the steps below:
Navigate to the Manager → Approval Requests → Video Logs.

## [p80]

www.arconnet.com|Copyright © 2025 80
2.
•
Select Video Log. The Video Log View Approval screen will appear.
Refer to the following table to understand the data displayed under each column:
Column Name Description
Log ID A unique ID with the log.
Transaction ID A unique ID is associated with each transaction.
From Date and Time Date/time from which logs are captured.
To Date and Time Date/time till which the logs are captured.
Object Type Set by default to video log.
Operation Type Action performed:
View - To view the video logs
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the activity performed by the user.
Current Level The current approval level of the request.
Last Level The last approval level of the request.

## [p81]

www.arconnet.com|Copyright © 2025 81
•
•
•
4.
View Request Details of the request (click to view).
Transaction Details
Transaction By Name of the Administrator who wants to view the video
log.
Object type Set by default to video log.
Operation Type Name of the operation performed:
View - To view the video logs
Transaction Details Details of the transaction
Approval Details
Log ID A unique ID with a log.
From Date and Time Date/time from which the users want to access logs.
To Date and Time Date/time until which the users want to access logs.
Description Summary of the request explaining the purpose of the
request to the approver.
Options Request by the user:
Show Details - View the video log.
Export to Word - Allow exporting the video log in
Word format.
Approval Details
Current Approval Level The present level of approval.
Last Approval Level The last level of approval.
Comments Text to be entered by the Administrator before
approving or rejecting the request.
Click View Request.

## [p82]

www.arconnet.com|Copyright © 2025 82
1.
2.
5. Click the Approve button to approve the request or the Reject button to reject the request.
1.5.5.2.4.9 Split Password
What is the Service Password Split Request?
By splitting a password between two people, the Service Password Split Request increases the security of
privileged accounts. Only when both Administrators submit their halves of the passwords can the service be
created/modified. The first owner initiates the transaction by entering their portion of the password and
designating the second owner as the transaction's finisher. The second owner will then receive an ACMO
notification and will be able to finish the transaction started by the first owner.
How to Approve a Request?
To create a new service, follow the steps below:
Navigate to the Manager → Approval Requests → Split Password.
Select the Split Password option. The Service Split Passwords Requests screen will appear.

## [p83]

www.arconnet.com|Copyright © 2025 83
•
•
Refer to the following table to understand the data displayed under each column:
Column Name Description
Service Type The name of the service type.
Host Name The host name of the target server.
Host IP The host IP of the target server.
Username The username of the target server.
Domain The domain name of the target server.
Other Owned The name of the second owner who will enter the second
half and create/modify the target server.
Transaction Type Activity performed:
Created - To create the service with split
password.
Modified - To modify the service with split
password.
Transaction By Displays the name of the first Administrator by whom the
transaction was initiated.
Transaction On Date/time at which the transaction was initiated by the
first Administrator.
Vaulted On Date/time at which the transaction was completed by
second Administrator.

## [p84]

www.arconnet.com|Copyright © 2025 84
•
•
4.
Column Name Description
Status Final status of the request:
Pending - The second half of the password is still
remaining.
Vaulted - The second half of the password is
entered and transaction is complete
Click on the
  icon. Enter the other half of the password and vault the service. The password for the
service will now be vaulted.
1.5.5.2.5 Approval Logs
Approval logs track information of all approved requests. Logs are generated based on filters selected by
Administrators.
1.5.5.2.5.1 Service Access Approval Logs
What is Service Access Request and Approval Logs?
If the user wants to access the target service which has not been assigned, the user can raise the service access
request. Refer to, Service Access Request. Once that raised request got approved by the admin, the user can
see the requested target service in my services list.
How to view Service Access Approval Logs?
The user can see all these service access approval logs at the following path: Manager > Approval Logs >
Service Access.
The Approval Logs - Service Access screen will display as shown below:

## [p85]

www.arconnet.com|Copyright © 2025 85
1.
2.
•
•
•
Proceed with the below steps to view Service Access Approval Logs:
Navigate to, Manage > Approval Logs > Service Access.
Select Date From and Date To and click on GO! button. Logs of details associated with the request will
be displayed.
Refer to the following table to understand the data displayed under each column:
Field Name Description
Requested By The name of the user who had raised the service access request.
LOB Name of the LOB from which the request was raised.
Requested On Date/time of the raised service access request
Request Access Type Type of request
Permanent
Time-Based
One-time
Service Type The type of the target service for which the request has been raised.
Service Host The host name of the target server for which the request has been raised.
Service Username The user name assigned to the service.

## [p86]

www.arconnet.com|Copyright © 2025 86
•
•
•
3.
4.
Field Name Description
Final Status The status of the request:
Approved
Rejected
Pending
Approved By The name of the user who approved the request.
View Details Details of the request (click to view).
Revoke The requested target service access can be revoked by clicking on this option.
Click on Details.
The following screen will display:

## [p87]

www.arconnet.com|Copyright © 2025 87
•
•
•
Refer to the following table to understand the data displayed under each row:
Field Name Description
LOB Profile The LOB/Profile name of the request.
Requested By The name of the user who raised the request.
Requested On Date/time of the raised service access request.
Requested Description Text entered as a brief summary by the user while raising the request.
Requested Access Type Type of request raised by the user:
Permanent
Time-Based
One-time
Service Type The name of the service type.
Service IP Address The IP address of the target server.
Domain Name The domain name of the target server.
Service User Name Username of the service.
DB Instance Displays DB Instance of service.
Access Required From
Date
Date/time from which the request is required.
Access Required To Date Date/time until which the request is valid.

## [p88]

www.arconnet.com|Copyright © 2025 88
•
•
•
•
•
•
Field Name Description
Access Duration Time The dates between which the user requires server access.
Access Period The period of time during which the user requires access to the server between
the dates provided in the access duration.
Current Approval Level The current approval level.
Approval Levels The total number of approval levels configured in workflow.
Approver 1 User Name Username of the first approver.
Approver 1 Status Status of the request by first approver:
Approved
Rejected
Approver 1 Status On Date/time at which the request was approved/rejected by first approver.
Approver 1 Comment Remarks entered by approver 1
Approver 1 Email ID Email ID associated with approver 1
Approver 2 User Name Username of the second approver.
Approver 2 Status Status of the request by second approver:
Approved
Rejected
Approver 2 Status On Date/time at which the request was approved/rejected by second approver.
Approver 2 Comment Remarks entered by approver 2
Approver 2 Email ID Email ID associated with approver 2
Approver 3 User Name Username of the third approver.
Approver 3 Status Status of the request by third approver:
Approved
Rejected
Approver 3 Status On Date/time at which the request was approved/rejected by third approver.
Approver 3 Comment Remarks entered by approver 3
Approver 3 Email ID Email ID associated with approver 3
Approver 4 User Name Username of the fourth approver.

## [p89]

www.arconnet.com|Copyright © 2025 89
•
•
•
•
•
•
•
•
4.
Field Name Description
Approver 4 Status Status of the request by fourth approver:
Approved
Rejected
Approver 4 Status On Date/time at which the request was approved/rejected by fourth approver.
Approver 4 Comment Remarks entered by approver 4
Approver 4 Email ID Email ID associated with approver 4
Approver 5 User Name Username of the fifth approver.
Approver 5 Status Status of the request by fifth approver:
Approved
Rejected
Approver 5 Status On Date/time at which the request was approved/rejected by fifth approver.
Approver 5 Comment Remarks entered by approver 5
Approver 5 Email ID Email ID associated with approver 5
Final status Final degree of the request:
Approved
Rejected
Command Profile The command profile selected by approver while approving or rejecting the
request.
Final Status The final status of service access request:
Approved
Rejected
Click on OK to close the pop-up window.
1.5.5.2.5.2 Service Password Approval Logs
What is Service Access Request and Approval Logs?
In case of password requirement of any target services, the user can raise the password request. Once it is
approved by the admin, the user will get an email where that password can be displayed or copied.
How to generate Service Access Request and Approval Logs?
The generated approval logs can be displayed on the following path: Manager > Approval Logs > Service
Password.

## [p90]

www.arconnet.com|Copyright © 2025 90
1.
2.
3.
•
•
•
To generate the approval logs, proceed with the following steps:
Navigate to, Manager > Approval Logs > Service Password.
Select Date From and Date To.
Click on Go!. Log details associated with the request are displayed in tabular format.
Refer to the following table to understand the data displayed under each column:
Field Name Description
Request ID Unique ID associated with each password request.
Transaction ID A unique ID associated with each transaction.
Requested By The name of the user who raised the service password
request.
Requested On Date/time at which the request was raised.
Description Text entered by the user to give a summary of the
request to the approver.
Requested Till Date/time till which the user should should be able to see
the password of that service.
Service The server for which the request has been raised.
Final Status Displays the status of the request:
Approved
Rejected
Pending
Is View Now Whether the “view now” checkbox was selected by the
user at the time of raising the request.

## [p91]

www.arconnet.com|Copyright © 2025 91
1.
2.
3.
•
•
•
•
•
•
•
Field Name Description
Close To close the open password.
1.5.5.2.5.3 Ticket Approval Logs
Ticket Approval Logs display approval details of ticket requests raised by users.
How to view Ticket Approval Logs?
Follow the steps below to view Ticket Approval Logs:
Click on :w: Approval Logs.
Click on Ticket. Approval Logs -A ticket page will appear.
Logs of details associated with the request are displayed.
Refer to the following table to understand the data displayed under each column:
Fields Description
Ticket Number A unique ticket number associated with the ticket.
LOB The LOB/Profile name from which the request was
raised.
Ticket Status Ticket status of the request:
Initiated - Initial status of the Tickets.
Approval Pending - Tickets pending for approval.
Approved - Tickets approved by approver.
Rejected - Tickets rejected by approver.
Postponed - Tickets postponed by approver.
Completed - The ticket approval process is
completed by the approver.
Cancelled -Tickets cancelled by approver.
Remarks Text entered by the approver at the time of approval.
Requested By The name of the user who raised the ticket request.
This is displayed only to the final approver and if
the final status is approved.

## [p92]

www.arconnet.com|Copyright © 2025 92
•
•
•
•
1.
2.
3.
Fields Description
Service Group The name of the service group to which the service
belongs.
Service The name of the service for which the request is raised.
Ticket Type The ticket type of the request:
PE - Planned Event
CR - Change Request
Activity Type The activity type:
SA (Service Affecting)
NSA (Non Service Affecting)
Executor The user who uses the ticket to access the service.
Start Time Date/time from which the ticket is valid.
End Time Date/time until which the ticket is valid.
Approval Status The status of the ticket request.
1.5.5.2.5.4 Critical Commands Approval Logs
What is Critical Command Request?
The admin can restrict the critical command which cannot be fired by the user. If the user wants to fire those
commands, the critical command request can be raised. Once it will approve by the admin, the approval logs will
be generated.
How to Logs critical command?
To see the generated critical command approval logs, proceed with the following steps:
Navigate to, Manage > Approval Logs > Critical Command.
Select Date From and Date To.
Click on Go!. Log details associated with the request are displayed in tabular format.
Refer to the following table to understand the data displayed under each column:

## [p93]

www.arconnet.com|Copyright © 2025 93
1.
Field Name Description
Transaction ID A unique ID associated with each transaction
Requested By The name of the user who wants to fire the critical
command.
Requested On Date/time at which the the request was raised.
Approved On Date/time at which the request was approved.
Command Name of the command that the user wants to fire.
Description Description of the command request.
Session ID Unique Session ID associated with each session.
Current status Present status of the request.
Request The status of the request as follows:
Approved
Rejected
Pending
Comments The comment putted by the approver.
1.5.5.2.5.5 Service Transactions Approval Logs
Service transactions approval logs display approval details of all the service transactions in ARCON | PAM.
How to view Service Transactions Approval Logs?
Follow the steps below to view Service Transactions Approval Logs:
Navigate to, Master > Approval Logs > Service Transaction.

## [p94]

www.arconnet.com|Copyright © 2025 94
2.
3.
•
•
•
Select the Date From and Date To.
Click on Go!. Logs of details associated with the request are displayed in tabular format.
Refer to the following table to understand the data displayed under each column:
Field Name Description
Transaction ID A unique ID associated with each transaction.
Transaction Set to service transaction by default.
Operation Action performed at service level:
Create - Creation of service.
Modify - Modification of service.
Delete - Deletion of service.
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the target server IP.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
Approval Date Date/time at which the request was approved/rejected.

## [p95]

www.arconnet.com|Copyright © 2025 95
•
•
1.
2.
3.
•
•
•
•
•
Field Name Description
Approvals Final status of the request:
Approved
Rejected
1.5.5.2.5.6 User Transactions Approval Logs
User transactions approval logs display approval details of all the user transactions in ARCON | PAM.
How to view User Transactions Approval Logs?
Follow the steps below to view User Transactions Approval Logs:
Click on :w: Approval Logs.
Click on User Transactions. Approval Logs - User Transactions page will appear.
Logs of details associated with the request are displayed.
Refer to the following table to understand the data displayed under each column:
Fields Description
Transaction ID A unique ID associated with each transaction
Transaction Set to user transaction by default.
Operation Action performed at user level:
Create - Creation of user
Modify - Modification of user
Delete - Deletion of user
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the target server IP.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
Approval Date Date/time at which the request was approved/rejected.
Approvals Final status of the request:
Approved
Rejected

## [p96]

www.arconnet.com|Copyright © 2025 96
1.
2.
3.
•
•
1.5.5.2.5.7 User Group-Service Group Transactions Approval Logs
User Group-Service Group transaction approval logs display approval details of all the User Group-Service
Group transactions in ARCON | PAM.
How to view User Group-Service Group Transactions Approval Logs?
Follow the steps below to view User Group-Service Group Transactions Approval Logs:
Click on :w: Approval Logs.
Click on User Group and Service Group Transactions. Approval Logs - User Group and Service Group
Transactions page will appear.
Logs of details associated with the request are displayed.
Refer to the following table to understand the data displayed under each column:
Fields Description
Operation Action performed at user level:
Assigned - Assign server group to user group
Revoked - Revoke server group from user group
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the activity performed by the user.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
Approval Date Date/time at which the request was approved/rejected.

## [p97]

www.arconnet.com|Copyright © 2025 97
•
•
1.
2.
3.
•
•
•
Fields Description
Approvals Final status of the request:
Approved
Rejected
1.5.5.2.5.8 Requests to View Video Log Approvals
Video Logs - View Approvals displays approval details of all requests to view video logs made in ARCON | PAM.
How to view Requests to view Video Log Approvals?
Follow the steps below to view Requests to View Video Log Approvals:
Click on :w: Approval Logs.
Click on Video Logs. Approval Logs - Video Logs page will appear.
Logs of details associated with the request are displayed.
Refer to the following table to understand the data displayed under each column:
Fields Description
Log ID A unique ID with log.
From Date and Time Date/time from which logs are captured
To Date and Time Date/time till which the logs are captured
Object Type Set to video log by default.
Operation Type Action performed
View - To view the video logs
Requested By The name of the Administrator who performed the
transaction.
Requested On Date/time of transaction.
Details Details of the activity performed by the user.
Current Level The current approval level of the request.
Last Level The last approval level of the request.
Approval Date Date/time at which the request was approved/rejected.
Approvals Final status of the request:
Approved
Rejected

## [p98]

www.arconnet.com|Copyright © 2025 98
1.5.5.2.6 Access Logs
Video logs are recorded and stored for multiple activities in ARCON | PAM such as services accessed,
processes used, and commands fired. These logs are crucial as they help in auditing and monitoring security and
regulatory compliance.
1.5.5.2.6.1 How to Create a Video Log request?
Follow the steps below to create a video log request:
• To view the details of activity performed by users on services, users must have the following
permission(s):
View Server Access Log

## [p99]

www.arconnet.com|Copyright © 2025 99
1.
2.
3.
•
•
Select the Manager tab.
Select Access Logs
  from the left pane.
Select the filters and click submit. Access log details will be generated in a grid.
Refer to the following table to understand the data displayed under each column:
Fields Description
Session ID A unique session ID associated with each session.
User ID ID associated with the user.
User Machine Machine details of the user whose activity is captured.
Service IP The IP address of the target servers.
Service Username The username of the service.
DB Instance The instance of the target servers.
Service Type The name of the service type.
Service Reference Number The reference number of the service.
Other Details Any extra details.
Service Logged On Date/time from which logs are captured.
Service Logged Out Date/time until which the logs are captured.
Details Details of the request (click to view).
View Video Log Request
From Date and Time Date/time from which you want to access the log.
To Date and Time Date/time until which you want to access the log.
Description Brief summary of the request explaining the purpose of
the request to the approver.
Options Request by the user:
Show Details - View the video log
Export to Word - Allow export of the log in word
format.
1.5.5.2.7 Application Settings
1.5.5.2.7.1 What is API User Registration?
This section allows you to register users in an API hosted in your environment. You can register users for APIs
such as DWH Applications, Reporting Portal, ARCON PAM API, and so on. In the API environment, users can
configure service onboarding settings and AGW.

## [p100]

www.arconnet.com|Copyright © 2025 100
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
1.5.5.2.7.2 Why is API User Registration Needed?
Enable secure and managed access to various ARCON APIs
Support automation and integration with third-party systems and tools
Allow granular control over who can interact with which API endpoints
Ensure proper configuration of service onboarding and API Gateway behavior
Strengthen API governance and prevent unauthorized API usage
The following topics are included in this section:
API User List
Application List
User Self-Registration
Service Onboarding Settings
AGW Configuration
1.5.5.2.7.3 How to Access Application Settings?
To navigate to this section, click Manager → Application Settings.
1.5.5.2.7.4 API User List
The API User Registration creates a user account in the ARCON | PAM application. It allows Administrators to
register users for configured applications, edit user details and access types, delete registered users, and
register new users.
0How to create an API User?
Select the API User List option from Application Settings. The API Registered User List will appear.

## [p101]

www.arconnet.com|Copyright © 2025 101
2.
3.
Click the + New User option.
Enter the new user details and then click Register.
Refer to the table below to understand the data to be entered in each field:

## [p102]

www.arconnet.com|Copyright © 2025 102
•
•
•
1.
2.
3.
Field Name Description
User Name The name of the user.
Password The password of the user.
Confirm Password Re-enter the password of the user.
Email ID The email ID of the User.
Access Type Select the type of access for the user.
ARCON PAM User Details
ARCON PAM Service Details
ARCON Service Creation
How to update the details of an existing user?
From the API Registered user list, click the Edit icon as shown below.
API User Edit screen is displayed.
Update the details of the user.

## [p103]

www.arconnet.com|Copyright © 2025 103
4.
1.
2.
3.
Click Update. Updated information is reflected on the API User List page.
How to delete details of an existing user?
From the API Registered user list, click the Delete icon as shown below.
Delete User confirmation box pops up.
Click Ok to delete.
1.5.5.2.7.5 Application List
This section lists the API details for which Administrators can register users. They can also edit and delete
configurations and add applications.

## [p104]

www.arconnet.com|Copyright © 2025 104
•
•
1.
2.
3.
Pre-Requisites
The API must be hosted in your environment before the user registration process is initiated.
Hosting Pre-requisites (One or both):
ARCON PAM and ARCON PAM API should both be running on HTTPS with a valid SSL Certificate.
ARCON PAM and ARCON PAM API should both be running on HTTP without a certificate.
How to Create an Application List?
Select Application List from Application Settings.
Click + Add New Application.
Enter details of the new API and click Submit.
•
•
•
To view the Application Settings option, Client users must have the following permission(s):
Manager Menu Display
API User Registration
To view the Application Settings option, Administrators users must have the following permission(s):
API User Registration

## [p105]

www.arconnet.com|Copyright © 2025 105
1.
2.
3.
Refer to the table below to understand the data to be entered in each field:
Field Description
Application Name Select the Application Name of API hosted in your
environment.
URL (with port number if any) Specify the URL of API
Is Active Select the Is Active checkbox to activate the
Application API
How to update details of an existing application?
From the Application list, click the Edit icon as shown below.
Update the details of the API.
Click Update. Updated information will be reflected on the Application List page.
How to delete details of an existing application?
Multiple entries for one Application Name cannot be created. Only one entry against each Application
Name is allowed.

## [p106]

www.arconnet.com|Copyright © 2025 106
1.
2.
3.
From the Application list, click the Delete icon as shown below.
Delete Application confirmation box pops up.
Click Ok to delete.
User Self-Registration
User Self-Registration is a process for self-registration of users, thus eliminating the dependency on
Administrators for creating users in Server Manager.
How to add URL for Self-Registration?
To add the URL for Self-Registration of users to the login page, use the following path:
Client Manager → Manager → Application Settings
Users can edit or delete existing application configurations by selecting the respective icons. Click on the
Delete icon to delete the application or click the Edit icon to modify an application.

## [p107]

www.arconnet.com|Copyright © 2025 107
1.
2.
3.
4.
5.
How to add a New Application?
Add a new application by clicking on Add New Application. The following screen will be displayed.
The Application List screen contains the following fields:
Field Name Description
Application Name Select the application name of APIs hosted in your environment
URL (with Port Number if any) Enter URL of API
Select or enter the required details and click Submit to save the configuration. The “Application saved
successfully” success message will be displayed.
The configuration will be listed in the Application List screen.
Click on the Edit icon to edit the configured Application List. The following screen will be displayed.
You can edit the URL for the selected Application Name. The new Application Name must be different
from all existing Application Names.
6. Enter or select details and click on Update. The “Application details updated successfully“success
message will be displayed.
7. Once the URL is added successfully, the link for User Registration will appear on the login page.
How to Login Using User Registration?
For ARCON | PAM users, the link to the User Registration Portal will be displayed on the login page. The link
can also be provided to the individual users separately.
Follow the below steps to login into User Registration Portal:
Only ARCON | PAM domain users can login to the User Registration Portal.

## [p108]

www.arconnet.com|Copyright © 2025 108
1.
2.
3.
Enter the URL “http(s)://ip-address:port” in the address bar. The User Registration Portal Login screen
will be displayed:
Enter the domain username and password:
Field Name Description
Username Enter a user name.
Password Enter a password.
Once logged in, the following page will be displayed:

## [p109]

www.arconnet.com|Copyright © 2025 109
4. Enter the field level details and click on Submit.
Field Name Description
User Type Select the user type to be Administrator or Client
user. The client will be selected by default.
Domain Name Select the domain name for the user.
•
•
For new users, only the domain from
which the user logged in will be
displayed.
For ARCON | PAM users, all the
available active domains will be
displayed.

## [p110]

www.arconnet.com|Copyright © 2025 110
5.
Field Name Description
User ID For new users, only the user ID of the logged in
user will be displayed.
ARCON | PAM users will be allowed to select a user
from the drop-down list.
User Name For new users, only the Display Name of the logged in
user will be displayed.
For ARCON | PAM users, the username for the User
ID selected in the above field will automatically pop
up.
Email ID Enter the email address of the user.
Privilege User Account Details (For Service Account)
Domain Name   Select the domain name for the privileged account.
User ID Specify the User ID by which the name service has to
be created.
Password Specify the password for the above user ID.
LOB Select the LOB to which the user has to be mapped.
User Group Select the user group to which the user has to be
mapped.
Assign all Services Select this check box to assign all the services of the
selected group to this user.
Submit Click to submit the details.
On clicking Submit, the following window will be displayed with the message Performed Transaction
Added in Workflow. Will Get completed Once Approved.
Users will receive the email notification on
workflow approval.

## [p111]

www.arconnet.com|Copyright © 2025 111
6. Once approved, the user will have been successfully added to ARCON | PAM.
1.5.5.2.7.6 Service Onboarding Settings
What is vRA Integration?
•
•
•
•
Privileged Account field is mandatory to be filled in for Domain Users
Only users with privileged accounts can be created in ARCON | PAM.
Privileged user account details will be used for automatically creating named services.
Condition for creating named services:
There should be at least one named service created and mapped in the server group that
is mapped to the user group to which the user will be mapped.
Domain name of the named service and the domain name of the privileged user account
should be the same.

## [p112]

www.arconnet.com|Copyright © 2025 112
1.
2.
1.
2.
The virtualization of privileged accounts is supported by the ARCON | PAM Onboarding module. vRealize
Automation (vRA) is an important application that allows the onboarding of virtualized privileged accounts.
ARCON | PAM Integration is a one-time manual activity for mapping of vRA Details with ARCON | PAM
entities using ARCON PAM vRA API. After mapping the application to services, these services are
automatically onboarded in ARCON | PAM.
How to Configure VRA Integration Settings?
To navigate to VRA integration settings in ARCON | PAM Client Manager, follow the steps below:
Click on Manager.
Navigate to the sidebar, click Application Settings → Service Onboarding Settings.
How to Add Application Name Mapping?
The Add Application Name Mapping screen for application and Server Group-User Group Mapping is shown
below. Perform the following steps to map the Application to the Server Group and User Group in ARCON |
PAM:
Click on the + Add Mapping option on the right side of the screen.
Enter the details as required.
Field Description
Application Name Add Application Name to integrate.
Server Group Select Server Group from ARCON | PAM in the drop-
down.
User Group Select User Group from ARCON | PAM in the drop-
down.
3. The new configuration will be added to the list.
• User Group Mapping:
Scenario 1: If the specified User Group mapping is available in ARCON | PAM, the API
will check for the Requester's OLM ID (ARCON | PAM User ID) mapping with User
Group.

## [p113]

www.arconnet.com|Copyright © 2025 113
1.
2.
3.
Service Creation Configuration
To navigate through the configuration for Service Mapping, follow the steps below:
Hover on Application Settings.
Select Service Config Mapping. The Application Name Mapping screen will appear.
Click on the + Add Mapping option on the right side of the screen. Enter the details required and click
Add.
•
Scenario 2: If ARCON | PAM User ID is available in the specified User Group, the API
will map the Service to all the users in the specified User Group.
Scenario 3: If ARCON | PAM User ID is not available in the User Group, the API will add
the User ID to the specified User Group and the Service will be mapped to all users in
the specified User Group.
Server Group Mapping :
Scenario 1: If the specified Server Group is available, the API will automatically map the
Service in the existing Server Group.
Scenario 2: If the specified Server Group is not available, the API will do the following:
Create a new Server Group and add the Service to the newly created Server
Group.
Map the Server Group to the LOB from the LOB mapping screen.

## [p114]

www.arconnet.com|Copyright © 2025 114
4.
1.
2.
3.
The new configuration will be added to the list.
LOB Mapping
ARCON | PAM will select LOB based on mapping done in ARCON. It creates a new service and maps it in the
same LOB Request with a new LOB name (which is not mapped in ARCON). As a result, it will set the default
LOB marked in Mapping.0
To navigate to the configuration for LOB Mapping, follow the steps below:
Hover on Application Settings.
Select LOB Mapping. The LOB Mapping screen appears.
Click on the + Add Mapping option on the right side of the screen.
•
•
ARCON will select the respective Service Type mapped for vRA.
Service requests will be rejected for any unmapped value. After all the above details have been
Configured in ARCON | PAM, the following additional information needs to be passed for API in
XML or JSON for Service Creation and assigning to Server Group.

## [p115]

www.arconnet.com|Copyright © 2025 115
4. The new configuration will be added to the list.
Use Cases
Use Case Description
Scenario 1 (All Mapping Configured)
LOBID: NOIDA1
ServerGroupName: DTH-DARTS
IPAddress: 10.12.250.1
ServiceUserName: arcos_user
AutoMapUsersInUserGroup: true
RequestorUserID: raj.sharma
RequestorDomain: oneairtel
vRA calls ARCON API with the required Service
Parameters (as given) along with
BU/App Name(Server Group) as DTH-DARTS and the
Requestor ID OLM (ARCOS User
ID) as raj.sharma. API checks for the Application
Name Mapping of specified
details and finds a mapping for the same. It adds the
service to Server Group
and maps this Service to specified User ID and all
Users in User Group
(“AutoMapUsersInUserGroup” is passed as true in API
Parameters) as
DTH-DARTS_USERS

## [p116]

www.arconnet.com|Copyright © 2025 116
Use Case Description
Scenario 2 (vRA Application and Server Group not
Mapped)
LOBID: NOIDA1
ServerGroupName: DTH-CloudOps
IPAddress: 10.12.250.1
ServiceUserName: arcos_user
AutoMapUsersInUserGroup: true
RequestorUserID: raj.sharma
RequestorDomain: oneairtel
vRA calls ARCON API with the required Service
Parameters along with BU/App
Name (Server Group) as DTH-CloudOps and the
Requestor ID OLM (ARCOS User ID)
as raj.sharma. API checks for the Application Name
Mapping of specified
details but doesn’t find any mapping for the same. It
creates a new Server
Group and adds the service to the newly created
Server Group. It also maps this
Service to a specified User ID and all Users in User
Group(If
“AutoMapUsersInUserGroup” is passed as true in API
Parameters) as
DTH-CloudOps_USERS
Scenario 3 (vRA Application, Server Group, and User
Group not Mapped)
LOBID: NOIDA1
ServerGroupName: DTH-CloudOps
IPAddress: 10.12.250.1
ServiceUserName: arcos_user
AutoMapUsersInUserGroup: true
RequestorUserID: raj.sharma
RequestorDomain: oneairtel
vRA calls ARCON API with the required Service
Parameters (as given) along
with BU/App Name(Server Group) as DTH-CloudOps,
and the Requestor ID
OLM(ARCOS User ID) as raj.sharma. The API checks
for the Application
Name Mapping of specified details but doesn’t find
any mapping for the
same. It creates a new Server Group and adds the
service to the newly
created Server Group. It also checks for availability
User Group as
DTH-CloudOps_USERS but doesn’t find the user
group, so it creates a
new User Group and maps this Service to specified
User ID and all Users in
the newly added User Group(If
“AutoMapUsersInUserGroup” is passed as
true in API Parameters) as DTH-CloudOps_USERS

## [p117]

www.arconnet.com|Copyright © 2025 117
•
•
•
•
•
•
•
•
Use Case Description
Scenario 4 (All mapping configured. OLM ID (User ID)
not available)
LOBID: NOIDA1
ServerGroupName: DTH-DARTS
IPAddress: 10.12.250.1
ServiceUserName: arcos_user
AutoMapUsersInUserGroup: true
RequestorUserID: raj.sharma
RequestorDomain: oneairtel
vRA calls ARCON API with the required Service
Parameters (as given) along
with BU/App Name(Server Group) as DTH-DARTS,
and the Requestor ID
OLM (ARCOS User ID) as raj.sharma. The API checks
for the Application
Name Mapping of specified details and finds a
mapping for the same. It adds the service to Server
Group and checks if the Requestor’s User
ID is available in ARCOS. It doesn’t find the specified
User ID, so it adds the User ID in ARCOS with the
specified LOB after creating a new User ID. It maps
this Service to a specified User ID and all Users in User
Group
(“AutoMapUsersInUserGroup” is passed as true in API
Parameters) as
DTH-DARTS_USERS
1.5.5.2.7.7 AGW Configuration
What is the Application Gateway Server (AGW)?
Application Gateway Server (AGW) is a solution that controls all the entry points into your environment. The
AGW Server is placed in a secure environment and monitored at all times. Remote sessions can be taken from
the AGW Server to other applications and machines. Connections can also be recorded and isolated
connections with an AGW Server.
Pre-requisites
For AGW connection, Use AGW for Open Connection configuration should be enabled under Settings.
It is recommended to install AGW on an independent server other than the app server.
RDS in Windows Server 2012 requires Active Directory, 2003 or newer.
Make sure that the Windows Server 2012 or more is installed and the server you are using is joined to
that domain.
Domain ID is required for the installation of the RDS role.
This Domain ID should be a part of the Administrators group on the AGW Plus server.
IIS Manager is required on the AGWPlus server and Default Website should not be deleted.
.NET Framework 4.5 is needed on the AGWPlus Server. Any two custom ports need to be available/open
on the AGWPlus Server. (Preferred 8008,8080)
AGW Configuration
Follow the steps below to set up the AGW configuration: 0
•
To view this configuration, users must have the following permission(s):
Application Gateway Server

## [p118]

www.arconnet.com|Copyright © 2025 118
1.
2.
3.
The AGW Configuration will be displayed under Application Settings as shown in the image below for
users with the Application Gateway Server permission.
Click on AGW Configuration. The AGW Dashboard will appear. Multiple AGW Servers can be added
here.
Click + Add New. The following ADD Configuration screen will be displayed.

## [p119]

www.arconnet.com|Copyright © 2025 119
4. Enter all descriptions as shown in the table below and click Add.
Field Description
Configuration Name Name of AGW Server.
Configuration Description Description of AGW Server.
Configuration URL Enter the URL of the AGW Server where TS Plus is
configured.
EXE Path Full Path of ARWH executable.
Exe Directory Path Directory path of the ARWH Executable file.
User Name Local user of the AGW Server.
Password Password of the above username.

## [p120]

www.arconnet.com|Copyright © 2025 120
•
•
1.
Field Description
PIN PIN configured in TS Plus Web Credential.
Use of Server Manager Select this checkbox to launch server manager on a
particular AGW Server.
If only one AGW server is hosted and this
checkbox is enabled, then the server manager
will be hosted on that particular AGW server.
If there are multiple AGW Servers hosted and
this checkbox is enabled, then the server
manager will be hosted on any one of the AGW
servers randomly.
Is Active Select this checkbox if this AGW server is the one to
be kept active.
5. Once AGW is configured, users can map services to the AGW Server.
AGW Service Mapping
This option allows users to map services to AGW servers so that users can make connections through AGW.
Follow the steps below to map a service to AGW:
Click AGW to Service Mapping.

## [p121]

www.arconnet.com|Copyright © 2025 121
2.
3.
4.
5.
6.
7.
Select the AGW Server Name, LOB, Server Group, Service Type, and AGW preference path.
On clicking the Use only AGW checkbox, the connection for that service will always take place
via AGW.
Click Apply to enable/allow AGW for all the listed services.
A pop-up message will be displayed with the total number of services that will be mapped.
Click Proceed to continue with mapping all the services in the selected category with the AGW Server.
Click Review Selection to list all the services in the selected category and select the services for which
AGW has to be enabled.
Click Apply.

## [p122]

www.arconnet.com|Copyright © 2025 122
8.
9.
10.
a.
A pop-up message will be displayed with the total number of services that will be mapped.
Click Proceed to continue with the mapping process.
On the successful mapping of AGW to the services, the following message will be displayed on the
screen.
Arcon Terminal Server is Mapped to Services
AGW to Service UnMapping
This option will allow users to unmap services to AGW servers so that AGW permissions are revoked for the
particular services.

## [p123]

www.arconnet.com|Copyright © 2025 123
1.
2.
3.
4.
5.
Follow the steps below to unmap a service to AGW:
Click AGW to Service UnMapping.
Select the AGW Server Name, LOB, Server Group, and Service Type.
Click Apply to unmap AGW for all the listed services in the selected category.
A pop-up message will be displayed with the total number of services that will be unmapped.
Click Proceed to continue with the unmapping process. On successful unmapping, it will display the
message AGW server is unmapped to services.
Click Review Selection to list all the services in the selected category and users can select the services
to be unmapped from the list. Click Apply.

## [p124]

www.arconnet.com|Copyright © 2025 124
6.
7.
8.
A pop-up message will be displayed with the total number of services that will be unmapped.
Click Proceed to continue with the unmapping process. On successful unmapping, a message will be
displayed.
The selected Service has been updated
AGW Preference Path0

## [p125]

www.arconnet.com|Copyright © 2025 125
This option will allow users to map the path of the thick clients installed on the Application Gateway Server.
The AGW Preference Path screen contains the following fields:
Field Description
AGW Name Name of the AGW Server.
LOB Select the LOB name from the drop-down.
Service Type Select the service type from the drop-down.
Preference Path Enter the integrated third-party application’s exe
path.
Enter the above details and click Update.
Final Connection
Once the above configurations are done, the user has two choices to make a connection - either via AGW or a
normal open connection. ARCON | PAM supports multiple sessions, whereby a user can access multiple
services at a time. All the sessions opened are recorded and stored in different files.

## [p126]

www.arconnet.com|Copyright © 2025 126
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
1.5.5.3 Reports
1.5.5.3.1 Overview
ARCON | PAM provides reports of all transactions performed under its systems to help users discover and
prioritize important fixes such as dashboards, group reports, privilege reports, security reports, service reports,
user reports, and Vault reports. Reports are fetched from the Client Manager. Reports can be obtained easily
from the Client Manager and exported in .xls, .doc, .csv, and .pdf file formats. Reports can be generated
automatically, daily, weekly, or monthly, based on the scheduler configured in Server Manager (Refer to
Scheduler Master and Schedule Reports for detailed information).
The Reports Section Includes:
Dashboard Reports
Group Reports
LOB Reports
Logs Report
Performance Reports
Privilege Reports
Security Reports
Service Reports
User Reports
Vault Reports
1.5.5.3.2 Report Builder Functionalities
The following report builder functionalities are applicable to all reports on ACMO. The Active Services Group
Wise Report is shown as an example below:
•
•
If for a particular service AGW is not configured, the user will not see the ‘Have this open
connection’ option and a normal connection will be taken directly.
If Use only AGW checkbox is selected on the AGW to Service Mapping  configuration, the
connection for that service will always take place via AGW. In this case, also, the user will not
see the ‘Have this open connection’ option.

## [p127]

www.arconnet.com|Copyright © 2025 127
Refer to the following table to understand the Report Builder Functionalities:
UI Components Description
Filter Filtering provides a more advanced and versatile way
of controlling which records should be displayed. The
filters can be selected from the attributes at the top.
Pin Filter Filters can be pinned to access the report directly and
eliminate the need for selection over and over again.
Show Entries Display the number of rows selected from the drop-
down in the reporting grid.
Searching The search filter at the top provides a quick and easy
way to reduce the records in the report grid and
display only those records that contain the data that
you want to see.
Sorting Sort data alphabetically or numerically in ascending/
descending order. This functionality is available at the
top of every column.

## [p128]

www.arconnet.com|Copyright © 2025 128
1.
2.
UI Components Description
Pagination The Report grid at the bottom is paginated. It prints all
the data in a table, no matter how long. You can scroll
down through all the rows with the scroll bar on the
right.
Export to CSV, Excel, Word, and PDF Export and download any report downloaded
in .CSV, .XLS, DOC or .PDF format.
Expand Click on the Expand icon to view columns that are not
displayed because of limited screen size.
1.5.5.3.3 How to Generate a Report?
1.5.5.3.3.1 Overview
Reports are generated based on activities performed in PAM. Not all reports are accessible/visible to everyone.
Users can view reports only those reports for which they have permission. These permissions have to be
assigned by Administrators. This section helps to generate the report in multiple categories such as Logs, LOB,
performance, Vault, services, etc. All generated data can be exported in multiple formats such
as .CSV, .PDF, .Doc, etc.
1.5.5.3.3.2 Steps to generate a report
From the Menu Bar, select the Reports menu.
Click on the three-line icon to expand the left pane.

## [p129]

www.arconnet.com|Copyright © 2025 129
3.
4.
5.
6.
Choose the type of report.
Apply the required filters in the Filter section.
Click on the View Report button to see the report.
Choose the file format from the drop-down and click on the Download File icon to download the report.

## [p130]

www.arconnet.com|Copyright © 2025 130
7.
8.
The following message pop-up is displayed. Checkbox Email Notification, enter the required Email ID,
and Click Submit.
The following message pop-up is displayed “You will be notified once report is available for download”
then click the Close button.

## [p131]

www.arconnet.com|Copyright © 2025 131
9.
10.
The download request will be processed and the report will appear in the Exported Reports screen.
Refer to the Exported Reports section for further steps information.
1.5.5.3.4 Exported Reports
1.5.5.3.4.1 Overview
The Exported Reports is the feature that is used to download the offline report in multiple formats. This section
explains how to export the reports requested for download in various formats as shown in the table below. The
Exported Reports page (also titled My Report Downloads) will help you download or delete exported reports
record-wise from the list. Users can download or delete all the exported reports at once.
The user needs to generate and export the report so that this report will be listed in the exported reports
section as shown in the below image:

## [p132]

www.arconnet.com|Copyright © 2025 132
1.
2.
3.
4.
1.
2.
3.
4.
1.
2.
3.
4.
1.
2.
3.
4.
Reports can be exported in the following formats:
Format Procedure
CSV In the Generated Reports list, click on the .csv icon.
Select the Email Notification  checkbox and enter the email address to receive the
report via email. Reports received on emails are usually longer. For example, reports
generated for 3 months or more.
Smaller reports (generated for less than 90 days) can be downloaded directly from the
Exported Report section.
The name of the downloaded report will be LOBName_ReportName.csv
XLS In the Generated Reports list, click on the .xls icon.
Select the Email Notification  checkbox and enter the email address to receive the
report via email. Reports received on emails are usually longer. For example, reports
generated for 3 months or more.
Smaller reports (generated for less than 90 days) can be downloaded directly from the
Exported Report section.
The name of the downloaded report will be LOBName_ReportName.xls
DOC In the Generated Reports list, click on the .doc icon.
Select the Email Notification  checkbox and enter the email address to receive the
report via email. Reports received on emails are usually longer. For example, reports
generated for 3 months or more.
Smaller reports (generated for less than 90 days) can be downloaded directly from the
Exported Report section.
The name of the downloaded report will be LOBName_ReportName.doc
PDF In the Generated Reports list, click on the .pdf icon.
Select the Email Notification  checkbox and enter the email address to receive the
report via email. Reports received on emails are usually longer. For example, reports
generated for 3 months or more.
Smaller reports (generated for less than 90 days) can be downloaded directly from the
Exported Report section.
The name of the downloaded report will be LOBName_ReportName.pdf
1.5.5.3.4.2 Deleting Reports
To delete reports in bulk from the Exported Reports section, click on the Check/ Uncheck All button to select
all reports and then click the Delete Selected Mails button.
1.5.5.3.5 Dashboard Reports
What is a Dashboard Report?
The Dashboard Report displays a graphical view of real-time user interfaces of different activities being
performed in ARCON | PAM. It is a graphical view of the user’s access to services in terms of commands fired,

## [p133]

www.arconnet.com|Copyright © 2025 133
•
•
•
•
password rotation, and status of password security. The Dashboard Report further provides links to view and
filter the various reports running in the ARCON | PAM application.
The following reports are available in Dashboard Reports:
ARCON PAM Live
Enterprise Password
Live Server Sessions
User Access & Usage
1.5.5.3.5.1 ARCON PAM Live
The ARCON PAM Live report generates a line graph that displays user activity over the last 5 hours. It displays
the number of users who have logged in, the number of services that have been accessed, the total number of
commands that have been fired, and the number of critical and restricted commands that have been fired.
Drag and navigate the cursor anywhere on the graph to view the exact count details.
For instance, In the above figure, you can see that at 10:26:00 AM on 01/06/2022 there were only two users
logged in, zero Services Accessed, zero Commands Fired (both Critical and Non-Critical), and zero Restricted
Commands.
•
To view this report, users must have the following permission(s):
ARCON PAM Live
Click on the Refresh Dashboard button on the extreme right-hand side of the report window to
refresh the report.

## [p134]

www.arconnet.com|Copyright © 2025 134
1.5.5.3.5.2 Enterprise Password
The Enterprise Password report displays a dashboard that gives information about the rotation frequency of
passwords changed and scheduled, the compliant status of the password, the security status of the password
(open or closed), the success/failure rate of the password change, and provides a table containing information
about upcoming password reviews.
Drag and navigate the cursor anywhere on the graph to view the exact count details.
For example, the Password Rotation Frequency graph above shows the Changed password and the Scheduled
password for November 2021.
1.5.5.3.5.3 Live Server Sessions
What is Live Server Sessions Report?
The Live Server Sessions  report is used to generate the report which displays a list of ongoing sessions and
services that users have accessed. Information about access to critical servers is shown in a table and pie
•
To view this report, users must have the following permission(s):
Enterprise Password
Click on the Refresh Dashboard button on the extreme right-hand side of the report window to
refresh the report.

## [p135]

www.arconnet.com|Copyright © 2025 135
graphs. The most-used servers are displayed as a bar graph. The LOB and filters need to be selected from the
dropdown by the user then the report will be generated automatically.
1.5.5.3.5.4 User Access & Usage
What is User Access and Usage Report?
The User Access & Usage report gives information about criticality-based user activity, time-based user
activity, service access, high usage service accounts, and provides a table containing information about critical
•
To view this report, users must have the following permission(s):
Live Server Sessions
Click on the Refresh Dashboard button on the extreme right-hand side of the report window to
refresh the report.

## [p136]

www.arconnet.com|Copyright © 2025 136
commands and their count to identify the risk and damage of the assets. Select the required information from
the dropdown of the filters and click on view report. The report generates automatically.
Drag and navigate the cursor anywhere on the graph to view the exact count details.
For example, the Criticality Based User Activity graph shows the exact count of the servers accessed in the
month of November, December, and January of Low Critical Status.
•
To view this report, users must have the following permission(s):
User Access & Usage

## [p137]

www.arconnet.com|Copyright © 2025 137
•
•
•
•
•
1.5.5.3.6 Group Reports
What are Group reports?
Group Reports is the feature where the user can generate and download the report data of servers and users.
for example, all the users created in user groups and all the servers created in service groups. Also, the user can
see all the service details in the service group which helps to find the total services in server groups.
The following reports are available in Group Reports:
Servers In Server Group
Service Group Report
Services In Server Group
User Group Report
Users In User Group
1.5.5.3.6.1 Servers in Service Group
What is Servers in Service Group Report?
The Servers in Service Group report displays details of all the servers created in a Service Group, regardless of
the LOB. The information is represented in a graphical and grid view format, based on the server's IP address.
The user needs to click the View Report button to generate the report. This report can be downloaded in
multiple formats such as CSV, PDF, XLS, and DOC.
Click on the Refresh Dashboard button on the extreme right-hand side of the report window to
refresh the report.
•
To view this report, users must have the following permission(s):
Servers In Service Group

## [p138]

www.arconnet.com|Copyright © 2025 138
The following columns can be seen in this report:
Field Name Description
Sr. No. To identify and distinguish rows
IP Address Displays IP address of the target servers
Host Name Displays hostname of the target servers
Instance Displays instance of the target servers
Port Displays port number of the target server (if configured)
Domain Name Displays the domain name to which the target server belongs
Service Group Displays the service group name to which that particular server
belongs

## [p139]

www.arconnet.com|Copyright © 2025 139
Field Name Description
LOB/Profile Displays name of the LOB for which the server is configured
1.5.5.3.6.2 Service Group Report
What is Service Group report?
Service Group Reports is the feature used to generate a report of the services created and mapped with a
group of services. The user needs to click the View Report button, and then the report generates automatically
in grid view. The report can be exported and downloaded in multiple formats, such as CSV, PDF, XLS, and DOC.
The following columns can be seen in this report:
Field Name Description
Sr. No. To identify and distinguish rows
LOB Displays the domain name to which the target service belongs
Group Name The name of the service group
Group Description Text entered during the creation of the service group
Created By The name of the user who created the service group
Created On Date/time of the creation of the service group
1.5.5.3.6.3 Services in Service Group
What is Services in Service Group Report?
The Services in Service Group  report displays information about all the services created in a Service Group,
regardless of the LOB. The information is represented in a graphical and grid view format based on the server's
•
To view this report, users must have the following permission(s):
Service Group Report

## [p140]

www.arconnet.com|Copyright © 2025 140
Service username. The user needs to click the View Report button to generate and export in multiple formats,
such as CSV, XLS, PDF, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target servers
Service User Name The username of the service
Host Name The hostname of the target servers
Instance The instance of the target servers
•
To view this report, users must have the following permission(s):
Services in Service Group

## [p141]

www.arconnet.com|Copyright © 2025 141
Field Names Description
Port The port number of the target server (if configured)
Domain Name The domain name to which the target server belongs
Service Group The service group name to which that particular
server belongs
LOB/Profile The name of the LOB for which the server is
configured
1.5.5.3.6.4 User Group Report
What is a User Group Report?
The User Group Report provides information about all of the user groups created in ARCON | PAM, regardless
of the LOB. The report is generated in table format. The user needs to click the View Report to generate and
export in multiple formats such as CSV, PDF, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB It displays the name of the LOB
Group Name The name of the user group
Group Description Text entered during the creation of the user group
•
To view this report, users must have the following permission(s):
User Group Report

## [p142]

www.arconnet.com|Copyright © 2025 142
Field Names Description
Created By The name of the Administrator who created the user
group
Created On Date/time of the creation of the user group by the
Administrator
1.5.5.3.6.5 Users in User Group
What is Users in User Group Report?
The Users in User Group report displays information about all the users created in a User Group, regardless of
the LOB. The information is represented in a graphical and grid view format based on the server's Service
username. The user needs to click the View Report button to generate and export in multiple formats, such as
CSV, XLS, PDF, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
Users in the User Group

## [p143]

www.arconnet.com|Copyright © 2025 143
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
Field Names Description
Sr. No. To identify and distinguish rows
User name The name of the user
Display Name The display name of the user
Domain The domain name to which that user belongs
User Type Type of user
Client
Admin
LOB It displays the name of the LOB to which that user
belongs
User Group User group name to which that particular user
belongs
1.5.5.3.7 LOB Reports
What are LOB Reports?
LOB Reports generate details for all ARCON | PAM LOBs and their relationships with PAM entities such as
users, services, groups, etc. It helps generate a graphical view and exact count of group-wise details of users and
services that are active and inactive in ARCON | PAM. In addition, it also displays detailed descriptions of all the
LOBs created in ARCON | PAM, descriptions of the objects mapped to LOBs, and the LOB-wise status of
unique IP addresses and services.
The following reports are available in LOB Reports:
Active Services Group Wise Report
Active Services Report
Active Users Report
Dormant Users Report
Inactive Services Report
LOB Details Report
Object Status Report
Service Count Report
1.5.5.3.7.1 Active Services Group Wise Report
What is Active Services Group Wise Report?
Active Services Group Wise Report displays the information about all active services in ARCON | PAM service
groups. The user can find the all details of active services such as LOB, IP address, hostname, port, description,
and the time till the service is activated. The user needs to select the required information in available filters
and then click the View Report button to generate and export in multiple formats such as CSV, XLS, PDF, and
DOC.

## [p144]

www.arconnet.com|Copyright © 2025 144
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB/Profile The name of the LOB in which there are active
services
Service Type The active service type for the selected server group
IP Address The IP address of the target server
•
To view this report, users must have the following permission(s):
Active Services Group Wise Report

## [p145]

www.arconnet.com|Copyright © 2025 145
Field Names Description
Host Name The hostname of the target server
User ID The User ID associated with the user
Domain Name The domain name to which the target server belongs
DB Instance The instance of the target servers
Port The port number of the target server (if configured)
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Active Till The date until which the service will work
1.5.5.3.7.2 Active Services Report.
What are Active Services Report?
Active Services Report is the feature where the user can find information about valid services. This report
generates information about all active services in ARCON | PAM. Active services are ones whose validity has
not expired yet. The user needs to select the required information in available filters and click the View Report
button to generate the report. This report can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Active Services Report

## [p146]

www.arconnet.com|Copyright © 2025 146
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows.
Username The username given to the service by the
Administrator.
Server IP The IP address of the target server.
Service Type The active service type.
Host Name Displays the name of the host or IP address.
Created On Date and time of the user's creation by the
administrator.
DB Instance The instance of the target servers.
Description 1 Text entered during the creation of the service by the
Administrator.
Parameter Display the parameter given to the service.
Last Accessed By The name of the administrator who last accessed the
service.

## [p147]

www.arconnet.com|Copyright © 2025 147
Field Names Description
Service Valid Till Date/time until which the service will work.
Assigned By The Administrator who allocated the user to the
service.
Assigned On The date and time when the service was assigned to
the user.
Password Change Enable It specifies whether the password change is enabled
or not.
“Yes” denotes that the password change is enabled.
“No“ denotes that the password change is not
enabled.
Last Access Time Date/time on which the service was last used.
Service Groups The name of the service group to which the server
belongs.
1.5.5.3.7.3 Active Users Report
What is Active Users Report?
The Active Users Report gives information about all active users and their related LOBs in ARCON | PAM. An
active user is defined as one who has interacted with the PAM application within a certain period. To generate
this report, the user needs to select the required information in available filters and click on the View Report
button. It can be exported and downloaded in formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Active Users Report

## [p148]

www.arconnet.com|Copyright © 2025 148
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name Name of the LOB that has active users
LOB Description Description of the LOB that has active users
User ID The User ID associated with the user
Display Name The display name of the user
Valid Till Date until which the user will be active
Email ID Email address of the user as configured by the
Administrator
Mobile Number Mobile number of the user as configured by the
Administrator

## [p149]

www.arconnet.com|Copyright © 2025 149
Field Names Description
User Created By The name of the Administrator who created the user
User Created On Date-time of the creation of the user by the
Administrator
Assign By The Administrator who allocated the user to the LOB
Assign On Date/time of allocation of the user to LOB by the
Administrator
Active Duration Total time duration since the user is active.
User Group Name Specify the user group name to which the user
belongs.
1.5.5.3.7.4 Dormant Users Report.
What is Dormant Users Report?
The Dormant Users Report generates information about all dormant users and their related LOBs in ARCON
PAM. A dormant user has not interacted with the PAM application in a certain period of time. To generate this
report, the user needs to click the View Report button. It can be exported and downloaded in multiple formats
such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Dormant Users Report

## [p150]

www.arconnet.com|Copyright © 2025 150
•
•
Field Names Description
Username The name of the user
Display Name The display name of the user
Email ID Email ID of the user
LOB The name of the LOB in which the user is present
User Group Name Specify the user group name to which the user
belongs.
Domain The domain name to which the user belongs
User Type Type of user
Client
Admin
1.5.5.3.7.5 Inactive Services Report
What is Inactive Services Report?
The Inactive Services Report provides information about all inactive services and their associated Lines of
Business (LOBs) in ARCON | PAM. To generate this report, users must select the necessary information using
the available filters and then click the View Report button. The report can also be exported and downloaded.
•
To view this report, users must have the following permission(s):
Inactive Services Report

## [p151]

www.arconnet.com|Copyright © 2025 151
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name Name of the LOB that has active users
LOB Description Description of the LOB that has active users
Username The name of the user
Server IP The IP address of the target server
Host Name It displays the hostname or IP address
DB Instance It displays the instance name of the service
Service Type It displays the inactive service type
Created On Date/time that the service was created on
Service Valid Till Date/time until which the service will work

## [p152]

www.arconnet.com|Copyright © 2025 152
Field Names Description
Assign By The Administrator who allocated the user to the LOB
Assign On Date/time of allocation of the user to LOB by the
Administrator
Last Accessed Time Date/time at which the service was last used
Last Accessed By Name of the admin, the service was last accessed by
Service Group Specify the service group name to which the service
belongs.
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
1.5.5.3.7.6 LOB Details Report
What is LOB Details Report?
The LOB Details Report is the feature that generates detailed information about all the LOBs created in
ARCON | PAM which helps to know the description, name of the user who has created the respective LOB,
date, and time when it was created. To generate this report, the user needs to click the View Report button. It
can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
LOB Details Report

## [p153]

www.arconnet.com|Copyright © 2025 153
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Name Name of the LOB that was created
Short Name Short name assigned to that LOB
Description Description of the LOB entered by the Administrator
at the time of creation
Address LOB Address
Created By The name of the Administrator who created the LOB
Created On Date/time of the creation of the user by the
Administrator
1.5.5.3.7.7 Object Status Report
What is Object Status Report?
The Object Status Report gives information about the relationship between PAM entities (objects) and LOBs.
The information is represented in a graphical and grid view format and gives the exact count of the total
number of objects that are mapped to LOB. To generate this report, the user needs to click the View Report
button. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.

## [p154]

www.arconnet.com|Copyright © 2025 154
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Profile Name Name of the LOB
•
To view this report, users must have the following permission(s):
Object Status Report

## [p155]

www.arconnet.com|Copyright © 2025 155
•
•
Field Names Description
LOB Profile Description Description of the LOB entered by the Administrator
at the time of the creation
Active Users Count of active users LOB-wise
Inactive Users Count of inactive users LOB-wise
Active Services Count of active services LOB-wise
Inactive Services Count of inactive services LOB-wise
Active Unique IP Count of active unique IPs LOB-wise
Inactive Unique IP Count of inactive unique IPs LOB-wise
User Groups Count of user groups LOB-wise
Service Groups Count of service groups LOB-wise
1.5.5.3.7.8 Service Count Report
What is Service Count Report?
The Service Count Report gives information about the relationship between PAM services and LOBs. The
information is represented in a graphical and grid view format and gives the exact count of:
Unique (Active & Inactive) IP status LOB-wise
Service (Active & Inactive) status LOB-wise
To generate this report, the user needs to click the View Report button. It can be exported and downloaded in
multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Count Report

## [p156]

www.arconnet.com|Copyright © 2025 156
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Profile Name Name of the LOB
LOB Profile Description Description of the LOB entered by the Administrator
at the time of the creation
Service Type Name of the service type
Active Services Count of active services LOB-wise
Inactive Services Count of inactive services LOB-wise
Unique Active IPAddress Count of active unique IPs LOB-wise
Unique Inactive IPAddress Count of inactive unique IPs LOB-wise

## [p157]

www.arconnet.com|Copyright © 2025 157
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
•
•
•
1.5.5.3.8 Logs Report
What is Logs Report?
Logs report is the feature that captures details of all the available logs in a report format. A log report helps
users prevent anything harmful from happening from a security perspective. By routinely reviewing logs, you
can spot malicious activity. The events within a system, including transactions, mistakes, and intrusions, are
historically recorded in log files.
The following reports are available in Logs Reports:
APEM Logs
Approval Delegation Report
Collaboration Report
Day Wise Summary Report
Day Wise User Access Summary Report
Incident Management Logs
Log Review Report
My Vault Logs
Outside ARCON PAM Access Log
Service Access Log
Service Access Log Day Wise Report
Service Password Request Workflow Logs
Service Password Status Logs
Service Request Workflow Logs
Session Activity Log
Session Log Report
Session Wise Summary Report
SIEM command Logs Report
SMS and Email Logs
Ticket Request Workflow Logs
User Access Log report
1.5.5.3.8.1 APEM Logs Report
What is APEM Logs report?
The APEM Logs Report captures print password activities performed via the APEM tool. To generate this
report, the user needs to select the required information in available filters and click the View Report button. It
can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
APEM Logs Report

## [p158]

www.arconnet.com|Copyright © 2025 158
•
•
•
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
File Name Name of the file
Activity Performed Captures all the print password actions taken through
the APEM tool
APEM tool opened
Password Viewed
Read File
Read File process completed
SSH key file successfully downloaded
Envelope No. The unique number associated with each generated
envelope

## [p159]

www.arconnet.com|Copyright © 2025 159
Field Names Description
Envelope Generated On Date/time of generation of the envelope by the
Administrator
Envelope Generated By The Administrator who generated the envelope
Service Type Name of the service type
Service IP Address The IP address of the target server for which the
password is opened through the APEM tool
Server name Name of the server
Server user name Username assigned to the server
Domain Name The domain name to which the target server belongs
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Desktop Details Details of desktop
Log Date Date of log
1.5.5.3.8.2 Approval Delegation Report
What is Approval Delegation Report?
The Approval Delegation Report keeps track of operations performed in the ARCON | PAM delegation module.
Delegation is the process of transferring ownership to a higher-level employee to complete transactions such
as approving raised requests. To generate this report, the user needs to select the required information in
available filters and click the View Report button. It can be exported and downloaded in multiple formats such
as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Approval Delegation Report

## [p160]

www.arconnet.com|Copyright © 2025 160
•
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Operation Actions that are taken on delegation
Create
Modify
Delete
Delegated By The user who sets the delegation module
Delegated To The user who becomes the approver in the absence of
an actual approver set in the workflow
Approval Type Type of approvals users
Start Date Date/time from which the delegation is active
End Date Date/time until which the delegation will be active
Is Active If the module is ON
Created By The name of the user who created the delegation
Created On Date/time of the creation of the delegation by the
user
Modified By The user who changed an existing delegation module

## [p161]

www.arconnet.com|Copyright © 2025 161
Field Names Description
Last Modified On Date/time of change in delegation module
Date Date/time of appointment of the module
1.5.5.3.8.3 Collaboration Report
What is Collaboration Report?
A Collaboration Report displays the details of collaborative sessions between individuals or teams. To generate
this report, the user must select the required information from the available filters and click the View Report
button. It can be exported and downloaded in formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr. No. To identify and distinguish rows.
Session ID It displays the unique identifier assigned to each session.
Service Type It displays the type of service used for session collaboration.
Service Host Name It displays the IP address of the service.
Service User Name It displays the user name of the service.
Participants It displays the total number of individuals who participated in the
session.
Collab Id It displays the unique identifier assigned to a specific collaboration
session.
•
To view this report, users must have the following permission(s):
Collaboration Report

## [p162]

www.arconnet.com|Copyright © 2025 162
Column Name Description
Total Collab Duration It displays the duration of collaboration between users during the
session.
Video Log Specifies whether the video logs are generated or not.
View Details Specifies the details of the session collaboration.
1.5.5.3.8.4 Critical Command Workflow Log
What is Critical Command Workflow Log?
The Critical Command Workflow Log records all high-risk or sensitive commands executed by privileged users
during remote sessions. This log helps administrators monitor, review, and audit command-level activities. To
generate this report, the user must select the required information from the available filters and click the View
Report button. It can be exported and downloaded in formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr. No. To identify and distinguish rows.
Requestor Name The name or ID of the user who initiated the critical command
request.
Request Date The date and time when the request was submitted for approval.
Command Displays the actual critical command executed by the user during
the session.
Description A user-provided note or justification explaining the purpose of
the command.
To view this report, users must have the following permission(s):
Critical Command Workflow Log

## [p163]

www.arconnet.com|Copyright © 2025 163
Column Name Description
On Session Session ID in which the command was executed or requested.
Approver The administrator or authorized user who is responsible for
reviewing and approving the command.
Approver Comment The remarks provided by the approver during the approval
process.
Current Status Shows the current stage of the request (e.g., First Level
Approval).
Request Indicates the request’s current action (e.g., Approved, Requested
Approval).
Approved On Timestamp when the command was approved.
Current Approval Level Displays the level/stage of approval the request is currently in.
Approval Levels The total number of approval levels defined for such critical
command workflows.
1.5.5.3.8.5 Day Wise Summary Report
What is Day Wise Summary Report?
The Day Wise Summary Report displays the date- and time-wise count of activities performed on the Server.
To generate this report, the user needs to click the View Report button. It can be exported and downloaded in
multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Day-wise Summary Report

## [p164]

www.arconnet.com|Copyright © 2025 164
The following columns can be seen in this report:
Filed Names Description
Sr. No. To identify and distinguish rows
Day Date for which the summary is given
Time The time range for which the summary of that day is
given
Session Count Number of sessions accessed on that day
User Count Number of users using PAM on that day
Critical Command The total number of critical commands fired on that
day
Restricted Command The total number of restricted commands fired on
that day
Open Password Number of passwords viewed on that day
Restricted Process Number of restricted processes
1.5.5.3.8.6 Day Wise User Access Summary Report
What is Day Wise User Access Summary Report?

## [p165]

www.arconnet.com|Copyright © 2025 165
The Day Wise User Access Summary Report displays the information for the day-wise unique count of users. To
generate this report, the user needs to select the required information in available filters and click the View
Report button. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Day The date for which the summary is given
Unique Count of Users Specify the unique count of total users
Click the (+) action button located under the Sr.No. column to view the unique count of users.
1.5.5.3.8.7 Incident Management Logs
What are Incident Management Logs?
The Incident Management Logs report captures the logs of the incident which is raised or closed performed by
Incident Management.
When the admin user watches video logs and checks the text logs, the user should be able to raise incidents for
the session. In case they find any suspicious activity and notify the group admin of the server group to which the
service belongs. The group admin should review that incident to take necessary actions and close the incident.
•
To view this report, users must have the following permission(s):
Day Wise User Access Summary Report
To view this report, users must have the following permission(s):

## [p166]

www.arconnet.com|Copyright © 2025 166
The following columns can be seen in this report:
Field Name Description
Sr. No. To identify and distinguish rows
Incident ID This is an ID number that is given to identify the incident.
Session ID This is an ID number that is given to identify the session.
Service Type This column shows the type of service
Service This column shows the name of the service and it contains the service IP
address and server user name of the user etc.
User Name This column shows the name of the user.
• Incident Management Logs

## [p167]

www.arconnet.com|Copyright © 2025 167
Field Name Description
Incident Raised Comment This column shows the comment put by used while raising the incident.
Incident Raised By This column shows the name of the user who raised the incident.
Raised On This column shows the date and time when the incident was raised.
Status This column shows the status of this incident as closed or open.
Incident Closed Comment This column shows the comment put by used while closing the incident.
Closed By This column shows the name of the user who closed the incident.
Closed On This column shows the date and time when the incident was closed.
1.5.5.3.8.8 Log Review Report
What is Log Review Report?
The Log Review Report displays details of all the logs accessed or viewed by Administrators in ARCON | PAM.
Additionally, it also records information from real-time session monitoring, such as video viewing, session
freeze, unfreeze, and logout activities. To generate this report, the user needs to select the required
information in available filters and click on view report. It can be exported and downloaded in multiple formats
such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Log Review Report

## [p168]

www.arconnet.com|Copyright © 2025 168
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows.
Log Name Specify the name of the logs.
Log Type Specify the type of the logs.
Log Viewed By User Id Specify the ID of the user who viewed the logs.
Log Viewed By User Name Specify the name of the user who viewed the logs.
Log Viewed On Specify the date and time when the logs were viewed.
Session accessed By User ID Specify the session was accessed using the specified
User ID.
Session Accessed By User Name Specify the session was accessed using the specified
User Name.
Session Log ID Specify the unique session log ID.
Service IP Specify the IP address of the target server.
Service Host Specify the hostname of the target server.

## [p169]

www.arconnet.com|Copyright © 2025 169
Field Names Description
User Machine Details Specifies the machine details of the user
Service Logged In Specify the date and time when the user logged in to
the service.
Service Logged Out Specify the date and time when the user logged out of
the service.
1.5.5.3.8.9 My Vault Logs
What is My Vault Logs report?
The My Vault Logs report captures all the activities that are carried out in My Vault of ARCON | PAM. To
generate this report, the user needs to select the required information in available filters and click the View
Report button. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
My Vault Logs

## [p170]

www.arconnet.com|Copyright © 2025 170
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
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
File Name Name of the file used in My Vault
Extension Type of file
Text
PDF
JPG
GIF
PNG
Size Weight of file
Status Activity performed on my vault
Upload
Download
Shared
Deleted
Added By The Administrator who added the file
Added On Date/time at which the file was added to my vault
Shared On Date/time at which the file was shared (value will
come only if it was shared) with some user
Shared With The Administrator who shared the file
File Available Till Date/time until which the file will be accessible on my
vault
Deleted By The Administrator who deleted the file
Deleted On Date/time at which the file was deleted (value will
come only if it was deleted)
Recorded On  Date/time at which the file was uploaded
Storage The repository where the file is stored
Database
File Server
1.5.5.3.8.10 Outside ARCON PAM Access Log
What is Outside ARCON PAM Access Log report?

## [p171]

www.arconnet.com|Copyright © 2025 171
The Outside ARCON PAM Access Log report displays information about unauthorized users (outsiders)
attempting to access ARCON | PAM services. To generate this report, the user needs to select the required
information in available filters and click the View Report button. It can be exported and downloaded in multiple
formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Type Name of the service type
Server IP Address The IP address of the target server
Domain Name The domain name of the target server
Client Host Name The hostname of the end user’s machine
Client IP Address The IP address of the end user’s machine
Client User Name The name of the end-user
•
To view this report, users must have the following permission(s):
Outside ARCON PAM Access Logs

## [p172]

www.arconnet.com|Copyright © 2025 172
•
•
•
Field Names Description
Action Performed Activity performed on that service
Block
Email
Email-Block
Server Access Date Time Date/time when the server was accessed
1.5.5.3.8.11 Secret Service Logs
What are Secret Service Logs in PAM?
Secret Service logs in PAM (Privileged Access Management) refer to the detailed records of actions taken by
users with elevated access rights within a system. These logs capture who accessed what resources, when, and
what actions were performed, ensuring accountability and security. To generate this report, the user must
select the required information in available filters and click the View Report  button. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr. No. The sequential number is assigned to each row.
Transaction Type Specify the Activity performed such as created, modified, etc.
Transaction By Specify the name of the administrator by whom the transaction was
initiated.
Secret Type Specify the type of the secret.
Vault Type Specify the type of the vault.
Host Name Specify the hostname of the target server.

## [p173]

www.arconnet.com|Copyright © 2025 173
Column Name Description
IP Address Specify the IP address of the target server.
Domain Specify the domain name of the target server.
User Name Specify the user name assigned to the service.
Description Specify the description given to the Secret Service.
Shared to Specify the name of the individual to whom the administrator
provided the logs.
Recorded On Specify the date and time the logs were recorded.
1.5.5.3.8.12 Service Access Log
What is Service Access Log Report?
The Service Access Log report displays information about all of the services that users have accessed based on
the filters they have chosen. To generate this report, the user needs to select the required information in
available filters and click the View Report button. It can be exported and downloaded in multiple formats such
as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Access Log

## [p174]

www.arconnet.com|Copyright © 2025 174
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Session Log ID Unique session ID assigned to a specific user session.
WorkflowID Unique ID generated for the workflow request.
User ID Unique ID associated with the user.
User Machine IP Machine IP Details of the target server.

## [p175]

www.arconnet.com|Copyright © 2025 175
Field Names Description
Service Type Name of the service type.
Connection Connection details of the target server.
Username The username associated with the target server.
Prompt_UserAccessedUsingUser Name of the prompt user.
Service Ref No Reference Number associated with each SSO while accessing
the service.
Service Reference type Reference Type associated with each SSO while accessing the
service.
Service Reference Detail Reference Details associated with each SSO while accessing the
service.
Domain Name The domain name to which the service belongs.
Host Name The hostname of the service.
Description 1 Text entered during the creation of the service by the
Administrator.
Description 2 Text entered during the creation of the service by the
Administrator.
Description 3 Text entered during the creation of the service by the
Administrator.
Other Details Text entered during the creation of the service by the
Administrator.
Service Logged In Date/time of logging in to that service.
Service Logged Out Date/time of logging out of that service.
Total Session Duration Minutes The timespan while accessing the service.
connection_type Type of connection to that server.
Application SessionId Unique ID associated with all sessions.
Session Extended No Information about whether the session was extended or not.
Session Extended Count The number of times the session was extended.
Access Type Indicates the type of access granted to the user. This can be
Permanent (ongoing access), One-Time (single-use access), or
Time-Based (restricted to a specific time window).
1.5.5.3.8.13 Service Access Log Day Wise Report
What is Service Access Log Day Wise Report?

## [p176]

www.arconnet.com|Copyright © 2025 176
Service Access Log Day Wise Report displays information about the user's total session duration in the hour-
minute format. To generate this report, the user needs to select the required information in available filters and
click the View Report button. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS,
and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User_ID Unique ID associated with the user
TotalSessionDurationInhours:mins Total time spanned in hours : minutes while accessing
the service
1.5.5.3.8.14 Service Password Request Workflow Logs
What is Service Password Request Workflow Logs report?
The Service Password Request Workflow Logs report displays information about all the service password
requests raised by users and actions taken by the approver for that request. To generate this report, the user
needs to select the required information in available filters and click the View Report  button. It can be
exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Access Log Day Wise Report

## [p177]

www.arconnet.com|Copyright © 2025 177
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Service Password Request Workflow Logs

## [p178]

www.arconnet.com|Copyright © 2025 178
•
•
Field Names Description
Request Number The unique number associated with every raised
request
WorkflowId Unique ID generated for the workflow request
LOB/Profile The name of the LOB from which the request was
raised
Requested By The username of the user who raised the request
Requested On Date/time at which the request was raised
Requester EmailId Email ID associated with the user who raised the
request
LOB Workflow LOB name for which the workflow is working
User Group Workflow User group for which the workflow is working
Server Group Workflow The server group for which the workflow is working
Priority Priority of the workflow as defined by the
Administrator at the time of the creation
Description Text entered during the creation of that workflow by
the Administrator
Service type Name of the service type
Service IP address IP Address of the target server
Domain Name The domain name to which the service belongs
Service Username The username associated with the target server
DB Instance Displays instances of the target servers
View On date Date/time on which the request was opened
Open for Hours Time in hours until which the request will remain valid
Open till Date The last date till which the request will remain valid
Current Approver Level The latest level of approval
Approver Levels Total number of approval levels in the workflow
Approver 1 User Name The username of the first approver
Approver 1 Status Status of the request by the first approver
Approved
Rejected

## [p179]

www.arconnet.com|Copyright © 2025 179
•
•
•
•
•
•
Field Names Description
Approver 1 Status On Date/time at which the request was approved/
rejected by the first approver
Approver 1 Comment Remarks entered by approver 1
Approver 1 Email ID Email ID associated with the approver 1
Approver 2 User Name The username of the second approver
Approver 2 Status Status of the request by the second approver
Approved
Rejected
Approver 2 Status On Date/time at which the request was approved/
rejected by the second approver
Approver 2 Comment Remarks entered by approver 2
Approver 2 Email ID Email ID associated with the approver 2
Approver 3 User Name The username of the third approver
Approver 3 Status Status of the request by the third approver
Approved
Rejected
Approver 3 Status On Date/time at which the request was approved/
rejected by the third approver
Approver 3 Comment Remarks entered by approver 3
Approver 3 Email ID Email ID associated with the approver 3
Approver 4 User Name The username of the fourth approver
Approver 4 Status Status of the request by the fourth approver
Approved
Rejected
Approver 4 Status On Date/time at which the request was approved/
rejected by the fourth approver
Approver 4 Comment Remarks entered by approver 4
Approver 4 Email ID Email ID associated with the approver 4
Approver 5 User Name Username of the fifth approver

## [p180]

www.arconnet.com|Copyright © 2025 180
•
•
•
•
Field Names Description
Approver 5 Status Status of the request by the fifth approver
Approved
Rejected
Approver 5 Status On Date/time at which the request was approved/
rejected by the fifth approver
Approver 5 Comment Remarks entered by approver 5
Approver 5 Email ID Email ID associated with the approver 5
Final status The final degree of the request
Approved
Rejected
1.5.5.3.8.15 Service Password Status Logs
What is Service Password Status Logs Report?
The Service Password Status Logs report displays information about the password status of all services. To
generate this report, the user needs to select the required information in available filters and click the View
Report button. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Status Logs

## [p181]

www.arconnet.com|Copyright © 2025 181
The following columns can be seen in this report:
Field Description
Sr. No. To identify and distinguish rows
Service ID Name of the Service Group to which the target server
belongs
IP Address The IP address of the target server
User Name The username associated with the target server
Password Request or Details Specify the details of the requested password
Host Name The hostname of the target server
DB Instance The instance of that target server
Password Age Number of days passed until which password was the
same as the target server
Password Last Changed Date/time of last password change

## [p182]

www.arconnet.com|Copyright © 2025 182
•
•
Field Description
Password Next Change Date/time of next password change
Password Status Status of the password
Open
Close
Password opened from Days Number of days passed after the password was
viewed and opened
Password Opened By Name of the user who viewed the password
Password Opened On Date/time at which the password was viewed
Service Type Name of the service type of the target server
Password Closed By Name of the Administrator who changed the
password of the target server which was open
Password Closed On Date/time at which the password was closed
Service Group Name Name of the Service Group to which the target server
belongs
1.5.5.3.8.16 Service Request Workflow Logs
What is Service Request Workflow Logs Report?
The Service Request Workflow Logs report displays information about all the service access requests raised by
users and actions taken by the approver on that request. To generate this report, the user needs to select the
required information in available filters and click the View Report button. It can be exported and downloaded
in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Request Workflow Logs

## [p183]

www.arconnet.com|Copyright © 2025 183
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
WorkflowID Unique ID generated for the workflow request
LOB/Profile The name of the LOB from which the request was
raised

## [p184]

www.arconnet.com|Copyright © 2025 184
•
•
•
•
•
Field Names Description
Requested By Username who raised the request
Requester Email Id Email ID associated with the user who raised the
request
LOB Workflow LOB name for which the workflow is working
UserGroup_Workflow User group for which the workflow is working
ServerGroup_Workflow Server group for which the workflow is working
Priority Priority of the workflow as defined by the
Administrator at the time of the creation
Requested On Date/time at which the request was raised
Requested Description Text entered at the time of raising the request by the
Administrator
Reference Details
Service Access Requested type Type of service access requested
New
Existing
Requested Access Type Type of request access to that service by the user
Permanent
Time-based
One-time
Service Type Name of the service type
Service IP Address IP Address of the target server
Domain Name The domain name to which the service belongs
Service User Name The user name associated with the target server
DB Instance Displays instances of the target servers
Access Required From Date Date/time from which access is required
Access Required To Date Date/time until which service access is valid
Access Duration Time The total duration of access
Access Period Time at which the user accessed the service
Current Approver Level The latest level of approval

## [p185]

www.arconnet.com|Copyright © 2025 185
•
•
•
•
•
•
•
•
Field Names Description
Approver Levels Total number of approval levels in the workflow
Approver 1 User Name The username of the first approver
Approver 1 Status Status of the request by the first approver
Approved
Rejected
Approver 1 Status On Date/time at which the request was approved/
rejected by the first approver
Approver 1 Comment Remarks entered by approver 1
Approver 1 Email ID Email ID associated with the approver 1
Approver 2 User Name User name of the second approver
Approver 2 Status Status of the request by the second approver
Approved
Rejected
Approver 2 Status On Date/time at which the request was approved/
rejected by the second approver
Approver 2 Comment Remarks entered by approver 2
Approver 2 Email ID Email ID associated with the approver 2
Approver 3 User Name The username of the third approver
Approver 3 Status Status of the request by the third approver
Approved
Rejected
Approver 3 Status On Date/time at which the request was approved/
rejected by the third approver
Approver 3 Comment Remarks entered by approver 3
Approver 3 Email ID Email ID associated with the approver 3
Approver 4 User Name The username of the fourth approver
Approver 4 Status Status of the request by the fourth approver
Approved
Rejected

## [p186]

www.arconnet.com|Copyright © 2025 186
•
•
•
•
•
•
Field Names Description
Approver 4 Status On Date/time at which the request was approved/
rejected by the fourth approver
Approver 4 Comment Remarks entered by approver 4
Approver 4 Email ID Email ID associated with the approver 4
Approver 5 User Name Username of the fifth approver
Approver 5 Status Status of the request by the fifth approver
Approved
Rejected
Approver 5 Status On Date/time at which the request was approved/
rejected by the fifth approver
Approver 5 Comment Remarks entered by approver 5
Approver 5 Email ID Email ID associated with the approver 5
Forwarded to If the request has been forwarded
AdHoc username Name of ad hoc users to whom the request has been
forwarded
AdHoc status Status of the request by ad hoc approver
Approved
Rejected
AdHoc status on Date/time at which the request was approved/
rejected by ad hoc approver
AdHoc comment Remarks entered by ad hoc approver
Final status The final degree of the request
Approved
Rejected
Revoke By Specifies the name of the person who revoked the
service request.
Revoke On Specifies the date and time of the service request
revoked.
Revoke Reason Specifies the reason for the service request being
revoked.

## [p187]

www.arconnet.com|Copyright © 2025 187
1.5.5.3.8.17 Session Activity Log
What is Session Activity Log Report?
The Session Activity Log report displays the logs containing the reasons for switching users in SSH Linux,
Telnet, and SQL Plus. To generate this report, the user needs to select the required information in available
filters and click the View Report button. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Username The name of the user
Domain Name The domain name to which the user belongs
Host Name The hostname of the target server
Port Displays port of the target servers
User Input This is the information about switching user
•
To view this report, users must have the following permission(s):
Session Activity Log

## [p188]

www.arconnet.com|Copyright © 2025 188
Field Names Description
Date Date and time at which the user started the session
activity
Activity Type Type of activity
(For example, Switch User Logs)
1.5.5.3.8.18 Session Log Report
What is Session Log Report?
The Session Log Report displays information about the login and logout time of the services taken by users
based on the filters. To generate this report, the user needs to select the required information in available
filters and click the View Report button. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
•
To view this report, the user must have the following permissions:
Session Log Report

## [p189]

www.arconnet.com|Copyright © 2025 189
The following columns can be seen in this report:
Field Name Description
Sr. No. Specifies the number of rows.
Description Specifies the description of the session log.
Session ID Specifies the session ID.
Service Type Specifies the child’s type of service.
Child Type
Server IP Specify the IP of the service.
Host Name Specifies the hostname of the service.
Service Username Specifies the username of the service.
Username Specifies the username associated with the target
server.
User Machine Details Specifies the machine details of the user.
Connection via Specifies the type of connection of that server.
Total Active Time Specifies the total time of the session when Active.
Total Idle Time Specifies the total time of the session when Idle.
Total Session Lockout Time Specifies the lockout time of the session.
No. of Disconnection Error Specifies the error populated while disconnection of
the session.
Total Duration Specifies the total duration of the session.
Video Log Enable Specifies the status of the video log is enabled or not.
Video Available Specifies the status of the video log is available or not.
Text Log Enabled Specifies the status of the text log is enabled or not.
Text Log Available Specifies the status of the text log is available or not.
Input Log Available Specifies whether the input log is available or not.
Output Log Available Specifies the output log is available or not.
Session Login Time Specifies the session login time of the respective
services.
Session Logout Time Specifies the session logout time of the respective
services.
Log Out Status Specifies the log-out status of the respective service.

## [p190]

www.arconnet.com|Copyright © 2025 190
Field Name Description
Number of Images Taken Specifies the number of images that have been taken
in the session.
Saved Path Specifies the path where captured images have stored
to create video logs.
File Name Specifies the file name of captured images.
Connection Type Specifies the connection type of the respective
service.
View Details Click on view details to see the log of the session as
per time.
1.5.5.3.8.19 Session Wise Summary Report
What is Session Wise Summary Report?
Session Wise Summary Report displays a session-by-session count of activities performed on the server and
service details. To generate this report, the user needs to click the View Report button. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Session-wise Summary Report

## [p191]

www.arconnet.com|Copyright © 2025 191
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Session ID Unique ID associated with each session
Image Log count Total number of images captured in the session
Critical Command The total number of critical commands fired on the
day
Restricted command The total number of restricted commands fired on the
day
Restricted Process Number of restricted processes
Start Time Time at which the session starts
End Time Time at which the session ends
User Log Id Log ID associated with the session
User Id User ID associated with the user
Service Username Username of the service

## [p192]

www.arconnet.com|Copyright © 2025 192
1.5.5.3.8.20 SIEM Command Logs Report
What is SIEM Command Logs Report?
The SIEM Command Logs Report displays logs of commands run on Linux services that are obtained from the
SIEM service. To generate this report, the user needs to click the View Report button. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID ID associated with the user
User Session LogID Log ID associated with each session
User Logged In Date/time of login by user
User Logged Out Date/time of logout by user
IPMAC IPMAC Address of the target server
•
To view this report, users must have the following permission(s)
SIEM Command Logs

## [p193]

www.arconnet.com|Copyright © 2025 193
•
•
Field Names Description
Service Type Name of the service type
Service Description A combination of IP Address, service username,
domain name, hostname, and description
Command Lists the commands fired
Command Time Stamp Date/time when the command was fired
Command Response Captures the response after the command is fired
Service Logged In Date/time when the user logged in to the service
Service Logged Out Date/time when the user logged out from the service
Service Log ID Log ID associated with the service
Password Age Number of days passed until which the password of
the target server was the same
Password Last Changed Date/time of last password change
Password Next Changed Date/time of next password change
Password Status Status of the password
Open
Close
Password Opened By Name of the user who viewed the password
Password Opened Date Date/time at which the password was viewed
1.5.5.3.8.21 SMS and Email Logs
What is SMS and Email Logs?
The SMS and Email Logs report keeps track of failed login attempts on ACMO and records the reasons for
authentication failures where SMS and Mobile are configured as 2FA. To generate this report, the user needs to
select the required information in available filters and click the View Report  button. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
SMS and Email Logs

## [p194]

www.arconnet.com|Copyright © 2025 194
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Source The start point of login failure
Error Type Type of error
Error Message The reason why the authentication failed
Timestamp Date/time at which authentication failed
1.5.5.3.8.22 Ticket Request Workflow Logs
What is Ticket Request Workflow Logs Report?
The Ticket Request Workflow Logs report displays information about all the ticket requests raised by users and
actions taken by the approver on that request. To generate this report, the user needs to select the required
information in available filters and click the View Report button. It can be exported and downloaded in multiple
formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Ticket Request Workflow Logs

## [p195]

www.arconnet.com|Copyright © 2025 195
•
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Ticket ID The unique number associated with every raised
ticket request
LOB/Profile The name of the LOB from which the request was
raised
Ticket Number The unique number associated with the ticket
Ticket Status Status of the ticket
Initiated
Approved
Rejected

## [p196]

www.arconnet.com|Copyright © 2025 196
•
•
•
•
Field Names Description
Ticket Type Name of ticket type
Planned Event (PE)
Changed Request (CR)
Requester Email Id Email ID associated with the user who raised the
request
LOB Workflow Name of the LOB used for creating workflow
User Group Workflow User group for which the workflow is working
Server Group Workflow The server group for which the workflow is working
Priority Priority of the workflow as defined by the
Administrator at the time of the creation
Activity Type Name of Activity type
Service Affecting (SA)
Non-Service Affecting (NSA)
Service Group The server group for which the ticket is raised
Server Domain Name Domain Name of the target server
Server Instance Displays Instances of the target servers
Server Port Displays Port required to connect to the target
servers
Originator Name of the requestor who raised the ticket
Executor Name of the executor who is accessing the ticket
Start Time Date/time from which access is given
End time Date/time until which access is working
Request Date Date/time at which the request was raised
Description Text entered during the creation of that workflow by
the Administrator
Impact Impact on ticket
Impact Location Location of impact
Requested By User Username who raised the request
Current Status Status of the current request

## [p197]

www.arconnet.com|Copyright © 2025 197
•
•
•
•
•
•
Field Names Description
Current Approver Level The latest level of approval
Approver Levels Total number of approval levels in the workflow
Approver 1 Username The username of the first approver
Approver 1 Status Status of the request by the first approver
Approved
Rejected
Approver 1 Status On Date/time at which the request was approved/
rejected by the first approver
Approver 1 Comment Remarks entered by approver 1
Approver 1 Email ID Email ID associated with approver 1
Approver 2 Username The username of the second approver
Approver 2 Status Status of the request by the second approver
Approved
Rejected
Approver 2 Status On Date/time at which the request was approved/
rejected by the second approver
Approver 2 Comment Remarks entered by approver 2
Approver 2 Email ID Email ID associated with approver 2
Approver 3 Username The username of the third approver
Approver 3 Status Status of the request by the third approver
Approved
Rejected
Approver 3 Status On Date/time at which the request was approved/
rejected by the third approver
Approver 3 Comment Remarks entered by approver 3
Approver 3 Email ID Email ID associated with approver 3
Approver 4 Username The username of the fourth approver

## [p198]

www.arconnet.com|Copyright © 2025 198
•
•
•
•
•
•
Field Names Description
Approver 4 Status Status of the request by the fourth approver
Approved
Rejected
Approver 4 Status On Date/time at which the request was approved/
rejected by the fourth approver
Approver 4 Comment Remarks entered by approver 4
Approver 4 Email ID Email ID associated with approver 4
Approver 5 Username Username of the fifth approver
Approver 5 Status Status of the request by the fifth approver
Approved
Rejected
Approver 5 Status On Date/time at which the request was approved/
rejected by the fifth approver
Approver 5 Comment Remarks entered by approver 5
Approver 5 Email ID Email ID associated with approver 5
Final Approver status The final degree of the request
Approved
Rejected
1.5.5.3.8.23 User Access Log Report
What is User Access Log Report?
User Access Log Report displays the users logged into the PAM application in graphical format. The table below
displays additional information, such as the user's login and log-out times. To generate this report, the user
needs to select the required information in available filters and click the View Report  button. It can be
exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User Access Log Report

## [p199]

www.arconnet.com|Copyright © 2025 199
The following columns can be seen in this report:
Field Names Description
Sr. No.' To identify and distinguish rows
LOB/Profile Name of the LOB
User name Name of the user
Display Name The display name of the user
IP Address IP Address of the target server

## [p200]

www.arconnet.com|Copyright © 2025 200
•
•
•
•
•
•
•
Field Names Description
Logged In Date/time of login into the PAM application by the
user
Logged Out Date/time of logout from the PAM application by the
user
User Type Type of user
Client
Admin
Connection Type Type of connection
Direct
Gateway
AGW
1.5.5.3.9 Performance Reports
1.5.5.3.9.1 What is Performance Report?
Performance Reports provide information about the performance of the application. Specifically, Performance
Reports focus on the network user experience. These reports help to visualize how well the application user
experience is displayed in an application performance report.
1.5.5.3.9.2 Why is Performance Report Important?
Understanding the network user experience is crucial because poor performance directly impacts user
satisfaction and productivity. Performance Reports help IT teams quickly identify bottlenecks, detect
anomalies, and take corrective actions to maintain optimal application performance. This proactive monitoring
ensures a smooth and reliable user experience.
The following reports are available in Performance Reports:
MS SQL Connection Report
New Arcon DeskInsight Devices
1.5.5.3.9.3 MS SQL Connection Report
What is MS SQL Connection Report?
The MS SQL Connection Report displays information about all users who have access to the MS SQL instance
on the ARCON | PAM database server. To generate this report, the user needs to click the View Report button.
It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
MS SQL Connection Report

## [p201]

www.arconnet.com|Copyright © 2025 201
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Database Name Name of the database with which the target server is
integrated
User Name The username of the target server
Background Count of background instances
Runnable Count of runnable instances
Sleeping Count of sleeping instances
Suspended Count of suspended instances
1.5.5.3.9.4 New Arcon DeskInsight Devices
What is Arcon DeskInsight Devices Report?

## [p202]

www.arconnet.com|Copyright © 2025 202
•
•
The New Arcon DeskInsight Devices report displays newly added desktops in Windows Active Directory
Organizational Units (OUs). It retrieves information about ARCON | PAM-integrated desktops. To generate
this report, the user needs to select the required information in available filters and click the View Report
button. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The above-mentioned details can be accessed in one of these two ways:
Discovered Devices in Server Manager → Manage
New ARCON DeskInsight Devices report in ACMO
New ARCON PAM DeskInsight Devices report in ACMO
Upon installing the service, update the configurations shown on the screen below in the configuration file.
Then, wait for an hour to fetch the report.
•
To view this report, users must have the following permission(s):
New Arcon DeskInsight Devices

## [p203]

www.arconnet.com|Copyright © 2025 203
•
•
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Host Name Hostname of the target server
Device Type Type of device
Last Discovered By Name of last discovery
Last Discovered On Date/time of last discovery
1.5.5.3.10 Privilege Reports
What are Privilege Reports?
Privilege reports provide information about the permissions that give users the ability to conduct activities in
ARCON | PAM. These reports provide details regarding the data kept in the Privilege Cloud, the Safes, the
users, and the operational links between them. The delegation of power to carry out security-related
operations on a computer system is referred to as a privilege in the field of computing. A privilege enables a
user to take a security-related activity. The ability to create a new user, install software, or modify kernel
functions are a few examples of different privileges. By reviewing the privilege reports users can increase
safety and maintain conformity with regulations.
The following reports are available in Privilege Reports:
Client Manager Privilege Report
Group Admin Privilege Report
Server Manager Privilege Report
User & Services Privileges

## [p204]

www.arconnet.com|Copyright © 2025 204
• User & Services Privileges - Windows RDP
1.5.5.3.10.1 Client Manager Privilege Report
What is Client Manager Privilege Report?
The Client Manager Privilege Report lists and describes all ACMO privileges that have been assigned to users
in graphical and grid view format. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
•
To view this report, users must have the following permission(s):
Client Manager Privilege Report

## [p205]

www.arconnet.com|Copyright © 2025 205
Field Names Description
Display Name The display name of the user
Privilege Group The name of the privilege group to which the privilege
belongs
Privilege The name of the assigned privilege
1.5.5.3.10.2 Group Admin Privilege Report
What is Group Admin Privilege Report?
Group Admin Privilege Report lists and describes all of the ARCON | PAM group admin privileges that have
been assigned to Administrators in graphical and grid view format. To generate this report, the user needs to
select the required information in available filters and click on View Report. It can export and download in
multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Group Admin Privilege Report

## [p206]

www.arconnet.com|Copyright © 2025 206
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Group Name The name of the group to which the privilege belongs
Assigned Privilege The name of the assigned privilege
1.5.5.3.10.3 Server Manager Privilege Report
What is Server Manager Privilege Report?
Server Manager Privilege Report lists and describes all of the ARCON server manager privileges that have
been assigned to Administrators in graphical and grid view format. To generate this report, the user needs to

## [p207]

www.arconnet.com|Copyright © 2025 207
select the required information in available filters and click on View Report. It can export and download in
multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Privilege Group The name of the privilege group to which the privilege
belongs
Assigned Privilege The name of the assigned privilege
•
To view this report, users must have the following permission(s):
Server Manager Privilege Report

## [p208]

www.arconnet.com|Copyright © 2025 208
1.5.5.3.10.4 User & Services Privileges
What is User and Service Privileges?
The User and Services Privileges report lists and describes all of the configuration command privileges that
have been assigned to users and are mapped to the SSH Linux service type in graphical and grid view format. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User and Services Privileges - SSH Linux

## [p209]

www.arconnet.com|Copyright © 2025 209
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
IP Address The IP address of the target server
Host Name The Hostname of the target server

## [p210]

www.arconnet.com|Copyright © 2025 210
Field Names Description
Host username The Host username of the target server
Domain Name The domain name to which that user belongs
Port The port number of the target server
Command List of all the commands mapped to that user
1.5.5.3.10.5 User & Services Privileges - Windows RDP
What is User and Services Privileges - Windows RDP Report?
The User and Services Privileges - Windows RDP report lists and describes all of the command privileges that
have been assigned to users and are mapped to the Windows RDP service type in graphical and grid view
format. To generate this report, the user needs to select the required information in available filters and click
on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User and Services Privileges - Windows RDP

## [p211]

www.arconnet.com|Copyright © 2025 211
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
IP Address The IP address of the target server
Host Name The Hostname of the target server
Host UserName The Host username of the target server
Command List of all the commands mapped to that user
Port The port number of the target server
Domain Name The domain name to which the user belongs

## [p212]

www.arconnet.com|Copyright © 2025 212
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
Field Names Description
Assigned By The Administrator who allocated the commands to
the user
Assigned On Date/time of allocation of command to the user by the
Administrator
1.5.5.3.11 Security Reports
What are Security Reports?
Security Reports give information about the security of ARCON | PAM such as command execution and
restriction, usage of services, service access, and desktop logon made by the user. An organization's cyber risk
posture can be understood and problem areas can be found with the aid of a cyber security report.
Why need Security Reports?
Increased awareness of cyber threats: Reports give a thorough insight into possible dangers and offer
suggestions for better managing these risks.
The following reports are available in Security Reports:
Blacklisted Processes Attempted Report
Commands executed on service session detail report
Critical Commands Executed Report
High Usage (in hrs) Services Report
Invalid Login Attempts Report
Low Usage (in days) Services Report
Multiple Desktop Logon Report
Multiple User Logon Report
Network Segment Wise Logon Report
Restricted Commands Executed Report
Service Access Off Production Hrs Report
Service Accessed – Multiple Times Report
User Service Accessed – Multiple Times Report
1.5.5.3.11.1 Blacklisted Processes Attempted Report
What is Blacklisted Processes Attempted Report?
The Blacklisted Processes Attempted Report is the feature that shows the report of the processes which is
blacklisted by the administrator and the user is attempted to execute. To generate this report, the user needs
to select the required information in available filters and click on View Report. The report will be generated in a
graphical chart as well as a table grid format. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.

## [p213]

www.arconnet.com|Copyright © 2025 213
Refer below table to understand the available fields:
Field Name Description
Sr. No. Specifies the row number
User ID Specifies the user ID name/ number
User Machine Details Specifies the details of the user’s machine
Service Type Specifies the service type
IP Address Specifies the IP address of the service
Process Name Specifies the name of the blacklisted process
Process Title Specifies the title of the blacklisted process
Timestamp Specifies the date and time when the user attempted
the blacklisted process.
1.5.5.3.11.2 Commands Executed Report
What is Command Executed Report?

## [p214]

www.arconnet.com|Copyright © 2025 214
Commands Executed on Service Session Detail Report displays commands executed in a session by the user
while accessing that service. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name The name of the LOB in which there are active
services
Service Type The name of the service type whose session is taken
Service IP Address The IP address of the target server
User ID The User ID associated with the user
User Machine IP The IP address assigned to the user machine
Service User name The username of the service
Domain The domain name of the target server
Hostname The hostname of the target server
Command Details List of commands executed in that session
Logout Status Specify the status of the logout, such as "Manual
logout or forcefully terminated" etc.
•
To view this report, users must have the following permission(s):
Commands Executed on Service Session Detail Report

## [p215]

www.arconnet.com|Copyright © 2025 215
•
•
Field Names Description
Service Logged in Specify the service logged in date.
Service Logged out Specify the service logged out date.
Prompt User Name Specify the name of the prompt user.
1.5.5.3.11.3 Critical Commands Executed Report
What is Critical Command Executed Report?
The Critical Commands Executed Report displays all the critical commands executed by users on the servers in
grid view format. Critical commands are defined by Administrators in the server manager. In addition the bar
graphs display:
Top ten users who fired critical commands.
Top ten IP Addresses from where the critical commands were fired.
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
Critical Commands Executed Report

## [p216]

www.arconnet.com|Copyright © 2025 216
•
•
•
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
IP Address Desktop The IP address of the desktop from where the
command was fired
Service Type The name of the service type where critical commands
were executed
IP Address The IP address of the target server
Service Username The username of the service
DB Instance Instance of the target servers
Command List of commands fired
Command Response Captures the response after the command is fired
Timestamp Date/time when the command was fired
Service Group Name of the service group to which the target server
belongs
1.5.5.3.11.4 High Usage (in hrs) Services Report
What is High Usage Services Report?
The High Usage (in hrs) Services Report displays services that are used a maximum number of times depending
on the time range:
Between 30 - 60 mins
Greater than 1 hour but less than 2 hours
Greater than 2 hours.
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
High Usage (in hrs) Services Report

## [p217]

www.arconnet.com|Copyright © 2025 217
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Type The name of the service type whose usage is displayed
in hours
Service IP The IP address of the target server
Service Username The username of the service
No of times accessed >30 <60 mins Number of times the service was used for a duration
of greater than 30 mins but less than 1 hour
No of times accessed >=1 <2 hours Number of times the service was used for a duration
of greater than or equal to 1 hour but less than 2
hours
No of times accessed >=2 hours Number of times the service was used for a duration
of greater than or equal to 2 hours
1.5.5.3.11.5 Invalid Login Attempts Report
What is Invalid Login Attempts Report?
The Invalid Login Attempts Report displays the number of invalid login attempts faced while logging into
ACMO as well as the reason for the invalid login. To generate this report, the user needs to select the required

## [p218]

www.arconnet.com|Copyright © 2025 218
information in available filters and click on View Report. It can export and download in multiple formats such as
PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Domain The domain name to which the user belongs
Desktop Finger Print Specify the machine details of the user
Module Name Specify the version of the module
User Identified Specify whether the user is identified is PAM
Comment Specify the remarks entered by the administrator
Attempt Number Specify the total number of invalid login attempts
Time Stamp Date/time when the invalid attempt was made
•
To view this report, users must have the following permission(s):
Invalid Login Attempts Report

## [p219]

www.arconnet.com|Copyright © 2025 219
1.5.5.3.11.6 Low Usage (in days) Services Report
What is Low Usage (in days) Services Report?
The Low Usage (in days) Services Report displays the services that were used the least, along with the number
of days they were not used, in graphical and grid format. To generate this report, the user needs to select the
required information in available filters and click on view report. It can export and download in multiple
formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Low Usage (in days) Services Report

## [p220]

www.arconnet.com|Copyright © 2025 220
Field Names Description
Service Type The name of the service type not used for many days
Service IP The IP address of the target server
Service User Name The username of the service
Last Accessed On Date/time on which the service was last used
No. of Days Not Accessed Number of days passed since service was not used
1.5.5.3.11.7 Multiple Desktop Logon Report
What is Multiple Desktop Logon Report?
Multiple Desktop Logon Report displays information about the desktop IP address used by multiple users to log
in to ARCON | PAM in grid view format. Additionally, a bar graph displays the top ten IP user logins. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Multiple Desktop Logon Report

## [p221]

www.arconnet.com|Copyright © 2025 221
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address (Desktop) The IP address of the target server
No. of Users Logon from IP (Desktop) Number of users logged on from that IP
1.5.5.3.11.8 Multiple User Logon Report
What is Multiple User Logon Report?
Multiple User Logon Report displays information about users who logged into ARCON | PAM from various IP
addresses/desktops. Additionally, a bar graph displays the top ten IP user logins. To generate this report, the
user needs to select the required information in available filters and click on View Report. It can export and
download in multiple formats such as PDF, CSV, XLS, and DOC.

## [p222]

www.arconnet.com|Copyright © 2025 222
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
No of IP Address (Desktop) from User Logon Number of desktops used by users to log in
1.5.5.3.11.9 Network Segment Wise Logon Report
What is Network Segment Wise Logon Report?
•
To view this report, users must have the following permission(s):
Multiple User Logon Report

## [p223]

www.arconnet.com|Copyright © 2025 223
The Network Segment Wise Logon Report displays information about all users who have logged into ARCON |
PAM via any network device configured in the Network Segments module of Settings. To generate this report,
the user needs to select the required information in available filters and click on View Report. It can export and
download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
User Display Name The display name of the user
Desktop Finger Print Captures the fingerprint
User IP Address The IP Address of the user logged in
Network Segment Name of the network segment
•
To view this report, users must have the following permission(s):
Network Segment-wise Logon Report

## [p224]

www.arconnet.com|Copyright © 2025 224
•
•
1.5.5.3.11.10 Restricted Commands Executed Report
What is Restricted Commands Executed Report?
Restricted Commands Executed Report displays all the restricted commands entered by users on the servers in
grid view format. Restricted commands are defined by Administrators in the server manager. In addition the
bar graphs display:
Top ten users who entered restricted commands.
Top ten IP Addresses from where the restricted commands were entered.
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Restricted Commands Executed Report

## [p225]

www.arconnet.com|Copyright © 2025 225
The following columns are available in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
IP Address Desktop The IP Address of the User logged in
Service Type Name of the service type
IP Address IP Address of the target server

## [p226]

www.arconnet.com|Copyright © 2025 226
Field Names Description
Service Username The username associated with the target server
DB Instance Instance of the target servers
Command Lists the commands fired
Command Response Captures the response after the command was fired
Timestamp Date/time when the command was fired
1.5.5.3.11.11 Service Access Off Production Hrs Report
What is Service Access off Production Hrs Report?
The Service Access Off Production Hrs Report displays records of users accessing the services during non-
working hours. Working hours are set in start shift time and end shift time by Administrators in Settings. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
Service Access Off Production Hrs Report

## [p227]

www.arconnet.com|Copyright © 2025 227
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Username Name of the user accessing the service
Service Type Name of the service type
Service IP Address IP Address of the target server
Service Username The username associated with the target server
Domain The domain name to which the server belongs
DB Instance Instance of the target servers
Host Name The hostname of the target server
Logged In Time Date/time when the service access started
1.5.5.3.11.12 Service Accessed – Multiple Times Report
What is Service Accessed - Multiple Times Report?
The Service Accessed - Multiple Times Report displays details of all the services accessed multiple times by
users in grid view format. Additionally, a bar graph displays the top ten IP users who accessed the service
numerous times. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Accessed - Multiple Times Report

## [p228]

www.arconnet.com|Copyright © 2025 228
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Type Name of the service type
Service IP Address IP Address of the target server
Service Username The username associated with the target server
DB Instance Displays Instance of the target servers
Service Accessed Number of Times Number of times the service was accessed
1.5.5.3.11.13 User Service Accessed - Multiple Times Report
What is User Service Accessed - Multiple Times Report?

## [p229]

www.arconnet.com|Copyright © 2025 229
The User Service Accessed - Multiple Times Report displays the number of times the user has accessed services
within the defined range. To generate this report, the user needs to select the required information in available
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
User Display Name The display name of the user
No of Times Accessed > 10 < 20 Number of services accessed by the user - greater
than 10 and less than 20 times
No of Times Accessed >= 20 < 40 Number of services accessed by the user - greater
than or equal to 20 and less than 40 times
No of Times Accessed >= 40 Number of services accessed by the user - greater
than or equal to 40 times
•
To view this report, users must have the following permission(s):
User Service Accessed - Multiple Times Report

## [p230]

www.arconnet.com|Copyright © 2025 230
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
•
•
•
•
•
•
•
•
•
1.5.5.3.12 Service Reports
1.5.5.3.12.1 What is Service Report?
A Service Report is used to generate details of the services that are active in ARCON | PAM. In addition, it
generates details of the reference number provided by the user before accessing any service and unique IP
addresses of services. Service reports assist organizations in determining the degree of risk associated with
critical operational and security choices.
1.5.5.3.12.2 Why is Service Report Important?
Service Reports help organizations assess the risk levels related to operational and security decisions. By
offering visibility into which services are active, who accessed them, and from where, these reports support
compliance, auditing, and incident response. This information is critical for managing privileged access and
maintaining secure IT environments.
The following reports are available in Service Reports:
Active Services Report
Active Session Report
AGW Service Access Report
Command Profile Report
Device Detailed Report
DMZ Gateway Report
Lock to Console Report
Multiple Service Reference No. Report
Password Dependency(Actions)
Password Envelope Never Generated Report
Password Envelope Print Report
Password Policy Report
Scheduled Password Change Services
Server Last Accessed On
Servers in Domain
Service Accessed Summary Day Wise Report
Service Accessed Summary Report
Service Application Report
Service audit logs Reports
Services Creation Deletion Details Report
Services Creation Deletion Summary Report
Service Dependency Report
Service Group Wise Service Type Report
Service Timeline Report
Service Assign to AGW Server
Services in Domain Report
Unique Services IP Address Report
1.5.5.3.12.3 Active Services Report
What is Active Services Report?

## [p231]

www.arconnet.com|Copyright © 2025 231
Active Services Report displays information about all ARCON | PAM active services. Active service has not
expired or has a valid till date that is greater than today's date. To generate this report, the user needs to select
the required information in available filters and click on View Report. It can export and download in multiple
formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Active Services Report

## [p232]

www.arconnet.com|Copyright © 2025 232
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows

## [p233]

www.arconnet.com|Copyright © 2025 233
Field Names Description
LOB/Profile The name of the LOB to which the service belongs
Service Type The name of the service type whose session is taken
Service Group The name of the service group to which the service
belongs
IP address The IP address of the target server
Host Name The hostname of the target server
User ID Specify the User ID by which the name service has to
be created
Domain Name The domain name of the target server
DB Instance Displays DB Instance of service
Port The port number of the target server
Description1 Text entered during the creation of that service by the
administrative user
Parameter Specify the parameter of the target server
Last Accessed Time Date-time on which the service was last used
Active Till The date until which the service is active
LOB Status Displays the status of the LOB
Created By The name of the Administrator who created the
service
Created On Date/time of the creation of the service by the
Administrator
1.5.5.3.12.4 Active Session Report
What is Active Session Report?
Active Session Report displays a list of ongoing sessions in ARCON | PAM. To generate this report, the user
needs to select the required information in available filters and click on View Report. It can export and
download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Active Session Report

## [p234]

www.arconnet.com|Copyright © 2025 234
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Server IP The IP address of the target server
User ID The User ID associated with the user
Display Name The display name of the user
Service Type The name of the service type whose session is taken
Service Username The username assigned to the service
Session Source Source of session
1.5.5.3.12.5 AGW Service Access Report
What is AGW Service Access Report?
The AGW (Arcon Gateway) Service Access Report lists all of the users who have connected to the services
using ARCON AGW. To generate this report, the user needs to select the required information in available
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.
•
To view this report, users must have the following permission(s):
AGW Service Access Report

## [p235]

www.arconnet.com|Copyright © 2025 235
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
AGW Name Name of the AGW (Arcon Gateway) server
AGW Description Text entered during the creation of that AGW server
Username The name of the user
IP Address The IP address of the target server
Service User Name The username of the service
Host Name The hostname of the target server
Domain Name The domain name of the target server
Logged In Time Date/time of login
Logout Time Date/time of logout
1.5.5.3.12.6 Command Profile Report
What is Command Profile Report?

## [p236]

www.arconnet.com|Copyright © 2025 236
Command Profile Report will derive all the details of custom command mapping of services. To generate this
report, the user needs to select the required information in available filters and click on View Report. Users can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr.No To identify and distinguish rows.
User ID Unique ID associated with the user.
Display Name The display name of the user.
IP Address Specify the IP address of the target server.
Service User Name Specify the user name of the service.
Service Type Specify the type of the service.
Host Name Specify the name of the host.
Port Specify the port number.
Instance Specify the name of the instance of the target server.
Domain Name Specify the domain name of the target server.
Command Profile Name Specify the name of the command profile.
1.5.5.3.12.7 Device Detailed Report
What is Device Detailed Report?
•
To view this report, users must have the following permission(s)
Command Profile Report

## [p237]

www.arconnet.com|Copyright © 2025 237
The Device Detailed Report assists in locating and viewing a specific service across all LOBs. The user can
search details for multiple IP addresses in the service/server IP filter with comma-separated search queries. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name of the LOB
Service Type The name of the service type
Service Group The server group in which the service belongs
Domain Name The domain name of the target server
•
To view this report, users must have the following permission(s):
Device Detailed Report

## [p238]

www.arconnet.com|Copyright © 2025 238
Field Names Description
IP Address The IP address of the target server
Host name The hostname of the target server
Service Username The user name of the service
Service Mapped to User The user name to which the service is mapped
DB Instance Instance of the target servers
1.5.5.3.12.8 DMZ Gateway Report
What is DMZ Gateway Report?
DMZ Gateway Report will derive the details of DMZ gateway mapping with the services. To generate this
report, the user needs to select the required information in available filters and click on View Report. Users can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr. No To identify and distinguish rows.
IP Address Specify the IP address of the target server.
Service User Name Specify the user name of the service.
Service Type Specify the type of the service.
•
To view this report, users must have the following permission(s)
DMZ Gateway Report

## [p239]

www.arconnet.com|Copyright © 2025 239
Column Name Description
Host Name Specify the name of the host.
Port Specify the port number.
Instance Specify the name of the instance of the target server.
Domain Name Specify the domain name of the target server.
DMZ Gateway IP Address Specify the IP address of the DMZ Gateway.
DMZ Gateway hostname Specify the hostname of the DMZ gateway.
DMZ Gateway User Name Specify the user name of the DMZ gateway.
1.5.5.3.12.9 Lock to Console Report
What is Lock to Console Report?
Lock to Console Report will derive all the details of Lock to Console. To generate this report, the user needs to
select the required information in available filters and click on View Report. Users can export and download in
multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr.No To identify and distinguish rows.
IP Address Specify the IP address of the target server.
•
To view this report, users must have the following permission(s)
Lock to Console Report

## [p240]

www.arconnet.com|Copyright © 2025 240
Column Name Description
Service User Name Specify the user name of the service.
Service Type Specify the type of the service.
Host Name Specify the name of the host.
Port Specify the port number.
Instance Specify the name of the instance of the target server.
Domain Name Specify the domain name of the target server.
LTC IP Address Specify the IP address of Lock to Console (LTC).
LTC Host Name Specify the hostname of Lock to Console (LTC).
LTC User Name Specify the user name of Lock to Console (LTC).
1.5.5.3.12.10 Multiple Service Reference No. Report
What is Multiple Service Reference No Report?
The Multiple Service Reference No. The report displays the reference number provided to the user before
accessing any service in graphical and grid view format. To generate this report, the user needs to select the
required information in available filters and click on View Report. It can export and download in multiple
formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Multiple Service Reference Number Report

## [p241]

www.arconnet.com|Copyright © 2025 241
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name Name of the LOB
User ID The User ID associated with the user
Display Name The display name of the user
IP Address Desktop The IP address of the desktop
Service Type The name of the service type whose session is taken
IP Address The IP address of the target server
Service username The username of the service
DB Instance The instance of the target server
Reference Number The reference number of that service

## [p242]

www.arconnet.com|Copyright © 2025 242
Field Names Description
Reference Number Count Number of times the reference is used
1.5.5.3.12.11 Password Dependency(Actions)
What is Password Dependency (Actions)?
Password Dependency (Actions) report is to consolidate reports for all servers where the services are
configured as dependent on any particular account (or IDs). Users can have pre-actions and post-actions of
active and inactive reports. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Name Description
Sr.No. To identify and distinguish rows
Service IP The IP address of the target server
Host Name The hostname of the target server
Service User Name The username of the service
Service Type The name of the service type
Port The port number of the target server
Domain Name The domain name of the target server
•
To view this report, users must have the following permission(s)
Password Dependency (Actions)

## [p243]

www.arconnet.com|Copyright © 2025 243
Field Name Description
Instance Name The name of the instance
Active Pre Actions Specify Windows services, DCOM, and tasks.
Inactive Pre Actions Specify password dependency under window connections.
Pre Actions Count Specify the total count of pre-actions.
Active Post Actions Specify the action that needs to be executed after the password
change.
Inactive Post Actions Specify the action that should not be executed after the password
change.
Post Actions Count Specify the number of actions created.
1.5.5.3.12.12 Password Envelope Never Generated Report
What is Password Envelope Never Generated Report?
The Password Envelope Never Generated Report displays details of those services for which password
envelopes have never been produced. To generate this report, the user needs to select the required
information in available filters and click on View Report. It can export and download in multiple formats such as
PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Password Envelope Never Generated Report

## [p244]

www.arconnet.com|Copyright © 2025 244
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Type The name of the service type for which a password
was never generated
IP Address The IP address of the target server
Host name The Hostname of the target servers
User ID The User ID associated with the user
Domain Name The domain name to which the target server belongs
for which a password was never generated
DB Instance The instance of the target servers
Port The port number of the target server
Active Till Date until which the service will work
1.5.5.3.12.13 Password Envelope Print Report
What is Password Envelope Print Report?

## [p245]

www.arconnet.com|Copyright © 2025 245
The Password Envelope Print Report displays information about users who have printed password envelopes
and confirmed the process. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Envelope Printed By Name of the user who printed the envelope
First Verifier Name of the first Administrator who verified the print
command before printing the envelope
Second Verifier Name of the second Administrator who verified the
print command before printing the envelope
Number of Services Number of services set for print by the user
Printed On Date/time at which the envelope was printed
•
To view this report, users must have the following permission(s):
Password Envelope Print Report

## [p246]

www.arconnet.com|Copyright © 2025 246
1.5.5.3.12.14 Password Policy Report
What is Password Policy Report?
The Password Policy report displays details of all the password policies that are applied to the active services.
To generate this report, the user needs to select the required information from the available filters and click on
View Report. It can export and download in PDF, CSV, XLS, and DOC formats.
The following columns can be seen in this report:
Column Name Description
Sr.No To identify and distinguish rows
IP Address Specify the IP address of the target server
User Name Specify the name of the user
Service Type Specify the type of the service
Host Name Specify the host name of the target server
Port The port number of the target server
Domain Name The domain name of the target server
DB Instance The instance of the target servers
Password Policy Specify the name of the assigned password policy
1.5.5.3.12.15 Scheduled Password Change Services
What is Scheduled Password Change Services?
•
To view this report, users must have the following permission(s):
Password Policy Report

## [p247]

www.arconnet.com|Copyright © 2025 247
The Scheduled Password Change Services report displays details of all the services that are scheduled for the
password change process. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
•
To view this report, users must have the following permission(s):
Scheduled Password Change Services

## [p248]

www.arconnet.com|Copyright © 2025 248
Field Names Description
Service type Name of the service type
LOB Name The name of the LOB in which passwords are
scheduled for change
Service Group The name of the service group to which the service
belongs
Password Last Changed On Date/time of last password change
Min Password Age Lowest age of the password
Max Password Age Maximum age of the password after which the
password changes
Password Policy Name of the assigned password policy
Scheduled On Date/time when the password was scheduled
1.5.5.3.12.16 Server Last Accessed On
What is Server Last Accessed On?
The Server Last Accessed On report displays records of servers that have not been accessed for a number of
days. The number of days is set in the Days of the server last accessed on configuration by the Administrator in
Settings. To generate this report, the user needs to select the required information in available filters and click
on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s)
Server Last Accessed On

## [p249]

www.arconnet.com|Copyright © 2025 249
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Server IP The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
Last Accessed On Date/time when the server was last used
Days Since Last Accessed The number of days passed since the server was
accessed
1.5.5.3.12.17 Servers in Domain
What is Servers in Domain?
The Servers in Domain report provides information about all the servers in a domain regardless of the LOB in
the graphical and grid View Report. To generate this report, the user needs to click on view report. It can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
To view this report, users must have the following permission(s):

## [p250]

www.arconnet.com|Copyright © 2025 250
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Domain Name The domain name of the target server
IP Address The IP address of the target server
Host Name The hostname of the target server
Instance The instance of the target server
Port The port number of the target server
LOB/Profile The name of the LOB in which the servers are present
1.5.5.3.12.18 Service Accessed Summary Day Wise Report
What is Serviced Accessed Summary Day Wise Report?
The Service Accessed Summary Day Wise Report provides information about the total count of the services
accessed on a daily basis. To generate this report, the user needs to select the required information in available
• Servers in Domain

## [p251]

www.arconnet.com|Copyright © 2025 251
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB/Profile The name of the LOB through which the services are
accessed
Date wise - first date as selected in the filter
(Example- 3rd May 2021)
Total number of services accessed on that day
1.5.5.3.12.19 Service Accessed Summary Report
What is Service Accessed Summary Report?
The Service Accessed Summary Report displays the total number of services accessed by users on a monthly
basis, LOB-wise. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Accessed Summary Day-wise Report

## [p252]

www.arconnet.com|Copyright © 2025 252
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB/Profile The name of the LOB through which the services are
accessed
Date wise - first date as selected in the filter
(Example- Dec 2021)
Total number of services accessed in that month
1.5.5.3.12.20 Service Application Report
What is Service Application Report?
The Service Application Report displays the mapping of all the applications to their service type while
configuring the service. To generate this report, the user needs to select the required information in available
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.
•
To view this report, users must have the following permission(s):
Service Accessed Summary Report
To view this report, users must have the following permission(s):

## [p253]

www.arconnet.com|Copyright © 2025 253
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name The name of the LOB in which the services are
accessed
Service Group The name of the service group to which the service
belongs
IP Address The IP address of the target server
Instance Name The instance of the target servers
Host name The Hostname of the target server
Domain name The domain name to which the target server belongs
Service User Name Specify the user name of the service
Service type The name of the service type
Application Name Names of applications that are mapped to the main
service
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
1.5.5.3.12.21 Service audit logs Reports
What is Service Audit Logs Report?
• Service Application Report

## [p254]

www.arconnet.com|Copyright © 2025 254
Service audit logs reports provide comprehensive details about service activities, including the specific services
accessed, timestamps indicating when access occurred, and the duration of each session. To generate this
report, the user needs to select the required information from the available filters and click on View Report. It
can export and download in PDF, CSV, XLS, and DOC formats.
The following columns can be seen in this report:
Column Name Description
Sr.No To identify and distinguish rows
Service User Name Specify the user name of the service
IP Address Specify the IP address of the target server
Port The port number of the target server
Service Type Specify the type of the service
Operation Action performed at service level:
Create - Creation of service
Modify - Modification of service
Delete - Deletion of service
Domain The domain name of the target server
Host Name The Hostname of the target servers
DB Instance The instance of that target server
•
To view this report, users must have the following permission(s):
Service audit logs Report

## [p255]

www.arconnet.com|Copyright © 2025 255
Column Name Description
Valid Until Specify the date and time until the service is valid
User Lock to Console Used for SSH Linux services to log in to root and allow change of
passwords.
Description 1 Text entered during the creation of the service by the
Administrator.
Description 2
Description 3
Parameter Display the parameter given to the service.
Reference Type Specify the reference type of the request, if entered by the user
while raising the request.
Reference Details Specify the reference details of the request, if entered by the user
while raising the request.
Date Specify the server login date and time
User Name Specify the user name of the service.
1.5.5.3.12.22 Services Creation Deletion Details Report
What is Services Creation Deletion Details Report?
The Services Creation Deletion Details Report informs the user about the creation or deletion of service groups
in ARCON | PAM. To generate this report, the user needs to click on View Report. It can export and download
in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Services Creation Deletion Details Report

## [p256]

www.arconnet.com|Copyright © 2025 256
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Server IP The IP address of the target server
Service User Name Specify the service user name of the target server
Host Name The name of the LOB in which the services are
accessed
Domain Name The domain name to which the target server belongs
Instance Name The instance of the target servers
Port The port number of the target server
OperationTimestamp Specifies the date and time when the service is
created or deleted
Operation Performed Activity performed on the service
Creation
Deletion
1.5.5.3.12.23 Services Creation Deletion Summary Report
What is Services Creation Deletion Summary Report?
The Services Creation Deletion Summary Report displays the total number of services created and deleted on a
date-by-date basis. To generate this report, the user needs to click on View Report. It can export and download
in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Services Creation Deletion Summary Report

## [p257]

www.arconnet.com|Copyright © 2025 257
The following columns are available in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Creation Deletion Date Date/time of service created and deleted
Created The total number of servers created on that day
Deleted The total number of servers deleted on that day
Active Service Count The total number of active servers on that day
1.5.5.3.12.24 Service Dependency Report
What is Service Dependency Report?
The Service Dependency Report displays the details of dependency between mapped applications and their
services. To generate this report, the user needs to select the required information in available filters and click
on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Dependency Report

## [p258]

www.arconnet.com|Copyright © 2025 258
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Parent Service IP address The IP address of the parent server
Parent Service Hostname The Hostname of the parent server
Parent Service Username The username of the parent server
Dependent Service IP The IP address of the dependent server
Dependent Service Hostname The Hostname of the dependent server
Dependent Service Username The username of the dependent server
Dependent Service Type The service type of the dependent server
Dependent Service LOB The service LOB of the dependent server
Dependency Type Specify the type of dependency server

## [p259]

www.arconnet.com|Copyright © 2025 259
Field Names Description
Assigned By Specifies the name of the assignee who has assigned
service
Assigned On Specifies the date and time when the service has
assigned
1.5.5.3.12.25 Service Group Wise Service Type Report
What is Service Group Wise Service Type Report?
The Service Group Wise Service Type Report informs the user about all the service groups in ARCON | PAM
and the services that belong to them. To generate this report, the user needs to click on View Report. It can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Group The name of the service group to which the services
belong
•
To view this report, users must have the following permission(s):
Service Group-wise Service Type Report

## [p260]

www.arconnet.com|Copyright © 2025 260
Field Names Description
Service Type List of all the service types belonging to that service
group
1.5.5.3.12.26 Service Timeline Report
What is Service Timeline Report?
The Service Timeline Report informs the user about the start and termination times of the service. To generate
this report, the user needs to select the required information in available filters and click on View Report. It can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service IP The IP Address of the target server
Start time Date/time captured at the start when accessing the
target server
End time Date/time captured at end of the session
•
To view this report, users must have the following permission(s):
Service Timeline Report

## [p261]

www.arconnet.com|Copyright © 2025 261
1.5.5.3.12.27 Service Assign to AGW Server
What is Service Assign to AGW Server Report?
The Service Assign to AGW Server report lists all of the services mapped to the AGW Server (ARCON
Gateway). To generate this report, the user needs to select the required information in available filters and click
on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The below table shows the information of the table column with its description:
Field Name Description
Sr. No. Specifies the row number.
AGW Configuration Name Specifies the name of the AGW configuration.
Configuration URL Specifies the configuration URL.
LOB Specifies the LOB name of the service belongs.
Service Types Specifies the type of the Services.
Service Name Specifies the name of the services.
Service Group Specifies the name of the service group.
Preference Path Specifies the path where the launching .EXE has
stored.
•
To view this report, users must have the following permission(s):
AGW Service Access Report

## [p262]

www.arconnet.com|Copyright © 2025 262
Field Name Description
Assigned By Specifies the name of the assignee who has assigned
service to AGW server.
Assigned On Specifies the date and time when the service has
assigned to AGW server by the assignee.
1.5.5.3.12.28 Services in Domain Report
What are Services in Domain Report?
The Services in Domain Report informs the user about all the services in a domain in graphical and grid view
format, regardless of the LOB. To generate this report, the user needs to click on View Report. It can export
and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s)
Services in Domain Report

## [p263]

www.arconnet.com|Copyright © 2025 263
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Domain Name The domain name of the target server
Service username The username of the service
IP Address The IP address of the target server
Hostname The hostname of the target server
Instance Instance of the target servers
Port Port number of the target server
LOB/Profile The name of the LOB

## [p264]

www.arconnet.com|Copyright © 2025 264
1.5.5.3.12.29 Unique Services IP Address Report
What is Unique Service IP Address Report?
The Unique Services IP Address Report displays information on all services with unique IP addresses in a
graphical and grid view format. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can export and download in multiple formats such as PDF, CSV,
XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Unique Services IP Address Report

## [p265]

www.arconnet.com|Copyright © 2025 265
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
Field Names Description
Service type The name of the service type
LOB Name The name of the LOB
Host Name The hostname of the target server
IP address The IP address of the target server
Total services The total number of services
Active services The total number of active services
Inactive services The total number of inactive services
1.5.5.3.13 User Reports
1.5.5.3.13.1 What are User Reports?
User reports generate details of all types of users, whether they are active, inactive, dormant, logged out, etc.,
and the activities performed by them. By opening a user report, you can keep track of how vulnerable your
users are to data compromise. The user reports offering a thorough look at the users, how the users share/
access data, and whether they take the necessary security safeguards.
1.5.5.3.13.2 Why are User Reports Important?
User Reports are essential for identifying potential vulnerabilities related to user behavior. By monitoring user
activity and security practices, organizations can detect risky patterns, prevent data compromise, and ensure
compliance with security policies. This helps in strengthening overall access governance and minimizing insider
threats.
The following reports are available in User Reports:
*Active Users Report
Consolidated User & Service Mapping Report
Dormant User Report
Dual Factor Auth Configuration Report
Dual Factor Auth Configuration Report - All LOB
Endpoint Access Control Configuration Report
Idle Users Report
Inactive Users Report
Last Service Accessed Report
Locked Out User Report
User & Service Mapping Report
User Biometric Auth Report
User Biometric Auth Report - All LOB
User Compliance Report

## [p266]

www.arconnet.com|Copyright © 2025 266
•
•
•
•
•
•
•
User Creation Deletion Summary Report
User Dormant in next 5 day Report
User Hardware Auth Report
User Last Logon Report
User Mobile OTP Auth Report
User SMS OTP Auth Report
User Status Report
1.5.5.3.13.3 *Active Users Report
What are Active Users Report?
The Active Users Report displays information about all active users and their type in graphical and grid view
format. An active user has interacted with the PAM application within a certain time period. To generate this
report, the user needs to select the required information in available filters and click on View Report. It can
export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s)
Active Users Report

## [p267]

www.arconnet.com|Copyright © 2025 267
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Domain The domain name to which the user belongs
User Valid till Date until which the user will be active
User Type Type of user
Client
Admin
User Group Specify the user group name that the user is part of.

## [p268]

www.arconnet.com|Copyright © 2025 268
Field Names Description
Created By The name of the Administrator who created the user
Email Id Email address of the user as configured by the
Administrator
Mobile Number The mobile number of the user as configured by the
Administrator
Active Duration Total time duration since the user is active
Description 1 Text entered during the creation of the service by the
Administrator
Description 2 Text entered during the creation of the service by the
Administrator
Description 3 Text entered during the creation of the service by the
Administrator
Created On Date/time of the creation of the user by the Administrator
1.5.5.3.13.4 Consolidated User & Service Mapping Report
What is Consolidated User & Service Mapping Report?
The Consolidated User & Service Mapping Report displays the total count of each service type linked to the
user. To generate this report, the user needs to select the required information in available filters and click on
View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Consolidated User & Service Mapping Report

## [p269]

www.arconnet.com|Copyright © 2025 269
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Service Type The name of the service type
User Group The name of the user group to which the user belongs
Total Services Count The total of all the services of a particular service type
mapped to the user
1.5.5.3.13.5 Dormant User Report
What is Dormant User Report?
The Dormant User Report displays information about all the dormant users in ARCON | PAM. A dormant user
has not interacted with the PAM application in a certain period of time (specified in the User Dormancy Alert -

## [p270]

www.arconnet.com|Copyright © 2025 270
•
•
Schedule Days configuration in global configuration). To generate this report, the user needs to select the
required information in available filters and click on View Report. It can export and download in multiple
formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Username The name of the user
Display Name The display name of the user
Domain The domain name to which the user belongs
LOB The name of the LOB in which the user is present
User Email ID Specify the email ID of the user
Mobile Number Specify the mobile number of the user
User Type Type of user
Client
Admin
Last Login Date/time when the user last logged in
Valid Till Date until which the user will be active
User Group The name of the user group to which the user belongs
•
To view this report, users must have the following permission(s):
Dormant User Report

## [p271]

www.arconnet.com|Copyright © 2025 271
Field Names Description
Dormant On Displays the timestamp when a user becomes
dormant.
1.5.5.3.13.6 Dual Factor Auth Configuration Report
What is Dual Factor Authentication Report?
Dual Factor Auth Configuration Report displays information of all the users and the status (enabled,
configured, not configured, etc.) of each dual-factor authentication configuration to make the ACMO login
process more secure. To generate this report, the user needs to select the required information in available
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The user ID associated with the user
Display Name The display name of the user
Email ID Displays the email ID of the user
•
To view this report, users must have the following permission(s):
Dual Factor Auth Configuration Report

## [p272]

www.arconnet.com|Copyright © 2025 272
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
Field Names Description
Email OTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Email OTP Configured on Date/time when email 2FA was configured
Mobile No Mobile number of the user configured by the
Administrator
Mobile OTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Mobile OTP Configured On Date/time when mobile OTP was configured
RSA secure ID Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
RSA secure ID Configured On Date/time when RSA secure ID 2FA was configured
Biometric Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Biometric Configured On Date/time when biometric 2FA was configured
SMS OTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
SMS OTP Configured On Date and time when SMS OTP was configured
TOTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled

## [p273]

www.arconnet.com|Copyright © 2025 273
Field Names Description
TOTP Configured On Date and time when TOTP was configured
1.5.5.3.13.7 Dual Factor Auth Configuration Report - All LOB
What is Dual Factor Auth Configuration Report - All LOB?
The Dual Factor Auth Configuration Report - All LOB display reports for the users who have configured the
dual-factor authorization across all LOBs to make the login process more secure. To generate this report, the
user needs to select the required information in available filters and click on View Report. It can export and
download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Email ID Email ID of the user
Mobile No. Mobile number of the user configured by the
Administrator
•
To view this report, users must have the following permission(s):
Dual Factor Auth Configuration Report - All LOB

## [p274]

www.arconnet.com|Copyright © 2025 274
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
Field Names Description
Mobile OTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Mobile OTP Configured on Date/time when mobile OTP was configured
RSA Secure ID Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
RSA Secure ID Configured on Date/time when RSA secure ID 2FA was configured
Biometric Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Biometric Configured on Date/time when biometric 2FA was configured
SMS OTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
SMS OTP Configured on Date/time when SMS OTP was configured
TOTP Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
TOTP Configured on Date/time when TOTP was configured
1.5.5.3.13.8 Endpoint Access Control Configuration Report
What is Endpoint Access Control Configuration Report?
This report contains data on Endpoint Based Access Control setting configured against all the active PAM
users. This report will give information about the details of the Endpoint through which the active users are
allowed to access PAM. To generate this report, the user needs to select the required information in available
filters and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and
DOC.

## [p275]

www.arconnet.com|Copyright © 2025 275
The following columns can be seen in this report:
Column Name Description
Sr.No To identify and distinguish rows
User ID The User ID associated with the user
Domain Name The domain name to which the user belongs
Is Endpoint Access Control Enabled Displays whether Endpoint Access Control is enabled or
disabled
Is Endpoint Access Control Configured Displays whether Endpoint Access Control is configured or
not configured
Endpoint Access Control Filter Type Configure the endpoint access control filter type
Is Filter Type Active Displays whether the filter type is active or inactive
Endpoint Details Displays the machine details of the endpoint
1.5.5.3.13.9 Idle Users Report
What is Idle Users Report?
The Idle Users Report displays information on all idle users who do not belong to user and service groups in
ARCON | PAM. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Idle Users Report

## [p276]

www.arconnet.com|Copyright © 2025 276
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name The name of the LOB to which the idle user belongs
Username The name of the user
Display name The display name of the user
Domain name The domain name to which that user belongs
Last Logon Date/time when the user last logged in
Not Logon Since Days Number of days since passed since the last login
User status Status of the user
Active
Inactive

## [p277]

www.arconnet.com|Copyright © 2025 277
•
•
1.5.5.3.13.10 Inactive Users Report
What is Inactive Users Report?
Inactive Users Report informs the user about all inactive users in ARCON | PAM. To generate this report, the
user needs to select the required information in available filters and click on View Report. It can export and
download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Domain The domain name to which the user belongs
User Valid Till Date until which the user will be active
User Email ID Displays the email ID of the user
Mobile Number Displays the mobile number of the user
User Type Type of user
Client
Admin
Created By The name of the Administrator who created the user
•
In order to view this report, users must have the following permission(s):
Inactive Users Report

## [p278]

www.arconnet.com|Copyright © 2025 278
Field Names Description
Created On Date/time of the creation of the user by the
Administrator
Active Duration Displays the active duration of the user
1.5.5.3.13.11 Last Service Accessed Report
What is Last Service Accessed Report?
The Last Service Accessed Report displays information about users and the last time they accessed that service.
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
Last Service Accessed Report

## [p279]

www.arconnet.com|Copyright © 2025 279
•
•
Field Names Description
Sr. No. To identify and distinguish rows
LOB Displays the name of the LOB
User Display Name The display name of the user
Username The name of the user
User Domain The domain name in which the user belongs
Service Host Displays the service host address
User Type Type of user
Client
Admin
Service IP Address The IP Address of the target server used last
Service Username The username of the service
Host Name Displays the host name of the service
Service Domain Displays the service domain name
Service Type Displays the type of the service
Number of days from last Access Displays the number of days that the service was last accessed.
Service Logged In Time Date/time of the last login to the service
1.5.5.3.13.12 Locked Out User Report
What is Locked Out User Report?
The Locked Out User Report displays users who attempted to log in with an invalid password and exceeded the
lockout attempts value defined in Settings. Such users get their ID gets locked and added to the Lockout Users
List under Manage Users. They are not able to log into ARCON | PAM even with the correct password. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can export and download in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Locked Out User Report

## [p280]

www.arconnet.com|Copyright © 2025 280
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Username The name of the user
Display Name The display name of the user
Domain The name of the domain
LOB The name of the LOB
User Type Type of user
Admin
Client
Last Login Date/time when the user last logged in
Valid Till Date until which the user will be active
1.5.5.3.13.13 User & Service Mapping Report
What is User & Service Mapping Report?
The User & Service Mapping Report displays information about users and services that are mapped to the user
and service groups, LOB-wise. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.

## [p281]

www.arconnet.com|Copyright © 2025 281
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
•
To view this report, users must have the following permission(s):
User & Service Mapping Report

## [p282]

www.arconnet.com|Copyright © 2025 282
•
•
•
Field Names Description
Display Name The display name of the user
User Group The name of the user group to which the user belongs
Service Type The name of service type
IP Address The IP address of the target server
Host Name The hostname of the target server
Service Username The username of the service
DB Instance Instance of the target server
Service Assigned By Displays the name by whom the service was assigned
to the user
Service Assigned on Date/time of assignment of the service to the user
Request Type Type of access
Permanent
Time-based
One-time
Config Command Restriction Type The restricted command for that target server
Service Group The name of the service group to which the server
belongs
1.5.5.3.13.14 User Biometric Auth Report
What is User Biometric Auth Report?
User Biometric Auth Report displays information about all the users and the status (enabled, configured, not
configured, etc) of biometric dual-factor authentication to make the ACMO login process more secure. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User Biometric Auth Report

## [p283]

www.arconnet.com|Copyright © 2025 283
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
Email ID The email ID of the user as configured by the
Administrator
Mobile No The mobile number of the user as configured by the
Administrator

## [p284]

www.arconnet.com|Copyright © 2025 284
•
•
•
Field Names Description
Is Configured Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Configured By Name of the user who configured the 2FA biometric
Configured On Date/time when biometric 2FA was configured
1.5.5.3.13.15 User Biometric Auth Report - All LOB
What is User Biometric Auth Report - All LOB?
User Biometric Auth Report - ALL LOB display reports for the users who have configured the biometric
authorization to make the login process more secure across all LOBs. To generate this report, the user needs to
select the required information in available filters and click on View Report. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
User Biometric Auth Report - All LOB

## [p285]

www.arconnet.com|Copyright © 2025 285
•
•
•
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name Name of the LOB
User ID The User ID associated with the user
Display Name The display name of the user
Email ID The email ID of the user as configured by the
Administrator
Mobile No The mobile number of the user as configured by
Administrator
Is Configured Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Configured By Name of the user who configured the 2FA biometric
Configured On Date/time when biometric 2FA was configured
1.5.5.3.13.16 User Compliance Report
What is User Compliance Report?
The User Compliance Report shows the user's status (Active/Inactive) and whether or not multi-factor
authentication has been activated. To generate this report, the user needs to click on View Report. It can be
exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User Compliance Report

## [p286]

www.arconnet.com|Copyright © 2025 286
•
•
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The User ID associated with the user
Display Name The display name of the user
User Status Status of the user
Active
Inactive
MFA Status Status of multi-factor authentication
Enabled
Disabled
Last Logon Date/time when the user last logged in
Duplicate access to multiple user group Whether the user has duplicate access to multiple
user groups or not
1.5.5.3.13.17 User Creation Deletion Summary Report
What is User Creation Deletion Summary Report?
The User Creation Deletion Summary Report gives the total cumulative count of users created and deleted
date-wise until a particular date. To generate this report, the user needs to click on View Report. It can be
exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.

## [p287]

www.arconnet.com|Copyright © 2025 287
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Creation Deletion Date Date/time of user was created and deleted
Created Displays the total number of users created on that day
Deleted Displays the total number of users deleted on that day
Active User Count Displays the total number of users active users
1.5.5.3.13.18 User Dormant in next 5 day Report
What is User Dormant Report?
The User Dormant in next 5 day Report displays users whose accounts are about to go dormant in the next five
days. Dormancy days are configured in Application Configuration under Settings. To generate this report, the
user needs to click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV,
XLS, and DOC.
•
To view this report, users must have the following permission(s):
User Creation Deletion Summary Report
•
To view this report, users must have the following permission(s):
User Dormant in next 5 day Report

## [p288]

www.arconnet.com|Copyright © 2025 288
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Username The name of the user
Display Name The display name of the user
Domain The domain name to which the user belongs
LOB The name of the LOB in which the user is present
User Type Type of user
Client
Admin
Last Login Date/time when the user last logged in
Valid Till Date until which the user will be active
1.5.5.3.13.19 User Hardware Auth Report
What is User Hardware Auth Report?
User Hardware Auth Report displays information of all the users and the status (enabled, configured, not
configured, etc.) of the user hardware tool as dual-factor authentication to make the ACMO login process more
secure. To generate this report, the user needs to select the required information in available filters and click on
View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.

## [p289]

www.arconnet.com|Copyright © 2025 289
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The user ID associated with the user
Display Name The display name of the user
Email ID The email ID of the user as configured by the
Administrator
•
To view this report, users must have the following permission(s):
User Hardware Auth Report

## [p290]

www.arconnet.com|Copyright © 2025 290
•
•
•
Field Names Description
Mobile No Mobile number of the user as configured by the
Administrator
Is configured Status of configuration
Not configured yet
Configured but not enabled
Configured
Configured By The name of the Administrator who configured this
authentication
Configured On Date/time when the user hardware authentication
was configured
1.5.5.3.13.20 User Last Logon Report
What is User Last Logon Report?
The User Last Logon Report displays when a user last logged into the ARCON | PAM application. To generate
this report, the user needs to select the required information in available filters and click on View Report. It can
be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
User Last Logon Report

## [p291]

www.arconnet.com|Copyright © 2025 291
Refer to the below table for detailed information:
Field Names Description
Sr. No. To identify and distinguish rows
LOB Name The name of the LOB
Username The name of the user
Display Name The display name of the user
Domain Name The domain name to which the user belongs
Last Logon Date/time of the last login by that user into the
application
Not logon Since Days Number of days passed since the last login
1.5.5.3.13.21 User Mobile OTP Auth Report
What is User Mobile OTP Auth Report?
The User Mobile OTP Auth Report displays information of all the users and the status (enabled, configured, not
configured, etc.) of Mobile OTP as dual-factor authentication to make the ACMO login process more secure. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.

## [p292]

www.arconnet.com|Copyright © 2025 292
•
•
•
The following columns are available in this report:
Field Names Description
Sr No. To identify and distinguish rows
User ID The user ID associated with the user
Display Name The display name of the user
Email ID The email ID of the user as configured by the
Administrator
Is Configured Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Configured By Name of the user who configured the Mobile OTP
2FA
Configured On Date/time when mobile OTP was configured
•
To view this report, users must have the following permission(s)
User Mobile OTP Auth Report

## [p293]

www.arconnet.com|Copyright © 2025 293
1.5.5.3.13.22 User SMS OTP Auth Report
What is User SMS OTP Auth Report?
User SMS OTP Auth Report displays information of all the users and the status (enabled, configured, not
configured, etc) of SMS OTP as dual-factor authentication to make the ACMO login process more secure. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User ID The user ID associated with the user
Display Name The display name of the user
Email ID The email ID of the user as configured by the
administrative user
•
To view this report, users must have the following permission(s):
User SMS OTP Auth Report

## [p294]

www.arconnet.com|Copyright © 2025 294
•
•
•
Field Names Description
Is Configured Status of configuration
Not configured yet
Configured but not enabled
Configured and enabled
Mobile No Mobile number of the user as configured by the
Administrator
Configured By Name of the user who configured the SMS OTP 2FA
Configured On Date/time when SMS OTP was configured
1.5.5.3.13.23 User Status Report
What is User Status Report?
The User Status Report displays a history of a user's status, such as when they were dormant, locked out, or
disabled, and when they became active again. To generate this report, the user needs to select the required
information in available filters and click on  View Report. It can be exported and downloaded in multiple
formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User Name Displays the name of the user
•
To view this report, users must have the following permission(s):
User Status Report

## [p295]

www.arconnet.com|Copyright © 2025 295
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
Field Names Description
User ID Displays user ID of the user
Creation Date Displays the Date/time of user was created.
Current Status Displays the current status of the user
No_of_Times Number of times the status of the user changed
LOB The name of the LOB
User Group The name of the user group to which the user belongs
1.5.5.3.14 Vault Reports
1.5.5.3.14.1 What are Vault Reports?
The vault is the secure storage space for all the passwords in ARCON | PAM, where the users' and services'
passwords are saved. Vault reports generate details of all the password activities performed in ARCON | PAM.
Vault reports offer tailored reports to assist in controlling each user's access to vital corporate credentials. To
get rid of weak passwords throughout the organization, you can study all reports and create the appropriate
password regulations.
1.5.5.3.14.2 Why are Vault Reports Needed?
Vault Reports are essential for enforcing strong password policies and safeguarding critical credentials. They
help organizations monitor password hygiene, identify weak or reused passwords, and ensure that access to
sensitive data is controlled and compliant with security standards. By analyzing these reports, administrators
can implement effective password regulations and minimize the risk of unauthorized access.
The following reports are available in Vault Reports:
Allow Password Change Report
Credentials Accessed via API Report
Current Password Status Report
Maximum Password Failed Attempts Report
Restore Service Password Option Used
Service Consolidated Vault Status Report
Service Last Password Failed Reason
Service Password Age Report
Service Password Change Consolidated Report
Service Password Change Failed (Server Unavailable) Report
Service Password Changed Status Report
Service Password Changed Status Report - All LOB
Service Password Changed Success/Failed Report
Service Password Check Out Report
Service Password Envelope Print Status Report
Service Password Expires in 5 Days Report
Service Password Manually Changed Report
Service Password Never Changed Report

## [p296]

www.arconnet.com|Copyright © 2025 296
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
Service Password Never Changed Report - All LOB
Service Password Security Status Report
Service Password Vaulting Status
Service Password Vaulting Summary Report
Service Password Viewed By Administrator
Service Reached Maximum Failed Attempts
Service Reconcile Status Report
Services Details for SPC - Maximum Failed Attempts
Services Scheduled for SPC
SPC Not Configured Report
SPC Success and Failed Report
Users Extracting Password Envelope Report
1.5.5.3.14.3 Allow Password Change Report
What is Allow Password Change Report?
The Allow Password Change Report displays information on the services for which password change is allowed.
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Allow Password Change Report

## [p297]

www.arconnet.com|Copyright © 2025 297
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP Address of the target server
Host Name The hostname of the target server
Username The name of the user
DB Instances The instance of the target server
Service Type Name of the service type
Group Name Name of the server group to which the server belongs
Min. Password Age Minimum age set for the password to be valid
Max. Password Age Maximum age set for the password to be valid
Current Password Age The current age of the password set
Last Password Changed On The last date when the password was changed
Password Expired On The date for when the password expires

## [p298]

www.arconnet.com|Copyright © 2025 298
1.5.5.3.14.4 Credentials Accessed via API Report
What is the Credentials Accessed via API Report?
The Credentials Accessed via API Report provides visibility into all credentials accessed through APIs in the
Password Vault system. To generate this report, the user needs to select the required information in the
available filters and click View Report. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
The following columns can be seen in this report:
Column Name Description
Sr. No. The serial number indicates the order of entries in the report.
IP Address The IP Address of the target server
Username The username for which the credentials were accessed via API.
•
To view this report, users must have the following permission(s):
Credentials Accessed via API Report

## [p299]

www.arconnet.com|Copyright © 2025 299
Column Name Description
Host Name The hostname of the target server
Service Type The type of service accessed (e.g., SSH LINUX, Windows RDP).
Domain Name The domain associated with the accessed account.
Instances The instance of the target server
Port The port number used for the connection
LOB Name The access associated with a specific Line of Business
Server Group Name Name of the server group to which the server belongs
Accessed On Timestamp when the credential was accessed.
Accessed By Specifies the API username or system API that initiated the access request.
SourceMachineDetails Information about the machine that made the API request.
NonInteractiveUsername It displays the user name of the API.
1.5.5.3.14.5 Current Password Status Report
What is the Current Password Status Report?
The Current Password Status Report displays the current password status (open/closed) of all services. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Current Password Status Report

## [p300]

www.arconnet.com|Copyright © 2025 300
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance Displays instance of the target servers
Port Displays port connecting to the target server
Service type Name of the service type
Changed By Name of the Administrator who changed the
password

## [p301]

www.arconnet.com|Copyright © 2025 301
•
•
•
•
•
•
Field Names Description
Changed On Date/time of password change
Max Password Age Maximum age of password after which the password
changes
Current Password age The present age of the password
Current Password Status Status of password
Open
Closed
Account Status Status of the service account
Enabled
Disabled
Last Accessed Time Date/time when the service was last used
Auto Schedule If password change will happen automatically
Enabled
Disabled
Failure Reason Steps captured during the password change
1.5.5.3.14.6 Maximum Password Failed Attempts Report
What is Maximum Password Failed Attempts Report?
The Maximum Password Failed Attempts Report displays all the services for which the scheduled password
change has been terminated due to exceeding the maximum number of failed attempts. The maximum number
of failed attempts is specified in the Scheduled Password Change - Maximum Failed Attempt in Settings. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Maximum Password Failed Attempts Report

## [p302]

www.arconnet.com|Copyright © 2025 302
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Count Number of times the password change failed
Service ID The ID associated with the target server
IP Address The IP address of the target server
Host Name The hostname of the target server
Domain name The domain name of the target server
User Name The name of the user
DB Instance Instance of the target server
Service type Name of the service type
Service Group Name of the service group to which the server
belongs
Last Password Changed By Name of the user who changed the password last
1.5.5.3.14.7 Restore Service Password Option Used
What is Restore Service Password Option Used?
The Restore Service Password Option Used report displays the list of users who used the Restore Service
Password option. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and
DOC.

## [p303]

www.arconnet.com|Copyright © 2025 303
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
User Name The name of the user
Server IP The IP address of the target server
Server Host The hostname of the target server
Domain name The domain name of the target server
Port Port of the target server
Description Step at which restore service password was used
Restore Date Date/time at which the service was restored
Credential type It displays the type of credentials such as “password“
1.5.5.3.14.8 Service Consolidated Vault Status Report
What is Service Consolidated Vault Status Report?
The Service Consolidated Vault Status Report displays the complete status report of service vaults. To
generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Restore Service Password Option Used
To view this report, users must have the following permission(s):

## [p304]

www.arconnet.com|Copyright © 2025 304
The below table describes the field information of this report:
Field Name Description
Sr. No. Specifies the row number.
LOB Specifies the name of LOB which is belongs to that particular server.
Service IP The IP address associated with the target server.
• Service Consolidated Vault Status Report

## [p305]

www.arconnet.com|Copyright © 2025 305
•
•
•
Field Name Description
Host Name Specifies the host name of respective service.
Privilege ID (Service Username) Specifies the name of the service user.
Domain Specifies the name of the domain.
Service Instance Specifies the instance of the target servers
Port Specifies the port number of the target server.
Service Type Specifies the type of service.
Service Group Specify the name of the service group.
Allow Password Change Specify wheater the password change feature enabled or not.
Allow Schedule Password
Change
Specifies the status of Allow Schedule Password Change Has enable or not.
First Successful Password
Change by SPC
Specifies the date and time when the password has changed for the very
first time by SPC.
Last Password Changed By Specifies the name of the user who has change last password manually.
Password Last Changed On Specifies the date and time of recent password change.
Current Password Age Specifies the count of days are remaining to rotate the password
automatically.
Min Password Age Specifies the minimum age of password after which the password changes.
Max Password Age Specifies the maximum age of password after which the password changes.
Allow Auto Heal Specifies the auto heal feature is enabled or not.
Vault Status Specifies the status of the vault as below:
Manually Vaulted
Vaulted
Not Vaulted
APC Error Specifies if APC error found.
Auto Heal Triggered During Last
Password Change
Specifies whether auto heal is triggered during last password change or not.
AutoHeal Error Specify a failure in the system's automated recovery processes meant to
maintain service health and stability.
Custom Command Specifies if any commands are fired on the server.
Password Next Change Date Specifies the date/time of next password change.

## [p306]

www.arconnet.com|Copyright © 2025 306
Field Name Description
LTC Service IP Specify the IP of the LTC Service.
LTC User Name Specify the username of the LTC Service.
Password Open By Specify the name of the user who opens the password.
Password Open For Hours Specify the time for which you want the password to remain open.
Password Open On Specify the date when the password was open
Password Open Till Specify the date and time until when the password is open for use.
Dependancy Service Specifies the type of dependancy service.
Password Failed Attempts
(After last Success)
Specifies the number of unsuccessful login attempts made after the most
recent successful login.
Description 1 Specifies the text entered during the creation of the service by the
Administrator.
Description 2 Specifies the text entered during the creation of the service by the
Administrator.
Description 3 Specifies the text entered during the creation of the service by the
Administrator.
1.5.5.3.14.9 Service Last Password Failed Reason
What is Service Last Password Failed Reason?
The Service Last Password Failed Reason report displays the reason for the failure of the password change for
each service type. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and
DOC.
•
To view this report, users must have the following permission(s):
Service Last Password Failed Reason Report

## [p307]

www.arconnet.com|Copyright © 2025 307
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB/Profile The name of the LOB to which the service belongs
Service Type Name of the service type
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
Domain Name The domain name of the target server
Port Port of the target server
SPH Started By Steps captured of why the password change failed
Timestamp Date and time of the last service password change
Error Log Steps captured of why the password change failed
1.5.5.3.14.10 Service Password Age Report
What is Service Password Age Report?
The Service Password Age Report displays the password's age for each service, which is the number of days the
password has been active in ARCON | PAM, in graphical and grid view format. In addition, the bar graphs
display:
Group name-wise service count
Password age bucketing

## [p308]

www.arconnet.com|Copyright © 2025 308
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
•
To view this report, users must have the following permission(s):
Service Password Age Report

## [p309]

www.arconnet.com|Copyright © 2025 309
Field Names Description
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Max Password Age Maximum age of password - after this the password
changes
Current Password Age Age of the current password
Group Name Name of the group to which the server belongs
Credential Type It displays the type of credentials such as “password“
1.5.5.3.14.11 Service Password Change Consolidated Report
What is Service Password Change Consolidated Report?
Service Password Change Consolidated Report displays the consolidated information of the password changes
for the different services. To generate this report, the user needs to click on View Report. It can be exported
and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission
Service Password Change Consolidated Report

## [p310]

www.arconnet.com|Copyright © 2025 310
The following columns are available in the report:
Field Names Description
Sr. No To identify and distinguish rows
IP Address The IP Address of the target server
Host Name The hostname of the target servers
Password Changed By The username of the user that changed the password
Status The status of the password change, if it was a success
or a failure
Failure Reason The reason for which the password change failed for
Password Change Attempt The date on which the password changed was
attempted
Last Successful Password Change The last date on which the password change was
successful

## [p311]

www.arconnet.com|Copyright © 2025 311
1.5.5.3.14.12 Service Password Change Failed (Server Unavailable) Report
What is Service Password Change Failed Report?
The Service Password Change Failed (Server Unavailable) Report displays all the services that have had their
password changes fail due to server downtime. To generate this report, the user needs to select the required
information in available filters and click on View Report. It can be exported and downloaded in multiple
formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Change Failed (Server Unavailable) Report

## [p312]

www.arconnet.com|Copyright © 2025 312
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows

## [p313]

www.arconnet.com|Copyright © 2025 313
•
•
Field Names Description
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Service Type Name of the service type
Changed By Name of the Administrator who changed the
password
Changed On Date/time at which the password was changed
Current Status Present status of the password
Open
Closed
Error Description It displays the description for password failure
Error Reason It displays the reason for password failure
Credential Type It displays the type of credential such as “Password“
1.5.5.3.14.13 Service Password Changed Status Report
What is Service Password Changed Status Report?
The Service Password Changed Status Report displays services that have had their passwords successfully
changed since they were created. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Changed Status Report

## [p314]

www.arconnet.com|Copyright © 2025 314
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
Last Successful Password Changed By Name of the Administrator who changed the last
password successfully
Last Successful Password Changed On Date/time at which the last password was changed
Last Successful Password Changed Through The method by which the last password was changed

## [p315]

www.arconnet.com|Copyright © 2025 315
•
•
Field Names Description
No. of Successful Password Changes Total number of successful password changes
Current status Present status of the password
Open
Closed
Credential Type It displays the type of credentials such as “password“
1.5.5.3.14.14 Service Password Changed Status Report - All LOB
What is Service Password Changed Status Report - All LOB?
The Service Password Changed Status Report - All LOB display details of all the services whose passwords have
been successfully changed since the service was created across all LOBs. To generate this report, the user
needs to select the required information in available filters and click on View Report. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Changed Status Report-All LOB

## [p316]

www.arconnet.com|Copyright © 2025 316
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
Username The name of the user of the target server
DB Instance Displays the instance of the target server
Service Type Displays the type of the service of the target server
Last Successful Password Changed By Name of the Administrator who changed the last
password successfully
Last Successful Password Changed On Date/time at which the last password was changed
Last Successful Password Changed Through The method by which the last password was changed

## [p317]

www.arconnet.com|Copyright © 2025 317
•
•
Field Names Description
No. of Successful Password Changes Total number of successful password changes
Current Status Present status of the password
Open
Closed
1.5.5.3.14.15 Service Password Changed Success/Failed Report
What is Service Password Changed Success/Failed Report?
The Service Password Changed Success/Failed Report displays if the password change is successful or failed
for all services. To generate this report, the user needs to select the required information in available filters and
click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service Name of the service type
•
To view this report, users must have the following permission(s):
Service Password Changed Success Failed Report

## [p318]

www.arconnet.com|Copyright © 2025 318
•
•
•
•
Field Names Description
Host Name The hostname of the target server
Service IP The IP address of the target server
User Name The name of the user
Domain Name The domain name of the target server
Start Date Date/time at which the password was changed
Status Status of the password change
Success
Failed
Credential Type It displays the type of credentials such as “password“
1.5.5.3.14.16 Service Password Check Out Report
What is Service Password Check Out Report?
The Service Password Check Out Report displays details of users who have requested to view the service
password for a specified amount of time in graphical and grid view format. In addition, the bar graph displays:
Group-wise Password Viewed Report
Current Status-wise Count
To generate this report, the user needs to select the required information in available filters and click on View
Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Check Out Report

## [p319]

www.arconnet.com|Copyright © 2025 319
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Request Number The unique number associated with each service
password raised request
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server

## [p320]

www.arconnet.com|Copyright © 2025 320
•
•
•
•
Field Names Description
Service Type Name of the service type
Password viewed by Name of the user who viewed the password
Description Text entered while viewing the password
Open for Hours Number of hours the password remains open
Open Till Date/time till which the password remains open
Authentication 1 Name of approver 1
Authentication 2 Name of approver 2
Authentication 3 Name of approver 3
Authentication 4 Name of approver 4
Authentication 5 Name of approver 5
Approver Name of final approver who approved the request
Password Viewed On Date/time at which the password was viewed
View Status If the password is viewed
Open
Closed
Current Status Present status of the password
Open
Closed
Group Name Name of the server group to which the server belongs
Credentials Type It displays the type of credentials such as “password“
1.5.5.3.14.17 Service Password Envelope Print Status Report
What is Service Password Envelope Print Status Report?
The Service Password Envelope Print Status Report displays the print status of all the services for which the
password envelope was created. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Envelope Print Status Report

## [p321]

www.arconnet.com|Copyright © 2025 321
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB The name of the LOB to which the service belongs
Service Host The hostname of the target server
Service User Name The name of the user
Domain The domain name of the target server
Instance The Instance of the target servers
Service Port Port of the target servers
Service Type Name of the service type
Printing status Status of print
Generated
Credential Type It displays the type of credentials such as “password“
Printed Via It displays the method of password printed
1.5.5.3.14.18 Service Password Expires in 5 Days Report
What is Service Password?
The Service Password Expires in 5 Days Report displays the services whose passwords will expire in the next 5
days. To generate this report, the user needs to select the required information in available filters and click on
View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
To view this report, users must have the following permission(s):

## [p322]

www.arconnet.com|Copyright © 2025 322
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target servers
Service Type Name of the service type
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
• Service Password Expires in 5 days Report

## [p323]

www.arconnet.com|Copyright © 2025 323
Field Names Description
Max Password Age Maximum age of password after which the password
changes
Current Password Age The current age of passwords in days
Group Name Name of the server group to which the server belongs
Credential Type It displays the type of credentials such as “password“
1.5.5.3.14.19 Service Password Manually Changed Report
What is Service Password Manually Changed Report?
The Service Password Manually Changed Report displays all of the services whose passwords have been
manually changed. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and
DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
•
To view this report, users must have the following permissions(s):
Service Password Manually Changed Report

## [p324]

www.arconnet.com|Copyright © 2025 324
Field Names Description
DB Instance The instance of the target servers
Service Type Name of the service type
Changed By Name of the Administrator who changed the
password manually
Changed On Date/time at which the password was changed
Credential type It displays the type of credentials such as “password“
1.5.5.3.14.20 Service Password Never Changed Report
What is Service Password Never Changed Report?
The Service Password Never Changed Report displays all of the services that have never had their passwords
changed, either manually or through a password change process. To generate this report, the user needs to
select the required information in available filters and click on View Report. It can be exported and
downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Never Changed Report

## [p325]

www.arconnet.com|Copyright © 2025 325
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
Group Name Name of the service group to which the server
belongs

## [p326]

www.arconnet.com|Copyright © 2025 326
Field Names Description
Credential type It displays the type of credentials such as “password“
1.5.5.3.14.21 Service Password Never Changed Report - All LOB
What is Service Password Never Changed Report - All LOB?
The Service Password Never Changed Report - All LOB display details of all the services whose passwords have
never been changed, either manually or through the password change process, across all LOBs. To generate
this report, the user needs to select the required information in available filters and click on View Report. It can
be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Never Changed Report-All LOB

## [p327]

www.arconnet.com|Copyright © 2025 327
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
Group Name Name of the service group to which the server
belongs
1.5.5.3.14.22 Service Password Security Status Report
What is Service Password Security Status Report?
The Service Password Security Status Report displays the security password status (open/closed) of all services
in graphical and grid view format. To generate this report, the user needs to select the required information in
available filters and click on View Report. It can be exported and downloaded in multiple formats such as PDF,
CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Password Security Status Report

## [p328]

www.arconnet.com|Copyright © 2025 328
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Service User Name The user name of the service
Service IP Address The IP address of the target server
Service Host Name The hostname of the target server
Service Instance The instance of the target server
Service Domain The domain name of the target server
Service Type Name of the service type
1.5.5.3.14.23 Service Password Vaulting Status
What is Service Password Vaulting Status?
The Service Password Vaulting Status Report displays the vaulting password status (open/closed) of all services
in grid view format. To generate this report, the user needs to select the required information in available filters
and click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and
DOC.

## [p329]

www.arconnet.com|Copyright © 2025 329
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
Service Password Vaulting Status Report
Zoom out to the screen to view all the columns or click on the + button to expand the hidden columns.

## [p330]

www.arconnet.com|Copyright © 2025 330
Field Names Description
Sr. No. To identify and distinguish rows
Service IP The IP associated with the target server
LOB Line of Business
Group Name of the Server Group
Service Type The name of the service type
System IP Instance hostname The hostname of the IP instance
Host Name The hostname of the target server
Instance Name The instance of the target server
URL Parameter Displays the URL parameter
Privileged Service User Name The username of the privilege Id service
Port Displays the port number of the target server
Domain The domain name of the target server
Current Password Age Age of the current password
Min Password Age The lowest age of the password
Max Password Age Maximum age of the password after which the
password changes
Allow Password Change Is the password change feature enabled
Allow SPC Is the SPC feature enabled
Seal Status Status of Seal
Vault Status As On Report Date Status of the Vault on till date
Password Open By Name of the User who opens the password
Password Open For Hours Select the time for which you want the password to
remain open
Password Open On Displays the date when the password was open
Password Open Till Displays the date and time until when the password is
open for use
Password Rotate Status Status of the password rotation
APC Errors Display if APC error found
Allow Auto Heal Is the Auto Heal feature enabled

## [p331]

www.arconnet.com|Copyright © 2025 331
Field Names Description
LTC IP and Username of the LTC Service
Last Password Change On Displays the date when the password was changed
last time
Last Password Change By Displays the name who has changed the password last
time
Next Password Change Displays the date of the next password change
Dependency On Primary Service Displays if has a dependency on primary service
Service Status Status of the Service
1.5.5.3.14.24 Service Password Vaulting Summary Report
What is Service Password Vaulting Summary Report?
The Service Password Vaulting Summary Report displays the total number of services, the number of services
vaulted, and the number of services pending for vaulting, LOB-wise. To generate this report, the user needs to
click on View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Service Password Vaulting Summary Report

## [p332]

www.arconnet.com|Copyright © 2025 332
Field Names Description
LOB The name of the LOB
LOB Description Description of the LOB entered by the Administrator
at the time of creation
Total No of services Total number of services in that LOB
Number of services vaulted Total number of services vaulted
Number of services pending for vaulting Total number of services pending for vaulting
1.5.5.3.14.25 Service Password Viewed By Administrator
What is Service Password Viewed By Administrator?
The Service Password Viewed By Administrator Report displays details of all the service passwords viewed by
the Administrators in grid view format. To generate this report, the user needs to select the required
information from the available filters and click on View Report. It can be exported and downloaded in formats
such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
•
To view this report, users must have the following permission(s):
Service Password Viewed By Administrator
Zoom out to the screen to view all the columns or click on the + button to expand the hidden columns.

## [p333]

www.arconnet.com|Copyright © 2025 333
Field Names Description
ID The ID of the service
Requested By The name of the user who raised the request
Requested On Date/time at which the request was raised
Service IP The IP address of the target servers
Service Host Name The hostname of the target server
Service Domain Name The domain name to which the service belongs
Service Type The server type for which the request has been raised
Approver 1 User ID The User ID associated with the Approver 1
Approved On Date and Time Date/time at which the service password was
approved by Approver 1
Approver 2 User ID The User ID associated with the Approver 2
Approved On Date and Time Date/time at which the service password was
approved by Approver 2
Description Description of the service password
Open For Hours Time in hours until which the request will remain valid
Current Status The current status of the request
1.5.5.3.14.26 Service Reached Maximum Failed Attempts
What is Service Reached Maximum Failed Attempts Report?
The Service Reached Maximum Failed Attempts Report displays all the services for which the scheduled
password change has been terminated due to exceeding the maximum number of failed attempts. The
maximum number of failed attempts is specified in the Scheduled Password Change - Service Reached
Maximum Failed Attempts in Settings. To generate this report, the user needs to click on View Report. It can
be exported and downloaded in formats such as PDF, CSV, XLS, and DOC.
•
To view this report, users must have the following permission(s):
Service Reached Maximum Failed Attempts

## [p334]

www.arconnet.com|Copyright © 2025 334
The following columns are available in this report:
Field Names Description
Sr No. To identify and distinguish rows
Service type Name of the service type
IP Address The IP address of the target server
User Name Username of the service
DB Instance Displays DB Instance of service
1.5.5.3.14.27 Service Reconcile Status Report
What is Service Reconcile Status Report?
The Service Reconcile Status Report displays the status of all reconciliations as well as the details of each
reconciliation. To generate this report, the user needs to select the required information from the available
filters and click on  View Report. It can be exported and downloaded in formats such as PDF, CSV, XLS, and
DOC.
Zoom out to the screen to view all the columns or click on the + button to expand the hidden columns.
•
To view this report, users must have the following permission(s):
Service Reconcile Status Report

## [p335]

www.arconnet.com|Copyright © 2025 335
•
•
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
LOB/Profile The name of the LOB
Service Type Name of the service type
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
Domain Name The domain name of the target server
Port The port opened to connect to the target server
Reconciled Status Status of the password reconciliation
Reconciled success
Never reconciled
Reconciled On Date/time at which the reconciliation happened
Error Errors captured in case of failure of reconciliation

## [p336]

www.arconnet.com|Copyright © 2025 336
Field Names Description
Server Group Name Name of the server group to which the target server
belongs
Started By Name of the Administrator who started Service
1.5.5.3.14.28 Services Details for SPC - Maximum Failed Attempts
What is Service Details for SPC - Maximum Failed Attempts report?
The Service Details for SPC - Maximum Failed Attempts report displays the information of the services for SPC
for which there were maximum failed attempts. To generate this report, the user needs to click on View Report.
It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP Address of the target server
Host Name The host name of the target server
Domain Name The domain name of the target server
•
To view this report, users must have the following permission(s):
Service Details for SPC - Maximum Failed Attempts

## [p337]

www.arconnet.com|Copyright © 2025 337
Field Names Description
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
Group Name Name of the server group for which the services were
scheduled for SPC.
1.5.5.3.14.29 Services Scheduled for SPC
What is Services Scheduled for SPC Report?
The Services Scheduled for SPC Report displays services that are scheduled or queued for password change. To
generate this report, the user needs to select the required information from the available filters and click on
View Report. It can be exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
•
To view this report, users must have the following permission(s):
Services Scheduled for SPC Report

## [p338]

www.arconnet.com|Copyright © 2025 338
Field Names Description
Service Type Name of the service type
Max Password Age Maximum age of password after which the password
changes
Min Password Age Minimum age of password after which the password
changes
Current Password Age The current age of passwords in days
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Service Group Name of the server group in which the services are
scheduled for SPC
1.5.5.3.14.30 SPC Not Configured Report
What is SPC Not Configured Report?
SPC Not Configured Report displays services for which SPC has not been configured. To generate this report,
the user needs to select the required information from the available filters and click on View Report. It can be
exported and downloaded in multiple formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
SPC Not Configured Report

## [p339]

www.arconnet.com|Copyright © 2025 339
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
User Name The name of the user
DB Instance The instance of the target server
Service Type Name of the service type
Description 1 Text entered during the creation of the service
Description 2 Text entered during the creation of the service
Description 3 Text entered during the creation of the service
Service Group Name of the service group in which the service is
present
1.5.5.3.14.31 SPC Success and Failed Report
What is SPC Success and Failed Report?
Field SPC Success and Failed Report displays details of service password changes through the SPC service. To
generate this report, the user needs to select the required information from the available filters and click on
View Report. It can be exported and downloaded in formats such as PDF, CSV, XLS, and DOC.
The following columns can be seen in this report:
•
To view this report, users must have the following permission(s):
SPC Success and Failed Report

## [p340]

www.arconnet.com|Copyright © 2025 340
•
•
Field Names Description
Sr. No. To identify and distinguish rows
IP Address The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
Server Group name Name of the server group to which the server belongs
Last Password Changed On Date/time at which the last password was changed
Current Status Present status of the password
Success
Failed
1.5.5.3.14.32 Users Extracting Password Envelope Report
What is Users Extracting Password Envelope Report?
The Users Extracting Password Envelope Report displays details of users who have opened the printed
password envelopes. To generate this report, the user needs to select the required information from the
available filters and click on View Report. It can be exported and downloaded in formats such as PDF, CSV, XLS,
and DOC.
•
To view this report, users must have the following permission(s):
Users Extracting Password Envelope Report

## [p341]

www.arconnet.com|Copyright © 2025 341
The following columns can be seen in this report:
Field Names Description
Sr. No. To identify and distinguish rows
Login User Name of the user opening the password envelope
LOB Name of the LOB
Authenticator 1 Name of the first authorizer who allowed the
envelope to be opened
Authenticator 2 Name of the second authorizer who allowed the
envelope to be opened
Domain of Authenticator 1 Domain to which the Authorizer 1 belongs
Domain of Authenticator 2 Domain to which the Authorizer 2 belongs

## [p342]

www.arconnet.com|Copyright © 2025 342
Field Names Description
Envelope Category Type of password envelope
Service IP The IP address of the target server
Host Name The hostname of the target server
Domain Name The domain name of the target server
User Name The name of the user
Service Type Name of the service type
Envelope Status Status of envelope
Date of Generation Date/time at which the envelope was created
1.5.5.4 Dashboard
1.5.5.4.1 PAM DASHBOARD OVERVIEW
The Dashboard section simplifies the complex data and provides several useful graphical representations of
the various actions performed and important information in the ARCON PAM. The Dashboard is used in
monitoring and controlling processes and allows you to quickly understand the most crucial elements of your
data. You can obtain competitive assessments and real-time insights to help discover issues needing immediate
attention, streamline workflows, and allocate resources more effectively. Additionally, it shows the pinned
reports that you can manually manage to add to or delete from your dashboard.
The dashboard has two main sections: cards and graphs. The cards section displays all the information in an
easy-to-read format, while the graph section displays information in an interactive way.
Users having Dashboard privileges will only be able to view the Dashboard menu in Client Manager.

## [p343]

www.arconnet.com|Copyright © 2025 343
•
•
•
•
•
•
1.5.5.4.1.1 What are Cards in dashboard ?
Cards highlight the count of general activities in ARCON | PAM. Detailed information can be viewed in a
tabular format by clicking on the More Info option associated with each card.
The following cards are available:
Users Currently Logged On: The Users Currently Logged On  widget shows real-time details like user
name, display name, and active session count, helping monitor user activity across services.
Services Currently Being Accessed: The Services Currently Being Accessed  widget shows real-time
information on services accessed by users, including server IP, user details, service type, and machine
info, helping track user access to specific services.
Critical Commands Fired: The Critical Commands Fired  widget shows details of high-risk commands
executed on the server, including the command, response, user info, service type, timestamp, and server
IP, helping prevent major system damage.
Open Passwords: The Open Passwords widget displays details of server passwords viewed by users and
pending change, including server IP, service username, service type, and the expiry time of the open
password.
1.5.5.4.1.2 Graphs
The graphs section of the Dashboard will display the reports that are pinned to display in the Dashboard. You
can do the following activities with the pinned graph reports:
Hide Graph: Hide Graph allows users to temporarily remove a pinned report from the Dashboard view.
This helps declutter the interface without deleting the report. Users can unhide the report anytime by
clicking the + icon.
Remove Graph: Remove Graph  allows users to delete a pinned report from the Dashboard. This helps
free up space when the maximum limit of six pinned reports is reached. Once removed, the report must
be re-pinned to appear again on the Dashboard.

## [p344]

www.arconnet.com|Copyright © 2025 344
•
1.
2.
Add Graph: Add Reports allows users to pin selected reports to the Dashboard for quick access. It helps
present complex data in a simplified format, making it easier to monitor key information and spot issues
quickly.
1.5.5.4.2 Users Currently Logged On
The Users Currently Logged On widget provides real-time details of a user accessing a number of services. It
displays details such as the user’s name, display name, and the number of sessions accessed by that user at that
particular time. By using this feature, the user can monitor the users and their activity.
Follow the steps below to view details of the User Currently Logged On widget:
Click on the Dashboard menu:
Click on the More Info link present below the Users Currently Logged On widget:

## [p345]

www.arconnet.com|Copyright © 2025 345
3.
4.
5.
The Users Currently Logged On screen appears:
Select the number of entries from the Show entries drop-down list to display only those many records in
the grid:
To search for a particular record, enter the required search filter in the Search text field on the right-
hand side of the screen:

## [p346]

www.arconnet.com|Copyright © 2025 346
1.
2.
Refer to the following table to understand the data displayed under each column:
Field Name Description
Username It shows the name of the user.
Display Name It shows the display name of the user.
Number Of Sessions It shows the number of sessions accessed by the user
on that day.
1.5.5.4.2.1 View Report
To view the Users Currently Logged On report, follow these steps:
Click “Click to view Report” as illustrated below.
The User Currently Logged On screen is displayed. Select the LOB and User Group from the dropdown
list.

## [p347]

www.arconnet.com|Copyright © 2025 347
3.
4.
1.
Click View Report.
The report below displays all the users currently logged on. The report can be exported and downloaded
in formats such as PDF, CSV, XLS, and DOC.
1.5.5.4.3 Services Currently Being Accessed
The Services Currently Being Accessed widget provides real-time details of services currently being accessed
by users. It displays details such as Server IP Address, User ID details, the display name of the user, the type of
service accessed, the user name of the service, and machine details from where the service is being accessed. It
may help to monitor the user who has accessed any particular services.
Follow the steps below to view the details of the Services Currently Being Accessed widget.
Click on the Dashboard menu:

## [p348]

www.arconnet.com|Copyright © 2025 348
2.
3.
4.
Click on the More Info link present below the Services Currently Being Accessed widget:
The Services Currently Being Accessed screen appears:
Select the number of entries from the Show entries drop-down list to display only those many records in
the grid:

## [p349]

www.arconnet.com|Copyright © 2025 349
5. To search for a particular record, enter the required search filter in the Search text field on the right-
hand side of the screen:
Refer to the following table to understand the data displayed under each column:
Field Name Description
Service IP It shows the IP address of the target server.
User ID It shows the ID of the user.
Display Name It shows the display name of the user.
Service Type It shows the name of the service type.
Service User Name It shows the username of the service.
Session Source It shows the name of source of the session.
Host Name It shows the Host name of the target server.

## [p350]

www.arconnet.com|Copyright © 2025 350
1.
2.
Field Name Description
LOB Name It shows the name of the LOB to which the server
belongs.
1.5.5.4.4 Critical Commands Fired
Critical Commands Fired  widget provides details of critical commands fired on the server. It displays details
such as the command fired, the response to the command fired, date and time details, type of service, name of
the user who fired the command, the ID of the user, and the server IP on which the command was fired. This
feature helps to prevent the system from major harm and irrecoverable damage.
Follow the steps below to view details of the Critical Commands Fired widget:
Click on the Dashboard men
Click on the More Info link present below the Critical Commands Fired widget:
The Critical Commands Fired screen appears:

## [p351]

www.arconnet.com|Copyright © 2025 351
3. Select the number of entries from the Show entries drop-down list to display only those many records in
the grid:

## [p352]

www.arconnet.com|Copyright © 2025 352
4. To search for a particular record, enter the required search filter in the Search text field on the right-
hand side of the screen:
Refer to the following table to understand the data displayed under each column:
Field Name Description
Command It shows the critical commands fired on the server.
Command Response It shows the response to the command fired.
Timestamp It shows the date and time details of the commands
fired.
Service Type It shows the name of the service type.
User Name It shows the name of the user.
User ID It shows the ID of the user.
Server IP It shows the IP address of the target server.
1.5.5.4.5 Open Passwords
The  Open Passwords  widget provides details of the server password, which are viewed by the user and are
pending change. It displays details such as the server IP whose password is open, the user name of the service,
the type of service, and the date and time details till when the password will be open.
Follow the steps below to view details of the Open Passwords widget:

## [p353]

www.arconnet.com|Copyright © 2025 353
1.
2.
3.
4.
Click on the Dashboard menu:
Click on the More Info link present below the Open Passwords widget:
The Open Passwords screen appears:
Select the number of entries from the Show entries drop-down list to display only those many records in
the grid:

## [p354]

www.arconnet.com|Copyright © 2025 354
5.
1.
To search for a particular record, enter the required search filter in the Search text field on the right-
hand side of the screen:
Refer to the following table to understand the data displayed under each column:
Field Name Description
IP Address It shows the IP address of the target server.
User Name It shows the name of the user.
Service Type It shows the name of the service type.
Open Till It shows the date and time details till when the
password will be opened.
Password Open By It specifies the name of the user who has opened the
requested password for the required service.
Description It shows the remarks if mentioned.
1.5.5.4.6 Hide Graph
Follow the steps below to hide the reports in the Dashboard:
Select the Dashboard from the menu bar:

## [p355]

www.arconnet.com|Copyright © 2025 355
2.
3.
Click on the Hide icon to hide the pinned report:
The report will be hidden. Click on the + icon to unhide the report:

## [p356]

www.arconnet.com|Copyright © 2025 356
1.
2.
1.5.5.4.7 Remove Graph
The maximum number of pinned reports in the Dashboard menu is six. You need to remove the pinned report
viewed in the Dashboard menu if you want to pin any new report exceeding the limit.
Follow the steps below to remove the reports from the Dashboard:
Select the Dashboard from the menu bar:
Click on the Remove From Dashboard icon to remove the pinned report:

## [p357]

www.arconnet.com|Copyright © 2025 357
3.
4.
1.
A pop-up window is displayed. Then click on the Delete button to delete the pinned report.
The report will be deleted from the Dashboard.
1.5.5.4.8 Add Graph
You can add a report to the Dashboard to get a complex report in a simplified format that helps you to quickly
understand your data and discover issues needing immediate attention.
Follow the steps below to pin the reports to the Dashboard:
Click on the Reports menu to go to the desired reports:
The maximum number of pinned reports in the Dashboard menu is six. You need to remove the pinned
report viewed in the Dashboard menu if you want to pin any new report exceeding the limit.

## [p358]

www.arconnet.com|Copyright © 2025 358
2.
3.
Select the desired report from the Report section:
Click on the pin icon to pin the report:

## [p359]

www.arconnet.com|Copyright © 2025 359
4.
5.
It opens the below pop-up window and shows the message that Report successfully pinned to
dashboard. Then click on the Close button to complete the process:
The report will be displayed on the Dashboard.
1.5.5.5 About
1.5.5.5.1 Overview
In the about page, the user can find the important information about the ARCON PAM client manager that is
the version of software which is being used, the copyright information, the date when the current version of the
PAM is released, warning note which provides the constructive notice about the authority of this software, and
account name. Also the user can add the contact details by clicking on below available edit option. The pop-up
window will get open where the user can add contact information.

## [p360]

www.arconnet.com|Copyright © 2025 360
1.
2.
1.5.5.5.1.1 How to Edit Contact Details in the About Section?
Click on the Edit Contact Details icon.
The Edit Contact Details screen will be displayed. Then enter the details and save them.
•
To change the contact details, users must have the following permission:
Edit Contact

## [p361]

www.arconnet.com|Copyright © 2025 361
3.
•
•
•
•
•
•
•
Your new contact information will be saved. This contact information will be displayed on about page
exactly below the account name.
1.5.6 Side Menu Bar
This is an index of the icons on the Side Menu bar.
1.5.6.1 Side Menu
1.5.6.1.1 My Services
1.5.6.1.2 Preferences
My Preferences
Delegation
1.5.6.1.3 Raise Request
Service Access Request
Service Password Request
Ticket Request
1.5.6.1.4 View Pending Requests
Service Access Requests
Service Password Requests

## [p362]

www.arconnet.com|Copyright © 2025 362
•
•
•
•
•
•
Ticket Requests
1.5.6.1.5 Request Logs
Service Access Request Log
Service Password Request Logs
1.5.6.2 RaiseRequest
What is a Raise Request ?
The user can raise the request to access any existing services, service password envelope, and to raise the
ticket as simple as normal ticketing system. ARCON PAM provides ticketing system that is designed to create
and handle tickets and track requests in a similar way. The user needs to navigate to the third icon on the Side
Menu is the Raise Request icon :w:. It helps to raise requests to the Admin/Approver for access to services and
passwords. This section provides information on the creation of requests.
Requests can be of the following types:
Service Access Request
Service Password Request
Ticket Request
1.5.6.2.1 Service Access Request
What is a Service Access Request?
The Service Access Request  is the feature that allows the user to raise a request for access to privileged
services they do not currently have access to. The approvers who have been configured in the workflow matrix
can approve this service access request. Approvers must be configured by the Administrator. Multi-level and
multiple approvers can be set in a workflow to streamline the process. The approvers must read the
description, understand the purpose of the request, and then choose to approve, decline, or forward the

## [p363]

www.arconnet.com|Copyright © 2025 363
1.
2.
3.
1.
2.
3.
request.
Types of service access requests:
Permanent: This approach requests complete control of the privileged account. On approval, the user is
provisioned to that service for a lifetime and receives an SSO.
Time-based: This approach allows a temporary elevation of privileges, enabling users to access
privileged accounts or run privileged commands on a by-request, time-based basis. The access is
removed when the stipulated time period has ended.
One-Time: This approach allows access to the privileged account or service only once after the request
has been approved.
How to Create a Service Access Request?
To access an unassigned service, navigate to the My Access window and click the Raise Request icon in
the left pane.
Select Service Access.
Enter the required details as shown in the table below and submit your request.
•
To raise a service access request, the following configuration must be enabled from the global
configuration:
ARCOS Service Access- Is Enabled
•
•
•
•
To raise a permanent service access request, the following configuration must be enabled from
the global configuration:
Permanent Request Service Access - Is Enabled
To raise a time-based service access request, the following configuration must be enabled from
the global configuration:
Time-Based Request Service Access - Is Enabled
To raise a one-time service access request, the following configuration must be enabled from
global configuration:
One-Time Request Service Access - Is Enabled
One-time or time-based requests can be raised for services across all LOB by the user only if
the following configuration is enabled:
Allow Service Access Request for all services in LOB

## [p364]

www.arconnet.com|Copyright © 2025 364
Refer to the table below to understand the fields:
Fields Description
LOB The name of the LOB
Service Type The name of the service type for which the request is raised.
Search service (IP
Address / Hostname)
The target server can be searched directly by entering its IP address, hostname,
username, or description labels.
Configuration
Commands
Specify the configuration commands you need access to for that server.
Time Duration Permanent The request is raised to access the target server permanently.
Time-Based Access The request is raised to access the target server for a certain
duration
•
The configuration command box is visible only if the following configuration is
disabled in Settings:
Hide Configuration Command for Service Request

## [p365]

www.arconnet.com|Copyright © 2025 365
Fields Description
Access Duration The dates between which the
user requires server access.
Access Period The period during which the user
requires access to the server is
between the specified start and
end dates of the access duration.
Per Session Duration In a session, the amount of time,
in hours and minutes, that a user
can access the service.
One-Time Access The request is raised to access the target server only once.
Access Duration The dates between which the
user requires server access.
Per Session duration In a session, the number of hours
and minutes a user can access
the service.
Description Summary explaining the purpose of the request to the approver.
Reference Type
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
Reference Details
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled

## [p366]

www.arconnet.com|Copyright © 2025 366
1.
2.
3.
Fields Description
Verification Code This CAPTCHA code is entered only to validate human identity.
1.5.6.2.1.1 JIT Provisioning
User accounts on target servers are automatically provisioned and de-provisioned based on PAM's internal
workflow. When access to a PAM SSO server is granted, the user is automatically provisioned on the
corresponding target server. Once the service access period expires, the user is automatically removed from
the target server.
Follow these steps to create a Service Access Request with JIT Provisioning:
Select the JIT Provisioning from the Type dropdown field.
Select the Service Type from the Service Type drop-down field.
Enter the required details as shown in the table below and submit your request.
•
The verification code appears only if the following configuration is enabled in
Settings.
CAPTCHA Validation In ACMO Service Access and Password Request
- Is Enabled

## [p367]

www.arconnet.com|Copyright © 2025 367
Refer to the table below to understand the fields:
Fields Description
Type Select the type of provisioning from the dropdown list.
LOB The name of the LOB
Service Type The name of the service type for which the request is raised.
Search service (IP
Address / Hostname)
The target server can be searched directly by entering its IP address, hostname,
username, or description labels.
The Type drop-down field is displayed only when the JIT Request Access Service toggle is turned on in
the settings.

## [p368]

www.arconnet.com|Copyright © 2025 368
Fields Description
User Name Displays an automatically generated username combining the logged-in user's name
and a timestamp (example: ARCOSA_080720251715). This value is not editable.
Role Name Displays the role linked to the selected service type. When a role is chosen, the user will
be assigned to that role on Linux.
Group Name Displays the group linked to the selected service type. When a group is chosen, the user
will be assigned to that group on a Windows machine.
Description Summary explaining the purpose of the request to the approver.
Time Duration Time-Based Access The request is raised to access the target server for a certain
duration
Access Duration The dates between which the
user requires server access.
Access Period The period during which the user
requires access to the server is
between the specified start and
end dates of the access duration.
Per Session Duration In a session, the amount of time,
in hours and minutes, that a user
can access the service.
One Time The request is raised to access the target server only once.
Access Duration The dates between which the
user requires server access.
Per Session duration In a session, the number of hours
and minutes a user can access
the service.
This field is visible only when JIT Provisioning is selected from the Type
dropdown and either SSH Linux or Windows RDP is selected from the Service
Type dropdown.
This field is visible only when JIT Provisioning is selected from the Type
dropdown and SSH Linux is selected from the Service Type dropdown.
This field is visible only when JIT Provisioning is selected from the Type
dropdown and Windows RDP is selected from the Service Type dropdown.

## [p369]

www.arconnet.com|Copyright © 2025 369
1.
2.
3.
Fields Description
Reference Type
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
Reference Details
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
Verification Code This CAPTCHA code is entered only to validate human identity.
1.5.6.2.1.2 Access Mapping
In the Service Access Request screen, Access Mapping enables users to submit requests for access to
privileged services they currently do not have access.
Follow these steps to create a Service Access Request with Access Mapping:
Select the Access Mapping from the Type dropdown field.
Select the Service Type from the Service Type drop-down field.
Enter the required details as shown in the table below and submit your request.
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled
•
The verification code appears only if the following configuration is enabled in
Settings.
CAPTCHA Validation In ACMO Service Access and Password Request
- Is Enabled

## [p370]

www.arconnet.com|Copyright © 2025 370
Refer to the table below to understand the fields:
Fields Description
Type Select the Access Mapping from the dropdown list.
LOB The name of the LOB
Service Type The name of the service type for which the request is raised.
Search service (IP
Address / Hostname)
The target server can be searched directly by entering its IP address, hostname,
username, or description labels.
User Name Displays the user name of the selected service type.
Description Summary explaining the purpose of the request to the approver.
Time Duration Permanent The request is raised to access the target server permanently.
Time-Based Access The request is raised to access the target server for a certain
duration
Access Duration The dates between which the user
requires server access.

## [p371]

www.arconnet.com|Copyright © 2025 371
Fields Description
Access Period The period during which the user
requires access to the server is
between the specified start and end
dates of the access duration.
Per Session Duration In a session, the amount of time, in
hours and minutes, that a user can
access the service.
One Time The request is raised to access the target server only once.
Access Duration The dates between which the user
requires server access.
Per Session duration In a session, the number of hours and
minutes a user can access the service.
Reference Type
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
Reference Details
(Customized field)
This field name is bespoke and can be set according to your organization's needs
in Settings.
Verification Code This CAPTCHA code is entered only to validate human identity.
Once the request has been raised, it goes to the approver set in the workflow for approval. Users can check the
status of the raised request in the View your pending service access request tab.
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled
•
This field is mandatory only if the following configuration is enabled in
Settings:
Reference Details Mandate while raising Service Access Request - Is
Enabled
•
The verification code appears only if the following configuration is enabled in
Settings.
CAPTCHA Validation In ACMO Service Access and Password Request
- Is Enabled

## [p372]

www.arconnet.com|Copyright © 2025 372
1.
1.5.6.2.2 Service Password Request
The Service Password Request is the feature that is used to raise the request of any service type or connection
to enter the password manually. Also, enter the password while accessing the service from outside the ARCON
PAM. A standard user can raise a request to view the password of any service that the Administrator has posed.
The password lets users access the server directly. Once a password is viewed by the user, it remains open until
it is changed. Open Password Cards can be seen on the ACMO Dashboard.
How to Create a Service Password Request ?
To view the password of a server, go to the My Access window and then click on the Raise Request :w:
icon → Service Password in the left side menu.
•
To raise a service password request, users must have the following permission(s):
Allow Service Password Request
•
To raise a service password request, the following configuration must be enabled in Settings:
ARCOS Service Password - Is Enabled

## [p373]

www.arconnet.com|Copyright © 2025 373
2. Enter the details into the form and submit the request:
Refer to the below table to understand the fields and data present in the Service Password Request:
Fields Description
LOB The name of the LOB
Service Type The name of the service type for which the request is raised
Search service (IP Address /
Hostname)
The target server can be searched directly by entering its IP Address /
Hostname / Description1 labels.
All Services A list of all the services in the service box which are not assigned to
that user but belong to that LOB and Service type.
Service Select the target server for which the request is raised.
Description Brief note explaining the purpose of request to the approver.

## [p374]

www.arconnet.com|Copyright © 2025 374
Fields Description
View On The start date/time from which the user can view the password of the
server.
Open Till Date The end date/time until which the user can view the password of the
server.
Now This checkbox will allow the user to view the password as soon as the
approver has passed the request.
Open for Hours The number of hours for which the
password remains open .
Verification Code This CATCHA code is entered only for validating human identity.
Once the request has been raised, it goes to the approver set in the workflow for approval. Users can check the
status of the raised request in the View your pending service password request tab.
•
The verification code appears only if the following
configuration is enabled in Settings.
CAPTCHA Validation In ACMO Service Access and
Password Request - Is Enabled

## [p375]

www.arconnet.com|Copyright © 2025 375
1.5.6.2.2.1
Handling Duplicate Requests
Users are not allowed to submit multiple requests, which implies that once a request is submitted and delivered
to the approver, it must be approved or rejected first. The user can only make the same request again once the
approver has taken action.
Once the request is raised, a Successfully Raised message dialog will appear. However, if the request already
exists, a message for a Duplicate Request will appear. Two other links are also shown on the right side.
View Raised Details
Click on the View Raised Details to check the details of all raised requests.
Clear Raised Details
To remove all the existing raised requests from the table, click on Clear Details.

## [p376]

www.arconnet.com|Copyright © 2025 376
1.5.6.2.2.2 Service Password Request Workflow
Passwords for all Services are vaulted safely in ARCON | PAM. Users must request these password to gain
access to servers. The user can request passwords of only those services that are assigned to them. The
workflow for such a request needs to be configured in Settings prior to the request being raised by the user
through the Client Manager. Requests raised by users from the Client Manager are sent for approval based on
the approval levels configured in the workflow matrix. Therefore, the workflow provides a definite audit trail
and a proper flow of events that be monitored closely.
Service Password Request Workflow Configuration
The process of configuring workflow, raising requests, approval process, receiving the password, and viewing
approval logs is explained below.
Step 1: Configuring User Request Approval Workflow
The User Request Approval Workflow is configured in Settings.
Delegation
Delegation is assigning the responsibility or authority to another person, from a manager to a subordinate to
execute the raised request i.e. Service Access, Service Password, and Ticket activities. However, the user who
delegates the work remains accountable for the output of the work. Delegation helps subordinates to make
decisions in the absence of higher authorities. In other words, it is the shifting of authority from one level to
another. It helps the organization to make a decision quickly, helps in building the skills of subordinates, and
motivates them to perform better.
To delegate approval rights, use the following path:
Client Manager → My Access → Preferences → Delegation
The workflow should be defined in Settings before delegating any responsibility.

## [p377]

www.arconnet.com|Copyright © 2025 377
The Approver configured in User Request Approval Workflow needs to
configure Delegation for Any or Service Password if they want another user to approve/reject requests in
their absence.
Step 2: Raise Service Password Request
The Service Password Request feature helps the user raise a request to access the password of a service to the
Admin/Approver. Users can raise Service password requests for only those Services which are assigned to
them.
Use the following path to configure Service Password Request:
Client Manager → My Access → Raise Request :s: → Service Password

## [p378]

www.arconnet.com|Copyright © 2025 378
The Service Password Request screen contains the following fields:
Field Name Description
LOB Select the LOB
Service Type Select the Service Type
Search Service (IP Address / Hostname) Enter the Service details and click Search  icon.
You can click the Search icon without entering any
value in Search Service (IP Address / Hostname) to
enable the Service drop-down.
Service Select the Service.
Description Enter the Description.
View On Click on the Now checkbox to view password as soon
as approval process has been completed.
You can deselect the Now checkbox and enter a date
and time in the field just below the checkbox.
The Service Password will be delivered after approval
process in your ARCON | PAM Mailbox at the
configured date and time.

## [p379]

www.arconnet.com|Copyright © 2025 379
1.
1.
Field Name Description
Open For Hours Select the time for which you want the password to
remain open.
Open Till Date Displays the date and time until when the password is
open for use.
The data in this field is auto-populated based on the
values selected in View On and Open For Hours.
Verification Code Enter the displayed verification code.
Enter or select details and click Submit. The request will be raised for the selected service.
If the user has raised a request for Service Password selecting to view password as soon as the approval
process has been completed, the password will be open for 1 hour after it has been delivered to requestor's
mailbox.
Pending Requests
The Service Password Pending Request feature helps you to view a list of requests raised by users that are
pending approval.
To view pending Service Password Request, use the following path:
Client Manager → My Access → Pending Requests → Service Password
The Approver or Delegated User needs to click the View Request link to view the request. The following
screen will be displayed.

## [p380]

www.arconnet.com|Copyright © 2025 380
2. Enter comments and click Approve to approve the request. The request will be sent to the second
Approver.
Step  3: Approve Service Password Request
Service Password Request Approval allows the Admin/Approver to view and approve the request raised by the
user to access the password of the service. When a request is raised, the request is sent to the Approvers
bucket and their Email ID.
To approve a Service Password Request, use the following path:
Client Manager → Manager → Approval Requests :s: → Service Password
If you click Reject, the request will be terminated at this approval level.

## [p381]

www.arconnet.com|Copyright © 2025 381
1.
A similar screen will be displayed to the Delegated User at that approval level. The screen is as follows:
Click the View Request link to view request details. The following screen will be displayed.

## [p382]

www.arconnet.com|Copyright © 2025 382
2.
3.
Request at level 1 needs to be approved either by a First-level Approver or Delegated User.
When a request is approved at level 1, it will be sent to the second-level approver.
4. If all the Approvers approve the request, then the password will be delivered to the requester's mailbox.
Step 4: View the Password of the Requested Service
The Password of the service requested by the user will be delivered in the requester's ARCON | PAM mailbox if
all Approvers approve the request.
To view Password of the requested service, use the following path:
Client Manager → Click the Mailbox
  icon. The following screen will be displayed.
If either Approver or Delegated User rejects the request, the request thread will be terminated at that
level.

## [p383]

www.arconnet.com|Copyright © 2025 383
1.
2.
View the details displayed in the Subject column and click the Open link adjacent to it. The following
window pops up displaying the password of the service.
Click OK. The window will be closed.
If you select 1 value in Open For Hours drop-down while Raising Request but you finish working on
the server in 30 mins, then you can click Close Password to allow ARCON | PAM to change password
of Service at that moment. You can also request your last-level Approver to close the password.

## [p384]

www.arconnet.com|Copyright © 2025 384
Steps 5: View Logs
The Approval Logs - Service Password screen helps you to view the logs of the service password request raised
by the User. In addition, it also displays the Request Approval details such as the name of the Approver, the
status of approval, and the date/time requested for access. Approval Logs are displayed for all Approvers. Only
the Approver at the last level can close the password of the service if requested by the requester.
To view Service Password Request logs, use the following path:
Client Manager → Manager → Approval Logs ( :w: )→ Service Password
Server Manager →  Manage →  ARCOS Workflow Tracker →  Service Password Request Workflow
Tracker → Click View
Process Flow Diagram
This is a process flow diagram for Service Password Request with 2 Approvers.
Click on Close if you want to close password of the Service.

## [p385]

www.arconnet.com|Copyright © 2025 385
1.
2.
3.
1.5.6.2.3 Ticket Request
The ARCON PAM has its own ticketing system as simple as normal ticketing system which permits the user to
raise any ticket for any service modification request. ARCON | PAM runs much like the usual ticketing system
of any organization. It is designed to create and handle tickets and track requests in a similar way. These tickets
will be approved by the approver who has configured in approval workflow.
1.5.6.2.3.1 Creating a Ticket Request
To view the password of a server, go to My Access window and then click on the Raise Request :w: icon
on the left side menu.
Select Ticket request.
Enter the details into the form and submit the request.
1.
2.
Pre-requisites for Creating a Ticket Request
The ticket template must be set by the Administrator in the Service Reference Template  in
Settings.
The server reference/call log must be set for services by the Administrator in Settings.
Users can now create a ticket request.

## [p386]

www.arconnet.com|Copyright © 2025 386
•
•
Refer to the below table to understand the fields present in the Ticket Report:
Fields Description
LOB The name of the LOB
Location Select the location
Service Group The name of the service group to which the service belongs.
Service Type The name of the service type for which the request is raised.
Service (IP Address / Hostname) The target server can be searched directly by entering its IP
Address / Hostname.
Executor The user who uses the ticket to access the service.
Ticket Type The following ticket types are available:
PE - Planned Event: Any periodical process of raising a ticket
or pre-planned cyclic procedure for ticket is considered a
Planned Event.
CR - Change Request: To make a change in an already raised
request, select Change Request.
Users are populated based on the selected service assigned
to them.

## [p387]

www.arconnet.com|Copyright © 2025 387
•
•
•
•
•
•
Fields Description
Activity Type The following activity types are available:
SA - Service Affecting: The proposed activity affects the
service as a whole.
NSA - Non-Service Affecting: The proposed activity will have
no effect on/make changes to the service.
Start Time Date/time from which the ticket is valid.
End Time Date/time until which the ticket is valid.
Expected Duration In a session, the amount of time in hours and minutes a user can
access the service.
Impact The impact this ticket has
Low
Medium
High
Critical
Impact Location Location of the impact
Description Brief note explaining the purpose of request to the approver
Attachment 1 Browse to attach file
Attachment 2 Browse to attach file
Once the request has been raised, it goes to the approver set in the workflow for approval. Users can check the
status of the raised request in the View your pending service ticket request tab.
•
The maximum value of this dropdown is set under the
following configuration in settings
Max Hours for Ticket Session Duration (in hours)
The attachment should be less than 10 MB.
The attachment should be less than 10 MB.

## [p388]

www.arconnet.com|Copyright © 2025 388
•
1.5.6.3 Pending Requests
1.5.6.3.1 What is Pending Requests ?
The Pending Requests  feature in ARCON | PAM  allows users to view all the requests they have raised—
whether for service access, service passwords, or support tickets. Accessible via the fourth icon  on the Side
Menu, this section displays the current status of each request submitted through the Service Request  and
Service Password options.
1.5.6.3.2 Why is it important ?
Tracking the status of access or support requests is essential for transparency and operational efficiency. The
Pending Requests  feature enables users to monitor the progress of their submissions, identify delays, and
follow up when necessary, thereby improving request visibility and reducing turnaround time.
The options available under Pending Requests are as follows:
View Pending Service Access Requests

## [p389]

www.arconnet.com|Copyright © 2025 389
•
•
1.
2.
•
•
•
View Pending Service Password Requests
View Pending Ticket Requests
1.5.6.3.3 View Pending Service Access Requests
What is View Pending Service Access Requests?
In the ARCON PAM, the View Pending Service Access Request is the feature that can be used to check the
status of all raised ticket requests to access the required service. The user can see all the raised service access
requests queued in the Pending Service Access Requests section. Users can check the status of their requests
and obtain information as to which level the request has been escalated to and is pending with which approver.
Perform the following steps to view the pending requests for Service Access:
Click on Service Access. The Pending Service Access Request page will appear.
Refer to the following table to understand the details associated with the pending requests displayed.
Refer to the table below to understand the columns:
Fields Description
Requested By The name of the user who raised the request.
Transaction ID A unique ID assigned to the particular service access request.
Requested On Date/time at which the request was raised.
Description Text entered by the user while raising the request.
Access Type Type of access requested by the user
Permanent
Time-based
One-time
Service The target server for which the request was raised.

## [p390]

www.arconnet.com|Copyright © 2025 390
1.
2.
Fields Description
Current Status Present status or approval level of the raised request.
Offline Access Displays whether the service access is taken offline or online.
Final Approver Displays the name of the final approver.
Final Approver Comment Displays the comment provided by the final approver during the approval of
the request.
Request Changed The level-wise change of the request by the approver.
Pending With Displays the name of the approver with whom the request is pending.
1.5.6.3.4 View Pending Service Password Requests
What is View Pending Service Password Requests?
In the ARCON PAM, under the Pending Request section, the user can see the service password requests which
is yet to approved by the approver. The approver must be configured by the administrator in the approver
workflow. All the raised service password requests are queued in the Pending Service Password Requests
section. Users can check the status of their requests and obtain information as to which level the request has
been escalated to and is pending with which approver.
Process to view pending request for Service Password:
Click the Service Password  option from the Pending Requests navigation bar. The Pending Service
Password Request page will appear.
Refer to the following table to understand the details associated with the requests displayed.
Approval levels and approvers are defined in the user request
approval workflow in Settings.

## [p391]

www.arconnet.com|Copyright © 2025 391
Refer to the table below to understand the columns:
Field Name Description
Request ID A unique ID associated with each service password
request.
Transaction ID A unique ID associated with each transaction.
Requested On Date/time at which the request was raised.
Requested By The name of the user who raised the request.
Description Text entered by the user while raising the request.
Requested Till Date/time until which the request is valid.
Service The target server for which the request is raised.
Current Status Displays the present status or approval level of the
raised request.
Is View Now Displays the name of the approver with whom the
request is pending.
Approval levels and approvers are defined in
the user request approval workflow in
Global Configuration.

## [p392]

www.arconnet.com|Copyright © 2025 392
1.
Field Name Description
Cancel Click to cancel the service password request. The
below text box is displayed. Enter the reason to cancel
the request and click Submit.
1.5.6.3.5 View Pending Ticket Requests
What is View Pending Ticket Requests ?
In the ARCON PAM, under the Pending Request section the user can see the raised tickets which are yet to
approve by approver. The approver must be configured by administrator in approval workflow. All the raised
service ticket requests are queued in the Pending Service Ticket section. Users can check the status of their
requests and obtain information as to on which level the request has been escalated and is pending with which
approver.
Perform the following steps to view the pending requests for Tickets:
Click on Ticket. The Pending Ticket Requests page will appear.

## [p393]

www.arconnet.com|Copyright © 2025 393
2. Refer to the following table to understand the details associated with the requests displayed.
Fields Description
Ticket No. A unique number associated with each service
password request.
LOB Name of the LOB
Service Group Name of the service group to which the target server
belongs
Service The target server for which the request is raised.
Ticket Type The type of ticket
Activity Type The activity type
Executor Name of the approver
Start Time Date/time from which the request starts
End Time Date/time until which the request is valid
Current Status Displays the present status or approval level of the
raised request.
Pending With Displays the name of the approver with whom the
request is pending.
4. Click on View Details to view the details of the ticket.
5. In the Approve - Ticket Request window, the user can view Requestor/Executor Details, Service Details, and
Ticket Details.
The Search option is available on the right hand side to search the entries directly.
Approval levels and approvers are defined in
the user request approval workflow in
Settings.

## [p394]

www.arconnet.com|Copyright © 2025 394
•
•
1.5.6.4 Request Logs
The ARCON PAM provides a feature where the user can see the generated log while requesting any service
access and service password. The fifth icon on the Side Menu Bar is the Request Logs  feature. This feature
tracks all information related to requests raised, i.e., it displays the status of requests and whether a particular
request is approved or rejected. The logs are displayed for:
Service Access Request Logs
Service Password Request Logs
Only the authorized Approver/Admin can approve the ticket.

## [p395]

www.arconnet.com|Copyright © 2025 395
1.
2.
3.
•
•
•
1.5.6.4.1 Service Access Request Logs
The Service Access Request Logs feature allows the user to see the transactions which made from raised
request to request approval including transaction ID, access type, name of the service, current status, and name
of requester and final approver. Service Access Request Logs display the logs for all the service access requests
raised by the user that is currently logged in.
Perform the following steps to view the Service Access Requests Log:
Click on :pe: the Request logs icon.
Click Service Access. The Service Access Request log page will appear.
Refer to the following table to understand the logs of details associated with the requests displayed.
Field Name Description
Requested By The name of the user who has raised the service
access request
Transaction ID A unique ID assigned to that particular transaction
Requested On Date/time of the raised service access request
Description Brief note explaining the purpose of the request to the
approver
Access type Type of request
Permanent
Time-based
One-time
Service The name of the target server for which the request
has been raised

## [p396]

www.arconnet.com|Copyright © 2025 396
•
•
•
1.
2.
3.
Field Name Description
Current Status Displays the status of the request
Approved
Rejected
Pending
Final Approver The name of the final approver
Request Changed This column has the View link, which lets users view
the details of the intended request log
1.5.6.4.2 Service Password Request Logs
The Service Password Request Logs feature enables the user to see the transaction which made from raised
request to request approval including transaction ID, date and time when the request was raised, requested till,
name of the service, current status, and name of the requester and final approver. It displays the logs for all the
service password requests raised by the user that is currently logged in.
Perform the following steps to view the Service Password Request Logs:
Click on :pe: the Request log icon.
Click Service Password. The Service Password Request Logs page will appear.
Refer to the following table to understand logs of details associated with the requests displayed.
Field Name Description
Requested ID Unique ID associated with each raised password
request
Transaction ID A unique ID assigned to that particular transaction or
request log
Requested By The name of the user who has raised the service
access request
Requested On Date/time of the raised service access request

## [p397]

www.arconnet.com|Copyright © 2025 397
•
•
•
•
•
•
Field Name Description
Description Brief note explaining the purpose of the request to the
approver
Requested till The date/time until which the user can view the
password of the server
Service The name of the target server for which the request
has been raised
Current Status Displays the status of the request
Approved
Rejected
Pending
Final Approver The name of the final approver
1.5.6.5 My Service
See the My Access section for detailed information.
1.6 About The Client Manager Guide
1.6.1 Related Documents
Below are the related documents that may help to understand ARCON | PAM in detail:
ARCON | PAM Installation & Configuration Guide describes how to prepare the environment, install,
and configure the ARCON Privileged Access Management Solution.
ARCON | PAM Privileged Access Management (PAM) Admin User Guide  describes the features,
benefits, and functionalities of each component.
ARCON | PAM Feature Guides - We provide separate documents for each PAM feature.
1.6.2 Acronyms
The acronyms used in this manual are as follows:
Acronyms Description
PAM Privileged Access Management
ACMO ARCON Client Manager Online
ESR Enforce Self-Registration
SM Server Manager
CM Client Manager
LOB Line of Business
SSH Secure Shell

## [p398]

www.arconnet.com|Copyright © 2025 398
•
•
•
•
•
Acronyms Description
SSO Single Sign-on
RDP Remote Desktop Protocol
OTP One-Time Password
DB Database
EPAM Enterprise Privilege Access Management
PVSL Password Vault & Session Logging
AGW Application Gateway
vRA vRealize Automation
1.6.3 POC (Points of Contact) & Support Information
The product is developed and maintained by ARCON Tech Solutions Private Limited. We at ARCON are
continuously thriving to develop and deliver the best quality products. As a valued customer, we would like to
know your feedback, suggestions, and ideas for improvements to our products and services. You can always
reach out to us through the below-mentioned ways of communication:
Web
https://arconnet.com/
Sales Contact
You can directly contact us with sales-related topics at the email address sales@arconnet.com, or leave us your
contact information and we will call you back.
Support Contact
To access ARCON | PAM Support Centre (ASC), sign in with your account.
Remote support is available 24*7.
ARCON | PAM Support System is available only for registered users with a valid support package.
ARCON | PAM Support Centre (ASC): https://support.arconnet.com/
Central Support E-mail Address: arcos.support@arconnet.com
Support hotline:
Global: +91 8080005577 (For ARCON | PAM Support Press 3)
UAE: 800035703628 (Press 1)

## [p399]

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
