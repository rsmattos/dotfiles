-- set leader key to space
vim.g.mapleader = " "

-- use jk to exit insert mode
vim.keymap.set('i', 'jk', '<ESC>')

-- clear search highlights
vim.keymap.set("n", "<leader>nh", ":nohl<CR>")

-- window management
vim.keymap.set("n", "<leader>sv", "<C-w>v")        -- split window vertically
vim.keymap.set("n", "<leader>sh", "<C-w>s")        -- split windows horizontally
vim.keymap.set("n", "<leader>se", "<C-w>=")        -- makes split windows equal width and height
vim.keymap.set("n", "<leader>sx", ":close<CR>")    -- closes current split window

