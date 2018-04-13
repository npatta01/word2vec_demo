# About
This is a simple word2vec app.

# Endpoints

/similar?positive=king,woman&negative=man
/alive

# Build
Download model
```
export GCP_BILLING_PROJECT=np-tutorials
gsutil -u $GCP_BILLING_PROJECT cp gs://np-tutorials-public/models/word2vec/word2vec-slim/GoogleNews-vectors-negative300-SLIM.bin.gz .
gunzip GoogleNews-vectors-negative300-SLIM.bin.gz
```

```
gcloud auth configure-docker
docker build -t w2vec .
```

# Run
```
docker run --rm -p 80:80 w2vec


```




# Running own project
```
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
```
