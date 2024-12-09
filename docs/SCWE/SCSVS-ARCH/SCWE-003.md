---
title: Insertion of Sensitive Data into Logs
id: SCWE-003
alias: data-in-logs
platform: []
profiles: [L1, L2, R]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-2, SCSVS-CODE-1]
  cwe: [200, 359, 497, 532]
  android-risks:
  - https://developer.android.com/privacy-and-security/risks/log-info-disclosure
refs:
  - https://stackoverflow.com/questions/45270547/is-read-logs-a-normal-or-dangerous-android-permission
status: new
---

## Overview

Mobile apps may write [sensitive data]() to logs. This may include sensitive user data, such as passwords, credit card numbers, or other personally identifiable information (PII), as well as sensitive system data, such as cryptographic keys, session tokens, or other sensitive information.

Logging all possible information is very useful at development time, especially for debugging the app. However, in production it might not always be necessary and should be prevented whenever possible to avoid any accidentally exposure to potential attackers.

## Modes of Introduction

This can typically occur in two ways:

- **System Logs**: The application may log sensitive data to the system log, which can be accessed by other applications on the device (in old OS versions or compromised devices or if they hold the appropriate permissions).
- **App Logs**: The application may log sensitive data to a file in the application's data directory, which can be accessed by any application on the device if the device is rooted.

## Impact

Loss of confidentiality: Sensitive data within logs is at risk of being exposed to an attacker with access to the device who may be able to extract it. This may lead to further attacks, such as identity theft, or compromise of the application's backend.

## Mitigations

The following are generic recommendations to avoid logging sensitive data in production releases:

- Avoid logging sensitive data at all.
- Redact sensitive data in logs.
- Remove logging statements unless deemed necessary to the application or explicitly identified as safe, e.g. as a result of a security audit.
- Use log levels properly to ensure that sensitive data is not logged in production releases.
- Use flags to disable logging in production releases.

The documentation for each platform provides best practices for developers:

- [Android mitigations to avoid log disclosure](https://developer.android.com/privacy-and-security/risks/log-info-disclosure#mitigations)
- [iOS mitigations to avoid log disclosure](https://developer.apple.com/documentation/os/logging/generating_log_messages_from_your_code#3665948)
