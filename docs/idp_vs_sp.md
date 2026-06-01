## Identity Provider (IdP)
System that:
authenticates users
verifies identity
manages login

Examples
Okta
Microsoft Entra ID
Auth0

What IdP Does
- Login handling
- Password validation
- MFA
- User identity verification
- SSO

## Service Provider (SP)
Application/service user wants to access.

Examples
Salesforce
AWS
Slack
Jira
What SP Does
- Provides application/service
- Trusts IdP authentication
- Grants access after validation

## Authentication Flow
1. User opens Salesforce
2. Salesforce redirects user to Okta
3. User logs into Okta
4. Okta validates credentials
5. Okta sends SAML response
6. Salesforce grants access

IdP
Identity Provider authenticates users and manages identities.
SP
Service Provider is the application that trusts the IdP and provides services to authenticated users.

The SP:

does NOT verify password directly

It trusts:

the IdP

## Architecture Diagram
+--------+        +--------+        +-------------+
| User   | -----> | Okta   | -----> | Salesforce  |
|        |        | (IdP)  |        |    (SP)     |
+--------+        +--------+        +-------------+
