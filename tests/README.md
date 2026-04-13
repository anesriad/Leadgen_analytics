# Tests

Unit and integration tests.

```bash
python -m pytest tests/ -v
```

| File | Tests | Covers |
|------|-------|--------|
| `test_api.py` | 7 | `/health`, `/score`, validation, unseen categories, tier logic |
| `test_train.py` | 6 | Artefact existence, model interface, encoder keys, feature order |
