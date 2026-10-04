---
name: the-bigger-picture
description: Ensures any new hunting tool, script, feature, or automation is delivered complete and tested so it actually increases productivity and income. Infers missing pieces, implements the full working set, tests before delivery, and shows expected results. Use whenever adding capability to the bug-bounty toolkit.
---

# The Bigger Picture

Load this skill whenever the user asks to add something — a feature, capability, option, integration, or any kind of add-on.

Users typically request only the single visible piece they have in mind. Your job is to reconstruct the complete picture so the addition actually works.

## Core Principle

Never implement a requested feature in isolation. Always determine *why* the user wants it and *what else* must exist for it to function correctly. Then test the full addition before delivering it.

## Workflow

### Phase 1: Understand Intent

1. **Identify the stated request**
   - What exact feature or change did the user ask for?

2. **Infer the underlying goal**
   - Why is the user asking for this?
   - What problem are they trying to solve?
   - What does success look like from their perspective?

3. **Map the imagined experience**
   - What does the user expect to happen after the feature is added?
   - What inputs will they provide?
   - What outputs or behaviors do they expect?

### Phase 2: Expand the Scope

4. **List everything required for the feature to work**
   - Supporting functions, data structures, configuration, error handling
   - UI/UX elements (if applicable)
   - Dependencies, imports, or external services
   - Edge cases and failure modes
   - Integration points with existing code or systems

5. **Identify gaps the user did not mention**
   - Missing validation
   - Missing state management
   - Missing documentation or usage examples
   - Missing tests or verification steps
   - Missing rollback or compatibility considerations

6. **Decide the minimal complete set**
   - Include only what is necessary for a working, coherent result
   - Avoid scope creep beyond what is required to fulfill the intent

### Phase 3: Implement and Test

7. **Build the complete addition**
   - Write all required pieces (not just the surface-level change)
   - Keep changes coherent with existing style and architecture

8. **Test before delivery**
   - Execute the new functionality with realistic inputs
   - Verify the results match the user's expected behavior
   - Check edge cases and error paths that are part of the complete picture
   - Confirm no regressions in related functionality

9. **Iterate internally if tests fail**
   - Fix issues discovered during testing
   - Re-test until the addition behaves as intended

### Phase 4: Deliver with Transparency

10. **Present the additions**
    - Show the complete set of changes (code, config, docs, etc.)
    - Clearly indicate what was added beyond the literal request and why

11. **Report expected results**
    - Describe exactly what the user should observe when using the new feature
    - Include example inputs and corresponding outputs based on your tests
    - Note any limitations or assumptions

12. **Invite feedback**
    - Ask the user to confirm whether the results match their vision
    - Offer to adjust based on their response

## Key Behaviors

- Always expand the request into a working whole before coding
- Never ship untested additions
- Prefer clarity over cleverness when explaining extra pieces you included
- Keep the user in the loop — they own the final judgment of whether it matches their intent

## When NOT to Use This Skill

- Pure informational questions with no addition requested
- Simple one-line fixes that require no supporting context
- Requests that are already fully specified and self-contained

## Quick Reference

**Trigger phrases include:**
- "add X"
- "can you include Y"
- "I want a feature that..."
- "make it also do Z"
- "add support for..."
- any request to extend existing functionality

**Success criteria:**
- The delivered addition works end-to-end
- Tests confirm expected behavior
- User receives both the implementation and a clear description of results to evaluate
