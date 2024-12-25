# Blog CDN
This is the CDN that I use for my blog.

Store your images in `./CDN/images`.

Create `secrets.json` with the following keys:
- "secretKey"
- "dev"

`dev` should be either `true` or `false`. If it is set to true then the program doesn't try to pull from the repo on first startup.
`secretKey` should be a random string of characters.