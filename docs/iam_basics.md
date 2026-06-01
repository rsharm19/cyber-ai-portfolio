# IAM Basics

## SSO
Single Sign-On allows one login for multiple applications.

## MFA
Multi-Factor Authentication adds additional verification.

## SAML
Security Assertion Markup Language enables authentication exchange.

## RBAC
Role-Based Access Control manages permissions using roles.

IdP	Identity Provider
SP	Service Provider
SSO	Single login for multiple apps
MFA	Extra authentication
RBAC	Role-based permissions

## IAM flow
User → Okta (IdP) → Salesforce (SP)
User → Microsoft Entra ID (IdP) → Salesforce (SP)

## Conditional Access Policy
Enable at Application level 
Conditional Access gives you the ability to enforce access requirements when specific conditions occur. 
When any user is outside the company network   They're required to sign in with multifactor authentication
When users in the 'Managers' group sign-in     They are required be on an Intune compliant or domain-joined device