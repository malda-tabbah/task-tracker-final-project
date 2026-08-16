# Pytest verification

Automated tests run one by one from `backend/` with `venv\Scripts\python.exe -m pytest`.

**Last run:** 16 August 2026. Combined result: **29 passed, 0 failed**.

| Suite | Tests | Passed | Failed |
| --- | --- | --- | --- |
| `tests/test_overdue.py` | 12 | 12 | 0 |
| `tests/test_search_filter.py` | 7 | 7 | 0 |
| `tests/test_due_date.py` | 10 | 10 | 0 |
| **Total** | **29** | **29** | **0** |

---

## `test_overdue.py`

| # | File | Test | Result |
| --- | --- | --- | --- |
| 1 | `test_overdue.py` | `test_is_overdue_when_due_date_passed_and_todo` | **PASS** |
| 2 | `test_overdue.py` | `test_is_overdue_when_due_date_passed_and_in_progress` | **PASS** |
| 3 | `test_overdue.py` | `test_is_overdue_false_when_due_date_is_today` | **PASS** |
| 4 | `test_overdue.py` | `test_is_overdue_false_when_due_date_is_future` | **PASS** |
| 5 | `test_overdue.py` | `test_is_overdue_false_when_status_is_done` | **PASS** |
| 6 | `test_overdue.py` | `test_is_overdue_false_when_due_date_missing` | **PASS** |
| 7 | `test_overdue.py` | `test_overdue_true_when_due_date_passed_and_todo` | **PASS** |
| 8 | `test_overdue.py` | `test_overdue_true_when_due_date_passed_and_in_progress` | **PASS** |
| 9 | `test_overdue.py` | `test_overdue_false_when_due_date_is_today` | **PASS** |
| 10 | `test_overdue.py` | `test_overdue_false_when_due_date_is_future` | **PASS** |
| 11 | `test_overdue.py` | `test_done_task_is_never_overdue` | **PASS** |
| 12 | `test_overdue.py` | `test_overdue_becomes_false_when_status_changes_to_done` | **PASS** |

---

## `test_search_filter.py`

| # | File | Test | Result |
| --- | --- | --- | --- |
| 1 | `test_search_filter.py` | `test_filter_by_due_date_returns_only_matches` | **PASS** |
| 2 | `test_search_filter.py` | `test_filter_by_overdue_true_returns_only_overdue` | **PASS** |
| 3 | `test_search_filter.py` | `test_filter_by_overdue_false_excludes_overdue` | **PASS** |
| 4 | `test_search_filter.py` | `test_filter_by_assignee_exact_match` | **PASS** |
| 5 | `test_search_filter.py` | `test_search_by_title_partial_case_insensitive` | **PASS** |
| 6 | `test_search_filter.py` | `test_combined_filters_use_logical_and` | **PASS** |
| 7 | `test_search_filter.py` | `test_filters_no_match_returns_empty_list` | **PASS** |

---

## `test_due_date.py`

| # | File | Test | Result |
| --- | --- | --- | --- |
| 1 | `test_due_date.py` | `test_create_task_with_valid_due_date_returns_201` | **PASS** |
| 2 | `test_due_date.py` | `test_create_task_missing_due_date_returns_422` | **PASS** |
| 3 | `test_due_date.py` | `test_create_task_invalid_due_date_format_returns_422` | **PASS** |
| 4 | `test_due_date.py` | `test_create_task_rejects_client_supplied_due_date_change_date` | **PASS** |
| 5 | `test_due_date.py` | `test_create_task_rejects_client_supplied_overdue` | **PASS** |
| 6 | `test_due_date.py` | `test_patch_due_date_sets_change_date_to_server_today` | **PASS** |
| 7 | `test_due_date.py` | `test_patch_same_due_date_does_not_set_change_date` | **PASS** |
| 8 | `test_due_date.py` | `test_patch_unrelated_field_does_not_change_due_date_change_date` | **PASS** |
| 9 | `test_due_date.py` | `test_patch_invalid_due_date_does_not_change_either_date_field` | **PASS** |
| 10 | `test_due_date.py` | `test_patch_due_date_missing_task_returns_404` | **PASS** |
