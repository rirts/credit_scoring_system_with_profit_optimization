# API and Project Fixes

## Plan
1. Fix src/api/main.py: Add `explainer = shap.TreeExplainer(model.named_steps['model'], background)` after loads.
2. Fix src/api/utils.py: Remove redundant explainer code.
3. Create src/models/train.py from notebook logic.
4. Add to src/features/__init__.py: def build_features().
5. Add to src/evaluation/__init__.py: def calculate_profit().
6. Create tests/test_api.py: import pytest, test_predict.

Test: uvicorn & pytest.

**Dependencies**: shap, pytest in requirements.txt (yes).
**Risks**: Pipeline structure changes – test after each.
**Outcomes**: Bug-free API, complete src, tests pass.
