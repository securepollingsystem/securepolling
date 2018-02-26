DOC_FORMAT = html
.PHONY: doc sync push sync git-push fossil-push git-remote

doc:
	cd doc && gmake ${DOC_FORMAT}
	find doc/_build/${DOC_FORMAT} -type f -exec fossil uv add '{}' \;

sync: fossil-push git-push
fossil-push:
	fossil uv sync
	fossil configuration sync all
	fossil push
git-push:
	fossil export --git | git fast-import
	git push

git-remote:
	git remote add origin git@github.com:securepollingsystem/securepolling
	git push -u origin trunk
