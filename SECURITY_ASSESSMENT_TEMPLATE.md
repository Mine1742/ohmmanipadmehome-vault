# Security Assessment Template & Prompt Guide

**Purpose:** Reusable template and instructions for generating comprehensive security assessments for applications and proposals requiring security manager approval.

**Usage:** Use this template to gather requirements and create a security assessment document similar to SECURITY_ASSESSMENT.md

---

## How to Use This Template

### Step 1: Gather Application Information
Before generating the assessment, collect the following information about the application:

- [ ] Application name and version
- [ ] Business purpose and value
- [ ] Technology stack (languages, frameworks, libraries)
- [ ] External systems/APIs it integrates with
- [ ] Authentication mechanism (OAuth, API keys, credentials, etc.)
- [ ] Data classification (what data does it handle?)
- [ ] User base (internal, external, customers?)
- [ ] Deployment environment (cloud, on-premises, desktop, web)
- [ ] Open source vs proprietary
- [ ] Dependencies (list of libraries/packages)
- [ ] Code location (git repo, internal server, etc.)

### Step 2: Use AI Assistant Prompt (Below)
Copy the prompt below and provide it to an AI assistant (Claude, ChatGPT, etc.) along with the application details you've gathered.

### Step 3: Review & Customize
The generated assessment will follow this structure. Review each section and customize with organization-specific details.

### Step 4: Send to Security Manager
Once reviewed, the document is ready to send to your security manager (Kevin Scott) for approval.

---

## Pre-Assessment Information Gathering Checklist

**Before generating a security assessment, use this checklist to gather all necessary information. A complete assessment requires thorough information about the application.**

### Application Basics

- [ ] **Application Name** - Exact official name used in organization
- [ ] **Version Number** - Current version (e.g., 1.0.0, 2.3.1)
- [ ] **Project Status** - Development, Beta, Production-ready, Legacy
- [ ] **Requestor Name** - Who is requesting the security assessment
- [ ] **Requestor Department** - Which department/team is requesting
- [ ] **Target Security Manager** - Kevin Scott or other approver
- [ ] **Target Deployment Date** - When does this need to be approved by
- [ ] **Business Owner** - Executive sponsor or department head

### Purpose & Business Context

- [ ] **Business Purpose** - What problem does it solve? What business need does it address?
- [ ] **Business Value** - How does it benefit the organization? (cost savings, efficiency, etc.)
- [ ] **Users** - Who will use this? (internal staff, customers, partners, public?)
- [ ] **User Count** - How many users will access it?
- [ ] **Criticality** - Is this mission-critical, important, or nice-to-have?
- [ ] **Compliance Requirements** - Any regulatory requirements? (HIPAA, PCI-DSS, GDPR, SOC2, ISO27001, etc.)
- [ ] **Data Sensitivity** - What's the highest classification of data handled? (Public, Internal, Confidential, Secret?)

### Technical Architecture

- [ ] **Programming Language** - Python, Java, JavaScript, Go, Rust, etc.
- [ ] **Language Version** - Specific version (e.g., Python 3.8+, Node.js 18)
- [ ] **Framework** - Django, Flask, Spring Boot, Express, etc.
- [ ] **Architecture Type** - Monolithic, microservices, serverless, etc.
- [ ] **Code Repository** - Where is code stored? (GitHub, GitLab, Azure DevOps, internal server?)
- [ ] **Code Visibility** - Public, Private, Internal only?

### Deployment & Infrastructure

- [ ] **Deployment Type** - Web application, Desktop app, Mobile app, CLI tool, API/backend service
- [ ] **Target OS/Platform** - Windows, Linux, Mac, iOS, Android, Web browsers
- [ ] **OS Versions** - Specific versions supported (e.g., Windows 7+, Ubuntu 20.04+)
- [ ] **Cloud Provider** - AWS, Azure, Google Cloud, on-premises, hybrid?
- [ ] **Infrastructure as Code** - Docker, Kubernetes, Terraform, CloudFormation?
- [ ] **Execution Environment** - Single server, load-balanced, containerized, serverless?
- [ ] **Privileges Required** - Admin, root, user-level, or service account?
- [ ] **Network Exposure** - Internal only, internet-facing, hybrid?

### Authentication & Authorization

- [ ] **Authentication Method** - OAuth 2.0, SAML, LDAP, API keys, username/password, MFA?
- [ ] **Identity Provider** - Azure AD, Google, Okta, internal LDAP, Amazon Cognito?
- [ ] **MFA Capability** - Is multi-factor authentication supported/required?
- [ ] **Session Management** - How are sessions handled? (cookies, tokens, JWTs?)
- [ ] **Session Timeout** - What's the timeout period?
- [ ] **Authorization Model** - Role-based (RBAC), attribute-based (ABAC), access control lists?
- [ ] **Permission Levels** - How many different permission levels exist?
- [ ] **Service Accounts** - Does it use service accounts? How are they authenticated?

### Data & Integration

- [ ] **Data Types** - What kind of data does it process? (personal info, financial, health, business secrets?)
- [ ] **Data Sources** - Where does data come from? (user input, database, APIs, files?)
- [ ] **Data Storage** - Where is data stored? (database, file system, cloud storage, cache?)
- [ ] **Database Type** - SQL, NoSQL, in-memory, other?
- [ ] **Sensitive Data Fields** - List specific sensitive fields (SSN, passwords, API keys, etc.)
- [ ] **External APIs** - What third-party APIs does it use? (List them with authentication method)
- [ ] **Webhook Usage** - Does it use webhooks? From/to where?
- [ ] **File Upload** - Does it accept file uploads? What types? Size limits?
- [ ] **API Documentation** - Is API documentation available?

### Dependencies & Libraries

- [ ] **Package Manager** - npm, pip, Maven, Gradle, Cargo, etc.
- [ ] **Dependency List** - List all major dependencies (language, version, license)
- [ ] **Open Source Libraries** - Count of OSS dependencies used
- [ ] **Commercial Libraries** - Any paid/commercial libraries?
- [ ] **License Types** - MIT, Apache, GPL, Proprietary? Any GPL?
- [ ] **Dependency Scanning** - Is vulnerability scanning enabled for dependencies?
- [ ] **SBOM Available** - Is a Software Bill of Materials available or documented?

### Security Practices (Current State)

- [ ] **Input Validation** - Are there input validation checks? Where? How comprehensive?
- [ ] **Output Encoding** - Is output encoded to prevent injection attacks?
- [ ] **Hardcoded Secrets** - Any hardcoded API keys, passwords, credentials?
- [ ] **Configuration Management** - How are secrets managed? (.env, environment variables, vault, etc.?)
- [ ] **Logging** - What's currently logged? (application, API, authentication events?)
- [ ] **Error Handling** - How are errors handled? Does it expose sensitive data?
- [ ] **HTTPS/TLS** - Is encryption enforced for all network communication?
- [ ] **Code Review Process** - Is there a code review process in place?
- [ ] **Vulnerability Scanning** - Are automated security scans run? (SAST, DAST, dependency checks?)

### Testing & Quality

- [ ] **Test Coverage** - What percentage of code is covered by tests?
- [ ] **Security Testing** - Any security-specific tests? (penetration testing, threat modeling?)
- [ ] **Testing Framework** - What testing framework is used?
- [ ] **CI/CD Pipeline** - Is there an automated pipeline? (GitHub Actions, Jenkins, GitLab CI?)
- [ ] **Staging Environment** - Is there a staging/pre-prod environment for testing?
- [ ] **Performance Testing** - Are there load/performance tests?

### Integration Points

- [ ] **External Systems** - List all systems it integrates with (name, protocol, frequency)
- [ ] **API Endpoints** - How many API endpoints? (Public, internal, partner?)
- [ ] **Webhooks** - Does it send/receive webhooks? Where?
- [ ] **Database Connections** - What databases does it connect to? (internal, cloud, third-party?)
- [ ] **Message Queues** - Does it use message queues? (Kafka, RabbitMQ, SQS?)
- [ ] **Email Service** - Does it send emails? (SMTP, SendGrid, SES?)
- [ ] **Payment Processing** - Does it handle payments? (Stripe, PayPal, etc.?)
- [ ] **Third-Party APIs** - Full list of external API dependencies

### Documentation

- [ ] **README** - Is there a README with setup/deployment instructions?
- [ ] **Architecture Documentation** - Is architecture documented?
- [ ] **API Documentation** - Is API documentation available?
- [ ] **Security Documentation** - Is there any security documentation?
- [ ] **Deployment Guide** - Are deployment procedures documented?
- [ ] **Configuration Guide** - Are configuration options documented?
- [ ] **Troubleshooting Guide** - Is troubleshooting documented?
- [ ] **Runbook** - Is there an operational runbook?

### Known Issues & Risks

- [ ] **Known Vulnerabilities** - Any known security vulnerabilities?
- [ ] **Technical Debt** - Any identified technical security debt?
- [ ] **Limitations** - Any known limitations or constraints?
- [ ] **Deprecated Dependencies** - Any deprecated libraries in use?
- [ ] **Breaking Changes** - Recent changes that might affect security?
- [ ] **Previous Security Reviews** - Any prior security assessments? Results?

### Team & Support

- [ ] **Development Team** - Who built this? (names, contact info)
- [ ] **Technical Lead** - Who is the technical lead for this application?
- [ ] **Operations Team** - Who will operate/maintain this?
- [ ] **Security Contact** - Is there a designated security contact?
- [ ] **Support Escalation** - Who handles critical issues?
- [ ] **Documentation Owner** - Who maintains documentation?

### Additional Context

- [ ] **Compliance Certifications** - Required certifications (SOC2, ISO27001, PCI-DSS, HIPAA?)
- [ ] **Privacy Requirements** - Privacy policy requirements? GDPR compliance?
- [ ] **Industry Standards** - Any industry-specific standards? (NIST, CIS, etc.?)
- [ ] **Related Systems** - Other systems it depends on or affects?
- [ ] **Migration Path** - If replacing existing system, migration plan?
- [ ] **Rollback Plan** - Is there a rollback plan if issues arise?
- [ ] **Disaster Recovery** - Is there a DR/backup plan?
- [ ] **Support SLA** - Service level agreement requirements?

---

### Information Gathering Tips

**If you're missing information:**
- [ ] Contact the development team directly
- [ ] Request technical documentation from project lead
- [ ] Schedule a kickoff meeting with development team
- [ ] Review any existing README or architecture docs
- [ ] Ask for code repository access to review firsthand
- [ ] Request any prior security assessments or audit results
- [ ] Review project tickets or issues for known problems
- [ ] Check any existing compliance documentation

**Documentation to Request:**
- [ ] Source code repository (GitHub/GitLab access)
- [ ] Architecture diagrams or documentation
- [ ] Database schema documentation
- [ ] API documentation
- [ ] Deployment procedures
- [ ] Configuration guide
- [ ] Any prior security assessments
- [ ] Compliance audit results
- [ ] SBOM or dependency list

---

## AI Assistant Prompt Template

**Copy this prompt and replace bracketed items with your application details:**

---

### Prompt Start

You are creating a comprehensive security assessment document for a software application that requires security manager approval.

**Application Details:**
- **Name:** [Application Name]
- **Version:** [Version Number]
- **Date:** [Today's Date]
- **Requestor:** [Your Name / Team Name]
- **Security Manager:** [Kevin Scott or other]

**Application Purpose:** [Describe what the app does, its business value]

**Technology Stack:**
- **Language/Runtime:** [e.g., Python 3.8+, Node.js 18, Java 11]
- **Framework:** [e.g., Django, Express, Spring Boot]
- **Deployment:** [e.g., Windows desktop, Web server, Docker container, Cloud service]
- **Platform:** [e.g., Windows 7+, Linux, Mac, Web browser]

**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**External Integrations:**
- [System 1]: [Technology, authentication method]
- [System 2]: [Technology, authentication method]

**Authentication Method:** [OAuth 2.0, API keys, username/password, LDAP, etc.]

**Data Handled:** [Describe types of data: user info, financial records, health data, etc.]

**Dependencies:** [List major dependencies/libraries and count]

**Code Location:** [Git repo, internal server, etc.]

Please generate a professional security assessment document with the following structure:

1. **Executive Summary** - Overview, key findings, recommendations
2. **Application Overview** - Purpose, business value, technology stack, deployment
3. **Security Architecture & Controls** (10 subsections):
   - Authentication & authorization (describe mechanism, verify best practices)
   - Data security (classification, storage, protection)
   - Input validation & data integrity (what validation exists?)
   - API security (if applicable, endpoint security, encryption)
   - Configuration security (secrets management, environment-based config)
   - Code security (vulnerability assessment: SQL injection, XSS, command injection, hardcoded secrets, etc.)
   - Access control & permissions (multi-layer controls)
   - Logging & audit trail (current logging, recommendations)
   - Dependency management & supply chain (SBOM, license compliance, vulnerability scanning)
   - Encryption & data protection (transport, at-rest, key management)
4. **Risk Assessment**:
   - Threat model analysis
   - Risk ratings (critical, high, medium, low)
   - Residual risk summary
5. **Compliance & Governance**:
   - Security controls checklist (25+ items)
   - Pre-deployment checklist (40+ items)
   - Post-deployment checklist (20+ items)
6. **Architecture Documentation**:
   - Application architecture diagram (text-based)
   - Data model overview
   - Security-relevant code flows
7. **Recommendations**:
   - Pre-deployment requirements
   - Initial deployment recommendations
   - Post-deployment recommendations
   - Ongoing recommendations
8. **Appendices** - Files, contacts, references

**Format Requirements:**
- Markdown format (.md)
- Professional tone, suitable for security manager
- Use tables for data organization
- Include checkboxes (- [ ] ) for checklists
- Use emojis sparingly (✅, ⚠️, 🔴, 🟡, 🟢)
- Include code examples where relevant
- Reference specific files and locations

**Focus Areas:**
- Assume role of security auditor reviewing the application
- Identify risks honestly (no glossing over issues)
- Provide practical mitigations, not theoretical ones
- Use rating system: ✅ (secure), ⚠️ (monitor), 🔴 (critical fix required)
- Include detailed checklists with checkboxes for approval tracking

Generate the complete security assessment document now.

### Prompt End

---

## Template Content Structure

Use this outline when reviewing or customizing a generated assessment:

```
# [Application Name] - Security Assessment & Compliance Review

**Prepared for:** [Security Manager Name]
**Date:** [Date]
**Application:** [Name] [Version]
**Status:** Authorization Requested
**Requestor:** [Your Name/Team]

---

## Executive Summary

- One paragraph overview
- Key findings (5-8 bullet points with ✅, ⚠️, 🔴)
- Recommendation (Approved / Conditional / Rejected)

---

## 1. Application Overview

### Purpose & Business Value
- What it does
- Why organization needs it
- Business drivers

### Technology Stack
- Runtime environment
- Frameworks
- Integrations
- Deployment platform

### Platform & Deployment
- Operating systems
- Network requirements
- Privilege requirements

---

## 2. Security Architecture & Controls

### 2.1 Authentication & Authorization
- Mechanism used
- Security properties
- Flow diagrams
- Best practices assessment

### 2.2 Data Security
- Data classification
- Storage locations
- Protection measures
- Data flow diagrams

### 2.3 Input Validation & Data Integrity
- Validation rules (table format)
- Implementation details
- When validation occurs

### 2.4 API Security
- Endpoint security
- Transport security
- Authentication
- Error handling

### 2.5 Configuration Security
- Environment-based config approach
- Secrets management
- Configuration validation
- Best practices

### 2.6 Code Security
- Vulnerability assessment table
- Common weakness mitigation
- Secure coding practices
- Library usage assessment

### 2.7 Access Control & Permissions
- Multi-layer controls diagram
- Who can do what
- Permission enforcement

### 2.8 Logging & Audit Trail
- Current logging
- Audit trail capabilities
- Recommendations
- Log security

### 2.9 Dependency Management
- Dependency table (package, version, license, status)
- SBOM reference
- Vulnerability scanning capability
- License compliance

### 2.10 Encryption & Data Protection
- Transport security
- Data at rest encryption
- Key management
- Standards compliance

---

## 3. Risk Assessment

### 3.1 Threat Model
- Attack vectors
- Threat analysis
- Mitigation status

### 3.2 Risk Ratings
- Critical risks
- High risks
- Medium risks
- Low risks

### 3.3 Residual Risk Summary
- Risk table with likelihood/impact/rating

---

## 4. Compliance & Governance

### 4.1 Security Controls Checklist
- 25+ items organized by category
- ✅/⚠️ status indicators
- Coverage across all control areas

### 4.2 Pre-Deployment Checklist
- 40+ verification items
- Organized by category
- Checkboxes for tracking

### 4.3 Post-Deployment Checklist
- 20+ ongoing items
- Implementation tracking
- Timeline recommendations

---

## 5. Architecture Documentation

### 5.1 Application Architecture
- Text-based architecture diagram
- Layer descriptions
- Component relationships

### 5.2 Data Model
- Key data structures
- Field definitions
- Relationships

### 5.3 Security-Relevant Code Paths
- Authentication flow
- Data creation/update flow
- Error handling flow

---

## 6. Recommendations

### 6.1 Pre-Deployment Requirements
- Critical items (must complete before production)
- Timeline and effort estimates

### 6.2 Initial Deployment Recommendations
- High-priority items (complete in first iteration)
- Implementation guidance

### 6.3 Post-Deployment Recommendations
- Medium-priority items (within 90 days)
- Ongoing improvements

### 6.4 Ongoing Recommendations
- Continuous security practices
- Monitoring and maintenance
- Review cadence

---

## 7. Conclusion

- Summary of findings
- Recommended action
- Conditions for approval (if any)

---

## Appendix A: Files Referenced

- Key documentation files
- Code repositories
- Configuration examples

---

## Appendix B: Contact & Support

- Security manager contact
- Development team contact
- Incident reporting

---

**Document Status:** [Authorization Requested / Approved / Conditional]
**Date Prepared:** [Date]
**Version:** 1.0
**Classification:** Internal Use
```

---

## Customization Checklist

When generating a security assessment for a new application, ensure you:

- [ ] **Replace all [bracketed items]** with actual application details
- [ ] **Verify all claims** about security controls (if you made them up, the security manager will know)
- [ ] **Include real code examples** (don't invent authentication mechanisms that don't exist)
- [ ] **Be honest about risks** (security managers respect truthfulness more than false perfection)
- [ ] **Provide practical mitigations** (not theoretical, but actionable steps)
- [ ] **Include references** (point to actual files, documentation, code locations)
- [ ] **Use consistent formatting** (tables, lists, diagrams)
- [ ] **Add organization-specific details** (your security policies, compliance requirements, risk tolerance)
- [ ] **Review for accuracy** (have a technical team member verify claims before submitting)
- [ ] **Identify known issues** (be upfront about security gaps, not evasive)

---

## Tips for Quality Security Assessments

### Do ✅
- Be thorough and detailed
- Use actual data from code review
- Reference specific files and line numbers
- Provide actionable recommendations
- Include effort/timeline estimates
- Use risk rating system consistently
- Include checklists for approval tracking
- Organize information logically
- Use tables for comparison data
- Provide clear diagrams (text-based)
- Reference official documentation
- Be specific (not vague)

### Don't ❌
- Make up security features that don't exist
- Ignore obvious vulnerabilities
- Be overly negative or dismissive
- Use jargon without explanation
- Write vague recommendations
- Forget to include checklists
- Make assumptions without verification
- Skip technical details
- Use different formatting inconsistently
- Avoid honest risk assessment
- Be overly theoretical
- Use undefined acronyms

---

## Common Security Assessment Scenarios

### Scenario 1: Web Application
**Focus areas:**
- HTTPS/TLS encryption
- SQL injection prevention
- XSS (Cross-site scripting) prevention
- CSRF (Cross-site request forgery) prevention
- Authentication (session management, password handling)
- API rate limiting
- Input validation (all user inputs)
- Database security
- Deployment security (containerization, orchestration)
- Infrastructure security (CDN, WAF, DDoS protection)

### Scenario 2: Desktop Application
**Focus areas:**
- Local file security
- Operating system privilege model
- System integration security
- Configuration file protection
- No admin privileges required
- Offline functionality security
- Data caching
- Update mechanism security
- Third-party library integration

### Scenario 3: Mobile Application
**Focus areas:**
- Mobile OS security features (certificate pinning, secure storage)
- API authentication
- Local data encryption
- Sensitive data in memory
- Third-party SDKs
- App store security requirements
- Jailbreak/rooting detection (if applicable)
- Biometric authentication
- Location data handling

### Scenario 4: Cloud Service
**Focus areas:**
- Multi-tenancy isolation
- Encryption at rest and in transit
- Key management
- Identity and access management (IAM)
- Audit logging
- Compliance certifications
- Data residency
- Backup and disaster recovery
- Network security (VPC, firewalls)
- Vulnerability scanning and penetration testing

### Scenario 5: API/Backend Service
**Focus areas:**
- API authentication (OAuth, JWT, API keys)
- Rate limiting
- Input validation
- Output encoding
- Error handling
- Logging (without exposing secrets)
- Dependency management
- Infrastructure security
- Scalability and DoS protection
- Data validation and sanitization

---

## Quick Reference: Security Control Categories

When creating a security assessment, ensure you cover these control categories:

1. **Identity & Access Management**
   - Authentication mechanism
   - Authorization model
   - User provisioning/deprovisioning
   - Multi-factor authentication
   - Privilege escalation prevention

2. **Data Security**
   - Data classification
   - Encryption at rest
   - Encryption in transit
   - Data retention
   - Data residency

3. **Application Security**
   - Input validation
   - Output encoding
   - Error handling
   - Secure coding practices
   - Dependency management

4. **Infrastructure Security**
   - Network security
   - Operating system hardening
   - Configuration management
   - Patch management
   - Physical security (if applicable)

5. **Logging & Monitoring**
   - Audit logging
   - Alert mechanisms
   - Log retention
   - Log access control
   - Anomaly detection

6. **Incident Response**
   - Incident handling procedures
   - Communication plan
   - Recovery procedures
   - Root cause analysis
   - Lessons learned process

7. **Compliance & Governance**
   - Regulatory compliance (HIPAA, PCI-DSS, GDPR, etc.)
   - Security policies
   - Risk assessment
   - Security training
   - Third-party assessments

---

## Document Submission Checklist

Before submitting to security manager, verify:

- [ ] Document is in Markdown (.md) format
- [ ] Professional formatting and structure
- [ ] All sections populated with actual data (no placeholders)
- [ ] No spelling or grammar errors
- [ ] Checkboxes included for approval tracking
- [ ] Risk ratings are consistent
- [ ] Recommendations are specific and actionable
- [ ] All claims are verifiable (reference actual files/code)
- [ ] Executive summary is clear and concise
- [ ] Checklists are comprehensive
- [ ] Document reflects actual application (not idealized version)
- [ ] Security manager name included in "Prepared for"
- [ ] Date and requestor information included
- [ ] Status clearly marked "Authorization Requested"

---

## Example Security Assessment Reference

For a complete example, see: **SECURITY_ASSESSMENT.md** (Device Inventory Tracker)

This template was used to generate that assessment. You can use it as a reference for structure and content organization.

---

**Template Version:** 1.0
**Created:** January 15, 2026
**Last Updated:** January 15, 2026
**Status:** Ready for Use

