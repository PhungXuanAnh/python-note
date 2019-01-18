# Run server 
```shell
./run.sh
```

# Token authentication

## Request post not auth
```shell
curl -XPOST http://localhost:5010/api_token_auth
```

## Request post with auth header
```shell
curl -XPOST http://localhost:5010/api_token_auth -H "Authorization: Token token123"
```

## Request get no need auth header
```shell
curl -XGET http://localhost:5010/api_token_auth
```

