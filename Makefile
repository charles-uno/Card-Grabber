
TAG := card-finagler

image:
	docker build . -f Dockerfile -t $(TAG)

flip:
	docker run --rm -v $(PWD):/sandbox -w /sandbox $(TAG) ./builder.py
