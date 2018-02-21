DOC_FORMAT = html
.PHONY: doc

doc:
	cd doc && gmake ${DOC_FORMAT}
	find doc/_build/${DOC_FORMAT} -type f -exec fossil uv add '{}' \;
