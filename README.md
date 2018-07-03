```bash
export GITHUB_ORG="my-github-organization"
for login in `http https://api.github.com/orgs/${GITHUB_ORG}/members -p b | jq '.[].login' | tr -d '"'` ; do http https://api.github.com/users/${login}/keys -p b | jq '.[].key' ; done
```

# Ideas

## Get refreshed from Github Organization webhooks

Ideally, when using this, you want to keep your users synced to the Team
members, and thus remove people when they are removed from the Team and/or
Organization.

This could be notified directly by [Github
webhooks](https://developer.github.com/webhooks/), especially since
[Organization webhooks were
added](https://developer.github.com/changes/2014-12-03-preview-the-new-organization-webhooks-api/)


## Backups

Backup `/etc/passwd`, `/etc/group` and `/etc/shadow` files with Ansible instead
of the current wrapper shell scripts?

