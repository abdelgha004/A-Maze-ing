
install:
	pip install

run:
	@python3 a_maze_ing.py
# 	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdp a_maze_ing.py config.txt

clean:
lint:

lint-strict: #optional

.phony: install run debug clean lint lint-strict