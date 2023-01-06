-- line numbering
vim.o.relativenumber = true             -- show relative line numbers
vim.o.number = true                     -- show absolute current line number

-- tabs & indentation
vim.o.tabstop = 4                       -- 4 spaces for tabs
vim.o.shiftwidth = 4                    -- 4 spaces for indent
vim.o.expandtab = true                  -- changes tabs to spaces
vim.o.autoindent = true                 -- copy current indent when creating new line

-- clipboard
-- vim.o.clipboard:append("unnamedplus")   -- use system clipboard as buffer

-- split windows
vim.o.splitright = true                 -- split vertical window to the right
vim.o.splitbelow = true                 -- split vertical window to the bottom
