
install:
	pip install

run:
# 	@python3 a_maze_ing.py
	@python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
# it need to fix or remove


lint:
lint-strict: #optional

.PHONY: install run debug clean lint lint-strict