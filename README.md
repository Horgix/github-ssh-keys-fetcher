```bash
export GITHUB_ORG="my-github-organization"
for login in `http https://api.github.com/orgs/${GITHUB_ORG}/members -p b | jq '.[].login' | tr -d '"'` ; do http https://api.github.com/users/${login}/keys -p b | jq '.[].key' ; done
```
