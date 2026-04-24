# Usage

**1.Build**
```
docker build -t ctp-logger .
```
**2.Create a Volume**
```
docker volume create ctp-logger-logs
```
**3.Run**
```
docker run --rm \
  --name ctp-logger \
  -v ctp-logger-logs:/app/logs \
  ctp-logger
```