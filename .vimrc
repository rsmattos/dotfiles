set nocompatible
filetype indent plugin on
syntax on

"===OPTIONS===
set hidden
set wildmenu
set showcmd

"===USABILITY===
set ignorecase
set smartcase
set backspace=indent,eol,start
set nostartofline
set ruler
set laststatus=2
set confirm
set number
set mouse=a

"===RELATIVE NUMBERING===
set rnu
function! ToggleNumbersOn()
    set nu!
    set rnu
endfunction
function! ToggleRelativeOn()
    set rnu!
    set nu
endfunction
autocmd FocusLost * call ToggleRelativeOn()
autocmd FocusGained * call ToggleRelativeOn()
autocmd InsertEnter * call ToggleRelativeOn()
autocmd InsertLeave * call ToggleRelativeOn()

"===INDENTATION===
set autoindent
set shiftwidth=4
set softtabstop=4
set expandtab

