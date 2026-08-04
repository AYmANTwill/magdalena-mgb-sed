# Usable from Git Bash: make test | figures | deck | watch
# python is python3.10 on this box (plain `python` is a different interpreter).
PY ?= python3.10

.PHONY: test figures deck watch

test:
	$(PY) -m pytest tests/ -q

# scripts/ is being assembled in parallel; these paths are the agreed contract.
figures:
	$(PY) scripts/extract_notebook_figures.py
	$(PY) scripts/make_deck_charts.py

deck:
	$(PY) scripts/build_deck.py

watch:
	$(PY) watch_calib.py
