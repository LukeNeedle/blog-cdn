# Blog CDN
This is the CDN that I use for my blog.

Store your images in `./CDN/images`.

Create `secrets.json` with the following keys:
- "secretKey"
- "dev"
- "url"

`url` is the url of the deployed cdn node (in this case the only cdn server). It should include `http`/`https` but not the the trailing /. For example `'url': 'http://localhost:8080'`

`dev` should be either `true` or `false`. If it is set to true then the program doesn't try to pull from the repo on first startup.

`secretKey` should be a random string of characters.
