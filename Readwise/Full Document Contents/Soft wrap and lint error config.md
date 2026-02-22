# Soft wrap and lint error config

![rw-book-cover](https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png)

## Metadata
- Author: [[CommunityEducational]]
- Full Title: Soft wrap and lint error config
- Category: #articles
- Summary: The user is trying to set up Neovim for editing markdown but is struggling with soft wrapping text to a readable length. They have configured options for text wrapping, but it doesn't seem to work as expected. Additionally, they are having trouble configuring markdownlint-cli2 to ignore certain line length rules.
- URL: https://www.reddit.com/r/neovim/comments/1fz29r2/comment/mhjk36k/?context=3

## Full Document
[r/neovim](https://www.reddit.com/r/neovim/) 

 [CommunityEducational](https://www.reddit.com/user/CommunityEducational/) 

  [Need Help┃Solved](https://www.reddit.com/r/neovim/?f=flair_name%3A%22Need%20Help%E2%94%83Solved%22)  

I am trying to use nvim for markdown. First question is about the soft wrap. What I am expecting is for nvim to keep the text line lengths to a readable length and not just full screen.

`vim.opt.wrap = true`

`vim.opt.linebreak = true`

`vim.opt.textwidth = 80`

But there is no difference with these set of not.

My other question is, how to configure the rules used by markdownlint-cli2, so that I can ignore the line length ones. I have tried setting the config in conform and using a rc file in the project dir. But the rule config isn't being obeyed!

He is what I see;

[![r/neovim - Soft wrap and lint error config](https://preview.redd.it/soft-wrap-and-lint-error-config-v0-my0uokp6ujtd1.png?width=1080&crop=smart&auto=webp&s=be9792d4cac5418e65191c0788a6b2234bca9006)](https://preview.redd.it/soft-wrap-and-lint-error-config-v0-my0uokp6ujtd1.png?width=1845&format=png&auto=webp&s=691c08bf284187e5949b81067c1d87b4fd8305e3)If you are out there and you feel you could give me advice to solve this, I would be very happy. Probably more so than I should be given the state of the rest of the world!
 Archived post. New comments cannot be posted and votes cannot be cast. 

  [MSPlive](https://www.reddit.com/user/MSPlive/)  

return {

"mfussenegger/nvim-lint",

optional = true,

opts = {

linters = {

["markdownlint-cli2"] = {

prepend\_args = { "--config", "/home/xxx/.config/.markdownlint.json", "--" },

},

},

},

}

---

% cat ~/.config/.markdownlint.json

{

"MD013": false,

"MD033": false,

"default": true

}

 }
