---
name: scientist
description: Deep investigation skill used when a high-potential vulnerability cannot yet be triggered. Compiles source, studies internals, and exhaustively tests payloads, mutations, and encodings to either confirm a payable finding or prove the endpoint is secure so time is not wasted.
---

# Scientist: Targeted Vulnerability Research & Exhaustive Testing

Load this skill when you have identified a potential vulnerability but are having difficulty triggering it. This skill guides a methodical, research-driven approach to either prove an endpoint is not vulnerable through exhaustive testing, or confirm and document a vulnerability.

## Core Principle

The only way to conclusively prove an endpoint is secure is to test every possible attack vector, payload, mutation, and encoding until no further tests remain. This is the "scientist" approach: systematic, thorough, and evidence-based.

## Workflow

### Phase 1: Target Acquisition & Source Analysis

1. **Identify the Exact Endpoint**
   - URL path, API route, GraphQL query/mutation, or specific function
   - Note the technology stack (e.g., Taskcluster GraphQL, AWS Lambda, Node.js, Python Flask)
   - Document all known parameters, headers, and input vectors

2. **Download and Compile Source Code**
   - Locate the official repository for the endpoint's codebase
   - Download the complete source code
   - Set up the development environment
   - Compile/build the project to understand dependencies
   - Identify the specific code handling the target endpoint

3. **Study Internal Mechanics**
   - Read the source code for the endpoint handler
   - Trace data flow: input → processing → output
   - Identify all parsing, validation, and sanitization functions
   - Map the execution path and any called internal/external services
   - Document all libraries and frameworks involved
   - Note any custom parsing or business logic

### Phase 2: Historical Exploit Research

4. **Research Similar Exploits**
   - Load the serpapi skill to perform targeted web searches for:
     - Major bug bounty platforms (HackerOne, Bugcrowd, etc.) for reports on the same technology stack, endpoint type, vendor/product, or vulnerability class
     - Vulnerability databases (CVE, NVD, Exploit-DB)
     - Security advisory mailing lists
     - GitHub for proof-of-concept exploits
   - Document all relevant findings with links and descriptions

5. **Extract Attack Patterns**
   - From each relevant exploit, extract:
     - The specific vulnerability condition
     - The payloads that worked
     - The context/environment where it succeeded
     - Any special encoding or obfuscation used
     - The patch/fixed version details
   - Identify common themes and variations

### Phase 3: Hypothesis Generation

6. **Formulate Test Hypotheses**
   - Based on source code analysis and historical research, generate specific hypotheses:
     - "If I send [payload] with [encoding], it might trigger [vulnerability] because [reason from code]"
     - "The endpoint might be vulnerable to [attack type] due to [missing validation in code]"
   - Prioritize hypotheses by likelihood and potential impact

### Phase 4: Exhaustive Testing

7. **Create Comprehensive Test Matrix**
   For each hypothesis, systematically test:

   **Payload Types:**
   - Standard exploit payloads for the vulnerability class
   - Obfuscated payloads (base64, URL, Unicode, etc.)
   - Polyglot payloads
   - Payloads from historical exploits (Phase 2)

   **Mutation Strategies:**
   - Case variations (upper, lower, mixed)
   - Character substitutions (homoglyphs, similar-looking)
   - Whitespace variations (spaces, tabs, newlines, URL-encoded)
   - Comment insertion (//, /* */, #, etc.)
   - Truncation and partial payloads
   - Concatenation with other strings

   **Encoding Schemes:**
   - URL encoding (single, double, mixed)
   - Base64, Base64URL
   - Hex encoding
   - Unicode (UTF-8, UTF-16, UTF-32)
   - HTML entity encoding
   - JavaScript string escaping
   - JSON escaping
   - XML/CDATA escaping
   - Custom encoding used by the application

   **Context Variations:**
   - Different HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
   - Different content types (application/json, application/x-www-form-urlencoded, multipart/form-data, text/plain, etc.)
   - Different headers (Content-Type, Accept, User-Agent, custom headers)
   - Different parameter locations (query string, body, headers, cookies, path parameters)
   - Different authentication states (unauthenticated, authenticated, different privilege levels)

8. **Execute Tests Methodically**
   - Start with the most likely hypotheses
   - For each test, document:
     - Exact request (method, URL, headers, body)
     - Response received (status code, headers, body)
     - Any observed anomalies
     - Timestamp
   - If a test produces unexpected behavior, investigate further
   - If a test triggers an error, analyze the error for clues

### Phase 5: Analysis & Conclusion

9. **Analyze Results**
   - Review all test results systematically
   - Look for patterns in responses
   - Identify any partial successes or near-misses
   - Correlate findings with source code analysis

10. **Draw Conclusion**
    - **Vulnerability Confirmed:** If any test successfully exploits the endpoint, document:
      - Steps to reproduce
      - Impact assessment
      - Suggested remediation
    - **Endpoint Proven Secure:** If all tests are exhausted with no vulnerability triggered, document:
      - Comprehensive list of all tests performed
      - Reasoning for why the endpoint is considered secure
      - Any remaining uncertainty or limitations

## Deliverables

When this skill completes, produce:

1. **Target Profile Document**
   - Endpoint details
   - Source code location and relevant files
   - Internal mechanics summary
   - Technology stack

2. **Research Findings Report**
   - List of all relevant historical exploits found
   - Extracted attack patterns
   - Links to all references

3. **Test Matrix & Results**
   - Complete list of all tests performed
   - Request/response pairs for each test
   - Any anomalies or notable responses

4. **Final Assessment**
   - Conclusion (vulnerable or secure)
   - Evidence supporting the conclusion
   - Any recommendations or next steps

## Tools & Resources

Use these tools during the scientist workflow:
- **Code Analysis:** Read and analyze source code directly
- **Web Search:** Use the serpapi skill for all web search tasks (CVEs, exploits, bug bounty reports)
- **GitHub:** Search for proof-of-concepts and vulnerable code patterns
- **Local Testing:** Set up and test against local instances when possible
- **Proxy Tools:** Use intercepting proxies to manipulate requests (when in testing environment)

## Important Notes

- Always ensure you have proper authorization before testing any endpoint
- Respect rate limits and terms of service
- Do not perform destructive testing on production systems
- Document everything meticulously - this is the scientific method applied to security
- If testing on live systems, use only authorized test accounts and environments
- Consider the legal and ethical implications of all testing activities
