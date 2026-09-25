# Graph Report - E:\Omkar\Automation\Dev Project\pam\PAM  (2026-07-28)

## Corpus Check
- Detected: 12,950 files · ~19,281,945 words under `pam/PAM`.
- **Graphed: 9,288 code files only** (6,859 `.cs` · 1,142 `.sql` · 877 `.js` · 181 `.csproj` · 126 `.java` · 27 `.cshtml` · 35 `.sln` · misc).
- **Deliberately excluded by the operator** — not in this graph: 3,570 images, 11 videos, 6 PDFs, 75 documents (`.txt`/`.html`). These are web assets and misc files; semantic extraction over them would have cost thousands of vision/transcription calls for negligible architectural value.
- Scanned with `gitignore=False` because `.gitignore:363` (`/PAM`) excludes the entire product tree. Build artifacts (`bin`, `obj`, `packages`, `.vs`, `Debug`, `Release`, `x64`, `x86`, `TestResults`, `ClientBin`, `Generated Files`) were excluded explicitly instead — 0 leaked into the corpus.
- 32 files (mostly `.json` config) parsed to zero nodes and are absent from the graph.
- Token cost: **0** — code-only corpus, so extraction was pure AST. No LLM, no API key.

## Graph Health (integrity gate)
Surfaced by the pre-labeling diagnostic; the graph is usable but these are real:
- 24,941 **dangling-endpoint edges** — references to types outside the corpus (.NET BCL, third-party assemblies). Expected for a Framework app, but it means those targets are not nodes.
- 70,879 edges **collapsed** into 269,879 unique undirected pairs (from 365,615 raw). Mostly repeated `references` to the same type from many lines in one file; an undirected simple `Graph` keeps one edge per pair. Re-run with `--directed` to preserve direction.
- 109 self-loop edges · 8,442 exact-duplicate edges.
- 1,943 weakly-connected nodes.

## Summary
- 112628 nodes · 269879 edges · 4895 communities (4132 shown, 763 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 15107 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- ARCOS Server Manager WinForms UI
- ARCON Common Data Access Layer
- Session Details & HSM Framework
- DeskInsight Desktop Streaming
- Secure SSO Application Launcher
- ACM Common Entity Objects
- Scheduled Password Change Service
- ACM Terminal Connection Launcher
- Server Framework Config Objects
- JSch SSH Keep-Alive & Buffers
- ACMO Web Common Functions
- SqlHelper Database Access
- Java-to-.NET File IO Shim
- Mobile OTP & App Type Registry
- JStream Java Stream Shim
- ACMO Web Client Bundled JS
- PKCS#11 Interop Mechanism Params
- JSch Cipher & Key Exchange
- JSch Cipher & HASH Primitives
- ACMO Audit Log Web Pages
- HSM Encryption & LUNA Operations
- ARCON Password Manager
- ACM Application Control Automation
- Application Event Logging
- Server Manager ListView Helpers
- Server Config Entity Helpers
- SSH Terminal Granados UI
- Secure Network Stream
- Services — Alert Service
- Services — SLPF
- ASM Server — Pkcs11Interop
- ACM Client — Framework CM
- ASM Server — Pkcs11Interop
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Services — SLPF
- Services — SLPF
- ASM Server — Pkcs11Interop
- ACMO Web — Client Manager
- Services — Log Archiver Service
- Services — Log Archiver Service
- Offline MultiTab — Offline API
- ACM Client — App Exe
- Services — SLPF
- ACM Common — SLPF
- ACMO Web — Client Manager
- ACM Client — App Exe
- ASM Server — Pkcs11Interop
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- MultiTab — src
- ACM Client — DQS
- Services — .Utilities.Sign Tool
- ACMO Web — Client Manager
- Services — TSPlugin Service
- ACM Client — Framework CM
- ASM Server — Pkcs11Interop
- ACM Client — SSHTerminal
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ASM Server — .PIMUD
- Services — Auto Healing
- Services — SLPF
- Common — USPSql Parameter Master
- ACM Client — SSHTerminal
- Services — Privilege User Discovery
- Services — Scheduler Service
- Services — Provisioning Service
- ACMO Web — Client Manager
- Services — Schedule Password Change
- ACM Client — DQS
- ACM Common — USPSql Parameter
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- MultiTab — src
- MultiTab — src
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- Services — SLPF
- ACM Client — SSHTerminal
- Services — SLPF
- ACM Client — SFTPTeminal
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACM Client — SFTPTeminal
- ACMO Web — Client Manager
- Services — Database Setting
- ACMO Web — Client Manager
- ACM Client — SSHTerminal
- ACM Client — Framework CM
- Services — TSPlugin Service
- ACMO Web — Portal
- Services — Schedule Password Change
- ACMO Web — Client Manager
- Services — SLPF
- Services — Provisioning Scheduler
- Services — .Smtp Send Mail.Security
- Services — SLPF
- Services — SLPF
- MultiTab — src
- ACM Client — SSHTerminal
- Services — SLPF
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Passworde Envelope Manager
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — SLPF
- ACMO Web — Client Manager
- ACM Client — SFTPTeminal
- ASM Server — Server Manager
- ACM Client — DQS
- Services — Schedule Password Change
- ACM Client — DQS
- ACM Client — Web Browser
- ACM Client — SSHTerminal
- Services — Schedule Password Change
- Services — SLPF
- Services — Password Change Vault
- Services — Schedule Password Change
- ACM Client — AS400Terminal
- Services — Password Change Vault
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACM Client — Framework CM
- ACMO Web — Web Services
- Services — Provisioning Scheduler
- ACM Client — Web Browser
- ACMO Web — Client Manager
- Onboarding — USPSql Parameter Master
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ASM Server — Pkcs11Interop
- ACMO Web — Client Manager
- ACM Client — Framework CM
- Services — .User Controls
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ASM Server — SLPF
- ACM Client — SSHTerminal
- ACM Common — Tab Strip
- ACM Common — Tab Strip
- ACM Client — SSHTerminal
- Services — SLPF
- MultiTab — src
- ASM Server — Server Manager
- ACM Client — DQS
- ACM Client — Framework CM
- Services — SLPF
- Services — Log Archiver Service
- ASM Server — Pkcs11Interop
- ACMO Web — Client Manager
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- ACM Client — STerminal Control
- ACM Common — Web References
- ACMO Web — Client Manager
- Services — Cloud File Uploader
- ASM Server — Server Manager
- ACM Client — Script Manager
- ACM Client — Framework CM
- ACMO Web — Client Manager
- Common — Enitity Objects
- Services — Password Change Vault
- Services — TSPlugin Service
- Services — SLPF
- ACMO Web — APIOnline
- ASM Server — Tab Strip
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — TSPlugin Service
- Services — Desk Insight
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Services — Log Archiver Service
- ASM Server — Pkcs11Interop
- Services — Arcon Auto Failover
- Services — Log Archiver Service
- MultiTab — src
- Services — SLPF
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — TSPlugin Service
- ACM Client — SSHTerminal
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Log Archiver Service
- ACM Client — SSHTerminal
- ASM Server — Pkcs11Interop
- ACM Client — Framework CM
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ASM Server — Pkcs11Interop
- Services — ADScanner Service ACMO
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — SSHTerminal
- ACMO Web — Portal
- ACMO Web — Portal
- Services — ADScanner Service
- ACM Client — SSHTerminal
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Schedule Password Change
- Services — Provisioning Scheduler
- ACM Client — Framework CM
- Services — TSPlugin Service
- ASM Server — Server Manager
- Services — SIEMConnector Service
- Services — Web References
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Arcon Auto Failover
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Pkcs11Interop
- ACM Common — .Utilities.Sign Tool
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Desk Insight
- Offline MultiTab — Offline API
- ACM Common — Log Images
- Services — Provisioning Service
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACM Client — SFTPTeminal
- ACM Common — .User Controls
- ACM Common — SLPF
- Services — Desk Insight
- Offline MultiTab — Offline API
- ACM Client — Script Manager
- ACM Client — RDPTerminal
- ACM Client — Oracle Query
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Desk Insight
- ASM Server — Server Manager
- Common — SLPF
- ACMO Web — Client Manager
- ACM Client — RStream Client
- ASM Server — Server Manager
- ACM Client — Framework CM
- Onboarding — OUProperties
- Onboarding — Common Functions
- Common — .IARCOSWeb API
- Services — ADScanner Service ACMO
- ACM Client — RStream Client
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACM Client — Framework CM
- Services — SLPF
- ACMO Web — Client Manager
- Services — ADScanner Service
- Services — Schedule Password Change
- Services — SLPF
- ACMO Web — Client Manager
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — Desk Insight Master
- Services — SLPF
- ACM Client — Oracle SDTerminal
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- Services — Desk Insight
- ACMO Web — User Access
- ACM Client — Biometric Finger
- ACM Common — VPNClient
- ACMO Web — Portal
- Onboarding — Common Functions Userob
- ACM Client — VNCTerminal
- Services — User On Boarding
- ACMO Web — Client Manager
- Onboarding — User Onboarding
- Services — SLPF
- Services — Log Archiver Service
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Desk Insight
- Services — Desk Insight
- ACM Client — SSHTerminal
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Log Archiver Service
- ASM Server — Server Manager
- ACM Client — Framework CM
- ACMO Web — Common Functions
- Services — TSPlugin Service
- ACM Client — DQS
- Services — SLPF
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Common — .User Controls
- Services — Log Archiver Service
- MultiTab — src
- ACM Client — SSHTerminal
- ASM Server — Server Manager
- ACMO Web — Web Services
- ACMO Web — Client Manager
- Services — PAM Agents
- Services — Desk Insight
- Services — Log Archiver Service
- Onboarding — cls Onboarding
- ASM Server — Pkcs11Interop
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Offline MultiTab — Offline API
- ACM Client — Sshkey SFTP
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ACM Client — SSHTerminal
- Services — TSPlugin Service
- Services — Log Archiver Service
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Desk Insight
- ACM Client — DQS
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACM Client — Sshkey SFTP
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ASM Server — Server Manager
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Desk Insight
- Services — TSPlugin Service
- ACM Client — SSHTerminal
- Common — Common Functions Utils
- Services — Desk Insight
- Services — TSPlugin Service
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- ACM Client — Framework CM
- Services — TSPlugin Service
- Services — APEMService
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — PAM Agents
- Services — TSPlugin Service
- Services — Server Manager
- ACM Client — Framework CM
- Services — Log Archiver Service
- Services — PAM Agents
- Services — Desk Insight
- ACM Client — Framework CM
- ACM Client — Web Browserv35
- Services — Schedule Password Change
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Services — Schedule Password Change
- ACM Client — SFTPTeminal
- Services — User On Boarding
- ASM Server — Server Manager
- ACMO Web — Portal
- ACMO Web — Provisioning Web
- Services — SLPF
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Portal
- Offline MultiTab — Offline API
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — SLPF
- ASM Server — ARC SEC
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Desk Insight
- Services — Password Change Vault
- User Discovery — ADScanner
- ACMO Web — Provisioning Web
- Common — Tab Strip
- ACM Common — User Service
- ACM Common — Enitity Objects
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — Data Sync
- MultiTab — src
- ACM Client — SSHTerminal
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — TSPlugin Service
- Services — Schedule Password Change
- MultiTab — src
- ACM Client — Arcoss SSMDesktop
- ASM Server — Server Manager
- ACM Common — Enitity Objects
- Services — PAM Agents
- MultiTab — src
- ACM Client — Framework CM
- ACM Client — VNCTerminal
- Services — Provisioning Service
- ACM Client — Web Browser
- ACMO Web — Client Manager
- User Discovery — Scanner Processor
- MultiTab — src
- ACM Client — RStream Client
- ACM Client — Smar Term
- ASM Server — Server Manager
- Services — Desk Insight
- Services — Desk Insight
- Offline MultiTab — Offline API
- Offline MultiTab — Offline API
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- Services — SLPF
- Services — TSPlugin Service
- ACM Common — Enitity Objects
- ACM Common — Custom App
- ACMO Web — Provisioning Web
- MultiTab — src
- ACM Client — Smar Term
- ACM Client — Web Browser
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — Sync Failed Password
- Services — Desk Insight
- Services — Schedule Password Change
- ASM Server — Server Manager
- ACM Client — Oracle TTerminal
- ACM Common — Enitity Objects
- ACMO Web — Client Manager
- Services — Desk Insight
- Services — Migrate Data Utility
- MultiTab — src
- ACM Client — VNCTerminal
- ASM Server — Server Manager
- ACMO Web — Provisioning Web
- ACMO Web — Client Manager
- User Discovery — IPScanner
- Services — TSPlugin Service
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Provisioning Service
- ASM Server — Server Manager
- ACM Client — RStream Client
- ACM Client — DQS
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ASM Server — .PIMUD
- ASM Server — Server Manager
- ACMO Web — Client Manager
- Offline MultiTab — Windows Service
- Offline MultiTab — Offline API
- ACM Client — Biometric Finger
- ACM Client — DQS
- ASM Server — Server Manager
- Services — Desk Insight
- Services — Migrate Data Utility
- Onboarding — Service Onboarding
- ACM Client — SSHTerminal
- Services — APEMService
- ASM Server — SLPF
- ASM Server — Server Manager
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- SSM — Arcoss SSMDesktop
- MultiTab — src
- ACM Client — Framework CM
- Services — TSPlugin Service
- Common — SData Grid View
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- ASM Server — Server Manager
- ACM Common — Ticket
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ACM Client — SSHTerminal
- ACM Common — Connection Properties
- ACM Common — Common Functions
- ACM Common — Tab Strip
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- Services — TSPlugin Service
- ASM Server — Server Manager
- ACM Client — Script Manager
- ACM Common — .User Controls
- ACM Common — S
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- Services — Provisioning Scheduler
- Services — Staging Log Sync
- MultiTab — src
- ACM Client — Framework CM
- ACMO Web — Provisioning Web
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- Services — Desk Insight
- Services — Z POC
- MultiTab — src
- MultiTab — src
- ACM Client — Sshkey SFTP
- Services — TSPlugin Service
- ASM Server — .User Controls
- ACM Common — SData Grid
- ACM Common — SLPF
- ACM Common — SSHKey Common
- PAMSSHWRAPPER — SSHKey Generation
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Offline MultiTab — Offline API
- Services — Log Manager Service
- Services — Windows Vaulting Service
- Offline MultiTab — Offline API
- ASM Server — Server Manager
- ACM Client — SSHTerminal
- Services — TSPlugin Service
- ACM Client — SSHTerminal
- ACM Common — .User Controls
- ACM Common — SEncrypt Decrypt
- ASM Server — Server Manager
- Services — Data Sync
- MultiTab — src
- MultiTab — src
- ACM Client — SFTPTeminal
- Services — TSPlugin Service
- ASM Server — Server Manager
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — Desk Insight
- Services — Log Manager Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Onboarding — Common Enum
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- Services — TSPlugin Service
- Services — Log Archiver Service
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Services — Script Scheduler
- Offline MultiTab — Offline API
- ACM Common — .User Controls
- ACM Client — Script Manager
- ASM Server — Server Manager
- Services — User On Boarding
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Schedule Password Change
- SSM — Arcoss SSMDesktop
- MultiTab — src
- ACM Client — Framework CM
- ACM Common — SEncrypt Decrypt
- Services — User On Boarding
- ACM Client — Network Devices
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — UITheme
- Services — PAM Agents
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Migrate Data Utility
- ACM Client — RStream Client
- ACM Client — Sshkey SFTP
- ACM Client — Framework CM
- ACM Common — SList View
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Common — SList View Addin
- Services — Desk Insight
- Services — Log Manager Service
- Services — Passworde Envelope Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ACMO Web — Offline API
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — User On Boarding
- Services — Windows Vaulting Service
- Offline MultiTab — Offline API
- Offline MultiTab — Offline API
- ACM Client — VNCTerminal
- ACM Client — RStream Client
- ACM Client — VNCTerminal
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Portal
- ASM Server — Server Manager
- Services — APEMService
- Services — Passworde Envelope Manager
- Services — TSPlugin Service
- Services — Windows Service Updater
- ACM Client — PAMSecure SSOApps
- ACM Client — Framework CM
- ASM Server — Enitity Objects
- Common — Password Manager
- ACM Common — UITheme
- ACMO Web — Client Manager
- Services — Schedule Password Change
- SSM — Arcoss SSMDesktop
- ACM Client — Framework CM
- ACM Common — APICalling
- ACM Client — Framework CM
- ACM Client — Framework CM
- ASM Server — Server Manager
- ACM Common — VPNClient
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — User Access
- ASM Server — Server Manager
- Common — VPNClient
- MultiTab — src
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- Common — .User Controls
- Services — Schedule Password Change
- ASM Server — Server Manager
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — Enitity Objects
- Services — Arcon File Upload
- Services — Desk Insight
- Services — Migrate Data Utility
- MultiTab — src
- ACM Client — DQS
- ACM Client — SSHTerminal
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- Services — Schedule Password Change
- Services — SLPF
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- Common — SLPF
- Common — Enitity Objects
- Services — Arcon File Upload
- Services — Desk Insight
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Staging Log Sync
- Services — TSPlugin Service
- ACM Client — Sshkey SFTP
- ACM Client — DB2TTerminal
- Services — TSPlugin Service
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Common — .PIMUD
- ACM Common — .PIMUD
- ACM Common — .User Controls
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- Services — Desk Insight
- Services — TSPlugin Service
- ACM Client — RStream Client
- ACM Client — DB2TTerminal
- ACM Client — DQS
- ACM Client — Framework CM
- Services — Auto Healing
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — PAM Agents
- Services — Arcon Auto Failover
- Services — Arcon File Upload
- Services — Desk Insight
- Services — Perf Mon IT
- Services — Provisioning Service
- Offline MultiTab — Offline API
- ACM Client — Framework CM
- ACM Client — VNCTerminal
- ACM Common — .API
- ACMO Web — Client Manager
- ACM Common — SLPF
- ACM Common — Enitity Objects
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- Services — Alert Service
- Services — PAM Agents
- Services — TSPlugin Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Log Manager Service
- Services — Password Change Vault
- Services — Provisioning Service
- Services — Schedule Password Change
- Offline MultiTab — Offline API
- SSM — Arcoss SSMDesktop
- Services — Desk Insight
- ACM Client — RStream Client
- ACM Client — Framework CM
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ACM Common — Tab Strip
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ACMO Web — Portal
- ACMO Web — User Access
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- Common — .User Controls
- Common — Enitity Objects
- Services — PAM Agents
- Services — DBSync Service
- Services — DBSync Service
- Services — Desk Insight
- Services — Perf Mon IT
- Services — TSPlugin Service
- Services — TSPlugin Service
- MultiTab — src
- Offline MultiTab — Offline API
- Offline MultiTab — Service Installer
- Offline MultiTab — Windows Service
- ACM Client — ACMCommon Functions
- ACM Client — RStream Client
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — DQS
- ACM Client — Script Manager
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Script Manager
- ASM Server — Server Manager
- ACM Common — SLPF
- ASM Server — Server Manager
- ACM Common — Enitity Objects
- ACM Common — Server Common
- ACMO Web — APIRA
- ACMO Web — Common Functions
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — Alert Service
- Common — Enitity Objects
- Services — PAM Agents
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Z POC
- Offline MultiTab — Offline API
- ACM Client — App Exe
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ACM Common — .User Controls
- ACM Common — SLPF
- ACM Common — SLPF
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .User Controls
- Common — .User Controls
- Common — SLPF
- Services — PAM Agents
- Services — PAM Agents
- Services — PAM Agents
- Services — Arcon File Upload
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Migrate Data Utility
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — User On Boarding
- Offline MultiTab — Offline API
- ACM Client — Sshkey SFTP
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — SLPF
- Common — Data Access
- Services — ADScanner Service
- Services — PAM Agents
- Services — Arcon Auto Failover
- Services — DBSync Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Staging Log Sync
- Services — TSPlugin Service
- LDAPAuthenticator
- Onboarding — SQLHelper
- Offline MultiTab — Windows Service
- ACM Client — Sshkey SFTP
- ACM Client — Web Browser
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — Sync Failed Password
- Services — Passworde Envelope Manager
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- LDAPAuthenticator — .Radius
- Services — Schedule Password Change
- ACM Common — SLPF
- ACMO Web — Provisioning Web
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — DBSync Service
- Services — Folder Sync Service
- Services — Log Manager Service
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- Services — Z POC
- LDAPAuthenticator
- MultiTab — src
- Offline MultiTab — Offline API
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Common — SLPF
- ACM Common — Enitity Objects
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — PAM Agents
- Services — Cloud File Uploader
- Services — DBSync Service
- Services — DBSync Service
- Services — Desk Insight
- Services — Provisioning Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- ACM Client — RStream Client
- SSM — Arcoss SSMDesktop
- ACM Client — Framework CM
- ACM Client — VNCTerminal
- ACMO Web — APIOnline
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- Services — TSPlugin Service
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Web Services
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — Password Manager
- Common — SLPF
- Services — PAM Agents
- Services — PAM Agents
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Password Change Vault
- Services — Schedule Password Change
- Services — Staging Log Sync
- MultiTab — src
- ASM Server — Server Manager
- ACM Common — .User Controls
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — AS400Terminal
- ACM Client — Framework CM
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ASM Server — PAM.Server Manager.Tests
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — APICalling
- Common — .PIMUD
- Common — Password Manager
- Common — SLPF
- Services — Cloud File Uploader
- Services — Cloud File Uploader
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- MultiTab — src
- ACM Client — RStream Client
- ACM Client — DQS
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Common — APICalling
- SSM — Arcoss SSMDesktop
- ASM Server — Server Manager
- ACM Common — Enitity Objects
- ACM Common — Common APICall
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — Common Functions DB
- Services — Alert Service
- Services — PAM Agents
- Services — Cloud File Uploader
- Services — Data Sync
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Migrate Data Utility
- Services — Privilege User Discovery
- Services — TSPlugin Service
- Services — TSPlugin Service
- Datum Bridge
- Datum Bridge Client
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- Services — Schedule Password Change
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Services — Active Directory Insight
- Services — Active Directory Insight
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Folder Sync Service
- Services — Passworde Envelope Manager
- Services — Scheduler Service
- Services — TSPlugin Service
- Offline MultiTab — Windows Service
- Database SQL — Arcon Pam
- Offline MultiTab — Offline API
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Script Manager
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ASM Server — Server Manager
- Services — Enitity Objects
- ACM Common — Enitity Objects
- ACM Common — Workflow Id
- ASM Server — Server Manager
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — User Access
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .Encrypt Descrypt File
- Common — SLPF
- Common — Enitity Objects
- Services — Migrate Data Utility
- Services — Perf Mon IT
- Services — Provisioning Scheduler
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Staging Log Sync
- Services — TSPlugin Service
- Services — TSPlugin Service
- Database SQL — Arcon Pam
- Offline MultiTab — Offline API
- ACM Client — PAMMulti Tab
- ACM Client — Sshkey SFTP
- ACM Client — App Exe
- ACM Client — RDPTerminal
- ASM Server — Server Manager
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- LDAPAuthenticator — .Radius
- ASM Server — Server Manager
- ASM Server — Server Manager
- ACM Common — Random String
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SLPF
- Services — Active Directory Insight
- Services — PAM Agents
- Services — Desk Insight
- Services — Desk Insight
- Services — Provisioning Scheduler
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- Services — Z POC
- MultiTab — src
- ACM Client — PAMSecure SSOApps
- ACM Client — App Exe
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ASM Server — Server Manager
- Common — Server Common Functions
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — APICalling
- Common — .PIMUD
- Common — Random String Generator
- Services — PAM Agents
- Services — Desk Insight
- Services — Desk Insight
- Services — Migrate Data Utility
- Services — Scheduler Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Datum Bridge
- Datum Bridge Client
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — .PIMUD
- ACM Common — SLPF
- ACM Common — SPlease Wait
- ACM Common — Properties
- ACMO Web — APIOnline
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — .PIMUD
- Common — .User Controls
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — SPlease Wait Control
- Common — Tab Strip
- Services — Alert Service
- Services — Cloud File Uploader
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Perf Mon IT
- Services — Provisioning Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Z POC
- Services — Z POC
- Datum Bridge
- Datum Bridge Client
- Database SQL — Arcon Pam
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — .Smtp Send
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- LDAPAuthenticator
- ACMO Web — Common Functions
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — SExport Utility
- Common — Reference Details
- Services — Active Directory Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Privilege User Discovery
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- LDAPAuthenticator
- Database SQL — Arcon Pam
- Offline MultiTab — Offline API
- Offline MultiTab — Windows Service
- ACM Client — Framework CM
- ACM Client — ACMCommon Functions
- ACM Client — RStream Client
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Arcoss SSMDesktop
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — .Radius
- ACM Common — .User Controls
- ACM Common — SLPF
- ACM Common — SLPF
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Web Services
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .Radius
- Common — SLPF
- Common — SLPF
- Services — Cloud File Uploader
- Services — Cloud File Uploader
- Services — Data Sync
- Services — DBSync Service
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Migrate Data Utility
- Services — Passworde Envelope Manager
- Services — Provisioning Scheduler
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Database SQL — Arcon Pam
- MultiTab — src
- Offline MultiTab — Offline API
- ACM Client — RStream Client
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — App Exe
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- Services — Framework CM
- ACM Client — RDPTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Common — .User Controls
- ASM Server — Server Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .User Controls
- Common — Enitity Objects
- Services — Cloud File Uploader
- Services — Cloud File Uploader
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Migrate Data Utility
- Services — Provisioning Scheduler
- Services — Schedule Password Change
- Services — Windows Vaulting Service
- Datum Bridge — NUnit Database
- Database SQL — Arcon Pam
- MultiTab — src
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Oracle Query
- ACM Client — Script Manager
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ACM Client — VNCTerminal
- ACM Common — SExport Utility
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Common — HSMCommon Function
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — User Access
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — Password Manager
- Common — S
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — Server Common Functions
- Common — Reference Details
- Services — PAM Agents
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Perf Mon IT
- Services — Provisioning Scheduler
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Scheduler Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- LDAPAuthenticator
- LDAPAuthenticator
- SSM — Arcos Compression
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — App Exe
- ACM Client — App Exe
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — RDPTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — Web Browserv35
- ACM Common — .Smtp Send
- ACM Common — .User Controls
- ACM Common — .User Controls
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Client — Network Devices
- ACM Client — Network Devices
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — User Access
- ACMO Web — User Access
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .Smtp Send Mail.Security
- Common — .User Controls
- Common — .User Controls
- Common — SLPF
- Common — SLPF
- Common — HSMCommon Function
- Services — ADScanner Service
- Services — ADScanner Service
- Services — Cloud File Uploader
- Services — DBSync Service
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Migrate Data Utility
- Services — Passworde Envelope Manager
- Services — Perf Mon IT
- Services — Privilege User Discovery
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Onboarding — IPMACManager
- MultiTab — src
- Offline MultiTab — Offline API
- ACM Client — PAMMulti Tab
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACMO Web — Client Manager
- ACM Client — Script Manager
- ACM Client — Script Manager
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — .Security.Desktop
- Services — TSPlugin Service
- ACM Common — Enitity Objects
- ACMO Web — Provisioning Web
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- Common — .PIMUD
- Common — .PIMUD
- Common — .Security.Desktop
- Common — .Smtp Send Mail.Security
- Common — S
- Common — SList View Addin
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Server Common Functions
- Common — Server Common Functions
- Services — Alert Service
- Services — Alert Service
- Services — Cloud File Uploader
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Log Manager Service
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Password Change Vault
- Services — Passworde Envelope Manager
- Services — Perf Mon IT
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- LDAPAuthenticator — Unit Testing
- Onboarding — Connection Param
- SSM — Arcoss SSMDesktop
- MultiTab — src
- ACM Client — RStream Client
- ACM Client — RStream Client
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — Sshkey SFTP
- ACM Client — Sshkey SFTP
- ACM Client — App Exe
- ACM Client — Biometric Finger
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Oracle Query
- ACM Client — RDPTerminal
- ACM Client — RDPTerminal
- ACM Client — RDPTerminal
- ACM Client — RDPTerminal
- ACM Client — Script Manager
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — APICalling
- ACM Common — .Radius
- ACM Common — .User Controls
- ACM Common — SFilter Controls
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Common — SLPF
- ACM Common — Enitity Objects
- ACMO Web — .ACMO.Test
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Encrpt Decrypt
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- Common — .Radius
- Common — .User Controls
- Common — .User Controls
- Common — App
- Common — SFilter Controls
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — VPNClient
- Services — PAM Agents
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Log Archiver Service
- Services — Migrate Data Utility
- Services — Passworde Envelope Manager
- Services — Privilege User Discovery
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Scheduler Service
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- Services — Windows Vaulting Service
- Services — Windows Vaulting Service
- MultiTab — src
- Offline MultiTab — Windows Service
- ACM Client — ACMCommon Functions
- ACM Client — PAMMulti Tab
- ACM Client — PAMSecure SSOApps
- ACM Client — SFTPTerminal.LTS.v2
- ACM Client — App Exe
- ACM Client — App Exe
- ACM Client — App My
- ACM Client — AS400Terminal
- ACM Client — DB2TTerminal
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Login ACMO
- ACM Client — MSSQLEMLocal
- ACM Client — Oracle SDTerminal
- ACM Client — Oracle TTerminal
- ACM Client — Script Manager
- ACM Client — Script Manager
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — Smar Term
- ACM Client — Smar Term
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Client — Web Browserv35
- ACM Common — .PIMUD
- ACM Common — .User Controls
- ACM Common — .User Controls
- ACM Common — Database Setting
- ACM Common — Enitity Objects
- ACM Common — User Access
- ACM Client — Network Devices
- Services — Provisioning Service
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Common Functions
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Server Manager
- Common — .User Controls
- Common — .User Controls
- Common — SLPF
- Common — SLPF
- Common — SLPF
- Common — SUtil
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Server Common Functions
- Services — Active Directory Insight
- Services — ADScanner Service
- Services — Alert Service
- Services — PAM Agents
- Services — PAM Agents
- Services — PAM Agents
- Services — Cloud File Uploader
- Services — Data Sync
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight Master
- Services — Folder Sync Service
- Services — Folder Sync Service
- Services — Folder Sync Service
- Services — Log Archiver Service
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Migrate Data Utility
- Services — Password Change Vault
- Services — Passworde Envelope Manager
- Services — Passworde Envelope Manager
- Services — Perf Mon IT
- Services — Provisioning Scheduler
- Services — Provisioning Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Script Scheduler
- Services — Script Scheduler
- Services — Staging Log Sync
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- Services — Windows Vaulting Service
- Services — Z POC
- Services — Z POC
- User Discovery — Logger
- Onboarding — Updater
- Offline MultiTab — Service Installer
- MultiTab — src
- MultiTab — src
- SSM — Arcoss SSMDesktop
- ACM Client — App Exe
- ASM Server — Server Manager
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — Oracle Query
- ACM Client — Oracle Query
- ACM Client — RDPTerminal
- ACM Client — SFTPTeminal
- ACM Client — Web Browser
- ACM Client — Web Browserv35
- ACM Common — .User Controls
- ACMO Web — Common Functions
- ACMO Web — Provisioning Web
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Common Functions
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Server Manager
- Common — .User Controls
- Common — Password Manager
- Common — SLPF
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Services — Active Directory Insight
- Services — ADScanner Service
- Services — Alert Service
- Services — Auto Healing
- Services — Services.NUnit Test
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Password Change Vault
- Services — Provisioning Service
- Services — Schedule Password Change
- Services — Schedule Password Change
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Windows Vaulting Service
- Services — Z POC
- LDAPAuthenticator
- LDAPAuthenticator
- Offline MultiTab — Offline API
- ACM Client — DQS
- ACM Client — Framework CM
- ACM Client — Framework CM
- ACM Client — RDPTerminal
- ACM Client — RDPTerminal
- ACMO Web — Client Manager
- ACM Client — Script Manager
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — VNCTerminal
- ACM Client — Web Browser
- ACM Client — Web Browser
- ACM Common — .User Controls
- ACM Common — Enitity Objects
- ACM Common — Enitity Objects
- ACM Common — Enitity Objects
- Services — User On Boarding
- ACMO Web — Portal
- ACMO Web — APIOnline
- ACMO Web — APIRA
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Staging Log
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- ASM Server — Pkcs11Interop
- Common — .User Controls
- Common — .User Controls
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Enitity Objects
- Services — ADScanner Service
- Services — PAM Agents
- Services — Cloud File Uploader
- Services — Cloud File Uploader
- Services — DBSync Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Log Manager Service
- Services — Log Manager Service
- Services — Migrate Data Utility
- Services — Privilege User Discovery
- Services — Provisioning Service
- Services — Provisioning Service
- Services — Schedule Password Change
- Services — Script Scheduler
- Services — Script Scheduler
- Services — SIEMConnector Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — Z POC
- Datum Bridge Client
- Database SQL — Arcon Pam
- Offline MultiTab — Service Installer
- ACM Client — App Exe
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — DQS
- ACM Client — Framework CM
- Services — TSPlugin Service
- ACM Client — Framework CM
- ACM Client — Oracle Query
- ACM Client — Script Manager
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Client — SSHTerminal
- ACM Common — .API.Models
- Common — USPSql Parameter Master
- ACM Common — Server Common
- ACM Common — Logger Helper
- ACM Client — Network Devices
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Session Log
- ACMO Web — Web Services
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — .API.Models
- Common — .API.Models
- Common — Password Manager
- Common — Enitity Objects
- Common — Enitity Objects
- Common — Server Common Functions
- Common — Server Common Functions
- Common — Common Functions
- Common — Common Functions
- Services — ADScanner Service
- Services — ADScanner Service ACMO
- Services — ADScanner Service ACMO
- Services — Alert Service
- Services — Desk Insight
- Services — Desk Insight
- Services — Desk Insight
- Services — Folder Sync Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Log Archiver Service
- Services — Provisioning Service
- Services — Script Scheduler
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — TSPlugin Service
- Services — User On Boarding
- Services — Windows Vaulting Service
- Datum Bridge
- Datum Bridge
- Onboarding — Common Modify Parameter
- MultiTab — src
- Offline MultiTab — Service Installer
- ACM Client — RStream Client
- ACM Client — Framework CM
- ACM Client — Login ACMO
- ACM Client — SFTPTeminal
- ACM Client — SSHTerminal
- ACM Common — SPlease Wait
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — Provisioning Web
- ACMO Web — APIOnline
- ACMO Web — APIRA
- ACMO Web — APIRA
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Staging Log
- ACMO Web — Web Services
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- ASM Server — Server Manager
- Common — Password Manager
- Common — SPlease Wait Control
- Services — PAM Agents
- Services — Auto Healing
- Services — Migrate Data Utility
- Services — Password Change Vault
- Services — Schedule Password Change
- Services — Staging Log Sync
- Services — TSPlugin Service
- Services — User On Boarding
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Offline MultiTab — Windows Service
- ACM Client — DQS
- ACMO Web — Client Manager
- ACMO Web — Client Manager
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ACMO Web — Portal
- ASM Server — Server Manager
- ASM Server — Pkcs11Interop
- Common — USPSql Parameter Master
- Services — Z POC
- Onboarding — USPSql Parameter Master
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Arcon Pam
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- Database SQL — Reporting Db
- MultiTab — src
- Database SQL — Arcon Pam
- MultiTab — pom.xml

## God Nodes (most connected - your core abstractions)
1. `System.Collections.Generic` - 2372 edges
2. `CommonFunctions` - 969 edges
3. `ARCOSEnitityObjects` - 960 edges
4. `CommonFunctions` - 902 edges
5. `CommonFunctionsACMO` - 748 edges
6. `ServerConnectionProperties` - 724 edges
7. `CommonFunctions` - 688 edges
8. `ARCONCommonLibrary` - 526 edges
9. `CommonFunctionsCM` - 516 edges
10. `ARCONS.LPF.sch` - 444 edges

## Surprising Connections (you probably didn't know these)
- `Init()` --references--> `Type`  [EXTRACTED]
  ARCON_ACM/ARCOSSSHTerminal/Common/EnumDescription.cs → ARCON_ACMO/ARCONProvisioningWebAPI/Areas/HelpPage/Views/Help/DisplayTemplates/ModelDescriptionLink.cshtml
- `GetFingerPrint` --references--> `ScanningDevices`  [EXTRACTED]
  ARCON_ACM/ARCOSBiometricFingerPrintAuthenticator/ARCONFingerScan/GetFingerPrint.cs → ARCON_ASM/ARCOSServerManager/ARCONSFramework/ARCONFingerScan/SourceAFIS.cs
- `JavaString` --inherits--> `String`  [EXTRACTED]
  ARCON_ASM/ARCOSServerManager/ARCONSFramework/ARCONSLPF/java/util/JavaString.cs → ARCON_ACM_Common/ARCONSLPF/java/String.cs
- `JavaString` --inherits--> `String`  [EXTRACTED]
  ARCON_Common/ARCONSLPF/java/util/JavaString.cs → ARCON_ACM_Common/ARCONSLPF/java/String.cs
- `JavaString` --inherits--> `String`  [EXTRACTED]
  ARCON_Services/SchedulePasswordChange/SPCService/ARCONSFramework/ARCONSLPF/java/util/JavaString.cs → ARCON_ACM_Common/ARCONSLPF/java/String.cs

## Import Cycles
- None detected.

## Communities (4895 total, 763 thin omitted)

### Community 0 - "ARCOS Server Manager WinForms UI"
Cohesion: 0.00
Nodes (331): PIMSDEventArgs, DataGridView, DataTable, ListView, ARCOSLOBStagingLogServer, Boolean, Int32, string (+323 more)

### Community 1 - "ARCON Common Data Access Layer"
Cohesion: 0.01
Nodes (97): ARCOSCommonSelectParameter, int, long, string, CommandProfile, DateTime, Int32, Int64 (+89 more)

### Community 2 - "Session Details & HSM Framework"
Cohesion: 0.00
Nodes (314): GetSessionDetails, ServiceDetailsClient, string, CommonAPIConstants, string, ATSMappingModel, List, ATSPreferencePathModel (+306 more)

### Community 3 - "DeskInsight Desktop Streaming"
Cohesion: 0.00
Nodes (251): string, ErrorMessages, Program, STAThread, ImageList, List, PySSOData, PySSOSteps (+243 more)

### Community 4 - "Secure SSO Application Launcher"
Cohesion: 0.00
Nodes (317): Program, STAThread, StaticCommonFunctions, ServerSessionLogger, ActiveWindowLog, HeaderModel, client_StateChanged(), ShellSessionStateChangedEventArgs (+309 more)

### Community 5 - "ACM Common Entity Objects"
Cohesion: 0.01
Nodes (90): ARCONUserGrpServerGrpMapping, string, ARCOSFileStorageEntity, bool, byte, Int32, long, String (+82 more)

### Community 6 - "Scheduled Password Change Service"
Cohesion: 0.00
Nodes (191): Exception, Integer, int, InetAddress, IPAddress, Platform, RuntimeException, Arrays (+183 more)

### Community 7 - "ACM Terminal Connection Launcher"
Cohesion: 0.01
Nodes (134): OpenConnnection, STAThread, LinkLabelLinkClickedEventArgs, STAThread, FormClosingEventArgs, OpenConnnection, Program, Boolean (+126 more)

### Community 8 - "Server Framework Config Objects"
Cohesion: 0.00
Nodes (522): ObjectCommonProperties, RestrictionType, Boolean, DateTime, long, ARCOSCPCSConfig, Boolean, Int32 (+514 more)

### Community 9 - "JSch SSH Keep-Alive & Buffers"
Cohesion: 0.01
Nodes (194): Buffer, byte, int, Channel, bool, byte, int, Vector (+186 more)

### Community 10 - "ACMO Web Common Functions"
Cohesion: 0.01
Nodes (94): TypesOfAccessOfSecrets, ARCOSLogsOnWebParam, ARCOSReportParam, Boolean, int, String, Arsim_ServerDetails, Boolean (+86 more)

### Community 11 - "SqlHelper Database Access"
Cohesion: 0.01
Nodes (40): SqlConnectionOwnership, SqlHelper, CommandType, DataSet, SqlCommand, SqlConnection, SqlDataReader, SqlTransaction (+32 more)

### Community 12 - "Java-to-.NET File IO Shim"
Cohesion: 0.01
Nodes (74): File, FileInfo, string, FileInputStream, FileStream, SeekOrigin, FileOutputStream, FileStream (+66 more)

### Community 13 - "Mobile OTP & App Type Registry"
Cohesion: 0.01
Nodes (148): AGWLogLevel, ARCOSAppType, ARCOSAppTypeName, String, LoginUserDetail, bool, Boolean, DateTime (+140 more)

### Community 14 - "JStream Java Stream Shim"
Cohesion: 0.01
Nodes (118): JStream, SeekOrigin, Socket, Sock, SocketOptionLevel, SocketOptionName, Stream, Hashtable (+110 more)

### Community 15 - "ACMO Web Client Bundled JS"
Cohesion: 0.01
Nodes (285): Base(), $43d7963e56408b24$export$3c52dd84024ae72c(), $43d7963e56408b24$export$410364bbb673ddbc(), $43d7963e56408b24$export$52c8ea63abd07594(), $43d7963e56408b24$export$727d9dbc4fbb948f(), $43d7963e56408b24$export$7b6804e8df61fcf5(), $43d7963e56408b24$export$92f6187db8ca6d26(), $43d7963e56408b24$export$941569448d136665() (+277 more)

### Community 16 - "PKCS#11 Interop Mechanism Params"
Cohesion: 0.01
Nodes (127): MechanismParamsFactory, bool, Mechanism, bool, NativeULong, CkSsl3KeyMatOut, bool, CkSsl3KeyMatParams (+119 more)

### Community 17 - "JSch Cipher & Key Exchange"
Cohesion: 0.01
Nodes (129): AES, MyUserInfo, String, ChangePassphrase, String, KeyGen, KnownHosts, MyUserInfo (+121 more)

### Community 18 - "JSch Cipher & HASH Primitives"
Cohesion: 0.01
Nodes (105): Cipher, int, HASH, String, IdentityFile, bool, byte, int (+97 more)

### Community 19 - "ACMO Audit Log Web Pages"
Cohesion: 0.01
Nodes (94): frmARCOSLogs, CultureInfo, DataTable, DateTime, EventArgs, int, Int32, RepeaterCommandEventArgs (+86 more)

### Community 20 - "HSM Encryption & LUNA Operations"
Cohesion: 0.01
Nodes (144): ARCSEC_EDT_DE, DateTime, List, Pkcs11Library, string, Uri, AppType, CKA (+136 more)

### Community 21 - "ARCON Password Manager"
Cohesion: 0.03
Nodes (64): ServiceDefaultPort, String, ServerConnectionProperties, AWBAPIJSONRequest, ChangePassword, ARCONApp, ArrayList, bool (+56 more)

### Community 22 - "ACM Application Control Automation"
Cohesion: 0.01
Nodes (142): ApplicationControl, AutoClosingMessageBox, ImageList, Rect, AutomationElement, bool, Boolean, CaptureProcess (+134 more)

### Community 23 - "Application Event Logging"
Cohesion: 0.01
Nodes (137): ApplicationLogger, DataRow, DataTable, Int32, String, ApplicationLog, DateTime, int (+129 more)

### Community 24 - "Server Manager ListView Helpers"
Cohesion: 0.01
Nodes (39): ArrayList, ComboBox, Panel, frmManageGroupUtility, EventArgs, MouseEventArgs, frmUserServiceGroupV2, ManageService (+31 more)

### Community 25 - "Server Config Entity Helpers"
Cohesion: 0.01
Nodes (65): ArconGenServiceConfiguration, ARCOSSStagingLogServer, Boolean, Int32, String, DualFactorIPRange, Int32, String (+57 more)

### Community 26 - "SSH Terminal Granados UI"
Cohesion: 0.01
Nodes (143): Button, Container, Label, TextBox, ChangePassphrase, CipherFactory, MAC, MACFactory (+135 more)

### Community 27 - "Secure Network Stream"
Cohesion: 0.01
Nodes (127): AsyncCallback, bool, Exception, IAsyncResult, SeekOrigin, SecureNetworkStream, AsyncCallback, bool (+119 more)

### Community 28 - "Services — Alert Service"
Cohesion: 0.02
Nodes (98): SMTPSettings, bool, int, MailClientAuthenticationMethod, ProxyHttpConnectAuthMethod, ProxyType, SecurityMode, string (+90 more)

### Community 29 - "Services — SLPF"
Cohesion: 0.01
Nodes (98): ITransferProtocol, ScpFrom, Stream, ScpTo, Stream, Hashtable, UIKeyboardInteractive, Scp (+90 more)

### Community 30 - "ASM Server — Pkcs11Interop"
Cohesion: 0.00
Nodes (250): bool, CkDsaParameterGenParam, bool, CkGcmParams, bool, CkGostR3410KeyWrapParams, bool, CkKeyDerivationStringData (+242 more)

### Community 31 - "ACM Client — Framework CM"
Cohesion: 0.01
Nodes (87): CommonFunctions, DataCapturedEventArgs, MonitorPacket, Bitmap, bool, Boolean, Byte, CommandType (+79 more)

### Community 32 - "ASM Server — Pkcs11Interop"
Cohesion: 0.02
Nodes (31): uint, CKF, uint, CKZ, Dictionary, MiscSettings, Net.Pkcs11Interop.HighLevelAPI40.MechanismParams, Net.Pkcs11Interop.HighLevelAPI.Factories (+23 more)

### Community 33 - "Services — Schedule Password Change"
Cohesion: 0.01
Nodes (76): CertificateContext, CertificateInfo, DateTime, IntPtr, RSA, StringCollection, X509Certificate, Certificate (+68 more)

### Community 34 - "ACMO Web — Client Manager"
Cohesion: 0.01
Nodes (107): AFMFont(), arrayClone(), asciiSlice(), base64Slice(), bi_reverse(), build_tree(), checkIEEE754(), checkWidth() (+99 more)

### Community 35 - "ACMO Web — Client Manager"
Cohesion: 0.01
Nodes (111): AccessLogRequest, DateTime, int, string, ARCOSWorkflowActionXMLFormat, ARCOSWorkflowDetails, Boolean, DateTime (+103 more)

### Community 36 - "ASM Server — Server Manager"
Cohesion: 0.03
Nodes (56): IPEndPoint, ARCOSCPCSConfig, Boolean, int, Int32, String, UserAccessControlSettings, Boolean (+48 more)

### Community 37 - "Services — SLPF"
Cohesion: 0.02
Nodes (69): CipherSuites, ClientHandshakeLayer, SslAlgorithms, bool, byte, MD5, RNGCryptoServiceProvider, RSACryptoServiceProvider (+61 more)

### Community 38 - "Services — SLPF"
Cohesion: 0.01
Nodes (122): int, string, SecurityConstants, AlertLevel, bool, VerifyEventArgs, DHKeyGeneration, byte (+114 more)

### Community 39 - "ASM Server — Pkcs11Interop"
Cohesion: 0.01
Nodes (59): CKR, bool, byte, Dictionary, List, string, ulong, Pkcs11Uri (+51 more)

### Community 40 - "ACMO Web — Client Manager"
Cohesion: 0.01
Nodes (63): frmProfileCreation, DataTable, EventArgs, int, string, frmUpdateProfile, DataTable, EventArgs (+55 more)

### Community 41 - "Services — Log Archiver Service"
Cohesion: 0.01
Nodes (159): ARCONDeskInsightMaster, IContainer, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller (+151 more)

### Community 42 - "Services — Log Archiver Service"
Cohesion: 0.02
Nodes (138): ARCOSLogArchiverServiceSettings, ARCOSVideoLogFile, Boolean, DateTime, String, ARCOSApp, ARCOSLogArchiverService, Bitmap (+130 more)

### Community 43 - "Offline MultiTab — Offline API"
Cohesion: 0.01
Nodes (163): ActionExecutedContext, ActionExecutingContext, ActionFilterAttribute, APP_DAL, APP_Common.Helpers, APP_Common.Extensions, APP.Common, APP_DAL.EFModels (+155 more)

### Community 44 - "ACM Client — App Exe"
Cohesion: 0.01
Nodes (140): frmARCOSAppExeTerminal, ApplicationIdle, Bitmap, bool, Button, byte, ContextMenuStrip, DllImport (+132 more)

### Community 45 - "Services — SLPF"
Cohesion: 0.01
Nodes (95): HostKey, byte, int, String, HostKeyRepository, int, KnownHosts, ArrayList (+87 more)

### Community 46 - "ACM Common — SLPF"
Cohesion: 0.01
Nodes (133): InputStream, SeekOrigin, InputStreamWrapper, Stream, ChannelSftp, Header, InputStreamGet, bool (+125 more)

### Community 47 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (92): RDPSServerdetails, ARCOSServiceReference, Boolean, String, PasswordGenerator, Boolean, HttpBrowserCapabilities, ExportLog (+84 more)

### Community 48 - "ACM Client — App Exe"
Cohesion: 0.02
Nodes (103): FormClosingEventArgs, frmWinAppOptions, Boolean, DialogResult, EventArgs, FormClosingEventArgs, Int32, String (+95 more)

### Community 49 - "ASM Server — Pkcs11Interop"
Cohesion: 0.01
Nodes (121): CKC, CKD, CKG, CKH, CKK, CKM, CKN, CKO (+113 more)

### Community 50 - "ASM Server — Server Manager"
Cohesion: 0.02
Nodes (20): frmServersDMZSupport, DataTable, EventArgs, ListViewItem, MouseEventArgs, frmUserServiceGroup, BindingSource, Boolean (+12 more)

### Community 51 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (74): ARCOSSessionCommandLogAPI2, Boolean, DataTable, DateTime, Hashtable, Int32, PrincipalPermission, ScriptMethod (+66 more)

### Community 52 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (248): absCeil(), absFloor(), absRound(), add$1(), addFormatToken(), addParseToken(), addRegexToken(), addSubtract() (+240 more)

### Community 53 - "MultiTab — src"
Cohesion: 0.03
Nodes (64): Accordion, ColorPicker, DataFormat, Document, TwoFAActivationRA, DraggingTabPaneSupport, Tab, TabPane (+56 more)

### Community 54 - "ACM Client — DQS"
Cohesion: 0.02
Nodes (38): DB2Browser, DB2Node, Boolean, int, string, StringCollection, SqlBrowser, SqlNode (+30 more)

### Community 55 - "Services — .Utilities.Sign Tool"
Cohesion: 0.01
Nodes (139): AllocMethod, AuthenticodeTools, RevocationCheckFlags, SignCheck, StateAction, TrustProviderFlags, UiChoice, UIContext (+131 more)

### Community 56 - "ACMO Web — Client Manager"
Cohesion: 0.01
Nodes (97): HttpWebRequest, ServerSessionLogger, SMServiceObject, frmArsimCreateServerProfile, DataTable, DropDownList, EventArgs, int (+89 more)

### Community 57 - "Services — TSPlugin Service"
Cohesion: 0.02
Nodes (45): Int32, ServiceTypeCF, Boolean, ARCOSVPNDetails, Boolean, string, ARCOSVPNTunnel, Boolean (+37 more)

### Community 58 - "ACM Client — Framework CM"
Cohesion: 0.01
Nodes (84): Channel, ChannelFactory, LocalToRemoteChannelFactory, RemoteToLocalChannelFactory, SynchronizedSocket, SynchronizedSSHChannel, AsyncCallback, bool (+76 more)

### Community 59 - "ASM Server — Pkcs11Interop"
Cohesion: 0.01
Nodes (216): DllImport, int, IntPtr, MarshalAs, NativeMethods, IntPtr, UnmanagedLibrary, IntPtr (+208 more)

### Community 60 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (51): ArrayList, PaintEventArgs, Graphics, IntPtr, RoundRectColors, DllImport, IntPtr, Win32 (+43 more)

### Community 61 - "ASM Server — Server Manager"
Cohesion: 0.02
Nodes (86): ARCOSServerValues, Boolean, Int32, String, ARCOSAPISynController, DataTable, DateTime, HttpGet (+78 more)

### Community 62 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (36): ARCOSDelegation, DelegationDetail, DelegationMaster, DateTime, frmConnection, UGrpChildren, UserGroups, ArrayList (+28 more)

### Community 63 - "ASM Server — .PIMUD"
Cohesion: 0.02
Nodes (73): PIMPRStatus, PIMUDEventArgs, Boolean, String, MSSQL, Boolean, DataTable, String (+65 more)

### Community 64 - "Services — Auto Healing"
Cohesion: 0.04
Nodes (46): CommandType, ARCOSApp, Boolean, Int32, Boolean, Form, String, AWBAPIJSONRequest (+38 more)

### Community 65 - "Services — SLPF"
Cohesion: 0.02
Nodes (78): bool, Exception, ManualResetEvent, object, WaitHandle, AsyncAcceptResult, AsyncResult, ArrayList (+70 more)

### Community 67 - "ACM Client — SSHTerminal"
Cohesion: 0.01
Nodes (154): Button, GroupBox, IContainer, Label, TextBox, FileMask, Button, IContainer (+146 more)

### Community 68 - "Services — Privilege User Discovery"
Cohesion: 0.02
Nodes (77): CheckTargetConnection, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent, DB2, DB2DBConnection (+69 more)

### Community 69 - "Services — Scheduler Service"
Cohesion: 0.03
Nodes (41): ARCOSMailBox, Boolean, Int32, String, ReportDownloadLog, bool, int, string (+33 more)

### Community 70 - "Services — Provisioning Service"
Cohesion: 0.03
Nodes (62): DateTime, Log, EventArgs, ILog, Process, String, ActiveDirectory, ILog (+54 more)

### Community 71 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (53): _addToZip(), _api_scope(), arrayMove(), _buttonInit(), _buttonSourced(), ColReorder(), ColumnControl(), Criteria() (+45 more)

### Community 72 - "Services — Schedule Password Change"
Cohesion: 0.07
Nodes (25): ConnectingForm, MoveToRemoteFolder, MoveToRemoteFolder, frmTestForm1, frmChangePassword, ArrayList, Boolean, DataSet (+17 more)

### Community 73 - "ACM Client — DQS"
Cohesion: 0.02
Nodes (27): StringCollection, ISQLBrowser, Boolean, StringCollection, TreeNode, IBrowser, StringCollection, TreeNode (+19 more)

### Community 74 - "ACM Common — USPSql Parameter"
Cohesion: 0.02
Nodes (3): USPSqlParameterMaster, SqlParameter, String

### Community 75 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (54): SSH2ConnectionInfo, DataFragment, SSH2DataReader, SSHConnection, SynchronizedPacketReceiver, AuthenticationResult, BigInteger, bool (+46 more)

### Community 76 - "ACM Client — SSHTerminal"
Cohesion: 0.01
Nodes (101): AddResourceTable(), Assembly, Assembly, ResourceManager, string, StringResources, ArrayList, IEnumerator (+93 more)

### Community 77 - "MultiTab — src"
Cohesion: 0.02
Nodes (82): AnnotatedField, AnnotatedMethod, ApiController, Application, ArrayList, Button, Control, DefaultHttpClient (+74 more)

### Community 78 - "MultiTab — src"
Cohesion: 0.01
Nodes (27): Composite, CTabItem, DatagramSocket, EventListener, GridBagConstraints, JTextField, InvokeProgram, Override (+19 more)

### Community 79 - "ACM Client — SSHTerminal"
Cohesion: 0.01
Nodes (75): int, IntPtr, string, ContainerInterThreadUIService, CService, DragEventArgs, Form, Keys (+67 more)

### Community 80 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (97): bool, FieldInfo, float, int, string, ValueType, ConfigBoolElementAttribute, ConfigElementAttribute (+89 more)

### Community 81 - "Services — SLPF"
Cohesion: 0.02
Nodes (83): bool, ICryptoTransform, int, KeyedHashAlgorithm, CipherDefinition, CipherSuite, Ssl3CipherSuites, bool (+75 more)

### Community 82 - "ACM Client — SSHTerminal"
Cohesion: 0.01
Nodes (133): frmSearchFiles, bool, EventArgs, int, Int32, LinkLabelLinkClickedEventArgs, Message, MouseEventArgs (+125 more)

### Community 83 - "Services — SLPF"
Cohesion: 0.01
Nodes (61): CommandLineParams, IEnumerator, NameAttribute, ArrayList, CertificateNameInfo, DistinguishedName, Array, ArrayList (+53 more)

### Community 84 - "ACM Client — SFTPTeminal"
Cohesion: 0.03
Nodes (36): ConnectionState, MainLTS, AsyncMethodCompletedEventArgs, bool, Boolean, CancelEventArgs, Color, ColumnClickEventArgs (+28 more)

### Community 85 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (125): a(), aa(), ai(), ao(), As(), at(), average(), b() (+117 more)

### Community 86 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (71): AtsConfiguration, ARCOSObjectTypes, frmARCONApplicationLogs, bool, DateTime, EventArgs, int, Int32 (+63 more)

### Community 87 - "ACM Client — SFTPTeminal"
Cohesion: 0.03
Nodes (39): AsyncMethodCompletedEventArgs, bool, Boolean, CancelEventArgs, Color, ColumnClickEventArgs, ConnectionState, Control (+31 more)

### Community 88 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (45): AjaxAdapter(), AllowClear(), ArrayAdapter(), AttachBody(), AttachContainer(), BaseAdapter(), BaseSelection(), callDep() (+37 more)

### Community 89 - "Services — Database Setting"
Cohesion: 0.02
Nodes (79): ConnectionParam, ArrayList, bool, Boolean, String, ConnectionParam_MYSQL, ArrayList, bool (+71 more)

### Community 90 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (70): frmACViewProfile, EventArgs, RepeaterCommandEventArgs, frmAssignedViewProfile, DataTable, EventArgs, RepeaterCommandEventArgs, String (+62 more)

### Community 91 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (38): EventArgs, bool, DllImport, Entry, Keys, string, ContainerConnectionCommandTarget, ContainerGlobalCommandTarget (+30 more)

### Community 92 - "ACM Client — Framework CM"
Cohesion: 0.02
Nodes (73): RemoteToLocalChannelProfile, ConfigBoolElementAttribute, ConfigElementAttribute, ConfigEnumElementAttribute, ConfigFlagElementAttribute, ConfigFloatElementAttribute, ConfigIntElementAttribute, ConfigStringArrayElementAttribute (+65 more)

### Community 93 - "Services — TSPlugin Service"
Cohesion: 0.02
Nodes (83): ChannelType, string, PrivateKeyFileHeader, SCPFileTransferStatus, SCPClientException, SCPClientInvalidStatusException, SCPClientTimeoutException, SFTPFileTransferStatus (+75 more)

### Community 94 - "ACMO Web — Portal"
Cohesion: 0.02
Nodes (45): AjaxAdapter(), AllowClear(), ArrayAdapter(), AttachBody(), AttachContainer(), BaseAdapter(), BaseSelection(), callDep() (+37 more)

### Community 95 - "Services — Schedule Password Change"
Cohesion: 0.03
Nodes (55): DataRow, ARCOSApp, Boolean, Int32, ARCOSSPCService, bool, Boolean, EventArgs (+47 more)

### Community 96 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (160): addIfString(), addListener(), addPointsBelow(), autoSkip(), axisFromPosition(), BACKGROUND_COLORS, beforeDatasetDraw(), beforeDatasetsDraw() (+152 more)

### Community 97 - "Services — SLPF"
Cohesion: 0.02
Nodes (55): SignatureDSA, CryptoStream, DSAParameters, SHA1CryptoServiceProvider, KeyPairGenRSA, SignatureDSA, SignatureRSA, HostKey (+47 more)

### Community 98 - "Services — Provisioning Scheduler"
Cohesion: 0.01
Nodes (100): string, ApplicationSettings, string, Constants, Button, GroupBox, IContainer, Label (+92 more)

### Community 99 - "Services — .Smtp Send Mail.Security"
Cohesion: 0.01
Nodes (109): CertProvider, Button, ComboBox, GroupBox, IContainer, Label, CertValidator, Button (+101 more)

### Community 100 - "Services — SLPF"
Cohesion: 0.02
Nodes (78): MD2, bool, int, MD2CryptoServiceProvider, MD4, bool, int, MD4CryptoServiceProvider (+70 more)

### Community 101 - "Services — SLPF"
Cohesion: 0.02
Nodes (67): CompressionAlgorithm, bool, byte, ICryptoTransform, int, KeyedHashAlgorithm, ulong, RecordLayer (+59 more)

### Community 102 - "MultiTab — src"
Cohesion: 0.06
Nodes (21): APIController, JSONArray, JSONObject, MasterChildServiceData, SuppressWarnings, TreeItem, User, ConfigurationDetails (+13 more)

### Community 103 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (29): AsyncMethodCompletedEventArgs, bool, CancelEventArgs, Color, ColumnClickEventArgs, ConnectionState, Control, DragEventArgs (+21 more)

### Community 104 - "Services — SLPF"
Cohesion: 0.02
Nodes (56): bool, int, string, StringBuilder, ushort, ActionCode, CharKind, HandlerAdapter (+48 more)

### Community 105 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (15): di(), be, e(), Fi, Fs, G, pi, Qt (+7 more)

### Community 106 - "ACMO Web — Portal"
Cohesion: 0.03
Nodes (36): selected(), AjaxAdapter(), AllowClear(), ArrayAdapter(), AttachBody(), BaseAdapter(), BaseSelection(), callDep() (+28 more)

### Community 107 - "Services — Passworde Envelope Manager"
Cohesion: 0.02
Nodes (57): EncryptionDecryption, Boolean, Byte, DataTable, List, string, clsLog, ExceptionLog (+49 more)

### Community 108 - "ASM Server — Server Manager"
Cohesion: 0.02
Nodes (38): AssemblyDetails, Assembly, DateTime, ARCONApp, Boolean, Form, Int32, String (+30 more)

### Community 109 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (30): SqlDataReader, ARCOSLogDetails, ARCOSLogger, ARCOSUpdater, CommonFunctionsUserob, Servers, ServiceOnboarding, UserOnboarding (+22 more)

### Community 110 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (73): UCSSOMenu, EventArgs, UCSSOPreference, Boolean, EventArgs, USPSqlParameterMaster, UCSSOResponseMessage, Boolean (+65 more)

### Community 111 - "Services — SLPF"
Cohesion: 0.02
Nodes (27): byte, CompatibilityLayer, CompatibilityResult, ProtocolVersion, Ssl3ClientHandshakeLayer, Ssl3ServerHandshakeLayer, SecureProtocol, byte (+19 more)

### Community 112 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (16): d(), f(), i(), Ln, mo, ps, Qi, Qn (+8 more)

### Community 113 - "ACM Client — SFTPTeminal"
Cohesion: 0.03
Nodes (38): Boolean, ARCOSSFTPPrivileges, bool, DragEventArgs, DragAndDropListView, AsyncMethodCompletedEventArgs, bool, Boolean (+30 more)

### Community 114 - "ASM Server — Server Manager"
Cohesion: 0.02
Nodes (16): ArconCustomCommandConfig, Int64, ReconciliationSchedulerFunctions, DataTable, String, ServicesParamConfigFunctions, DataTable, String (+8 more)

### Community 115 - "ACM Client — DQS"
Cohesion: 0.02
Nodes (37): QueryForm, ResultsTabType, WordAndPosition, ArrayList, bool, Color, Control, DataGridView (+29 more)

### Community 116 - "Services — Schedule Password Change"
Cohesion: 0.02
Nodes (91): bool, ICryptoTransform, ARCFourManaged, CipherMode, KeySizes, PaddingMode, RNGCryptoServiceProvider, RC4 (+83 more)

### Community 117 - "ACM Client — DQS"
Cohesion: 0.03
Nodes (18): MRUFileAddedEventArgs, string, MainForm, Bitmap, bool, byte, CaptureProcess, DllImport (+10 more)

### Community 118 - "ACM Client — Web Browser"
Cohesion: 0.02
Nodes (76): BrowserCommands, CommandStateEventArgs, TextChangedEventArgs, string, CWPRETSTRUCT, frmARCOSWebBrowser, HookType, LASTINPUTINFO (+68 more)

### Community 119 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (54): ArrayList, bool, FormWindowState, int, Rectangle, string, ContainerOptions, GFrameStyle (+46 more)

### Community 120 - "Services — Schedule Password Change"
Cohesion: 0.02
Nodes (51): MyPipedInputStream, PassiveInputStream, PassiveOutputStream, PipedInputStream, bool, byte, int, MethodImpl (+43 more)

### Community 121 - "Services — SLPF"
Cohesion: 0.02
Nodes (109): AsyncCallback, IAsyncResult, IntPtr, CertificateChain, AuthType, CertificateChainOptions, CertificateStatus, KeyUsage (+101 more)

### Community 122 - "Services — Password Change Vault"
Cohesion: 0.02
Nodes (95): Connect, bool, ConcurrentBag, ForwardedPortLocal, ILog, SshClient, string, Tuple (+87 more)

### Community 123 - "Services — Schedule Password Change"
Cohesion: 0.02
Nodes (71): AsyncResult, byte, DataType, int, TransferItem, XBuffer, ArrayList, AsyncCallback (+63 more)

### Community 124 - "ACM Client — AS400Terminal"
Cohesion: 0.02
Nodes (72): AccessibleTreeItem, frmARCOSAppMySQLAdministrator, ApplicationIdle, Bitmap, byte, EventArgs, IContainer, KeyEventArgs (+64 more)

### Community 125 - "Services — Password Change Vault"
Cohesion: 0.03
Nodes (68): IpResolver, IPAddress, DatabaseCrud, BatchProcessorMap, ComponentMasterMap, ConfigurationMap, DomainMap, GenericSchedulerSettingsMap (+60 more)

### Community 126 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (139): addIfString(), addListener(), addPointsBelow(), autoSkip(), axisFromPosition(), BACKGROUND_COLORS, beforeDatasetDraw(), beforeDatasetsDraw() (+131 more)

### Community 127 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (34): AjaxAdapter(), AllowClear(), ArrayAdapter(), AttachBody(), BaseAdapter(), BaseSelection(), callDep(), CloseOnSelect() (+26 more)

### Community 128 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (46): StringBuilder, SSH1ConnectionInfo, SSH1DataReader, AuthenticationResult, bool, Exception, int, ISSHChannelEventReceiver (+38 more)

### Community 129 - "ACMO Web — Web Services"
Cohesion: 0.03
Nodes (72): EncryptionDecryption_Web, String, ARCONOpenSourceService, RequestAssignedServiceList, CacheEntryUpdateArguments, int, long, string (+64 more)

### Community 130 - "Services — Provisioning Scheduler"
Cohesion: 0.02
Nodes (70): Common, ILog, List, ExtensionMethods, ProvisioningClient, HttpClient, ILog, string (+62 more)

### Community 131 - "ACM Client — Web Browser"
Cohesion: 0.03
Nodes (60): ImageRecordProcessDetails, IntPtr, APIAuthToken, APIConfig, VideoParameterDetails, WebdtAuthToken, AppEricssionSSO, DllImport (+52 more)

### Community 132 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (76): at(), b(), beforeUpdate(), Bi(), Bn(), buildTicks(), ca, _calculateBarIndexPixels() (+68 more)

### Community 134 - "Services — Schedule Password Change"
Cohesion: 0.01
Nodes (69): bool, HashAlgorithm, int, Ssl3HandshakeMac, bool, HashAlgorithm, int, Ssl3RecordMAC (+61 more)

### Community 136 - "ASM Server — Pkcs11Interop"
Cohesion: 0.02
Nodes (93): bool, NativeULong, CkWtlsKeyMatOut, bool, CkWtlsKeyMatParams, bool, CkWtlsMasterKeyDeriveParams, bool (+85 more)

### Community 137 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (60): frmARCONApiLogs, bool, DataTable, DateTime, EventArgs, int, Int32, frmARCONApiReqResLogs (+52 more)

### Community 138 - "ACM Client — Framework CM"
Cohesion: 0.02
Nodes (52): CipherAlgorithm, MACAlgorithm, SSHProtocol, CipherFactory, MACFactory, byte, int, Base64 (+44 more)

### Community 139 - "Services — .User Controls"
Cohesion: 0.01
Nodes (82): DgvDateRangeColumnFilter, ComboBox, DateTimePicker, IContainer, DgvCheckBoxColumnFilter, CheckBox, ComboBox, IContainer (+74 more)

### Community 140 - "Services — Schedule Password Change"
Cohesion: 0.01
Nodes (66): LogEntry, OneTimeToken, XwdHistoryLog, ARCONRecon, IContainer, Program, STAThread, ProjectInstaller (+58 more)

### Community 141 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (92): appendContent(), AudioTrackList(), BoxPosition(), classRegExp(), _cleanUpEvents(), clearCacheForPlayer(), computedStyle(), computeLinePos() (+84 more)

### Community 142 - "ASM Server — SLPF"
Cohesion: 0.02
Nodes (51): MyUserInfo, String, MyProgressMonitor, MyUserInfo, Sftp, ElapsedEventArgs, int, long (+43 more)

### Community 143 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (55): AutoResetEvent, bool, int, IPAddress, IWin32Window, Socket, string, ISocketWithTimeoutClient (+47 more)

### Community 144 - "ACM Common — Tab Strip"
Cohesion: 0.02
Nodes (67): FATabStrip, bool, CollectionChangeEventArgs, Color, ContextMenuStrip, ControlCollection, EventArgs, Font (+59 more)

### Community 145 - "ACM Common — Tab Strip"
Cohesion: 0.03
Nodes (50): FATabStripItem, bool, Control, Image, RectangleF, Size, string, FATabStripItemCollection (+42 more)

### Community 146 - "ACM Client — SSHTerminal"
Cohesion: 0.05
Nodes (44): ValueType, DescriptionCollection(), For(), FromDescription(), FromName(), GetDescription(), GetName(), Init() (+36 more)

### Community 147 - "Services — SLPF"
Cohesion: 0.02
Nodes (46): InputStream, ChannelExec, bool, Stream, String, ChannelSession, byte, ChannelSubsystem (+38 more)

### Community 148 - "MultiTab — src"
Cohesion: 0.02
Nodes (44): BufferedImage, DWORD, HANDLE, HMODULE, IntByReference, JsonInclude, JsonProperty, User (+36 more)

### Community 149 - "ASM Server — Server Manager"
Cohesion: 0.03
Nodes (33): frmPleaseWait, Button, IContainer, Label, Panel, KeyEventArgs, frmLogModule, LogNavigator (+25 more)

### Community 150 - "ACM Client — DQS"
Cohesion: 0.03
Nodes (45): DbClientFactory, string, ConnectForm, EventArgs, Message, ConnectionSettings, ConnectionType, ServerList (+37 more)

### Community 151 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (43): bool, byte, HMACSHA1, MACSHA1, BlowfishCipher1, TripleDESCipher1, BlowfishCipher2, RijindaelCipher2 (+35 more)

### Community 152 - "Services — SLPF"
Cohesion: 0.02
Nodes (20): bool, byte, string, Extension, CertificateContext, CertificateInfo, DateTime, IntPtr (+12 more)

### Community 153 - "Services — Log Archiver Service"
Cohesion: 0.02
Nodes (119): LogImageType, LogOrderType, ARCOSLogArchiverServiceSettings, ARCOSVideoLogFile, LogImageType, LogOrderType, Boolean, DateTime (+111 more)

### Community 154 - "ASM Server — Pkcs11Interop"
Cohesion: 0.02
Nodes (78): List, bool, CkOtpParam, bool, CkOtpParams, bool, IList, List (+70 more)

### Community 155 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (25): aa(), addBox(), Ae(), afterDatasetsUpdate(), configure(), d(), Di(), generateLabels() (+17 more)

### Community 156 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (36): bool, Exception, AgentForwadPacketType, AgentForwardingChannel, IAgentForward, byte, int, SimpleMemoryStream (+28 more)

### Community 157 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (50): Keys, Thread, ThreadStart, UILibUtil, Container, KeyEventArgs, Keys, HotKey (+42 more)

### Community 158 - "ACM Client — STerminal Control"
Cohesion: 0.03
Nodes (42): bool, Container, Control, DragEventArgs, EventArgs, Graphics, Image, int (+34 more)

### Community 159 - "ACM Common — Web References"
Cohesion: 0.02
Nodes (21): ARCOSServiceValidationBAParam, ARCOSSessionLog, ARCOSWebDT, ConfigIds, ObjectCommonProperties, PriorityMaster, RecordStatus, SessionActivityLogs (+13 more)

### Community 160 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (40): addAll(), addPageItem(), beginClip(), bottomMostContext(), calculatePageHeight(), cloneLine(), createMetadata(), createPatterns() (+32 more)

### Community 161 - "Services — Cloud File Uploader"
Cohesion: 0.02
Nodes (18): ARCOSServiceValidationBAParam, ARCOSSessionLog, ARCOSWebDT, ObjectCommonProperties, PriorityMaster, RecordStatus, UserDualFactorOTP, bool (+10 more)

### Community 162 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (30): ARCOSCRITICALWFM, DataRow, Object, Boolean, Int32, Computers, Int32, string (+22 more)

### Community 163 - "ACM Client — Script Manager"
Cohesion: 0.03
Nodes (40): ComboBox, DialogResult, frmOracleClientOptions, Boolean, DialogResult, EventArgs, FormClosingEventArgs, Message (+32 more)

### Community 164 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (40): ChannelProfile, ChannelProfileCollection, LocalToRemoteChannelProfile, ArrayList, bool, IEnumerator, ProtocolType, string (+32 more)

### Community 165 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (124): callbackify(), s(), A(), _applyDecoratedDescriptor(), assign(), at(), b(), be() (+116 more)

### Community 166 - "Common — Enitity Objects"
Cohesion: 0.02
Nodes (95): RecordStatus, MultipleIntefaces, DateTime, int, String, WindowsDCOM, Boolean, DateTime (+87 more)

### Community 167 - "Services — Password Change Vault"
Cohesion: 0.02
Nodes (80): ConnectivityPing, bool, ILog, string, Dispatcher, bool, ILog, int (+72 more)

### Community 168 - "Services — TSPlugin Service"
Cohesion: 0.03
Nodes (30): IARCOSWebAPI, Boolean, Byte, CommandType, DataSet, DataTable, DateTime, Int32 (+22 more)

### Community 169 - "Services — SLPF"
Cohesion: 0.03
Nodes (59): byte, IntPtr, short, CryptoMethod, CryptoProvider, PUBLICKEYSTRUC, RC4UnmanagedTransform, int (+51 more)

### Community 170 - "ACMO Web — APIOnline"
Cohesion: 0.04
Nodes (48): WebAPIParam, DataTable, DateTime, Hashtable, IDataParameter, string, IARCOSWebAPI, ARCOSWebDT (+40 more)

### Community 171 - "ASM Server — Tab Strip"
Cohesion: 0.02
Nodes (54): ICaptionSupport, FATabStripCloseButton, bool, Graphics, Rectangle, ToolStripProfessionalRenderer, FATabStripMenuGlyph, bool (+46 more)

### Community 172 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (9): Ue(), Fi, Fs, G, pi, Qt, remove(), Wi (+1 more)

### Community 173 - "ACMO Web — Portal"
Cohesion: 0.02
Nodes (67): actOnCachedSelection(), addStyle(), _appendLineBreak(), _applySelectorRules(), areMatchingAllready(), autoLink(), _changeLinks(), _checkAttribute() (+59 more)

### Community 174 - "Services — TSPlugin Service"
Cohesion: 0.03
Nodes (47): BigInteger, Random, DSAKeyPair, DSAPublicKey, BigInteger, byte, IKeyWriter, ISigner (+39 more)

### Community 175 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (32): ARCONDeskInsightService, bool, DateTime, EventArgs, int, SessionChangeDescription, String, Timer (+24 more)

### Community 176 - "ACM Client — SSHTerminal"
Cohesion: 0.02
Nodes (86): frmScriptManager, Button, ColumnHeader, ComboBox, ContextMenuStrip, IContainer, ImageList, Label (+78 more)

### Community 177 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (36): Login, EventArgs, LoginInfo, int, ProxyHttpConnectAuthMethod, ProxyType, string, ARCONConnectionMethod (+28 more)

### Community 178 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (54): at(), b(), beforeUpdate(), buildTicks(), _calculateBarIndexPixels(), cn(), dn(), ea() (+46 more)

### Community 179 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (26): B(), be, Ce, D(), e(), getDataAttributes(), H(), I() (+18 more)

### Community 180 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (28): frmCreateUserProfile, DataTable, EventArgs, string, CommonFunctionsLocal, DataColumn, DataRow, DataTable (+20 more)

### Community 181 - "ASM Server — Server Manager"
Cohesion: 0.03
Nodes (47): CertValidator, bool, EventArgs, string, X509Certificate2, frmCustomCommandConfigurationpopup, DataRow, EventArgs (+39 more)

### Community 182 - "Services — Log Archiver Service"
Cohesion: 0.04
Nodes (44): ConfigDataType, LOBConfig, LOBConfigMaster, Boolean, Int32, String, LOBConfig, LOBConfigMaster (+36 more)

### Community 183 - "ASM Server — Pkcs11Interop"
Cohesion: 0.04
Nodes (31): bool, Mechanism, bool, CkVersion, IntPtr, NativeULong, CK_ATTRIBUTE, IntPtr (+23 more)

### Community 184 - "Services — Arcon Auto Failover"
Cohesion: 0.03
Nodes (43): ARCONPAM_Validate_SetkeyCompletedEventArgs, ARCOSServiceValidationBAParam, ARCOSSessionLog, ARCOSSqlParameter, ARCOSWebDT, ARCOSWebDTParams, ExecuteNonQueryCompletedEventArgs, ExtendSessionDurationCompletedEventArgs (+35 more)

### Community 185 - "Services — Log Archiver Service"
Cohesion: 0.02
Nodes (54): ARCONActiveDirectoryInsightSetup, ARCONADScannerService, ARCONADScannerSetup, ARCOSADScannerService, ARCOSADScannerSetup, ARCON PAM Plugin, ARCONPAMPluginSetup, ARCONPAMSetup (+46 more)

### Community 186 - "MultiTab — src"
Cohesion: 0.04
Nodes (40): ChangeListener, Button, CheckBox, ChoiceBox, FXML, Label, ObservableList, Override (+32 more)

### Community 187 - "Services — SLPF"
Cohesion: 0.02
Nodes (24): SecurityElement, DiffieHellman, SecurityElement, DH, byte, SecurityElement, DiffieHellman, DH (+16 more)

### Community 188 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (52): frmACSessionMonitor, EventArgs, Aelog, EventArgs, dashboardtest, EventArgs, frmCollaborationLog, DataTable (+44 more)

### Community 189 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (81): re(), a(), b(), c(), d(), f(), A(), B() (+73 more)

### Community 190 - "Services — TSPlugin Service"
Cohesion: 0.03
Nodes (38): AsyncCallback, byte, Exception, IAsyncResult, ManualResetEvent, Queue, Socket, SSHChannel (+30 more)

### Community 191 - "ACM Client — SSHTerminal"
Cohesion: 0.04
Nodes (35): ArrayList, bool, Control, DragEventArgs, EventArgs, Graphics, IContainer, Image (+27 more)

### Community 192 - "ACMO Web — Client Manager"
Cohesion: 0.02
Nodes (52): addNumericalSeparator(), addParserEvents(), _applyDecoratedDescriptor(), base64End(), base64Text(), DBCSDecoder(), DBCSEncoder(), decodeCodePointsArray() (+44 more)

### Community 193 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (88): b(), c(), d(), f(), a(), aa(), ab(), b() (+80 more)

### Community 194 - "Services — Log Archiver Service"
Cohesion: 0.05
Nodes (33): CommonFunctions, AmazonS3Client, ArcosConfig, BlobContainerClient, bool, Boolean, CommandType, DataColumnCollection (+25 more)

### Community 195 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (49): BigInteger, Random, DSAKeyPair, DSAPublicKey, BigInteger, byte, IKeyWriter, ISigner (+41 more)

### Community 196 - "ASM Server — Pkcs11Interop"
Cohesion: 0.04
Nodes (28): bool, CkVersion, IntPtr, NativeULong, CK_C_INITIALIZE_ARGS, IntPtr, CK_FUNCTION_LIST, byte (+20 more)

### Community 197 - "ACM Client — Framework CM"
Cohesion: 0.05
Nodes (37): Encoding, ICollection, SFTPFileTransferProgressDelegate, SSHChannel, uint, SFTPClient, string, uint (+29 more)

### Community 198 - "Services — Schedule Password Change"
Cohesion: 0.02
Nodes (64): VerifyException, byte, SSHException, VerifyException, byte, SSHException, InvalidOptionException, UnknownEscapeSequenceException (+56 more)

### Community 199 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (92): bl(), a(), aa(), ac(), b(), ba(), bd(), c() (+84 more)

### Community 200 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (47): AnchorStyles, AnimateSpeed, Bitmap, Color, ContextMenu, ErrorProvider, EventArgs, float (+39 more)

### Community 201 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (69): addChunk(), addErrorHandlerIfEventEmitter(), _addListener(), afterWrite(), arrayClone(), callFinal(), checkListener(), chunkInvalid() (+61 more)

### Community 202 - "ASM Server — Pkcs11Interop"
Cohesion: 0.05
Nodes (26): bool, Mechanism, bool, CkVersion, byte, NativeULong, CK_INFO, IntPtr (+18 more)

### Community 203 - "Services — ADScanner Service ACMO"
Cohesion: 0.03
Nodes (60): bool, DataRow, DirectorySearcher, int, List, object, SearchResult, string (+52 more)

### Community 204 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.04
Nodes (34): LocalFileInfo, LoginInfo, MainLocalToServer, SFTPPrivileges, bool, CancelEventArgs, CancellationTokenSource, ColumnClickEventArgs (+26 more)

### Community 205 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (26): ArrayList, bool, int, MemoryStream, ProcessResult, TelnetCode, TelnetNegotiator, TelnetOption (+18 more)

### Community 206 - "ACMO Web — Portal"
Cohesion: 0.06
Nodes (91): a(), aa(), ac(), b(), ba(), bd(), c(), ca() (+83 more)

### Community 207 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (78): adapt(), asFloat(), asInt(), basicToDigit(), C(), calculateBorders(), capitalize(), cleanupContainer() (+70 more)

### Community 208 - "Services — ADScanner Service"
Cohesion: 0.03
Nodes (60): PIMPRStatus, PIMSDEventArgs, PIMUDEventArgs, Boolean, String, Exception, IPAddress, List (+52 more)

### Community 209 - "ACM Client — SSHTerminal"
Cohesion: 0.05
Nodes (35): byte, char, DCB, DllImport, int, IntPtr, OVERLAPPED, POINT (+27 more)

### Community 210 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (20): TabStripItemChangedEventArgs, frmRDPLogViewer, bool, Boolean, DataTable, Double, EventArgs, Int32 (+12 more)

### Community 211 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (18): addBox(), afterDatasetsUpdate(), configure(), d(), Di(), es(), f(), generateLabels() (+10 more)

### Community 212 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (68): defaults(), buildSlotSegLevels(), Calendar(), chunkFormatString(), compareForwardSlotSegs(), compareSegs(), computeForwardSlotSegs(), computeIntervalAs() (+60 more)

### Community 213 - "Services — Schedule Password Change"
Cohesion: 0.03
Nodes (53): ARCONApp, bool, int, List, ServiceModel, ARCONRecon, bool, EventArgs (+45 more)

### Community 214 - "Services — Provisioning Scheduler"
Cohesion: 0.04
Nodes (45): ARCOSObjectTypes, ARCOSOperationTypes, DataSet, Hashtable, Boolean, DataTable, IList, ILog (+37 more)

### Community 215 - "ACM Client — Framework CM"
Cohesion: 0.03
Nodes (41): SSHConnector, HostKeyCheckCallback, string, string, SSHConnectionInfo, ISocketWithTimeoutClient, SocketWithTimeout, AutoResetEvent (+33 more)

### Community 216 - "Services — TSPlugin Service"
Cohesion: 0.03
Nodes (43): ByteArrayUtil, ISSH1PrivateKeyLoader, PrivateKeyFileFormat, BigInteger, byte, string, PrivateKeyLoader, byte (+35 more)

### Community 217 - "ASM Server — Server Manager"
Cohesion: 0.02
Nodes (74): DataGridViewAutoFilter, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator, DataGridViewFunctions, AdvancedDataGridView (+66 more)

### Community 218 - "Services — SIEMConnector Service"
Cohesion: 0.05
Nodes (37): ARCOSOutBox, Boolean, Byte, int, Int32, String, ARCOSApp, ARCOSSIEMConnectorService (+29 more)

### Community 219 - "Services — Web References"
Cohesion: 0.05
Nodes (100): ARCONPAM_Validate_SetkeyCompletedEventArgs, CallInlineQueryCompletedEventArgs, CallInlineReturnDataSetCompletedEventArgs, EndServiceSession_NewCompletedEventArgs, ExecuteDatatableCompletedEventArgs, ExecuteNonQueryCompletedEventArgs, ExtendSessionDurationCompletedEventArgs, GetApiTokenCompletedEventArgs (+92 more)

### Community 220 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (18): frmDeviceOnboardingNew, Boolean, DataTable, EventArgs, GridViewCommandEventArgs, GridViewDeleteEventArgs, GridViewPageEventArgs, GridViewRowEventArgs (+10 more)

### Community 221 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (38): ReportDownloads, DataTable, Dictionary, EventArgs, int, List, RepeaterCommandEventArgs, RepeaterItemEventArgs (+30 more)

### Community 222 - "ACMO Web — Portal"
Cohesion: 0.03
Nodes (67): buildSlotSegLevels(), Calendar(), chunkFormatString(), compareForwardSlotSegs(), compareSegs(), computeForwardSlotSegs(), computeIntervalAs(), computeIntervalUnit() (+59 more)

### Community 223 - "Services — Arcon Auto Failover"
Cohesion: 0.03
Nodes (50): ARCOSApp, ARCOSAutoFailover, DataSet, DataTable, double, EventArgs, int, ServiceController (+42 more)

### Community 224 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (74): adapt(), asInt(), basicToDigit(), C(), calculateBorders(), capitalize(), cleanupContainer(), cloneCanvasContents() (+66 more)

### Community 225 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (90): o(), _addNumericSort(), _fnAddColumn(), _fnAddData(), _fnAddOptionsHtml(), _fnAddTr(), _fnAdjustColumnSizing(), _fnAjaxDataSrc() (+82 more)

### Community 226 - "ASM Server — Pkcs11Interop"
Cohesion: 0.05
Nodes (23): bool, CkVersion, IntPtr, CK_FUNCTION_LIST, byte, NativeULong, CK_INFO, NativeULong (+15 more)

### Community 227 - "ACM Common — .Utilities.Sign Tool"
Cohesion: 0.05
Nodes (56): SIGNER_CERT, SIGNER_CERT_STORE_INFO, SIGNER_CONTEXT, SIGNER_FILE_INFO, SIGNER_PROVIDER_INFO, SIGNER_SIGNATURE_INFO, SIGNER_SUBJECT_INFO, SignerCertUnion (+48 more)

### Community 228 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (6): autoSetupTimeout(), executeRight(), mediate(), Player(), setSource(), toggleClass()

### Community 229 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (44): ComboBox, AlertNotificationConfig, AlertNotificationMaster, Boolean, DateTime, int, Int32, Int64 (+36 more)

### Community 230 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (19): CheckBoxHeaderCellEventArgs, frmBulkUpdatet, bool, Boolean, CheckBoxHeaderCell, CheckBoxHeaderCellEventArgs, DataSet, DataTable (+11 more)

### Community 231 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (61): B, c(), f(), n(), t(), A(), LookupList(), c() (+53 more)

### Community 232 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (79): a(), ae(), at(), B(), bi(), bt(), c(), ce() (+71 more)

### Community 233 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (90): appendChoices(), _colGroup(), _columnAutoRender(), decodeTriplet(), done(), _emptyRow(), encode(), _fnAddData() (+82 more)

### Community 234 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (61): SECURITY_ATTRIBUTES, RunProcess, Boolean, String, ACCESS_MASK, CreateProcessFlags, INFOBLOCK, LUID (+53 more)

### Community 235 - "Offline MultiTab — Offline API"
Cohesion: 0.07
Nodes (25): SaveAPIOutputBLL, ILog, RequestResponseApi, RequestResponseNewApi1, RequestResponseStatus, Exception, List, SaveAPIOutputDAL (+17 more)

### Community 236 - "ACM Common — Log Images"
Cohesion: 0.03
Nodes (52): WebApiCall, HttpWebRequest, GenericResponse, ImageDetailsModel, ImageSessionLog, ImageValidation, ResponseImageHash, bool (+44 more)

### Community 237 - "Services — Provisioning Service"
Cohesion: 0.03
Nodes (40): Verification, EventArgs, ForwardedPortLocal, ILog, SshClient, Gateway, ILog, List (+32 more)

### Community 238 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (63): St, bootstrapDelegationHandler(), A(), ae(), B(), be(), c(), Ce() (+55 more)

### Community 239 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (89): _addNumericSort(), _fnAddColumn(), _fnAddData(), _fnAddOptionsHtml(), _fnAddTr(), _fnAdjustColumnSizing(), _fnAjaxDataSrc(), _fnAjaxParameters() (+81 more)

### Community 240 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (67): bm(), c(), d(), e(), f(), g(), h(), i() (+59 more)

### Community 241 - "ACM Client — SFTPTeminal"
Cohesion: 0.04
Nodes (50): ARCOSSFTPMain, bool, Boolean, ConnectionState, Control, EventArgs, int, KeyEventArgs (+42 more)

### Community 242 - "ACM Common — .User Controls"
Cohesion: 0.03
Nodes (54): ColumnFilterEventArgs, bool, DataGridViewColumn, DgvBaseColumnFilter, bool, CancelEventArgs, DataGridViewColumn, DataView (+46 more)

### Community 243 - "ACM Common — SLPF"
Cohesion: 0.05
Nodes (23): ProtectionType, bool, byte, DataProtectionCryptoServiceProvider, DataBlob, DllImport, IntPtr, SspiProvider (+15 more)

### Community 244 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (28): AdminAccess, ExitWindows, DateTime, DllImport, EventArgs, JObject, List, Timer (+20 more)

### Community 245 - "Offline MultiTab — Offline API"
Cohesion: 0.04
Nodes (33): ServiceDetailsBLL, DateTime, ILog, List, RestrictedProcesses, ServiceDetail, ServiceDetailsDAL, bool (+25 more)

### Community 246 - "ACM Client — Script Manager"
Cohesion: 0.04
Nodes (36): FileData, bool, byte, DateTime, int, long, string, CheckTargateConnectivity (+28 more)

### Community 247 - "ACM Client — RDPTerminal"
Cohesion: 0.03
Nodes (46): frmSessionFreeze, Button, CheckBox, GroupBox, IContainer, Label, Panel, PictureBox (+38 more)

### Community 248 - "ACM Client — Oracle Query"
Cohesion: 0.03
Nodes (45): ApplicationControl, ApplicationControlScroll, bool, Boolean, CaptureProcess, DllImport, EventArgs, int (+37 more)

### Community 249 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (87): _addNumericSort(), _fnAddColumn(), _fnAddData(), _fnAddOptionsHtml(), _fnAddTr(), _fnAdjustColumnSizing(), _fnAjaxDataSrc(), _fnAjaxParameters() (+79 more)

### Community 250 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (87): _addNumericSort(), _fnAddColumn(), _fnAddData(), _fnAddOptionsHtml(), _fnAddTr(), _fnAdjustColumnSizing(), _fnAjaxDataSrc(), _fnAjaxParameters() (+79 more)

### Community 251 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (63): Boolean, String, Session, SESSION_TYPE, SessionManager, int, List, SESSION_TYPE (+55 more)

### Community 252 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (30): CG4ImageType, CG4ScannerType, APIWrapper, CG4ImageResolution, CG4ImageType, CG4KeypadType, CG4LedType, CG4MScannerExist (+22 more)

### Community 253 - "Common — SLPF"
Cohesion: 0.03
Nodes (45): HMACMD5, byte, CryptoStream, int, String, bool, byte, HashAlgorithm (+37 more)

### Community 254 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (25): Ae(), afterDraw(), afterEvent(), afterUpdate(), ba, Bi(), Ci(), configure() (+17 more)

### Community 255 - "ACM Client — RStream Client"
Cohesion: 0.04
Nodes (36): MessageReceivedArgs, NetworkTool, Node, bool, Boolean, double, Hashtable, int (+28 more)

### Community 256 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (19): EndpointBasedControlSettings, Boolean, Int32, long, String, Bitmap, frmUserSecuritySettings, Boolean (+11 more)

### Community 257 - "ACM Client — Framework CM"
Cohesion: 0.04
Nodes (29): bool, Exception, int, ManualResetEvent, SCPProgression, Stream, string, ScpChannelReceiverBase (+21 more)

### Community 258 - "Onboarding — OUProperties"
Cohesion: 0.04
Nodes (55): Program, DllImport, int, IntPtr, ADDomainDetails, int, string, ADScanner (+47 more)

### Community 259 - "Onboarding — Common Functions"
Cohesion: 0.04
Nodes (38): Program, UserServerOnboardingFactory, string, ADGroups, int, string, ADservices, int (+30 more)

### Community 260 - "Common — .IARCOSWeb API"
Cohesion: 0.06
Nodes (28): IARCOSWebAPI, ARCOSWebDT, ARCOSWebDTParams, Boolean, Byte, CommandType, DataSet, DataTable (+20 more)

### Community 261 - "Services — ADScanner Service ACMO"
Cohesion: 0.06
Nodes (30): ARCOSApp, ADDomainDetails, int, string, ADGroups, int, string, CommonFunctions (+22 more)

### Community 262 - "ACM Client — RStream Client"
Cohesion: 0.04
Nodes (38): MessageHeaderEnum, MessageReceivedArgsInternet, NetworkToolInternet, RDPOperation, bool, Boolean, byte, DateTime (+30 more)

### Community 263 - "ASM Server — Server Manager"
Cohesion: 0.03
Nodes (60): ListViewAutoFiler, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator, ListViewFunctions, Int32 (+52 more)

### Community 264 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (56): absCeil(), absFloor(), absRound(), add_subtract__addSubtract(), addParseToken(), addWeekParseToken(), as(), bubble() (+48 more)

### Community 265 - "ACM Client — Framework CM"
Cohesion: 0.04
Nodes (34): Cipher, MAC, uint, CRC, Random, FilterDataHandler, bool, int (+26 more)

### Community 266 - "Services — SLPF"
Cohesion: 0.04
Nodes (30): Runnable, ServerSocket, ChannelDirectTCPIP, int, Stream, String, ForwardedTCPIPDaemon, Object (+22 more)

### Community 267 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (32): ADDomainDetails, ADGroups, AdScannerCommonFunctions, ADservices, ADUsers, ARCOSApp, ARCOSCommonSelectParameter, CommonFunctions (+24 more)

### Community 268 - "Services — ADScanner Service"
Cohesion: 0.04
Nodes (35): CommonFunctions, Boolean, DataSet, DataTable, DateTime, EventLog, EventLogEntryType, Hashtable (+27 more)

### Community 269 - "Services — Schedule Password Change"
Cohesion: 0.03
Nodes (19): Thread, GlobalRequestReply, int, Thread, Thread, GlobalRequestReply, int, Thread (+11 more)

### Community 270 - "Services — SLPF"
Cohesion: 0.03
Nodes (32): ChannelShell, bool, SshStream, bool, Regex, SeekOrigin, string, SshStream (+24 more)

### Community 271 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (23): B(), Ce, D(), getDataAttributes(), H(), I(), Ie, j() (+15 more)

### Community 272 - "Services — Script Scheduler"
Cohesion: 0.06
Nodes (17): ARCOSApp, Boolean, CommandType, DataRow, DataSet, DataTable, DateTime, EventLog (+9 more)

### Community 273 - "Services — TSPlugin Service"
Cohesion: 0.05
Nodes (9): int, Random, uint, BigInteger, int, Random, uint, BigInteger (+1 more)

### Community 274 - "Services — Desk Insight Master"
Cohesion: 0.05
Nodes (36): IPRangeFinder, IEnumerable, IPAddress, NewDevies, Boolean, DateTime, Int32, String (+28 more)

### Community 275 - "Services — SLPF"
Cohesion: 0.02
Nodes (45): BlowfishCBC, Random, byte, int, RNGCryptoServiceProvider, BlowfishCBC, Random, byte (+37 more)

### Community 276 - "ACM Client — Oracle SDTerminal"
Cohesion: 0.04
Nodes (36): ApplicationControl, Rect, bool, Boolean, CaptureProcess, DllImport, double, EventArgs (+28 more)

### Community 277 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (64): addCombinator(), adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), assert(), boxModelAdjustment(), buildFragment() (+56 more)

### Community 278 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (32): bind(), calculateCurvePoints(), flatten(), getBounds(), hasOpacity(), hasText(), inlineLevel(), isElement() (+24 more)

### Community 279 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (9): frmPasswordManager, ColumnClickEventArgs, ColumnHeader, EventArgs, int, MouseEventArgs, SplitterEventArgs, String (+1 more)

### Community 280 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (31): MessageHeaderEnum, MessageReceivedArgsInternet, NetworkToolInternet, bool, Boolean, byte, DateTime, DllImport (+23 more)

### Community 281 - "ACMO Web — User Access"
Cohesion: 0.04
Nodes (60): addCombinator(), adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), boxModelAdjustment(), buildFragment(), buildParams() (+52 more)

### Community 282 - "ACM Client — Biometric Finger"
Cohesion: 0.05
Nodes (27): AfisEngine, GetFingerPrint, SignatureTemplate, Bitmap, bool, Boolean, byte, CaptureCallback (+19 more)

### Community 283 - "ACM Common — VPNClient"
Cohesion: 0.03
Nodes (49): ARCOSUpdater, Boolean, String, WebProxy, ARCONVPNClientV4, Optimizer, bool, DllImport (+41 more)

### Community 284 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (60): addCombinator(), adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), boxModelAdjustment(), buildFragment(), buildParams() (+52 more)

### Community 285 - "Onboarding — Common Functions Userob"
Cohesion: 0.06
Nodes (25): ARCOSOnBoardingConfigParameter, bool, int, string, CommonFunctionsUserob, bool, Boolean, CommandType (+17 more)

### Community 286 - "ACM Client — VNCTerminal"
Cohesion: 0.04
Nodes (27): Rectangle, EncodedRectangleFactory, bool, int, Rectangle, string, Framebuffer, BinaryReader (+19 more)

### Community 287 - "Services — User On Boarding"
Cohesion: 0.06
Nodes (20): ARCOSApp, ARCOSUserOnBoardingService, Boolean, EventArgs, Timer, CommonFunctionsOB, bool, Boolean (+12 more)

### Community 288 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (44): alloc(), allocUnsafe(), arrayIndexOf(), ArrayReader(), asciiToBytes(), asciiWrite(), assertSize(), base64clean() (+36 more)

### Community 289 - "Onboarding — User Onboarding"
Cohesion: 0.09
Nodes (28): ARCOSLogDetails, Int32, ARCOSLogger, String, ARCOSObjectTypes, GroupType, SqlParameter, Groups (+20 more)

### Community 290 - "Services — SLPF"
Cohesion: 0.04
Nodes (30): SshShell, bool, Regex, Stream, string, SshShell, bool, Regex (+22 more)

### Community 291 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (28): ARCOSCommonModifyParameter, Byte, int, long, string, CommonFunctions, ArcosConfig, bool (+20 more)

### Community 292 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (73): addHandler(), areValidElements(), arrow(), bootstrapDelegationHandler(), bootstrapHandler(), computeAutoPlacement(), computeOffsets(), computeStyles() (+65 more)

### Community 293 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (18): addBox(), afterDatasetsUpdate(), an(), ct(), ge(), generateLabels(), ke(), Mn() (+10 more)

### Community 294 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (76): backgroundRepeatShape(), calculateCurvePoints(), capitalize(), clipBounds(), createShape(), createStack(), documentHeight(), documentWidth() (+68 more)

### Community 295 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (34): asFloat(), bind(), flatten(), getWidth(), hasOpacity(), hasParentClip(), hasText(), inlineLevel() (+26 more)

### Community 296 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (55): Boolean, bool, Boolean, byte, DllImport, INFOBLOCK, int, Int16 (+47 more)

### Community 297 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (40): DataTypeEnum, DeviceCap, GDI32, MessageTypeEnum, RECT, SizeConstants, StateObject, StreamAgentInternet (+32 more)

### Community 298 - "ACM Client — SSHTerminal"
Cohesion: 0.03
Nodes (41): Color, EventArgs, PaintEventArgs, ColorButton, bool, Button, CheckBox, Color (+33 more)

### Community 299 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (41): arrayToHash(), buildCanvas(), copyStyle(), DocMeasure(), DocPreprocessor(), FontProvider(), fontStringify(), format() (+33 more)

### Community 300 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (76): backgroundRepeatShape(), calculateCurvePoints(), capitalize(), clipBounds(), createShape(), createStack(), documentHeight(), documentWidth() (+68 more)

### Community 301 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 302 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (28): SignatureTemplate, GetFingerPrint, SignatureTemplate, Bitmap, bool, Boolean, byte, CaptureCallback (+20 more)

### Community 303 - "ACM Client — Framework CM"
Cohesion: 0.05
Nodes (35): ExtendedWindowStyles, RECT, ShowWindowEnum, WINDOWINFO, WindowSnap, WindowStyles, Bitmap, bool (+27 more)

### Community 304 - "ACMO Web — Common Functions"
Cohesion: 0.07
Nodes (23): APICallRequest, DataTable, dynamic, HttpResponseMessage, HttpWebRequest, DomainServers, Boolean, Int32 (+15 more)

### Community 305 - "Services — TSPlugin Service"
Cohesion: 0.06
Nodes (28): CommonAPI, HttpWebRequest, STAThread, CommonFunctions, Boolean, EventLog, EventLogEntryType, int (+20 more)

### Community 306 - "ACM Client — DQS"
Cohesion: 0.03
Nodes (46): MainForm, DockPanel, IContainer, MenuStrip, OpenFileDialog, StatusStrip, Timer, ToolStrip (+38 more)

### Community 307 - "Services — SLPF"
Cohesion: 0.05
Nodes (31): CryptoAlgorithm, bool, byte, CipherMode, int, PaddingMode, SymmetricKey, bool (+23 more)

### Community 308 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (41): Logging, clsAdscanner, bool, List, ADScanner, AllProperties, clsADScannerFunctions, ConfigReader (+33 more)

### Community 309 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (14): frmUserOnboardingNew, Boolean, EventArgs, GridViewCommandEventArgs, GridViewDeleteEventArgs, GridViewPageEventArgs, GridViewRowEventArgs, int (+6 more)

### Community 310 - "Common — .User Controls"
Cohesion: 0.03
Nodes (43): DgvBaseColumnFilter, HFilterAlignment, VFilterAlignment, bool, CancelEventArgs, DataGridViewColumn, DataView, string (+35 more)

### Community 311 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 312 - "MultiTab — src"
Cohesion: 0.05
Nodes (26): DatePicker, KeyEvent, Button, CheckBox, ChoiceBox, FXML, Label, ObservableList (+18 more)

### Community 313 - "ACM Client — SSHTerminal"
Cohesion: 0.04
Nodes (36): Entry, int, ChannelCollection, Entry, ArrayList, bool, CommandResult, Hashtable (+28 more)

### Community 314 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (19): LOB, Bitmap, string, LOBVPNServers, VPNServers, VPNServersVIP, Boolean, String (+11 more)

### Community 315 - "ACMO Web — Web Services"
Cohesion: 0.06
Nodes (17): ReportAPI, DataTable, WebMethod, UserDashboardDBHelper, Boolean, DataSet, DataTable, String (+9 more)

### Community 316 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (21): addBox(), afterDatasetsUpdate(), Chart, compare2Level(), createTitle(), _detectPlatform(), determineLastEvent(), generateLabels() (+13 more)

### Community 317 - "Services — PAM Agents"
Cohesion: 0.05
Nodes (54): ACCESS_MASK, CreateProcessFlags, INFOBLOCK, LUID, LUID_AND_ATTRIBUTES, NetJoinStatus, PEB, PROCESS_BASIC_INFORMATION (+46 more)

### Community 318 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (35): ClickDetector, AutomationElement, bool, DllImport, IKeyboardMouseEvents, IntPtr, KeyEventArgs, MouseEventArgs (+27 more)

### Community 319 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 320 - "Onboarding — cls Onboarding"
Cohesion: 0.05
Nodes (18): psCtrl, EventArgs, ARCOSCommonAlterParameter, int, object, string, clsOnboarding, lstcls (+10 more)

### Community 321 - "ASM Server — Pkcs11Interop"
Cohesion: 0.03
Nodes (42): bool, CkRsaAesKeyWrapParams, bool, CkRsaPkcsOaepParams, bool, CkRsaAesKeyWrapParams, bool, CkRsaPkcsOaepParams (+34 more)

### Community 322 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 323 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 324 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 325 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 326 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 327 - "Services — Log Archiver Service"
Cohesion: 0.06
Nodes (23): CommonFunctions, ArcosConfig, bool, Boolean, CommandType, DataColumnCollection, DataRow, DataSet (+15 more)

### Community 328 - "Offline MultiTab — Offline API"
Cohesion: 0.05
Nodes (54): GenericResponse, INFOBLOCK, LUID, LUID_AND_ATTRIBUTES, NetJoinStatus, PEB, PROCESS_BASIC_INFORMATION, PROCESS_INFORMATION (+46 more)

### Community 329 - "ACM Client — Sshkey SFTP"
Cohesion: 0.05
Nodes (12): ConnectionState, MainSTS, bool, Boolean, CancelEventArgs, EventArgs, Hashtable, HostKeyVerifyingEventArgs (+4 more)

### Community 330 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (74): WebAPIParamTypeDetails, ARCOSCommonModifyParameter, ARCOSOnBoarding, ARCOSOnBoardingConfigParameter, ARCOSServiceOnBoarding, LoginUserDetail, ServersParameters, ServiceType (+66 more)

### Community 331 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (15): barSign(), callback(), computeMinSampleSize(), determineMaxTicks(), garbageCollect(), generateTicks$1(), getPixelForGridLine(), _getTargetValue() (+7 more)

### Community 332 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (41): DgvBaseColumnFilter, bool, CancelEventArgs, DataGridViewColumn, DataView, string, DgvDateRangeColumnFilter, CancelEventArgs (+33 more)

### Community 333 - "ACM Client — SSHTerminal"
Cohesion: 0.04
Nodes (39): Color, uint, DrawUtil, RoundBorderElement, RoundRectColors, CheckBox, EventArgs, GroupBox (+31 more)

### Community 334 - "Services — TSPlugin Service"
Cohesion: 0.04
Nodes (41): HFilterAlignment, VFilterAlignment, DgvBaseColumnFilter, HFilterAlignment, VFilterAlignment, bool, CancelEventArgs, DataGridViewColumn (+33 more)

### Community 335 - "Services — Log Archiver Service"
Cohesion: 0.05
Nodes (20): ARCON.ACMO.Test, ARCOSPortal, ARCOSStagingLogServer, ARCONPAM.ServerManager.Tests, net472, Microsoft.NET.Test.Sdk (16.5.0), NUnit (3.12.0), NUnit3TestAdapter (3.16.1) (+12 more)

### Community 336 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (42): addCombinator(), adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), augmentWidthOrHeight(), buildFragment(), condense() (+34 more)

### Community 337 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (43): fcssescape(), addCombinator(), adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), augmentWidthOrHeight(), buildFragment() (+35 more)

### Community 338 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (19): Exception, MessageBoxButtons, MessageBoxIcon, frmARCONRAMainInternet, RECT, Boolean, DllImport, DllImportAttribute (+11 more)

### Community 339 - "ACM Client — DQS"
Cohesion: 0.04
Nodes (8): IDB2Browser, Boolean, TreeNode, IMYSQLBrowser, Boolean, StringCollection, TreeNode, TreeViewCancelEventArgs

### Community 340 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (73): addHandler(), allowedAttribute(), AttachmentMap, bootstrapDelegationHandler(), bootstrapHandler(), customEvents, Data, Default (+65 more)

### Community 341 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (13): barSign(), determineMaxTicks(), garbageCollect(), generateTicks$1(), getPixelForGridLine(), getTickMarkLength(), getTicksLimit(), getTitleHeight() (+5 more)

### Community 342 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (53): be(), bi(), Ce(), ci(), D(), De(), _e(), ei() (+45 more)

### Community 343 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (30): afterDraw(), afterEvent(), alignX(), alignY(), BasicPlatform, computeCircularBoundary(), createPointLabelContext(), createTooltipContext() (+22 more)

### Community 344 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (72): areEqualArrayBuffers(), areSimilarFloatArrays(), areSimilarRegExps(), areSimilarTypedArrays(), AssertionError(), _assertThisInitialized(), checkBoxedPrimitive(), checkIsPromise() (+64 more)

### Community 345 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (41): ARCOSMONITWebService, validateARCOSServiceCompletedEventArgs, bool, object, SendOrPostCallback, ARCOSIBUDAA, IsUDAAValidatedCompletedEventArgs, bool (+33 more)

### Community 346 - "ACM Client — Sshkey SFTP"
Cohesion: 0.03
Nodes (42): FileMask, EventArgs, FileOperation, Button, IContainer, Label, FolderNamePrompt, EventArgs (+34 more)

### Community 347 - "ACM Client — SSHTerminal"
Cohesion: 0.05
Nodes (22): bool, HMACSHA1, BlowfishCipher1, BlowfishCipher2, Cipher, MACSHA1, RijindaelCipher2, TripleDESCipher1 (+14 more)

### Community 348 - "ACM Client — VNCTerminal"
Cohesion: 0.04
Nodes (29): frmARCOSVNCTerminal, IContainer, MenuStrip, Timer, ToolStripMenuItem, Bitmap, bool, EventArgs (+21 more)

### Community 349 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (28): ARCOSPRAWFM, Boolean, DateTime, Int32, List, long, String, PasswordRequestOverridingWorkflow (+20 more)

### Community 350 - "ACMO Web — APIRA"
Cohesion: 0.05
Nodes (45): i(), n(), r(), t(), u(), an(), at(), bt() (+37 more)

### Community 351 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (19): afterDraw(), afterEvent(), afterUpdate(), Ba(), Ci(), cs, ki(), lo() (+11 more)

### Community 352 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (58): escapeAttributeValue(), onError(), onReset(), validationInfo(), adler32(), bi_flush(), bi_windup(), binstring2buf() (+50 more)

### Community 353 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (18): afterDatasetsUpdate(), Chart, compare2Level(), createStack(), _detectPlatform(), determineLastEvent(), generateLabels(), getCanvas() (+10 more)

### Community 354 - "ACMO Web — Portal"
Cohesion: 0.05
Nodes (60): e(), cmyk2hsl(), cmyk2hsv(), cmyk2hwb(), cmyk2keyword(), cmyk2rgb(), _extendDeep(), getAlpha() (+52 more)

### Community 355 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (31): ARCONRunAs, WinSessionDetails, Int32, List, Processes, Boolean, String, CURSORINFO (+23 more)

### Community 356 - "Services — TSPlugin Service"
Cohesion: 0.07
Nodes (20): FindChildWindow2, GetWindowCmd, KeyModifiers, MouseEventFlags, POINTAPI, ProcessAccessFlags, RECT, WinAPI (+12 more)

### Community 357 - "ACM Client — SSHTerminal"
Cohesion: 0.07
Nodes (15): WindowStatus, frmSSHClientMain, Bitmap, bool, Boolean, byte, EventArgs, int (+7 more)

### Community 358 - "Common — Common Functions Utils"
Cohesion: 0.05
Nodes (21): EncryptDescryptFile, Bitmap, Boolean, Image, Int32, String, ARCOSEncryptionDecryption, DateTime (+13 more)

### Community 359 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (37): MessageReceivedArgs, NetworkTool, Node, bool, double, Hashtable, int, IPAddress (+29 more)

### Community 360 - "Services — TSPlugin Service"
Cohesion: 0.05
Nodes (52): ACCESS_MASK, CreateProcessFlags, INFOBLOCK, LUID, LUID_AND_ATTRIBUTES, NetJoinStatus, PEB, PROCESS_BASIC_INFORMATION (+44 more)

### Community 361 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (12): BarController, beforeUpdate(), BubbleController, computeFitCategoryTraits(), computeFlexCategoryTraits(), createTooltipItem(), isDirectUpdateMode(), isFloatBar() (+4 more)

### Community 362 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (51): a(), ai(), average(), da(), dataset(), determineDataLimits(), draw(), e() (+43 more)

### Community 363 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (3): DllImport, IntPtr, SspiProvider

### Community 364 - "Common — SLPF"
Cohesion: 0.08
Nodes (3): DllImport, IntPtr, SspiProvider

### Community 365 - "Services — Schedule Password Change"
Cohesion: 0.08
Nodes (3): DllImport, IntPtr, SspiProvider

### Community 366 - "Services — Schedule Password Change"
Cohesion: 0.08
Nodes (3): DllImport, IntPtr, SspiProvider

### Community 367 - "Services — TSPlugin Service"
Cohesion: 0.08
Nodes (3): DllImport, IntPtr, SspiProvider

### Community 368 - "ACM Client — Framework CM"
Cohesion: 0.05
Nodes (28): BigInteger, bool, int, Stream, Test, BERReader, BERReaderTest, BERTagInfo (+20 more)

### Community 369 - "Services — TSPlugin Service"
Cohesion: 0.05
Nodes (35): INPUT, AccessControlLogData, AccessControlLogData_min, APIFuncs, APIMembers, CustomPSRSettings, INPUT, MOUSEINPUT (+27 more)

### Community 370 - "Services — APEMService"
Cohesion: 0.05
Nodes (21): Settings, String, CryptoHash, CryptoHashType, String, EncryptionDecryption_Web, String, CommonFunctionsUtils (+13 more)

### Community 371 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (14): BarController, BubbleController, computeFitCategoryTraits(), computeFlexCategoryTraits(), computeMinSampleSize(), createTooltipItem(), _getTargetPixel(), isDirectUpdateMode() (+6 more)

### Community 372 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (6): clearMenus(), getParent(), getTargetFromTrigger(), Plugin(), NOTE: POPOVER EXTENDS tooltip.js, ScrollSpy()

### Community 373 - "Services — PAM Agents"
Cohesion: 0.07
Nodes (22): ARWH, ShowWindowEnum, bool, Boolean, decrypt, DllImport, EncryptionDecryption, EventArgs (+14 more)

### Community 374 - "Services — TSPlugin Service"
Cohesion: 0.06
Nodes (41): Object, TSVirtualChannel, TSVirtualChannelEventArgs, WtsApiWrapper, WtsSession, Boolean, DllImport, Int32 (+33 more)

### Community 375 - "Services — Server Manager"
Cohesion: 0.03
Nodes (27): ARCONCoolProgressBarv2, EventArgs, ARCONCoolProgressBarv2, IContainer, ProgressBar, ARCONCoolProgressBarv2, EventArgs, ARCONCoolProgressBarv2 (+19 more)

### Community 376 - "ACM Client — Framework CM"
Cohesion: 0.07
Nodes (25): MouseHookStruct, POINT, User32APIManager, DllImport, DllImportAttribute, EnumThreadDelegate, HookProc, HookProcedureDelegate (+17 more)

### Community 377 - "Services — Log Archiver Service"
Cohesion: 0.03
Nodes (39): AssemblyDetails, Assembly, DateTime, ServiceDetailsClient, ServiceDetailsClient, string, ServiceDetailsClient, string (+31 more)

### Community 378 - "Services — PAM Agents"
Cohesion: 0.06
Nodes (21): HardwareDetails, String, IPMACManager, String, CommonFunction, Listener, Port, Boolean (+13 more)

### Community 379 - "Services — Desk Insight"
Cohesion: 0.05
Nodes (31): AppSetting, Chunk, FileMetaDataModel, List, ReadCSVModel, int, SortedFile, Utils (+23 more)

### Community 380 - "ACM Client — Framework CM"
Cohesion: 0.08
Nodes (33): bool, Cancellation, byte, int, object, SSHChannel, SSHConnection, OpenForTest() (+25 more)

### Community 381 - "ACM Client — Web Browserv35"
Cohesion: 0.04
Nodes (51): Cancelable, CustomPromptService, frmARCOSWebBrowserGecko, awbOperations_Load(), awbOperations_OperationTypeChanged(), closeToolStripMenuItem_Click(), Bitmap, Boolean (+43 more)

### Community 382 - "Services — Schedule Password Change"
Cohesion: 0.03
Nodes (58): bool, int, CAPIProvider, bool, byte, int, IntPtr, short (+50 more)

### Community 383 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (22): Channel, bool, byte, InputStream, int, MethodImpl, Stream, Vector (+14 more)

### Community 384 - "ASM Server — Pkcs11Interop"
Cohesion: 0.03
Nodes (69): C_CancelFunctionDelegate, C_CloseAllSessionsDelegate, C_CloseSessionDelegate, C_CopyObjectDelegate, C_CreateObjectDelegate, C_DecryptDelegate, C_DecryptDigestUpdateDelegate, C_DecryptFinalDelegate (+61 more)

### Community 385 - "Services — Schedule Password Change"
Cohesion: 0.04
Nodes (22): Channel, bool, byte, InputStream, int, MethodImpl, Stream, Vector (+14 more)

### Community 386 - "ACM Client — SFTPTeminal"
Cohesion: 0.05
Nodes (36): ShBrowseInfo, ShellAPI, ShellExecuteInfo, SHFileInfo, DllImport, Form, Image, int (+28 more)

### Community 387 - "Services — User On Boarding"
Cohesion: 0.12
Nodes (16): GroupType, Groups, bool, string, GroupsMapping, string, UserServiceHelper, Boolean (+8 more)

### Community 388 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (15): frmRPAJsonUpload, Button, IContainer, TextBox, frmServicesQuickSearch_Modify, bool, Boolean, DataTable (+7 more)

### Community 389 - "ACMO Web — Portal"
Cohesion: 0.07
Nodes (67): aa(), Ab(), B(), Bb(), C(), ca(), Cb(), da() (+59 more)

### Community 390 - "ACMO Web — Provisioning Web"
Cohesion: 0.07
Nodes (29): ApiParameterDescription, GeneratePageResult(), HelpPageConfigurationExtensions, HttpConfiguration, IDictionary, IDocumentationProvider, MediaTypeHeaderValue, string (+21 more)

### Community 391 - "Services — SLPF"
Cohesion: 0.03
Nodes (27): AES128CBC, ICryptoTransform, int, RijndaelManaged, AES128CBC, ICryptoTransform, int, RijndaelManaged (+19 more)

### Community 392 - "ACMO Web — Provisioning Web"
Cohesion: 0.05
Nodes (34): actualDisplay(), addCombinator(), ajaxConvert(), ajaxHandleResponses(), Animation(), augmentWidthOrHeight(), condense(), createFxNow() (+26 more)

### Community 393 - "ACMO Web — APIRA"
Cohesion: 0.05
Nodes (34): actualDisplay(), addCombinator(), ajaxConvert(), ajaxHandleResponses(), Animation(), augmentWidthOrHeight(), condense(), createFxNow() (+26 more)

### Community 394 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (13): assign(), blockTextSelection(), ClickableComponent(), DescriptionsButton(), evented(), isPlain(), Plugin(), ProgressControl() (+5 more)

### Community 395 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (25): addRegexToken(), duration_add_subtract__add(), duration_add_subtract__addSubtract(), duration_add_subtract__subtract(), getSet(), isArray(), isFunction(), locale_calendar__calendar() (+17 more)

### Community 396 - "Offline MultiTab — Offline API"
Cohesion: 0.05
Nodes (34): actualDisplay(), addCombinator(), ajaxConvert(), ajaxHandleResponses(), Animation(), augmentWidthOrHeight(), condense(), createFxNow() (+26 more)

### Community 397 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (19): addIfFound(), allPlugins(), cachedKeys(), Config, createDescriptors(), getOpts(), getResolver(), hasFunction() (+11 more)

### Community 398 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (14): beforeUpdate(), buildTicks(), _calculateBarValuePixels(), go(), ii(), initialize(), labelColor(), labelPointStyle() (+6 more)

### Community 399 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (3): AbstractChosen(), Chosen(), SelectParser()

### Community 400 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (17): addIfFound(), allPlugins(), cachedKeys(), cloneIfNotShared(), Config, createDescriptors(), getOpts(), getResolver() (+9 more)

### Community 401 - "Services — SLPF"
Cohesion: 0.04
Nodes (23): DHKeyGeneration, byte, DHParameters, BigInteger, bool, byte, DiffieHellmanManaged, BigInteger (+15 more)

### Community 402 - "ASM Server — ARC SEC"
Cohesion: 0.05
Nodes (18): ARC_CommonFunctionsUtils, int, string, ARCSEC_EDT, DataTable, List, string, ARCSEC_EDT_FL (+10 more)

### Community 403 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (62): addHandler(), allowedAttribute(), AttachmentMap, bootstrapHandler(), customEvents, Data, Default, Default$1 (+54 more)

### Community 404 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (15): clearStacks(), convertObjectDataToArray(), createDataContext(), createDatasetContext(), createStack(), DatasetController, getFirstScaleId(), _getLabelForValue() (+7 more)

### Community 405 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (37): a(), ai(), average(), da(), dataset(), determineDataLimits(), draw(), e() (+29 more)

### Community 406 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (15): Be(), ei(), fn(), gn(), je(), n(), ne(), numeric() (+7 more)

### Community 407 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (26): ControlPanelRestriction, GenerateUserRules, AccessControlType, bool, FileSystemRights, List, string, ActivityRules (+18 more)

### Community 408 - "Services — Password Change Vault"
Cohesion: 0.04
Nodes (31): Connect, bool, ILog, string, ISessionFactory, FluentHelper, bool, ILog (+23 more)

### Community 409 - "User Discovery — ADScanner"
Cohesion: 0.05
Nodes (34): ADScanner, bool, DateTime, Dictionary, DirectorySearcher, dynamic, List, object (+26 more)

### Community 410 - "ACMO Web — Provisioning Web"
Cohesion: 0.06
Nodes (23): Class, ObjectGenerator, SimpleTypeObjectGenerator, Dictionary, Func, int, long, SuppressMessage (+15 more)

### Community 411 - "Common — Tab Strip"
Cohesion: 0.05
Nodes (23): FATabStripMenuGlyph, bool, Graphics, Rectangle, ToolStripProfessionalRenderer, FATabStrip, bool, CollectionChangeEventArgs (+15 more)

### Community 412 - "ACM Common — User Service"
Cohesion: 0.07
Nodes (37): ARCOSLogs, ARCOSServiceLogs, ManageServicePassword, RDPSessionCheck, ServiceReferenceLogParams, UserAndServerRequestLogsParams, ViewARCOSLogParams, ViewDBALogParams (+29 more)

### Community 413 - "ACM Common — Enitity Objects"
Cohesion: 0.05
Nodes (25): DailySchedule, IntervalSchedule, MonthlySchedule, OneTimeSchedule, Schedule, ScheduleType, SelectedWeekSchedule, WeeklySchedule (+17 more)

### Community 414 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (41): attrib(), beginWhiteSpace(), charAt(), checkBufferLength(), closeTag(), closeText(), debuglog(), decode() (+33 more)

### Community 415 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (27): absCeil(), absFloor(), as(), bubble(), daysToMonths(), duration_add_subtract__add(), duration_add_subtract__addSubtract(), duration_add_subtract__subtract() (+19 more)

### Community 416 - "Services — Data Sync"
Cohesion: 0.07
Nodes (24): ARCOSApp, CommonFunctionsDataSync, Boolean, CommandType, DataSet, DataTable, DateTime, EventLog (+16 more)

### Community 417 - "MultiTab — src"
Cohesion: 0.05
Nodes (12): LaunchMultiService, ConfigCommand, Override, FavouriteServices, JsonProperty, Override, Override, MyViewTreeDataEmpty (+4 more)

### Community 418 - "ACM Client — SSHTerminal"
Cohesion: 0.04
Nodes (21): IEnumerator, ConnectionListImpl, DebugServiceImpl, EnumeratorWrapper, FrameImpl, UtilImpl, IEnumerator, Connection (+13 more)

### Community 419 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (24): ARCOSAPI, ARCOSAPICommonFunctions, ARCOSMessage, ARCOSMessageCodes, ARCOSMessageStore, ARCOSObject, LOBProfileServiceGroup, LOBProfileServices (+16 more)

### Community 420 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (7): an, es, Ss, W, Zi, nn(), tn()

### Community 421 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (14): beforeUpdate(), clearStacks(), cloneIfNotShared(), convertObjectDataToArray(), createDataContext(), createDatasetContext(), DatasetController, getFirstScaleId() (+6 more)

### Community 422 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (33): accumulate(), all(), checkEntryCRC32(), checkSupport(), ConvertWorker(), createIterResult(), Document(), fixFilename() (+25 more)

### Community 423 - "Services — TSPlugin Service"
Cohesion: 0.04
Nodes (20): RequestPtyReq, String, Channel, bool, byte, InputStream, int, MethodImpl (+12 more)

### Community 424 - "Services — Schedule Password Change"
Cohesion: 0.04
Nodes (29): ARCOSSPCService, IContainer, StringExtensions, ARCOSCommonModifyParameter_temp, Byte, int, string, ARCOSCommonSelectParameter (+21 more)

### Community 425 - "MultiTab — src"
Cohesion: 0.06
Nodes (23): Button, CheckBox, ChoiceBox, FXML, Label, ObservableList, Override, ResourceBundle (+15 more)

### Community 426 - "ACM Client — Arcoss SSMDesktop"
Cohesion: 0.08
Nodes (3): ARCOSSSHTerminal, ArcosCompression, ArcosSSMDesktop

### Community 427 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (22): Scheduler, ArrayList, Boolean, frmSchedulerMaster, Boolean, Button, CheckBox, CheckBoxComboBox (+14 more)

### Community 428 - "ACM Common — Enitity Objects"
Cohesion: 0.05
Nodes (60): APIConfiguration, ArcosConfigSLS, BlankObject, CompleteSessionDetails, LastPwdChanged, PamAppSettings, PamSetting, ProfileDetailAccessControl (+52 more)

### Community 429 - "Services — PAM Agents"
Cohesion: 0.07
Nodes (15): CommonFunction, Listener, Boolean, EncryptionDecryption, EventArgs, EventLog, EventLogEntryType, HttpListener (+7 more)

### Community 430 - "MultiTab — src"
Cohesion: 0.07
Nodes (23): Button, CheckBox, FXML, JSONArray, Label, ObservableList, Override, ResourceBundle (+15 more)

### Community 431 - "ACM Client — Framework CM"
Cohesion: 0.06
Nodes (19): ActivityEventArgs, ActivityMessages, WarnSettings, ARCONAppIdleTime, bool, EventArgs, IAsyncResult, IContainer (+11 more)

### Community 432 - "ACM Client — VNCTerminal"
Cohesion: 0.05
Nodes (30): ARCOSVNCiUtil, DllImport, IntPtr, String, ApplicationControl, bool, CaptureProcess, DllImport (+22 more)

### Community 433 - "Services — Provisioning Service"
Cohesion: 0.05
Nodes (28): VirtualTerminal, HttpClient, ILog, SecureShellConnection, Task, Consumer, ILog, Task (+20 more)

### Community 434 - "ACM Client — Web Browser"
Cohesion: 0.09
Nodes (11): DWebBrowserEvents2, IWebBrowser2, UnsafeNativeMethods, DispId, IntPtr, MethodImpl, PreserveSig, OLECMDEXECOPT (+3 more)

### Community 435 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (44): a(), b(), c(), d(), e(), f(), g(), ga() (+36 more)

### Community 436 - "User Discovery — Scanner Processor"
Cohesion: 0.05
Nodes (24): DeviceScanner, IPAddress, P0fScanner, BackgroundWorker, bool, DoWorkEventArgs, IPAddress, object (+16 more)

### Community 437 - "MultiTab — src"
Cohesion: 0.07
Nodes (23): ActionEvent, Button, FXML, Override, TextField, Timer, MobileTwoFAController, Pane (+15 more)

### Community 438 - "ACM Client — RStream Client"
Cohesion: 0.05
Nodes (33): bool, Color, Container, EventArgs, Graphics, GraphicsPath, int, PaintEventArgs (+25 more)

### Community 439 - "ACM Client — Smar Term"
Cohesion: 0.06
Nodes (27): ApplicationControl, bool, Boolean, DllImport, EventArgs, int, IntPtr, Process (+19 more)

### Community 440 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (11): HSMDataFunctions, DataTable, FrmUDFKey, AesCryptoServiceProvider, bool, Boolean, DataTable, EventArgs (+3 more)

### Community 441 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (16): StartUBA, bool, DateTime, DllImport, ElapsedEventArgs, EventArgs, List, SessionSwitchEventArgs (+8 more)

### Community 442 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (23): EventArgs, ServerProxyTestController, CertificateSelectionEventArgs, CertificateValidationEventArgs, ConsoleColor, DataEventArgs, ExplicitProxyEndPoint, IExternalProxy (+15 more)

### Community 443 - "Offline MultiTab — Offline API"
Cohesion: 0.05
Nodes (20): offline_ssh_logs, OfflineSyncBLL, Byte, ILog, SslPolicyErrors, X509Certificate, X509Chain, APIHelper (+12 more)

### Community 444 - "Offline MultiTab — Offline API"
Cohesion: 0.06
Nodes (36): b(), c(), d(), f(), an(), at(), bt(), ct() (+28 more)

### Community 445 - "ACM Client — SSHTerminal"
Cohesion: 0.05
Nodes (18): byte, Encoding, int, EncodingProfile, EUCJPProfile, ISO8859_1Profile, ShiftJISProfile, UTF8Profile (+10 more)

### Community 446 - "ACM Client — VNCTerminal"
Cohesion: 0.05
Nodes (25): Bitmap, Point, CopyRectRectangle, CoRreRectangle, CPixelReader, Bitmap, Framebuffer, Rectangle (+17 more)

### Community 447 - "Services — SLPF"
Cohesion: 0.05
Nodes (11): KeyPairGenDSA, byte, KeyPairGenDSA, KeyPairGenDSA, byte, KeyPairGenDSA, byte, KeyPairGenDSA (+3 more)

### Community 448 - "Services — TSPlugin Service"
Cohesion: 0.05
Nodes (23): FATabStripCloseButton, bool, Graphics, Rectangle, ToolStripProfessionalRenderer, FATabStrip, bool, CollectionChangeEventArgs (+15 more)

### Community 449 - "ACM Common — Enitity Objects"
Cohesion: 0.04
Nodes (50): ARCOSMessageBoard, Boolean, DateTime, Int32, String, AccessType, AccountType, ArconObjectTypes (+42 more)

### Community 450 - "ACM Common — Custom App"
Cohesion: 0.06
Nodes (21): APIGenericResponse, CustomApplicationError, bool, Exception, string, CustomAppErrorFunctions, DataTable, Exception (+13 more)

### Community 451 - "ACMO Web — Provisioning Web"
Cohesion: 0.05
Nodes (35): b(), c(), e(), an(), at(), bt(), ct(), er() (+27 more)

### Community 452 - "MultiTab — src"
Cohesion: 0.07
Nodes (25): AnchorPane, Button, CheckBox, FXML, ImageView, JSONArray, Label, ObservableList (+17 more)

### Community 453 - "ACM Client — Smar Term"
Cohesion: 0.06
Nodes (26): ApplicationControl, bool, Boolean, DllImport, EventArgs, int, IntPtr, Process (+18 more)

### Community 454 - "ACM Client — Web Browser"
Cohesion: 0.05
Nodes (26): frmARCOSWebBrowserGecko, Bitmap, Boolean, byte, EventArgs, GeckoNavigatedEventArgs, GeckoNavigatingEventArgs, Message (+18 more)

### Community 455 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (21): TabStripItemClosingEventArgs, bool, FATabStrip, bool, CollectionChangeEventArgs, Color, ContextMenuStrip, ControlCollection (+13 more)

### Community 456 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (5): Collapse, getUID(), noop(), reflow(), Tooltip

### Community 457 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (9): each(), emptyEl(), getAttribute(), insertContent(), LoadingSpinner(), LoadProgressBar(), ModalDialog(), textContent() (+1 more)

### Community 458 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (5): Alert, Modal, Offcanvas, remove(), Toast

### Community 459 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (38): attachDropdown(), BrotliBitReader(), BrotliDecompress(), BrotliDecompressBuffer(), BrotliDecompressedSize(), CFFFont(), _close(), CopyUncompressedBlockToOutput() (+30 more)

### Community 460 - "ACMO Web — Client Manager"
Cohesion: 0.04
Nodes (35): animComplete(), bindRemoveEvent(), camelCase(), childComplete(), complete(), Datepicker(), datepicker_bindHover(), datepicker_handleMouseover() (+27 more)

### Community 461 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (8): CertificateContext, CertificateInfo, DateTime, IntPtr, RSA, StringCollection, X509Certificate, Certificate

### Community 462 - "Common — SLPF"
Cohesion: 0.04
Nodes (18): Channel, bool, byte, InputStream, int, MethodImpl, Stream, Vector (+10 more)

### Community 463 - "Services — Sync Failed Password"
Cohesion: 0.07
Nodes (20): CommonFunctionsSFP, Boolean, CommandType, DataSet, DataTable, DateTime, EventLog, EventLogEntryType (+12 more)

### Community 464 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (26): AppStatus, CommonFunctions, InstanceType, Proces, Processes, RDPSConfig, ReconnectType, RemoteStatus (+18 more)

### Community 465 - "Services — Schedule Password Change"
Cohesion: 0.06
Nodes (8): CertificateContext, CertificateInfo, DateTime, IntPtr, RSA, StringCollection, X509Certificate, Certificate

### Community 466 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (12): frmDomainOnBoarding, Boolean, DataTable, EventArgs, ListViewItem, String, frmServicesMultipleInterfaces, Boolean (+4 more)

### Community 467 - "ACM Client — Oracle TTerminal"
Cohesion: 0.07
Nodes (23): ApplicationControl, bool, Boolean, CaptureProcess, DllImport, EventArgs, int, IntPtr (+15 more)

### Community 468 - "ACM Common — Enitity Objects"
Cohesion: 0.09
Nodes (12): ARCOSSecretStorage, DataTable, DateTime, List, String, ARCOSSecretStorageEntity, DateTime, ARCOSSecretStorage (+4 more)

### Community 469 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (11): constructColor(), formatTime(), isSingleLeftClick(), LiveDisplay(), MouseTimeDisplay(), PlayProgressBar(), SeekBar(), TextTrackDisplay() (+3 more)

### Community 470 - "Services — Desk Insight"
Cohesion: 0.04
Nodes (39): ButtonZ, Color, EventArgs, int, MouseEventArgs, PaintEventArgs, String, frmARCONRARequest (+31 more)

### Community 471 - "Services — Migrate Data Utility"
Cohesion: 0.07
Nodes (20): SqlParameter, String, USPSqlParameterMaster, Boolean, ARCOSMigrateDataUtilitySettings, Boolean, DataTable, DateTime (+12 more)

### Community 472 - "MultiTab — src"
Cohesion: 0.07
Nodes (19): GridPane, Button, FXML, Label, ObservableList, Override, ResourceBundle, Stage (+11 more)

### Community 473 - "ACM Client — VNCTerminal"
Cohesion: 0.06
Nodes (19): InfBlocks, byte, int, long, Object, InfCodes, byte, int (+11 more)

### Community 474 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (21): PasswordChangeAction, bool, Boolean, Int32, long, String, frmServersPasswordDependency, DataTable (+13 more)

### Community 475 - "ACMO Web — Provisioning Web"
Cohesion: 0.07
Nodes (26): CollectionModelDescription, ComplexTypeModelDescription, Collection, DictionaryModelDescription, EnumTypeModelDescription, Collection, EnumValueDescription, IModelDocumentationProvider (+18 more)

### Community 476 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (16): afterDraw(), afterEvent(), afterUpdate(), Ba(), ki(), lo(), Oi(), Si() (+8 more)

### Community 477 - "User Discovery — IPScanner"
Cohesion: 0.05
Nodes (29): ConfigReader, NameValueCollection, IAppScanner, List, IPScanner, OS_TYPE, byte, int (+21 more)

### Community 478 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (3): ExpectedException, Test, SCPChannelStreamTest

### Community 479 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (4): noop(), Popover, TemplateFactory, Tooltip

### Community 480 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (15): point(), Canvas(), Canvas(), Plot(), Plot(), FIXME: consider another form of shadow when filling is turned on, FIXME: inline moveTo is buggy with excanvas, FIXME: figure out a way to add shadows (for instance along the right edge) (+7 more)

### Community 481 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (34): afterTransform(), arrayLikeToString(), assign(), cache(), call(), CFFEncodingVersion(), CFFPointer(), CFFSubset() (+26 more)

### Community 482 - "ACMO Web — Client Manager"
Cohesion: 0.03
Nodes (49): ARCOSWorkflow2, Button, HiddenField, HtmlGenericControl, Label, TextBox, UCResponseMessage, ARCOSWorkflow (+41 more)

### Community 483 - "Services — Provisioning Service"
Cohesion: 0.08
Nodes (16): ILog, int, object, SshTerminalControl, string, HP_UX, ILog, int (+8 more)

### Community 484 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (17): RECT, bool, DllImport, double, ElapsedEventArgs, int, IntPtr, MarshalAs (+9 more)

### Community 485 - "ACM Client — RStream Client"
Cohesion: 0.04
Nodes (34): frmController, IContainer, Panel, PictureBox, frmRequestComment, EventArgs, frmRequestComment, Button (+26 more)

### Community 486 - "ACM Client — DQS"
Cohesion: 0.04
Nodes (5): IQueryForm, RunStates, QueryOptionsForm, EventArgs, Message

### Community 487 - "ACM Client — SSHTerminal"
Cohesion: 0.04
Nodes (12): Stream, StreamWriter, StringBuilder, XmlWriter, BinaryLogger, DefaultLogger, ITerminalBinaryLogger, ITerminalLogger (+4 more)

### Community 488 - "ACM Client — VNCTerminal"
Cohesion: 0.09
Nodes (14): Config, Deflate, byte, int, short, String, StaticTree, int (+6 more)

### Community 489 - "ASM Server — .PIMUD"
Cohesion: 0.07
Nodes (25): CheckTargetConnection, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent, Network, Boolean (+17 more)

### Community 490 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (20): WebAPIRegistration, Boolean, Int64, String, frmWebAPIRegistration, Boolean, ColumnHeader, DataTable (+12 more)

### Community 491 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (24): _addClass(), assetTarget(), Button(), CheckList(), cleanHeader(), _columnAutoClass(), createElement(), _createNode() (+16 more)

### Community 492 - "Offline MultiTab — Windows Service"
Cohesion: 0.04
Nodes (33): OfflineMultiTabService.Common, OfflineMultiTabService, OfflineMultiTabService.Helper, OfflineMultiTabService.PAMAPISync, OfflineMultiTabService.Models, Compress, Constants, EncodeDecode (+25 more)

### Community 493 - "Offline MultiTab — Offline API"
Cohesion: 0.05
Nodes (29): MultiTabDataBLL, ILog, ARCOSAppType, ARCOSAppTypeName, UserType, string, GetOfflineUsersServicesIds, MultiTabDataDAL (+21 more)

### Community 494 - "ACM Client — Biometric Finger"
Cohesion: 0.12
Nodes (8): GlobalSpaceWrapper, Boolean, Byte, DllImport, int, IntPtr, String, UInt32

### Community 495 - "ACM Client — DQS"
Cohesion: 0.05
Nodes (19): SqlDBClient, IDbCommand, IDbConnection, IDbDataAdapter, SqlInfoMessageEventArgs, OracleDbClient, Boolean, IDbCommand (+11 more)

### Community 496 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (8): GlobalSpaceWrapper, Boolean, Byte, DllImport, int, IntPtr, String, UInt32

### Community 497 - "Services — Desk Insight"
Cohesion: 0.07
Nodes (25): Logger, bool, Boolean, byte, DllImport, EventArgs, EventArrivedEventArgs, float (+17 more)

### Community 498 - "Services — Migrate Data Utility"
Cohesion: 0.08
Nodes (11): AesCryptoServiceProvider, bool, Boolean, ComboBox, DataTable, EventArgs, KeyPressEventArgs, List (+3 more)

### Community 499 - "Onboarding — Service Onboarding"
Cohesion: 0.09
Nodes (21): ARCOSOnBoarding, DateTime, int, string, ARCOSServiceOnBoarding, int, string, Servers (+13 more)

### Community 500 - "ACM Client — SSHTerminal"
Cohesion: 0.07
Nodes (15): Main, AsyncMethodCompletedEventArgs, bool, Boolean, DataReceivedEventArgs, EventArgs, FormClosingEventArgs, Int32 (+7 more)

### Community 501 - "Services — APEMService"
Cohesion: 0.04
Nodes (19): EncryptionDecryption_F, EncryptionDecryption_Web, String, EncryptionDecryption_F, EncryptionDecryption_Web, String, ARCONAPEMService, IContainer (+11 more)

### Community 502 - "ASM Server — SLPF"
Cohesion: 0.07
Nodes (29): CONSOLE_SCREEN_BUFFER_INFO, ConsoleProgressBar, COORD, SMALL_RECT, COORD, DllImport, int, short (+21 more)

### Community 503 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (12): ConfigMapping, bool, Boolean, DateTime, int, string, frmDomainOnBoarding, Boolean (+4 more)

### Community 504 - "ACMO Web — Provisioning Web"
Cohesion: 0.05
Nodes (4): clearMenus(), getParent(), NOTE: POPOVER EXTENDS tooltip.js, ScrollSpy()

### Community 505 - "ACMO Web — APIRA"
Cohesion: 0.05
Nodes (4): clearMenus(), getParent(), NOTE: POPOVER EXTENDS tooltip.js, ScrollSpy()

### Community 506 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (37): U(), a(), ae(), be(), C(), ct(), Ee(), et() (+29 more)

### Community 507 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (52): addChunk(), _addListener(), afterTransform(), afterWrite(), attrib(), beginWhiteSpace(), charAt(), checkListener() (+44 more)

### Community 508 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.08
Nodes (23): COPYDATASTRUCT, DllImport, EventArrivedEventArgs, IntPtr, MemoryStream, Point, Task, COPYDATASTRUCT (+15 more)

### Community 509 - "MultiTab — src"
Cohesion: 0.07
Nodes (17): Initializable, Button, FXML, Label, ObservableList, Override, ResourceBundle, Stage (+9 more)

### Community 510 - "ACM Client — Framework CM"
Cohesion: 0.06
Nodes (23): EnumListItem, EnumValueAttribute, FieldInfo, string, StringResourceDictionary, StringResources, Assembly, Dictionary (+15 more)

### Community 511 - "Services — TSPlugin Service"
Cohesion: 0.07
Nodes (25): NetworkTool, Node, bool, Hashtable, int, IPEndPoint, ISynchronizeInvoke, MessageReceivedDelegate (+17 more)

### Community 512 - "Common — SData Grid View"
Cohesion: 0.07
Nodes (17): DataGridViewAutoFilter, AdvancedDataGridView, ArrayList, bool, Boolean, ContextMenuStrip, DataGridView, DataGridViewCellEventArgs (+9 more)

### Community 513 - "Services — TSPlugin Service"
Cohesion: 0.08
Nodes (20): APIMembers, CustomFolderSettings, FileLogDetails, frmMain, Boolean, DataRow, DataTable, DateTime (+12 more)

### Community 514 - "Services — Windows Vaulting Service"
Cohesion: 0.08
Nodes (22): AppSAPLogonPwdChange, Logger, LogLevel, bool, DllImport, dynamic, EventArgs, int (+14 more)

### Community 515 - "ASM Server — Server Manager"
Cohesion: 0.04
Nodes (38): ComboBox, IContainer, frmServiceReferenceTemplateDesc, Button, CheckBox, ColumnHeader, ComboBox, GroupBox (+30 more)

### Community 516 - "ACM Common — Ticket"
Cohesion: 0.07
Nodes (18): ARCOSTicketDetails, ARCOSTicketEntity, ARCOSTicketSearchCriteria, Boolean, DateTime, int, Int32, List (+10 more)

### Community 517 - "ACMO Web — APIRA"
Cohesion: 0.04
Nodes (4): ExceptionDetails(), Sample(), SamplingScoreGenerator(), SplitTest()

### Community 518 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (50): addPageBreaksIfNecessary(), ae(), ce(), clone(), copyStyle(), createErrorType(), ct(), de() (+42 more)

### Community 519 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (43): a(), ae(), bn(), Bt(), ce(), ee(), fe(), Ft() (+35 more)

### Community 520 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (18): AdminSAML, EventArgs, bool, HttpRequest, HttpResponse, List, string, SamlCustomAttribute (+10 more)

### Community 521 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (16): frmWebAPIRegistration, Boolean, ColumnHeader, DataTable, EventArgs, Int32, Int64, ItemCheckedEventArgs (+8 more)

### Community 522 - "ACM Client — SSHTerminal"
Cohesion: 0.07
Nodes (20): bool, byte, int, IntPtr, long, MemoryStream, Stream, string (+12 more)

### Community 523 - "ACM Common — Connection Properties"
Cohesion: 0.05
Nodes (28): AuthType, BaseObject, AuthType, ServerConnectionProperties, ServerConnectionPropertiesWithAge, bool, Boolean, int (+20 more)

### Community 524 - "ACM Common — Common Functions"
Cohesion: 0.05
Nodes (15): KeyGenerator, DateTime, string, CommonFunctionsUtils, ARCOSEncryptionDecryption, ContextMenuStrip, EncryptionDecryption, EncryptionDecryption_F (+7 more)

### Community 525 - "ACM Common — Tab Strip"
Cohesion: 0.04
Nodes (29): FATabStripItemDesigner, FATabStripItem, IComponent, IDesigner, IDictionary, PaintEventArgs, SelectionRules, FATabStripItemDesigner (+21 more)

### Community 526 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (13): abstract(), addTick(), DateAdapterBase, determineMajorUnit(), determineUnitForAutoTicks(), determineUnitForFormatting(), getAllScaleValues(), getLastIndexInStack() (+5 more)

### Community 527 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (17): addBox(), CategoryScale, changeExponent(), createTitle(), generateTicks(), _getLabelForValue(), getStartAndCountOfVisiblePointsSimplified(), getUserBounds() (+9 more)

### Community 528 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (12): Be(), bo, getLabelAndValue(), getLabelForValue(), getValueForPixel(), jn, ko, n() (+4 more)

### Community 529 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (13): beforeLayout(), buildLookupTable(), En, Fo(), _generate(), getDecimalForValue(), _getTimestampsForTable(), init() (+5 more)

### Community 530 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (9): Be(), gn(), n(), ne(), numeric(), Oe(), pi(), rn() (+1 more)

### Community 531 - "ACMO Web — Portal"
Cohesion: 0.06
Nodes (21): a(), b$(), bk(), bl(), bW(), bY(), bZ(), cp() (+13 more)

### Community 532 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (8): Category, frmScheduleReports, Boolean, EventArgs, int, List, Object, String

### Community 533 - "Services — TSPlugin Service"
Cohesion: 0.06
Nodes (18): IPAddressSet, NetUtil, NMHDR, Util, Win32, DialogResult, DllImport, Form (+10 more)

### Community 534 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (24): frmDatabaseConnectionPleaseWait, IContainer, Label, frmMSSQLConnectionRetry, Boolean, EventArgs, Exception, SqlConnection (+16 more)

### Community 535 - "ACM Client — Script Manager"
Cohesion: 0.04
Nodes (30): frmAddNewData, Button, GroupBox, IContainer, Label, Panel, TextBox, TextBoxWithSave (+22 more)

### Community 536 - "ACM Common — .User Controls"
Cohesion: 0.05
Nodes (21): DgvBaseFilterHost, Bitmap, Color, ComboBox, Control, EventArgs, Region, Size (+13 more)

### Community 537 - "ACM Common — S"
Cohesion: 0.06
Nodes (21): frmARCONSMobileOTPValidator, Boolean, EventArgs, FormClosingEventArgs, Int32, MouseEventArgs, DualFactorConfig, Int32 (+13 more)

### Community 538 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (37): addHandler(), bootstrapDelegationHandler(), bootstrapHandler(), find(), findHandler(), focusableChildren(), get(), getDataAttribute() (+29 more)

### Community 539 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (9): AudioTrackButton(), Button(), CustomControlSpacer(), isInFrame(), Menu(), MenuButton(), prependTo(), setAttribute() (+1 more)

### Community 540 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (10): AudioTrackMenuItem(), CaptionsButton(), ChaptersTrackMenuItem(), ErrorDisplay(), MenuItem(), OffTextTrackMenuItem(), PlaybackRateMenuButton(), PlaybackRateMenuItem() (+2 more)

### Community 541 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (37): addHandler(), bootstrapDelegationHandler(), bootstrapHandler(), find(), findHandler(), focusableChildren(), get(), getDataAttribute() (+29 more)

### Community 542 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (7): h2cRenderContext(), CanvasRenderer(), Color(), hasEntries(), isPercentage(), Renderer(), Support()

### Community 543 - "ACMO Web — Portal"
Cohesion: 0.04
Nodes (21): TODO: determine which cases actually cause this to happen, TODO: Unwrap at same DOM position, TODO: make renderAxis a prototype function, TODO: Seems like a bug to cache this.outerDimensions, TODO: remove after 1.12, TODO: Remove hack when datepicker implements, TODO: switch return back to widget declaration at top of file when this is…, TODO: Remove in 1.13 along with call to it below (+13 more)

### Community 544 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (15): frmRDPLogViewer_Streaming, AsyncCompletedEventArgs, bool, Boolean, Double, EventArgs, FormClosingEventArgs, Image (+7 more)

### Community 545 - "Services — Provisioning Scheduler"
Cohesion: 0.08
Nodes (21): ArrayList, bool, string, ConnectionParam, DatabaseConnection, DataSet, DataTable, IList (+13 more)

### Community 546 - "Services — Staging Log Sync"
Cohesion: 0.09
Nodes (22): ARCOSStagingLogSyncService, Boolean, EventArgs, Int32, String, Timer, ARCOSStagingLogSyncServiceONS, Boolean (+14 more)

### Community 547 - "MultiTab — src"
Cohesion: 0.08
Nodes (18): Button, ChoiceBox, FXML, Label, ObservableList, Override, ResourceBundle, Stage (+10 more)

### Community 548 - "ACM Client — Framework CM"
Cohesion: 0.06
Nodes (29): DataCapturedEventArgs, Delay, Packet, Precedence, Protocol, Reliability, Throughput, byte (+21 more)

### Community 549 - "ACMO Web — Provisioning Web"
Cohesion: 0.06
Nodes (20): ApiDescriptionExtensions, HelpPageConfig, HttpConfiguration, SuppressMessage, HelpPageAreaRegistration, ImageSample, InvalidSample, TextSample (+12 more)

### Community 550 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (32): a(), ae(), b(), c(), ce(), d(), de(), ee() (+24 more)

### Community 551 - "ACMO Web — Portal"
Cohesion: 0.08
Nodes (33): a(), ae(), b(), c(), ce(), d(), de(), ee() (+25 more)

### Community 552 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (20): DataSet2, DataTable1DataTable, DataTable1Row, CollectionChangeEventArgs, DataColumn, DataRelationCollection, DataRow, DataRowBuilder (+12 more)

### Community 553 - "Services — Desk Insight"
Cohesion: 0.09
Nodes (15): bool, ElapsedEventArgs, EventArgs, EventLog, EventLogEntryType, List, string, Timer (+7 more)

### Community 554 - "Services — Z POC"
Cohesion: 0.06
Nodes (25): bool, ForwardedPortLocal, SafeHandle, SecureShellConnection, SshClient, string, ARCONVPNClient, bool (+17 more)

### Community 555 - "MultiTab — src"
Cohesion: 0.09
Nodes (17): Button, ChoiceBox, FXML, Label, ObservableList, Override, ResourceBundle, Stage (+9 more)

### Community 556 - "MultiTab — src"
Cohesion: 0.08
Nodes (4): JSONArray, JsonProperty, Override, RaiseServiceAccessRequest

### Community 557 - "ACM Client — Sshkey SFTP"
Cohesion: 0.10
Nodes (13): AsyncMethodCompletedEventArgs, Color, Control, Exception, FileInfoBase, FileInfoCollection, IList, KeyEventArgs (+5 more)

### Community 558 - "Services — TSPlugin Service"
Cohesion: 0.06
Nodes (20): ChannelStatusChangedDelegate, DataReceivedDelegate, Exception, Dump(), SCPChannelStatus, SCPClientChannelEventReceiver, byte, ChannelStatusChangedDelegate (+12 more)

### Community 559 - "ASM Server — .User Controls"
Cohesion: 0.04
Nodes (25): GripBounds, int, Rectangle, PopupComboBox, IContainer, ctlPopupToolTip, IContainer, Label (+17 more)

### Community 560 - "ACM Common — SData Grid"
Cohesion: 0.08
Nodes (15): DataGridViewAutoFilter, AdvancedDataGridView, ArrayList, bool, Boolean, ContextMenuStrip, DataGridView, DataGridViewColumn (+7 more)

### Community 561 - "ACM Common — SLPF"
Cohesion: 0.06
Nodes (25): bool, CipherMode, ICryptoTransform, int, KeySizes, PaddingMode, RijndaelManaged, RijndaelCryptoServiceProvider (+17 more)

### Community 562 - "ACM Common — SSHKey Common"
Cohesion: 0.08
Nodes (14): MSSqlDBConnection, SqlConnection, String, SqlConnection, SSHKeyCommon, DataTable, Int32, SqlConnection (+6 more)

### Community 563 - "PAMSSHWRAPPER — SSHKey Generation"
Cohesion: 0.12
Nodes (14): SSHKeyGeneration, Exception, SshClient, SshKey, ErrorModel, KeyCurve, Response, SSHModel (+6 more)

### Community 564 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (15): CustomHeaderModule, Global_asax, bool, CacheEntryUpdateArguments, ElapsedEventArgs, EventArgs, HttpApplication, Page (+7 more)

### Community 565 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (8): BaseComponent, Config, enableDismissTrigger(), getElement(), isDisabled(), isElement(), TemplateFactory, toType()

### Community 566 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (18): afterDraw(), afterEvent(), alignX(), alignY(), BasicPlatform, createTooltipContext(), determineAlignment(), determineYAlign() (+10 more)

### Community 567 - "Offline MultiTab — Offline API"
Cohesion: 0.08
Nodes (24): LogImageBLL, Bitmap, int, Size, Task, Tuple, DatabaseCrud, ARCOSLogManagerSettings (+16 more)

### Community 568 - "Services — Log Manager Service"
Cohesion: 0.09
Nodes (15): ARCOSApp, CommonFunctions, ARCOSLogManagerSettings, bool, CommandType, DataSet, DataTable, EventLog (+7 more)

### Community 569 - "Services — Windows Vaulting Service"
Cohesion: 0.07
Nodes (10): bool, DllImport, int, IntPtr, Program, int, Task, TcpClient (+2 more)

### Community 570 - "Offline MultiTab — Offline API"
Cohesion: 0.11
Nodes (22): ConfigurationBLL, ILog, List, ConfigurationDAL, ILog, List, APIConfiguration, ArcosConfigSLS (+14 more)

### Community 571 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (29): CaseInsensitiveComparer, int, SortOrder, LocalListViewColumnSorter, DataGridViewComparer, int, SortOrder, ListViewComparer (+21 more)

### Community 572 - "ACM Client — SSHTerminal"
Cohesion: 0.06
Nodes (20): ArrayList, bool, CommandResult, int, TextReader, PasteProcessor, Button, Container (+12 more)

### Community 573 - "Services — TSPlugin Service"
Cohesion: 0.08
Nodes (11): TickEventArgs, bool, ARCONAppIdleTime, bool, EventArgs, IAsyncResult, IContainer, Message (+3 more)

### Community 574 - "ACM Client — SSHTerminal"
Cohesion: 0.10
Nodes (5): int, Random, uint, BigInteger, Granados

### Community 575 - "ACM Common — .User Controls"
Cohesion: 0.06
Nodes (23): DgvFilterManager, BindingSource, bool, DataGridView, DataGridViewCellMouseEventArgs, DataGridViewCellPaintingEventArgs, DataGridViewColumn, DataGridViewColumnEventArgs (+15 more)

### Community 576 - "ACM Common — SEncrypt Decrypt"
Cohesion: 0.07
Nodes (17): CryptoRandom, byte, int, RNGCryptoServiceProvider, CryptoRandom, byte, int, RNGCryptoServiceProvider (+9 more)

### Community 577 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (7): frmUserPrivilegesSetting, Boolean, DataTable, EventArgs, int, ListViewItem, string

### Community 578 - "Services — Data Sync"
Cohesion: 0.05
Nodes (33): CommandLogDetails, DateTime, Int32, CommandLogResponse, DateTime, EndUserServiceSession, GenericResponse, GenricResponse (+25 more)

### Community 579 - "MultiTab — src"
Cohesion: 0.09
Nodes (18): description, Button, ChoiceBox, FXML, Label, ObservableList, Override, ResourceBundle (+10 more)

### Community 580 - "MultiTab — src"
Cohesion: 0.11
Nodes (19): Cursor, MouseEvent, Node, Stage, TreeView, VBox, OnDragResizeEventListener, S (+11 more)

### Community 581 - "ACM Client — SFTPTeminal"
Cohesion: 0.09
Nodes (27): ArrayList, bool, byte, DllImport, Hashtable, Icon, int, IntPtr (+19 more)

### Community 582 - "Services — TSPlugin Service"
Cohesion: 0.07
Nodes (17): frmARCOSVPNClientV4, ARCOSVPNDetails, Boolean, EventArgs, ARCOSVPNDetails, Boolean, string, frmARCOSVPNClientV4 (+9 more)

### Community 583 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (16): ServiceTypes, DateTime, int, string, frmController, bool, EventArgs, int (+8 more)

### Community 584 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (16): ReconciliationScheduler, DateTime, int, String, ReconciliationSchedulerFunctions, DataTable, String, frmScheduleReconciliation (+8 more)

### Community 585 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (25): An(), at(), ct(), Dn(), En(), fn(), gt(), Hn() (+17 more)

### Community 586 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (14): AddressFamily, AsyncCallback, EndPoint, IAsyncResult, IntPtr, ProtocolType, SelectMode, Socket (+6 more)

### Community 587 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (34): frmServiceAccessRequestTimeBased, Boolean, EventArgs, FormClosedEventArgs, Int32, ListView, ListViewItem, string (+26 more)

### Community 588 - "Common — SLPF"
Cohesion: 0.09
Nodes (14): AddressFamily, AsyncCallback, EndPoint, IAsyncResult, IntPtr, ProtocolType, SelectMode, Socket (+6 more)

### Community 589 - "Services — Desk Insight"
Cohesion: 0.10
Nodes (28): Boolean, byte, DllImport, Guid, int, IntPtr, List, long (+20 more)

### Community 590 - "Services — Log Manager Service"
Cohesion: 0.10
Nodes (13): CommonFunctions, bool, CommandType, DataSet, DataTable, EventLog, Hashtable, Int32 (+5 more)

### Community 591 - "Services — Schedule Password Change"
Cohesion: 0.09
Nodes (14): AddressFamily, AsyncCallback, EndPoint, IAsyncResult, IntPtr, ProtocolType, SelectMode, Socket (+6 more)

### Community 592 - "Services — Schedule Password Change"
Cohesion: 0.09
Nodes (14): AddressFamily, AsyncCallback, EndPoint, IAsyncResult, IntPtr, ProtocolType, SelectMode, Socket (+6 more)

### Community 593 - "Services — TSPlugin Service"
Cohesion: 0.09
Nodes (14): AddressFamily, AsyncCallback, EndPoint, IAsyncResult, IntPtr, ProtocolType, SelectMode, Socket (+6 more)

### Community 594 - "Onboarding — Common Enum"
Cohesion: 0.05
Nodes (42): AccountType, AlertNotificationMode, ARCOSAppType, ARCOSAppTypeName, ARCOSCPCSServerType, ARCOSFileStorageType, ARCOSLogType, ARCOSOnBoardingType (+34 more)

### Community 595 - "ACM Client — Framework CM"
Cohesion: 0.10
Nodes (21): CURSORINFO, ICONINFO, MouseEventDataXButtons, MouseEventFlags, POINT, RECT, TernaryRasterOperations, WindowsApi (+13 more)

### Community 596 - "ACM Client — SSHTerminal"
Cohesion: 0.09
Nodes (19): Color, DrawItemEventArgs, Font, int, Keys, Pen, SolidBrush, Consts (+11 more)

### Community 597 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (6): ChaptersButton(), createTrackHelper(), Html5(), HtmlTrackElementList(), TextTrackList(), TrackList()

### Community 598 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (13): abstract(), addTick(), DateAdapterBase, determineMajorUnit(), determineUnitForAutoTicks(), determineUnitForFormatting(), interpolate(), interpolatedLineTo() (+5 more)

### Community 599 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (42): _fnBlur(), _fnCaptureKeys(), _fnCellFromCoords(), _fnClick(), _fnCoordsFromCell(), _fnEventAdd(), _fnEventAddTemplate(), _fnEventFire() (+34 more)

### Community 600 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (32): addNamespace(), addNamespacesAndStylesheet(), appendFill(), appendStroke(), assertImageIsValid(), CanvasGradient_(), CanvasPattern_(), CanvasRenderingContext2D_() (+24 more)

### Community 601 - "ACMO Web — Portal"
Cohesion: 0.07
Nodes (32): addNamespace(), addNamespacesAndStylesheet(), appendFill(), appendStroke(), assertImageIsValid(), CanvasGradient_(), CanvasPattern_(), CanvasRenderingContext2D_() (+24 more)

### Community 602 - "Services — TSPlugin Service"
Cohesion: 0.10
Nodes (19): ActivityLog, ARCOSProcess, ARCOSTSPlugin, CommonAPI, CommonFunctions, SensLogonEventArgs, SensLogonEventType, Boolean (+11 more)

### Community 603 - "Services — Log Archiver Service"
Cohesion: 0.07
Nodes (26): ApplicationSettingsBase, Settings, Settings, Resources, CultureInfo, ResourceManager, Settings, Settings (+18 more)

### Community 604 - "ACM Client — DQS"
Cohesion: 0.10
Nodes (15): MYSQLCodeSnippetClass, OracleCodeSnippetClass, Test, ArrayList, Dictionary, int, Int32, string (+7 more)

### Community 605 - "ACM Client — Framework CM"
Cohesion: 0.06
Nodes (18): HelperTool, NameValuePair, SerializableHashtable, Bitmap, Image, ImageCodecInfo, object, string (+10 more)

### Community 606 - "ACM Client — Framework CM"
Cohesion: 0.07
Nodes (23): UInt16, UInt32, HARDWAREINPUT, UInt32, INPUT, DllImport, IEnumerable, Int16 (+15 more)

### Community 607 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (16): frmAPIRegistration, bool, DataTable, EventArgs, HttpWebRequest, int, Message, WebMethod (+8 more)

### Community 608 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (13): frmARCOSDashboardPassword, EventArgs, String, frmARCOSDashboardPerfMonIT, EventArgs, Int32, String, frmARCOSDashboardServerSessions (+5 more)

### Community 610 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (14): addClass(), AudioTrack(), Component(), getAttributes(), MediaLoader(), mergeOptions(), removeAttribute(), setAttributes() (+6 more)

### Community 613 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (14): DataGridViewAutoFilter, ArrayList, bool, Boolean, ContextMenuStrip, DataGridView, DataGridViewColumn, DataGridViewColumnEventArgs (+6 more)

### Community 614 - "Services — Script Scheduler"
Cohesion: 0.08
Nodes (18): EventLogEntryType, HttpWebRequest, Boolean, DataRow, Dictionary, Encoding, EventArgs, HttpContent (+10 more)

### Community 615 - "Offline MultiTab — Offline API"
Cohesion: 0.06
Nodes (36): Cassia (2.0.0.60), EntityFramework (6.4.4), Microsoft.AspNetCore.Authentication.JwtBearer (3.1.11), Microsoft.AspNetCore.Mvc.NewtonsoftJson (3.1.11), Microsoft.EntityFrameworkCore (3.1.11), Microsoft.EntityFrameworkCore.Design (3.1.11), Microsoft.EntityFrameworkCore.Sqlite (3.1.11), Microsoft.EntityFrameworkCore.Tools (3.1.11) (+28 more)

### Community 616 - "ACM Common — .User Controls"
Cohesion: 0.07
Nodes (21): frmPleaseWait, Button, IContainer, Label, PictureBox, ARCONCoolProgressBar, bool, Color (+13 more)

### Community 617 - "ACM Client — Script Manager"
Cohesion: 0.09
Nodes (9): frmScriptManager, Boolean, DataTable, EventArgs, ListViewItem, MouseEventArgs, SplitterEventArgs, String (+1 more)

### Community 618 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (13): ARCOSServerMaster, Boolean, Int32, long, String, frmARCOSServerMaster, Boolean, DrawListViewColumnHeaderEventArgs (+5 more)

### Community 619 - "Services — User On Boarding"
Cohesion: 0.15
Nodes (9): ARCOSServiceOnBoarding, int, string, ServiceOnboarding, Boolean, DataTable, List, SqlParameter (+1 more)

### Community 620 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (3): Button, Collapse, Toast

### Community 621 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (12): le(), ue(), bn(), ce(), de, dt(), he(), pn() (+4 more)

### Community 622 - "Services — Schedule Password Change"
Cohesion: 0.07
Nodes (23): authenticateUserCompletedEventArgs, changeUserPassCompletedEventArgs, ResponseType, StatusCodeType, UCPService, bool, object, SendOrPostCallback (+15 more)

### Community 623 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.10
Nodes (20): ArcosSSMDesktop.Utility, Dispatcher, Key, KeyboardCallbackAsync, InterceptKeys, KeyboardListener, KeyEvent, RawKeyEventArgs (+12 more)

### Community 624 - "MultiTab — src"
Cohesion: 0.12
Nodes (16): DragResizeMod, Cursor, MouseEvent, Node, OnDragResizeEventListener, S, DEFAULT, DRAG (+8 more)

### Community 625 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (3): ExpectedException, Test, SCPChannelStreamTest

### Community 626 - "ACM Common — SEncrypt Decrypt"
Cohesion: 0.10
Nodes (15): CryptoHash, CryptoHashType, String, CryptoHash, CryptoHashType, String, CryptoHash, CryptoHashType (+7 more)

### Community 627 - "Services — User On Boarding"
Cohesion: 0.12
Nodes (18): CommonFunctionsDB, Boolean, CommandType, DataSet, DataTable, SqlConnection, SqlConnectionStringBuilder, SqlParameter (+10 more)

### Community 628 - "ACM Client — Network Devices"
Cohesion: 0.07
Nodes (20): frmARCOSAppNetnumanZTEGSM, ApplicationIdle, Bitmap, bool, Button, byte, ContextMenuStrip, DllImport (+12 more)

### Community 630 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (3): Button, Collapse, Toast

### Community 631 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (36): c(), F(), g(), GetNextKey(), NextTableBitSize(), ReplicateValue(), p(), A() (+28 more)

### Community 632 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (5): DataTable1Row, DataRow, DataRowBuilder, DebuggerNonUserCodeAttribute, GeneratedCodeAttribute

### Community 633 - "ASM Server — Pkcs11Interop"
Cohesion: 0.07
Nodes (15): IPkcs11InteropLogger, IPkcs11InteropLoggerFactory, Exception, NullPkcs11InteropLogger, NullPkcs11InteropLoggerFactory, Pkcs11InteropLoggerFactory, Pkcs11InteropLogLevel, bool (+7 more)

### Community 634 - "Common — UITheme"
Cohesion: 0.07
Nodes (17): ARCOSUITheme, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+9 more)

### Community 635 - "Services — PAM Agents"
Cohesion: 0.09
Nodes (11): AppRegistryUpdater, AutoUpdateService, FileManager, GlobalSettings, string, Program, ReportLogger, ServiceManager (+3 more)

### Community 636 - "Services — DBSync Service"
Cohesion: 0.06
Nodes (22): frmAboutBox, EventArgs, frmAboutBox, Button, IContainer, Label, PictureBox, TableLayoutPanel (+14 more)

### Community 637 - "Services — Desk Insight"
Cohesion: 0.08
Nodes (10): CaptureLocation, MTPRestriction, SecurityEvent, DateTime, EventArgs, SnippingRestrict, WindowsServicecManager, EventArgs (+2 more)

### Community 638 - "Services — Desk Insight"
Cohesion: 0.06
Nodes (23): frmARCONRAMainInternet, Button, ContextMenuStrip, GroupBox, IContainer, Label, NotifyIcon, Panel (+15 more)

### Community 639 - "Services — Migrate Data Utility"
Cohesion: 0.07
Nodes (17): ARCOSUITheme, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+9 more)

### Community 640 - "ACM Client — RStream Client"
Cohesion: 0.11
Nodes (18): CURSORINFO, ICONINFO, MouseEventDataXButtons, MouseEventFlags, POINT, RECT, TernaryRasterOperations, WindowsApi (+10 more)

### Community 641 - "ACM Client — Sshkey SFTP"
Cohesion: 0.09
Nodes (14): AsyncCompletedEventArgs, ConnectionState, Setting, EventArgs, SettingInfo, bool, int, string (+6 more)

### Community 642 - "ACM Client — Framework CM"
Cohesion: 0.12
Nodes (17): KeyLogger, LASTINPUTINFO, RECT, WINDOWINFO, bool, DllImport, EventArgs, int (+9 more)

### Community 643 - "ACM Common — SList View"
Cohesion: 0.09
Nodes (12): ListViewAutoFiler, ArrayList, bool, Boolean, ColumnHeader, ColumnWidthChangedEventArgs, ContextMenuStrip, EventArgs (+4 more)

### Community 644 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (7): frmAPIApplicationNameMapping, EventArgs, RepeaterCommandEventArgs, frmAPIDefaultServiceCreationConfig, EventArgs, RepeaterCommandEventArgs, DefaultServiceConfig

### Community 645 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (4): BaseComponent, Config, sanitizeHtml(), TemplateFactory

### Community 646 - "ACMO Web — Client Manager"
Cohesion: 0.23
Nodes (27): a(), b(), c(), ct(), d(), e(), f(), g() (+19 more)

### Community 647 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (4): BaseComponent, Config, sanitizeHtml(), TemplateFactory

### Community 648 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (20): bo, bs(), ct(), Fs(), ge(), getRange(), _i(), is() (+12 more)

### Community 649 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (12): ListViewAutoFiler, ArrayList, bool, Boolean, ColumnHeader, ColumnWidthChangedEventArgs, ContextMenuStrip, EventArgs (+4 more)

### Community 650 - "Common — SList View Addin"
Cohesion: 0.09
Nodes (12): ListViewAutoFiler, ArrayList, bool, Boolean, ColumnHeader, ColumnWidthChangedEventArgs, ContextMenuStrip, EventArgs (+4 more)

### Community 651 - "Services — Desk Insight"
Cohesion: 0.08
Nodes (16): ARCOSUITheme, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+8 more)

### Community 652 - "Services — Log Manager Service"
Cohesion: 0.11
Nodes (18): ARCOSLogManagerService, Bitmap, Boolean, DataTable, EventArgs, int, Size, string (+10 more)

### Community 653 - "Services — Passworde Envelope Manager"
Cohesion: 0.08
Nodes (16): ARCOSUITheme, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+8 more)

### Community 654 - "ASM Server — Server Manager"
Cohesion: 0.05
Nodes (26): GetFingerPrint, Button, CheckBox, ComboBox, GroupBox, IContainer, Label, Panel (+18 more)

### Community 655 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (12): HSMData, int, string, Boolean, DataRow, frmHSMConfig, Boolean, EventArgs (+4 more)

### Community 656 - "ACMO Web — Offline API"
Cohesion: 0.08
Nodes (20): HelpController, ActionResult, HttpConfiguration, string, HomeController, HomeController, ActionResult, HttpPost (+12 more)

### Community 657 - "ACMO Web — Client Manager"
Cohesion: 0.05
Nodes (37): ACMO_New, CheckBox, ContentPlaceHolder, DropDownList, HiddenField, HtmlForm, HtmlGenericControl, HyperLink (+29 more)

### Community 658 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (4): BaseComponent, Config, sanitizeHtml(), TemplateFactory

### Community 659 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (3): Es, fs(), Es

### Community 660 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (4): bufferedPercent(), createTimeRanges(), createTimeRangesObj(), Tech()

### Community 661 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (12): computeCircularBoundary(), createPointLabelContext(), determineLimits(), drawArc(), drawRadiusLine(), fitWithPointLabels(), _getTargetValue(), getTickBackdropHeight() (+4 more)

### Community 662 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (9): frmSchedulePasswordEnvelope, Boolean, DataTable, EventArgs, ItemCheckedEventArgs, List, String, frmAboutBox (+1 more)

### Community 663 - "Services — TSPlugin Service"
Cohesion: 0.09
Nodes (24): WTS_CONNECTSTATE_CLASS, WTS_SESSION_INFO, UInt32, TerminalSessionData, TerminalSessionInfo, TermServicesManager, WTS_CLIENT_ADDRESS, WTS_CLIENT_DISPLAY (+16 more)

### Community 664 - "Services — TSPlugin Service"
Cohesion: 0.11
Nodes (20): CURSORINFO, ICONINFO, MouseEventDataXButtons, MouseEventFlags, POINT, RECT, TernaryRasterOperations, WindowsApi (+12 more)

### Community 665 - "Services — User On Boarding"
Cohesion: 0.07
Nodes (16): ARCOSUITheme, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+8 more)

### Community 666 - "Services — Windows Vaulting Service"
Cohesion: 0.07
Nodes (10): bool, DllImport, LdapConnection, SafeHandle, string, UInt32, X509Certificate, USER_INFO_1003 (+2 more)

### Community 667 - "Offline MultiTab — Offline API"
Cohesion: 0.06
Nodes (24): ControllerBase, RASynBLL, ILog, List, EncryptDecrypt, EncryptDecrypt_F, ARCOSEncryptionDecryption, DateTime (+16 more)

### Community 668 - "Offline MultiTab — Offline API"
Cohesion: 0.07
Nodes (31): ActivityLogsBLL, ILog, List, AccessControlLogData, AccessControlResponse, ObjectTextData, PsrBulkActivity, TextData (+23 more)

### Community 669 - "ACM Client — VNCTerminal"
Cohesion: 0.06
Nodes (18): ApplicationException, TelnetNegotiationException, int, string, ConnectEventArgs, Bitmap, Rectangle, IDesktopUpdater (+10 more)

### Community 670 - "ACM Client — RStream Client"
Cohesion: 0.09
Nodes (11): EncryptionDecryption, Byte, string, ToolWindow, DataTable, EventArgs, ILog, Program (+3 more)

### Community 671 - "ACM Client — VNCTerminal"
Cohesion: 0.06
Nodes (18): Adler32, int, SupportClass, Int32, Stream, String, TextReader, ZInputStream (+10 more)

### Community 672 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (37): addTimeToArrayFromToken(), checkOverflow(), compareArrays(), computeMonthsParse(), computeWeekdaysParse(), configFromInput(), configFromISO(), configFromString() (+29 more)

### Community 673 - "ACMO Web — Common Functions"
Cohesion: 0.08
Nodes (15): ARCOSUITheme_Temp, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+7 more)

### Community 674 - "ACMO Web — Portal"
Cohesion: 0.09
Nodes (36): assertNodeNotReadOnly(), assertNoDocTypeNotationEntityAncestor(), assertRangeValid(), assertValidNodeType(), assertValidOffset(), comparePoints(), createIterator(), createPrototypeRange() (+28 more)

### Community 675 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): CheckTargateConnectivity, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent, frmPrivilegedUserDiscovery_Popup, ArrayList (+6 more)

### Community 676 - "Services — APEMService"
Cohesion: 0.09
Nodes (20): ARCONAPEMService, WebAPI, EventArgs, SqlParameter, string, Timer, clsLog, FileParams (+12 more)

### Community 677 - "Services — Passworde Envelope Manager"
Cohesion: 0.06
Nodes (20): frmAddNewData, EventArgs, String, frmAddNewData, Button, GroupBox, IContainer, Label (+12 more)

### Community 678 - "Services — TSPlugin Service"
Cohesion: 0.10
Nodes (11): ListViewAutoFiler, ArrayList, bool, Boolean, ColumnHeader, ColumnWidthChangedEventArgs, EventArgs, Int32 (+3 more)

### Community 679 - "Services — Windows Service Updater"
Cohesion: 0.08
Nodes (14): APICall, EncryptDecrypt, Program, String, Settings, bool, DateTime, EventArgs (+6 more)

### Community 680 - "ACM Client — PAMSecure SSOApps"
Cohesion: 0.08
Nodes (24): ARCONPAMGlobalHook, keyboardHookStruct, DllImport, int, IntPtr, keyboardHookProc, List, frmSecureSSOApps (+16 more)

### Community 681 - "ACM Client — Framework CM"
Cohesion: 0.09
Nodes (18): ARCOSSessionLog, ARCOSSLS001, InitializeConnectionCompletedEventArgs, IsConnectedCompletedEventArgs, SessionLogDataCompletedEventArgs, bool, byte, DateTime (+10 more)

### Community 682 - "ASM Server — Enitity Objects"
Cohesion: 0.07
Nodes (32): ARCOSTicketActionType, ARCOSTicketActionType, ARCOSTicketDetails, ARCOSTicketEntity, ARCOSTicketSearchCriteria, Boolean, DateTime, int (+24 more)

### Community 683 - "Common — Password Manager"
Cohesion: 0.11
Nodes (17): UtimacoHSMData, UtimacoInput, List, List, HSMCommonFunctionSPC, DataTable, List, UtimacoInput (+9 more)

### Community 684 - "ACM Common — UITheme"
Cohesion: 0.08
Nodes (16): ARCOSUITheme, ArrayList, Color, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs, Font (+8 more)

### Community 685 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (17): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+9 more)

### Community 686 - "Services — Schedule Password Change"
Cohesion: 0.07
Nodes (14): ArrayList, bool, int, string, StringBuilder, ushort, ActionCode, AttrListImpl (+6 more)

### Community 687 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.08
Nodes (26): ArcosCompression, ArcosSSMDesktop.Pulley, CompressionTypes, LogData, Rect, ObjectTextData, RDPImageDbDetails, SsmModel (+18 more)

### Community 688 - "ACM Client — Framework CM"
Cohesion: 0.09
Nodes (17): AuthenticationResult, Task, frmLogin, VideoRecordingStatus, Boolean, ComboBox, Control, DataTable (+9 more)

### Community 689 - "ACM Common — APICalling"
Cohesion: 0.09
Nodes (13): JObject, PlatformFile, UniversalProxy, Process, APIWrapper, bool, HttpWebRequest, JObject (+5 more)

### Community 690 - "ACM Client — Framework CM"
Cohesion: 0.08
Nodes (18): ARCOSUITheme, FilePath, UserMessage, ArrayList, Color, Control, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs (+10 more)

### Community 691 - "ACM Client — Framework CM"
Cohesion: 0.08
Nodes (21): ServerSessionLogger, bool, Byte, DllImport, Int16, Int32, IntPtr, object (+13 more)

### Community 692 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (12): ServiceCriticalCommands, Boolean, Int32, String, frmServiceCriticalCommands, Boolean, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs (+4 more)

### Community 693 - "ACM Common — VPNClient"
Cohesion: 0.09
Nodes (17): frmARCOSVPNClientV4, MyUserInfo, Boolean, DllImport, EventArgs, ForwardedPortLocal, int, Int32 (+9 more)

### Community 694 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (10): clsOnboarding, lstcls, xmlgrp, Boolean, DataTable, int, Int32, List (+2 more)

### Community 696 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (16): ArcElement, BarElement, binarySearch(), dataset(), Element, evaluateInteractionItems(), getAxisItems(), getDistanceMetricForAxis() (+8 more)

### Community 697 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (16): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 698 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (11): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), jo() (+3 more)

### Community 699 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (13): beforeLayout(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), Go(), ho() (+5 more)

### Community 700 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (12): ArchivedLogEntry, frmARCONArchivedLogs, bool, DataTable, DateTime, Dictionary, EventArgs, int (+4 more)

### Community 701 - "ACMO Web — User Access"
Cohesion: 0.11
Nodes (16): DefaultV2, Boolean, EventArgs, DefaultV3, Boolean, EventArgs, Boolean, EventArgs (+8 more)

### Community 702 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (23): DataSet1, CachedrptPasswordEnvelop, rptPasswordEnvelop, ReportDocument, RequestContext, Section, TimeSpan, CachedrptPasswordEnvelopA4 (+15 more)

### Community 703 - "Common — VPNClient"
Cohesion: 0.09
Nodes (17): frmARCOSVPNClientV4, MyUserInfo, Boolean, DllImport, EventArgs, ForwardedPortLocal, int, Int32 (+9 more)

### Community 704 - "MultiTab — src"
Cohesion: 0.10
Nodes (4): Override, PreferencesModel, Override, UserServicePrefrence

### Community 705 - "ACM Client — SSHTerminal"
Cohesion: 0.06
Nodes (21): Config, Button, IContainer, TreeView, Login, Button, ComboBox, IContainer (+13 more)

### Community 706 - "ACM Client — Web Browser"
Cohesion: 0.06
Nodes (3): WebBrowserExtendedEvents, DispId, DWebBrowserEvents2

### Community 707 - "Common — .User Controls"
Cohesion: 0.09
Nodes (18): PopupAnimations, Popup, bool, CancelEventArgs, Control, CreateParams, EventArgs, int (+10 more)

### Community 708 - "Services — Schedule Password Change"
Cohesion: 0.10
Nodes (28): Sign, Compare(), Compare(), BarrettReduction(), bitCount(), clearBit(), Compare(), BigInteger (+20 more)

### Community 709 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (15): SqlHelperParameterCache, Hashtable, SqlParameter, SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet (+7 more)

### Community 710 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (21): DataTableCollection, frmCommandLogTextViewer, Boolean, DataTableCollection, Double, EventArgs, int, LogNavigator (+13 more)

### Community 711 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (15): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+7 more)

### Community 712 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (7): Cs, fe(), ks(), nn(), os(), sn, xt

### Community 713 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (16): K(), a(), b$(), bj(), bk(), bZ(), co(), cp() (+8 more)

### Community 714 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (11): afterUpdate(), calculateItemHeight(), calculateItemSize(), calculateItemWidth(), calculateLegendItemHeight(), getBoxSize(), getTickBackdropHeight(), isListened() (+3 more)

### Community 715 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (6): Animation, Animations, Animator, awaitAll(), PluginService, resolveTargetOptions()

### Community 716 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 717 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 718 - "ACMO Web — Portal"
Cohesion: 0.09
Nodes (34): addFormatToken(), addWeekYearFormatToken(), create__createDuration(), duration_humanize__relativeTime(), expandFormat(), format(), formatMoment(), from() (+26 more)

### Community 719 - "ACMO Web — Portal"
Cohesion: 0.40
Nodes (30): a(), b(), c(), d(), e(), f(), g(), ga() (+22 more)

### Community 720 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (14): ArrayList, bool, int, string, StringBuilder, ushort, ActionCode, AttrListImpl (+6 more)

### Community 722 - "Common — Enitity Objects"
Cohesion: 0.05
Nodes (27): ARCOSCommonModifyParameter, Byte, int, string, PrivilegedAccountPasswordChange, Int64, String, ARCOSCommonModifyParameter (+19 more)

### Community 723 - "Services — Arcon File Upload"
Cohesion: 0.09
Nodes (18): APIcls, ARCOSFileStorageEntity, CommonFunctionsACMO, HttpRequestDetails, UploadFileDetails, byte, DateTime, HttpWebRequest (+10 more)

### Community 724 - "Services — Desk Insight"
Cohesion: 0.11
Nodes (15): ProxyTestController, CertificateSelectionEventArgs, CertificateValidationEventArgs, ConsoleColor, DataEventArgs, ExplicitProxyEndPoint, IExternalProxy, MultipartRequestPartSentEventArgs (+7 more)

### Community 725 - "Services — Migrate Data Utility"
Cohesion: 0.13
Nodes (12): DataSet, DataTable, SqlCommand, SqlConnection, SqlParameter, PrimarySqlDbConnectionBase, DataSet, DataTable (+4 more)

### Community 726 - "MultiTab — src"
Cohesion: 0.09
Nodes (9): Override, KeyValue, Stage, SuppressWarnings, Tab, PAMApplicationHelper, Root, XMLConvertor (+1 more)

### Community 727 - "ACM Client — DQS"
Cohesion: 0.08
Nodes (4): IPOSTGREBrowser, Boolean, StringCollection, TreeNode

### Community 728 - "ACM Client — SSHTerminal"
Cohesion: 0.10
Nodes (19): IFileInfo, int, SortOrder, ListViewItemComparerBase, ListViewItemDateComparer, ListViewItemNameComparer, ListViewItemPermissionsComparer, ListViewItemSizeComparer (+11 more)

### Community 729 - "ACM Client — SFTPTeminal"
Cohesion: 0.09
Nodes (13): EventArgs, Setting, bool, int, string, SettingInfo, DllImport, Form (+5 more)

### Community 730 - "ACM Client — SSHTerminal"
Cohesion: 0.07
Nodes (15): Config, Dictionary, EventArgs, TreeViewEventArgs, AppearancePage, bool, BasePage, TerminalPage (+7 more)

### Community 731 - "Services — Schedule Password Change"
Cohesion: 0.07
Nodes (12): StringBuffer, StringBuilder, StringBuffer, StringBuilder, StringBuffer, StringBuilder, StringBuffer, StringBuilder (+4 more)

### Community 732 - "Services — SLPF"
Cohesion: 0.07
Nodes (9): Enumeration, bool, IEnumerator, Hashtable, Hashtable, Hashtable, Hashtable, Hashtable (+1 more)

### Community 733 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (6): Animation, Animations, Animator, awaitAll(), PluginService, resolveTargetOptions()

### Community 734 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (14): allowedAttribute(), _createClass(), _defineProperties(), _defineProperty(), getSpecialTransitionEndEvent(), _objectSpread(), NOTE: 1 DOM access here, NOTE: 1 DOM access here (+6 more)

### Community 735 - "ACMO Web — Portal"
Cohesion: 0.09
Nodes (33): addRangeToControlSelection(), alertOrLog(), assertNodeInSameDocument(), consoleLog(), createControlSelection(), createModule(), fail(), fragmentFromNodeChildren() (+25 more)

### Community 736 - "ACMO Web — Portal"
Cohesion: 0.10
Nodes (21): a(), aa(), B(), c(), D(), F(), g(), h() (+13 more)

### Community 737 - "ACMO Web — Portal"
Cohesion: 0.10
Nodes (5): h2cRenderContext(), CanvasRenderer(), hasEntries(), Renderer(), Support()

### Community 738 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (8): createSocketRun, Util, byte, DateTime, Exception, int, Object, String

### Community 739 - "Common — SLPF"
Cohesion: 0.08
Nodes (8): createSocketRun, Util, byte, DateTime, Exception, int, Object, String

### Community 740 - "Common — Enitity Objects"
Cohesion: 0.11
Nodes (21): APIMethods, APIRegisterMembers, AppSettings, APPURLDetails, APPURLDetails_temp, ChildServices, HttpExternalAPIRequestDetails, HttpRequestDetails (+13 more)

### Community 741 - "Services — Arcon File Upload"
Cohesion: 0.10
Nodes (11): ArconFileUpload, bool, DateTime, EventArgs, FileSystemProgressEventArgs, ForwardedPortLocal, int, PortForwardEventArgs (+3 more)

### Community 742 - "Services — Desk Insight"
Cohesion: 0.12
Nodes (12): ConnectionRequest, Boolean, EventArgs, String, Winsock, WinsockConnectedEventArgs, WinsockConnectionRequestEventArgs, WinsockDataArrivalEventArgs (+4 more)

### Community 743 - "Services — Schedule Password Change"
Cohesion: 0.08
Nodes (8): createSocketRun, Util, byte, DateTime, Exception, int, Object, String

### Community 744 - "Services — Schedule Password Change"
Cohesion: 0.08
Nodes (8): createSocketRun, Util, byte, DateTime, Exception, int, Object, String

### Community 745 - "Services — Staging Log Sync"
Cohesion: 0.07
Nodes (15): Sorter, FileInfo, ARCOSApp, ARCOSStagingLogSyncServiceONS, IContainer, Sorter, FileInfo, Program (+7 more)

### Community 746 - "Services — TSPlugin Service"
Cohesion: 0.08
Nodes (8): createSocketRun, Util, byte, DateTime, Exception, int, Object, String

### Community 747 - "ACM Client — Sshkey SFTP"
Cohesion: 0.11
Nodes (22): BROWSEINFO, FileIconManager, FolderType, IconSize, ITEMIDLIST, NativeMethodsShell32, NativeMethodsUser32, SHFILEINFO (+14 more)

### Community 748 - "ACM Client — DB2TTerminal"
Cohesion: 0.14
Nodes (14): DB2Launcher, FindChildWindow2, FindTopLevelWindow, GetWindowCmd, bool, CallBackPtr, DllImport, int (+6 more)

### Community 749 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (17): INPUT, MOUSEINPUT, HARDWAREINPUT, INPUT, KEYBDINPUT, MOUSEINPUT, SimulateMouseKeyboardEvents, byte (+9 more)

### Community 750 - "ACM Client — SSHTerminal"
Cohesion: 0.08
Nodes (15): Config, Dictionary, EventArgs, TreeViewEventArgs, AppearancePage, bool, BasePage, TerminalPage (+7 more)

### Community 751 - "ACM Client — SSHTerminal"
Cohesion: 0.14
Nodes (11): DllImport, Int32, IntPtr, string, uint, UInt16, ushort, WinApi (+3 more)

### Community 752 - "ACM Common — .PIMUD"
Cohesion: 0.12
Nodes (13): ConnectionRequest, bool, Boolean, int, string, TcpClient, Winsock, Desktop (+5 more)

### Community 753 - "ACM Common — .PIMUD"
Cohesion: 0.10
Nodes (14): Oracle, OracleDBConnection, Boolean, DataTable, int, OracleConnection, String, Oracle (+6 more)

### Community 754 - "ACM Common — .User Controls"
Cohesion: 0.09
Nodes (18): Popup, bool, CancelEventArgs, Control, CreateParams, EventArgs, int, Keys (+10 more)

### Community 755 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (10): SeviceClassification, string, frmServiceClassification, Boolean, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs (+2 more)

### Community 756 - "ACMO Web — Client Manager"
Cohesion: 0.06
Nodes (27): frmATSConfiguration, EventArgs, frmATSConfiguration, Button, Label, TextBox, UCResponseMessage, frmATSDashboard (+19 more)

### Community 757 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (15): AesMode, Algorithm, ElectronCryptor, HmacAlgorithm, Options, PayloadComponents, Pbkdf2Prf, Schema (+7 more)

### Community 758 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (32): applyStyles(), effect$2(), getBoundingClientRect(), getClientRectFromMixedType(), getClippingParents(), getCompositeRect(), getComputedStyle$1(), getContainingBlock() (+24 more)

### Community 759 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (6): BaseComponent, Config, enableDismissTrigger(), getElement(), isElement(), toType()

### Community 760 - "ACMO Web — Client Manager"
Cohesion: 0.23
Nodes (28): bt(), ce(), k(), me(), Te(), a(), b(), c() (+20 more)

### Community 761 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (17): Popup, bool, CancelEventArgs, Control, CreateParams, EventArgs, int, Keys (+9 more)

### Community 762 - "Services — Desk Insight"
Cohesion: 0.11
Nodes (11): frmARCONRSSMain, Boolean, EventArgs, FormClosingEventArgs, Int32, MessageReceivedArgs, NetworkTool, Node (+3 more)

### Community 763 - "Services — TSPlugin Service"
Cohesion: 0.09
Nodes (19): WinAPI, DllImport, Int32, IntPtr, Process, StringBuilder, frmMain, ColumnHeader (+11 more)

### Community 764 - "ACM Client — RStream Client"
Cohesion: 0.11
Nodes (13): ConnectionRequest, bool, Boolean, int, string, TcpClient, Winsock, LogOn (+5 more)

### Community 765 - "ACM Client — DB2TTerminal"
Cohesion: 0.14
Nodes (10): ApplicationControl, bool, Boolean, CaptureProcess, DllImport, EventArgs, int, IntPtr (+2 more)

### Community 766 - "ACM Client — DQS"
Cohesion: 0.09
Nodes (20): bool, Boolean, EventArgs, int, Message, string, frmCriticalWithApproval, ARCOSCRITICALWFM (+12 more)

### Community 767 - "ACM Client — Framework CM"
Cohesion: 0.10
Nodes (19): AccessControlParam, AppSettings_temp, APPURLDetails_temp, HostFileManagerClientMessage, HostFileManagerServerResponse, ImageBasedJSONResponse_temp, RDPSServerdetails_Temp, RestrictedCriticalCmdResponse (+11 more)

### Community 768 - "Services — Auto Healing"
Cohesion: 0.12
Nodes (13): CloudConnectionData, int, List, string, HSMCommonFunctionSPC, DataTable, List, HSMDataFunctionsSPC (+5 more)

### Community 769 - "ACMO Web — Client Manager"
Cohesion: 0.16
Nodes (7): frmUARDetails, Boolean, DataTable, EventArgs, GridViewPageEventArgs, Int32, String

### Community 770 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (4): Carousel, getNextActiveElement(), isRTL(), isVisible()

### Community 771 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (23): beforeLayout(), bs(), ct(), eo(), f(), g(), ge(), Go() (+15 more)

### Community 772 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (10): aa(), Bn(), _calculateBarValuePixels(), getBasePixel(), getLabelAndValue(), getLabelForValue(), jn(), update() (+2 more)

### Community 773 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (25): CheckBoxHeaderCell, CheckBoxState, DataGridViewAdvancedBorderStyle, DataGridViewCellMouseEventArgs, DataGridViewCellStyle, DataGridViewElementStates, DataGridViewPaintParts, Graphics (+17 more)

### Community 774 - "ASM Server — Server Manager"
Cohesion: 0.06
Nodes (28): frmPasswordManagerV2, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DateTimePicker (+20 more)

### Community 775 - "Common — SLPF"
Cohesion: 0.11
Nodes (25): BarrettReduction(), bitCount(), clearBit(), Compare(), BigInteger, RandomNumberGenerator, Difference(), EvenPow() (+17 more)

### Community 776 - "Services — PAM Agents"
Cohesion: 0.12
Nodes (8): IPMACManager, IEnumerable, String, ApiResponse, Port, ReportLogger, RetryManager, string

### Community 777 - "Services — Arcon Auto Failover"
Cohesion: 0.15
Nodes (16): CommonFunctionsDB, Boolean, CommandType, DataSet, DataTable, SqlConnection, SqlParameter, String (+8 more)

### Community 778 - "Services — Arcon File Upload"
Cohesion: 0.07
Nodes (17): ArconFileUpload, IContainer, Label, PictureBox, FileUpload, IContainer, Label, PictureBox (+9 more)

### Community 779 - "Services — Desk Insight"
Cohesion: 0.13
Nodes (15): GDI32, RECT, ScreenCapture, User32, WINDOWINFO, Bitmap, DllImport, Image (+7 more)

### Community 780 - "Services — Perf Mon IT"
Cohesion: 0.07
Nodes (16): ARCOSApp, ARCOSPerfMonITService, IContainer, ARCOSPerfMonITSettings, Boolean, DateTime, Int32, Program (+8 more)

### Community 781 - "Services — Provisioning Service"
Cohesion: 0.09
Nodes (19): Dictionary, Func, ILog, List, AssignPriority, int, object, Rule (+11 more)

### Community 782 - "Offline MultiTab — Offline API"
Cohesion: 0.22
Nodes (8): RequestResponseNewApi, AllowAnonymous, DateTime, HttpPost, ILogger, List, Route, ServiceDetailsController

### Community 783 - "ACM Client — Framework CM"
Cohesion: 0.14
Nodes (14): GDI32, RECT, SizeConstants, StreamAgent, User32, Bitmap, Boolean, DllImport (+6 more)

### Community 784 - "ACM Client — VNCTerminal"
Cohesion: 0.10
Nodes (10): frmARCOSVNCTerminal, Bitmap, byte, CancelEventArgs, EventArgs, FormClosingEventArgs, Message, PaintEventArgs (+2 more)

### Community 785 - "ACM Common — .API"
Cohesion: 0.10
Nodes (15): CommonAPIFunctions, DataTable, HttpWebRequest, List, HttpRequestDetails, APIMethods, APIRegisterMembers, AppSettings (+7 more)

### Community 786 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (10): ARCONSMobileOTP, Boolean, Int32, String, UCMobileOTPValidator, EventArgs, Int64, UCUDFSRMobileOTP (+2 more)

### Community 787 - "ACM Common — SLPF"
Cohesion: 0.12
Nodes (24): BarrettReduction(), bitCount(), clearBit(), Compare(), BigInteger, RandomNumberGenerator, Difference(), EvenPow() (+16 more)

### Community 788 - "ACM Common — Enitity Objects"
Cohesion: 0.07
Nodes (25): ServerGroup, DateTime, Int32, List, string, UserGroup, DateTime, Int32 (+17 more)

### Community 789 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (29): frmConnection, Button, CheckBox, CheckBoxList, DropDownList, FileUpload, GridView, HiddenField (+21 more)

### Community 790 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (4): Nt, bt(), ft(), $t()

### Community 791 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (6): CategoryScale, changeExponent(), getStartAndCountOfVisiblePointsSimplified(), getUserBounds(), LinearScale, LogarithmicScale

### Community 792 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (29): addFormatToken(), addWeekYearFormatToken(), create__createDuration(), duration_humanize__relativeTime(), expandFormat(), format(), formatMoment(), from() (+21 more)

### Community 793 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (25): A(), b(), c(), D(), e(), i(), l(), n() (+17 more)

### Community 794 - "ACMO Web — Portal"
Cohesion: 0.14
Nodes (30): clone(), cloneWithOffset(), create__createDuration(), diff(), duration_get__get(), endOf(), from(), fromNow() (+22 more)

### Community 795 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (24): BarrettReduction(), bitCount(), clearBit(), BigInteger, RandomNumberGenerator, Difference(), EvenPow(), gcd() (+16 more)

### Community 796 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (17): DailySchedule, IntervalSchedule, MonthlySchedule, OneTimeSchedule, Schedule, SchedulerEventType, ScheduleType, SelectedWeekSchedule (+9 more)

### Community 797 - "Services — Alert Service"
Cohesion: 0.08
Nodes (21): EmailAddress, EmailMessage, EmailResponse, EmailSender, IgnoreAdditionalDataContractResolver, ItemBody, DateTimeOffset, JsonProperty (+13 more)

### Community 798 - "Services — PAM Agents"
Cohesion: 0.08
Nodes (12): Listener, IContainer, ProjectInstaller, EventLog, EventLogEntryType, IDictionary, String, ProjectInstaller (+4 more)

### Community 799 - "Services — TSPlugin Service"
Cohesion: 0.07
Nodes (15): ARCOSTSPlugin, IContainer, Program, ProjectInstaller, InstallEventArgs, ProjectInstaller, IContainer, ServiceInstaller (+7 more)

### Community 800 - "Services — Desk Insight"
Cohesion: 0.08
Nodes (28): uint, ushort, Dot11AuthAlgorithm, Dot11BssType, Dot11CipherAlgorithm, Dot11OperationMode, Dot11PhyType, Dot11RadioState (+20 more)

### Community 801 - "Services — Desk Insight"
Cohesion: 0.10
Nodes (10): frmMain, EventArgs, string, WinsockConnectedEventArgs, WinsockConnectionRequestEventArgs, WinsockDataArrivalEventArgs, WinsockErrorReceivedEventArgs, WinsockReceiveProgressEventArgs (+2 more)

### Community 802 - "Services — Log Manager Service"
Cohesion: 0.15
Nodes (12): ARCOSLogManagerServiceONS, Bitmap, Boolean, DataTable, EventArgs, int, Int32, Size (+4 more)

### Community 803 - "Services — Password Change Vault"
Cohesion: 0.10
Nodes (17): GenericSchedulerSettingFunctions, bool, ILog, List, string, UsageAnalysis, bool, DllImport (+9 more)

### Community 804 - "Services — Provisioning Service"
Cohesion: 0.09
Nodes (15): CpuUsage, DllImport, ILog, MarshalAs, UsageDetail, Service1, ElapsedEventArgs, ILog (+7 more)

### Community 805 - "Services — Schedule Password Change"
Cohesion: 0.12
Nodes (24): BarrettReduction(), bitCount(), clearBit(), BigInteger, RandomNumberGenerator, Difference(), EvenPow(), gcd() (+16 more)

### Community 806 - "Offline MultiTab — Offline API"
Cohesion: 0.11
Nodes (18): LogsBLL, ILog, List, LogsDAL, ILog, List, CommandsessionLog, ServiceLog (+10 more)

### Community 807 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.16
Nodes (14): GDIStuff, DllImport, int, IntPtr, CaptureScreen, RECT, SIZE, Bitmap (+6 more)

### Community 808 - "Services — Desk Insight"
Cohesion: 0.12
Nodes (12): bool, Color, Container, EventArgs, Graphics, GraphicsPath, int, PaintEventArgs (+4 more)

### Community 809 - "ACM Client — RStream Client"
Cohesion: 0.13
Nodes (11): bool, DllImport, EventArgs, int, IntPtr, Message, ScrollEventType, uint (+3 more)

### Community 810 - "ACM Client — Framework CM"
Cohesion: 0.09
Nodes (14): frmARCOSVPNClientV4, ARCOSVPNDetails, bool, Boolean, EventArgs, ForwardedPortLocal, ILog, int (+6 more)

### Community 811 - "ACM Client — SFTPTeminal"
Cohesion: 0.11
Nodes (7): bool, Dictionary, EventArgs, TransferConfirmEventArgs, FileOperation, TransferConfirmEventArgs, TransferConfirmEventArgs

### Community 812 - "ACM Client — SSHTerminal"
Cohesion: 0.14
Nodes (14): bool, Brush, EventArgs, Graphics, Image, int, MouseEventArgs, PaintEventArgs (+6 more)

### Community 813 - "ACM Client — Web Browser"
Cohesion: 0.08
Nodes (16): NotifyCollection, EventArgs, ScriptError, int, string, Uri, ScriptErrorManager, object (+8 more)

### Community 814 - "ACM Common — Tab Strip"
Cohesion: 0.09
Nodes (13): BaseStyledPanel, EventArgs, ToolStripProfessionalRenderer, BaseStyledPanel, EventArgs, ToolStripProfessionalRenderer, BaseStyledPanel, EventArgs (+5 more)

### Community 815 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (15): frmAddApplication_PEDM, DataTable, EventArgs, string, WebMethod, frmApplicationInventory, DataTable, EventArgs (+7 more)

### Community 816 - "ACMO Web — Client Manager"
Cohesion: 0.19
Nodes (24): U, A(), b(), C(), d(), E(), f(), g() (+16 more)

### Community 817 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (7): CaptionSettingsMenuItem(), CloseButton(), FullscreenToggle(), MuteToggle(), PlayToggle(), SubsCapsButton(), SubsCapsMenuItem()

### Community 818 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (10): ao(), Bi(), Ci(), co(), cs, Do(), Fi(), inXRange() (+2 more)

### Community 819 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (29): allocUnsafe(), arrayIndexOf(), asciiWrite(), assertSize(), base64ToBytes(), base64Write(), bidirectionalIndexOf(), blitBuffer() (+21 more)

### Community 820 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (29): addRegexToken(), clone(), cloneWithOffset(), diff(), duration_get__get(), endOf(), getSet(), getSetDayOfYear() (+21 more)

### Community 821 - "ACMO Web — Client Manager"
Cohesion: 0.07
Nodes (14): Service, ValidateARCOSUserCompletedEventArgs, bool, object, SendOrPostCallback, SoapDocumentMethodAttribute, XmlElementAttribute, Service (+6 more)

### Community 822 - "LDAPAuthenticator"
Cohesion: 0.11
Nodes (10): int, IPEndPoint, string, uint, RadiusClient, byte, List, ushort (+2 more)

### Community 823 - "ACMO Web — Portal"
Cohesion: 0.11
Nodes (8): CustomHeaderModule, Global, Global_asax, EventArgs, Page, Queue, HttpApplication, IHttpModule

### Community 824 - "ACMO Web — User Access"
Cohesion: 0.07
Nodes (18): _Default, HtmlForm, LinkButton, Repeater, DefaultV2, HtmlForm, DefaultV2GetVideo, HtmlForm (+10 more)

### Community 825 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (14): DgvFilterManager, BindingSource, bool, DataGridView, DataGridViewCellMouseEventArgs, DataGridViewCellPaintingEventArgs, DataGridViewColumn, DataGridViewColumnEventArgs (+6 more)

### Community 826 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (26): frmConfigureDefaults, BackgroundWorker, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView (+18 more)

### Community 827 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (9): frmServiceDiscovery_Popup, ArrayList, Boolean, EventArgs, FormClosedEventArgs, FormClosingEventArgs, ListView, ListViewItem (+1 more)

### Community 828 - "ASM Server — Pkcs11Interop"
Cohesion: 0.07
Nodes (21): bool, CkSsl3RandomData, bool, IntPtr, NativeULong, CK_SSL3_KEY_MAT_PARAMS, IntPtr, CK_SSL3_MASTER_KEY_DERIVE_PARAMS (+13 more)

### Community 829 - "ASM Server — Pkcs11Interop"
Cohesion: 0.07
Nodes (21): bool, CkSsl3RandomData, bool, IntPtr, NativeULong, CK_SSL3_KEY_MAT_PARAMS, IntPtr, CK_SSL3_MASTER_KEY_DERIVE_PARAMS (+13 more)

### Community 830 - "ASM Server — Pkcs11Interop"
Cohesion: 0.07
Nodes (21): bool, CkSsl3RandomData, bool, IntPtr, NativeULong, CK_SSL3_KEY_MAT_PARAMS, IntPtr, CK_SSL3_MASTER_KEY_DERIVE_PARAMS (+13 more)

### Community 831 - "ASM Server — Pkcs11Interop"
Cohesion: 0.07
Nodes (21): bool, CkSsl3RandomData, bool, IntPtr, NativeULong, CK_SSL3_KEY_MAT_PARAMS, IntPtr, CK_SSL3_MASTER_KEY_DERIVE_PARAMS (+13 more)

### Community 832 - "Common — .User Controls"
Cohesion: 0.10
Nodes (14): DgvFilterManager, BindingSource, bool, DataGridView, DataGridViewCellMouseEventArgs, DataGridViewCellPaintingEventArgs, DataGridViewColumn, DataGridViewColumnEventArgs (+6 more)

### Community 833 - "Common — Enitity Objects"
Cohesion: 0.07
Nodes (16): DailySchedule, IntervalSchedule, MonthlySchedule, OneTimeSchedule, Schedule, SchedulerEventType, ScheduleType, SelectedWeekSchedule (+8 more)

### Community 834 - "Services — PAM Agents"
Cohesion: 0.11
Nodes (9): List, AccessRightsProvider, AccessControlType, FileSystemRights, string, AccessRightsProviderFolder, Program, RemoveAllFolder (+1 more)

### Community 835 - "Services — DBSync Service"
Cohesion: 0.10
Nodes (13): frmMain, ARCOSDBSyncServiceSetting, Boolean, EventArgs, String, frmMain, Button, CheckBox (+5 more)

### Community 836 - "Services — DBSync Service"
Cohesion: 0.24
Nodes (7): Boolean, EventLogEntryType, ARCOSDBSyncService, Boolean, EventArgs, String, Timer

### Community 837 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (11): bool, EventArgs, EventArrivedEventArgs, string, Timer, MyHandler, Program, IList (+3 more)

### Community 838 - "Services — Perf Mon IT"
Cohesion: 0.15
Nodes (9): CommonFunctionsPerMon, Boolean, CommandType, DataColumnCollection, DateTime, EventLog, SqlConnection, SqlParameter (+1 more)

### Community 839 - "Services — TSPlugin Service"
Cohesion: 0.10
Nodes (14): DgvFilterManager, BindingSource, bool, DataGridView, DataGridViewCellMouseEventArgs, DataGridViewCellPaintingEventArgs, DataGridViewColumn, DataGridViewColumnEventArgs (+6 more)

### Community 840 - "Services — TSPlugin Service"
Cohesion: 0.07
Nodes (16): DailySchedule, IntervalSchedule, MonthlySchedule, OneTimeSchedule, Schedule, SchedulerEventType, ScheduleType, SelectedWeekSchedule (+8 more)

### Community 841 - "MultiTab — src"
Cohesion: 0.13
Nodes (3): JsonProperty, Override, ViewPassword

### Community 842 - "Offline MultiTab — Offline API"
Cohesion: 0.10
Nodes (14): CommandBLL, ILog, List, LogSecurity, String, CommandDAL, ILog, List (+6 more)

### Community 843 - "Offline MultiTab — Service Installer"
Cohesion: 0.13
Nodes (10): Exception, String, ExceptionLogging, String, Form1, dynamic, IDictionary, InstallEventArgs (+2 more)

### Community 844 - "Offline MultiTab — Windows Service"
Cohesion: 0.09
Nodes (22): HttpContent, SslPolicyErrors, Stream, X509Certificate, X509Chain, APIHelper, bool, byte (+14 more)

### Community 845 - "ACM Client — ACMCommon Functions"
Cohesion: 0.13
Nodes (11): Apartment, TestsCF, Boolean, DataTable, int, SetUp, string, Test (+3 more)

### Community 846 - "ACM Client — RStream Client"
Cohesion: 0.06
Nodes (16): frmSelectResolution, Button, GroupBox, IContainer, RadioButton, LogOn, IContainer, Label (+8 more)

### Community 847 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.14
Nodes (6): bool, EventArgs, KeyEventArgs, Message, string, SetPermissionsDialog

### Community 848 - "ACM Client — DQS"
Cohesion: 0.14
Nodes (6): EditManager, ContextMenu, ContextMenuStrip, Control, EventArgs, ToolStripMenuItem

### Community 849 - "ACM Client — Script Manager"
Cohesion: 0.14
Nodes (14): DataTableCollection, frmCommandLogTextViewer_ScriptManager, LogNavigator, DataTable, DataTableCollection, EventArgs, int, ListView (+6 more)

### Community 850 - "ACM Client — Framework CM"
Cohesion: 0.07
Nodes (21): GradiantArea, ImageLayoutType, ProgressBarEx, ProgressDir, Bitmap, bool, Color, EventArgs (+13 more)

### Community 851 - "ACM Client — Framework CM"
Cohesion: 0.11
Nodes (13): frmSplashScreen, Boolean, Color, DllImport, EventArgs, FormClosingEventArgs, Graphics, GraphicsPath (+5 more)

### Community 852 - "ACM Client — Script Manager"
Cohesion: 0.07
Nodes (25): frmScriptScheduler, Button, CheckBox, CheckBoxComboBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView (+17 more)

### Community 853 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (22): Resources, Bitmap, CultureInfo, ResourceManager, frmHSMConfig, Button, ColumnHeader, GroupBox (+14 more)

### Community 854 - "ACM Common — SLPF"
Cohesion: 0.09
Nodes (7): ArrayList, AttrListImpl, ArrayList, AttrListImpl, ArrayList, AttrListImpl, IMutableAttrList

### Community 855 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (6): DateTime, SftpATTRS, int, long, String, uint

### Community 856 - "ACM Common — Enitity Objects"
Cohesion: 0.10
Nodes (16): WindowsDCOM, Boolean, DateTime, int, String, WindowsServices, Boolean, DateTime (+8 more)

### Community 857 - "ACM Common — Server Common"
Cohesion: 0.08
Nodes (17): frmDatabaseConnectionPleaseWait, IContainer, Label, frmMSSQLConnectionRetry, Boolean, EventArgs, Exception, SqlConnection (+9 more)

### Community 858 - "ACMO Web — APIRA"
Cohesion: 0.09
Nodes (4): AppInsights(), Initialization(), PageViewManager(), PageViewPerformance()

### Community 859 - "ACMO Web — Common Functions"
Cohesion: 0.12
Nodes (17): frmNetworkChart, DataTable, Dictionary, EventArgs, List, WebMethod, string, DataRecords (+9 more)

### Community 860 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (4): ot, lt, it(), st()

### Community 862 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (9): ao(), bo, co(), Do(), inXRange(), inYRange(), Oe(), ro() (+1 more)

### Community 863 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (28): _arrayLikeToArray(), CFFDict(), clearSubstitutionFlags(), CmapProcessor(), consonantPosition(), _createForOfIteratorHelper(), _createForOfIteratorHelperLoose(), DFont() (+20 more)

### Community 864 - "Services — Alert Service"
Cohesion: 0.14
Nodes (11): UDEKStorage, DateTime, HSMCommonFunctionAlert, DataTable, List, HSMDataFunctionsAlert, DataTable, Hashtable (+3 more)

### Community 865 - "Common — Enitity Objects"
Cohesion: 0.16
Nodes (27): ARCOSLogs, ARCOSServiceLogs, ManageServicePassword, RDPSessionCheck, ServiceReferenceLogParams, UserAndServerRequestLogsParams, ViewARCOSLogParams, ViewDBALogParams (+19 more)

### Community 866 - "Services — PAM Agents"
Cohesion: 0.16
Nodes (18): PROCESS_INFORMATION, ProcessExtensions, SECURITY_IMPERSONATION_LEVEL, STARTUPINFO, SW, TOKEN_TYPE, WTS_CONNECTSTATE_CLASS, WTS_SESSION_INFO (+10 more)

### Community 867 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (13): CapturingScreenImage, Bitmap, PlatformInvokeGDI32, DllImport, int, IntPtr, PlatformInvokeUSER32, SIZE (+5 more)

### Community 868 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (10): DebuggerStepThrough, DllImport, Guid, IntPtr, UInt32, WlanAccess, WlanIntfOpcode, WlanOpcodeValueType (+2 more)

### Community 869 - "Services — Desk Insight"
Cohesion: 0.08
Nodes (17): CustomFormState, MinMaxButton, Color, EventArgs, int, MouseEventArgs, PaintEventArgs, String (+9 more)

### Community 870 - "Services — Z POC"
Cohesion: 0.10
Nodes (13): string, OracleDB, SyncPassword, Program, EventArgs, Button, IContainer, Label (+5 more)

### Community 871 - "Offline MultiTab — Offline API"
Cohesion: 0.08
Nodes (18): ConcurrentDictionary, APP_Common.Appenders, EventId, ILogger, ILoggerProvider, ILoggerRepository, LogLevel, Configuration (+10 more)

### Community 872 - "ACM Client — App Exe"
Cohesion: 0.16
Nodes (11): ARCONRPAProcess, objectdata, Bitmap, DllImport, IList, Image, int, IntPtr (+3 more)

### Community 873 - "ACM Client — DQS"
Cohesion: 0.10
Nodes (12): DialogResult, QueryOptionsForm, Button, IContainer, Label, NumericUpDown, TabControl, TabPage (+4 more)

### Community 874 - "ACM Client — Framework CM"
Cohesion: 0.17
Nodes (12): HARDWAREINPUT, KEYBDINPUT, MOUSEINPUT, SimulateMouseKeyboardEvents, byte, DllImport, int, IntPtr (+4 more)

### Community 875 - "ACM Client — SSHTerminal"
Cohesion: 0.09
Nodes (18): Color, ColorUtil, ArrayList, Brush, Button, Container, EventArgs, Font (+10 more)

### Community 876 - "ACM Client — SSHTerminal"
Cohesion: 0.09
Nodes (13): bool, Button, Container, EventArgs, Label, TextBox, EditEnvVariable, Button (+5 more)

### Community 877 - "ACM Client — SSHTerminal"
Cohesion: 0.07
Nodes (17): Login, Button, ComboBox, IContainer, Label, TabControl, TabPage, TextBox (+9 more)

### Community 878 - "ACM Client — Web Browser"
Cohesion: 0.09
Nodes (13): ExtendedWebBrowser, WindowsMessages, Boolean, EventArgs, Message, frmPageControls, EventArgs, ConnectionPointCookie (+5 more)

### Community 879 - "ACM Common — .User Controls"
Cohesion: 0.15
Nodes (10): ScrollablePanel, bool, DllImport, EventArgs, int, IntPtr, Message, ScrollEventType (+2 more)

### Community 880 - "ACM Common — SLPF"
Cohesion: 0.10
Nodes (13): BigInteger, NextPrimeFinder, BigInteger, SequentialSearchPrimeGeneratorBase, BigInteger, NextPrimeFinder, BigInteger, NextPrimeFinder (+5 more)

### Community 881 - "ACM Common — SLPF"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 882 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (3): Alert, Modal, remove()

### Community 884 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (6): Backdrop, execute(), executeAfterTransition(), getTransitionDurationFromElement(), Swipe, triggerTransitionEnd()

### Community 885 - "ACMO Web — Client Manager"
Cohesion: 0.19
Nodes (25): convert_date(), FillSiteName(), GetFilter(), HideChart(), loadBarDoc(), loadDoc(), onFail(), onLobChange() (+17 more)

### Community 887 - "ACMO Web — Portal"
Cohesion: 0.49
Nodes (26): a(), b(), c(), d(), e(), f(), g(), h() (+18 more)

### Community 888 - "ACMO Web — Portal"
Cohesion: 0.09
Nodes (14): h(), d(), i(), r(), t(), v(), a(), n() (+6 more)

### Community 889 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (11): ARCONCoolProgressBar, bool, Color, Container, EventArgs, Graphics, GraphicsPath, int (+3 more)

### Community 890 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): ScrollablePanel, bool, DllImport, EventArgs, int, IntPtr, Message, ScrollEventType (+2 more)

### Community 891 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 892 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (24): frmConfigureDefaults, BackgroundWorker, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker (+16 more)

### Community 893 - "ASM Server — Server Manager"
Cohesion: 0.07
Nodes (25): frmLogModule, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker, GroupBox (+17 more)

### Community 894 - "Common — .User Controls"
Cohesion: 0.13
Nodes (11): ARCONCoolProgressBar, bool, Color, Container, EventArgs, Graphics, GraphicsPath, int (+3 more)

### Community 895 - "Common — .User Controls"
Cohesion: 0.15
Nodes (10): ScrollablePanel, bool, DllImport, EventArgs, int, IntPtr, Message, ScrollEventType (+2 more)

### Community 896 - "Common — SLPF"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 897 - "Services — PAM Agents"
Cohesion: 0.17
Nodes (16): PROCESS_INFORMATION, ProcessExtensions, SECURITY_IMPERSONATION_LEVEL, STARTUPINFO, SW, TOKEN_TYPE, WTS_CONNECTSTATE_CLASS, WTS_SESSION_INFO (+8 more)

### Community 898 - "Services — PAM Agents"
Cohesion: 0.15
Nodes (16): PROCESS_INFORMATION, STARTUPINFO, CreateProcessAsSystemWrapper, PROCESS_INFORMATION, SECURITY_ATTRIBUTES, SECURITY_IMPERSONATION_LEVEL, STARTUPINFO, TOKEN_TYPE (+8 more)

### Community 899 - "Services — PAM Agents"
Cohesion: 0.13
Nodes (13): ClientMessage, HostManager, ServerResponse, TrackingData, DateTime, Dictionary, HashSet, object (+5 more)

### Community 900 - "Services — Arcon File Upload"
Cohesion: 0.13
Nodes (11): ARCONCoolProgressBar, bool, Color, Container, EventArgs, Graphics, GraphicsPath, int (+3 more)

### Community 901 - "Services — Desk Insight"
Cohesion: 0.13
Nodes (14): frmFRApp, bool, DllImport, EventArgs, FilterInfoCollection, FormClosingEventArgs, int, IntPtr (+6 more)

### Community 902 - "Services — Folder Sync Service"
Cohesion: 0.15
Nodes (6): frmMain, bool, EventArgs, FormClosingEventArgs, MouseEventArgs, NotifyIcon

### Community 903 - "Services — Migrate Data Utility"
Cohesion: 0.13
Nodes (11): ARCONCoolProgressBar, bool, Color, Container, EventArgs, Graphics, GraphicsPath, int (+3 more)

### Community 904 - "Services — Schedule Password Change"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 905 - "Services — Schedule Password Change"
Cohesion: 0.14
Nodes (9): Exception, SSHKeyCommon, Boolean, DataSet, DataTable, Hashtable, Int32, SqlConnection (+1 more)

### Community 906 - "Services — Schedule Password Change"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 907 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (11): ARCONCoolProgressBar, bool, Color, Container, EventArgs, Graphics, GraphicsPath, int (+3 more)

### Community 908 - "Services — TSPlugin Service"
Cohesion: 0.15
Nodes (10): ScrollablePanel, bool, DllImport, EventArgs, int, IntPtr, Message, ScrollEventType (+2 more)

### Community 909 - "Services — TSPlugin Service"
Cohesion: 0.18
Nodes (13): SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet, Hashtable, SqlCommand, SqlConnection (+5 more)

### Community 910 - "Services — TSPlugin Service"
Cohesion: 0.17
Nodes (5): bool, byte, uint, ulong, RIPEMD160Managed

### Community 911 - "Services — User On Boarding"
Cohesion: 0.09
Nodes (10): ARCOSUserOnBoardingService, IContainer, ARCOSAlertServiceSettings, DateTime, Int32, String, UserServerOnboardingLogs, ARCOSUserOnBoardingService.LocalCommonFunctions (+2 more)

### Community 912 - "Offline MultiTab — Offline API"
Cohesion: 0.12
Nodes (15): UserDetailsBLL, ILog, KeyValuePair, List, UserDetailsDAL, ILog, KeyValuePair, List (+7 more)

### Community 913 - "ACM Client — Sshkey SFTP"
Cohesion: 0.13
Nodes (6): FileOperation, bool, Dictionary, EventArgs, TransferConfirmEventArgs, TransferConfirmEventArgs

### Community 914 - "ACM Client — Framework CM"
Cohesion: 0.08
Nodes (12): int, List, Queue, SetUp, Thread, DummySSHChannel, ScheduledEvent, ScheduledEventType (+4 more)

### Community 915 - "ACM Client — Framework CM"
Cohesion: 0.10
Nodes (10): AuthenticationResult, ISSHChannelEventReceiver, SSHConnectionInfo, DummySSHConnection, AuthenticationResult, ISSHChannelEventReceiver, SSHConnectionInfo, DummySSHConnection (+2 more)

### Community 916 - "ACM Client — Framework CM"
Cohesion: 0.16
Nodes (11): GDI32, RECT, ScreenCapture, User32, Bitmap, DllImport, Image, ImageFormat (+3 more)

### Community 919 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (4): addElements(), removeBox(), sn, stop()

### Community 920 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (4): addElements(), removeBox(), sn, stop()

### Community 921 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (10): MouseEventDataXButtons, MouseEventFlags, TernaryRasterOperations, WindowsApi, CURSORINFO, DllImport, ICONINFO, IntPtr (+2 more)

### Community 922 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (23): frmPasswordManager, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, FlowLayoutPanel, GroupBox (+15 more)

### Community 923 - "ASM Server — Pkcs11Interop"
Cohesion: 0.09
Nodes (25): NativeULong, TokenFlags, DateTime, NativeULong, string, TokenInfo, NativeULong, TokenFlags (+17 more)

### Community 924 - "Common — SLPF"
Cohesion: 0.11
Nodes (5): SftpATTRS, int, long, String, uint

### Community 925 - "Common — Data Access"
Cohesion: 0.20
Nodes (12): SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet, Hashtable, SqlCommand, SqlConnection (+4 more)

### Community 926 - "Services — ADScanner Service"
Cohesion: 0.19
Nodes (12): SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet, Hashtable, SqlCommand, SqlConnection (+4 more)

### Community 927 - "Services — PAM Agents"
Cohesion: 0.17
Nodes (16): PROCESS_INFORMATION, ProcessExtensions, SECURITY_IMPERSONATION_LEVEL, STARTUPINFO, SW, TOKEN_TYPE, WTS_CONNECTSTATE_CLASS, DllImport (+8 more)

### Community 928 - "Services — Arcon Auto Failover"
Cohesion: 0.21
Nodes (12): SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet, Hashtable, SqlCommand, SqlConnection (+4 more)

### Community 929 - "Services — DBSync Service"
Cohesion: 0.17
Nodes (7): DBSyncCommonFunctions, DataTable, EventLog, Int32, Object, SqlConnection, String

### Community 930 - "Services — Schedule Password Change"
Cohesion: 0.11
Nodes (5): SftpATTRS, int, long, String, uint

### Community 931 - "Services — Schedule Password Change"
Cohesion: 0.11
Nodes (5): SftpATTRS, int, long, String, uint

### Community 932 - "Services — Staging Log Sync"
Cohesion: 0.16
Nodes (10): CommonFunctions, Boolean, Byte, DateTime, EventLog, EventLogEntryType, Int32, Int64 (+2 more)

### Community 933 - "Services — TSPlugin Service"
Cohesion: 0.11
Nodes (5): SftpATTRS, int, long, String, uint

### Community 934 - "LDAPAuthenticator"
Cohesion: 0.16
Nodes (12): PAMADAuthenticatorController, HttpPost, LdapConnection, X509Certificate, string, TextWriter, LogWriter, verifySettings (+4 more)

### Community 935 - "Onboarding — SQLHelper"
Cohesion: 0.21
Nodes (12): SqlConnectionOwnership, SqlHelper, SqlHelperParameterCache, CommandType, DataSet, Hashtable, SqlCommand, SqlConnection (+4 more)

### Community 936 - "Offline MultiTab — Windows Service"
Cohesion: 0.28
Nodes (3): Exception, APIOutputForMultiTab, OfflineSync

### Community 937 - "ACM Client — Sshkey SFTP"
Cohesion: 0.09
Nodes (16): RichTextBoxTraceListener, Color, RichTextBox, TraceEventCache, TraceEventType, Color, RichTextBox, TraceEventCache (+8 more)

### Community 938 - "ACM Client — Web Browser"
Cohesion: 0.14
Nodes (9): WindowManager, EventArgs, String, SuppressMessage, TabControl, TabPage, Uri, WebBrowserDocumentCompletedEventArgs (+1 more)

### Community 939 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmRestorePasswordManually, Boolean, EventArgs, Int32, String, frmUpdateSSHKeyManually, EventArgs, Int32 (+2 more)

### Community 940 - "ACMO Web — Client Manager"
Cohesion: 0.08
Nodes (24): MasterLogin, ContentPlaceHolder, HiddenField, HtmlForm, HtmlGenericControl, HtmlHead, HyperLink, Image (+16 more)

### Community 941 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (10): HelperTool, NameValuePair, SerializableHashtable, Bitmap, Image, ImageCodecInfo, IPAddress, object (+2 more)

### Community 942 - "ASM Server — Server Manager"
Cohesion: 0.19
Nodes (24): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+16 more)

### Community 943 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (22): frmBulkUpdatet, Button, CachedrptPasswordEnvelop, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView (+14 more)

### Community 944 - "Common — SLPF"
Cohesion: 0.19
Nodes (24): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+16 more)

### Community 945 - "Services — Sync Failed Password"
Cohesion: 0.08
Nodes (13): ARCOSApp, Boolean, Int32, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller (+5 more)

### Community 946 - "Services — Passworde Envelope Manager"
Cohesion: 0.14
Nodes (18): AllocMethod, AuthenticodeTools, RevocationCheckFlags, SignCheck, StateAction, TrustProviderFlags, UiChoice, UIContext (+10 more)

### Community 947 - "Services — Schedule Password Change"
Cohesion: 0.19
Nodes (24): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+16 more)

### Community 948 - "Services — Schedule Password Change"
Cohesion: 0.19
Nodes (24): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+16 more)

### Community 949 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (8): SSHKeyCommon, Boolean, DataSet, DataTable, Hashtable, Int32, SqlConnection, String

### Community 950 - "Services — TSPlugin Service"
Cohesion: 0.19
Nodes (24): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+16 more)

### Community 951 - "LDAPAuthenticator — .Radius"
Cohesion: 0.09
Nodes (13): RadiusAttribute, byte, string, RadiusAttribute, byte, string, RadiusAttribute, byte (+5 more)

### Community 952 - "Services — Schedule Password Change"
Cohesion: 0.17
Nodes (9): ConfidenceFactor, BigInteger, PrimalityTests, BigInteger, PrimalityTests, BigInteger, PrimalityTests, BigInteger (+1 more)

### Community 953 - "ACM Common — SLPF"
Cohesion: 0.20
Nodes (23): byte, int, IntPtr, long, short, string, CERT_EXTENSION, CERT_PUBLIC_KEY_INFO (+15 more)

### Community 954 - "ACMO Web — Provisioning Web"
Cohesion: 0.18
Nodes (9): IP_Pass_MessageHandler, VerifyRequest, CancellationToken, HttpRequestMessage, HttpResponseMessage, ILog, string, Task (+1 more)

### Community 955 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (3): contains(), effect$1(), Tab

### Community 957 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (3): Backdrop, execute(), Swipe

### Community 958 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (9): ca, ga(), ha(), io(), la(), no(), oo, tt() (+1 more)

### Community 959 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (9): allowedAttribute(), _createClass(), _defineProperties(), _defineProperty(), getSpecialTransitionEndEvent(), _objectSpread(), TODO: Remove in v5, sanitizeHtml() (+1 more)

### Community 960 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (13): ACMenuControl, HtmlAnchor, HtmlGenericControl, LogMenuControl, HtmlGenericControl, LinkButton, UCFooter, EventArgs (+5 more)

### Community 961 - "LDAPAuthenticator"
Cohesion: 0.09
Nodes (15): byte, int, TunnelMediumTypeAttribute, byte, int, TunnelTypeAttribute, byte, int (+7 more)

### Community 962 - "ACMO Web — Portal"
Cohesion: 0.13
Nodes (5): FastClick(), init(), init(), TODO: add extra shadow inside hole (with a mask) if the pie is tilted., TODO: perhaps do some mathmatical trickery here with the Y-coordinate to…

### Community 963 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (14): frmAddNewData, Button, GroupBox, IContainer, Label, TextBox, frmController, IContainer (+6 more)

### Community 964 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (3): Buffer, byte, int

### Community 965 - "ASM Server — Server Manager"
Cohesion: 0.08
Nodes (21): frmUserServiceGroup, Button, CachedrptPasswordEnvelop, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker (+13 more)

### Community 966 - "Common — SLPF"
Cohesion: 0.13
Nodes (3): Buffer, byte, int

### Community 967 - "Services — DBSync Service"
Cohesion: 0.16
Nodes (6): frmMain, Boolean, ComboBox, EventArgs, FormClosingEventArgs, String

### Community 968 - "Services — Folder Sync Service"
Cohesion: 0.12
Nodes (10): FolderSyncConfiguration, List, ListViewItem, string, XmlDocument, frmDetail, bool, EventArgs (+2 more)

### Community 969 - "Services — Log Manager Service"
Cohesion: 0.09
Nodes (11): ARCOSApp, ARCOSLogManagerService, IContainer, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller (+3 more)

### Community 970 - "Services — Migrate Data Utility"
Cohesion: 0.14
Nodes (12): int, List, string, CloudConnectionData, DataTable, EventArgs, List, string (+4 more)

### Community 971 - "Services — Migrate Data Utility"
Cohesion: 0.09
Nodes (16): Color, EventArgs, int, MouseEventArgs, PaintEventArgs, String, ButtonZ, IContainer (+8 more)

### Community 972 - "Services — Schedule Password Change"
Cohesion: 0.13
Nodes (3): Buffer, byte, int

### Community 973 - "Services — Schedule Password Change"
Cohesion: 0.13
Nodes (3): Buffer, byte, int

### Community 974 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (3): Buffer, byte, int

### Community 975 - "Services — Windows Vaulting Service"
Cohesion: 0.09
Nodes (23): background, service_worker, content_scripts, externally_connectable, matches, host_permissions, icons, 128 (+15 more)

### Community 976 - "Services — Z POC"
Cohesion: 0.11
Nodes (11): AWBPasswordAPI, AWBServiceDetails, bool, int, string, Program, T24PasswordChange, bool (+3 more)

### Community 977 - "LDAPAuthenticator"
Cohesion: 0.09
Nodes (13): FilterConfig, GlobalFilterCollection, RouteConfig, RouteCollection, WebApiConfig, HttpConfiguration, MvcApplication, readme (+5 more)

### Community 979 - "Offline MultiTab — Offline API"
Cohesion: 0.19
Nodes (12): UIAutomationBLL, ILog, List, UIAutomationDAL, ILog, List, UIAutomationData, HttpPost (+4 more)

### Community 980 - "ACM Client — Sshkey SFTP"
Cohesion: 0.09
Nodes (21): MainSTS, Button, ColumnHeader, ContextMenuStrip, IContainer, ImageList, Label, LinkLabel (+13 more)

### Community 981 - "ACM Client — DQS"
Cohesion: 0.11
Nodes (14): SqlQueryOptons, bool, DialogResult, IDbConnection, int, string, SqlQueryOptionsForm, Button (+6 more)

### Community 982 - "ACM Client — SFTPTeminal"
Cohesion: 0.15
Nodes (6): FileOperation, bool, Dictionary, EventArgs, Message, TransferConfirmEventArgs

### Community 983 - "ACM Client — SSHTerminal"
Cohesion: 0.12
Nodes (12): bool, Button, byte, Color, EventArgs, Message, MouseEventArgs, Object (+4 more)

### Community 984 - "ACM Client — SSHTerminal"
Cohesion: 0.09
Nodes (20): Button, ColumnHeader, ContextMenuStrip, IContainer, ImageList, Label, MenuStrip, ProgressBar (+12 more)

### Community 985 - "ACM Common — SLPF"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 986 - "ACM Common — Enitity Objects"
Cohesion: 0.15
Nodes (10): ExportLog, DataTable, Image, Int32, List, String, WordDocument, LogModule_NUnit (+2 more)

### Community 993 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (7): ce(), de, dt(), en, he(), j(), So

### Community 994 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (4): Ae(), Us(), Y(), Ys()

### Community 995 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (23): chooseLocale(), configFromObject(), createAdder(), defineLocale(), deprecate(), deprecateSimple(), Duration(), hasOwnProp() (+15 more)

### Community 996 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (16): frmEmailPage, EventArgs, frmEmailPage, Button, HtmlForm, Label, TextBox, frmModelDiv (+8 more)

### Community 997 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (10): ARCOSCaptchaImage, Bitmap, GraphicsPath, int, string, HttpContext, CryptoRandom, int (+2 more)

### Community 998 - "ACMO Web — Portal"
Cohesion: 0.15
Nodes (23): addTimeToArrayFromToken(), checkOverflow(), configFromArray(), configFromInput(), configFromISO(), configFromString(), configFromStringAndArray(), configFromStringAndFormat() (+15 more)

### Community 999 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (13): MessageReceivedArgs, NetworkTool, Node, bool, Hashtable, int, IPEndPoint, ISynchronizeInvoke (+5 more)

### Community 1000 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 1001 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (20): frmCommandLogTextViewer, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, Label, ListView (+12 more)

### Community 1002 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (10): frmWindowsUtility, Boolean, EventArgs, Int16, Int32, MouseEventArgs, string, WinsockDataArrivalEventArgs (+2 more)

### Community 1003 - "Common — SLPF"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 1004 - "Services — PAM Agents"
Cohesion: 0.09
Nodes (10): OperationContract, ARWHModel, bool, int, ArwhService, EventArgs, String, Program (+2 more)

### Community 1005 - "Services — Cloud File Uploader"
Cohesion: 0.11
Nodes (12): ArconCloudFileUploader, bool, EventArgs, ILog, List, string, Timer, S3UploadManager (+4 more)

### Community 1006 - "Services — DBSync Service"
Cohesion: 0.17
Nodes (11): ARCOSDBSyncServiceSetting, BaseObject, DatabaseConfig, DatabaseConfigType, Boolean, Double, Int32, String (+3 more)

### Community 1007 - "Services — DBSync Service"
Cohesion: 0.09
Nodes (10): ARCOSDBSyncService, IContainer, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller (+2 more)

### Community 1008 - "Services — Desk Insight"
Cohesion: 0.09
Nodes (11): Program, IContainer, ServiceInstaller, ServiceProcessInstaller, ProjectInstaller, ProjectInstaller, IContainer, Service1 (+3 more)

### Community 1009 - "Services — Provisioning Service"
Cohesion: 0.10
Nodes (10): Program, ProjectInstaller, IDictionary, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller, Service1 (+2 more)

### Community 1010 - "Services — Schedule Password Change"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 1011 - "Services — Schedule Password Change"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 1012 - "Services — TSPlugin Service"
Cohesion: 0.09
Nodes (22): AccountType, AlertNotificationMode, ARCOSAppType, ARCOSCPCSServerType, ARCOSFileStorageType, ARCOSLogType, ARCOSObjectTypes, ARCOSOnBoardingType (+14 more)

### Community 1013 - "Services — TSPlugin Service"
Cohesion: 0.10
Nodes (5): ProtectedConsoleStream, AsyncCallback, IAsyncResult, ObjRef, SeekOrigin

### Community 1014 - "ACM Client — RStream Client"
Cohesion: 0.13
Nodes (10): HelperTool, NameValuePair, SerializableHashtable, Bitmap, Byte, Image, ImageCodecInfo, object (+2 more)

### Community 1015 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.12
Nodes (14): POINT, COMPOSITIONFORM, MouseHook, HookProc, int, IntPtr, Point, MouseHookStruct (+6 more)

### Community 1016 - "ACM Client — Framework CM"
Cohesion: 0.14
Nodes (14): RECT, TernaryRasterOperations, WINDOWINFO, WindowScreenShot, Bitmap, DllImport, int, IntPtr (+6 more)

### Community 1017 - "ACM Client — VNCTerminal"
Cohesion: 0.12
Nodes (8): ZOutputStream, bool, Boolean, byte, int, Int32, Int64, SeekOrigin

### Community 1018 - "ACMO Web — APIOnline"
Cohesion: 0.19
Nodes (20): CompareValidatorEvaluateIsValid(), CustomValidatorEvaluateIsValid(), Page_ClientValidate(), RangeValidatorEvaluateIsValid(), RegularExpressionValidatorEvaluateIsValid(), RequiredFieldValidatorEvaluateIsValid(), ValidationSummaryOnSubmit(), ValidatorCompare() (+12 more)

### Community 1019 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): ACMO, ContentPlaceHolder, HiddenField, HtmlForm, HtmlHead, Image, Label, Panel (+13 more)

### Community 1020 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): ACMO_Onboarding, ContentPlaceHolder, DropDownList, HiddenField, HtmlForm, HtmlGenericControl, Image, Label (+13 more)

### Community 1021 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): frmUserOnboardingNew, Button, CheckBox, DropDownList, GridView, HiddenField, HtmlButton, HtmlGenericControl (+13 more)

### Community 1022 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (14): ServiceCreationDeletionSummary, ServiceDate, ServiceDateMap, UserCreationDate, UserValidTillDate, DateTime, int, string (+6 more)

### Community 1023 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): frmARCOSServerManager, Button, CheckBox, CheckBoxList, DropDownList, GridView, HiddenField, HtmlAnchor (+13 more)

### Community 1024 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): frmConnections, Button, CheckBox, CheckBoxList, DropDownList, FileUpload, HiddenField, HtmlGenericControl (+13 more)

### Community 1025 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (3): Alert, Modal, remove()

### Community 1027 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (15): aa(), B(), c(), D(), F(), g(), h(), I() (+7 more)

### Community 1028 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (13): a(), at(), h(), i(), m(), n(), nt(), o() (+5 more)

### Community 1029 - "ACMO Web — Client Manager"
Cohesion: 0.09
Nodes (21): ACMO_NewDesign, ContentPlaceHolder, HiddenField, HtmlForm, Image, Label, Panel, ScriptManager (+13 more)

### Community 1030 - "ACMO Web — Portal"
Cohesion: 0.10
Nodes (22): absFloor(), absRound(), add_subtract__addSubtract(), addParseToken(), addWeekParseToken(), daysInMonth(), duration_as__valueOf(), get_set__get() (+14 more)

### Community 1031 - "ACMO Web — Portal"
Cohesion: 0.11
Nodes (22): chooseLocale(), createAdder(), defineLocale(), deprecate(), deprecateSimple(), isObject(), listMonthsImpl(), lists__get() (+14 more)

### Community 1032 - "ACMO Web — Web Services"
Cohesion: 0.18
Nodes (9): ARCOSClientManagerOnlineCF, Boolean, DataTable, DateTime, DropDownList, HttpBrowserCapabilities, HttpRequest, Int32 (+1 more)

### Community 1033 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (21): AccountType, AlertNotificationMode, ARCOSAppType, ARCOSCPCSServerType, ARCOSFileStorageType, ARCOSLogType, ARCOSObjectTypes, ARCOSOnBoardingType (+13 more)

### Community 1034 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (19): frmTestForm1, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+11 more)

### Community 1035 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (19): frmUserSecuritySettings, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn (+11 more)

### Community 1036 - "ASM Server — Server Manager"
Cohesion: 0.09
Nodes (19): frmLOBMasterNManager, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn (+11 more)

### Community 1037 - "ASM Server — Pkcs11Interop"
Cohesion: 0.11
Nodes (21): NativeULong, SlotFlags, NativeULong, string, SlotInfo, NativeULong, SlotFlags, NativeULong (+13 more)

### Community 1038 - "Common — Password Manager"
Cohesion: 0.11
Nodes (7): Exception, SSHKeyCommon, Boolean, DataTable, Int32, SqlConnection, String

### Community 1039 - "Common — SLPF"
Cohesion: 0.10
Nodes (11): bool, int, string, ushort, ActionCode, CharKind, IAttrList, IMutableAttrList (+3 more)

### Community 1040 - "Services — PAM Agents"
Cohesion: 0.21
Nodes (13): CreateProcessAsUserWrapper, PROCESS_INFORMATION, ShowWindowEnum, STARTUPINFO, WTS_CONNECTSTATE_CLASS, WTS_SESSION_INFO, DllImport, int (+5 more)

### Community 1041 - "Services — PAM Agents"
Cohesion: 0.14
Nodes (5): AppRegistry, FileManager, ServiceManager, Dictionary, List

### Community 1042 - "Services — Desk Insight"
Cohesion: 0.11
Nodes (9): HelperTool, NameValuePair, SerializableHashtable, Bitmap, Byte, ImageCodecInfo, object, string (+1 more)

### Community 1043 - "Services — Desk Insight"
Cohesion: 0.11
Nodes (13): frmFRScan, bool, CancelEventArgs, EventArgs, FilterInfoCollection, FlowLayoutPanel, FormClosingEventArgs, int (+5 more)

### Community 1044 - "Services — Desk Insight"
Cohesion: 0.14
Nodes (8): frmARCONRARequest, DllImportAttribute, EventArgs, ILog, int, IntPtr, KeyPressEventArgs, MouseEventArgs

### Community 1045 - "Services — Password Change Vault"
Cohesion: 0.10
Nodes (10): IContainer, PasswordChangeVaultService, Program, IDictionary, IContainer, ServiceInstaller, ServiceProcessInstaller, ProjectInstaller (+2 more)

### Community 1046 - "Services — Schedule Password Change"
Cohesion: 0.10
Nodes (11): bool, int, string, ushort, ActionCode, CharKind, IAttrList, IMutableAttrList (+3 more)

### Community 1047 - "Services — Staging Log Sync"
Cohesion: 0.09
Nodes (10): ARCOSApp, ARCOSStagingLogSyncService, IContainer, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller (+2 more)

### Community 1048 - "MultiTab — src"
Cohesion: 0.13
Nodes (3): ErrorLog, JsonInclude, JsonProperty

### Community 1049 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (16): AnimationFlags, Control, DllImport, HandleRef, SuppressUnmanagedCodeSecurity, AnimationFlags, MINMAXINFO, NativeMethods (+8 more)

### Community 1050 - "ACM Common — .User Controls"
Cohesion: 0.11
Nodes (13): ToolWindow, Button, CheckBox, ComboBox, GroupBox, IContainer, Label, OpenFileDialog (+5 more)

### Community 1051 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.10
Nodes (18): MainLocalToServer, Button, ColumnHeader, ContextMenuStrip, FlowLayoutPanel, FolderBrowserDialog, IContainer, Label (+10 more)

### Community 1052 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.14
Nodes (12): CaseInsensitiveComparer, int, SortOrder, RemoteListViewSorter, EventArgs, IEnumerable, List, Message (+4 more)

### Community 1053 - "ACM Client — AS400Terminal"
Cohesion: 0.16
Nodes (12): bool, Boolean, Button, CaptureProcess, DllImport, EventArgs, int, IntPtr (+4 more)

### Community 1054 - "ACM Client — Framework CM"
Cohesion: 0.11
Nodes (11): SecureShellOutgoingTunnel, int, SecureShellConnection, Socket, string, SecureShellTunnel, int, List (+3 more)

### Community 1055 - "Services — Schedule Password Change"
Cohesion: 0.10
Nodes (11): HandshakeType, byte, HandshakeMessage, byte, HandshakeMessage, byte, HandshakeMessage, byte (+3 more)

### Community 1056 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (20): frmDeviceOnboardingNew, Button, CheckBox, DropDownList, GridView, HiddenField, HtmlButton, HtmlGenericControl (+12 more)

### Community 1057 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (10): TODO: remove support for widgetEventPrefix, TODO: make sure destroying one instance of mouse doesn't mess with, TODO: determine which cases actually cause this to happen, TODO: Unwrap at same DOM position, TODO: make renderAxis a prototype function, TODO: Seems like a bug to cache this.outerDimensions, TODO: remove after 1.12, TODO: Find a more generic solution (+2 more)

### Community 1058 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (8): DataTableMerge, DataRow, DataTable, String, FrmRDPSFileTransferSettings, Control, DataTable, EventArgs

### Community 1060 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (8): afterUpdate(), calculateItemHeight(), calculateItemSize(), calculateItemWidth(), calculateLegendItemHeight(), getBoxSize(), isListened(), Legend

### Community 1061 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (3): d(), Di(), kn()

### Community 1062 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (20): SSOMaster, ContentPlaceHolder, HiddenField, HtmlForm, HyperLink, Panel, ScriptManager, UCAppMySQLOption (+12 more)

### Community 1063 - "LDAPAuthenticator"
Cohesion: 0.18
Nodes (6): byte, uint, VendorSpecificAttribute, byte, uint, VendorSpecificAttribute

### Community 1064 - "ASM Server — PAM.Server Manager.Tests"
Cohesion: 0.10
Nodes (10): DataGridViewAutoFilter_Nunit, SetUp, Test, Tests, SetUp, string, Test, UserServiceGroup_Nunit (+2 more)

### Community 1065 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (7): PipedInputStream, bool, byte, int, MethodImpl, SeekOrigin, Thread

### Community 1066 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (18): frmPrivilegedUserDiscovery, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn (+10 more)

### Community 1067 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (18): frmPrivilegedUserDiscoveryScheduler, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn (+10 more)

### Community 1068 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (18): frmServiceDiscovery, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn (+10 more)

### Community 1069 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): authenticateUserCompletedEventArgs, changeUserPassCompletedEventArgs, ResponseType, StatusCodeType, UCPService, bool, object, SendOrPostCallback (+4 more)

### Community 1070 - "Common — APICalling"
Cohesion: 0.20
Nodes (3): APIWrapper, HttpWebRequest, JObject

### Community 1071 - "Common — .PIMUD"
Cohesion: 0.17
Nodes (7): ConnectionRequest, bool, Boolean, int, string, TcpClient, Winsock

### Community 1072 - "Common — Password Manager"
Cohesion: 0.13
Nodes (12): authenticateUserCompletedEventArgs, changeUserPassCompletedEventArgs, ResponseType, StatusCodeType, UCPService, bool, object, SendOrPostCallback (+4 more)

### Community 1073 - "Common — SLPF"
Cohesion: 0.13
Nodes (7): PipedInputStream, bool, byte, int, MethodImpl, SeekOrigin, Thread

### Community 1074 - "Services — Cloud File Uploader"
Cohesion: 0.10
Nodes (11): ProxyBase, ILog, string, Program, ProxyConfiguration, ILog, string, ProxyRDPSServiceInsertV2 (+3 more)

### Community 1075 - "Services — Cloud File Uploader"
Cohesion: 0.11
Nodes (13): APIConfiguration, CloudStorageDetails, GenericResponse, RDPSConfig, RequestResponseApi, SSO_Arcos_Config, bool, Nullable (+5 more)

### Community 1076 - "Services — Desk Insight"
Cohesion: 0.16
Nodes (15): AutoResetEvent, bool, Guid, NetworkInterface, Queue, WlanReasonCode, WlanConnectionNotificationEventData, WlanInterface (+7 more)

### Community 1077 - "Services — Folder Sync Service"
Cohesion: 0.17
Nodes (10): ARCONFolderSyncService, CommonFunctions, Boolean, EventArgs, EventLog, EventLogEntryType, List, String (+2 more)

### Community 1078 - "Services — Schedule Password Change"
Cohesion: 0.13
Nodes (7): PipedInputStream, bool, byte, int, MethodImpl, SeekOrigin, Thread

### Community 1079 - "Services — Schedule Password Change"
Cohesion: 0.13
Nodes (7): PipedInputStream, bool, byte, int, MethodImpl, SeekOrigin, Thread

### Community 1080 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (4): byte, int, DataFragment, SimpleMemoryStream

### Community 1081 - "Services — TSPlugin Service"
Cohesion: 0.11
Nodes (11): SecureShellOutgoingTunnel, int, SecureShellConnection, Socket, string, SecureShellTunnel, int, List (+3 more)

### Community 1082 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (7): PipedInputStream, bool, byte, int, MethodImpl, SeekOrigin, Thread

### Community 1083 - "Services — TSPlugin Service"
Cohesion: 0.12
Nodes (11): SecureShellOutgoingTunnelCompPro, int, SecureShellConnection, Socket, string, SecureShellTunnelCompPro, int, List (+3 more)

### Community 1084 - "MultiTab — src"
Cohesion: 0.11
Nodes (5): JsonInclude, TokenDetails, JsonInclude, JsonProperty, VideoLog

### Community 1085 - "ACM Client — RStream Client"
Cohesion: 0.12
Nodes (14): CommonFunctions, DiskParams, Point, RamDetails, RemoteStatus, Boolean, DateTime, ILog (+6 more)

### Community 1086 - "ACM Client — DQS"
Cohesion: 0.11
Nodes (19): LineNumberDockSide, LineNumberItem, LineNumbers_For_RichTextBox, bool, Color, float, Font, int (+11 more)

### Community 1087 - "ACM Client — SSHTerminal"
Cohesion: 0.13
Nodes (10): bool, int, Process, ProxyHttpConnectAuthMethod, ProxyType, string, TraceEventType, LoginInfo (+2 more)

### Community 1088 - "ACM Client — SSHTerminal"
Cohesion: 0.15
Nodes (17): byte, DllImport, int, IntPtr, SHFILEINFO, SHITEMID, string, uint (+9 more)

### Community 1089 - "ACM Client — SSHTerminal"
Cohesion: 0.17
Nodes (5): bool, Dictionary, EventArgs, TransferConfirmEventArgs, FileOperation

### Community 1090 - "ACM Common — APICalling"
Cohesion: 0.13
Nodes (18): AdAuthStatusResult, CompanyDomains, JsonResult, JsonResultAdAuth, LOBsGlobalConfig, Result, ResultSet, Dictionary (+10 more)

### Community 1091 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.16
Nodes (10): WebDtPully, bool, Boolean, Byte, DataSet, DataTable, DateTime, Hashtable (+2 more)

### Community 1092 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (11): SelectFromListType, frmSelectFromList, DataGridViewCellEventArgs, DataGridViewRow, DataRow, DataTable, EventArgs, Int32 (+3 more)

### Community 1093 - "ACM Common — Enitity Objects"
Cohesion: 0.16
Nodes (18): FormBuilderData, FormBuilderDataDt, FormBuilderJson, ProvisioningData, Root, SeleniumData, SeleniumDataDt, List (+10 more)

### Community 1094 - "ACM Common — Common APICall"
Cohesion: 0.14
Nodes (10): CommonAPICall, bool, HttpWebRequest, long, string, CommonAPICall, bool, HttpWebRequest (+2 more)

### Community 1095 - "ACMO Web — Provisioning Web"
Cohesion: 0.12
Nodes (10): BundleConfig, BundleCollection, FilterConfig, GlobalFilterCollection, RouteConfig, RouteCollection, WebApiConfig, HttpConfiguration (+2 more)

### Community 1096 - "ACMO Web — Provisioning Web"
Cohesion: 0.28
Nodes (8): ValuesController, HttpPost, HttpResponseMessage, ILog, HttpResponseMessage, Response, RpaBotRequest, HttpStatusCode

### Community 1097 - "ACMO Web — APIRA"
Cohesion: 0.12
Nodes (10): BundleConfig, BundleCollection, FilterConfig, GlobalFilterCollection, RouteConfig, RouteCollection, WebApiConfig, HttpConfiguration (+2 more)

### Community 1098 - "ACMO Web — Client Manager"
Cohesion: 0.10
Nodes (19): frmUARDetails, Button, DropDownList, GridView, HiddenField, HtmlForm, HtmlGenericControl, HtmlHead (+11 more)

### Community 1099 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (12): createAttachObserver(), createDetachObserver(), createResizeObserver(), DomPlatform, initCanvas(), isNullOrEmpty(), listenDevicePixelRatioChanges(), nodeListContains() (+4 more)

### Community 1100 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (5): ArcElement, drawArc(), Element, inRange$1(), PointElement

### Community 1101 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): BarElement, binarySearch(), dataset(), evaluateInteractionItems(), getAxisItems(), getDistanceMetricForAxis(), getIntersectItems(), getNearestCartesianItems() (+5 more)

### Community 1102 - "ACMO Web — Portal"
Cohesion: 0.21
Nodes (20): clone(), cloneWithOffset(), diff(), duration_get__get(), endOf(), getSetDayOfYear(), isAfter(), isBefore() (+12 more)

### Community 1103 - "ACMO Web — Portal"
Cohesion: 0.25
Nodes (19): _fnBlur(), _fnCaptureKeys(), _fnCellFromCoords(), _fnClick(), _fnCoordsFromCell(), _fnEventAdd(), _fnEventAddTemplate(), _fnEventFire() (+11 more)

### Community 1104 - "ACMO Web — Portal"
Cohesion: 0.15
Nodes (12): x(), y(), init(), init(), FIXME: LEGACY BROWSER FIX, init(), init(), FIXME: The drag handling implemented here should be (+4 more)

### Community 1105 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (17): frmScheduleReports, Button, CheckBox, ColumnHeader, ComboBox, DateTimePicker, FolderBrowserDialog, GroupBox (+9 more)

### Community 1106 - "ASM Server — Server Manager"
Cohesion: 0.21
Nodes (6): frmReportManager, Boolean, DataTable, EventArgs, ListViewItem, SplitterEventArgs

### Community 1107 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (17): frmARCOSWorkflowApprovalMatrix, Button, CheckBox, CheckedListBox, ColumnHeader, ComboBox, DateTimePicker, GroupBox (+9 more)

### Community 1108 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (17): frmUserAccessReviewWorkflow, Button, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker, GroupBox, IContainer (+9 more)

### Community 1109 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (17): frmUserRequestApprovalOverridingWorkflow, Button, CheckBox, CheckedListBox, ColumnHeader, ComboBox, DateTimePicker, GroupBox (+9 more)

### Community 1110 - "Common — Common Functions DB"
Cohesion: 0.28
Nodes (9): CommonFunctionsDB, Boolean, CommandType, DataSet, DataTable, SqlConnection, SqlConnectionStringBuilder, SqlParameter (+1 more)

### Community 1111 - "Services — Alert Service"
Cohesion: 0.18
Nodes (8): UserAccessReviewProcess, DataRow, DataSet, DataTable, Hashtable, Int32, String, USPSqlParameterMaster

### Community 1112 - "Services — PAM Agents"
Cohesion: 0.15
Nodes (8): Program, Boolean, STAThread, Stream, Resource, CultureInfo, ResourceManager, ARCONPAMThickClientPortable

### Community 1113 - "Services — Cloud File Uploader"
Cohesion: 0.14
Nodes (11): ErrorHandlerHelper, Exception, ILog, string, ProxyHelper, HttpWebRequest, ILog, int (+3 more)

### Community 1114 - "Services — Data Sync"
Cohesion: 0.10
Nodes (10): Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller, SynDBService, IContainer (+2 more)

### Community 1115 - "Services — DBSync Service"
Cohesion: 0.14
Nodes (14): ObjectCommonProperties, PriorityMaster, RecordStatus, Settings, bool, Boolean, DateTime, EventArgs (+6 more)

### Community 1116 - "Services — Desk Insight"
Cohesion: 0.11
Nodes (12): bool, CancelEventArgs, EventArgs, FilterInfoCollection, FormClosingEventArgs, int, NewFrameEventArgs, PowerModeChangedEventArgs (+4 more)

### Community 1117 - "Services — Desk Insight"
Cohesion: 0.16
Nodes (19): bool, byte, Dot11BssType, Dot11Ssid, ulong, WlanReasonCode, Dot11Ssid, WlanAssociationAttributes (+11 more)

### Community 1118 - "Services — Migrate Data Utility"
Cohesion: 0.18
Nodes (3): EventArgs, int, ParenForm

### Community 1119 - "Services — Privilege User Discovery"
Cohesion: 0.18
Nodes (6): ConnectionRequest, bool, Boolean, int, string, Winsock

### Community 1120 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (8): ConfigNode, ArrayList, Hashtable, IDictionaryEnumerator, IEnumerable, string, TextReader, TextWriter

### Community 1121 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (12): MessageReceivedArgs, NetworkTool, Node, bool, Hashtable, int, IPEndPoint, ISynchronizeInvoke (+4 more)

### Community 1122 - "Datum Bridge"
Cohesion: 0.14
Nodes (9): Database, DataTable, IDataParameter, IDbCommand, IDbConnection, IDbDataAdapter, DatabaseFactory, DatabaseFactory (+1 more)

### Community 1123 - "Datum Bridge Client"
Cohesion: 0.16
Nodes (9): MYSQLParam, IDbCommand, MySqlParameter, MYSQLDatabase, DataTable, IDataParameter, IDbCommand, IDbConnection (+1 more)

### Community 1124 - "ACM Client — DQS"
Cohesion: 0.16
Nodes (7): AddNewTableForm, DataGridViewCellEventArgs, DataSet, EventArgs, Message, string, DataGridViewCellValidatingEventArgs

### Community 1125 - "ACM Client — Framework CM"
Cohesion: 0.22
Nodes (8): HSMCommonFunctionCM, DataTable, List, UDEKStorage, HSMDataFunctionsCM, DataTable, UDEKStorage, DateTime

### Community 1126 - "ACM Client — Framework CM"
Cohesion: 0.16
Nodes (7): frmServicesQuickSearch, Control, DataGridViewCellEventArgs, DataTable, EventArgs, LinkLabelLinkClickedEventArgs, String

### Community 1127 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (12): SshOverTlsTunnel, TunnelOptions, CancellationToken, CancellationTokenSource, ForwardedPortLocal, Process, SshClient, Task (+4 more)

### Community 1128 - "ACM Client — SFTPTeminal"
Cohesion: 0.11
Nodes (12): MakeDirectoryDialog, Button, IContainer, Label, TextBox, PropertiesDialog, Button, CheckBox (+4 more)

### Community 1129 - "ACM Client — SSHTerminal"
Cohesion: 0.12
Nodes (8): Login, EventArgs, LoginInfo, int, ProxyHttpConnectAuthMethod, ProxyType, string, CancelEventArgs

### Community 1130 - "ACM Client — Web Browser"
Cohesion: 0.15
Nodes (7): BrowserControl, Control, EventArgs, KeyEventArgs, WebBrowserDocumentCompletedEventArgs, WebBrowserNavigatedEventArgs, HtmlElementErrorEventArgs

### Community 1131 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (8): BigInteger, ConfidenceFactor, PrimalityTest, PrimeGeneratorBase, BigInteger, SequentialSearchPrimeGeneratorBase, BigInteger, SequentialSearchPrimeGeneratorBase

### Community 1132 - "ACMO Web — Client Manager"
Cohesion: 0.24
Nodes (15): a(), b(), bindHover(), d(), Datepicker(), f(), h(), i() (+7 more)

### Community 1133 - "ACMO Web — Client Manager"
Cohesion: 0.11
Nodes (15): psCtrl, CheckBox, HiddenField, Label, LinkButton, Panel, stCtrl, EventArgs (+7 more)

### Community 1134 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (7): frmGatewayConfigurationDetails, Boolean, DataTable, EventArgs, ObjectCache, RepeaterCommandEventArgs, String

### Community 1137 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (4): CurrentTimeDisplay(), DurationDisplay(), RemainingTimeDisplay(), TimeDisplay()

### Community 1138 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), ei(), Ie(), je(), Ni(), oa() (+4 more)

### Community 1139 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (5): ce(), de, dt(), en, he()

### Community 1141 - "LDAPAuthenticator"
Cohesion: 0.23
Nodes (5): byte, RadiusAttribute, byte, RadiusAttribute, RadiusAttributeType

### Community 1143 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (12): frmRDPLogViewer_Streaming, AxWindowsMediaPlayer, Button, IContainer, ImageList, Label, Panel, PictureBox (+4 more)

### Community 1144 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmHardwareTokenRadiusServer, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+8 more)

### Community 1145 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmHardwareTokenRadiusServer, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+8 more)

### Community 1146 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmAddIPFilter, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, GroupBox, IContainer (+8 more)

### Community 1147 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmServicesQuickSearch, Button, ColumnHeader, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+8 more)

### Community 1148 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmSLAConfiguration, Button, CheckBox, ColumnHeader, ComboBox, DateTimePicker, GroupBox, IContainer (+8 more)

### Community 1149 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmWindowsConnection, Button, CheckBox, ColumnHeader, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+8 more)

### Community 1150 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmWindowsUtility, Button, CheckBox, ColumnHeader, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn, IContainer (+8 more)

### Community 1151 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (16): frmLOBDefaultSettings, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, GroupBox, IContainer (+8 more)

### Community 1152 - "Services — Active Directory Insight"
Cohesion: 0.19
Nodes (8): CommonFunctions, Boolean, DateTime, EventLog, EventLogEntryType, Int32, Object, String

### Community 1153 - "Services — Active Directory Insight"
Cohesion: 0.11
Nodes (9): ARCONActiveDirectoryInsight, IContainer, Program, ProjectInstaller, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller (+1 more)

### Community 1154 - "Services — DBSync Service"
Cohesion: 0.15
Nodes (8): INIFile, Boolean, DllImport, Int32, string, StringBuilder, CommonFunctions, Boolean

### Community 1155 - "Services — Desk Insight"
Cohesion: 0.17
Nodes (8): ClipboardMonitor, ClipboardWatcher, DllImport, int, IntPtr, Message, string, ClipboardWatcher

### Community 1156 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (9): FacialRecognition, bool, EventArgs, FilterInfoCollection, int, List, NewFrameEventArgs, string (+1 more)

### Community 1157 - "Services — Desk Insight"
Cohesion: 0.17
Nodes (7): frmRunAs, DllImportAttribute, DragEventArgs, EventArgs, int, IntPtr, MouseEventArgs

### Community 1158 - "Services — Folder Sync Service"
Cohesion: 0.12
Nodes (6): AutoResetEvent, bool, Queue, string, Thread, FolderSynchronization

### Community 1159 - "Services — Folder Sync Service"
Cohesion: 0.14
Nodes (9): string, FolderSynchorizationOption, FolderSynchronizationScanner, bool, DateTime, string, FolderSynchronizationScannerItem, FileInfo (+1 more)

### Community 1160 - "Services — Passworde Envelope Manager"
Cohesion: 0.11
Nodes (17): frmMain, Button, ColumnHeader, ContextMenuStrip, DataGridView, GroupBox, IContainer, ImageList (+9 more)

### Community 1161 - "Services — Scheduler Service"
Cohesion: 0.20
Nodes (8): UserAccessReviewProcess, DataRow, DataSet, DataTable, Hashtable, Int32, String, USPSqlParameterMaster

### Community 1162 - "Services — TSPlugin Service"
Cohesion: 0.23
Nodes (9): PBitmap, Rect, Bitmap, Boolean, DllImport, int, IntPtr, MarshalAs (+1 more)

### Community 1163 - "Offline MultiTab — Windows Service"
Cohesion: 0.16
Nodes (9): BackgroundService, IServiceScopeFactory, CancellationToken, ILogger, int, string, Task, Timer (+1 more)

### Community 1165 - "Offline MultiTab — Offline API"
Cohesion: 0.11
Nodes (18): ASPNETCORE_ENVIRONMENT, commandName, environmentVariables, launchBrowser, applicationUrl, sslPort, iisSettings, anonymousAuthentication (+10 more)

### Community 1166 - "ACM Client — Sshkey SFTP"
Cohesion: 0.18
Nodes (8): DragAndDropListView, DragItemData, bool, DragEventArgs, ItemDragEventArgs, List, ListViewItem, DragEventArgs

### Community 1167 - "ACM Client — DQS"
Cohesion: 0.12
Nodes (12): Settings, ServerList, Settings, CancelEventArgs, Resources, Bitmap, CultureInfo, Icon (+4 more)

### Community 1168 - "ACM Client — Framework CM"
Cohesion: 0.21
Nodes (5): AutomationFocusChangedEventArgs, DllImport, IntPtr, MonitorDpiType, StringBuilder

### Community 1169 - "ACM Client — Framework CM"
Cohesion: 0.25
Nodes (8): PBitmap, Rect, Bitmap, Boolean, DllImport, int, IntPtr, MarshalAs

### Community 1170 - "ACM Client — Framework CM"
Cohesion: 0.19
Nodes (8): frmSessionFreeze, bool, Boolean, EventArgs, FormClosingEventArgs, Int32, String, Timer

### Community 1171 - "ACM Client — Script Manager"
Cohesion: 0.11
Nodes (15): frmCommandLogTextViewer_ScriptManager, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ListView, Panel, ToolStrip (+7 more)

### Community 1172 - "ACM Client — SSHTerminal"
Cohesion: 0.19
Nodes (6): DllImport, Exception, Form, int, IntPtr, Util

### Community 1173 - "ACM Client — Web Browser"
Cohesion: 0.11
Nodes (12): frmARCOSWebBrowser_WB2, Button, IContainer, Panel, StatusStrip, TextBox, Timer, ToolStripStatusLabel (+4 more)

### Community 1174 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (7): ConfidenceFactor, BigInteger, SequentialSearchPrimeGeneratorBase, ConfidenceFactor, ConfidenceFactor, ConfidenceFactor, Mono.Math.Prime

### Community 1175 - "Services — Enitity Objects"
Cohesion: 0.12
Nodes (14): ARCOSWorkFlowType, ARCOSApproverDetails, int, Int32, string, ARCOSApproverDetails, int, Int32 (+6 more)

### Community 1176 - "ACM Common — Enitity Objects"
Cohesion: 0.12
Nodes (10): ARCOSLogMethod, ServiceLogMethod, SSOSeviceOpenConn, ARCOSLogMethod, ServiceLogMethod, ARCOSLogMethod, ServiceLogMethod, SSOSeviceOpenConn (+2 more)

### Community 1177 - "ACM Common — Workflow Id"
Cohesion: 0.17
Nodes (10): ARCONIdGenerator, int, long, object, string, ARCONIdGenerator, int, long (+2 more)

### Community 1178 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (6): frmUserRoleBulk, DataTable, EventArgs, Int32, LinkLabelLinkClickedEventArgs, ListViewItem

### Community 1179 - "ACMO Web — Provisioning Web"
Cohesion: 0.24
Nodes (16): addStyleSheet(), contains(), createDocumentFragment(), createElement(), getElements(), getExpandoData(), is(), isEventSupported() (+8 more)

### Community 1180 - "ACMO Web — APIRA"
Cohesion: 0.24
Nodes (16): addStyleSheet(), contains(), createDocumentFragment(), createElement(), getElements(), getExpandoData(), is(), isEventSupported() (+8 more)

### Community 1185 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (8): beforeDraw(), draw(), _getInterpolationMethod(), _getSegmentMethod(), LineElement, setStyle(), strokePathDirect(), strokePathWithCache()

### Community 1186 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (4): convert(), exists(), form(), Keystroke()

### Community 1189 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (8): beforeDraw(), draw(), _getInterpolationMethod(), _getSegmentMethod(), LineElement, setStyle(), strokePathDirect(), strokePathWithCache()

### Community 1191 - "ACMO Web — Client Manager"
Cohesion: 0.16
Nodes (12): x(), y(), init(), init(), FIXME: LEGACY BROWSER FIX, init(), init(), FIXME: The drag handling implemented here should be (+4 more)

### Community 1193 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (4): e(), i(), n(), s()

### Community 1194 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (18): arrow(), getBordersSize(), getBoundaries(), getBoundingClientRect(), getClientRect(), getFixedPositionOffsetParent(), getOffsetRectRelativeToArbitraryNode(), getOuterSizes() (+10 more)

### Community 1195 - "ACMO Web — Client Manager"
Cohesion: 0.26
Nodes (4): SSHLinuxOptionButton, UCSSHConnectionOption, EventArgs, UpdatePanelUpdateMode

### Community 1196 - "LDAPAuthenticator"
Cohesion: 0.12
Nodes (12): byte, List, ushort, RadiusPacket, Compression, Login, NasPortType, Protocol (+4 more)

### Community 1197 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (18): checkOverflow(), configFromInput(), configFromISO(), configFromString(), configFromStringAndArray(), configFromStringAndFormat(), createFromConfig(), defaultParsingFlags() (+10 more)

### Community 1198 - "ACMO Web — Portal"
Cohesion: 0.14
Nodes (18): addFormatToken(), addWeekYearFormatToken(), duration_humanize__relativeTime(), format(), getSetDayOfWeek(), getSetLocaleDayOfWeek(), getSetWeek(), getSetWeekYear() (+10 more)

### Community 1200 - "ACMO Web — User Access"
Cohesion: 0.26
Nodes (7): DefaultV5, AmazonS3Client, bool, Boolean, EventArgs, long, string

### Community 1201 - "ASM Server — Server Manager"
Cohesion: 0.10
Nodes (12): DataGridViewAutoFilter, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator, DataGridViewAutoFilter, Button (+4 more)

### Community 1202 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): bool, byte, string, AuthType, CertificateChainOptions, CertificateStatus, CertificateStoreType, Extension (+6 more)

### Community 1203 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (7): Servers, ServersParameters, Boolean, DateTime, Int32, Int64, string

### Community 1204 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmAlertNotificationConfiguration, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker, GroupBox (+7 more)

### Community 1205 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmARCOSServerMaster, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1206 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmDomainOnBoarding, Button, CheckBox, ColumnHeader, ComboBox, DateTimePicker, GroupBox, IContainer (+7 more)

### Community 1207 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmServiceCriticalCommands, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1208 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmWebAPIRegistration, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1209 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmAlertNotificationConfiguration, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, DateTimePicker, GroupBox (+7 more)

### Community 1210 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmARCOSServerMaster, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1211 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmDomainOnBoarding, Button, CheckBox, ColumnHeader, ComboBox, DateTimePicker, GroupBox, IContainer (+7 more)

### Community 1212 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmServiceCriticalCommands, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1213 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmWebAPIRegistration, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+7 more)

### Community 1214 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmHPSiteScope, Button, CheckBox, ColumnHeader, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+7 more)

### Community 1215 - "ASM Server — Server Manager"
Cohesion: 0.21
Nodes (6): frmAddServerServices, Boolean, DataTable, EventArgs, LinkLabelLinkClickedEventArgs, ListViewItem

### Community 1216 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (9): frmEnableSTP, CheckBoxHeaderCell, CheckBoxHeaderCellEventArgs, DataGridViewDataErrorEventArgs, DataTable, int, Int32, MouseEventArgs (+1 more)

### Community 1217 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmServersPasswordDependency_PPPCA, Button, CheckBox, ComboBox, ContextMenuStrip, GroupBox, IContainer, ImageList (+7 more)

### Community 1218 - "ASM Server — Server Manager"
Cohesion: 0.11
Nodes (15): frmServersPasswordDependency_SelectService, Button, CheckBox, ColumnHeader, ComboBox, ContextMenuStrip, GroupBox, IContainer (+7 more)

### Community 1219 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): DataSet1, DataTable1RowChangeEvent, CollectionChangeEventArgs, DataRelationCollection, DataRowAction, DataTable1DataTable, DataTableCollection, SchemaSerializationMode (+3 more)

### Community 1220 - "Common — .Encrypt Descrypt File"
Cohesion: 0.24
Nodes (6): EncryptDescryptFile, Bitmap, Boolean, Image, Int32, String

### Community 1221 - "Common — SLPF"
Cohesion: 0.12
Nodes (14): bool, byte, string, AuthType, CertificateChainOptions, CertificateStatus, CertificateStoreType, Extension (+6 more)

### Community 1222 - "Common — Enitity Objects"
Cohesion: 0.22
Nodes (7): ExportLog, DataTable, Image, Int32, List, String, WordDocument

### Community 1223 - "Services — Migrate Data Utility"
Cohesion: 0.17
Nodes (6): DataSet, DataTable, SqlCommand, SqlConnection, SqlParameter, ISqlDbConnectionBase

### Community 1224 - "Services — Perf Mon IT"
Cohesion: 0.18
Nodes (8): Windows, Boolean, Int32, String, Winsock, WinsockDataArrivalEventArgs, WinsockErrorReceivedEventArgs, WinsockSendEventArgs

### Community 1225 - "Services — Provisioning Scheduler"
Cohesion: 0.20
Nodes (9): DataTable, List, HSMCommonFunction, DataTable, HSMDataFunctions, AppSettings, UtimacoHSMData, List (+1 more)

### Community 1226 - "Services — Schedule Password Change"
Cohesion: 0.12
Nodes (14): bool, byte, string, AuthType, CertificateChainOptions, CertificateStatus, CertificateStoreType, Extension (+6 more)

### Community 1227 - "Services — Schedule Password Change"
Cohesion: 0.12
Nodes (14): bool, byte, string, AuthType, CertificateChainOptions, CertificateStatus, CertificateStoreType, Extension (+6 more)

### Community 1228 - "Services — Staging Log Sync"
Cohesion: 0.18
Nodes (12): ARCOSStagingLogSyncServiceSettings, TimeBetween, Boolean, DateTime, Int32, String, ARCOSStagingLogSyncServiceSettings, TimeBetween (+4 more)

### Community 1229 - "Services — TSPlugin Service"
Cohesion: 0.16
Nodes (7): Servers, ServersParameters, Boolean, DateTime, Int32, Int64, string

### Community 1230 - "Services — TSPlugin Service"
Cohesion: 0.12
Nodes (14): bool, byte, string, AuthType, CertificateChainOptions, CertificateStatus, CertificateStoreType, Extension (+6 more)

### Community 1232 - "Offline MultiTab — Offline API"
Cohesion: 0.24
Nodes (16): addStyleSheet(), contains(), createDocumentFragment(), createElement(), getElements(), getExpandoData(), is(), isEventSupported() (+8 more)

### Community 1233 - "ACM Client — PAMMulti Tab"
Cohesion: 0.19
Nodes (9): OpenConnnection, Program, bool, Boolean, SslPolicyErrors, STAThread, string, X509Certificate (+1 more)

### Community 1234 - "ACM Client — Sshkey SFTP"
Cohesion: 0.13
Nodes (5): ColumnClickEventArgs, FileSystemProgressEventArgs, SftpFileInfoCollection, SftpFilePermissions, SortOrder

### Community 1235 - "ACM Client — App Exe"
Cohesion: 0.18
Nodes (9): ARCOSLaunchSSO, CreateParams, DllImport, EventArgs, int, IntPtr, Point, Process (+1 more)

### Community 1236 - "ACM Client — RDPTerminal"
Cohesion: 0.15
Nodes (11): DllImport, DPI_AWARENESS_CONTEXT, OpenConnnection, Program, Boolean, DllImport, int, IntPtr (+3 more)

### Community 1237 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (16): ImageFormat, CG4ApiVersion, CG4AutoCapInfo, CG4PropertyInfo, CG4RunningInfo, CG4ScannerExist, CgRollParameters, ImageData (+8 more)

### Community 1238 - "ACM Client — Framework CM"
Cohesion: 0.18
Nodes (7): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, PaintEventArgs, String, Thread

### Community 1239 - "ACM Client — Framework CM"
Cohesion: 0.14
Nodes (16): COPYDATASTRUCT, CtrlType, CURSORINFO, HookType, MouseEventFlags, POINTAPI, Rect, User32 (+8 more)

### Community 1240 - "ACM Client — SSHTerminal"
Cohesion: 0.16
Nodes (9): ItemDragEventArgs, List, ListViewItem, DragItemData, bool, DragEventArgs, ItemDragEventArgs, DragAndDropListView (+1 more)

### Community 1241 - "ACM Client — SSHTerminal"
Cohesion: 0.12
Nodes (10): bool, Button, Container, EventArgs, int, PaintEventArgs, PictureBox, string (+2 more)

### Community 1242 - "ACM Client — SSHTerminal"
Cohesion: 0.12
Nodes (13): ColoredComboBox, Color, DrawItemEventArgs, int, KeyValuePair, List, ColoredComboBox, Color (+5 more)

### Community 1243 - "LDAPAuthenticator — .Radius"
Cohesion: 0.12
Nodes (4): RadiusCrypto, RadiusCrypto, RadiusCrypto, RadiusCrypto

### Community 1244 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (9): Popup, IContainer, PopupComboBox, Control, DateTime, Message, ObjectCollection, SecurityPermission (+1 more)

### Community 1245 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (7): ArconCustomCommands, frmCustomCommandConfigurationpopup, DataRow, EventArgs, int, Int64, ListViewItem

### Community 1246 - "ACM Common — Random String"
Cohesion: 0.20
Nodes (8): RandomStringGenerator, bool, Boolean, char, int, List, RNGCryptoServiceProvider, string

### Community 1247 - "ACMO Web — Client Manager"
Cohesion: 0.21
Nodes (5): frmOnboardingDashboard, clsOnboarding, EventArgs, ScriptMethod, WebMethod

### Community 1248 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (16): frmConnections_new, Button, CheckBox, DropDownList, GridView, HiddenField, HtmlGenericControl, Image (+8 more)

### Community 1249 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (16): frmFileServerConfig, Button, DropDownList, GridView, HtmlGenericControl, HtmlSelect, Label, LinkButton (+8 more)

### Community 1251 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (3): getNextActiveElement(), isVisible(), ScrollSpy

### Community 1253 - "ACMO Web — Client Manager"
Cohesion: 0.21
Nodes (12): aesEncrypt(), arrayBufferToBase64(), encryptData(), encryptSymmetricKey(), ErrorCall(), generateKeyAndIV(), GetError(), GetErrorInfo() (+4 more)

### Community 1254 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (17): configFromArray(), createUTCDate(), currentDateArray(), dayOfYearFromWeekInfo(), dayOfYearFromWeeks(), daysInYear(), firstWeekOffset(), getIsLeapYear() (+9 more)

### Community 1255 - "ACMO Web — Portal"
Cohesion: 0.15
Nodes (17): chooseLocale(), compareArrays(), copyConfig(), create_utc__createUTC(), createLocalOrUTC(), isDaylightSavingTimeShifted(), isUndefined(), list() (+9 more)

### Community 1256 - "ACMO Web — Portal"
Cohesion: 0.18
Nodes (17): configFromArray(), createUTCDate(), currentDateArray(), dayOfYearFromWeekInfo(), dayOfYearFromWeeks(), daysInYear(), defaults(), firstWeekOffset() (+9 more)

### Community 1257 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (5): HardwareDetails, String, IPMACManager, Boolean, String

### Community 1258 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmSchedulePasswordEnvelope, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+6 more)

### Community 1259 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmScheduleReconciliation, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+6 more)

### Community 1260 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmBulkUpdate, Button, ColumnHeader, ComboBox, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+6 more)

### Community 1261 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmImportDetails, Button, ColumnHeader, ComboBox, GroupBox, IContainer, Label, ListView (+6 more)

### Community 1262 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (9): frmPasswordChangeHistory, ColumnClickEventArgs, ColumnHeader, DrawListViewColumnHeaderEventArgs, DrawListViewItemEventArgs, DrawListViewSubItemEventArgs, EventArgs, int (+1 more)

### Community 1263 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmPasswordManager_PolicyServices, Button, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+6 more)

### Community 1264 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmRealTimeSessionMonitoring, Button, CheckBox, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList (+6 more)

### Community 1265 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (14): frmServersPasswordDependency, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, Label (+6 more)

### Community 1266 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (8): DataTable1DataTable, DataColumn, DataRowChangeEventArgs, DataTable, DataTable1Row, DataTable1RowChangeEvent, DataRowAction, TypedTableBase

### Community 1268 - "Services — Active Directory Insight"
Cohesion: 0.21
Nodes (9): ARCONActiveDirectoryInsightSettings, NewUserGroupAction, UserGroupAndUsers, Boolean, Char, DateTime, Int32, List (+1 more)

### Community 1269 - "Services — PAM Agents"
Cohesion: 0.13
Nodes (8): EventArgs, Timer, IContainer, frmKeepAlive, frmKeepAlive, STAThread, Program, KeepAliveAPP

### Community 1270 - "Services — Desk Insight"
Cohesion: 0.14
Nodes (12): Impersonation, SafeTokenHandle, DllImport, int, IntPtr, MarshalAs, String, SuppressUnmanagedCodeSecurity (+4 more)

### Community 1271 - "Services — Desk Insight"
Cohesion: 0.12
Nodes (14): frmElevationRequest, Button, CheckBox, CheckedListBox, ComboBox, DateTimePicker, FlowLayoutPanel, GroupBox (+6 more)

### Community 1272 - "Services — Provisioning Scheduler"
Cohesion: 0.20
Nodes (9): PasswordGenerator, bool, Boolean, char, ILog, int, List, RNGCryptoServiceProvider (+1 more)

### Community 1274 - "Services — TSPlugin Service"
Cohesion: 0.18
Nodes (8): PacketMonitor, byte, DllImport, IAsyncResult, int, IntPtr, IPAddress, Socket

### Community 1275 - "Services — TSPlugin Service"
Cohesion: 0.15
Nodes (9): int, List, Queue, Thread, ScheduledEvent, ScheduledEventType, StreamStateLog, StreamTester (+1 more)

### Community 1277 - "Services — TSPlugin Service"
Cohesion: 0.15
Nodes (6): ISensLogon2, SensEvents, Sink, Guid, ISensLogon2, Sink

### Community 1279 - "Services — Z POC"
Cohesion: 0.12
Nodes (10): EventArgs, Button, IContainer, Label, TextBox, Form1, Form1, STAThread (+2 more)

### Community 1282 - "ACM Client — PAMSecure SSOApps"
Cohesion: 0.20
Nodes (6): frmSecureSSOApps, IContainer, Panel, OpenConnection, Boolean, String

### Community 1283 - "ACM Client — App Exe"
Cohesion: 0.14
Nodes (9): frmSSOInProgress, EventArgs, int, frmSSOInProgress, Button, IContainer, Label, SplitContainer (+1 more)

### Community 1284 - "ACM Client — DQS"
Cohesion: 0.12
Nodes (13): QueryForm, ColumnHeader, ContextMenuStrip, IContainer, ImageList, ListView, SplitContainer, StatusStrip (+5 more)

### Community 1285 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (12): PortForwardEventArgs, IphlpAPIManager, MIB_TCPROW_OWNER_PID, MIB_TCPTABLE_OWNER_PID, TCP_TABLE_CLASS, byte, DllImport, int (+4 more)

### Community 1286 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (11): frmMSSQLConnectionRetry, Boolean, Byte, EventArgs, Exception, FormClosingEventArgs, int, Int32 (+3 more)

### Community 1287 - "ACM Client — Framework CM"
Cohesion: 0.17
Nodes (10): InputBox, InputBoxResult, Button, DialogResult, EventArgs, Form, int, Label (+2 more)

### Community 1288 - "ACM Client — SSHTerminal"
Cohesion: 0.17
Nodes (8): Button, Container, EventArgs, EventHandler, Keys, MenuItem, TextBox, LogNoteForm

### Community 1289 - "ACM Client — Web Browser"
Cohesion: 0.12
Nodes (13): ARCOSWebBrowserType, DPI_AWARENESS_CONTEXT, Program, string, frmARCOSWebBrowserGecko, Button, GeckoWebBrowser, IContainer (+5 more)

### Community 1290 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (10): ARCOSLinkedDomainParameter, bool, Boolean, int, string, frmLinkedDomainSetting, Boolean, DataTable (+2 more)

### Community 1291 - "Common — Server Common Functions"
Cohesion: 0.17
Nodes (9): frmMSSQLConnectionRetry, Button, IContainer, Label, PictureBox, TextBox, MSSqlDBConnection, SqlConnection (+1 more)

### Community 1292 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (15): frmARCOSDashboardUserAccess, Button, DropDownList, GridView, HiddenField, HtmlForm, HtmlGenericControl, Image (+7 more)

### Community 1293 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (15): frmReports, Button, CheckBox, DropDownList, GridView, HiddenField, HtmlGenericControl, HtmlInputHidden (+7 more)

### Community 1298 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (15): frmARCONServiceLogs, ACMenuControl, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden (+7 more)

### Community 1299 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (15): frmARCONServicePasswordStatusLogs, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+7 more)

### Community 1300 - "ACMO Web — Client Manager"
Cohesion: 0.12
Nodes (15): frmARCOSPamLogs, Button, DropDownList, GridView, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+7 more)

### Community 1301 - "ACMO Web — Portal"
Cohesion: 0.16
Nodes (16): cloneSubtree(), compareRanges(), extractSubtree(), gEBI(), getRangeDocument(), insertRangeBoundaryMarker(), removeMarkerElement(), removeMarkers() (+8 more)

### Community 1304 - "ASM Server — Server Manager"
Cohesion: 0.26
Nodes (6): EncryptDescryptFile, Bitmap, Boolean, Image, Int32, String

### Community 1305 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (9): DgvBaseFilterHost, Bitmap, Color, ComboBox, Control, EventArgs, Region, Size (+1 more)

### Community 1306 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (6): KeyGenerator, DateTime, string, KeyGenerator, DateTime, string

### Community 1307 - "ASM Server — Server Manager"
Cohesion: 0.23
Nodes (15): ManageServicePassword, ServiceReferenceLogParams, UserAndServerRequestLogsParams, ViewARCOSLogParams, ViewDBALogParams, ViewPasswordChangeLogParams, ViewProcessLogParams, ViewServerAccessOutsideParams (+7 more)

### Community 1308 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmServiceClassification, Button, ColumnHeader, GroupBox, IContainer, ImageList, Label, ListView (+5 more)

### Community 1309 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmServiceClassification, Button, ColumnHeader, GroupBox, IContainer, ImageList, Label, ListView (+5 more)

### Community 1310 - "ASM Server — Server Manager"
Cohesion: 0.23
Nodes (8): RandomStringGenerator, bool, Boolean, char, int, List, RNGCryptoServiceProvider, string

### Community 1311 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmAccessControl, ErrorProvider, IContainer, ImageList, ListBox, MenuStrip, StatusStrip, Timer (+5 more)

### Community 1312 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmManageGroupUtility, Button, ColumnHeader, ComboBox, ContextMenuStrip, GroupBox, IContainer, ImageList (+5 more)

### Community 1313 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (8): frmPasswordManagerQuickSearch, DataGridViewCellEventArgs, DataTable, EventArgs, LinkLabelLinkClickedEventArgs, List, MouseEventArgs, String

### Community 1314 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmServicesQuickSearch_Modify, Button, CheckBox, ComboBox, ContextMenuStrip, DateTimePicker, GroupBox, IContainer (+5 more)

### Community 1315 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmUserPrivilegesSetting, Button, ColumnHeader, GroupBox, IContainer, ImageList, Label, ListView (+5 more)

### Community 1316 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (8): PdfPage, PdfWriter, Byte, FileStream, float, int, long, StreamReader

### Community 1317 - "ASM Server — Server Manager"
Cohesion: 0.12
Nodes (13): frmPasswordReconciliation, Button, CheckBox, ComboBox, ContextMenuStrip, DataGridView, DataGridViewTextBoxColumn, GroupBox (+5 more)

### Community 1318 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (8): ManageCommand, Control, EventArgs, String, ManageCommand, IContainer, RadioButton, ARCOSServer.ManageCommand

### Community 1319 - "ASM Server — Pkcs11Interop"
Cohesion: 0.20
Nodes (7): bool, byte, Dictionary, List, string, ulong, Pkcs11UriBuilder

### Community 1320 - "Common — APICalling"
Cohesion: 0.27
Nodes (5): APICallRequest, DataTable, dynamic, HttpResponseMessage, HttpWebRequest

### Community 1321 - "Common — .PIMUD"
Cohesion: 0.17
Nodes (7): Oracle, OracleDBConnection, Boolean, DataTable, int, OracleConnection, String

### Community 1322 - "Common — Random String Generator"
Cohesion: 0.23
Nodes (8): RandomStringGenerator, bool, Boolean, char, int, List, RNGCryptoServiceProvider, string

### Community 1324 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (11): Elevation, bool, DateTime, EventArgs, List, string, frmArgumentforApp, EventArgs (+3 more)

### Community 1325 - "Services — Desk Insight"
Cohesion: 0.23
Nodes (5): frmUSBElevationRequest, DateTime, EventArgs, List, string

### Community 1326 - "Services — Migrate Data Utility"
Cohesion: 0.23
Nodes (8): RandomStringGenerator, bool, Boolean, char, int, List, RNGCryptoServiceProvider, string

### Community 1327 - "Services — Scheduler Service"
Cohesion: 0.21
Nodes (9): DataRow, ArcosReportDownload, ReportQueue, ReportQueueData, Int64, ReportQueueHelper, DataRow, DataTable (+1 more)

### Community 1328 - "Services — TSPlugin Service"
Cohesion: 0.26
Nodes (6): EncryptDescryptFile, Bitmap, Boolean, Image, Int32, String

### Community 1329 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (9): DgvBaseFilterHost, Bitmap, Color, ComboBox, Control, EventArgs, Region, Size (+1 more)

### Community 1330 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (3): byte, int, Rijndael

### Community 1331 - "Datum Bridge"
Cohesion: 0.22
Nodes (6): MYSQLDatabase, DataTable, IDataParameter, IDbCommand, IDbConnection, IDbDataAdapter

### Community 1332 - "Datum Bridge Client"
Cohesion: 0.18
Nodes (7): Database, DataTable, IDataParameter, IDbCommand, IDbConnection, IDbDataAdapter, string

### Community 1334 - "ACM Client — Sshkey SFTP"
Cohesion: 0.23
Nodes (8): ListViewItemComparerBase, ListViewItemDateComparer, ListViewItemNameComparer, ListViewItemPermissionsComparer, ListViewItemSizeComparer, FileInfoBase, int, SortOrder

### Community 1335 - "ACM Client — Sshkey SFTP"
Cohesion: 0.23
Nodes (8): ListViewItemComparerBaseCompro, ListViewItemDateComparerCompro, ListViewItemNameComparerCompro, ListViewItemPermissionsComparerCompro, ListViewItemSizeComparerCompro, FileInfoBase, int, SortOrder

### Community 1336 - "ACM Client — DQS"
Cohesion: 0.13
Nodes (12): ConnectForm, Button, CheckBox, ComboBox, GroupBox, IContainer, Label, RadioButton (+4 more)

### Community 1337 - "ACM Client — DQS"
Cohesion: 0.15
Nodes (5): MYSQLDBClient, IDbCommand, IDbConnection, IDbDataAdapter, MySqlInfoMessageEventArgs

### Community 1338 - "ACM Client — DQS"
Cohesion: 0.24
Nodes (5): IniLexer, int, Scintilla, string, Range

### Community 1339 - "ACM Client — Framework CM"
Cohesion: 0.13
Nodes (12): frmServicesQuickSearch, Button, ColumnHeader, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer, Label (+4 more)

### Community 1340 - "ACM Client — Framework CM"
Cohesion: 0.12
Nodes (11): frmSplashScreen, Button, IContainer, Label, Panel, PictureBox, frmPleaseWait, Button (+3 more)

### Community 1341 - "ACM Client — SFTPTeminal"
Cohesion: 0.23
Nodes (8): ListViewItemComparerBase, ListViewItemDateComparer, ListViewItemNameComparer, ListViewItemPermissionsComparer, ListViewItemSizeComparer, FileInfoBase, int, SortOrder

### Community 1342 - "ACM Client — SFTPTeminal"
Cohesion: 0.23
Nodes (8): FileInfoBase, int, SortOrder, ListViewItemComparerBaseCompro, ListViewItemDateComparerCompro, ListViewItemNameComparerCompro, ListViewItemPermissionsComparerCompro, ListViewItemSizeComparerCompro

### Community 1343 - "ACM Client — SSHTerminal"
Cohesion: 0.13
Nodes (13): Main, ApplicationIdle, IContainer, MenuStrip, SaveFileDialog, SshTerminalControl, StatusStrip, Timer (+5 more)

### Community 1344 - "ACM Client — SSHTerminal"
Cohesion: 0.15
Nodes (6): EventArgs, Icon, StatusBar, StatusBarPanel, Timer, GStatusBar

### Community 1345 - "ACM Client — SSHTerminal"
Cohesion: 0.25
Nodes (5): Hashtable, XmlReader, XmlWriter, XMLUtil, XmlNodeType

### Community 1346 - "ACM Client — VNCTerminal"
Cohesion: 0.28
Nodes (5): Image, Point, Rectangle, Size, VncScaledDesktopPolicy

### Community 1347 - "ACM Client — Web Browser"
Cohesion: 0.13
Nodes (12): frmARCOSWebBrowser, Button, ContextMenuStrip, IContainer, ImageList, Panel, StatusStrip, TabControl (+4 more)

### Community 1348 - "ACM Client — Web Browser"
Cohesion: 0.13
Nodes (12): frmARCOSWebBrowser, Button, ContextMenuStrip, IContainer, ImageList, Panel, StatusStrip, TabControl (+4 more)

### Community 1349 - "ACM Client — Web Browserv35"
Cohesion: 0.23
Nodes (8): UCARCOSWebBrowserSearch, Boolean, EventArgs, KeyPressEventArgs, Object, String, nsIWebBrowser, nsIWebBrowserFind

### Community 1350 - "ACM Common — .PIMUD"
Cohesion: 0.20
Nodes (6): DB2, DB2DBConnection, Boolean, DataTable, DB2Connection, String

### Community 1351 - "ACM Common — SLPF"
Cohesion: 0.22
Nodes (12): Obsolete, isProbablePrime(), BigInteger, PrimalityTests, Obsolete, isProbablePrime(), Obsolete, isProbablePrime() (+4 more)

### Community 1352 - "ACM Common — SPlease Wait"
Cohesion: 0.22
Nodes (6): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, String, Thread

### Community 1353 - "ACM Common — Properties"
Cohesion: 0.15
Nodes (11): Resources, Bitmap, CultureInfo, ResourceManager, Settings, Resources, Bitmap, CultureInfo (+3 more)

### Community 1354 - "ACMO Web — APIOnline"
Cohesion: 0.13
Nodes (10): ServiceType, int, string, Default, Button, GridView, HtmlForm, Label (+2 more)

### Community 1356 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONApplicationLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+6 more)

### Community 1357 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (10): EventArgs, _Default, _Default, string, Task, Startup1, AuthenticationFailedNotification, WebApplication2 (+2 more)

### Community 1358 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCOSApplicationList, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1359 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmLoginACMO, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlImage, HtmlInputHidden, Image (+6 more)

### Community 1360 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmUserActivityLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1362 - "ACMO Web — Client Manager"
Cohesion: 0.19
Nodes (7): a(), d(), e(), k(), l(), M(), N()

### Community 1363 - "ACMO Web — Client Manager"
Cohesion: 0.19
Nodes (9): beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), es(), Ie(), Ni(), oa(), ua() (+1 more)

### Community 1365 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONArchivedLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1366 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONCommandLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1367 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONEnvelopeLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+6 more)

### Community 1368 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONImportUtilityLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+6 more)

### Community 1369 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONProcessLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1370 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONServicePasswordRequestLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+6 more)

### Community 1371 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONUserAccessLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+6 more)

### Community 1372 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONUserActivityLog, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1373 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCONUserStatusLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1374 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): frmARCOSMetaDataTextLogs, ACMenuControl, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label (+6 more)

### Community 1375 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): ARCOSWorkflow_SMRAWFM, Button, CheckBox, CheckBoxList, DropDownList, GridView, HiddenField, HtmlGenericControl (+6 more)

### Community 1376 - "ACMO Web — Client Manager"
Cohesion: 0.13
Nodes (14): ArcosWorkflowTrans, Button, CheckBoxList, DropDownList, GridView, HiddenField, HtmlAnchor, HtmlGenericControl (+6 more)

### Community 1377 - "ACMO Web — Common Functions"
Cohesion: 0.20
Nodes (6): CacheService, byte, string, IDatabase, IgniteClientConfiguration, IIgniteClient

### Community 1379 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (6): DB2, DB2DBConnection, Boolean, DataTable, DB2Connection, String

### Community 1380 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (5): Socket, Sock, SocketOptionLevel, SocketOptionName, Stream

### Community 1381 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (7): ChannelX11, bool, byte, Hashtable, int, Socket, String

### Community 1382 - "ASM Server — Server Manager"
Cohesion: 0.16
Nodes (12): byte, SslStatus, AlertDescription, AlertLevel, CompatibilityResult, ContentType, HandshakeType, HashUpdate (+4 more)

### Community 1383 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (6): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, String, Thread

### Community 1384 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (7): FATabStripItem, bool, Control, Image, RectangleF, Size, string

### Community 1385 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmRDPLogViewer, Button, ColumnHeader, IContainer, ListView, Panel, PictureBox, SplitContainer (+4 more)

### Community 1386 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmConfigureDefaults_CPCS, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+4 more)

### Community 1387 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmCustomcmdConf, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, Label (+4 more)

### Community 1388 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmConfigureDefaults_CPCS, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, ImageList (+4 more)

### Community 1389 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmCustomcmdConf, Button, CheckBox, ColumnHeader, ComboBox, GroupBox, IContainer, Label (+4 more)

### Community 1390 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmAddServerDCOM, Button, CheckBox, ColumnHeader, GroupBox, IContainer, ImageList, Label (+4 more)

### Community 1391 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmAddServerServices, Button, CheckBox, ColumnHeader, GroupBox, IContainer, ImageList, Label (+4 more)

### Community 1392 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (7): frmChangePasswordWindwosRDP, Boolean, EventArgs, IMsTscAxEvents_OnDisconnectedEvent, IMsTscAxEvents_OnFatalErrorEvent, Int32, String

### Community 1393 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmReportManager, Button, ColumnHeader, ComboBox, DateTimePicker, GroupBox, IContainer, ImageList (+4 more)

### Community 1394 - "ASM Server — Server Manager"
Cohesion: 0.21
Nodes (8): UploadFile_UserServerMapping, ListView, ListViewItem, UserServerMapping, Boolean, int, long, string

### Community 1395 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frm_UserRoleBulkExcel, Button, ColumnHeader, IContainer, Label, ListView, OpenFileDialog, Panel (+4 more)

### Community 1396 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmServicesQuickSearch_Management, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, ListView (+4 more)

### Community 1397 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmServicesQuickSearch_Modify_Param, Button, CheckBox, ComboBox, DataGridView, DataGridViewTextBoxColumn, GroupBox, IContainer (+4 more)

### Community 1398 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmUserRoleManagement, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, ListView (+4 more)

### Community 1399 - "ASM Server — Server Manager"
Cohesion: 0.13
Nodes (12): frmViewPasswordV2, Button, CheckBox, ComboBox, DateTimePicker, ErrorProvider, GroupBox, IContainer (+4 more)

### Community 1400 - "ASM Server — Pkcs11Interop"
Cohesion: 0.14
Nodes (8): ObjectHandleFactory, ObjectHandleFactory, ObjectHandleFactory, ObjectHandleFactory, IObjectHandle, IObjectHandleFactory, IObjectHandle, ObjectHandleFactory

### Community 1401 - "Common — .PIMUD"
Cohesion: 0.20
Nodes (6): DB2, DB2DBConnection, Boolean, DataTable, DB2Connection, String

### Community 1402 - "Common — .User Controls"
Cohesion: 0.14
Nodes (11): AnimationFlags, MINMAXINFO, NativeMethods, Control, DllImport, HandleRef, int, IntPtr (+3 more)

### Community 1403 - "Common — SLPF"
Cohesion: 0.16
Nodes (5): Socket, Sock, SocketOptionLevel, SocketOptionName, Stream

### Community 1404 - "Common — SLPF"
Cohesion: 0.17
Nodes (7): ChannelX11, bool, byte, Hashtable, int, Socket, String

### Community 1405 - "Common — SLPF"
Cohesion: 0.16
Nodes (12): byte, SslStatus, AlertDescription, AlertLevel, CompatibilityResult, ContentType, HandshakeType, HashUpdate (+4 more)

### Community 1406 - "Common — SPlease Wait Control"
Cohesion: 0.22
Nodes (6): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, String, Thread

### Community 1407 - "Common — Tab Strip"
Cohesion: 0.13
Nodes (7): FATabStripItem, bool, Control, Image, RectangleF, Size, string

### Community 1408 - "Services — Alert Service"
Cohesion: 0.18
Nodes (9): MsalHttpClientFactory, OfficeEmailService, dynamic, HttpClient, Message, string, Task, ProxySettings (+1 more)

### Community 1409 - "Services — Cloud File Uploader"
Cohesion: 0.18
Nodes (6): ProxyARCOSWebDT, ARCOSWebDT, DataSet, Hashtable, ILog, string

### Community 1410 - "Services — Desk Insight"
Cohesion: 0.23
Nodes (9): DateTime, DllImport, IntPtr, StringBuilder, UIntPtr, RegistryHelper, RegistryUtils, FILETIME (+1 more)

### Community 1411 - "Services — Desk Insight"
Cohesion: 0.16
Nodes (8): Lazy, LogType, Logger, LogType, string, SystemDetails, PackageExtraction, KeepAlive

### Community 1412 - "Services — Folder Sync Service"
Cohesion: 0.13
Nodes (12): frmDetail, Button, CheckBox, FolderBrowserDialog, GroupBox, IContainer, Label, NumericUpDown (+4 more)

### Community 1413 - "Services — Migrate Data Utility"
Cohesion: 0.22
Nodes (6): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, String, Thread

### Community 1414 - "Services — Migrate Data Utility"
Cohesion: 0.15
Nodes (9): Assembly, Boolean, Dictionary, Stream, EmbeddedAssembly, Assembly, ResolveEventArgs, STAThread (+1 more)

### Community 1415 - "Services — Migrate Data Utility"
Cohesion: 0.13
Nodes (12): Button, CheckBox, ComboBox, DataGridView, GroupBox, IContainer, Label, Panel (+4 more)

### Community 1416 - "Services — Perf Mon IT"
Cohesion: 0.22
Nodes (6): ARCOSPerfMonITService, Boolean, EventArgs, Exception, Timer, EventLogEntryType

### Community 1417 - "Services — Provisioning Service"
Cohesion: 0.20
Nodes (9): CpuUsage, UsageDetail, bool, DllImport, dynamic, ILog, int, MarshalAs (+1 more)

### Community 1418 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (5): Socket, Sock, SocketOptionLevel, SocketOptionName, Stream

### Community 1419 - "Services — Schedule Password Change"
Cohesion: 0.17
Nodes (7): ChannelX11, bool, byte, Hashtable, int, Socket, String

### Community 1420 - "Services — Schedule Password Change"
Cohesion: 0.19
Nodes (8): bool, CipherMode, ICryptoTransform, int, KeySizes, PaddingMode, RijndaelManaged, RijndaelCryptoServiceProvider

### Community 1421 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (12): byte, SslStatus, AlertDescription, AlertLevel, CompatibilityResult, ContentType, HandshakeType, HashUpdate (+4 more)

### Community 1422 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (5): Socket, Sock, SocketOptionLevel, SocketOptionName, Stream

### Community 1423 - "Services — Schedule Password Change"
Cohesion: 0.17
Nodes (7): ChannelX11, bool, byte, Hashtable, int, Socket, String

### Community 1424 - "Services — Schedule Password Change"
Cohesion: 0.19
Nodes (8): bool, CipherMode, ICryptoTransform, int, KeySizes, PaddingMode, RijndaelManaged, RijndaelCryptoServiceProvider

### Community 1425 - "Services — Schedule Password Change"
Cohesion: 0.16
Nodes (12): byte, SslStatus, AlertDescription, AlertLevel, CompatibilityResult, ContentType, HandshakeType, HashUpdate (+4 more)

### Community 1426 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (7): frmMain, IContainer, Program, UserActivity, IContainer, ARCOSUserActivity, ARCOSFileWatcher

### Community 1427 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (6): frmPleaseWait, Boolean, EventArgs, FormClosingEventArgs, String, Thread

### Community 1428 - "Services — TSPlugin Service"
Cohesion: 0.13
Nodes (7): FATabStripItem, bool, Control, Image, RectangleF, Size, string

### Community 1429 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (9): bool, double, long, Thread, MicroStopwatch, MicroTimer, MicroTimerEventArgs, MicroLibrary (+1 more)

### Community 1430 - "Services — TSPlugin Service"
Cohesion: 0.16
Nodes (5): Socket, Sock, SocketOptionLevel, SocketOptionName, Stream

### Community 1431 - "Services — TSPlugin Service"
Cohesion: 0.17
Nodes (7): ChannelX11, bool, byte, Hashtable, int, Socket, String

### Community 1432 - "Services — TSPlugin Service"
Cohesion: 0.19
Nodes (8): bool, CipherMode, ICryptoTransform, int, KeySizes, PaddingMode, RijndaelManaged, RijndaelCryptoServiceProvider

### Community 1433 - "Services — TSPlugin Service"
Cohesion: 0.16
Nodes (12): byte, SslStatus, AlertDescription, AlertLevel, CompatibilityResult, ContentType, HandshakeType, HashUpdate (+4 more)

### Community 1434 - "Services — Z POC"
Cohesion: 0.29
Nodes (4): DataTable, MigrateDB, Program, MigrateDB

### Community 1435 - "Services — Z POC"
Cohesion: 0.30
Nodes (4): Program, DataTable, XWDMigrate, XWD_Migrate

### Community 1436 - "Datum Bridge"
Cohesion: 0.24
Nodes (6): MSSQLDatabase, DataTable, IDataParameter, IDbCommand, IDbConnection, IDbDataAdapter

### Community 1437 - "Datum Bridge Client"
Cohesion: 0.24
Nodes (6): MSSQLDatabase, DataTable, IDataParameter, IDbCommand, IDbConnection, IDbDataAdapter

### Community 1438 - "Database SQL — Arcon Pam"
Cohesion: 0.13
Nodes (3): dbo].[sso_arcos_file_download_name_format_master, sso_ApiRequestResponseDetails, sso_file_server_detail

### Community 1439 - "ACM Client — Sshkey SFTP"
Cohesion: 0.22
Nodes (5): PropertiesFormCompro, bool, EventArgs, SftpFilePermissions, string

### Community 1440 - "ACM Client — DQS"
Cohesion: 0.16
Nodes (5): SYBASEDBClient, IDbCommand, IDbConnection, IDbDataAdapter, AseConnection

### Community 1441 - "ACM Client — DQS"
Cohesion: 0.14
Nodes (11): Button, ColumnHeader, IContainer, Label, ListView, Panel, SplitContainer, TableLayoutPanel (+3 more)

### Community 1442 - "ACM Client — Framework CM"
Cohesion: 0.21
Nodes (9): Export, ExportFormat, DataGridView, DataSet, DataTable, HttpResponse, ListView, string (+1 more)

### Community 1443 - "ACM Client — Framework CM"
Cohesion: 0.18
Nodes (9): frmErrorMessage, Action, DllImport, EventArgs, FormClosingEventArgs, int, IntPtr, Timer (+1 more)

### Community 1444 - "ACM Client — SFTPTeminal"
Cohesion: 0.22
Nodes (5): bool, EventArgs, SftpFilePermissions, string, PropertiesForm

### Community 1445 - "ACM Client — SFTPTeminal"
Cohesion: 0.22
Nodes (5): bool, EventArgs, SftpFilePermissions, string, PropertiesFormCompro

### Community 1446 - "ACM Client — SSHTerminal"
Cohesion: 0.14
Nodes (11): Button, ColumnHeader, IContainer, Label, ListView, Panel, SplitContainer, TableLayoutPanel (+3 more)

### Community 1447 - "ACM Client — SSHTerminal"
Cohesion: 0.27
Nodes (5): Util, DllImport, Form, int, IntPtr

### Community 1448 - "ACM Client — Web Browser"
Cohesion: 0.19
Nodes (11): IOleCommandTarget, NativeMethods, OLECMD, OLECMDEXECOPT, OLECMDF, OLECMDID, Guid, int (+3 more)

### Community 1449 - "ACM Client — Web Browserv35"
Cohesion: 0.14
Nodes (12): frmARCOSWebBrowserGecko, Button, ContextMenuStrip, GeckoWebBrowser, IContainer, ImageList, Panel, TabControl (+4 more)

### Community 1450 - "ACM Common — .Smtp Send"
Cohesion: 0.19
Nodes (6): CertTextExtractor, CertValidator, bool, EventArgs, string, X509Certificate2

### Community 1451 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): frmProfileCreation, ACMenuControl, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label (+5 more)

### Community 1452 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): frmUpdateProfile, ACMenuControl, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label (+5 more)

### Community 1453 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): frmAssignProfile, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton (+5 more)

### Community 1454 - "ACMO Web — Client Manager"
Cohesion: 0.27
Nodes (4): EncryptionDecryption, EncryptionDecryption_F, Byte, EncryptionDecryption_F

### Community 1455 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): frmGatewayConfigurationDetails, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton (+5 more)

### Community 1456 - "ACMO Web — Client Manager"
Cohesion: 0.14
Nodes (13): frmImageLogConfiguration, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton (+5 more)

### Community 1457 - "ACMO Web — Client Manager"
Cohesion: 0.30
Nodes (12): Stream(), cleanup(), listenerCount(), onclose(), ondata(), ondrain(), onerror(), onfinish() (+4 more)

### Community 1458 - "ACMO Web — Client Manager"
Cohesion: 0.21
Nodes (14): BrotliDecompress(), BrotliDecompressedSize(), CopyUncompressedBlockToOutput(), DecodeBlockType(), DecodeContextMap(), DecodeMetaBlockLength(), DecodeVarLenUint8(), DecodeWindowBits() (+6 more)

### Community 1459 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (13): clockwise(), computeAutoPlacement(), enableEventListeners(), findIndex(), flip(), getArea(), getOppositePlacement(), getOppositeVariation() (+5 more)

### Community 1460 - "LDAPAuthenticator"
Cohesion: 0.15
Nodes (8): AsyncTask, AsyncTask, int, IPEndPoint, string, uint, RadiusClient, Radius

### Community 1461 - "ACMO Web — Common Functions"
Cohesion: 0.27
Nodes (5): HSMCommonFunctionACMO, DataTable, List, HSMDataFunctionsACMO, DataTable

### Community 1462 - "ACMO Web — Portal"
Cohesion: 0.16
Nodes (14): absRound(), add_subtract__addSubtract(), daysInMonth(), get_set__get(), get_set__set(), getDateOffset(), getDaysInMonth(), getSetMonth() (+6 more)

### Community 1463 - "ACMO Web — Portal"
Cohesion: 0.19
Nodes (14): createUTCDate(), dayOfYearFromWeeks(), daysInYear(), firstWeekOffset(), getIsLeapYear(), getISOWeeksInYear(), getSetISOWeek(), getSetWeekYearHelper() (+6 more)

### Community 1464 - "ACMO Web — Portal"
Cohesion: 0.13
Nodes (11): Site, EventArgs, Site, ContentPlaceHolder, HtmlForm, HtmlHead, Image, Panel (+3 more)

### Community 1465 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (6): RadiusClient, ArrayList, bool, byte, int, string

### Community 1466 - "ASM Server — Server Manager"
Cohesion: 0.21
Nodes (9): Export, ExportFormat, DataGridView, DataSet, DataTable, HttpResponse, ListView, string (+1 more)

### Community 1467 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): frmARCONSTerminalEmulator, Button, ComboBox, GroupBox, IContainer, Label, Panel, RadioButton (+3 more)

### Community 1468 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): frmServicesMultipleInterfaces, Button, ColumnHeader, GroupBox, IContainer, ImageList, Label, LinkLabel (+3 more)

### Community 1469 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): frmPasswordExpiryReminder, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, Label (+3 more)

### Community 1470 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): frmPasswordManagerGroupAuth, Button, CheckBox, ComboBox, ErrorProvider, GroupBox, IContainer, Label (+3 more)

### Community 1471 - "ASM Server — Server Manager"
Cohesion: 0.14
Nodes (11): frmServersDMZSupport, Button, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, ListView (+3 more)

### Community 1472 - "Common — SExport Utility"
Cohesion: 0.21
Nodes (9): Export, ExportFormat, DataGridView, DataSet, DataTable, HttpResponse, ListView, string (+1 more)

### Community 1473 - "Common — Reference Details"
Cohesion: 0.14
Nodes (9): frmReferenceDetailsCF, Button, ComboBox, GroupBox, IContainer, Label, Panel, TextBox (+1 more)

### Community 1474 - "Services — Active Directory Insight"
Cohesion: 0.33
Nodes (6): ARCONActiveDirectoryInsight, Boolean, DirectoryEntry, EventArgs, String, Timer

### Community 1475 - "Services — Desk Insight"
Cohesion: 0.14
Nodes (11): frmUSBElevationRequest, Button, CheckedListBox, ComboBox, DateTimePicker, GroupBox, IContainer, Label (+3 more)

### Community 1476 - "Services — Desk Insight"
Cohesion: 0.20
Nodes (8): ProcessEvents, EventArrivedEventArgs, ManagementEventWatcher, ProcessHelper, DllImport, int, IntPtr, UInt32

### Community 1477 - "Services — Folder Sync Service"
Cohesion: 0.20
Nodes (7): Assembly, bool, List, string, ComponentLibrary, Assembly, GeneralLib

### Community 1478 - "Services — Privilege User Discovery"
Cohesion: 0.27
Nodes (5): HSMCommonFunctionUser, DataTable, List, HSMDataFunctionsUser, DataTable

### Community 1479 - "Services — Script Scheduler"
Cohesion: 0.20
Nodes (8): bool, DataSet, DataTable, Hashtable, Int32, object, String, ServerSessionLogger

### Community 1480 - "Services — TSPlugin Service"
Cohesion: 0.21
Nodes (9): Export, ExportFormat, DataGridView, DataSet, DataTable, HttpResponse, ListView, string (+1 more)

### Community 1481 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (4): List, PreserveSig, StringBuilder, UInt32

### Community 1482 - "Services — TSPlugin Service"
Cohesion: 0.14
Nodes (7): EventArgs, STAThread, IContainer, frmIApp, frmIApp, Program, IApp

### Community 1483 - "LDAPAuthenticator"
Cohesion: 0.25
Nodes (6): RadiusClient, ArrayList, bool, byte, int, string

### Community 1484 - "Database SQL — Arcon Pam"
Cohesion: 0.14
Nodes (3): dbo].[sso_Password_Expiry_Alert, dbo].[ssR_Users_Services_RequestTrack, tmp1

### Community 1488 - "Offline MultiTab — Windows Service"
Cohesion: 0.18
Nodes (7): ARCOSEncryptionDecryption, DateTime, Decryption, Encryption, int, String, EncryptDecrypt

### Community 1489 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (10): ANIMATIONINFO, ANIMATIONINFO, SPIF, XPAppearance, DllImport, int, MarshalAs, uint (+2 more)

### Community 1490 - "ACM Client — ACMCommon Functions"
Cohesion: 0.22
Nodes (6): Tests, Int32, SetUp, String, Test, TestCase

### Community 1491 - "ACM Client — RStream Client"
Cohesion: 0.19
Nodes (7): frmConnectForm, bool, Boolean, DoWorkEventArgs, EventArgs, int, ProgressChangedEventArgs

### Community 1492 - "ACM Client — DQS"
Cohesion: 0.19
Nodes (4): DB2DBClient, IDbCommand, IDbConnection, IDbDataAdapter

### Community 1493 - "ACM Client — DQS"
Cohesion: 0.15
Nodes (10): ExportOption, Button, CheckBox, ComboBox, GroupBox, IContainer, ImageList, PictureBox (+2 more)

### Community 1494 - "ACM Client — DQS"
Cohesion: 0.19
Nodes (6): ModifyColumnForm, bool, DataSet, EventArgs, Message, string

### Community 1495 - "ACM Client — Framework CM"
Cohesion: 0.21
Nodes (6): SecureShellTunnel, int, List, object, SecureShellChannel, Socket

### Community 1496 - "ACM Client — Framework CM"
Cohesion: 0.21
Nodes (6): SecureShellTunnel, int, List, object, SecureShellChannel, Socket

### Community 1497 - "ACM Client — Arcoss SSMDesktop"
Cohesion: 0.15
Nodes (10): IWin32WindowWrapper, IntPtr, IWin32WindowWrapper, IntPtr, IWin32WindowWrapper, IntPtr, ArcossSSMDesktop.Models, IWin32Window (+2 more)

### Community 1498 - "ACM Client — Framework CM"
Cohesion: 0.15
Nodes (10): frmLogin, Button, ComboBox, ErrorProvider, IContainer, Label, Panel, PictureBox (+2 more)

### Community 1499 - "ACM Client — Framework CM"
Cohesion: 0.19
Nodes (8): frmMSSQLConnectionRetry, Button, IContainer, PictureBox, TextBox, MSSqlDBConnection, SqlConnection, String

### Community 1500 - "ACM Client — Framework CM"
Cohesion: 0.18
Nodes (8): frmPreferenceSelection, Boolean, DialogResult, DrawItemEventArgs, EventArgs, FormClosingEventArgs, String, ToolTip

### Community 1501 - "ACM Client — Framework CM"
Cohesion: 0.21
Nodes (6): frmUserCredentials_Service, bool, Boolean, EventArgs, FormClosingEventArgs, string

### Community 1502 - "ACM Client — Framework CM"
Cohesion: 0.33
Nodes (5): WindowHelper, DllImport, int, IntPtr, Process

### Community 1503 - "ACM Client — SFTPTeminal"
Cohesion: 0.15
Nodes (10): frmSearchFiles, Button, CheckBox, GroupBox, IContainer, Label, LinkLabel, ListView (+2 more)

### Community 1504 - "ACM Client — SSHTerminal"
Cohesion: 0.15
Nodes (11): Main, IContainer, MenuStrip, SaveFileDialog, SshTerminalControl, StatusStrip, ToolStrip, ToolStripButton (+3 more)

### Community 1505 - "ACM Client — VNCTerminal"
Cohesion: 0.17
Nodes (7): LASTINPUTINFO, SessionIdleTime, DllImport, Int32, LASTINPUTINFO, uint, ARCOSVNCTerminal

### Community 1506 - "ACM Client — Web Browser"
Cohesion: 0.15
Nodes (6): BrowserExtendedNavigatingEventArgs, object, string, Uri, UrlContext, CancelEventArgs

### Community 1507 - "ACM Client — Web Browserv35"
Cohesion: 0.33
Nodes (5): UCARCOSWebBrowserOperations, WebBrowserOperationsEventArgs, WebBrowserOperationType, Boolean, EventArgs

### Community 1508 - "ACM Common — .Radius"
Cohesion: 0.28
Nodes (6): RadiusClient, ArrayList, bool, byte, int, string

### Community 1509 - "ACM Common — .User Controls"
Cohesion: 0.21
Nodes (7): AnimationFlags, MINMAXINFO, NativeMethods, int, IntPtr, Point, Size

### Community 1510 - "ACM Common — SLPF"
Cohesion: 0.19
Nodes (6): Err, Out, System, Array, System, Array

### Community 1511 - "ACM Common — SLPF"
Cohesion: 0.15
Nodes (3): KeyPairGenRSA, byte, RSAParameters

### Community 1513 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmATSMapping, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, ListBox (+4 more)

### Community 1514 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmATSUnMapping, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, ListBox (+4 more)

### Community 1515 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmARCOSDashboardPassword, DropDownList, GridView, HiddenField, HtmlForm, Image, Label, LinkButton (+4 more)

### Community 1516 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmARCOSDashboardPerfMonIT, GridView, HiddenField, HtmlForm, HtmlGenericControl, Image, LinkButton, MultiView (+4 more)

### Community 1517 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmARCOSDashboardServerSessions, DropDownList, GridView, HiddenField, HtmlForm, Image, Label, LinkButton (+4 more)

### Community 1518 - "ACMO Web — Client Manager"
Cohesion: 0.23
Nodes (7): frmARCOSMailBox, bool, DataTable, EventArgs, Int32, RepeaterCommandEventArgs, String

### Community 1519 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmDelegation, Button, CheckBox, DropDownList, HtmlGenericControl, Label, LinkButton, MultiView (+4 more)

### Community 1520 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmGatewayServerDetails, Button, CheckBox, HiddenField, HtmlGenericControl, Label, LinkButton, MultiView (+4 more)

### Community 1521 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmPasswordPolicyForSecrets, Button, DropDownList, GridView, HtmlGenericControl, Label, LinkButton, MultiView (+4 more)

### Community 1522 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): ReportDownloads, Button, DropDownList, HiddenField, HtmlAnchor, HtmlGenericControl, Label, LinkButton (+4 more)

### Community 1523 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmSecuredVault, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, HtmlInputCheckBox, HtmlInputHidden (+4 more)

### Community 1524 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): FrmRDPSFileTransferSettings, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, RegularExpressionValidator (+4 more)

### Community 1525 - "ACMO Web — Client Manager"
Cohesion: 0.31
Nodes (3): un, dn(), hn()

### Community 1529 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): SAMLReceiver, Button, DropDownList, HiddenField, HtmlForm, HtmlGenericControl, HtmlImage, HyperLink (+4 more)

### Community 1530 - "ACMO Web — Client Manager"
Cohesion: 0.15
Nodes (12): frmARCONMetadataLogs, Button, DropDownList, HiddenField, HtmlGenericControl, HtmlInputHidden, Label, LinkButton (+4 more)

### Community 1531 - "ACMO Web — Portal"
Cohesion: 0.15
Nodes (12): frmUserSelfRegistration, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, ListBox (+4 more)

### Community 1532 - "ACMO Web — Portal"
Cohesion: 0.31
Nodes (12): p(), A(), B(), C(), E(), G(), H(), I() (+4 more)

### Community 1533 - "ACMO Web — Portal"
Cohesion: 0.15
Nodes (13): addRegexToken(), expandFormat(), formatMoment(), getSet(), invalidDate(), isFunction(), locale_calendar__calendar(), locale_set__set() (+5 more)

### Community 1534 - "ACMO Web — Portal"
Cohesion: 0.26
Nodes (11): v(), dateGenerator(), floorInBase(), formatDate(), init(), makeUtcWrapper(), dateGenerator(), floorInBase() (+3 more)

### Community 1535 - "ACMO Web — Portal"
Cohesion: 0.46
Nodes (12): a(), b(), c(), d(), e(), f(), g(), h() (+4 more)

### Community 1536 - "ACMO Web — Portal"
Cohesion: 0.37
Nodes (11): a(), b(), c(), d(), e(), f(), g(), h() (+3 more)

### Community 1537 - "ACMO Web — Web Services"
Cohesion: 0.15
Nodes (7): ARCOSIBUDAA, IsUDAAValidatedCompletedEventArgs, bool, object, SendOrPostCallback, SoapDocumentMethodAttribute, ARCOSWebServices.ARCOSValidateUDAA

### Community 1538 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (3): KeyPairGenRSA, byte, RSAParameters

### Community 1539 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmCustomCommandConfigurationpopup, Button, CheckBox, ColumnHeader, GroupBox, IContainer, Label, ListView (+2 more)

### Community 1540 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmVPNServers_VIP, Button, CheckBox, ColumnHeader, GroupBox, IContainer, ImageList, Label (+2 more)

### Community 1541 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmCustomCommandConfigurationpopup, Button, CheckBox, ColumnHeader, GroupBox, IContainer, Label, ListView (+2 more)

### Community 1542 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmVPNServers_VIP, Button, CheckBox, ColumnHeader, GroupBox, IContainer, ImageList, Label (+2 more)

### Community 1543 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmMakerChecker, Button, CheckBox, ColumnHeader, GroupBox, IContainer, ImageList, ListView (+2 more)

### Community 1544 - "ASM Server — Server Manager"
Cohesion: 0.24
Nodes (6): frmServicesQuickSearch_Management, DataTable, EventArgs, ListViewItem, MouseEventArgs, String

### Community 1545 - "ASM Server — Server Manager"
Cohesion: 0.15
Nodes (10): frmUserRoleBulk, Button, ColumnHeader, DataGridView, GroupBox, IContainer, LinkLabel, ListView (+2 more)

### Community 1546 - "Common — .Radius"
Cohesion: 0.28
Nodes (6): RadiusClient, ArrayList, bool, byte, int, string

### Community 1548 - "Common — SLPF"
Cohesion: 0.15
Nodes (3): KeyPairGenRSA, byte, RSAParameters

### Community 1549 - "Services — Cloud File Uploader"
Cohesion: 0.18
Nodes (5): APIHelper, DateTime, ILog, MemoryCache, string

### Community 1550 - "Services — Cloud File Uploader"
Cohesion: 0.23
Nodes (7): GCPUploadManager, BlobContainerClient, ILog, StorageClient, string, Task, Google

### Community 1551 - "Services — Data Sync"
Cohesion: 0.17
Nodes (9): AccessToken, string, string, RestrictedArcosClient, Token, DateTime, string, ARCOSSynDBCommonFunctionsService.LocalCommonFunctions (+1 more)

### Community 1552 - "Services — DBSync Service"
Cohesion: 0.15
Nodes (9): Settings, Button, CheckBox, ComboBox, GroupBox, IContainer, Label, TextBox (+1 more)

### Community 1553 - "Services — DBSync Service"
Cohesion: 0.15
Nodes (11): frmMain, Button, CheckBox, ComboBox, GroupBox, IContainer, ImageList, Label (+3 more)

### Community 1554 - "Services — Desk Insight"
Cohesion: 0.27
Nodes (5): ProjectInstaller, EventLog, EventLogEntryType, IDictionary, String

### Community 1555 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (10): frmARCONRSSMain, Button, GroupBox, IContainer, Label, RadioButton, StatusStrip, TextBox (+2 more)

### Community 1556 - "Services — Desk Insight"
Cohesion: 0.18
Nodes (9): Resources, CultureInfo, ResourceManager, Settings, Resources, CultureInfo, ResourceManager, Settings (+1 more)

### Community 1557 - "Services — Folder Sync Service"
Cohesion: 0.28
Nodes (6): DllImport, int, IntPtr, String, WindowsImpersonationContext, ImpersonateUser

### Community 1558 - "Services — Migrate Data Utility"
Cohesion: 0.15
Nodes (9): About, About, Button, IContainer, Label, PictureBox, TableLayoutPanel, TextBox (+1 more)

### Community 1559 - "Services — Passworde Envelope Manager"
Cohesion: 0.19
Nodes (5): frmSplashScreen, Boolean, EventArgs, FormClosingEventArgs, Int32

### Community 1560 - "Services — Provisioning Scheduler"
Cohesion: 0.24
Nodes (3): Boolean, String, IPMACManager

### Community 1562 - "Services — Schedule Password Change"
Cohesion: 0.15
Nodes (3): KeyPairGenRSA, byte, RSAParameters

### Community 1564 - "Services — TSPlugin Service"
Cohesion: 0.27
Nodes (12): ServiceReferenceLogParams, UserAndServerRequestLogsParams, ViewARCOSLogParams, ViewDBALogParams, ViewPasswordChangeLogParams, ViewProcessLogParams, ViewServiceAccessLogParams, ViewServiceLogParams (+4 more)

### Community 1565 - "Services — TSPlugin Service"
Cohesion: 0.21
Nodes (6): SecureShellTunnel, int, List, object, SecureShellChannel, Socket

### Community 1567 - "Services — TSPlugin Service"
Cohesion: 0.15
Nodes (3): KeyPairGenRSA, byte, RSAParameters

### Community 1569 - "MultiTab — src"
Cohesion: 0.33
Nodes (7): EventType, IdleMonitor, Event, EventHandler, Node, Scene, Timeline

### Community 1570 - "Offline MultiTab — Offline API"
Cohesion: 0.19
Nodes (7): IApplicationBuilder, IServiceCollection, IWebHostEnvironment, IConfiguration, ILoggerFactory, String, Startup

### Community 1571 - "ACM Client — RStream Client"
Cohesion: 0.18
Nodes (7): frmConnectFormInternet, bool, Boolean, DoWorkEventArgs, EventArgs, int, ProgressChangedEventArgs

### Community 1572 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.17
Nodes (9): Button, ColumnHeader, IContainer, Label, ListView, Panel, ProgressBar, TextBox (+1 more)

### Community 1573 - "ACM Client — Sshkey SFTP"
Cohesion: 0.27
Nodes (5): PropertiesForm, bool, EventArgs, SftpFilePermissions, string

### Community 1574 - "ACM Client — Sshkey SFTP"
Cohesion: 0.17
Nodes (9): Setting, Button, CheckBox, GroupBox, IContainer, Label, RadioButton, TextBox (+1 more)

### Community 1575 - "ACM Client — App Exe"
Cohesion: 0.17
Nodes (9): frmWinAppOptions, Button, CheckBox, ComboBox, IContainer, Label, Panel, PictureBox (+1 more)

### Community 1576 - "ACM Client — DQS"
Cohesion: 0.26
Nodes (4): ExportOption, EventArgs, int, Message

### Community 1577 - "ACM Client — DQS"
Cohesion: 0.17
Nodes (9): HeaderFormates, Button, ComboBox, IContainer, Label, ListBox, PictureBox, RadioButton (+1 more)

### Community 1579 - "ACM Client — DQS"
Cohesion: 0.17
Nodes (9): ObjectExplorer, Button, ComboBox, ContextMenuStrip, IContainer, ImageList, MenuStrip, ToolStripMenuItem (+1 more)

### Community 1580 - "ACM Client — DQS"
Cohesion: 0.17
Nodes (9): AddNewTableForm, Button, DataGridView, DataGridViewCheckBoxColumn, DataGridViewTextBoxColumn, IContainer, Label, TextBox (+1 more)

### Community 1581 - "ACM Client — Framework CM"
Cohesion: 0.32
Nodes (6): IARCOSSLS, Boolean, Byte, DataSet, String, Uri

### Community 1582 - "Services — Framework CM"
Cohesion: 0.23
Nodes (9): WindowsOSBitType, WindowsOSVersionType, WinOSInfo, WindowsOSBitType, WindowsOSVersionType, WinOSInfo, WindowsOSBitType, WindowsOSVersionType (+1 more)

### Community 1583 - "ACM Client — RDPTerminal"
Cohesion: 0.17
Nodes (10): frmRDPControlV2, ApplicationIdle, ContextMenuStrip, DebuggerNonUserCode, DebuggerStepThrough, IContainer, Label, Panel (+2 more)

### Community 1584 - "ACM Client — SSHTerminal"
Cohesion: 0.21
Nodes (6): Button, ComboBox, Container, EventArgs, Label, ChangeLogDialog

### Community 1585 - "ACM Client — SSHTerminal"
Cohesion: 0.27
Nodes (5): bool, EventArgs, SftpFilePermissions, string, PropertiesForm

### Community 1586 - "ACM Client — SSHTerminal"
Cohesion: 0.38
Nodes (4): frmSCP, EventArgs, Object, string

### Community 1587 - "ACM Common — .User Controls"
Cohesion: 0.18
Nodes (7): PopupComboBox, Control, DateTime, Message, ObjectCollection, SecurityPermission, ToolStripDropDownClosedEventArgs

### Community 1588 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (5): UIAutomationData, frmRPAJsonUpload, bool, EventArgs, string

### Community 1589 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmARCONApiLogs, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LogMenuControl, Repeater (+3 more)

### Community 1590 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmAddApplication_PEDM, Button, CheckBox, FileUpload, HiddenField, HtmlButton, HtmlGenericControl, HtmlInputHidden (+3 more)

### Community 1591 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmArsimCreateServerProfile, ACMenuControl, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label (+3 more)

### Community 1592 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmAPIDefaultServiceCreationConfig, Button, CheckBox, HiddenField, HtmlGenericControl, HtmlSelect, Label, LinkButton (+3 more)

### Community 1593 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmAPIServiceConfiguration, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton (+3 more)

### Community 1594 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmCollaborationLog, GridView, HiddenField, HtmlForm, HtmlGenericControl, HtmlHead, Image, Label (+3 more)

### Community 1595 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmGatewayAssignDetails, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, MultiView (+3 more)

### Community 1596 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmUARLog, GridView, HiddenField, HtmlForm, HtmlGenericControl, HtmlHead, Image, Label (+3 more)

### Community 1597 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmUserList, Button, HiddenField, HtmlGenericControl, Label, LinkButton, ListBox, RegularExpressionValidator (+3 more)

### Community 1598 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmNattedIpSettings, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton (+3 more)

### Community 1599 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmRDPSlist, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, Repeater (+3 more)

### Community 1600 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): frmUnattendedaccesslist, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, Repeater (+3 more)

### Community 1603 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): UCViewAccessLogs, Button, CheckBox, DropDownList, HiddenField, HtmlGenericControl, Label, Repeater (+3 more)

### Community 1604 - "ACMO Web — Client Manager"
Cohesion: 0.17
Nodes (11): UCUserPasswordChange, Button, HiddenField, HtmlButton, HtmlGenericControl, Image, Label, Panel (+3 more)

### Community 1605 - "ACMO Web — Common Functions"
Cohesion: 0.17
Nodes (11): Compression, Login, NasPortType, Protocol, RadiusAttributeType, RadiusCode, Routing, Service (+3 more)

### Community 1606 - "ACMO Web — Portal"
Cohesion: 0.27
Nodes (4): frmServiceOnBoarding, DataTable, EventArgs, String

### Community 1607 - "ASM Server — Server Manager"
Cohesion: 0.24
Nodes (5): frmARCOSMailBox, DrawListViewColumnHeaderEventArgs, DrawListViewSubItemEventArgs, EventArgs, MouseEventArgs

### Community 1608 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmARCOSMailBox, ColumnHeader, IContainer, ImageList, ListView, TabControl, TabPage, ToolStrip (+1 more)

### Community 1609 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (6): frmARCONSWebBrowser, EventArgs, String, WebBrowserDocumentCompletedEventArgs, WebBrowserNavigatedEventArgs, WebBrowserNavigatingEventArgs

### Community 1610 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmViewPassword, Button, ComboBox, ErrorProvider, GroupBox, IContainer, Label, Panel (+1 more)

### Community 1611 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmARCOSApplicationLogs, Button, DataGridView, DateTimePicker, GroupBox, IContainer, ImageList, Label (+1 more)

### Community 1612 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmChangePasswordManually, Button, ComboBox, GroupBox, IContainer, Label, Panel, RadioButton (+1 more)

### Community 1613 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmLogin, Button, ComboBox, ErrorProvider, IContainer, Label, Panel, PictureBox (+1 more)

### Community 1614 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmLoginOtherDomain, Button, CheckBox, ErrorProvider, GroupBox, IContainer, Label, Panel (+1 more)

### Community 1615 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): frmPasswordEvelopeReprintVerify, Button, ComboBox, ErrorProvider, GroupBox, IContainer, Label, Panel (+1 more)

### Community 1616 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (9): FrmUDFKey, Button, CheckBox, ComboBox, GroupBox, IContainer, Label, RadioButton (+1 more)

### Community 1617 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (10): frmPrivilegedUserDiscovery_Popup, Button, ColumnHeader, GroupBox, IContainer, ImageList, ListView, Panel (+2 more)

### Community 1618 - "ASM Server — Server Manager"
Cohesion: 0.17
Nodes (10): frmServiceDiscovery_Popup, Button, ColumnHeader, GroupBox, IContainer, ImageList, ListView, Panel (+2 more)

### Community 1619 - "Common — .User Controls"
Cohesion: 0.18
Nodes (7): PopupComboBox, Control, DateTime, Message, ObjectCollection, SecurityPermission, ToolStripDropDownClosedEventArgs

### Community 1620 - "Common — Enitity Objects"
Cohesion: 0.23
Nodes (9): ARCOSWorkflowActionXMLFormat, ARCOSWorkflowDetails, Boolean, DataTable, DateTime, int, Int32, long (+1 more)

### Community 1621 - "Services — Cloud File Uploader"
Cohesion: 0.33
Nodes (7): APIConfig, CloudFileUploaderDetails, CloudFileUploaderIni, CommonManager, DataTable, ILog, string

### Community 1622 - "Services — Cloud File Uploader"
Cohesion: 0.21
Nodes (8): APIAuthToken, UserInfoToken, DateTime, AccessToken, APITokenInput, AuthHelper, ILog, string

### Community 1623 - "Services — Desk Insight"
Cohesion: 0.15
Nodes (6): ARCONDeskInsightService, IContainer, ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller

### Community 1624 - "Services — Desk Insight"
Cohesion: 0.30
Nodes (6): Updater, Boolean, ServiceController, String, WebProxy, ARCONDeskInsightUpdater

### Community 1625 - "Services — Folder Sync Service"
Cohesion: 0.17
Nodes (9): frmMain, Button, ColumnHeader, IContainer, Label, ListView, PictureBox, TabControl (+1 more)

### Community 1626 - "Services — Migrate Data Utility"
Cohesion: 0.29
Nodes (5): Boolean, Exception, SqlConnection, string, OpenConnections

### Community 1627 - "Services — Provisioning Scheduler"
Cohesion: 0.29
Nodes (11): List, string, FormBuilderData, FormBuilderDataDt, FormBuilderJson, MappingDatas, MappingList, ProvisioningData (+3 more)

### Community 1628 - "Services — Schedule Password Change"
Cohesion: 0.26
Nodes (7): ARCOSSPCService, Boolean, Int32, Program, DllImport, int, IntPtr

### Community 1629 - "Services — Windows Vaulting Service"
Cohesion: 0.17
Nodes (5): IDictionary, ProjectInstaller, IContainer, WindowsListenerInstaller, WindowsVaultingService

### Community 1630 - "Datum Bridge — NUnit Database"
Cohesion: 0.21
Nodes (6): DataWorker, Program, UserManager, Program, UserManager, NUnitDatabase

### Community 1631 - "Database SQL — Arcon Pam"
Cohesion: 0.17
Nodes (3): dbo].[sso_secret_types, OutputTbl, tmp1

### Community 1632 - "MultiTab — src"
Cohesion: 0.17
Nodes (10): Program, APP_CALCULATOR, APP_CAPTURE, APP_NOTEPAD, APP_REMOTE_DESK, APP_VNC, APP_WINSCP, DEFAULT_APP_KEYGEN (+2 more)

### Community 1633 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.25
Nodes (5): bool, EventArgs, Message, string, FileOrFolderRename

### Community 1634 - "ACM Client — Sshkey SFTP"
Cohesion: 0.18
Nodes (8): LoginInfo, bool, int, Process, ProxyHttpConnectAuthMethod, ProxyType, string, TraceEventType

### Community 1635 - "ACM Client — DQS"
Cohesion: 0.24
Nodes (5): AddColumnForm, DataSet, EventArgs, Message, string

### Community 1636 - "ACM Client — DQS"
Cohesion: 0.18
Nodes (8): EditTableForm, Button, DataGridView, DataGridViewCheckBoxColumn, DataGridViewTextBoxColumn, IContainer, Label, TextBox

### Community 1637 - "ACM Client — Oracle Query"
Cohesion: 0.18
Nodes (8): frmOracleClientOptions, Button, ComboBox, IContainer, Label, Panel, PictureBox, TextBox

### Community 1638 - "ACM Client — Script Manager"
Cohesion: 0.18
Nodes (8): frmReferenceDetails, Button, ComboBox, GroupBox, IContainer, Label, Panel, TextBox

### Community 1639 - "ACM Client — SFTPTeminal"
Cohesion: 0.18
Nodes (3): FileSystemProgressEventArgs, FileSystemProgressEventArgs, FileSystemProgressEventArgs

### Community 1640 - "ACM Client — SSHTerminal"
Cohesion: 0.20
Nodes (6): bool, Button, Container, EventArgs, TextBox, InputBox

### Community 1641 - "ACM Client — SSHTerminal"
Cohesion: 0.20
Nodes (7): Button, CheckBox, Container, Icon, Label, PaintEventArgs, WarningWithDisableOption

### Community 1642 - "ACM Client — SSHTerminal"
Cohesion: 0.18
Nodes (8): Button, CheckBox, ComboBox, IContainer, Label, RadioButton, TextBox, SynchronizeFolders

### Community 1643 - "ACM Client — SSHTerminal"
Cohesion: 0.18
Nodes (9): frmSCP, Button, Container, DebuggerNonUserCode, DebuggerStepThrough, Label, TabControl, TabPage (+1 more)

### Community 1644 - "ACM Client — VNCTerminal"
Cohesion: 0.24
Nodes (5): Image, Point, Rectangle, Size, VncClippedDesktopPolicy

### Community 1645 - "ACM Client — VNCTerminal"
Cohesion: 0.24
Nodes (5): Image, Point, Rectangle, Size, VncDesignModeDesktopPolicy

### Community 1646 - "ACM Common — SExport Utility"
Cohesion: 0.27
Nodes (7): Export, ExportFormat, DataSet, HttpResponse, string, XmlTextWriter, ExportFormat

### Community 1647 - "ACM Common — SLPF"
Cohesion: 0.20
Nodes (5): HMACMD596, byte, CryptoStream, int, String

### Community 1648 - "ACM Common — SLPF"
Cohesion: 0.22
Nodes (5): HMACSHA1, byte, CryptoStream, int, String

### Community 1649 - "ACM Common — SLPF"
Cohesion: 0.20
Nodes (5): HMACSHA196, byte, CryptoStream, int, String

### Community 1650 - "ACM Common — SLPF"
Cohesion: 0.20
Nodes (4): SignatureRSA, CryptoStream, RSAParameters, SHA1CryptoServiceProvider

### Community 1651 - "ACM Common — HSMCommon Function"
Cohesion: 0.36
Nodes (4): HSMCommonFunction, DataTable, List, UDEKStorage

### Community 1653 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmARCONApiReqResLogs, Button, DropDownList, HiddenField, Label, LogMenuControl, Repeater, TextBox (+2 more)

### Community 1654 - "ACMO Web — Client Manager"
Cohesion: 0.35
Nodes (7): ObjectShredder, DataTable, Dictionary, FieldInfo, IEnumerable, PropertyInfo, LoadOption

### Community 1655 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmAPIApplicationNameMapping, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, Repeater (+2 more)

### Community 1656 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmAPILOBMapping, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, Repeater (+2 more)

### Community 1657 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmAPIRegistration, Button, HiddenField, Label, ListBox, RegularExpressionValidator, RequiredFieldValidator, TextBox (+2 more)

### Community 1658 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): FrmRDPSIpMapping, Button, DropDownList, HiddenField, HtmlGenericControl, Label, ListBox, Repeater (+2 more)

### Community 1659 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmRDPSIpSegment, Button, CheckBox, HtmlGenericControl, Label, LinkButton, RegularExpressionValidator, Repeater (+2 more)

### Community 1660 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): FrmRDPSReport, Button, DropDownList, HiddenField, HtmlGenericControl, Label, Repeater, TextBox (+2 more)

### Community 1661 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): FrmRDPSUserMapping, Button, DropDownList, HiddenField, HtmlGenericControl, Label, ListBox, Repeater (+2 more)

### Community 1671 - "ACMO Web — Client Manager"
Cohesion: 0.24
Nodes (6): a(), u(), p(), s(), p(), s()

### Community 1674 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (11): applyStyle(), applyStyleOnLoad(), find(), hide(), isModifierRequired(), isNumeric(), offset(), parseOffset() (+3 more)

### Community 1675 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): UCAllService, Button, DropDownList, HiddenField, HtmlGenericControl, Label, RadioButton, Repeater (+2 more)

### Community 1676 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (3): UCOracleQAOption, EventArgs, UpdatePanelUpdateMode

### Community 1677 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): UCPendingRequests, Button, DropDownList, GridView, HtmlGenericControl, Label, LinkButton, Repeater (+2 more)

### Community 1678 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmAdminWorkflow, Button, DropDownList, HiddenField, Label, LogMenuControl, Repeater, TextBox (+2 more)

### Community 1679 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmCriticalCommandWorkflow, Button, DropDownList, HiddenField, Label, LogMenuControl, Repeater, TextBox (+2 more)

### Community 1680 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmPasswordWorkflow, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LogMenuControl, Repeater (+2 more)

### Community 1681 - "ACMO Web — Client Manager"
Cohesion: 0.18
Nodes (10): frmServiceWorkflow, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LogMenuControl, Repeater (+2 more)

### Community 1682 - "ACMO Web — Portal"
Cohesion: 0.18
Nodes (10): frmChangeUserStatus, Button, DropDownList, HiddenField, HtmlGenericControl, Label, TextBox, UCFooter (+2 more)

### Community 1683 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (10): a(), b(), c(), d(), DOMException(), e(), f(), g() (+2 more)

### Community 1684 - "ACMO Web — Portal"
Cohesion: 0.18
Nodes (11): addTimeToArrayFromToken(), computeMonthsParse(), configFromObject(), Duration(), getParseRegexForToken(), hasOwnProp(), monthsRegex(), monthsShortRegex() (+3 more)

### Community 1685 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (11): addParseToken(), addWeekParseToken(), compareArrays(), copyConfig(), duration_as__valueOf(), isDaylightSavingTimeShifted(), isUndefined(), Moment() (+3 more)

### Community 1686 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (11): computeMonthsParse(), computeWeekdaysParse(), create_utc__createUTC(), createLocalOrUTC(), day_of_week__handleStrictParse(), getParseRegexForToken(), localeMonthsParse(), localeWeekdaysParse() (+3 more)

### Community 1689 - "ACMO Web — User Access"
Cohesion: 0.27
Nodes (5): DefaultV4, AmazonS3Client, bool, RegionEndpoint, string

### Community 1691 - "ASM Server — Server Manager"
Cohesion: 0.24
Nodes (4): ChannelDirectTCPIP, int, Stream, String

### Community 1692 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (5): HMACMD5, byte, CryptoStream, int, String

### Community 1693 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (5): HMACSHA1, byte, CryptoStream, int, String

### Community 1694 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (5): HMACSHA196, byte, CryptoStream, int, String

### Community 1695 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (4): SignatureRSA, CryptoStream, RSAParameters, SHA1CryptoServiceProvider

### Community 1697 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmLinkedDomainSetting, Button, ColumnHeader, ComboBox, GroupBox, IContainer, Label, ListView

### Community 1698 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmReferenceDetails, Button, ComboBox, GroupBox, IContainer, Label, Panel, TextBox

### Community 1699 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmLinkedDomainSetting, Button, ColumnHeader, ComboBox, GroupBox, IContainer, Label, ListView

### Community 1700 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmARCONSMobileOTPValidator, Button, GroupBox, IContainer, Label, Panel, TextBox, Timer

### Community 1701 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmARCONSWebBrowser, Button, GroupBox, IContainer, StatusStrip, TextBox, ToolStripStatusLabel, WebBrowser

### Community 1702 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmAboutBox, Button, IContainer, Label, LinkLabel, Panel, PictureBox, TextBox

### Community 1703 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmChangePasswordManuallySplitPassword, Button, ComboBox, GroupBox, IContainer, Label, Panel, TextBox

### Community 1704 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmDefaultSettings, Button, ErrorProvider, GroupBox, IContainer, Label, Panel, TextBox

### Community 1705 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmHAConfig, Button, ErrorProvider, GroupBox, IContainer, Label, Panel, TextBox

### Community 1706 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmNotifyOutsideARCOSSessions, Button, CheckedListBox, ComboBox, GroupBox, IContainer, Label, Panel

### Community 1707 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmPasswordChangeHistory, ColumnHeader, ContextMenuStrip, GroupBox, IContainer, ImageList, ListView, ToolStripMenuItem

### Community 1708 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmPasteUserProfileOption, Button, CheckBox, FlowLayoutPanel, GroupBox, IContainer, Panel, RadioButton

### Community 1709 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmRegistrationForm, Button, DateTimePicker, GroupBox, IContainer, Label, Panel, TextBox

### Community 1710 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmRestorePasswordManually, Button, GroupBox, IContainer, Label, Panel, RadioButton, TextBox

### Community 1711 - "ASM Server — Server Manager"
Cohesion: 0.31
Nodes (3): frmScrollableMessageBox, EventArgs, MessageBoxButtons

### Community 1712 - "ASM Server — Server Manager"
Cohesion: 0.24
Nodes (7): frmServersPasswordDependency_SelectService, Boolean, DataTable, EventArgs, ListViewItem, long, String

### Community 1713 - "ASM Server — Server Manager"
Cohesion: 0.18
Nodes (8): frmUpdateSSHKeyManually, Button, GroupBox, IContainer, Label, Panel, RadioButton, TextBox

### Community 1714 - "Common — Password Manager"
Cohesion: 0.33
Nodes (4): HSMDataFunctionsSPC, DataSet, DataTable, Hashtable

### Community 1715 - "Common — S"
Cohesion: 0.18
Nodes (8): frmARCONSMobileOTPValidator, Button, GroupBox, IContainer, Label, Panel, TextBox, Timer

### Community 1717 - "Common — SLPF"
Cohesion: 0.24
Nodes (4): ChannelDirectTCPIP, int, Stream, String

### Community 1718 - "Common — SLPF"
Cohesion: 0.20
Nodes (5): HMACMD596, byte, CryptoStream, int, String

### Community 1720 - "Common — Server Common Functions"
Cohesion: 0.27
Nodes (3): IPMACManager, Boolean, String

### Community 1721 - "Common — Reference Details"
Cohesion: 0.27
Nodes (4): frmReferenceDetailsCF, DataTable, EventArgs, MouseEventArgs

### Community 1722 - "Services — PAM Agents"
Cohesion: 0.29
Nodes (5): ProjectInstaller, EventLog, EventLogEntryType, IDictionary, String

### Community 1723 - "Services — Desk Insight"
Cohesion: 0.29
Nodes (3): frmRunAs, DragEventArgs, EventArgs

### Community 1724 - "Services — Desk Insight"
Cohesion: 0.18
Nodes (8): frmRunAs, Button, ColumnHeader, ContextMenuStrip, IContainer, ImageList, ListView, ToolStripMenuItem

### Community 1725 - "Services — Desk Insight"
Cohesion: 0.18
Nodes (6): frmAllElevatedApps, DataGridView, DataGridViewCellEventArgs, EventArgs, PaintEventArgs, string

### Community 1726 - "Services — Desk Insight"
Cohesion: 0.31
Nodes (6): ConsoleHelper, DllImport, int, IntPtr, uint, ARCONUBACommon.Helper

### Community 1727 - "Services — Desk Insight"
Cohesion: 0.20
Nodes (6): StringBuilder, Dictionary, uint, WlanNotificationCallbackDelegate, WlanClient, WlanInterface

### Community 1728 - "Services — Desk Insight"
Cohesion: 0.18
Nodes (8): OfflineElevationApproval, Button, ComboBox, GroupBox, IContainer, Label, PictureBox, TextBox

### Community 1729 - "Services — Desk Insight"
Cohesion: 0.27
Nodes (5): frmProgess, Boolean, EventArgs, ILog, Timer

### Community 1730 - "Services — Perf Mon IT"
Cohesion: 0.27
Nodes (4): DataRow, Int32, Int64, Object

### Community 1731 - "Services — Provisioning Scheduler"
Cohesion: 0.33
Nodes (3): ARCOSProvisioningReconService, EventArgs, ILog

### Community 1732 - "Services — Schedule Password Change"
Cohesion: 0.31
Nodes (7): Action, Task, Program, StorageAccountKey, StorageAccountKeysResponse, RotateSaKeyAndUpsertKvSecret, DefaultAzureCredential

### Community 1734 - "Services — Schedule Password Change"
Cohesion: 0.24
Nodes (4): ChannelDirectTCPIP, int, Stream, String

### Community 1735 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (5): HMACMD596, byte, CryptoStream, int, String

### Community 1736 - "Services — Schedule Password Change"
Cohesion: 0.22
Nodes (5): HMACSHA1, byte, CryptoStream, int, String

### Community 1737 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): SignatureRSA, CryptoStream, RSAParameters, SHA1CryptoServiceProvider

### Community 1739 - "Services — Schedule Password Change"
Cohesion: 0.33
Nodes (4): HSMDataFunctionsSPC, DataSet, DataTable, Hashtable

### Community 1742 - "Services — Schedule Password Change"
Cohesion: 0.24
Nodes (4): ChannelDirectTCPIP, int, Stream, String

### Community 1743 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (5): HMACMD596, byte, CryptoStream, int, String

### Community 1744 - "Services — Schedule Password Change"
Cohesion: 0.22
Nodes (5): HMACSHA1, byte, CryptoStream, int, String

### Community 1745 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (5): HMACSHA196, byte, CryptoStream, int, String

### Community 1746 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): SignatureRSA, CryptoStream, RSAParameters, SHA1CryptoServiceProvider

### Community 1748 - "Services — Scheduler Service"
Cohesion: 0.33
Nodes (4): HSMDataFunctionsAlert, DataSet, DataTable, Hashtable

### Community 1749 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (3): IPMACManager, Boolean, String

### Community 1750 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (3): SSHProtocol, Stream, SSHUtil

### Community 1752 - "Services — TSPlugin Service"
Cohesion: 0.24
Nodes (4): ChannelDirectTCPIP, int, Stream, String

### Community 1753 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (5): HMACMD5, byte, CryptoStream, int, String

### Community 1754 - "Services — TSPlugin Service"
Cohesion: 0.20
Nodes (5): HMACMD596, byte, CryptoStream, int, String

### Community 1755 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (5): HMACSHA1, byte, CryptoStream, int, String

### Community 1756 - "Services — TSPlugin Service"
Cohesion: 0.20
Nodes (5): HMACSHA196, byte, CryptoStream, int, String

### Community 1759 - "Services — TSPlugin Service"
Cohesion: 0.18
Nodes (5): IContainer, frmStartApp, STAThread, Program, StartApp

### Community 1760 - "LDAPAuthenticator"
Cohesion: 0.18
Nodes (8): int, CodeConstants, bool, string, GenericResponse, string, MessageConstants, Models.Response

### Community 1761 - "LDAPAuthenticator"
Cohesion: 0.27
Nodes (9): ObjectCommonProperties, PriorityMaster, RecordStatus, RSASecurIDRadiusServer, Boolean, DateTime, int, Int32 (+1 more)

### Community 1762 - "SSM — Arcos Compression"
Cohesion: 0.24
Nodes (5): Compression, Bitmap, Image, MemoryStream, object

### Community 1763 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.27
Nodes (5): bool, EventArgs, Message, string, NewFolderDialog

### Community 1764 - "ACM Client — Sshkey SFTP"
Cohesion: 0.22
Nodes (3): ARCOSSFTPPrivileges, Boolean, LabelEditEventArgs

### Community 1765 - "ACM Client — Sshkey SFTP"
Cohesion: 0.20
Nodes (7): PropertiesForm, Button, CheckBox, GroupBox, IContainer, Label, TextBox

### Community 1766 - "ACM Client — App Exe"
Cohesion: 0.24
Nodes (6): frmUNIXGUIOptions, Boolean, DialogResult, EventArgs, FormClosingEventArgs, String

### Community 1767 - "ACM Client — App Exe"
Cohesion: 0.20
Nodes (7): frmUNIXGUIOptions, Button, ComboBox, IContainer, Label, Panel, PictureBox

### Community 1768 - "ACM Client — DQS"
Cohesion: 0.20
Nodes (7): AboutForm, Button, IContainer, Label, PictureBox, TableLayoutPanel, TextBox

### Community 1769 - "ACM Client — DQS"
Cohesion: 0.22
Nodes (9): CommonFunctions, ExportSetting, StaticCommonFunctions, bool, Boolean, int, ServerSessionLogger, String (+1 more)

### Community 1770 - "ACM Client — DQS"
Cohesion: 0.20
Nodes (7): AddColumnForm, Button, CheckBox, ComboBox, IContainer, Label, TextBox

### Community 1771 - "ACM Client — DQS"
Cohesion: 0.20
Nodes (7): ModifyColumnForm, Button, CheckBox, ComboBox, IContainer, Label, TextBox

### Community 1772 - "ACM Client — Framework CM"
Cohesion: 0.24
Nodes (6): frmDelimiterOptions, Boolean, DialogResult, EventArgs, FormClosingEventArgs, String

### Community 1773 - "ACM Client — Framework CM"
Cohesion: 0.20
Nodes (7): frmDelimiterOptions, Button, ComboBox, IContainer, Label, Panel, PictureBox

### Community 1774 - "ACM Client — Framework CM"
Cohesion: 0.20
Nodes (7): frmExtendSessionDuration, Button, ComboBox, GroupBox, IContainer, Label, TextBox

### Community 1775 - "ACM Client — Framework CM"
Cohesion: 0.20
Nodes (7): frmPreferenceSelection, Button, ComboBox, IContainer, Label, Panel, PictureBox

### Community 1776 - "ACM Client — Framework CM"
Cohesion: 0.20
Nodes (7): frmUserCredentials_Service, Button, CheckBox, IContainer, Label, PictureBox, TextBox

### Community 1777 - "ACM Client — RDPTerminal"
Cohesion: 0.20
Nodes (7): frmRDPControlChooseStartupCommand, Button, ComboBox, IContainer, Label, Panel, PictureBox

### Community 1778 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (6): EncodingListItem, TerminalPage, bool, Encoding, SshTerminalControl, string

### Community 1779 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (5): IContainer, Image, ImageList, int, IconList

### Community 1780 - "ACM Client — SSHTerminal"
Cohesion: 0.20
Nodes (6): Button, Container, IPAddress, Label, TextBox, ServerInfo

### Community 1781 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (6): Button, Container, Icon, Label, PaintEventArgs, ThreeButtonMessageBox

### Community 1782 - "ACM Client — SSHTerminal"
Cohesion: 0.20
Nodes (6): Config, Button, IContainer, TreeView, ControlsPageContainer, UserControl

### Community 1783 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (6): EncodingListItem, TerminalPage, bool, Encoding, SshTerminalControl, string

### Community 1784 - "ACM Client — Web Browserv35"
Cohesion: 0.31
Nodes (6): AddNewTab(), TabbedBrowserCreator, nsITabParent, nsIURI, nsIWebBrowserChrome, nsIWindowCreator2

### Community 1785 - "ACM Common — .Smtp Send"
Cohesion: 0.38
Nodes (4): CertProvider, EventArgs, X509Certificate2, X509Certificate2Collection

### Community 1786 - "ACM Common — .User Controls"
Cohesion: 0.20
Nodes (7): DgvFilterHost, IContainer, Label, Panel, PictureBox, ToolStrip, ToolStripButton

### Community 1787 - "ACM Common — .User Controls"
Cohesion: 0.20
Nodes (6): ctlPopupToolTip, EventArgs, Image, LinkLabelLinkClickedEventArgs, PaintEventArgs, String

### Community 1788 - "ACM Common — SLPF"
Cohesion: 0.22
Nodes (6): ChannelX11, bool, byte, Hashtable, int, Socket

### Community 1789 - "ACM Common — SLPF"
Cohesion: 0.20
Nodes (4): TripleDESCBC, ICryptoTransform, int, TripleDES

### Community 1790 - "ACM Client — Network Devices"
Cohesion: 0.24
Nodes (6): frmCheckPointClientOptions, Boolean, DialogResult, EventArgs, FormClosingEventArgs, String

### Community 1791 - "ACM Client — Network Devices"
Cohesion: 0.20
Nodes (7): frmCheckPointClientOptions, Button, ComboBox, IContainer, Label, Panel, PictureBox

### Community 1792 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmCreateUserProfile, Button, DropDownList, HtmlGenericControl, Label, ListBox, RadioButton, TextBox (+1 more)

### Community 1793 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): Default, Button, HtmlForm, HtmlHead, Label, TextBox, UCResponseMessage, ARCOSClientManagerOnline.Debugger (+1 more)

### Community 1794 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmAbout, Button, HiddenField, HtmlGenericControl, Label, LinkButton, Literal, UCResponseMessage (+1 more)

### Community 1795 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmARCOSDashboard, HiddenField, HtmlForm, Image, LinkButton, Panel, ScriptManager, UCPopupGridView (+1 more)

### Community 1796 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmARCOSLogs, Button, DropDownList, GridView, HtmlGenericControl, Label, Repeater, TextBox (+1 more)

### Community 1797 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmLoginACMO_Debug, Button, DropDownList, HiddenField, Label, LinkButton, RequiredFieldValidator, TextBox (+1 more)

### Community 1798 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmTypesOfAccessSecrets, Button, HiddenField, HtmlGenericControl, Label, LinkButton, Repeater, TextBox (+1 more)

### Community 1799 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): FrmAgentDetailReport, Button, DropDownList, HiddenField, HtmlGenericControl, Label, Repeater, UCResponseMessage (+1 more)

### Community 1800 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmRDPSConfiguration, Button, CheckBox, HtmlGenericControl, Label, LinkButton, Repeater, TextBox (+1 more)

### Community 1801 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (10): boundsError(), checkIntBI(), isEqual(), isNotEqual(), solveEquation(), textOnPath(), validateMatrix(), validateNumber() (+2 more)

### Community 1802 - "ACMO Web — Client Manager"
Cohesion: 0.24
Nodes (10): computeStyle(), destroy(), findCommonOffsetParent(), getOffsetParent(), getRoot(), getRoundedOffsets(), getSupportedPropertyName(), isModifierEnabled() (+2 more)

### Community 1803 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmARCONMetadataVideolog, Button, HtmlForm, HtmlHead, Label, LinkButton, ScriptManager, UCResponseMessage (+1 more)

### Community 1804 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): UCMobileOTPValidator, Button, HtmlGenericControl, Label, Panel, PlaceHolder, TextBox, UCResponseMessage (+1 more)

### Community 1805 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): UCRequestLogs, Button, DropDownList, GridView, HtmlGenericControl, Label, LinkButton, Repeater (+1 more)

### Community 1806 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): UCSMSOTPValidator, Button, HiddenField, HtmlGenericControl, Label, Panel, PlaceHolder, TextBox (+1 more)

### Community 1807 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): UCUDFSRTotpAuth, Button, HiddenField, HtmlGenericControl, Image, Label, TextBox, UCResponseMessage (+1 more)

### Community 1808 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): UCServiceReference, Button, DropDownList, HiddenField, HtmlGenericControl, Panel, RadioButton, TextBox (+1 more)

### Community 1809 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): ARCOSWorkflow_TKTWFM, Button, DropDownList, HiddenField, HtmlGenericControl, Label, LinkButton, TextBox (+1 more)

### Community 1810 - "ACMO Web — Client Manager"
Cohesion: 0.20
Nodes (9): frmLoginAWM, Button, DropDownList, HiddenField, ImageButton, Label, RequiredFieldValidator, TextBox (+1 more)

### Community 1812 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (9): frmLogin, Button, DropDownList, HiddenField, ImageButton, Label, RequiredFieldValidator, TextBox (+1 more)

### Community 1813 - "ACMO Web — Portal"
Cohesion: 0.20
Nodes (9): frmServiceOnBoarding, Button, CheckBox, DropDownList, HiddenField, Label, TextBox, UCFooter (+1 more)

### Community 1814 - "ACMO Web — Portal"
Cohesion: 0.67
Nodes (9): a(), e(), h(), i(), n(), o(), r(), s() (+1 more)

### Community 1815 - "ACMO Web — User Access"
Cohesion: 0.27
Nodes (5): _Default, Boolean, EventArgs, RepeaterItemEventArgs, String

### Community 1817 - "ASM Server — Server Manager"
Cohesion: 0.38
Nodes (4): CertProvider, EventArgs, X509Certificate2, X509Certificate2Collection

### Community 1818 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (6): ctlPopupToolTip, EventArgs, Image, LinkLabelLinkClickedEventArgs, PaintEventArgs, String

### Community 1820 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (9): ConnectionEnd, ControlType, CredentialVerification, DataType, HashType, SecureProtocol, SecurityFlags, SslAlgorithms (+1 more)

### Community 1821 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (7): frmShowServiceRootUsers, Button, ColumnHeader, GroupBox, IContainer, ImageList, ListView

### Community 1822 - "ASM Server — Server Manager"
Cohesion: 0.27
Nodes (5): CommonAPICall, bool, HttpWebRequest, Int32, string

### Community 1823 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (7): frmAddNewData, Button, GroupBox, IContainer, Label, Panel, TextBox

### Community 1824 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (7): frmAddNewProcesses, Button, GroupBox, IContainer, Label, Panel, TextBox

### Community 1825 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (7): frmAddNewWindowsService, Button, GroupBox, IContainer, Label, Panel, TextBox

### Community 1826 - "ASM Server — Server Manager"
Cohesion: 0.20
Nodes (7): frmViewHistoryPassword, Button, DateTimePicker, GroupBox, IContainer, Label, Panel

### Community 1827 - "Common — .Smtp Send Mail.Security"
Cohesion: 0.38
Nodes (4): CertProvider, EventArgs, X509Certificate2, X509Certificate2Collection

### Community 1828 - "Common — .User Controls"
Cohesion: 0.20
Nodes (7): DgvFilterHost, IContainer, Label, Panel, PictureBox, ToolStrip, ToolStripButton

### Community 1829 - "Common — .User Controls"
Cohesion: 0.20
Nodes (6): ctlPopupToolTip, EventArgs, Image, LinkLabelLinkClickedEventArgs, PaintEventArgs, String

### Community 1830 - "Common — SLPF"
Cohesion: 0.20
Nodes (4): Err, Out, System, Array

### Community 1832 - "Common — HSMCommon Function"
Cohesion: 0.42
Nodes (3): HSMCommonFunction, DataTable, List

### Community 1833 - "Services — ADScanner Service"
Cohesion: 0.33
Nodes (4): EncryptionDecryption, Boolean, Byte, string

### Community 1834 - "Services — ADScanner Service"
Cohesion: 0.29
Nodes (5): Program, DllImport, int, IntPtr, ARCOSApp

### Community 1835 - "Services — Cloud File Uploader"
Cohesion: 0.27
Nodes (9): AmazonS3Details, AzureDetails, CloudStorage, GCPDetails, AmazonS3Client, BlobContainerClient, StorageClient, BlobServiceClient (+1 more)

### Community 1836 - "Services — DBSync Service"
Cohesion: 0.36
Nodes (4): CertProvider, EventArgs, X509Certificate2, X509Certificate2Collection

### Community 1837 - "Services — DBSync Service"
Cohesion: 0.27
Nodes (5): CertValidator, bool, EventArgs, string, X509Certificate2

### Community 1838 - "Services — Desk Insight"
Cohesion: 0.20
Nodes (7): Button, IContainer, Label, Panel, PictureBox, Form1, NewWinFormCsharpWebCam

### Community 1839 - "Services — Desk Insight"
Cohesion: 0.20
Nodes (7): frmFRApp, Button, IContainer, Label, Panel, PictureBox, Timer

### Community 1840 - "Services — Desk Insight"
Cohesion: 0.24
Nodes (10): string, WlanConnectionMode, WlanConnectionAttributes, WlanConnectionParameters, WlanInterfaceInfo, WlanProfileInfo, WlanAssociationAttributes, WlanConnectionFlags (+2 more)

### Community 1841 - "Services — Desk Insight"
Cohesion: 0.31
Nodes (5): Dot11BssType, Dot11Ssid, WlanConnectionMode, WlanBssEntry, WlanConnectionParameters

### Community 1842 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1843 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1844 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1845 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1846 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1847 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1848 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1849 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1850 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1851 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1852 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1853 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1854 - "Services — Log Archiver Service"
Cohesion: 0.31
Nodes (10): ArcosConfig, GenericResponse, LAConfig, ResultGeneric, ResultSet, Servers_Config, bool, IDictionary (+2 more)

### Community 1855 - "Services — Migrate Data Utility"
Cohesion: 0.20
Nodes (7): frmAddNewData, Button, GroupBox, IContainer, Label, Panel, TextBox

### Community 1856 - "Services — Passworde Envelope Manager"
Cohesion: 0.20
Nodes (8): frmAboutBox, Button, IContainer, Label, LinkLabel, Panel, PictureBox, TextBox

### Community 1857 - "Services — Perf Mon IT"
Cohesion: 0.24
Nodes (3): DataSet, DataTable, Hashtable

### Community 1858 - "Services — Privilege User Discovery"
Cohesion: 0.24
Nodes (9): Boolean, DateTime, int, Int32, String, ObjectCommonProperties, PriorityMaster, RecordStatus (+1 more)

### Community 1859 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): Err, Out, System, Array

### Community 1861 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): TripleDESCBC, ICryptoTransform, int, TripleDES

### Community 1862 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (9): ConnectionEnd, ControlType, CredentialVerification, DataType, HashType, SecureProtocol, SecurityFlags, SslAlgorithms (+1 more)

### Community 1863 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): Err, Out, System, Array

### Community 1865 - "Services — Schedule Password Change"
Cohesion: 0.20
Nodes (4): TripleDESCBC, ICryptoTransform, int, TripleDES

### Community 1866 - "Services — Schedule Password Change"
Cohesion: 0.27
Nodes (6): bool, FieldInfo, IntPtr, PropertyInfo, RSACryptoServiceProvider, RSAKeyTransform

### Community 1867 - "Services — Script Scheduler"
Cohesion: 0.31
Nodes (3): Boolean, String, IPMACManager

### Community 1868 - "Services — TSPlugin Service"
Cohesion: 0.20
Nodes (4): Err, Out, System, Array

### Community 1870 - "Services — TSPlugin Service"
Cohesion: 0.20
Nodes (4): TripleDESCBC, ICryptoTransform, int, TripleDES

### Community 1871 - "Services — TSPlugin Service"
Cohesion: 0.24
Nodes (7): ActivityLog, APIMethods, CommonAPI, DateTime, HttpWebRequest, int, string

### Community 1872 - "Onboarding — IPMACManager"
Cohesion: 0.29
Nodes (3): IPMACManager, Boolean, String

### Community 1873 - "MultiTab — src"
Cohesion: 0.20
Nodes (7): Protocol, RAW, RLOGIN, SERIAL, SSH, SSH2, TELNET

### Community 1874 - "Offline MultiTab — Offline API"
Cohesion: 0.24
Nodes (4): clearMenus(), getParent(), getTargetFromTrigger(), NOTE: POPOVER EXTENDS tooltip.js

### Community 1875 - "ACM Client — PAMMulti Tab"
Cohesion: 0.22
Nodes (4): Form1, Form1, IContainer, ARCONPAMMultiTab

### Community 1876 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.31
Nodes (4): bool, EventArgs, Message, CancelDialog

### Community 1877 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.22
Nodes (6): Button, CheckBox, IContainer, Label, TextBox, SetPermissionsDialog

### Community 1878 - "ACM Client — Sshkey SFTP"
Cohesion: 0.22
Nodes (6): FileMask, Button, GroupBox, IContainer, Label, TextBox

### Community 1879 - "ACM Client — Sshkey SFTP"
Cohesion: 0.22
Nodes (6): NewNamePrompt, Button, GroupBox, IContainer, Label, TextBox

### Community 1880 - "ACM Client — Sshkey SFTP"
Cohesion: 0.22
Nodes (6): PasswordPrompt, Button, GroupBox, IContainer, Label, TextBox

### Community 1881 - "ACM Client — DQS"
Cohesion: 0.22
Nodes (6): CodeSnippetsForm, ComboBox, IContainer, Label, ListBox, TextBox

### Community 1882 - "ACM Client — DQS"
Cohesion: 0.22
Nodes (6): FindReplaceForm, Button, CheckBox, IContainer, Label, TextBox

### Community 1883 - "ACM Client — DQS"
Cohesion: 0.22
Nodes (6): FlickerFreeRichEditTextBox, bool, int, Message, short, Scintilla

### Community 1884 - "ACM Client — DQS"
Cohesion: 0.22
Nodes (6): OracleQueryParameter, Button, GroupBox, IContainer, Label, TextBox

### Community 1886 - "ACM Client — Framework CM"
Cohesion: 0.22
Nodes (6): frmAddNewData, Button, GroupBox, IContainer, Label, TextBox

### Community 1887 - "ACM Client — Framework CM"
Cohesion: 0.28
Nodes (5): frmCustomApplicationHeader, Boolean, EventArgs, FormClosingEventArgs, String

### Community 1888 - "ACM Client — Framework CM"
Cohesion: 0.22
Nodes (6): frmCustomApplicationHeader, Button, GroupBox, IContainer, Label, TextBox

### Community 1889 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (7): CultureInfo, ResourceManager, Resources, CultureInfo, ResourceManager, Resources, My.Resources

### Community 1890 - "ACM Client — Script Manager"
Cohesion: 0.31
Nodes (4): frmAddNewData, EventArgs, MouseEventArgs, String

### Community 1891 - "ACM Client — Script Manager"
Cohesion: 0.28
Nodes (4): RefernceDetails, Boolean, RefernceDetails, Boolean

### Community 1892 - "ACM Client — SFTPTeminal"
Cohesion: 0.22
Nodes (6): NewNamePrompt, Button, GroupBox, IContainer, Label, TextBox

### Community 1893 - "ACM Client — SSHTerminal"
Cohesion: 0.33
Nodes (5): EventArgs, int, Process, string, ARCOSPScpLauncher

### Community 1894 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (7): AppearancePage, CheckBox, ColoredComboBox, GroupBox, IContainer, Label, RadioButton

### Community 1895 - "ACM Client — SSHTerminal"
Cohesion: 0.28
Nodes (5): Color, DllImport, Theme, ThemeUtil, Theme

### Community 1896 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (6): Button, IContainer, Label, PictureBox, Timer, frmPuttyControlOptions

### Community 1897 - "ACM Client — SSHTerminal"
Cohesion: 0.39
Nodes (3): Icon, ResourceManager, GIcons

### Community 1898 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (6): ContextMenuStrip, IContainer, TabControl, TabPage, ToolStripMenuItem, MainForm

### Community 1899 - "ACM Client — SSHTerminal"
Cohesion: 0.22
Nodes (7): AppearancePage, CheckBox, ColoredComboBox, GroupBox, IContainer, Label, RadioButton

### Community 1900 - "ACM Client — VNCTerminal"
Cohesion: 0.22
Nodes (5): Button, Container, EventArgs, TextBox, ConnectionPassword

### Community 1901 - "ACM Client — Web Browser"
Cohesion: 0.22
Nodes (6): BrowserControl, Button, IContainer, Label, Panel, TextBox

### Community 1902 - "ACM Client — Web Browserv35"
Cohesion: 0.22
Nodes (4): frmPageControls, EventArgs, GeckoWebBrowser, ARCOSWebBrowserv35

### Community 1904 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (8): PriorityMaster, ARCOSAppTypeName, ObjectCommonProperties, UserAccessPrivilegeSetting, Boolean, DateTime, int, String

### Community 1905 - "ACM Common — Enitity Objects"
Cohesion: 0.50
Nodes (8): APIReferenceMapping, ServiceAccessReferenceTemplate, ServiceReferenceTemplate, ServiceReferenceTemplateLOBConfig, WebServiceValidatingParam, Boolean, Int32, String

### Community 1906 - "ACMO Web — Provisioning Web"
Cohesion: 0.22
Nodes (7): CultureInfo, ResourceManager, Resource1, CultureInfo, ResourceManager, Resource, Resources

### Community 1907 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): frmATSSetPreferencePath, Button, DropDownList, HtmlGenericControl, Label, TextBox, UCResponseMessage, UpdatePanel

### Community 1908 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (4): Default, Boolean, EventArgs, String

### Community 1909 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): frmUserActivityVideoSession, Button, HtmlGenericControl, Label, Repeater, TextBox, UCResponseMessage, UpdatePanel

### Community 1910 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): frmViewAccessLogsLOB, Button, DropDownList, HiddenField, Label, Repeater, TextBox, UCResponseMessage

### Community 1911 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): frmConfigureUnattended, DropDownList, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage, UpdatePanel

### Community 1915 - "ACMO Web — Client Manager"
Cohesion: 0.44
Nodes (8): callPlugin(), decrypt(), encrypt(), fetchMissingDetails(), getMachineDetailsFromDB(), parseMachineDetails(), saveMachineDetails(), startMachineDetailsPolling()

### Community 1916 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (3): createNewSlider(), inner(), createNewSlider()

### Community 1920 - "ACMO Web — Client Manager"
Cohesion: 0.36
Nodes (7): getNextIndex(), init(), processDatapoints(), processRawData(), FIXME: auto-detection should really not be defined here, setupCategoriesForAxis(), transformPointsOnAxis()

### Community 1921 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (7): WebClient, Uri, WebRequest, WebClient, Uri, WebRequest, WebClient

### Community 1922 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): frmSSOApps, Button, HtmlGenericControl, HtmlInputHidden, Repeater, UCSSOResponseMessage, UpdatePanel, UCSSOPreference

### Community 1923 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): UCSSOPreference, Button, HiddenField, HtmlGenericControl, Label, TextBox, UCSSOResponseMessage, UpdatePanel

### Community 1924 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): UCRSASecurIDRADIUSValidator, Button, HtmlGenericControl, Label, Panel, PlaceHolder, TextBox, UCResponseMessage

### Community 1925 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): UCUDFSRCMFATotpAuth, Button, HiddenField, HtmlGenericControl, Label, TextBox, UCResponseMessage, UpdatePanel

### Community 1926 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): ARCOSWorkflow_AccessLog, Button, CheckBox, HiddenField, HtmlGenericControl, Label, TextBox, UCResponseMessage

### Community 1927 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): MasterLoginAWM, ContentPlaceHolder, HiddenField, HtmlForm, HtmlHead, ScriptManager, UCInfoDetails, UCSMSOTPValidator

### Community 1928 - "ACMO Web — Client Manager"
Cohesion: 0.22
Nodes (8): MasterWorkflow, ContentPlaceHolder, HtmlForm, HtmlHead, ScriptManager, UCInfoDetails, UCLoginStatus, UCMenuWorkflow

### Community 1929 - "ACMO Web — Portal"
Cohesion: 0.36
Nodes (9): addClass(), addSelections(), bindSideclick(), handleMouseMove(), handleMouseUp(), handleSelectionMousedown(), removeCellSelections(), removeClass() (+1 more)

### Community 1930 - "ACMO Web — Portal"
Cohesion: 0.22
Nodes (9): configFromObject(), Duration(), hasOwnProp(), monthsRegex(), monthsShortRegex(), normalizeObjectUnits(), weekdaysMinRegex(), weekdaysRegex() (+1 more)

### Community 1931 - "ACMO Web — Portal"
Cohesion: 0.36
Nodes (7): getNextIndex(), init(), processDatapoints(), processRawData(), FIXME: auto-detection should really not be defined here, setupCategoriesForAxis(), transformPointsOnAxis()

### Community 1933 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (6): CheckTargetConnection, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent

### Community 1935 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (6): ListViewAutoFiler, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator

### Community 1936 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (3): File, FileInfo, string

### Community 1939 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (6): RestrictedAndCriticalCommand, IContainer, Label, PictureBox, RadioButton, ARCONSRestrictedAndCriticalCommand

### Community 1940 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (6): ARCOSWorkflowActionXMLFormat, ARCOSWorkflowDetails, Boolean, DateTime, Int32, String

### Community 1941 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (4): ExportLog, Image, String, WordDocument

### Community 1942 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (7): ServiceType, ServiceTypeCF, ServiceTypes, Boolean, DateTime, int, string

### Community 1943 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (4): OracleDBConnection, DataTable, OracleConnection, string

### Community 1944 - "ASM Server — Server Manager"
Cohesion: 0.42
Nodes (4): ARCONSMobileOTP, Boolean, Int32, String

### Community 1945 - "ASM Server — Server Manager"
Cohesion: 0.39
Nodes (3): frmARCONSTerminalEmulator, EventArgs, String

### Community 1946 - "ASM Server — Server Manager"
Cohesion: 0.22
Nodes (6): frmInfo, Button, GroupBox, IContainer, Panel, TextBox

### Community 1947 - "ASM Server — Server Manager"
Cohesion: 0.39
Nodes (3): frmPasteUserProfileOption, EventArgs, int

### Community 1948 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_AES_CBC_ENCRYPT_DATA_PARAMS

### Community 1949 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAriaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_ARIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1950 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkCamelliaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_CAMELLIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1951 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkDesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_DES_CBC_ENCRYPT_DATA_PARAMS

### Community 1952 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkKeaDeriveParams, bool, IntPtr, NativeULong, CK_KEA_DERIVE_PARAMS

### Community 1953 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_AES_CBC_ENCRYPT_DATA_PARAMS

### Community 1954 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAriaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_ARIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1955 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkSeedCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_SEED_CBC_ENCRYPT_DATA_PARAMS

### Community 1956 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_AES_CBC_ENCRYPT_DATA_PARAMS

### Community 1957 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAriaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_ARIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1958 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkCamelliaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_CAMELLIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1959 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkDesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_DES_CBC_ENCRYPT_DATA_PARAMS

### Community 1960 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkKeaDeriveParams, bool, IntPtr, NativeULong, CK_KEA_DERIVE_PARAMS

### Community 1961 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkKeyWrapSetOaepParams, byte, IntPtr, NativeULong, CK_KEY_WRAP_SET_OAEP_PARAMS

### Community 1962 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkAriaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_ARIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1963 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkCamelliaCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_CAMELLIA_CBC_ENCRYPT_DATA_PARAMS

### Community 1964 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkDesCbcEncryptDataParams, byte, IntPtr, NativeULong, CK_DES_CBC_ENCRYPT_DATA_PARAMS

### Community 1965 - "ASM Server — Pkcs11Interop"
Cohesion: 0.22
Nodes (6): bool, CkKeaDeriveParams, bool, IntPtr, NativeULong, CK_KEA_DERIVE_PARAMS

### Community 1966 - "Common — .PIMUD"
Cohesion: 0.22
Nodes (6): CheckTargateConnectivity, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent

### Community 1967 - "Common — .PIMUD"
Cohesion: 0.22
Nodes (6): CheckTargetConnection, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent

### Community 1969 - "Common — .Smtp Send Mail.Security"
Cohesion: 0.31
Nodes (5): CertValidator, bool, EventArgs, string, X509Certificate2

### Community 1971 - "Common — S"
Cohesion: 0.42
Nodes (4): ARCONSMobileOTP, Boolean, Int32, String

### Community 1972 - "Common — SList View Addin"
Cohesion: 0.22
Nodes (6): ListViewAutoFiler, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator

### Community 1973 - "Common — SLPF"
Cohesion: 0.22
Nodes (3): File, FileInfo, string

### Community 1976 - "Common — Enitity Objects"
Cohesion: 0.22
Nodes (7): ServiceType, ServiceTypeCF, ServiceTypes, Boolean, DateTime, int, string

### Community 1977 - "Common — Enitity Objects"
Cohesion: 0.22
Nodes (8): UserAndServerRequest, bool, Boolean, DateTime, Int32, List, long, String

### Community 1978 - "Common — Enitity Objects"
Cohesion: 0.36
Nodes (7): GatewayConfiguration, LOBGatewayConfiguration, LOBVPNServers, VPNServers, VPNServersVIP, Boolean, String

### Community 1979 - "Common — Server Common Functions"
Cohesion: 0.22
Nodes (6): frmMSSQLConnectionRetry, Button, IContainer, Label, PictureBox, TextBox

### Community 1980 - "Common — Server Common Functions"
Cohesion: 0.25
Nodes (4): OracleDBConnection, DataTable, OracleConnection, string

### Community 1981 - "Services — Alert Service"
Cohesion: 0.36
Nodes (3): SmsHelper, List, Regex

### Community 1982 - "Services — Alert Service"
Cohesion: 0.31
Nodes (9): PatchCallAPI, RequestResponseDetails, WebAPIConfiguration, WebServiceValidatingParam, Boolean, DateTime, Int32, ObjectCommonProperties (+1 more)

### Community 1983 - "Services — Cloud File Uploader"
Cohesion: 0.31
Nodes (4): AzureUploadManager, ILog, string, Task

### Community 1984 - "Services — Desk Insight"
Cohesion: 0.31
Nodes (4): frmProgess, Boolean, EventArgs, Timer

### Community 1985 - "Services — Desk Insight"
Cohesion: 0.22
Nodes (6): frmFRScan, Button, IContainer, Label, Panel, PictureBox

### Community 1986 - "Services — Desk Insight"
Cohesion: 0.22
Nodes (8): int, WlanNotificationCallbackDelegate, WlanNotificationData, WlanPhyRadioState, WlanRadioState, Dot11RadioState, WlanNotificationSource, WlanPhyRadioState

### Community 1987 - "Services — Desk Insight"
Cohesion: 0.22
Nodes (7): frmMain, Button, ColumnHeader, IContainer, ListView, TextBox, Winsock

### Community 1988 - "Services — Folder Sync Service"
Cohesion: 0.36
Nodes (4): DllImport, IntPtr, MarshalAs, SingleInstance

### Community 1989 - "Services — Log Manager Service"
Cohesion: 0.28
Nodes (8): ARCOSLogManagerSettings, LogImageType, LogOrderType, bool, Boolean, int, Int32, String

### Community 1992 - "Services — Password Change Vault"
Cohesion: 0.53
Nodes (4): ARCONPasswordChangeVaultServiceSetup, DataAccessLayer, EncryptionLayer, ARCONPAMVaultApp

### Community 1993 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.ArchLinux

### Community 1994 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Cent

### Community 1995 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Debian

### Community 1996 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Fedora

### Community 1997 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Kali

### Community 1998 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Redhat

### Community 1999 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Slackware

### Community 2000 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Solaris

### Community 2001 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Linux.Ubuntu

### Community 2002 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Unix.Aix

### Community 2003 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Unix.Bsd

### Community 2004 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Unix.HpUx

### Community 2005 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Unix.Iris

### Community 2006 - "Services — Password Change Vault"
Cohesion: 0.22
Nodes (5): ChangeThroughRoot, Custom, Default, LockToConsole, BusinessLayer.Core.Ssh.Unix.Solaris

### Community 2008 - "Services — Perf Mon IT"
Cohesion: 0.36
Nodes (5): UNIX_SSH2, Boolean, Int32, String, SshShell

### Community 2009 - "Services — Schedule Password Change"
Cohesion: 0.22
Nodes (3): File, FileInfo, string

### Community 2012 - "Services — Schedule Password Change"
Cohesion: 0.22
Nodes (3): File, FileInfo, string

### Community 2015 - "Services — Script Scheduler"
Cohesion: 0.28
Nodes (7): Boolean, DateTime, Int32, String, ARCONSSSettings, TimeBetween, ScriptSchedulers

### Community 2016 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (6): AcceptableCharacters, FilterTextBox, AcceptableCharacters, bool, EventArgs, string

### Community 2017 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (6): ListViewAutoFiler, Button, ContextMenuStrip, IContainer, ToolStripMenuItem, ToolStripSeparator

### Community 2018 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (6): ARCOSWorkflowActionXMLFormat, ARCOSWorkflowDetails, Boolean, DateTime, Int32, String

### Community 2019 - "Services — TSPlugin Service"
Cohesion: 0.22
Nodes (3): File, FileInfo, string

### Community 2023 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (3): EventArgs, int, frmStartApp

### Community 2024 - "LDAPAuthenticator — Unit Testing"
Cohesion: 0.22
Nodes (6): Program, int, RSASecurIDRadiusServer, string, verifySettings, UnitTesting

### Community 2025 - "Onboarding — Connection Param"
Cohesion: 0.50
Nodes (4): ConnectionParam, ArrayList, Boolean, String

### Community 2026 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.22
Nodes (5): ArcossSSMDesktop.Pulley, SSMMessageBox, Button, IContainer, Label

### Community 2029 - "ACM Client — RStream Client"
Cohesion: 0.36
Nodes (4): frmProgess, Boolean, EventArgs, Timer

### Community 2030 - "ACM Client — RStream Client"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCONRStreamClient.Properties

### Community 2031 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.25
Nodes (5): Button, IContainer, Label, PictureBox, CancelDialog

### Community 2032 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.25
Nodes (5): Button, IContainer, Label, TextBox, FileOrFolderRename

### Community 2033 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.25
Nodes (5): Button, IContainer, Label, TextBox, NewFolderDialog

### Community 2034 - "ACM Client — Sshkey SFTP"
Cohesion: 0.25
Nodes (5): MoveToRemoteFolder, Button, IContainer, Label, TextBox

### Community 2035 - "ACM Client — Sshkey SFTP"
Cohesion: 0.25
Nodes (5): UnknownHostKey, Button, GroupBox, IContainer, Label

### Community 2036 - "ACM Client — App Exe"
Cohesion: 0.25
Nodes (5): frmConfirmation, Button, IContainer, Label, PictureBox

### Community 2037 - "ACM Client — Biometric Finger"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSBiometricFingerPrintAuthenticator.Properties

### Community 2038 - "ACM Client — DQS"
Cohesion: 0.32
Nodes (5): Program, DllImport, IDbConnection, IntPtr, STAThread

### Community 2039 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): AddViewForm, Button, IContainer, Label, TextBox

### Community 2040 - "ACM Client — DQS"
Cohesion: 0.29
Nodes (4): GoToLineForm, EventArgs, KeyPressEventArgs, Message

### Community 2041 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): GoToLineForm, Button, IContainer, Label, TextBox

### Community 2042 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameColumnForm, Button, IContainer, Label, TextBox

### Community 2043 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameCONSTRAINTForm, Button, IContainer, Label, TextBox

### Community 2044 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameDBLINKForm, Button, IContainer, Label, TextBox

### Community 2045 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameFunctionForm, Button, IContainer, Label, TextBox

### Community 2046 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameIndexForm, Button, IContainer, Label, TextBox

### Community 2047 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameMaterializedViewForm, Button, IContainer, Label, TextBox

### Community 2048 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameMaterializedViewLogForm, Button, IContainer, Label, TextBox

### Community 2049 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenamePackageForm, Button, IContainer, Label, TextBox

### Community 2050 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameProcedureForm, Button, IContainer, Label, TextBox

### Community 2051 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameSEQUENCEForm, Button, IContainer, Label, TextBox

### Community 2052 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameSYNONYMForm, Button, IContainer, Label, TextBox

### Community 2053 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameTableForm, Button, IContainer, Label, TextBox

### Community 2054 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameTableSpaceForm, Button, IContainer, Label, TextBox

### Community 2055 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameTRIGGERForm, Button, IContainer, Label, TextBox

### Community 2056 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameTYPEForm, Button, IContainer, Label, TextBox

### Community 2057 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameUSERForm, Button, IContainer, Label, TextBox

### Community 2058 - "ACM Client — DQS"
Cohesion: 0.25
Nodes (5): RenameViewForm, Button, IContainer, Label, TextBox

### Community 2059 - "ACM Client — Framework CM"
Cohesion: 0.25
Nodes (5): SecureShellOutgoingTunnel, int, SecureShellConnection, Socket, string

### Community 2062 - "ACM Client — Framework CM"
Cohesion: 0.25
Nodes (5): frmARCOSVPNClientV4, Button, GroupBox, IContainer, Label

### Community 2063 - "ACM Client — Framework CM"
Cohesion: 0.25
Nodes (5): SecureShellOutgoingTunnel, int, SecureShellConnection, Socket, string

### Community 2064 - "ACM Client — Framework CM"
Cohesion: 0.25
Nodes (5): frmServiceProcessLog, Button, IContainer, Label, TextBox

### Community 2065 - "ACM Client — Framework CM"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSFrameworkCM.Properties

### Community 2066 - "ACM Client — Oracle Query"
Cohesion: 0.29
Nodes (6): LASTINPUTINFO, SessionIdleTime, DllImport, Int32, LASTINPUTINFO, uint

### Community 2067 - "ACM Client — RDPTerminal"
Cohesion: 0.25
Nodes (5): frmRDPConfirmation, Button, IContainer, Label, PictureBox

### Community 2068 - "ACM Client — RDPTerminal"
Cohesion: 0.25
Nodes (5): frmRDPControlOptions, Button, IContainer, Label, PictureBox

### Community 2069 - "ACM Client — RDPTerminal"
Cohesion: 0.25
Nodes (5): frmRDPWait, IContainer, Label, PictureBox, Timer

### Community 2070 - "ACM Client — RDPTerminal"
Cohesion: 0.25
Nodes (5): frmTSMonitorRDPControlOptions, Button, IContainer, Label, PictureBox

### Community 2071 - "ACM Client — Script Manager"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSScriptManager.Properties

### Community 2072 - "ACM Client — SSHTerminal"
Cohesion: 0.25
Nodes (5): Button, IContainer, Label, TextBox, ARCOSPScpLauncher

### Community 2073 - "ACM Client — SSHTerminal"
Cohesion: 0.29
Nodes (6): LASTINPUTINFO, SessionIdleTime, DllImport, Int32, LASTINPUTINFO, uint

### Community 2074 - "ACM Client — SSHTerminal"
Cohesion: 0.36
Nodes (3): BigInteger, Stream, SSH1UserAuthKey

### Community 2075 - "ACM Client — SSHTerminal"
Cohesion: 0.36
Nodes (3): bool, EventArgs, UnknownHostKey

### Community 2076 - "ACM Client — Web Browser"
Cohesion: 0.29
Nodes (6): WebBrowserSiteEx, Guid, IntPtr, IOleCommandTarget, OLECMD, WebBrowserSite

### Community 2077 - "ACM Client — Web Browser"
Cohesion: 0.36
Nodes (5): PopupBlockerFilterLevel, ARCOSWebBrowserSetting, SettingsHelper, Boolean, object

### Community 2078 - "ACM Client — Web Browser"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSWebBrowser.Properties

### Community 2079 - "ACM Client — Web Browserv35"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSWebBrowserv35.Properties

### Community 2080 - "ACM Common — APICalling"
Cohesion: 0.29
Nodes (7): APIParam, LicenseAPI, TokenResponse, UserInfoToken, DateTime, int, string

### Community 2082 - "ACM Common — .User Controls"
Cohesion: 0.25
Nodes (5): ctlPopupToolTip, IContainer, Label, LinkLabel, PictureBox

### Community 2083 - "ACM Common — SFilter Controls"
Cohesion: 0.29
Nodes (6): AcceptableCharacters, FilterTextBox, AcceptableCharacters, bool, EventArgs, string

### Community 2084 - "ACM Common — SLPF"
Cohesion: 0.29
Nodes (3): MD5, CryptoStream, MD5CryptoServiceProvider

### Community 2085 - "ACM Common — SLPF"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2086 - "ACM Common — SLPF"
Cohesion: 0.32
Nodes (4): bool, byte, int, ARCFourManagedTransform

### Community 2087 - "ACM Common — Enitity Objects"
Cohesion: 0.43
Nodes (7): AMCO_Constant, ASMEC_Constant, CRUD_Constant, ErrorApplicationName, ErrorLogType, ErrorOSType, string

### Community 2088 - "ACMO Web — .ACMO.Test"
Cohesion: 0.29
Nodes (5): CommonFunctionsACMOTests, DataRow, string, TestMethod, DataTestMethod

### Community 2089 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): frmACViewProfile, ACMenuControl, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage

### Community 2090 - "ACMO Web — Client Manager"
Cohesion: 0.36
Nodes (4): frmViewProfile, DataTable, EventArgs, String

### Community 2091 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): frmViewProfile, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage, ARCOSClientManagerOnline.ARCONAppSetup

### Community 2092 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): frmArsimViewProfile, ACMenuControl, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage

### Community 2093 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (5): frmErrorPage, EventArgs, frmErrorPage, HtmlHead, ARCOSClientManagerOnline.ErrorPages

### Community 2094 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): frmPendingRequests, GridView, HtmlForm, Label, Repeater, ScriptManager, UCResponseMessage

### Community 2095 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): frmSecretServiceConfiguration, Button, HtmlGenericControl, Label, LinkButton, TextBox, UCResponseMessage

### Community 2096 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): NOTE: Needed to display correct count of selected rows, NOTE: Needed to avoid duplicate call to updateStateCheckboxes() in…, NOTE: Needed to update table state, NOTE: Needed only to reduce memory footprint, TODO: it's not optimal to update state of checkboxes, NOTE: if row selection is enabled, checkbox selection/deselection, NOTE: If checkbox has indeterminate state,

### Community 2097 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (3): BigPlayButton(), isPromise(), silencePromise()

### Community 2099 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): NOTE: Needed to display correct count of selected rows, NOTE: Needed to avoid duplicate call to updateStateCheckboxes() in…, NOTE: Needed to update table state, NOTE: Needed only to reduce memory footprint, TODO: it's not optimal to update state of checkboxes, NOTE: if row selection is enabled, checkbox selection/deselection, NOTE: If checkbox has indeterminate state,

### Community 2100 - "ACMO Web — Client Manager"
Cohesion: 0.39
Nodes (8): bi_windup(), compress_block(), d_code(), put_short(), send_bits(), send_code(), send_tree(), _tr_stored_block()

### Community 2101 - "ACMO Web — Client Manager"
Cohesion: 0.36
Nodes (4): c(), d(), h(), i()

### Community 2102 - "ACMO Web — Client Manager"
Cohesion: 0.43
Nodes (6): getNextIndex(), init(), processDatapoints(), processRawData(), setupCategoriesForAxis(), transformPointsOnAxis()

### Community 2103 - "ACMO Web — Client Manager"
Cohesion: 0.46
Nodes (7): draw(), drawError(), drawPath(), drawSeriesErrors(), init(), parseErrors(), processRawData()

### Community 2104 - "ACMO Web — Client Manager"
Cohesion: 0.46
Nodes (7): draw(), drawError(), drawPath(), drawSeriesErrors(), init(), parseErrors(), processRawData()

### Community 2105 - "ACMO Web — Client Manager"
Cohesion: 0.64
Nodes (7): callbacks(), capitalize(), off(), on(), operate(), option(), tidy()

### Community 2106 - "ACMO Web — Client Manager"
Cohesion: 0.61
Nodes (6): D(), F(), k(), L(), t(), x()

### Community 2107 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): UCSSOUserPasswordChange, Button, HiddenField, Image, Panel, TextBox, UCSSOResponseMessage

### Community 2108 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): UCUDFSRMobileOTP, Button, HiddenField, HtmlGenericControl, Label, TextBox, UCResponseMessage

### Community 2109 - "ACMO Web — Client Manager"
Cohesion: 0.25
Nodes (7): UCUDFSRSMSOTP, Button, HiddenField, HtmlGenericControl, Label, TextBox, UCResponseMessage

### Community 2110 - "ACMO Web — Portal"
Cohesion: 0.25
Nodes (8): createAdder(), defineLocale(), deprecate(), deprecateSimple(), isObject(), mergeConfigs(), updateLocale(), warn()

### Community 2111 - "ACMO Web — Portal"
Cohesion: 0.43
Nodes (6): getNextIndex(), init(), processDatapoints(), processRawData(), setupCategoriesForAxis(), transformPointsOnAxis()

### Community 2112 - "ACMO Web — Portal"
Cohesion: 0.46
Nodes (7): draw(), drawError(), drawPath(), drawSeriesErrors(), init(), parseErrors(), processRawData()

### Community 2113 - "ACMO Web — Portal"
Cohesion: 0.46
Nodes (7): draw(), drawError(), drawPath(), drawSeriesErrors(), init(), parseErrors(), processRawData()

### Community 2114 - "ACMO Web — Portal"
Cohesion: 0.64
Nodes (7): callbacks(), capitalize(), off(), on(), operate(), option(), tidy()

### Community 2115 - "ACMO Web — Portal"
Cohesion: 0.61
Nodes (6): D(), F(), k(), L(), t(), x()

### Community 2116 - "ASM Server — Encrpt Decrypt"
Cohesion: 0.32
Nodes (3): ARCONEncryptDecryptFile, ARCONHashAlg, string

### Community 2118 - "ASM Server — Server Manager"
Cohesion: 0.36
Nodes (3): ComboBox, EventArgs, MethodInfo

### Community 2119 - "ASM Server — Server Manager"
Cohesion: 0.21
Nodes (8): CURSORINFO, ICONINFO, POINT, RECT, bool, int, Int32, POINT

### Community 2120 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (6): AcceptableCharacters, FilterTextBox, AcceptableCharacters, bool, EventArgs, string

### Community 2121 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (3): FileOutputStream, FileStream, SeekOrigin

### Community 2123 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (3): MD5, CryptoStream, MD5CryptoServiceProvider

### Community 2124 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2127 - "ASM Server — Server Manager"
Cohesion: 0.32
Nodes (4): bool, byte, int, ARCFourManagedTransform

### Community 2128 - "ASM Server — Server Manager"
Cohesion: 0.32
Nodes (4): RestrictedAndCriticalCommand, Control, EventArgs, String

### Community 2129 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (7): ARCOSAppTypeName, ObjectCommonProperties, UserAccessPrivilegeSetting, Boolean, DateTime, int, String

### Community 2130 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (6): ConfigMapping, bool, Boolean, DateTime, int, string

### Community 2131 - "ASM Server — Server Manager"
Cohesion: 0.43
Nodes (7): AMCO_Constant, ASMEC_Constant, CRUD_Constant, ErrorApplicationName, ErrorLogType, ErrorOSType, string

### Community 2132 - "ASM Server — Server Manager"
Cohesion: 0.36
Nodes (5): frmCommandLogViewer, EventArgs, int, Int32, String

### Community 2133 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (7): frmIndividualCommandLogViewer, Boolean, EventArgs, int, Int32, String, StringBuilder

### Community 2135 - "ASM Server — Server Manager"
Cohesion: 0.25
Nodes (5): frmARCOSVPNClientV4, Button, GroupBox, IContainer, Label

### Community 2136 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (5): ARCOSApp, Boolean, Form, Int32, String

### Community 2137 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (6): LASTINPUTINFO, SessionIdleTime, DllImport, Int32, LASTINPUTINFO, uint

### Community 2138 - "ASM Server — Server Manager"
Cohesion: 0.32
Nodes (4): frmSplashScreenServer, Boolean, EventArgs, Stream

### Community 2139 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkAesCtrParams, byte, NativeULong, CK_AES_CTR_PARAMS

### Community 2140 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCamelliaCtrParams, byte, NativeULong, CK_CAMELLIA_CTR_PARAMS

### Community 2141 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCcmParams, IntPtr, NativeULong, CK_CCM_PARAMS

### Community 2142 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCmsSigParams, IntPtr, NativeULong, CK_CMS_SIG_PARAMS

### Community 2143 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdh1DeriveParams, IntPtr, NativeULong, CK_ECDH1_DERIVE_PARAMS

### Community 2144 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdh2DeriveParams, IntPtr, NativeULong, CK_ECDH2_DERIVE_PARAMS

### Community 2145 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdhAesKeyWrapParams, IntPtr, NativeULong, CK_ECDH_AES_KEY_WRAP_PARAMS

### Community 2146 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcmqvDeriveParams, IntPtr, NativeULong, CK_ECMQV_DERIVE_PARAMS

### Community 2147 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGostR3410DeriveParams, IntPtr, NativeULong, CK_GOSTR3410_DERIVE_PARAMS

### Community 2148 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params2, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS2

### Community 2149 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS

### Community 2150 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc2CbcParams, byte, NativeULong, CK_RC2_CBC_PARAMS

### Community 2151 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc5CbcParams, IntPtr, NativeULong, CK_RC5_CBC_PARAMS

### Community 2152 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkTlsPrfParams, IntPtr, NativeULong, CK_TLS_PRF_PARAMS

### Community 2153 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942Dh2DeriveParams, IntPtr, NativeULong, CK_X9_42_DH2_DERIVE_PARAMS

### Community 2154 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942MqvDeriveParams, IntPtr, NativeULong, CK_X9_42_MQV_DERIVE_PARAMS

### Community 2155 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkAesCtrParams, byte, NativeULong, CK_AES_CTR_PARAMS

### Community 2156 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCamelliaCtrParams, byte, NativeULong, CK_CAMELLIA_CTR_PARAMS

### Community 2157 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCcmParams, IntPtr, NativeULong, CK_CCM_PARAMS

### Community 2158 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCmsSigParams, IntPtr, NativeULong, CK_CMS_SIG_PARAMS

### Community 2159 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdh1DeriveParams, IntPtr, NativeULong, CK_ECDH1_DERIVE_PARAMS

### Community 2160 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcmqvDeriveParams, IntPtr, NativeULong, CK_ECMQV_DERIVE_PARAMS

### Community 2161 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGcmParams, IntPtr, NativeULong, CK_GCM_PARAMS

### Community 2162 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGostR3410DeriveParams, IntPtr, NativeULong, CK_GOSTR3410_DERIVE_PARAMS

### Community 2163 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkKipParams, IntPtr, NativeULong, CK_KIP_PARAMS

### Community 2164 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPbeParams, IntPtr, NativeULong, CK_PBE_PARAMS

### Community 2165 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params2, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS2

### Community 2166 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc2CbcParams, byte, NativeULong, CK_RC2_CBC_PARAMS

### Community 2167 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc5CbcParams, IntPtr, NativeULong, CK_RC5_CBC_PARAMS

### Community 2168 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkSkipjackRelayxParams, IntPtr, NativeULong, CK_SKIPJACK_RELAYX_PARAMS

### Community 2169 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkWtlsPrfParams, IntPtr, NativeULong, CK_WTLS_PRF_PARAMS

### Community 2170 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942Dh1DeriveParams, IntPtr, NativeULong, CK_X9_42_DH1_DERIVE_PARAMS

### Community 2171 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942Dh2DeriveParams, IntPtr, NativeULong, CK_X9_42_DH2_DERIVE_PARAMS

### Community 2172 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkAesCtrParams, byte, NativeULong, CK_AES_CTR_PARAMS

### Community 2173 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCamelliaCtrParams, byte, NativeULong, CK_CAMELLIA_CTR_PARAMS

### Community 2174 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCcmParams, IntPtr, NativeULong, CK_CCM_PARAMS

### Community 2175 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkDsaParameterGenParam, IntPtr, NativeULong, CK_DSA_PARAMETER_GEN_PARAM

### Community 2176 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdh1DeriveParams, IntPtr, NativeULong, CK_ECDH1_DERIVE_PARAMS

### Community 2177 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcmqvDeriveParams, IntPtr, NativeULong, CK_ECMQV_DERIVE_PARAMS

### Community 2178 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGcmParams, IntPtr, NativeULong, CK_GCM_PARAMS

### Community 2179 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGostR3410KeyWrapParams, IntPtr, NativeULong, CK_GOSTR3410_KEY_WRAP_PARAMS

### Community 2180 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkKeyDerivationStringData, IntPtr, NativeULong, CK_KEY_DERIVATION_STRING_DATA

### Community 2181 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPbeParams, IntPtr, NativeULong, CK_PBE_PARAMS

### Community 2182 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params2, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS2

### Community 2183 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS

### Community 2184 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc2CbcParams, byte, NativeULong, CK_RC2_CBC_PARAMS

### Community 2185 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc5CbcParams, IntPtr, NativeULong, CK_RC5_CBC_PARAMS

### Community 2186 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkSkipjackRelayxParams, IntPtr, NativeULong, CK_SKIPJACK_RELAYX_PARAMS

### Community 2187 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942Dh2DeriveParams, IntPtr, NativeULong, CK_X9_42_DH2_DERIVE_PARAMS

### Community 2188 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkAesCtrParams, byte, NativeULong, CK_AES_CTR_PARAMS

### Community 2189 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCamelliaCtrParams, byte, NativeULong, CK_CAMELLIA_CTR_PARAMS

### Community 2190 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCcmParams, IntPtr, NativeULong, CK_CCM_PARAMS

### Community 2191 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkCmsSigParams, IntPtr, NativeULong, CK_CMS_SIG_PARAMS

### Community 2192 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkDsaParameterGenParam, IntPtr, NativeULong, CK_DSA_PARAMETER_GEN_PARAM

### Community 2193 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdh1DeriveParams, IntPtr, NativeULong, CK_ECDH1_DERIVE_PARAMS

### Community 2194 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcdhAesKeyWrapParams, IntPtr, NativeULong, CK_ECDH_AES_KEY_WRAP_PARAMS

### Community 2195 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkEcmqvDeriveParams, IntPtr, NativeULong, CK_ECMQV_DERIVE_PARAMS

### Community 2196 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGcmParams, IntPtr, NativeULong, CK_GCM_PARAMS

### Community 2197 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkGostR3410KeyWrapParams, IntPtr, NativeULong, CK_GOSTR3410_KEY_WRAP_PARAMS

### Community 2198 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPbeParams, IntPtr, NativeULong, CK_PBE_PARAMS

### Community 2199 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params2, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS2

### Community 2200 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkPkcs5Pbkd2Params, IntPtr, NativeULong, CK_PKCS5_PBKD2_PARAMS

### Community 2201 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc2CbcParams, byte, NativeULong, CK_RC2_CBC_PARAMS

### Community 2202 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkRc5CbcParams, IntPtr, NativeULong, CK_RC5_CBC_PARAMS

### Community 2203 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkSkipjackPrivateWrapParams, IntPtr, NativeULong, CK_SKIPJACK_PRIVATE_WRAP_PARAMS

### Community 2204 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (5): bool, CkX942Dh1DeriveParams, IntPtr, NativeULong, CK_X9_42_DH1_DERIVE_PARAMS

### Community 2205 - "ASM Server — Pkcs11Interop"
Cohesion: 0.25
Nodes (7): Microsoft.NET.Sdk, net20, net40, net45, netstandard2.0, Microsoft.NETFramework.ReferenceAssemblies (1.0.3), Microsoft.SourceLink.GitHub (8.0.0)

### Community 2207 - "Common — .User Controls"
Cohesion: 0.36
Nodes (3): ComboBox, EventArgs, MethodInfo

### Community 2208 - "Common — .User Controls"
Cohesion: 0.25
Nodes (5): ctlPopupToolTip, IContainer, Label, LinkLabel, PictureBox

### Community 2209 - "Common — App"
Cohesion: 0.29
Nodes (5): ARCONApp, Boolean, Form, Int32, String

### Community 2210 - "Common — SFilter Controls"
Cohesion: 0.29
Nodes (6): AcceptableCharacters, FilterTextBox, AcceptableCharacters, bool, EventArgs, string

### Community 2211 - "Common — SLPF"
Cohesion: 0.25
Nodes (3): FileOutputStream, FileStream, SeekOrigin

### Community 2212 - "Common — SLPF"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2214 - "Common — SLPF"
Cohesion: 0.32
Nodes (4): bool, byte, int, ARCFourManagedTransform

### Community 2215 - "Common — Enitity Objects"
Cohesion: 0.25
Nodes (6): ConfigMapping, bool, Boolean, DateTime, int, string

### Community 2216 - "Common — Enitity Objects"
Cohesion: 0.43
Nodes (7): AMCO_Constant, ASMEC_Constant, CRUD_Constant, ErrorApplicationName, ErrorLogType, ErrorOSType, string

### Community 2217 - "Common — Enitity Objects"
Cohesion: 0.25
Nodes (6): ProcessDBLog, Boolean, DateTime, Int32, long, String

### Community 2218 - "Common — Enitity Objects"
Cohesion: 0.25
Nodes (7): UserDiscoveryScheduler, bool, DateTime, int, Int64, Nullable, string

### Community 2219 - "Common — Enitity Objects"
Cohesion: 0.29
Nodes (7): WindowsService, WindowsServiceProfileModel, bool, DateTime, int, Nullable, string

### Community 2220 - "Common — VPNClient"
Cohesion: 0.25
Nodes (5): frmARCOSVPNClientV4, Button, GroupBox, IContainer, Label

### Community 2221 - "Services — PAM Agents"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARWH.Properties

### Community 2222 - "Services — DBSync Service"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSDBSyncServiceController.Properties

### Community 2223 - "Services — Desk Insight"
Cohesion: 0.32
Nodes (7): Session, SESSION_TYPE, SessionManager, int, List, SESSION_TYPE, string

### Community 2224 - "Services — Desk Insight"
Cohesion: 0.25
Nodes (5): frmArgumentforApp, Button, IContainer, Label, TextBox

### Community 2225 - "Services — Desk Insight"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCONRemoteAssist.Properties

### Community 2226 - "Services — Log Archiver Service"
Cohesion: 0.21
Nodes (6): Resources, CultureInfo, ResourceManager, Resources, CultureInfo, ResourceManager

### Community 2227 - "Services — Migrate Data Utility"
Cohesion: 0.29
Nodes (6): Bitmap, CultureInfo, ResourceManager, Resources, Settings, MigrateDataUtility.Properties

### Community 2228 - "Services — Passworde Envelope Manager"
Cohesion: 0.29
Nodes (6): Resources, Bitmap, CultureInfo, ResourceManager, Settings, ARCOSPasswordeEnvelopeManager.Properties

### Community 2229 - "Services — Privilege User Discovery"
Cohesion: 0.32
Nodes (6): ARCONUDSettings, TimeBetween, Boolean, DateTime, Int32, String

### Community 2230 - "Services — Schedule Password Change"
Cohesion: 0.25
Nodes (3): FileOutputStream, FileStream, SeekOrigin

### Community 2231 - "Services — Schedule Password Change"
Cohesion: 0.29
Nodes (3): MD5, CryptoStream, MD5CryptoServiceProvider

### Community 2232 - "Services — Schedule Password Change"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2235 - "Services — Schedule Password Change"
Cohesion: 0.32
Nodes (4): bool, byte, int, ARCFourManagedTransform

### Community 2236 - "Services — Schedule Password Change"
Cohesion: 0.25
Nodes (6): CheckTargateConnectivity, bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent

### Community 2237 - "Services — Schedule Password Change"
Cohesion: 0.25
Nodes (3): FileOutputStream, FileStream, SeekOrigin

### Community 2238 - "Services — Schedule Password Change"
Cohesion: 0.29
Nodes (3): MD5, CryptoStream, MD5CryptoServiceProvider

### Community 2239 - "Services — Schedule Password Change"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2241 - "Services — Schedule Password Change"
Cohesion: 0.32
Nodes (4): bool, byte, int, ARCFourManagedTransform

### Community 2242 - "Services — Scheduler Service"
Cohesion: 0.32
Nodes (6): CriticalWithApprovalRequest, DataTable, Hashtable, SqlConnection, String, USPSqlParameterMaster

### Community 2243 - "Services — Script Scheduler"
Cohesion: 0.25
Nodes (6): bool, Exception, IAsyncResult, IPEndPoint, ManualResetEvent, CheckTargateConnectivity

### Community 2244 - "Services — TSPlugin Service"
Cohesion: 0.43
Nodes (4): MSSqlDBConnection, frmMSSQLConnectionRetry, SqlConnection, String

### Community 2245 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (5): SecureShellOutgoingTunnel, int, SecureShellConnection, Socket, string

### Community 2247 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (3): FileOutputStream, FileStream, SeekOrigin

### Community 2248 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (3): MD5, CryptoStream, MD5CryptoServiceProvider

### Community 2249 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (3): SHA1, CryptoStream, SHA1CryptoServiceProvider

### Community 2252 - "Services — TSPlugin Service"
Cohesion: 0.25
Nodes (5): frmARCOSVPNClientV4, Button, GroupBox, IContainer, Label

### Community 2253 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (5): FindTopLevelWindow, SHFILEINFO, bool, string, uint

### Community 2255 - "Services — Windows Vaulting Service"
Cohesion: 0.25
Nodes (3): bool, SafeHandle, WindowsUserDiscovery

### Community 2256 - "Services — Windows Vaulting Service"
Cohesion: 0.29
Nodes (6): Resources, CultureInfo, Icon, ResourceManager, Settings, AppSAPLogonPwdChange.Properties

### Community 2257 - "MultiTab — src"
Cohesion: 0.36
Nodes (3): JsonInclude, JsonProperty, ServiceSession

### Community 2258 - "Offline MultiTab — Windows Service"
Cohesion: 0.25
Nodes (6): Microsoft.Extensions.Hosting (3.1.19), netcoreapp3.1, Microsoft.Extensions.Hosting.WindowsServices (3.1.19), Newtonsoft.Json (13.0.1), System.Management (5.0.0), Microsoft.NET.Sdk.Worker

### Community 2259 - "ACM Client — ACMCommon Functions"
Cohesion: 0.29
Nodes (7): ARCONACMCommonFunctionsCM.UnitTest, net472, Microsoft.NET.Test.Sdk (16.5.0), NUnit (3.12.0), NUnit3TestAdapter (3.16.1), Microsoft.NET.Sdk, Selenium.WebDriver (4.44.0)

### Community 2260 - "ACM Client — PAMMulti Tab"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONPAMMultiTab.Properties

### Community 2261 - "ACM Client — PAMSecure SSOApps"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONPAMSecureSSOApps.Properties

### Community 2262 - "ACM Client — SFTPTerminal.LTS.v2"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, SFTP.LocalToServer.v2.Properties

### Community 2263 - "ACM Client — App Exe"
Cohesion: 0.29
Nodes (4): ARCOSLaunchSSO, Button, IContainer, Label

### Community 2264 - "ACM Client — App Exe"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSAppExeTerminal.Properties

### Community 2265 - "ACM Client — App My"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSAppMySQLAdministrator.Properties

### Community 2266 - "ACM Client — AS400Terminal"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSAS400Terminal.Properties

### Community 2267 - "ACM Client — DB2TTerminal"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSDB2TTerminal.Properties

### Community 2268 - "ACM Client — DQS"
Cohesion: 0.38
Nodes (3): DB2QueryOptions, DialogResult, IDbConnection

### Community 2269 - "ACM Client — DQS"
Cohesion: 0.38
Nodes (3): OracleQueryOptions, DialogResult, IDbConnection

### Community 2270 - "ACM Client — DQS"
Cohesion: 0.33
Nodes (4): OracleQueryParameter, EventArgs, Message, String

### Community 2271 - "ACM Client — DQS"
Cohesion: 0.33
Nodes (3): StringExt, TextBoxExt, TextBox

### Community 2272 - "ACM Client — DQS"
Cohesion: 0.33
Nodes (4): EditTableForm, EventArgs, Message, string

### Community 2273 - "ACM Client — DQS"
Cohesion: 0.38
Nodes (3): RenameProcedureForm, EventArgs, Message

### Community 2274 - "ACM Client — Framework CM"
Cohesion: 0.33
Nodes (3): KeyLoggerExtension, List, XmlDocument

### Community 2275 - "ACM Client — Framework CM"
Cohesion: 0.57
Nodes (4): CustomFormTitleBarMenus, DllImport, Int32, IntPtr

### Community 2276 - "ACM Client — Framework CM"
Cohesion: 0.29
Nodes (7): FileData, bool, byte, DateTime, int, long, string

### Community 2277 - "ACM Client — Framework CM"
Cohesion: 0.43
Nodes (3): frmAddNewData, EventArgs, String

### Community 2278 - "ACM Client — Framework CM"
Cohesion: 0.29
Nodes (5): frmExtendSessionDuration, Boolean, EventArgs, FormClosingEventArgs, String

### Community 2279 - "ACM Client — Login ACMO"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSLoginACMO.Properties

### Community 2280 - "ACM Client — MSSQLEMLocal"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSMSSQLEMLocal.Properties

### Community 2281 - "ACM Client — Oracle SDTerminal"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSOracleSDTerminal.Properties

### Community 2282 - "ACM Client — Oracle TTerminal"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSOracleTTerminal.Properties

### Community 2283 - "ACM Client — Script Manager"
Cohesion: 0.43
Nodes (4): frmEditScript, Boolean, EventArgs, String

### Community 2284 - "ACM Client — Script Manager"
Cohesion: 0.29
Nodes (6): frmIndividualCommandLogViewer_ScriptManager, Boolean, EventArgs, int, Int32, String

### Community 2285 - "ACM Client — SFTPTeminal"
Cohesion: 0.29
Nodes (4): FileOperation, Button, IContainer, Label

### Community 2286 - "ACM Client — SFTPTeminal"
Cohesion: 0.38
Nodes (3): bool, EventArgs, UnknownHostKey

### Community 2287 - "ACM Client — Smar Term"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSSmarTermSSH2.Properties

### Community 2288 - "ACM Client — Smar Term"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSSmarTermTelnet.Properties

### Community 2289 - "ACM Client — SSHTerminal"
Cohesion: 0.33
Nodes (4): APIMessageBox, bool, EventArgs, FormClosingEventArgs

### Community 2290 - "ACM Client — SSHTerminal"
Cohesion: 0.29
Nodes (4): APIMessageBox, Button, IContainer, Label

### Community 2292 - "ACM Client — Web Browser"
Cohesion: 0.29
Nodes (4): frmPageControls, ColumnHeader, IContainer, ListView

### Community 2293 - "ACM Client — Web Browser"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSWebBrowserIE.Properties

### Community 2294 - "ACM Client — Web Browserv35"
Cohesion: 0.29
Nodes (4): frmPageControls, ColumnHeader, IContainer, ListView

### Community 2295 - "ACM Client — Web Browserv35"
Cohesion: 0.29
Nodes (5): UCARCOSWebBrowserSearch, Button, IContainer, Panel, TextBox

### Community 2296 - "ACM Common — .PIMUD"
Cohesion: 0.29
Nodes (5): CheckTargateConnectivity, bool, Exception, IAsyncResult, ManualResetEvent

### Community 2297 - "ACM Common — .User Controls"
Cohesion: 0.29
Nodes (4): DgvNumRangeColumnFilter, ComboBox, IContainer, TextBox

### Community 2298 - "ACM Common — .User Controls"
Cohesion: 0.29
Nodes (4): DgvDateColumnFilter, ComboBox, DateTimePicker, IContainer

### Community 2300 - "ACM Common — Database Setting"
Cohesion: 0.67
Nodes (4): ConnectionParam2, ArrayList, Boolean, String

### Community 2301 - "ACM Common — Enitity Objects"
Cohesion: 0.29
Nodes (6): ARCOSAgwEntities, bool, DateTime, int, long, string

### Community 2302 - "ACM Common — User Access"
Cohesion: 0.43
Nodes (4): UserAccessReviewFunctions, DataTable, Int32, String

### Community 2303 - "ACM Client — Network Devices"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSAppNetnumanZTEGSM.Properties

### Community 2304 - "Services — Provisioning Service"
Cohesion: 0.48
Nodes (5): ARCONProvisioningWebAPI, ARCONProvisioningService, ARCONProvisioningServiceSetup, ProvisioningBusinessLayer, ProvisioningDataAccessLayer

### Community 2305 - "ACMO Web — Provisioning Web"
Cohesion: 0.29
Nodes (6): ARCONProvisioningWebAPI.Areas.HelpPage, ARCONProvisioningWebAPI.Areas.HelpPage.Models, System.Web.Http, System.Web.Http.Controllers, System.Web.Http.Description, IGrouping<HttpControllerDescriptor

### Community 2306 - "ACMO Web — Provisioning Web"
Cohesion: 0.29
Nodes (6): ARCONProvisioningWebAPI.Areas.HelpPage.Models, System.Collections.ObjectModel, System.Web.Http, System.Web.Http.Controllers, System.Web.Http.Description, Collection<ApiDescription>

### Community 2307 - "ACMO Web — APIRA"
Cohesion: 0.33
Nodes (4): RDPImage, DateTime, ARCOSAPIRA.Controllers, ARCOSAPIRA.Models

### Community 2308 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): frmApplicationInventory, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage

### Community 2309 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): frmAssignedViewProfile, HtmlGenericControl, Label, LinkButton, Repeater, UCResponseMessage

### Community 2311 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): frmARCOSMailBox, HtmlInputHidden, HyperLink, LinkButton, Repeater, UCResponseMessage

### Community 2312 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): Filezilla, Button, DropDownList, HiddenField, HtmlForm, HtmlInputHidden

### Community 2313 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): ReferenceLogACMO, ContentPlaceHolder, HtmlForm, HtmlHead, HyperLink, UpdatePanel

### Community 2315 - "ACMO Web — Client Manager"
Cohesion: 0.38
Nodes (3): detectEncoding(), Utf16Decoder(), Utf32AutoDecoder()

### Community 2316 - "ACMO Web — Client Manager"
Cohesion: 0.38
Nodes (7): ab(), bc(), cd(), bezierCurve(), bezierCurve(), calculateCurvePoints(), getCurvePoints()

### Community 2317 - "ACMO Web — Client Manager"
Cohesion: 0.48
Nodes (6): v(), dateGenerator(), floorInBase(), formatDate(), init(), makeUtcWrapper()

### Community 2318 - "ACMO Web — Client Manager"
Cohesion: 0.48
Nodes (5): e(), f(), g(), h(), i()

### Community 2319 - "ACMO Web — Client Manager"
Cohesion: 0.48
Nodes (5): e(), f(), g(), h(), i()

### Community 2321 - "ACMO Web — Client Manager"
Cohesion: 0.52
Nodes (6): attachWheel(), getBarHeight(), hideBar(), _onWheel(), scrollContent(), showBar()

### Community 2322 - "ACMO Web — Client Manager"
Cohesion: 0.52
Nodes (6): attachWheel(), getBarHeight(), hideBar(), _onWheel(), scrollContent(), showBar()

### Community 2323 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): frmChatWindowPopup, Button, HtmlForm, HtmlGenericControl, Label, TextBox

### Community 2324 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): UCInfoDetails, Button, HiddenField, HtmlGenericControl, Label, TextBox

### Community 2325 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): UCShowDualFactorAuth, HiddenField, HtmlGenericControl, Label, LinkButton, PlaceHolder

### Community 2326 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): UCSSHConnectionOption, Button, HtmlGenericControl, HtmlImage, LinkButton, UpdatePanel

### Community 2327 - "ACMO Web — Client Manager"
Cohesion: 0.29
Nodes (6): UCWinRDPOption, Button, HtmlGenericControl, HtmlImage, LinkButton, UpdatePanel

### Community 2329 - "ACMO Web — Common Functions"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONACMOCommonFunctions.Properties

### Community 2331 - "ACMO Web — Portal"
Cohesion: 0.48
Nodes (5): e(), f(), g(), h(), i()

### Community 2332 - "ACMO Web — Portal"
Cohesion: 0.48
Nodes (5): e(), f(), g(), h(), i()

### Community 2334 - "ACMO Web — Portal"
Cohesion: 0.52
Nodes (6): attachWheel(), getBarHeight(), hideBar(), _onWheel(), scrollContent(), showBar()

### Community 2335 - "ACMO Web — Portal"
Cohesion: 0.52
Nodes (6): attachWheel(), getBarHeight(), hideBar(), _onWheel(), scrollContent(), showBar()

### Community 2336 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (4): DgvDateRangeColumnFilter, ComboBox, DateTimePicker, IContainer

### Community 2337 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (4): DgvNumRangeColumnFilter, ComboBox, IContainer, TextBox

### Community 2338 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (4): DgvDateColumnFilter, ComboBox, DateTimePicker, IContainer

### Community 2339 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): frmAddNewData, Boolean, EventArgs, Int32, String

### Community 2340 - "ASM Server — Server Manager"
Cohesion: 0.38
Nodes (4): BigInteger, ConfidenceFactor, PrimalityTest, PrimeGeneratorBase

### Community 2342 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (3): SftpProgressMonitor, int, String

### Community 2343 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (5): frmPleaseWait, Button, IContainer, Label, Panel

### Community 2344 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (4): ARCONSSerialBox, AcceptableCharacters, EventArgs, RightToLeft

### Community 2345 - "ASM Server — Server Manager"
Cohesion: 0.38
Nodes (3): IPRangeFinder, IEnumerable, IPAddress

### Community 2346 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (5): ProcessDBLog, Boolean, DateTime, Int32, String

### Community 2347 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (6): UserAndServerRequest, Boolean, DateTime, Int32, List, String

### Community 2348 - "ASM Server — Server Manager"
Cohesion: 0.52
Nodes (4): ARCOSUpdater, Boolean, String, WebProxy

### Community 2349 - "ASM Server — Server Manager"
Cohesion: 0.38
Nodes (3): frmFullScreenImage, EventArgs, MouseEventArgs

### Community 2350 - "ASM Server — Server Manager"
Cohesion: 0.38
Nodes (4): frmSessionIDListViewer, EventArgs, List, string

### Community 2351 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (5): frmSplashScreenServer, IContainer, Label, Panel, PictureBox

### Community 2352 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkExtractParams, NativeULong, CK_EXTRACT_PARAMS

### Community 2353 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkMacGeneralParams, NativeULong, CK_MAC_GENERAL_PARAMS

### Community 2354 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2MacGeneralParams, NativeULong, CK_RC2_MAC_GENERAL_PARAMS

### Community 2355 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2Params, NativeULong, CK_RC2_PARAMS

### Community 2356 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5MacGeneralParams, NativeULong, CK_RC5_MAC_GENERAL_PARAMS

### Community 2357 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5Params, NativeULong, CK_RC5_PARAMS

### Community 2358 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRsaPkcsPssParams, NativeULong, CK_RSA_PKCS_PSS_PARAMS

### Community 2359 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkTlsMacParams, NativeULong, CK_TLS_MAC_PARAMS

### Community 2360 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkExtractParams, NativeULong, CK_EXTRACT_PARAMS

### Community 2361 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkMacGeneralParams, NativeULong, CK_MAC_GENERAL_PARAMS

### Community 2362 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2MacGeneralParams, NativeULong, CK_RC2_MAC_GENERAL_PARAMS

### Community 2363 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2Params, NativeULong, CK_RC2_PARAMS

### Community 2364 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5MacGeneralParams, NativeULong, CK_RC5_MAC_GENERAL_PARAMS

### Community 2365 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5Params, NativeULong, CK_RC5_PARAMS

### Community 2366 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRsaPkcsPssParams, NativeULong, CK_RSA_PKCS_PSS_PARAMS

### Community 2367 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkTlsMacParams, NativeULong, CK_TLS_MAC_PARAMS

### Community 2368 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkExtractParams, NativeULong, CK_EXTRACT_PARAMS

### Community 2369 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkMacGeneralParams, NativeULong, CK_MAC_GENERAL_PARAMS

### Community 2370 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2MacGeneralParams, NativeULong, CK_RC2_MAC_GENERAL_PARAMS

### Community 2371 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2Params, NativeULong, CK_RC2_PARAMS

### Community 2372 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5MacGeneralParams, NativeULong, CK_RC5_MAC_GENERAL_PARAMS

### Community 2373 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5Params, NativeULong, CK_RC5_PARAMS

### Community 2374 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRsaPkcsPssParams, NativeULong, CK_RSA_PKCS_PSS_PARAMS

### Community 2375 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkTlsMacParams, NativeULong, CK_TLS_MAC_PARAMS

### Community 2376 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkExtractParams, NativeULong, CK_EXTRACT_PARAMS

### Community 2377 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkMacGeneralParams, NativeULong, CK_MAC_GENERAL_PARAMS

### Community 2378 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2MacGeneralParams, NativeULong, CK_RC2_MAC_GENERAL_PARAMS

### Community 2379 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc2Params, NativeULong, CK_RC2_PARAMS

### Community 2380 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5MacGeneralParams, NativeULong, CK_RC5_MAC_GENERAL_PARAMS

### Community 2381 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRc5Params, NativeULong, CK_RC5_PARAMS

### Community 2382 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkRsaPkcsPssParams, NativeULong, CK_RSA_PKCS_PSS_PARAMS

### Community 2383 - "ASM Server — Pkcs11Interop"
Cohesion: 0.29
Nodes (4): bool, CkTlsMacParams, NativeULong, CK_TLS_MAC_PARAMS

### Community 2384 - "ASM Server — Server Manager"
Cohesion: 0.29
Nodes (4): SetUp, Test, frmAboutBoxTest, ServerManagerNUnitTest

### Community 2385 - "Common — .User Controls"
Cohesion: 0.29
Nodes (4): DgvNumRangeColumnFilter, ComboBox, IContainer, TextBox

### Community 2386 - "Common — .User Controls"
Cohesion: 0.29
Nodes (4): DgvTextBoxColumnFilter, ComboBox, IContainer, TextBox

### Community 2387 - "Common — SLPF"
Cohesion: 0.38
Nodes (4): BigInteger, ConfidenceFactor, PrimalityTest, PrimeGeneratorBase

### Community 2389 - "Common — SLPF"
Cohesion: 0.29
Nodes (3): SftpProgressMonitor, int, String

### Community 2390 - "Common — SUtil"
Cohesion: 0.38
Nodes (3): IPRangeFinder, IEnumerable, IPAddress

### Community 2391 - "Common — Enitity Objects"
Cohesion: 0.29
Nodes (6): ARCOSAgwEntities, bool, DateTime, int, long, string

### Community 2392 - "Common — Enitity Objects"
Cohesion: 0.52
Nodes (6): IDAM, IdamAgentDetails, IdamService, Boolean, DateTime, String

### Community 2393 - "Common — Enitity Objects"
Cohesion: 0.29
Nodes (6): UserLoginAttempt, Boolean, DateTime, Int32, long, String

### Community 2394 - "Common — Server Common Functions"
Cohesion: 0.52
Nodes (4): ARCOSUpdater, Boolean, String, WebProxy

### Community 2395 - "Services — Active Directory Insight"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONActiveDirectoryInsight.Properties

### Community 2396 - "Services — ADScanner Service"
Cohesion: 0.29
Nodes (5): DomainServers, DomainServersProtocolType, Boolean, Int32, string

### Community 2397 - "Services — Alert Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSAlertService.Properties

### Community 2398 - "Services — PAM Agents"
Cohesion: 0.29
Nodes (4): ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller

### Community 2399 - "Services — PAM Agents"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONPAMThickClientPortable.Properties

### Community 2400 - "Services — PAM Agents"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, KeepAliveAPP.Properties

### Community 2401 - "Services — Cloud File Uploader"
Cohesion: 0.29
Nodes (4): ProjectInstaller, IContainer, ServiceInstaller, ServiceProcessInstaller

### Community 2402 - "Services — Data Sync"
Cohesion: 0.38
Nodes (6): ARCOSDataSyncServiceSettings, SyncOrderType, TimeBetween, Boolean, Int32, String

### Community 2403 - "Services — Desk Insight"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONDeskInsight.Properties

### Community 2404 - "Services — Desk Insight"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONDeskInsightUpdater.Properties

### Community 2405 - "Services — Desk Insight"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONRStreamServer.Properties

### Community 2406 - "Services — Desk Insight"
Cohesion: 0.29
Nodes (4): frmAllElevatedApps, DataGridView, IContainer, Label

### Community 2407 - "Services — Desk Insight"
Cohesion: 0.38
Nodes (4): Logger, LogType, Lazy, LogType

### Community 2408 - "Services — Desk Insight"
Cohesion: 0.38
Nodes (6): Facial_Recog, Facial_Respone, facil_Respone, ImageResult, MultipleFacialImages, List

### Community 2409 - "Services — Desk Insight"
Cohesion: 0.38
Nodes (3): IPRangeFinder, IEnumerable, IPAddress

### Community 2410 - "Services — Desk Insight"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONDeskInsightTestClient.Properties

### Community 2411 - "Services — Desk Insight Master"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONDeskInsightMaster.Properties

### Community 2412 - "Services — Folder Sync Service"
Cohesion: 0.33
Nodes (4): Dictionary, IList, string, MultiKeyCollection

### Community 2413 - "Services — Folder Sync Service"
Cohesion: 0.29
Nodes (4): bool, Form, Thread, SplashScreen

### Community 2414 - "Services — Folder Sync Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONFolderSyncService.Properties

### Community 2415 - "Services — Log Archiver Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSLogArchiverService_Cloud.Properties

### Community 2416 - "Services — Migrate Data Utility"
Cohesion: 0.29
Nodes (5): frmPleaseWait, Button, IContainer, Label, Panel

### Community 2417 - "Services — Migrate Data Utility"
Cohesion: 0.38
Nodes (5): CommandType, SqlCommand, SqlConnection, SqlParameter, SqlTransaction

### Community 2418 - "Services — Migrate Data Utility"
Cohesion: 0.29
Nodes (5): FingerPrints, String, FingerPrints, String, ARCOSPasswordeEnvelopeManager.Resources

### Community 2419 - "Services — Password Change Vault"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ArconPamVault.Properties

### Community 2421 - "Services — Passworde Envelope Manager"
Cohesion: 0.33
Nodes (3): frmdownloadsshkey, EventArgs, string

### Community 2422 - "Services — Perf Mon IT"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSPerfMonIT.Properties

### Community 2423 - "Services — Provisioning Scheduler"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSProvisioningReconConsole.Properties

### Community 2424 - "Services — Provisioning Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCONProvisioningService.Properties

### Community 2425 - "Services — Schedule Password Change"
Cohesion: 0.38
Nodes (4): BigInteger, ConfidenceFactor, PrimalityTest, PrimeGeneratorBase

### Community 2426 - "Services — Schedule Password Change"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSSPCService.Properties

### Community 2427 - "Services — Schedule Password Change"
Cohesion: 0.38
Nodes (4): BigInteger, ConfidenceFactor, PrimalityTest, PrimeGeneratorBase

### Community 2429 - "Services — Schedule Password Change"
Cohesion: 0.29
Nodes (3): SftpProgressMonitor, int, String

### Community 2430 - "Services — Schedule Password Change"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSSPCViewedPasswordService.Properties

### Community 2431 - "Services — Script Scheduler"
Cohesion: 0.29
Nodes (7): bool, byte, DateTime, int, long, string, FileData

### Community 2432 - "Services — Script Scheduler"
Cohesion: 0.29
Nodes (4): IContainer, ServiceInstaller, ServiceProcessInstaller, ProjectInstaller

### Community 2433 - "Services — Staging Log Sync"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, StagingLogSyncService.Properties

### Community 2434 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSFileWatcher.Properties

### Community 2435 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (4): DgvDateColumnFilter, ComboBox, DateTimePicker, IContainer

### Community 2436 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (4): DgvTextBoxColumnFilter, ComboBox, IContainer, TextBox

### Community 2437 - "Services — TSPlugin Service"
Cohesion: 0.38
Nodes (3): IPRangeFinder, IEnumerable, IPAddress

### Community 2438 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (5): ProcessDBLog, Boolean, DateTime, Int32, String

### Community 2439 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (6): UserAndServerRequest, Boolean, DateTime, Int32, List, String

### Community 2440 - "Services — TSPlugin Service"
Cohesion: 0.38
Nodes (3): byte, int, Base64

### Community 2441 - "Services — TSPlugin Service"
Cohesion: 0.29
Nodes (4): Assembly, ResourceManager, string, StringResources

### Community 2442 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSTSMonitor.Properties

### Community 2443 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSTSPlugin.Properties

### Community 2444 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): Resources, CultureInfo, ResourceManager, Settings, ARCOSUserActivity.Properties

### Community 2445 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, IApp.Properties

### Community 2446 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, StartApp.Properties

### Community 2447 - "Services — Windows Vaulting Service"
Cohesion: 0.29
Nodes (3): Task, TcpClient, DataProtector

### Community 2448 - "Services — Windows Vaulting Service"
Cohesion: 0.29
Nodes (4): IContainer, ServiceInstaller, ServiceProcessInstaller, ProjectInstaller

### Community 2449 - "Services — Z POC"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, PasswordChangeIPv6.Properties

### Community 2450 - "Services — Z POC"
Cohesion: 0.33
Nodes (5): CultureInfo, ResourceManager, Resources, Settings, SSH_Key_Debugger.Properties

### Community 2451 - "User Discovery — Logger"
Cohesion: 0.29
Nodes (3): Logger, Exception, IPAddress

### Community 2452 - "Onboarding — Updater"
Cohesion: 0.52
Nodes (4): ARCOSUpdater, Boolean, String, WebProxy

### Community 2453 - "Offline MultiTab — Service Installer"
Cohesion: 0.33
Nodes (5): WindowsFormsApp1.Properties, CultureInfo, ResourceManager, Resources, Settings

### Community 2454 - "MultiTab — src"
Cohesion: 0.33
Nodes (3): Library, ARCONPAMSecurity, ARCONPAMSecurityUtility

### Community 2456 - "SSM — Arcoss SSMDesktop"
Cohesion: 0.33
Nodes (4): SSMMessageBox, bool, EventArgs, FormClosingEventArgs

### Community 2457 - "ACM Client — App Exe"
Cohesion: 0.33
Nodes (3): frmFillCredentials, Button, IContainer

### Community 2459 - "ACM Client — DQS"
Cohesion: 0.33
Nodes (3): ConnectingForm, IContainer, Label

### Community 2460 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): FileUtil, string, StringCollection

### Community 2461 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): FindReplaceForm, EventArgs, Message

### Community 2462 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): AddViewForm, EventArgs, Message

### Community 2463 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameColumnForm, EventArgs, Message

### Community 2464 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameCONSTRAINTForm, EventArgs, Message

### Community 2465 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameDBLINKForm, EventArgs, Message

### Community 2466 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameFunctionForm, EventArgs, Message

### Community 2467 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameIndexForm, EventArgs, Message

### Community 2468 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameMaterializedViewForm, EventArgs, Message

### Community 2469 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameMaterializedViewLogForm, EventArgs, Message

### Community 2470 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenamePackageForm, EventArgs, Message

### Community 2471 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameSEQUENCEForm, EventArgs, Message

### Community 2472 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameSYNONYMForm, EventArgs, Message

### Community 2473 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameTableForm, EventArgs, Message

### Community 2474 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameTableSpaceForm, EventArgs, Message

### Community 2475 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameTRIGGERForm, EventArgs, Message

### Community 2476 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameTYPEForm, EventArgs, Message

### Community 2477 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameUSERForm, EventArgs, Message

### Community 2478 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): RenameViewForm, EventArgs, Message

### Community 2479 - "ACM Client — Framework CM"
Cohesion: 0.33
Nodes (5): ARCOSApproverDetails_temp, int, Int32, long, string

### Community 2480 - "ACM Client — Framework CM"
Cohesion: 0.33
Nodes (3): CertificateAuthTunnel, Process, string

### Community 2481 - "ACM Client — Framework CM"
Cohesion: 0.33
Nodes (3): frmErrorMessage, IContainer, Label

### Community 2482 - "ACM Client — Oracle Query"
Cohesion: 0.33
Nodes (4): Program, STAThread, StaticCommonFunctions, ServerSessionLogger

### Community 2483 - "ACM Client — Oracle Query"
Cohesion: 0.33
Nodes (5): Resources, Bitmap, CultureInfo, ResourceManager, ARCOSOracleQueryAnalyser.Properties

### Community 2484 - "ACM Client — RDPTerminal"
Cohesion: 0.33
Nodes (3): ReconnectForm, EventArgs, FormClosingEventArgs

### Community 2485 - "ACM Client — SFTPTeminal"
Cohesion: 0.33
Nodes (5): Resources, Bitmap, CultureInfo, ResourceManager, ARCOSSFTPTeminal.Properties

### Community 2486 - "ACM Client — Web Browser"
Cohesion: 0.33
Nodes (3): frmPageSource, IContainer, TextBox

### Community 2487 - "ACM Client — Web Browserv35"
Cohesion: 0.33
Nodes (3): UCARCOSWebBrowserOperations, Button, IContainer

### Community 2488 - "ACM Common — .User Controls"
Cohesion: 0.33
Nodes (3): DgvMonthYearColumnFilter, ComboBox, IContainer

### Community 2490 - "ACMO Web — Provisioning Web"
Cohesion: 0.33
Nodes (5): ARCONProvisioningWebAPI.Areas.HelpPage.ModelDescriptions, ARCONProvisioningWebAPI.Areas.HelpPage.Models, HelpPageApiModel, System.Web.Http, System.Web.Http.Description

### Community 2492 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): frmOnboardingDashboard, HtmlGenericControl, HtmlInputHidden, LinkButton, UpdatePanel

### Community 2493 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): frmSecretAuditTrail, HiddenField, HtmlGenericControl, Label, UCResponseMessage

### Community 2494 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): ReferenceLog, GridView, Label, Panel, UCResponseMessage

### Community 2496 - "ACMO Web — Client Manager"
Cohesion: 0.53
Nodes (4): Capture(), CommunicateBiometricSDK(), DeviceInfo(), getHttpError()

### Community 2497 - "ACMO Web — Client Manager"
Cohesion: 0.47
Nodes (6): deflate_fast(), deflate_slow(), fill_window(), flush_block_only(), flush_pending(), longest_match()

### Community 2498 - "ACMO Web — Client Manager"
Cohesion: 0.60
Nodes (5): dateGenerator(), floorInBase(), formatDate(), init(), makeUtcWrapper()

### Community 2499 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (6): attachToScrollParents(), disableEventListeners(), getScrollParent(), getWindow(), removeEventListeners(), setupEventListeners()

### Community 2500 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): SamlService, HtmlForm, HtmlGenericControl, Image, Panel

### Community 2501 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (3): Test, DataTable, EventArgs

### Community 2502 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): TestPage, HtmlAnchor, HtmlForm, HtmlImage, Label

### Community 2503 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): UCInfo, Button, HtmlGenericControl, Label, TextBox

### Community 2504 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): UCIBMAS400Option, Button, HtmlGenericControl, LinkButton, UpdatePanel

### Community 2505 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): UCLoginStatus, HyperLink, Label, LinkButton, UCUserDetails

### Community 2506 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): UCViewHistory, DropDownList, HtmlGenericControl, Label, Repeater

### Community 2507 - "ACMO Web — Client Manager"
Cohesion: 0.33
Nodes (5): UCResponseMessage, HtmlGenericControl, Image, Label, UpdatePanel

### Community 2508 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): urlmonMimeDetect, DllImport, IntPtr, HttpPostedFile

### Community 2509 - "ACMO Web — Common Functions"
Cohesion: 0.40
Nodes (5): SessionLogFilter_Web, ViewWorkflowTracker_Web, int, List, String

### Community 2510 - "ACMO Web — Portal"
Cohesion: 0.33
Nodes (5): MasterLogin, ContentPlaceHolder, HiddenField, HtmlForm, HtmlHead

### Community 2511 - "ACMO Web — Portal"
Cohesion: 0.40
Nodes (6): absCeil(), as(), bubble(), daysToMonths(), makeAs(), monthsToDays()

### Community 2512 - "ACMO Web — Portal"
Cohesion: 0.47
Nodes (6): ab(), bc(), cd(), bezierCurve(), bezierCurve(), getCurvePoints()

### Community 2513 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): ARCOSLinkedDomainParameter, bool, Boolean, int, string

### Community 2514 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (6): ARCOSLobWiseGlobalConfiguration, bool, DateTime, int, Int32, string

### Community 2515 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (5): APIGenericResponse, CustomApplicationError, bool, Exception, string

### Community 2516 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): NewDevies, Boolean, DateTime, Int32, String

### Community 2517 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): ServiceLogRealTime, Image, int, Int32, String

### Community 2518 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): UserLoginAttempt, Boolean, DateTime, Int32, String

### Community 2519 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (3): EmbeddedAssembly, Assembly, Dictionary

### Community 2520 - "ASM Server — Pkcs11Interop"
Cohesion: 0.33
Nodes (4): SerializationInfo, StreamingContext, string, Pkcs11Exception

### Community 2521 - "ASM Server — Pkcs11Interop"
Cohesion: 0.33
Nodes (4): int, SerializationInfo, StreamingContext, UnmanagedException

### Community 2522 - "ASM Server — Server Manager"
Cohesion: 0.33
Nodes (5): netcoreapp3.1, Microsoft.NET.Test.Sdk (16.5.0), NUnit (3.12.0), NUnit3TestAdapter (3.16.1), Microsoft.NET.Sdk

### Community 2523 - "Common — .User Controls"
Cohesion: 0.33
Nodes (3): DgvMonthYearColumnFilter, ComboBox, IContainer

### Community 2524 - "Common — Password Manager"
Cohesion: 0.33
Nodes (5): ARCONSPCServiceSettings, bool, DateTime, int, string

### Community 2526 - "Common — Enitity Objects"
Cohesion: 0.33
Nodes (5): ApplicationLog, DateTime, int, Int32, String

### Community 2527 - "Common — Enitity Objects"
Cohesion: 0.33
Nodes (5): ARCOSLinkedDomainParameter, bool, Boolean, int, string

### Community 2528 - "Common — Enitity Objects"
Cohesion: 0.33
Nodes (6): ARCOSLobWiseGlobalConfiguration, bool, DateTime, int, Int32, string

### Community 2529 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (5): APIGenericResponse, CustomApplicationError, bool, Exception, string

### Community 2530 - "Common — Enitity Objects"
Cohesion: 0.33
Nodes (5): NewDevies, Boolean, DateTime, Int32, String

### Community 2533 - "Services — Alert Service"
Cohesion: 0.47
Nodes (4): CriticalWithApprovalRequest, DataTable, Hashtable, String

### Community 2534 - "Services — Auto Healing"
Cohesion: 0.33
Nodes (5): ARCONAHServiceSettings, bool, DateTime, int, string

### Community 2535 - "Services — Services.NUnit Test"
Cohesion: 0.33
Nodes (5): net472, Microsoft.NET.Test.Sdk (16.5.0), NUnit (3.12.0), NUnit3TestAdapter (3.16.1), Microsoft.NET.Sdk

### Community 2536 - "Services — DBSync Service"
Cohesion: 0.33
Nodes (5): Resources, Bitmap, CultureInfo, ResourceManager, ARCOSDBSyncCommon.Properties

### Community 2537 - "Services — Desk Insight"
Cohesion: 0.33
Nodes (3): frmARCONDeskInsight, IContainer, Winsock

### Community 2539 - "Services — Desk Insight"
Cohesion: 0.47
Nodes (3): IntPtr, WlanAvailableNetwork, WlanGetAvailableNetworkFlags

### Community 2540 - "Services — Password Change Vault"
Cohesion: 0.33
Nodes (5): bool, int, string, ReconciliationResponse, Models.Reconciliation

### Community 2541 - "Services — Provisioning Service"
Cohesion: 0.40
Nodes (3): MySqlConnection, AuditLog, ProvisioningDataAccessLayer.Audit

### Community 2542 - "Services — Schedule Password Change"
Cohesion: 0.33
Nodes (4): Program, STAThread, Task, ARCONPCQEngine

### Community 2543 - "Services — Schedule Password Change"
Cohesion: 0.33
Nodes (4): Program, STAThread, Task, ARCONQueueEngine

### Community 2544 - "Services — Script Scheduler"
Cohesion: 0.33
Nodes (5): bool, DateTime, int, string, ScriptSchedulerClass

### Community 2545 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (5): ActivityLog, APIMethods, DateTime, int, string

### Community 2546 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): ARCOSLinkedDomainParameter, bool, Boolean, int, string

### Community 2547 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (6): ARCOSLobWiseGlobalConfiguration, bool, DateTime, int, Int32, string

### Community 2548 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): NewDevies, Boolean, DateTime, Int32, String

### Community 2549 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (5): UserLoginAttempt, Boolean, DateTime, Int32, String

### Community 2550 - "Services — TSPlugin Service"
Cohesion: 0.33
Nodes (3): frmDatabaseConnectionPleaseWait, IContainer, Label

### Community 2551 - "Services — Windows Vaulting Service"
Cohesion: 0.33
Nodes (3): bool, SafeHandle, WindowsIOFileOperations

### Community 2552 - "Services — Z POC"
Cohesion: 0.33
Nodes (4): netcoreapp3.1, System.Data.SqlClient (4.8.5), Microsoft.NET.Sdk, MySql.Data (8.1.0)

### Community 2556 - "ACM Client — DQS"
Cohesion: 0.40
Nodes (3): HeaderFormates, EventArgs, Message

### Community 2557 - "ACM Client — Framework CM"
Cohesion: 0.50
Nodes (3): frmServiceProcessLog, EventArgs, string

### Community 2558 - "ACM Client — Framework CM"
Cohesion: 0.50
Nodes (3): SystemInfoCapture, bool, IEnumerable

### Community 2560 - "ACM Client — RDPTerminal"
Cohesion: 0.40
Nodes (3): frmRDPWait, EventArgs, FormClosedEventArgs

### Community 2561 - "ACMO Web — Client Manager"
Cohesion: 0.60
Nodes (3): Settings, Settings, My

### Community 2562 - "ACM Client — Script Manager"
Cohesion: 0.50
Nodes (3): frmViewScriptManagerLoggedData, EventArgs, Int32

### Community 2563 - "ACM Client — SFTPTeminal"
Cohesion: 0.40
Nodes (3): NewNamePrompt, EventArgs, Message

### Community 2565 - "ACM Client — SSHTerminal"
Cohesion: 0.40
Nodes (4): CultureInfo, ResourceManager, Resources, PCSSSH.Properties

### Community 2566 - "ACM Client — VNCTerminal"
Cohesion: 0.40
Nodes (4): CultureInfo, ResourceManager, Resources, VncSharp.Properties

### Community 2567 - "ACM Client — Web Browser"
Cohesion: 0.50
Nodes (3): frmPageSource, PageSourceType, EventArgs

### Community 2568 - "ACM Client — Web Browser"
Cohesion: 0.50
Nodes (3): MenuHandler, IMenuHandler, IWebBrowser

### Community 2570 - "ACM Common — Enitity Objects"
Cohesion: 0.40
Nodes (5): OfflineTicketGeneration, bool, DateTime, Int32, String

### Community 2571 - "ACM Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): SessionLogActivity, SessionLogConfig, SessionLogDetails, Int64

### Community 2572 - "ACM Common — Enitity Objects"
Cohesion: 0.40
Nodes (3): ViewPasswordUserData, long, string

### Community 2573 - "Services — User On Boarding"
Cohesion: 0.40
Nodes (3): VaultUser, int, string

### Community 2575 - "ACMO Web — APIOnline"
Cohesion: 0.40
Nodes (3): ARCOSLogMethod, ServerConnection, ARCOSLogMethod

### Community 2578 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): CultureInfo, ResourceManager, Resource, ResourcesAcmo

### Community 2579 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (3): BundleConfig, BundleCollection, ARCOSClientManagerOnline.App_Start

### Community 2580 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): frmChangePasswordManually, Button, RadioButton, TextBox

### Community 2583 - "ACMO Web — Client Manager"
Cohesion: 0.70
Nodes (4): a(), b(), c(), d()

### Community 2584 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): AdminSAML, HtmlForm, ScriptManager, UCResponseMessage

### Community 2585 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): UCSSOLoginStatus, Button, HtmlGenericControl, Label

### Community 2586 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): UCSSOResponseMessage, HtmlGenericControl, Label, UpdatePanel

### Community 2587 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (3): UCPanelHeader, EventArgs, String

### Community 2588 - "ACMO Web — Client Manager"
Cohesion: 0.40
Nodes (4): UCPanelHeader, HtmlGenericControl, Image, Label

### Community 2591 - "ACMO Web — Portal"
Cohesion: 0.70
Nodes (4): a(), b(), c(), d()

### Community 2592 - "ACMO Web — Portal"
Cohesion: 0.40
Nodes (4): UCLoginStatus, Label, LinkButton, UCUserDetails

### Community 2593 - "ACMO Web — Staging Log"
Cohesion: 0.40
Nodes (4): Default, Button, HtmlForm, Label

### Community 2594 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (3): AssemblyDetails, Assembly, DateTime

### Community 2596 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (3): ARCONSSerialBox, IContainer, Label

### Community 2597 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (4): ApplicationLog, DateTime, Int32, String

### Community 2598 - "ASM Server — Server Manager"
Cohesion: 0.50
Nodes (4): ARCOSDelegation, DelegationDetail, DelegationMaster, DateTime

### Community 2599 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (4): ARCOSMailBox, Boolean, Int32, String

### Community 2600 - "ASM Server — Server Manager"
Cohesion: 0.40
Nodes (4): ARCOSOnBoardingConfigParameter, bool, int, string

### Community 2601 - "ASM Server — Server Manager"
Cohesion: 0.50
Nodes (3): ARCOSServiceReference, Boolean, String

### Community 2602 - "ASM Server — Pkcs11Interop"
Cohesion: 0.40
Nodes (3): SerializationInfo, StreamingContext, AttributeValueException

### Community 2603 - "ASM Server — Pkcs11Interop"
Cohesion: 0.40
Nodes (3): uint, ulong, CK

### Community 2604 - "ASM Server — Pkcs11Interop"
Cohesion: 0.40
Nodes (4): char, int, string, Pkcs11UriSpec

### Community 2605 - "ASM Server — Pkcs11Interop"
Cohesion: 0.40
Nodes (3): bool, int, Platform

### Community 2608 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): ARCOSCommonSelectParameter, int, long, string

### Community 2609 - "Common — Enitity Objects"
Cohesion: 0.50
Nodes (4): ARCOSDelegation, DelegationDetail, DelegationMaster, DateTime

### Community 2610 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): ARCOSMailBox, Boolean, Int32, String

### Community 2611 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): ARCOSOnBoardingConfigParameter, bool, int, string

### Community 2612 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): ARCOSLogsOnWebParam, ARCOSReportParam, int, String

### Community 2613 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): ImageDetailsModel, ImageValidation, ResponseSessionLog, Int64

### Community 2614 - "Common — Enitity Objects"
Cohesion: 0.50
Nodes (3): ARCOSServiceReference, Boolean, String

### Community 2615 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): SessionLogActivity, SessionLogConfig, SessionLogDetails, Int64

### Community 2616 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (4): SSO_PreferencePath_Pwd, int, long, string

### Community 2617 - "Common — Enitity Objects"
Cohesion: 0.40
Nodes (3): ViewPasswordUserData, long, string

### Community 2618 - "Services — ADScanner Service"
Cohesion: 0.40
Nodes (4): bool, DateTime, string, UserProperties

### Community 2622 - "Services — DBSync Service"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCOSDBSyncService.Properties

### Community 2623 - "Services — Desk Insight"
Cohesion: 0.70
Nodes (4): AWS, Azure, CloudParameterResponse, Google

### Community 2624 - "Services — Desk Insight"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCONUBACommon.Properties

### Community 2625 - "Services — Folder Sync Service"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCONFolderSyncConfig.Properties

### Community 2626 - "Services — Log Manager Service"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCOSLogManagerService.Properties

### Community 2627 - "Services — Log Manager Service"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCOSLogManagerServiceONS.Properties

### Community 2629 - "Services — Privilege User Discovery"
Cohesion: 0.40
Nodes (4): Boolean, Int32, ARCONApp, UserDiscovery.ARCON_Common

### Community 2630 - "Services — Provisioning Service"
Cohesion: 0.40
Nodes (4): Resource, CultureInfo, ResourceManager, ARCONProvisioningService.App_GlobalResources

### Community 2631 - "Services — Provisioning Service"
Cohesion: 0.40
Nodes (4): Resource, CultureInfo, ResourceManager, Arcos_BL.docs

### Community 2632 - "Services — Schedule Password Change"
Cohesion: 0.40
Nodes (4): Microsoft.NET.Sdk, net8.0, Azure.Identity (1.17.0), Azure.Security.KeyVault.Secrets (4.8.0)

### Community 2633 - "Services — Script Scheduler"
Cohesion: 0.50
Nodes (3): bool, IEnumerable, SystemInfoCapture

### Community 2635 - "Services — SIEMConnector Service"
Cohesion: 0.40
Nodes (4): Resources, CultureInfo, ResourceManager, ARCOSSIEMConnectorService.Properties

### Community 2636 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (4): ApplicationLog, DateTime, Int32, String

### Community 2637 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (4): ARCOSCommonModifyParameter, Byte, int, string

### Community 2638 - "Services — TSPlugin Service"
Cohesion: 0.50
Nodes (4): ARCOSDelegation, DelegationDetail, DelegationMaster, DateTime

### Community 2639 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (4): ARCOSFileStorageEntity, byte, Int32, String

### Community 2640 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (4): ARCOSOnBoardingConfigParameter, bool, int, string

### Community 2641 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (4): ServiceLogRealTime, Image, Int32, String

### Community 2642 - "Services — TSPlugin Service"
Cohesion: 0.50
Nodes (3): ARCOSServiceReference, Boolean, String

### Community 2643 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (3): ViewPasswordUserData, Int32, string

### Community 2644 - "Services — TSPlugin Service"
Cohesion: 0.40
Nodes (5): bool, int, long, string, SCPEntry

### Community 2645 - "Services — Z POC"
Cohesion: 0.40
Nodes (4): netcoreapp3.1, System.Data.SqlClient (4.8.5), Microsoft.NET.Sdk, System.Configuration.ConfigurationManager (7.0.0)

### Community 2646 - "Datum Bridge Client"
Cohesion: 0.40
Nodes (3): MYSQLParam, IDbCommand, MySqlParameter

### Community 2651 - "ACM Client — DQS"
Cohesion: 0.50
Nodes (4): DBObjectProperties, bool, object, string

### Community 2653 - "ACM Client — Framework CM"
Cohesion: 0.67
Nodes (3): ObjectTextData, TextDataOCR, DateTime

### Community 2655 - "ACM Client — Framework CM"
Cohesion: 0.50
Nodes (3): RealTimeSessionList, DataTable, Int32

### Community 2657 - "ACM Client — Script Manager"
Cohesion: 0.50
Nodes (4): frmScriptVersionHistory, DataTable, ListViewItem, String

### Community 2667 - "ACM Common — .API.Models"
Cohesion: 0.50
Nodes (3): ArcosFileStorage, FileServerDetails, DateTime

### Community 2669 - "ACM Common — Server Common"
Cohesion: 0.50
Nodes (3): frmDatabaseConnectionPleaseWait, EventArgs, String

### Community 2672 - "ACMO Web — Provisioning Web"
Cohesion: 0.50
Nodes (3): ARCONProvisioningWebAPI.Areas.HelpPage.Models, HelpPageApiModel, System.Web.Http

### Community 2673 - "ACMO Web — Provisioning Web"
Cohesion: 0.50
Nodes (3): ARCONProvisioningWebAPI.Areas.HelpPage.ModelDescriptions, ModelDescription, System.Web.Http

### Community 2675 - "ACMO Web — Client Manager"
Cohesion: 0.50
Nodes (3): frmARCOSOnboardLanding, HtmlGenericControl, Label

### Community 2682 - "ACMO Web — Client Manager"
Cohesion: 0.83
Nodes (3): connectToArconExtension(), getExtensionIds(), injectErrorPopup()

### Community 2685 - "ACMO Web — Client Manager"
Cohesion: 0.83
Nodes (3): drawSeries(), init(), processRawData()

### Community 2686 - "ACMO Web — Client Manager"
Cohesion: 0.83
Nodes (3): drawSeries(), init(), processRawData()

### Community 2690 - "ACMO Web — Client Manager"
Cohesion: 0.50
Nodes (3): TrialLicenseKey, string, ComponentPro

### Community 2699 - "ACMO Web — Portal"
Cohesion: 0.83
Nodes (3): drawSeries(), init(), processRawData()

### Community 2700 - "ACMO Web — Portal"
Cohesion: 0.83
Nodes (3): drawSeries(), init(), processRawData()

### Community 2707 - "ASM Server — Server Manager"
Cohesion: 0.50
Nodes (3): frmDatabaseConnectionPleaseWait, EventArgs, String

### Community 2712 - "Common — .API.Models"
Cohesion: 0.50
Nodes (3): ArcosFileStorage, FileServerDetails, DateTime

### Community 2713 - "Common — .API.Models"
Cohesion: 0.67
Nodes (3): PasswordPolicySettingsDetails, TypesOfAccessOfSecrets, DateTime

### Community 2714 - "Common — Password Manager"
Cohesion: 0.50
Nodes (3): SslPolicyErrors, X509Certificate, X509Chain

### Community 2717 - "Common — Server Common Functions"
Cohesion: 0.50
Nodes (3): frmDatabaseConnectionPleaseWait, EventArgs, String

### Community 2719 - "Common — Common Functions"
Cohesion: 0.50
Nodes (3): IsProvided, RefDetails, RefType

### Community 2720 - "Common — Common Functions"
Cohesion: 0.50
Nodes (3): SslPolicyErrors, X509Certificate, X509Chain

### Community 2724 - "Services — Alert Service"
Cohesion: 0.50
Nodes (3): SslPolicyErrors, X509Certificate, X509Chain

### Community 2725 - "Services — Desk Insight"
Cohesion: 0.83
Nodes (3): OfflineRequestParameters, RaiseRequestParameters, List

### Community 2726 - "Services — Desk Insight"
Cohesion: 0.50
Nodes (4): bool, ManualResetEvent, Point, Utility

### Community 2727 - "Services — Desk Insight"
Cohesion: 0.50
Nodes (3): Program, ILog, STAThread

### Community 2729 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2730 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2731 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2732 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2733 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2734 - "Services — Log Archiver Service"
Cohesion: 0.50
Nodes (3): Resources, CultureInfo, ResourceManager

### Community 2737 - "Services — TSPlugin Service"
Cohesion: 0.50
Nodes (3): ARCOSCommonSelectParameter, int, string

### Community 2739 - "Services — TSPlugin Service"
Cohesion: 0.50
Nodes (3): ServicesParamConfig, int, String

### Community 2740 - "Services — TSPlugin Service"
Cohesion: 0.50
Nodes (3): frmDatabaseConnectionPleaseWait, EventArgs, String

### Community 2742 - "Services — User On Boarding"
Cohesion: 0.50
Nodes (4): ARCOSOnBoarding, DateTime, int, string

### Community 2744 - "Datum Bridge"
Cohesion: 0.67
Nodes (3): ParameterizedConnectionString, ParameterizedConnectionStringRA, string

### Community 2745 - "Datum Bridge"
Cohesion: 0.50
Nodes (3): MSSQLParam, IDbCommand, SqlParameter

### Community 2746 - "Onboarding — Common Modify Parameter"
Cohesion: 0.50
Nodes (4): ARCOSCommonModifyParameter, Byte, int, string

### Community 2749 - "ACM Client — RStream Client"
Cohesion: 0.67
Nodes (3): Program, string, Mutex

### Community 2753 - "ACM Client — SSHTerminal"
Cohesion: 0.67
Nodes (3): NEWTEXTMETRICEX, FONTSIGNATURE, NEWTEXTMETRIC

### Community 2784 - "ACMO Web — Portal"
Cohesion: 0.67
Nodes (3): Datepicker(), datepicker_bindHover(), datepicker_handleMouseover()

### Community 2793 - "ASM Server — Server Manager"
Cohesion: 0.67
Nodes (3): frmHAConfig, Boolean, Dictionary

## Knowledge Gaps
- **1943 isolated node(s):** `MSSQLConfig`, `MYSQLConfig`, `MSSQLConfig`, `MYSQLConfig`, `Service` (+1938 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **763 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `System.Collections.Generic` connect `DeskInsight Desktop Streaming` to `Session Details & HSM Framework`, `Secure SSO Application Launcher`, `Server Framework Config Objects`, `ACM Application Control Automation`, `Application Event Logging`, `ACM Common — APICalling`, `ASM Server — Pkcs11Interop`, `ACM Common — Enitity Objects`, `ASM Server — Pkcs11Interop`, `Services — Log Archiver Service`, `Offline MultiTab — Offline API`, `ACMO Web — Client Manager`, `ACM Client — App Exe`, `Services — .Utilities.Sign Tool`, `ACMO Web — Client Manager`, `ACM Client — SSHTerminal`, `Services — Privilege User Discovery`, `ASM Server — Server Manager`, `Services — Provisioning Service`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Services — SLPF`, `Services — TSPlugin Service`, `Services — Provisioning Scheduler`, `Services — .Smtp Send Mail.Security`, `Services — Passworde Envelope Manager`, `Services — Password Change Vault`, `ACMO Web — Web Services`, `ACM Client — Web Browser`, `Services — .User Controls`, `Services — Schedule Password Change`, `ACM Client — SSHTerminal`, `ASM Server — Pkcs11Interop`, `Common — .User Controls`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Services — Privilege User Discovery`, `Services — Log Archiver Service`, `Services — ADScanner Service`, `Services — TSPlugin Service`, `Services — Arcon Auto Failover`, `ACM Client — Framework CM`, `ASM Server — Server Manager`, `Offline MultiTab — Offline API`, `ACM Common — Log Images`, `Services — Provisioning Service`, `ACM Common — .User Controls`, `Offline MultiTab — Offline API`, `ACM Common — .PIMUD`, `Services — Desk Insight`, `ACM Common — Enitity Objects`, `ACMO Web — APIRA`, `ACMO Web — Client Manager`, `ACMO Web — Common Functions`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ACM Client — Framework CM`, `ACM Client — DQS`, `ACMO Web — Client Manager`, `Common — .User Controls`, `ASM Server — Server Manager`, `Services — Desk Insight`, `ACMO Web — Client Manager`, `ASM Server — Server Manager`, `Services — TSPlugin Service`, `Common — SUtil`, `Common — Enitity Objects`, `Common — Enitity Objects`, `ACM Client — Sshkey SFTP`, `Services — ADScanner Service`, `Services — Data Sync`, `Services — Desk Insight`, `Services — Desk Insight`, `Services — Migrate Data Utility`, `Services — Passworde Envelope Manager`, `Services — Passworde Envelope Manager`, `Services — Server Manager`, `Services — Log Archiver Service`, `Services — Desk Insight`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `User Discovery — Logger`, `Services — Desk Insight`, `ACMO Web — Client Manager`, `Services — Schedule Password Change`, `ACM Common — Enitity Objects`, `Services — Desk Insight`, `ACM Common — Enitity Objects`, `ACMO Web — Client Manager`, `ACMO Web — Common Functions`, `Services — Desk Insight`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Services — Desk Insight`, `ASM Server — Server Manager`, `ACMO Web — Provisioning Web`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Services — Active Directory Insight`, `Services — ADScanner Service`, `Services — Desk Insight`, `Offline MultiTab — Windows Service`, `Services — Provisioning Service`, `Offline MultiTab — Offline API`, `Services — Desk Insight`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — APEMService`, `ACM Client — Framework CM`, `Services — TSPlugin Service`, `Services — Windows Vaulting Service`, `ACMO Web — Client Manager`, `ACM Common — Enitity Objects`, `ACM Common — Enitity Objects`, `ACMO Web — APIOnline`, `ACM Common — .User Controls`, `ACMO Web — Client Manager`, `ASM Server — Server Manager`, `ACMO Web — Provisioning Web`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Services — Desk Insight`, `Services — Z POC`, `ASM Server — .User Controls`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `PAMSSHWRAPPER — SSHKey Generation`, `Offline MultiTab — Offline API`, `Offline MultiTab — Offline API`, `Services — Cloud File Uploader`, `ACM Common — .User Controls`, `Services — Desk Insight`, `Services — Data Sync`, `Services — TSPlugin Service`, `Services — Desk Insight`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Onboarding — Common Enum`, `Datum Bridge Client`, `Services — TSPlugin Service`, `ACM Client — DQS`, `ACM Client — Framework CM`, `ACM Client — Framework CM`, `ACM Common — Logger Helper`, `ACM Client — Network Devices`, `SSM — Arcoss SSMDesktop`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `Services — PAM Agents`, `Services — DBSync Service`, `Services — Desk Insight`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `ACMO Web — Portal`, `Services — Log Manager Service`, `ASM Server — Server Manager`, `ACMO Web — Portal`, `ACMO Web — Offline API`, `ASM Server — Server Manager`, `Common — .API.Models`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Offline MultiTab — Offline API`, `Offline MultiTab — Offline API`, `Services — Desk Insight`, `Services — Passworde Envelope Manager`, `ASM Server — Enitity Objects`, `Common — Password Manager`, `Services — Provisioning Service`, `SSM — Arcoss SSMDesktop`, `Services — TSPlugin Service`, `ACM Client — Framework CM`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Datum Bridge`, `ACMO Web — User Access`, `Common — .User Controls`, `Common — Enitity Objects`, `ACM Client — SSHTerminal`, `Services — Staging Log Sync`, `ACM Client — SSHTerminal`, `ACMO Web — Client Manager`, `ACMO Web — Client Manager`, `ASM Server — Server Manager`, `Offline MultiTab — Windows Service`, `ACM Client — Framework CM`, `Services — PAM Agents`, `Services — Arcon File Upload`, `Services — Perf Mon IT`, `Services — Provisioning Service`, `ACM Common — Enitity Objects`, `Services — Alert Service`, `Services — PAM Agents`, `Services — TSPlugin Service`, `Services — Provisioning Service`, `LDAPAuthenticator`, `ACMO Web — User Access`, `ASM Server — Server Manager`, `Common — .User Controls`, `Services — PAM Agents`, `Services — TSPlugin Service`, `Offline MultiTab — Offline API`, `Offline MultiTab — Windows Service`, `ACMO Web — Common Functions`, `Services — Desk Insight`, `Services — Z POC`, `Services — User On Boarding`, `ACM Client — Framework CM`, `ASM Server — Server Manager`, `Services — Sync Failed Password`, `Services — Passworde Envelope Manager`, `ACMO Web — Client Manager`, `LDAPAuthenticator`, `ASM Server — Server Manager`, `Services — Log Manager Service`, `Services — Migrate Data Utility`, `LDAPAuthenticator`, `Offline MultiTab — Offline API`, `ACMO Web — Client Manager`, `Services — PAM Agents`, `Services — Cloud File Uploader`, `Services — DBSync Service`, `Services — DBSync Service`, `Services — Desk Insight`, `Services — Provisioning Service`, `Services — TSPlugin Service`, `ACM Client — RStream Client`, `Services — TSPlugin Service`, `ASM Server — Server Manager`, `Services — Desk Insight`, `Services — Staging Log Sync`, `ACM Common — .User Controls`, `ASM Server — PAM.Server Manager.Tests`, `Services — Cloud File Uploader`, `Services — Cloud File Uploader`, `ACM Common — APICalling`, `ACM Common — Enitity Objects`, `ACMO Web — Provisioning Web`, `ACMO Web — APIRA`, `Services — PAM Agents`, `Services — Cloud File Uploader`, `Services — Data Sync`, `ACMO Web — Client Manager`, `Services — Active Directory Insight`, `ACM Client — Sshkey SFTP`, `ACM Common — Enitity Objects`, `LDAPAuthenticator`, `Services — Staging Log Sync`, `ACM Client — SSHTerminal`, `LDAPAuthenticator — .Radius`, `ASM Server — Server Manager`, `Services — PAM Agents`, `Services — Z POC`, `ACM Client — App Exe`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Pkcs11Interop`, `Services — PAM Agents`, `Services — TSPlugin Service`, `ACMO Web — APIOnline`, `ACMO Web — Client Manager`, `Services — Desk Insight`, `Services — TSPlugin Service`, `Services — Z POC`, `ACMO Web — Portal`, `Common — Reference Details`, `Services — Desk Insight`, `Services — TSPlugin Service`, `ACM Client — Framework CM`, `ACM Client — Arcoss SSMDesktop`, `ACM Client — VNCTerminal`, `ACM Client — Web Browserv35`, `Services — Cloud File Uploader`, `Services — Migrate Data Utility`, `Services — Passworde Envelope Manager`, `Services — TSPlugin Service`, `Services — Framework CM`, `ACM Common — .User Controls`, `Common — .User Controls`, `Common — Enitity Objects`, `Services — Cloud File Uploader`, `Services — Desk Insight`, `Services — Provisioning Scheduler`, `ACMO Web — User Access`, `Services — Desk Insight`, `Services — TSPlugin Service`, `LDAPAuthenticator`, `ACM Client — Sshkey SFTP`, `ACM Common — .User Controls`, `ACMO Web — User Access`, `ASM Server — Server Manager`, `Common — .User Controls`, `Services — Cloud File Uploader`, `Services — Privilege User Discovery`, `ACM Client — PAMMulti Tab`, `ACM Client — Web Browserv35`, `ACM Common — Enitity Objects`, `ACMO Web — Client Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Common — .PIMUD`, `Common — .PIMUD`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Common — Enitity Objects`, `Services — Cloud File Uploader`, `Services — Desk Insight`, `Services — Folder Sync Service`, `Services — Log Manager Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `LDAPAuthenticator — Unit Testing`, `SSM — Arcoss SSMDesktop`?**
  _High betweenness centrality (0.259) - this node is a cross-community bridge._
- **Why does `System.Threading` connect `DeskInsight Desktop Streaming` to `ACM Client — Framework CM`, `Session Details & HSM Framework`, `Services — Desk Insight`, `Secure SSO Application Launcher`, `Services — Windows Vaulting Service`, `Scheduled Password Change Service`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `ASM Server — Server Manager`, `ACM Client — SSHTerminal`, `ASM Server — Server Manager`, `JSch Cipher & Key Exchange`, `ACM Client — SSHTerminal`, `ACM Client — Framework CM`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `SSH Terminal Granados UI`, `ACM Client — VNCTerminal`, `ACM Client — VNCTerminal`, `ACM Client — SSHTerminal`, `Services — SLPF`, `ASM Server — PAM.Server Manager.Tests`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Offline MultiTab — Offline API`, `Services — SLPF`, `Common — .PIMUD`, `Common — .PIMUD`, `Common — SLPF`, `Services — Provisioning Service`, `LDAPAuthenticator`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `ACM Client — Framework CM`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — SLPF`, `ACM Client — SSHTerminal`, `ASM Server — Server Manager`, `Services — Folder Sync Service`, `Services — ADScanner Service`, `Services — Z POC`, `ACM Client — VNCTerminal`, `Services — TSPlugin Service`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Services — Windows Vaulting Service`, `Services — TSPlugin Service`, `ASM Server — Server Manager`, `Common — SLPF`, `Services — Provisioning Scheduler`, `Services — .Smtp Send Mail.Security`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Offline MultiTab — Windows Service`, `Services — Provisioning Service`, `Services — Desk Insight`, `Services — Password Change Vault`, `ASM Server — SLPF`, `Services — Server Manager`, `ACM Common — .PIMUD`, `Services — SLPF`, `Services — TSPlugin Service`, `Services — Schedule Password Change`, `ACM Client — Web Browserv35`, `Services — TSPlugin Service`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `ARCONS.LPF.sch` connect `Scheduled Password Change Service` to `Session Details & HSM Framework`, `DeskInsight Desktop Streaming`, `Secure SSO Application Launcher`, `JSch SSH Keep-Alive & Buffers`, `Java-to-.NET File IO Shim`, `JStream Java Stream Shim`, `JSch Cipher & Key Exchange`, `JSch Cipher & HASH Primitives`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Common — SLPF`, `Services — SLPF`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Common — SLPF`, `ASM Server — Server Manager`, `Services — TSPlugin Service`, `Common — SLPF`, `Services — TSPlugin Service`, `Services — SLPF`, `ACM Common — SLPF`, `Common — SLPF`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Services — SLPF`, `Services — Schedule Password Change`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Common — SLPF`, `Services — Schedule Password Change`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `ASM Server — Server Manager`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — TSPlugin Service`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Common — SLPF`, `ASM Server — Server Manager`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Services — SLPF`, `ASM Server — Server Manager`, `Common — SLPF`, `Services — TSPlugin Service`, `Services — Schedule Password Change`, `Services — Schedule Password Change`, `Services — TSPlugin Service`, `Services — Schedule Password Change`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **What connects `MSSQLConfig`, `MYSQLConfig`, `MSSQLConfig` to the rest of the system?**
  _1943 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ARCOS Server Manager WinForms UI` be split into smaller, more focused modules?**
  _Cohesion score 0.004577445401955145 - nodes in this community are weakly interconnected._
- **Should `ARCON Common Data Access Layer` be split into smaller, more focused modules?**
  _Cohesion score 0.007742666878390683 - nodes in this community are weakly interconnected._
- **Should `Session Details & HSM Framework` be split into smaller, more focused modules?**
  _Cohesion score 0.004316080727532025 - nodes in this community are weakly interconnected._