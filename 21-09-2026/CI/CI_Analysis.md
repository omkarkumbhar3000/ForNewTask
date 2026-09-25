# CI (Converged Identity) Ticket Analysis — 2026-01-01 to 2026-09-21

**Generated:** 2026-09-22 19:09
**Source snapshot:** `ci-analysis-2026-01-01-to-2026-09-21.json` · sha256 `5e12f6be2f084c73`
**Project:** CI (CI) · **Date range:** 2026-01-01 to 2026-09-21
**Total tickets:** 5994 · **Client tickets:** 1456 · **Internal:** 4538

> **Open / Closed classification.** Every status is mapped by the owner's status lists, case-insensitively. A status in neither list is reported as **Unmapped** and is never guessed into a bucket, so each bifurcated table carries its own Unmapped column and **Total Count = Open Total + Closed Total + Unmapped**. 262 of 5994 tickets (4.4%) are unmapped.

> **Client / Internal.** CI's internal marker is `Internal Arcon`. 825 tickets (13.8%) carry no Primary Client and are counted as **Internal**, per the owner's decision; they are listed in their own section so the fallback is never silent.

---

## 1. Summary

| Metric | Count |
| --- | ---: |
| Total tickets | 5994 |
| Client tickets | 1456 (24.3%) |
| Internal tickets | 4538 (75.7%) |
| — of which no Primary Client | 825 (13.8%) |
| Sub-tasks | 1443 (24.1%) |
| Standalone (non-sub-task) | 4551 (75.9%) |
| Open | 1625 (27.1%) |
| Closed | 4107 (68.5%) |
| Unmapped status | 262 (4.4%) |

_No Total row: these rows count overlapping populations of the same ticket set, so summing them would double-count._

## 2. Status Distribution

| Status | Class | Count | % of Total |
| --- | --- | ---: | ---: |
| Closed | Closed | 3724 | 62.1% |
| Open | Open | 878 | 14.6% |
| Development Analysis | Open | 218 | 3.6% |
| Development Review | Unmapped | 170 | 2.8% |
| Ready For Released | Closed | 152 | 2.5% |
| Awaiting Response | Open | 148 | 2.5% |
| Rejected | Closed | 120 | 2.0% |
| Business Analysis | Open | 97 | 1.6% |
| Document Review | Closed | 94 | 1.6% |
| Duplicate | Unmapped | 82 | 1.4% |
| Reopen | Open | 49 | 0.8% |
| Audit | Open | 42 | 0.7% |
| Security Check | Open | 38 | 0.6% |
| Development | Open | 36 | 0.6% |
| QA Testing | Open | 29 | 0.5% |
| Dev Review and Testing | Open | 18 | 0.3% |
| Documentation | Closed | 17 | 0.3% |
| Patch Shared | Open | 14 | 0.2% |
| Solution Analysis | Open | 12 | 0.2% |
| Awaiting Session | Open | 11 | 0.2% |
| Under Observation (No Code Change) | Open | 11 | 0.2% |
| Patch Developed | Open | 10 | 0.2% |
| In Progress | Open | 5 | 0.1% |
| Product Hold | Open | 5 | 0.1% |
| Pending from DevOps | Open | 4 | 0.1% |
| Pre Dev Audit | Unmapped | 4 | 0.1% |
| Patch Tech Lead Review | Unmapped | 3 | 0.1% |
| Patch Passed | Unmapped | 2 | 0.0% |
| RCA/Resolution Review | Unmapped | 1 | 0.0% |
| **Total** |  | **5994** | **100.0%** |

## 3. Issue Type Distribution

| Issue Type | Count | % of Total |
| --- | ---: | ---: |
| Bug | 3131 | 52.2% |
| Sub-task | 1443 | 24.1% |
| Task | 735 | 12.3% |
| Story | 575 | 9.6% |
| Security Fix | 20 | 0.3% |
| Client-Support | 20 | 0.3% |
| APEM Tool | 18 | 0.3% |
| POC | 17 | 0.3% |
| Document | 16 | 0.3% |
| Performance | 13 | 0.2% |
| Test Case | 3 | 0.1% |
| Epic | 3 | 0.1% |
| **Total** | **5994** | **100.0%** |

## 4. Priority Distribution

| Priority | Total Count | Open |  |  | Closed |  |  | Unmapped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|  |  | Client | Internal | Total | Client | Internal | Total |  |
| Low | 1907 | 39 | 397 | 436 | 46 | 1259 | 1305 | 166 |
| High | 1833 | 235 | 319 | 554 | 553 | 678 | 1231 | 48 |
| Medium | 1478 | 39 | 335 | 374 | 72 | 998 | 1070 | 34 |
| ShowStopper | 674 | 112 | 88 | 200 | 290 | 170 | 460 | 14 |
| Unknown | 102 | 0 | 61 | 61 | 0 | 41 | 41 | 0 |
| **Total** | **5994** | **425** | **1200** | **1625** | **961** | **3146** | **4107** | **262** |

## 5. Severity Distribution

| Severity | Total Count | Open |  |  | Closed |  |  | Unmapped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|  |  | Client | Internal | Total | Client | Internal | Total |  |
| Not set | 5649 | 395 | 1114 | 1509 | 889 | 2999 | 3888 | 252 |
| Sev-0 | 145 | 11 | 30 | 41 | 35 | 65 | 100 | 4 |
| Sev-1 | 125 | 13 | 34 | 47 | 26 | 47 | 73 | 5 |
| Sev-2 | 65 | 6 | 21 | 27 | 8 | 29 | 37 | 1 |
| Sev-3 | 10 | 0 | 1 | 1 | 3 | 6 | 9 | 0 |
| **Total** | **5994** | **425** | **1200** | **1625** | **961** | **3146** | **4107** | **262** |

⚠️ **Severity is populated on 345 of 5994 tickets (5.8%).** Every figure above other than the `Not set` row is quoted over that subset; an unfilled Severity is not evidence of low severity.

## 6. Components

⚠️ **Components are multi-valued.** 313 tickets carry two or more components and are counted once per component, so the rows sum to 6356 component assignments across 5994 distinct tickets. The **Total** row states distinct tickets, which reconciles to the project count; it is deliberately not the column sum.

### 6A. Component — Total, Open and Closed

| Component | Total Count | Open | Closed | Unmapped |
| --- | ---: | ---: | ---: | ---: |
| (No component) | 1142 | 207 | 911 | 24 |
| Admin Console | 1080 | 220 | 833 | 27 |
| Connector | 593 | 227 | 230 | 136 |
| Workspace | 324 | 84 | 234 | 6 |
| Reports | 311 | 100 | 197 | 14 |
| Identity Hub | 297 | 55 | 232 | 10 |
| All modules | 276 | 141 | 129 | 6 |
| Settings | 255 | 61 | 187 | 7 |
| Password Vault | 236 | 59 | 173 | 4 |
| Auto onboarding | 235 | 58 | 171 | 6 |
| Digital Vault | 146 | 29 | 113 | 4 |
| Workflow | 139 | 40 | 96 | 3 |
| Session Monitoring | 121 | 30 | 88 | 3 |
| Access Control | 111 | 31 | 76 | 4 |
| Build and Deploy | 102 | 56 | 46 | 0 |
| Identity Governance | 80 | 16 | 62 | 2 |
| AGW | 77 | 40 | 37 | 0 |
| Onboarding Engine | 75 | 6 | 63 | 6 |
| Knight Analytics | 74 | 32 | 41 | 1 |
| APEM | 59 | 25 | 33 | 1 |
| Integration | 59 | 43 | 16 | 0 |
| Alerts and Notification | 58 | 10 | 44 | 4 |
| ACMO | 57 | 23 | 34 | 0 |
| Web-gateway/proxy | 54 | 25 | 28 | 1 |
| Application & Audit Logs | 49 | 18 | 27 | 4 |
| CI-MAC Thick Client | 46 | 12 | 33 | 1 |
| JML Engine | 46 | 19 | 23 | 4 |
| PyCLI | 32 | 15 | 17 | 0 |
| Linux Thick Client | 29 | 3 | 26 | 0 |
| CI Kubernetes Infrastructure | 28 | 0 | 26 | 2 |
| SIEM | 26 | 8 | 18 | 0 |
| Discovery | 23 | 10 | 13 | 0 |
|  CI OVA | 23 | 2 | 19 | 2 |
| Report/Dashboard | 21 | 6 | 15 | 0 |
| PAMAPI | 19 | 7 | 9 | 3 |
| PAM | 12 | 9 | 2 | 1 |
| Browser Plugin | 11 | 6 | 5 | 0 |
| RND | 10 | 8 | 2 | 0 |
| RTSM | 8 | 2 | 6 | 0 |
| MFA | 6 | 4 | 2 | 0 |
| NHI CI Integration | 4 | 1 | 3 | 0 |
| CI-Tag Management | 2 | 1 | 1 | 0 |
| **Total (distinct tickets)** | **5994** | **1625** | **4107** | **262** |

### 6B. Component — Client and Internal split

| Component | Total Count | Open |  |  | Closed |  |  | Unmapped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|  |  | Client | Internal | Total | Client | Internal | Total |  |
| (No component) | 1142 | 1 | 206 | 207 | 3 | 908 | 911 | 24 |
| Admin Console | 1080 | 75 | 145 | 220 | 225 | 608 | 833 | 27 |
| Connector | 593 | 93 | 134 | 227 | 138 | 92 | 230 | 136 |
| Workspace | 324 | 27 | 57 | 84 | 94 | 140 | 234 | 6 |
| Reports | 311 | 14 | 86 | 100 | 48 | 149 | 197 | 14 |
| Identity Hub | 297 | 20 | 35 | 55 | 49 | 183 | 232 | 10 |
| All modules | 276 | 45 | 96 | 141 | 47 | 82 | 129 | 6 |
| Settings | 255 | 5 | 56 | 61 | 25 | 162 | 187 | 7 |
| Password Vault | 236 | 13 | 46 | 59 | 76 | 97 | 173 | 4 |
| Auto onboarding | 235 | 12 | 46 | 58 | 49 | 122 | 171 | 6 |
| Digital Vault | 146 | 20 | 9 | 29 | 25 | 88 | 113 | 4 |
| Workflow | 139 | 13 | 27 | 40 | 19 | 77 | 96 | 3 |
| Session Monitoring | 121 | 9 | 21 | 30 | 20 | 68 | 88 | 3 |
| Access Control | 111 | 5 | 26 | 31 | 10 | 66 | 76 | 4 |
| Build and Deploy | 102 | 1 | 55 | 56 | 6 | 40 | 46 | 0 |
| Identity Governance | 80 | 5 | 11 | 16 | 10 | 52 | 62 | 2 |
| AGW | 77 | 17 | 23 | 40 | 19 | 18 | 37 | 0 |
| Onboarding Engine | 75 | 1 | 5 | 6 | 7 | 56 | 63 | 6 |
| Knight Analytics | 74 | 1 | 31 | 32 | 0 | 41 | 41 | 1 |
| APEM | 59 | 20 | 5 | 25 | 24 | 9 | 33 | 1 |
| Integration | 59 | 9 | 34 | 43 | 11 | 5 | 16 | 0 |
| Alerts and Notification | 58 | 8 | 2 | 10 | 26 | 18 | 44 | 4 |
| ACMO | 57 | 4 | 19 | 23 | 14 | 20 | 34 | 0 |
| Web-gateway/proxy | 54 | 12 | 13 | 25 | 16 | 12 | 28 | 1 |
| Application & Audit Logs | 49 | 4 | 14 | 18 | 4 | 23 | 27 | 4 |
| CI-MAC Thick Client | 46 | 4 | 8 | 12 | 9 | 24 | 33 | 1 |
| JML Engine | 46 | 8 | 11 | 19 | 13 | 10 | 23 | 4 |
| PyCLI | 32 | 0 | 15 | 15 | 0 | 17 | 17 | 0 |
| Linux Thick Client | 29 | 2 | 1 | 3 | 14 | 12 | 26 | 0 |
| CI Kubernetes Infrastructure | 28 | 0 | 0 | 0 | 0 | 26 | 26 | 2 |
| SIEM | 26 | 7 | 1 | 8 | 13 | 5 | 18 | 0 |
| Discovery | 23 | 0 | 10 | 10 | 0 | 13 | 13 | 0 |
|  CI OVA | 23 | 0 | 2 | 2 | 0 | 19 | 19 | 2 |
| Report/Dashboard | 21 | 1 | 5 | 6 | 3 | 12 | 15 | 0 |
| PAMAPI | 19 | 3 | 4 | 7 | 1 | 8 | 9 | 3 |
| PAM | 12 | 3 | 6 | 9 | 2 | 0 | 2 | 1 |
| Browser Plugin | 11 | 2 | 4 | 6 | 2 | 3 | 5 | 0 |
| RND | 10 | 0 | 8 | 8 | 1 | 1 | 2 | 0 |
| RTSM | 8 | 1 | 1 | 2 | 1 | 5 | 6 | 0 |
| MFA | 6 | 2 | 2 | 4 | 2 | 0 | 2 | 0 |
| NHI CI Integration | 4 | 0 | 1 | 1 | 0 | 3 | 3 | 0 |
| CI-Tag Management | 2 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| **Total (distinct tickets)** | **5994** | **425** | **1200** | **1625** | **961** | **3146** | **4107** | **262** |

## 7. Top Reporters (Top 20)

| Reporter | Count | % of Total |
| --- | ---: | ---: |
| Pratik Dadasaheb Magdum | 285 | 4.8% |
| Mudabbir Hussain Bhat | 238 | 4.0% |
| shailesh sawant | 226 | 3.8% |
| Poonam Kulkarni | 214 | 3.6% |
| Vajreshwari Chalindrawar | 171 | 2.9% |
| Nazia Shaikh | 157 | 2.6% |
| Nadeem Naik | 143 | 2.4% |
| Avdhut Tad | 135 | 2.3% |
| Raj Shah | 121 | 2.0% |
| Chaitanya Pathak | 116 | 1.9% |
| Anand  V | 104 | 1.7% |
| Harshad Prajapati | 103 | 1.7% |
| Keyur Solanki | 94 | 1.6% |
| Moiz Jawadwala | 80 | 1.3% |
| Heena Chaurasia | 80 | 1.3% |
| Sunil Ramesh Savale | 76 | 1.3% |
| Jeetendra Choudhary | 67 | 1.1% |
| Nishant Kumar Ghosh | 65 | 1.1% |
| Manish Shingre | 65 | 1.1% |
| pranay | 64 | 1.1% |
| **Total (top 20 shown)** | **2604** | **43.4%** |

_191 further values not shown, accounting for 3390 of 5994 tickets._

## 8. Top Assignees (Top 20)

| Assignee | Count | % of Total |
| --- | ---: | ---: |
| Uttam Nayak | 822 | 13.7% |
| Vijayashree Shetty | 752 | 12.5% |
| Kalpesh Pusalkar | 531 | 8.9% |
| Akhil | 405 | 6.8% |
| Janam Bhavsar | 332 | 5.5% |
| Shrikant Shedekar | 161 | 2.7% |
| Param Sannakke | 140 | 2.3% |
| Arpita Upadhyay | 128 | 2.1% |
| Pinak Bhaskar Dere | 119 | 2.0% |
| Ronit Bose | 115 | 1.9% |
| Anand  V | 103 | 1.7% |
| Parakh Shah | 88 | 1.5% |
| Heena Chaurasia | 87 | 1.5% |
| Jay Kawa | 74 | 1.2% |
| Moiz Jawadwala | 73 | 1.2% |
| Satyendra Pratap | 64 | 1.1% |
| Prashanth Reddy | 61 | 1.0% |
| balaji modalavalasa | 45 | 0.8% |
| Priyanshu Pandey | 42 | 0.7% |
| Jeetendra Choudhary | 41 | 0.7% |
| **Total (top 20 shown)** | **4183** | **69.8%** |

_209 further values not shown, accounting for 1811 of 5994 tickets._

## 9. Monthly Creation Trend

| Month | Count |
| --- | ---: |
| 2026-01 | 745 |
| 2026-02 | 736 |
| 2026-03 | 793 |
| 2026-04 | 634 |
| 2026-05 | 482 |
| 2026-06 | 506 |
| 2026-07 | 846 |
| 2026-08 | 734 |
| 2026-09 | 518 |
| **Total** | **5994** |

## 10. Weekly Creation Trend

| Week | Count |
| --- | ---: |
| 2026-W01 | 31 |
| 2026-W02 | 224 |
| 2026-W03 | 135 |
| 2026-W04 | 204 |
| 2026-W05 | 156 |
| 2026-W06 | 185 |
| 2026-W07 | 173 |
| 2026-W08 | 190 |
| 2026-W09 | 183 |
| 2026-W10 | 256 |
| 2026-W11 | 142 |
| 2026-W12 | 143 |
| 2026-W13 | 167 |
| 2026-W14 | 170 |
| 2026-W15 | 110 |
| 2026-W16 | 115 |
| 2026-W17 | 187 |
| 2026-W18 | 140 |
| 2026-W19 | 149 |
| 2026-W20 | 120 |
| 2026-W21 | 114 |
| 2026-W22 | 96 |
| 2026-W23 | 136 |
| 2026-W24 | 87 |
| 2026-W25 | 131 |
| 2026-W26 | 105 |
| 2026-W27 | 129 |
| 2026-W28 | 143 |
| 2026-W29 | 197 |
| 2026-W30 | 181 |
| 2026-W31 | 252 |
| 2026-W32 | 148 |
| 2026-W33 | 131 |
| 2026-W34 | 214 |
| 2026-W35 | 176 |
| 2026-W36 | 237 |
| 2026-W37 | 168 |
| 2026-W38 | 131 |
| 2026-W39 | 38 |
| **Total** | **5994** |

## 11. Fix Version Distribution

| Fix Version | Count |
| --- | ---: |
| V10.12.000 | 579 |
| V10.12.001 | 545 |
| V10.12.003 | 283 |
| V10.11.005 | 283 |
| V10.11.003 | 274 |
| V10.11.004 | 223 |
| Sprint-Backlog | 155 |
| V10.11.002 | 96 |
| V10.11.001 | 77 |
| V10.11.000 | 73 |
| V10.11.003_HF3 | 67 |
| V10.11.005_HF2 | 67 |
| V10.11.004_HF | 43 |
| V10.10.007 | 38 |
| V10.10.007_HF5 | 31 |
| V10.12.000_HF | 31 |
| V10.10.007_HF3 | 30 |
| V10.11.005_HF3 | 25 |
| Future Release Tickets | 24 |
| V10.11.005_HF1 | 17 |
| V10.11.003_HF2 | 15 |
| V10.10.007_HF2 | 13 |
| V10.12.004 | 12 |
| V10.12.002 | 11 |
| v10.10.007_HF4 | 10 |
| Mac Version 12.8.0.1 | 9 |
| Mac Version 12.9.0.0 | 6 |
| V10.10.004 | 6 |
| V10.11.003_HF | 6 |
| Backlog | 5 |
| **Total (top 30 shown)** | **3054** |

_27 further values not shown, accounting for 56 of 3110 fix-version assignments._

## 12. Root Cause Analysis (RCA)

| RCA | Count | % of Total |
| --- | ---: | ---: |
| Not set | 1695 | 28.3% |
| Requests - Enhancement | 1219 | 20.3% |
| Code - Logic Issue | 897 | 15.0% |
| Others - Working as expected | 338 | 5.6% |
| Others - Resolved Issue | 260 | 4.3% |
| Analysis - Inadequate Technical Design | 216 | 3.6% |
| Environment - Misconfiguration | 194 | 3.2% |
| Code - UI/UX Issue | 140 | 2.3% |
| Insufficient Unit Test case | 108 | 1.8% |
| Code - Incorrect Standards | 101 | 1.7% |
| Documentation - Administrator / User Guide | 97 | 1.6% |
| Not a bug | 93 | 1.6% |
| Code - Code Merge | 75 | 1.3% |
| Environment - Non replicated | 67 | 1.1% |
| Code - Packaging Issue | 57 | 1.0% |
| Analysis - Incomplete Requirement | 50 | 0.8% |
| Code - Performance Issue | 46 | 0.8% |
| Requests - Information Request | 45 | 0.8% |
| Analysis - Inadequate Test Coverage | 44 | 0.7% |
| Code - Security Issue | 35 | 0.6% |
| Environment- Env unavailable | 34 | 0.6% |
| Environment - Network | 30 | 0.5% |
| Missing Code / DB Scripts | 25 | 0.4% |
| Requests - APEM Tool | 25 | 0.4% |
| Deployment Issue | 21 | 0.4% |
| Documentation - Deployment Guide Inadequate | 19 | 0.3% |
| Environment - Resource Unavailability | 15 | 0.3% |
| Requests - Script Request | 15 | 0.3% |
| Code - Ansible / OCI Issue | 10 | 0.2% |
| Environment - 3rd Party compatibility | 7 | 0.1% |
| Environment - Hardware failure | 5 | 0.1% |
| Code not checked-in | 4 | 0.1% |
| Miscommunication | 4 | 0.1% |
| Insufficient Data | 2 | 0.0% |
| Data Issue | 1 | 0.0% |
| **Total** | **5994** | **100.0%** |

## 13. Hosting Environment

| Hosting Environment | Count | % of Total |
| --- | ---: | ---: |
| Not set | 4454 | 74.3% |
| Windows | 1134 | 18.9% |
| RHEL | 287 | 4.8% |
| Kubernetes | 90 | 1.5% |
| Ubuntu | 29 | 0.5% |
| **Total** | **5994** | **100.0%** |

## 14. Labels

| Label | Count |
| --- | ---: |
| CI | 299 |
| HI | 234 |
| Connector | 183 |
| RCA_SHEET | 145 |
| NHI | 134 |
| ENGG_TEAM | 124 |
| connector | 98 |
| Yuktee | 71 |
| UI | 70 |
| POC | 70 |
| Engg_AGW | 55 |
| Admin-console | 55 |
| tushar | 54 |
| kalpesh | 53 |
| workspace | 47 |
| EnggSprint1 | 43 |
| Sprint-05Jan26 | 41 |
| API | 36 |
| kevin | 32 |
| ENGG_July_26 | 31 |
| **Total (top 20 shown)** | **1875** |

_62 further values not shown, accounting for 397 of 2272 label assignments._

## 15. Sub-task Analysis

| Ticket Kind | Count |
| --- | ---: |
| Sub-tasks | 1443 |
| Standalone (non-sub-task) | 4551 |
| **Total** | **5994** |

The 1443 sub-tasks hang off **389 unique parent tickets**. That is a count of parents, not of tickets in this window, so it is kept out of the table above rather than added into a column it does not belong to.

### 15A. Top parent tickets by sub-task count

| Parent Key | Sub-tasks |
| --- | ---: |
| CI-16180 | 72 |
| CI-16147 | 68 |
| CI-22787 | 47 |
| CI-23135 | 39 |
| CI-20880 | 23 |
| CI-20701 | 18 |
| CI-22504 | 17 |
| CI-22991 | 17 |
| CI-20336 | 16 |
| CI-22078 | 16 |
| CI-21376 | 15 |
| CI-23089 | 15 |
| CI-23957 | 15 |
| CI-13552 | 13 |
| CI-20888 | 13 |
| **Total (top 15 shown)** | **404** |

_374 further parent tickets not shown, accounting for 1039 sub-tasks._

## 16. Unassigned Tickets

| Metric | Count |
| --- | ---: |
| Total unassigned | 19 |
| Client unassigned | 3 |
| Internal unassigned | 16 |

### Unassigned ticket details

| Key | Summary | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| [CI-19592](https://arcon-tech-solution.atlassian.net/browse/CI-19592) | Workspace - Message for Pinning and unpinning an asset needs to be corrected | Bug | Medium | Closed |
| [CI-19753](https://arcon-tech-solution.atlassian.net/browse/CI-19753) | SIB | Able to view all services in identity HUB for requesting | Bug | ShowStopper | Closed |
| [CI-20657](https://arcon-tech-solution.atlassian.net/browse/CI-20657) | OVA: Unable to do partial and full recon. | Bug | High | Closed |
| [CI-20773](https://arcon-tech-solution.atlassian.net/browse/CI-20773) |  Alerts and Configuration | Emails  are not being reveived for Report Scheduler | Bug | High | Rejected |
| [CI-20970](https://arcon-tech-solution.atlassian.net/browse/CI-20970) | OVA-Clicking on "Create and Apply Restrictions" Button during Profile Creation r | Bug | ShowStopper | Closed |
| [CI-21032](https://arcon-tech-solution.atlassian.net/browse/CI-21032) | 500 | Positive API Testing | Logs | Bug | Medium | Closed |
| [CI-21159](https://arcon-tech-solution.atlassian.net/browse/CI-21159) | 200 | Negative API Testing | Unauthorized Access | SCIM | Bug | Medium | Closed |
| [CI-21196](https://arcon-tech-solution.atlassian.net/browse/CI-21196) | PNB | Granular access control in certificate management | Story | High | Business Analysis |
| [CI-21697](https://arcon-tech-solution.atlassian.net/browse/CI-21697) | Kubernetes : 500 Error While Exporting Asset Group in Admin Console | Bug | High | Closed |
| [CI-21701](https://arcon-tech-solution.atlassian.net/browse/CI-21701) | Kubernetes : Unable to Change User Status to Sabbatical and Suspended | Bug | Medium | Closed |
| [CI-21729](https://arcon-tech-solution.atlassian.net/browse/CI-21729) | Routing WGW Connection via FRP (Aligned with AGWA Windows Setup) | Bug | High | Open |
| [CI-21766](https://arcon-tech-solution.atlassian.net/browse/CI-21766) | Kubernetes - LOB Filter Values Not Displayed in User Modification Based on SOT c | Bug | Medium | Closed |
| [CI-22696](https://arcon-tech-solution.atlassian.net/browse/CI-22696) | Running the WebDT and Connector API project | Sub-task | Low | Development Review |
| [CI-23298](https://arcon-tech-solution.atlassian.net/browse/CI-23298) | MFA command based restriction SSH Linux | Story | Low | Open |
| [CI-24621](https://arcon-tech-solution.atlassian.net/browse/CI-24621) | Unable to update My Profile in Identity Hub – 400 Bad Request error displayed on | Bug | High | Closed |
| [CI-24940](https://arcon-tech-solution.atlassian.net/browse/CI-24940) | FT - APIs for Basic PAM SCD | Story | Medium | Business Analysis |
| [CI-24944](https://arcon-tech-solution.atlassian.net/browse/CI-24944) | CLONE - New Connector Framework | Story | High | Open |
| [CI-25238](https://arcon-tech-solution.atlassian.net/browse/CI-25238) | Quds Bank || issues encountered while upgrading from version 10.11.003HF2 to 10. | Bug | High | Open |
| [CI-25424](https://arcon-tech-solution.atlassian.net/browse/CI-25424) | Adele | Unable to bulk import Digital Assets | Bug | High | Closed |

**Total listed:** 19 unassigned tickets.

## 17. Open High-Priority Tickets (High / ShowStopper / Critical)

| Key | Summary | Status | Priority | Assignee |
| --- | --- | --- | --- | --- |
| [CI-19093](https://arcon-tech-solution.atlassian.net/browse/CI-19093) | POC |HTI - frank's azure issue | Development Analysis | High | Param Sannakke |
| [CI-19115](https://arcon-tech-solution.atlassian.net/browse/CI-19115) | Unity Bank V10 || IDHUB – “Perform Action API Not Working” error during Approval | Open | High | Parakh Shah |
| [CI-19122](https://arcon-tech-solution.atlassian.net/browse/CI-19122) | Support for AGWA Setup and Configuration (Windows & Linux Components) | Internal | Awaiting Session | High | Jinit Hitesh Mehta |
| [CI-19124](https://arcon-tech-solution.atlassian.net/browse/CI-19124) | Need support in deploying Web Gateway for | Internal CI_Test_OVA | Open | High | Yashwanth Kumar H T |
| [CI-19198](https://arcon-tech-solution.atlassian.net/browse/CI-19198) | Assistance Required for Password Rotation Issue in Marico POC | Awaiting Response | High | Shabaz  Khan |
| [CI-19223](https://arcon-tech-solution.atlassian.net/browse/CI-19223) | NBF || Unable to record the session error while in middle of session | Development Analysis | High | Soumya Jyoti Das |
| [CI-19225](https://arcon-tech-solution.atlassian.net/browse/CI-19225) | Connector Request | Automate user SSO workflows between Easebuzz and Arcon CI | Business Analysis | High | Chinmay Maitre |
| [CI-19232](https://arcon-tech-solution.atlassian.net/browse/CI-19232) | CLONE - FT- Kubernetes cluster with rbac | Open | High | Vijayashree Shetty |
| [CI-19265](https://arcon-tech-solution.atlassian.net/browse/CI-19265) | Connector Request | Automate user SSO workflows between mtalkz and Arcon CI | Business Analysis | High | Chinmay Maitre |
| [CI-19292](https://arcon-tech-solution.atlassian.net/browse/CI-19292) | PNB | Client Requirements for Reports, Dashboard, and Encryption | Open | High | Akhil |
| [CI-19306](https://arcon-tech-solution.atlassian.net/browse/CI-19306) | Unity Bank V10 || Enable editable selected attributes while raising a new asset  | Open | High | Parakh Shah |
| [CI-19316](https://arcon-tech-solution.atlassian.net/browse/CI-19316) | CLONE - Xceedance | CI-PAM | Issue with Report scheduler | Patch Shared | High | Pratik Sawant |
| [CI-19346](https://arcon-tech-solution.atlassian.net/browse/CI-19346) | Issue with auto onboarding of users from Entra ID and need support configure com | Open | High | Yashwanth Kumar H T |
| [CI-19352](https://arcon-tech-solution.atlassian.net/browse/CI-19352) | Hero FinCorp SGW Issue: Connected host has failed to respond via SGW | Audit | ShowStopper | Moiz Jawadwala |
| [CI-19385](https://arcon-tech-solution.atlassian.net/browse/CI-19385) | Reg: Issue with SFTP File transfer for Key based Server_ CI 10.10.007_v3 | Awaiting Session | High | srikanth.rendla |
| [CI-19390](https://arcon-tech-solution.atlassian.net/browse/CI-19390) | User Attribute Field is not Populating in Asset. | Dev Review and Testing | High | Vijayashree Shetty |
| [CI-19399](https://arcon-tech-solution.atlassian.net/browse/CI-19399) | AGWA Installation - Hero FinCorp POC | Open | ShowStopper | Abhishek Manikandan |
| [CI-19411](https://arcon-tech-solution.atlassian.net/browse/CI-19411) | Performance Issue - CI Reports | Open | High | Arpita Upadhyay |
| [CI-19413](https://arcon-tech-solution.atlassian.net/browse/CI-19413) | Performance Issues - Access, Onboarding & Reports | Open | High | Arpita Upadhyay |
| [CI-19420](https://arcon-tech-solution.atlassian.net/browse/CI-19420) | JIO||NIC||Need to close the VAPT points. | Open | High | Manish Gupta |
| [CI-19430](https://arcon-tech-solution.atlassian.net/browse/CI-19430) | Admin Console | Incorrect Condition for Manual Reconciliation must be handled co | Development Analysis | High | Akhil |
| [CI-19454](https://arcon-tech-solution.atlassian.net/browse/CI-19454) | 00169496 || JFSL ||Ext ID creation issue | Development Analysis | High | Milan Garg |
| [CI-19459](https://arcon-tech-solution.atlassian.net/browse/CI-19459) | Pycli | Helping COE team to understand and host PyCLI for OCI and OVA | Audit | High | Shubham Murudkar |
| [CI-19543](https://arcon-tech-solution.atlassian.net/browse/CI-19543) | Develop a Test Connection API for ARCON CI Integration with third party IGA | Open | High | Satyendra Pratap |
| [CI-19547](https://arcon-tech-solution.atlassian.net/browse/CI-19547) | CCIL || Need restricted Thick Client | Business Analysis | ShowStopper | Prashanth Reddy |
| [CI-19550](https://arcon-tech-solution.atlassian.net/browse/CI-19550) | PNB | Mac Id issue for Credential Access Logs | Development Analysis | ShowStopper | Shrikant Shedekar |
| [CI-19584](https://arcon-tech-solution.atlassian.net/browse/CI-19584) | Reconciliation Failed – Missing SAMAccountName / Contact Not Fetched | Awaiting Response | High | Wahid Shaikh |
| [CI-19599](https://arcon-tech-solution.atlassian.net/browse/CI-19599) | Airtel B2B | Video Logs Background Notification Capture | Development Analysis | ShowStopper | Soumya Jyoti Das |
| [CI-19614](https://arcon-tech-solution.atlassian.net/browse/CI-19614) | SIB | store logs in Temp location when main drive is offline | Business Analysis | ShowStopper | Prashanth Reddy |
| [CI-19620](https://arcon-tech-solution.atlassian.net/browse/CI-19620) | JFL || CI 10.0.007 || Memory spike issue. | Open | ShowStopper | Milan Garg |

**Total listed:** 30 of 754 open high-priority tickets (724 not shown).

## 18. Unmapped Status Review

These 262 tickets (4.4%) carry a status present in neither the Open nor the Closed list. They are counted in every **Total Count** and in the **Unmapped** column, and in neither Open nor Closed. Listed here for a mapping decision.

| Status | Client | Internal | Total |
| --- | ---: | ---: | ---: |
| Development Review | 53 | 117 | 170 |
| Duplicate | 13 | 69 | 82 |
| Pre Dev Audit | 1 | 3 | 4 |
| Patch Tech Lead Review | 2 | 1 | 3 |
| Patch Passed | 1 | 1 | 2 |
| RCA/Resolution Review | 0 | 1 | 1 |
| **Total** | **70** | **192** | **262** |

**Mapping applied** — case-insensitive, with these wording aliases:

| Jira status (normalised) | Owner list entry |
| --- | --- |
| dev review and testing | dev review & testing |
| development analysis | dev analysis |
| ready for released | ready for release |
| under observation (no code change) | under obs |

## 19. Unspecified Primary Client

825 tickets (13.8%) carry no Primary Client. They are counted as **Internal** throughout this report, which is the owner's decision and matches PAMIT's rule for an unset field — it is a fallback, not a measurement. Without it they would be unattributable and the Client + Internal identity would fail.

| Metric | Count |
| --- | ---: |
| Open | 176 |
| Closed | 621 |
| Unmapped status | 28 |
| **Total** | **825** |

| Issue Type | Count |
| --- | ---: |
| Sub-task | 770 |
| Task | 42 |
| Document | 4 |
| Story | 4 |
| Client-Support | 3 |
| Bug | 2 |
| **Total** | **825** |

---

*Report generated by `tools/jira/ci_analysis_2026.py` on 2026-09-22 19:09*
