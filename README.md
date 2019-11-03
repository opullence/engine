# engine


## Start mongodb

```bash
docker run -d --rm -p 27017:27017 mongo
```

## Start a celery worker

```bash
celery worker -A opulence.engine.app --queues=engine -l info
```
