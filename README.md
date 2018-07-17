# Github SSH keys fetcher

This is a service that manages users on a server based on Github organization
members and their SSH public keys on Github.

## Minimal summary

It essentialy does this:

```bash
export GITHUB_ORG="my-github-organization"
for login in `http https://api.github.com/orgs/${GITHUB_ORG}/members -p b | jq '.[].login' | tr -d '"'` ; do http https://api.github.com/users/${login}/keys -p b | jq '.[].key' ; done
```

and creates users on a Linux system based on it.

## Improvements

### Get refreshed from Github Organization webhooks

Ideally, when using this, you want to keep your users synced to the Team
members, and thus remove people when they are removed from the Team and/or
Organization.

This could be notified directly by [Github
webhooks](https://developer.github.com/webhooks/), especially since
[Organization webhooks were
added](https://developer.github.com/changes/2014-12-03-preview-the-new-organization-webhooks-api/)
