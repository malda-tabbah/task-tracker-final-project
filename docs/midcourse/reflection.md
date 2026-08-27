# Reflection

Throughout this project, AI was used as both a planning assistant and a coding-support agent.

## Tools Used

- **ChatGPT Pro using GPT 5.5** for requirements, user stories, mini-ADR creation, ADR comparison, and documentation prompts
- **Cursor IDE using Grok 4.6 High** for backend and frontend implementation planning

## What Worked Well

AI helped most when the prompts were structured with:

- a clear role
- a clear task
- constraints
- source documents
- an output format

### User stories and architecture

- The user story prompt produced US-08 to US-11 for due date assignment, due date update, overdue detection, and search/filtering.
- The mini-ADR prompt helped translate these requirements into architecture changes without replacing the existing FastAPI and JSON-storage direction.

### Implementation planning in Cursor

The Cursor prompts were also useful because they referenced actual project files, which helped the agent produce backend and frontend plans grounded in the project structure:

- `@docs/midcourse/user-stories.md`
- `@docs/midcourse/mini-adr.md`
- `@backend/app/main.py`
- `@backend/app/models.py`

## Limitations and Issues

The logs also show that AI was not always consistent or precise.

### Weak backend testing prompt

- The request to “prepare the test script” caused the model to create an unwanted `acceptance_test.py` file instead of producing manual verification guidance.
- This was a prompting problem: the expected output should have been specified as curl commands, a manual test plan, or automated tests.

### Inconsistency in AI-generated requirements

- **US-08:** AI initially treated the due date as optional. Human review corrected it so that task creation fails when no due date is provided.
- **US-10:** AI first suggested that the overdue flag should no longer be returned when a task becomes `Done`. Review clarified that the flag should be set off automatically.

This review step was essential because it prevented unclear or incorrect acceptance criteria from becoming implementation input.

## Conclusion

- AI accelerated documentation, architecture thinking, and implementation planning.
- Human inspection remained necessary to catch ambiguity, control scope, and convert AI output into reliable project requirements.

