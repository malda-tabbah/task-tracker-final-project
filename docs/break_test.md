# Break Test — Due Date Validation

In this break test I want to weaken the due date validation on purpose by allowing tasks to be created with invalid due date in `TaskCreate.due_date` and `TaskUpdate.due_date` . Following this, the run `tests/test_due_date.py` tests fail. That shows the tests catch a broken rule.

## Where to change the code

Due date validation is not a custom function. FastAPI/Pydantic reject invalid dates because `due_date` is typed as `date` in `backend/app/models.py`

In `backend/app/models.py`:

1. `TaskCreate.due_date` — used when creating a task (US-08)
2. `TaskUpdate.due_date` — used when updating a task (US-09)

Change `date` to `str` so an invalid value such as `"not-a-date"` is accepted by the request model:

```python
# TaskCreate — break the create validation
due_date: str          # was: due_date: date

# TaskUpdate — break the update validation
due_date: Optional[str] = None   # was: due_date: Optional[date] = None
```

Do not change `TaskResponse.due_date`. Leave that as `date`.

## Run the Due Date Test Module

From `backend/`:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_due_date.py -v
```



## Expected result after the break

The invalid-date tests should fail. A passing suite would mean the tests did not catch the broken validation.

## Actual result

After changing `TaskCreate.due_date` and `TaskUpdate.due_date` to `str`.

**3 failed, 7 passed.**


| Test                                                              | Result after break | Why                                                                                         |
| ----------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------- |
| `test_create_task_with_valid_due_date_returns_201`                | PASS               | Valid ISO date still works                                                                  |
| `test_create_task_missing_due_date_returns_422`                   | PASS               | The field is still required                                                                 |
| `test_create_task_invalid_due_date_format_returns_422`            | **FAIL**           | `"not-a-date"` is accepted by `TaskCreate`; the request no longer returns 422               |
| `test_create_task_rejects_client_supplied_due_date_change_date`   | PASS               | Extra-field rule is unchanged                                                               |
| `test_create_task_rejects_client_supplied_overdue`                | PASS               | Extra-field rule is unchanged                                                               |
| `test_patch_due_date_sets_change_date_to_server_today`            | PASS               | Valid patch date still works                                                                |
| `test_patch_same_due_date_does_not_set_change_date`               | **FAIL**           | Request `due_date` is a string, stored value is a `date`, so the code treats it as a change |
| `test_patch_unrelated_field_does_not_change_due_date_change_date` | PASS               | Title-only update is unchanged                                                              |
| `test_patch_invalid_due_date_does_not_change_either_date_field`   | **FAIL**           | `"14-08-2026"` is accepted by `TaskUpdate`; the request no longer returns 422               |
| `test_patch_due_date_missing_task_returns_404`                    | PASS               | Missing-id rule is unchanged                                                                |


The two tests that prove US-08.3 and US-09.4 failed:

- `test_create_task_invalid_due_date_format_returns_422`
- `test_patch_invalid_due_date_does_not_change_either_date_field`

That is the break-test outcome: with validation removed, those tests no longer pass.

## Restore the code

Change the two fields back to `date`:

```python
due_date: date
due_date: Optional[date] = None
```

Then run the same pytest command. The suite should pass again (10 passed).