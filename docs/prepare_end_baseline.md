# End-of-Course Repository Preparation Procedure

## Purpose

This procedure documents how the completed mid-course Task Tracker project was used as the baseline for a separate end-of-course working environment, while preserving the mid-course project and maintaining separate private development and public submission repositories.

## Procedure

### 1. Preserve the Mid-Course Project as the Baseline

The completed mid-course project was retained as the starting point for the end-of-course work.

The objective was to avoid continuing development directly inside the mid-course project folder because that folder represented the completed mid-course submission.

The existing mid-course project therefore remained available as a historical and working reference.

---

### 2. Create a Separate Local End-Course Project Folder

A new local project folder was created from the existing mid-course project:

```text
C:\_Malda\Projects\task-tracker - end
```

This created a separate working environment for the end-of-course activities.

The resulting local structure conceptually became:

```text
C:\_Malda\Projects\
│
├── task-tracker - mid
│   └── preserved mid-course project
│
└── task-tracker - end
    └── working copy for end-course development
```

Because the new folder originated from the existing Git project, its Git history and repository configuration were also carried forward. This allowed the end-course project to retain the development history established during the earlier phases.

---

### 3. Establish the End-Course Development Branch

The end-course work was separated from the earlier project work through the dedicated branch:

```text
end-course-project
```

The branch became the working branch for end-course development rather than continuing directly on `master` or modifying the completed `mid-course-project` branch.

The branch relationship therefore became conceptually:

```text
Task Tracker development history
        │
        ├── master
        │
        ├── mid-course-project
        │       └── completed mid-course state
        │
        └── end-course-project
                └── end-course development
```

This preserved the earlier project milestones while allowing the end-course work to evolve independently.

---

### 4. Retain the Private Repository as the Development Repository

The cloned/copied end-course working directory retained `origin` as the private development repository:

```text
origin
https://github.com/malda-tabbah/task-tracker.git
```

The private repository therefore continued to hold the project's development branches, including:

```text
origin/master
origin/mid-course-project
origin/end-course-project
```

The end-course branch was synchronized with:

```text
origin/end-course-project
```

This meant that the private repository remained the source repository containing the complete development history.

---

### 5. Create/Configure a Separate Public End-Course Remote

A separate Git remote was configured for the public end-course repository:

```text
end-public
https://github.com/malda-tabbah/end-course-project.git
```

The repository arrangement therefore became:

```text
task-tracker - end
│
└── end-course-project
      │
      ├── origin
      │     └── Private task-tracker repository
      │           └── origin/end-course-project
      │
      └── end-public
            └── Public end-course repository
                  └── main
```

This separation allowed development to remain in the private repository while only the intended end-course version was published to the public repository.

---

### 6. Continue End-Course Development in the New Working Copy

Subsequent end-course activities were performed from:

```text
C:\_Malda\Projects\task-tracker - end
```

on:

```text
end-course-project
```

The end-course history included additional project work such as CI, Docker-related files, review documentation, technical notes, and governance/security documentation.

The dedicated folder and branch ensured that these changes did not alter the preserved mid-course working copy.

---

### 7. Verify the End-Course Working Repository Before Release

Before publishing the end-course repository, the local repository was explicitly verified:

```powershell
git rev-parse --show-toplevel
```

Result:

```text
C:/_Malda/Projects/task-tracker - end
```

The branch was verified using:

```powershell
git branch --show-current
```

Result:

```text
end-course-project
```

The remotes were verified using:

```powershell
git remote -v
```

confirming:

```text
end-public → public end-course-project repository
origin     → private task-tracker repository
```

Finally:

```powershell
git status
```

confirmed:

```text
On branch end-course-project
Your branch is up to date with 'origin/end-course-project'.
```

---

### 8. Check the Existing Public End-Course Repository

The public repository still contained the earlier mid-course project state.

Its current state was retrieved using:

```powershell
git fetch end-public
```

Remote branches were checked with:

```powershell
git branch -r
```

which confirmed:

```text
end-public/HEAD -> end-public/main
end-public/main
origin/end-course-project
origin/master
origin/mid-course-project
```

---

### 9. Compare Public Main with the End-Course Branch

Before changing the public repository, the histories were compared.

```powershell
git log --oneline end-public/main..end-course-project
```

This returned the end-course commits that were not yet present in public `main`.

The reverse comparison was then performed:

```powershell
git log --oneline end-course-project..end-public/main
```

No commits were returned.

This confirmed that the public repository was simply behind the end-course branch and had not independently diverged.

A force push was therefore unnecessary.

---

### 10. Publish the End-Course Version

The end-course branch was published to the public repository using:

```powershell
git push end-public end-course-project:main
```

Git reported:

```text
To https://github.com/malda-tabbah/end-course-project.git
f4b5b47..f3367a9  end-course-project -> main
```

The operation successfully advanced the public repository from its previous state at `f4b5b47` to the end-course state at `f3367a9`.

## Final Repository State

```text
LOCAL WORKING COPIES
│
├── task-tracker - mid
│     └── Preserved mid-course project
│
└── task-tracker - end
      └── end-course-project
              │
              ├──────────────► origin/end-course-project
              │                Private development repository
              │
              └──────────────► end-public/main
                               Public end-course repository
```

## Status Summary

| Item                                             | Final Status |
| ------------------------------------------------ | ------------ |
| Mid-course local project preserved               | **Yes**      |
| Separate end-course local folder created         | **Yes**      |
| Git history retained from earlier project        | **Yes**      |
| Dedicated `end-course-project` branch used       | **Yes**      |
| Private development repository retained          | **Yes**      |
| `origin/end-course-project` synchronized         | **Yes**      |
| Separate public end-course repository configured | **Yes**      |
| Public repository checked before publishing      | **Yes**      |
| Branch divergence detected                       | **No**       |
| Force push required                              | **No**       |
| End-course branch published to public `main`     | **Yes**      |
| Public `main` release commit                     | `f3367a9`    |

**Overall status:** The mid-course project was successfully preserved and used as the baseline for a separate end-course working environment. End-course development was isolated through a dedicated local folder and Git branch, maintained in the private development repository, and subsequently published to the separate public end-course repository.
