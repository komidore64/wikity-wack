.PHONY: clean
clean:
	find ./ -iname '*.pyc' -exec rm -rfv {} +
	find ./ -type d -iname __pycache__ -exec rm -rfv {} +
