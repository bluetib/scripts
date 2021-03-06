source ~/.vim/bundles.vim

" encoding dectection
set fileencodings=utf-8,gb2312,gb18030,gbk,ucs-bom,cp936,latin1

" enable filetype dectection and ft specific plugin/indent
filetype plugin on
filetype plugin indent on

" enable syntax hightlight and completion
syntax on

"--------
" Vim UI
"--------
" color scheme
set background=dark
colorscheme desert
"color vividchalk

" highlight current line
"au WinLeave * set nocursorline nocursorcolumn
"au WinEnter * set cursorline cursorcolumn
set cursorline
"set cursorcolumn

" search
set incsearch
"set highlight	" conflict with highlight current line
set noignorecase
set smartcase

" editor settings
set history=1000
set nocompatible

"set nofoldenable												   " disable folding"
set confirm														  " prompt when existing from an unsaved file
set backspace=indent,eol,start									  " More powerful backspacing
set t_Co=256													  " Explicitly tell vim that the terminal has 256 colors "
set mouse=a														  " use mouse in all modes
set report=0													  " always report number of lines changed				 "
set nowrap														  " dont wrap lines
set scrolloff=5													  " 5 lines above/below cursor when scrolling
set number														  " show line numbers
set showmatch													  " show matching bracket (briefly jump)
set showcmd														  " show typed command in status bar
set title														  " show file in titlebar
set laststatus=2												  " use 2 lines for the status bar
set matchtime=2													  " show matching bracket for 0.2 seconds
set matchpairs+=<:>												  " specially for html
set hlsearch
" set relativenumber
" set paste
set ttymouse=xterm2

" Default Indentation
set autoindent
set smartindent		" indent when
set tabstop=4		" tab width
set softtabstop=4	" backspace
set shiftwidth=4	" indent width
" set textwidth=79
" set smarttab
"set expandtab		 " expand tab to space
set wrap
"
autocmd FileType php setlocal tabstop=2 shiftwidth=2 softtabstop=2 textwidth=120
autocmd FileType ruby setlocal tabstop=2 shiftwidth=2 softtabstop=2 textwidth=120
autocmd FileType php setlocal tabstop=4 shiftwidth=4 softtabstop=4 textwidth=120
autocmd FileType coffee,javascript setlocal tabstop=2 shiftwidth=2 softtabstop=2 textwidth=120
autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 textwidth=120
autocmd FileType html,htmldjango,xhtml,haml setlocal tabstop=2 shiftwidth=2 softtabstop=2 textwidth=0
autocmd FileType sass,scss,css setlocal tabstop=2 shiftwidth=2 softtabstop=2 textwidth=120

" syntax support
autocmd Syntax javascript set syntax=jquery   " JQuery syntax support
" js
let g:html_indent_inctags = "html,body,head,tbody"
let g:html_indent_script1 = "inc"
let g:html_indent_style1 = "inc"

"-----------------
" Plugin settings
"-----------------
" Rainbow parentheses for Lisp and variants
let g:rbpt_colorpairs = [
	\ ['brown',		  'RoyalBlue3'],
	\ ['Darkblue',	  'SeaGreen3'],
	\ ['darkgray',	  'DarkOrchid3'],
	\ ['darkgreen',   'firebrick3'],
	\ ['darkcyan',	  'RoyalBlue3'],
	\ ['darkred',	  'SeaGreen3'],
	\ ['darkmagenta', 'DarkOrchid3'],
	\ ['brown',		  'firebrick3'],
	\ ['gray',		  'RoyalBlue3'],
	\ ['black',		  'SeaGreen3'],
	\ ['darkmagenta', 'DarkOrchid3'],
	\ ['Darkblue',	  'firebrick3'],
	\ ['darkgreen',   'RoyalBlue3'],
	\ ['darkcyan',	  'SeaGreen3'],
	\ ['darkred',	  'DarkOrchid3'],
	\ ['red',		  'firebrick3'],
	\ ]
let g:rbpt_max = 16
autocmd Syntax lisp,scheme,clojure,racket RainbowParenthesesToggle

" tabbar
let g:Tb_MaxSize = 2
let g:Tb_TabWrap = 1

hi Tb_Normal guifg=white ctermfg=white
hi Tb_Changed guifg=green ctermfg=green
hi Tb_VisibleNormal ctermbg=252 ctermfg=235
hi Tb_VisibleChanged guifg=green ctermbg=252 ctermfg=white

" easy-motion
let g:EasyMotion_leader_key = '<Leader>'

" Tagbar
let g:tagbar_left=1
let g:tagbar_width=30
let g:tagbar_autofocus = 1
let g:tagbar_sort = 0
let g:tagbar_compact = 1
" tag for coffee
if executable('coffeetags')
  let g:tagbar_type_coffee = {
		\ 'ctagsbin' : 'coffeetags',
		\ 'ctagsargs' : '',
		\ 'kinds' : [
		\ 'f:functions',
		\ 'o:object',
		\ ],
		\ 'sro' : ".",
		\ 'kind2scope' : {
		\ 'f' : 'object',
		\ 'o' : 'object',
		\ }
		\ }

  let g:tagbar_type_markdown = {
	\ 'ctagstype' : 'markdown',
	\ 'sort' : 0,
	\ 'kinds' : [
		\ 'h:sections'
	\ ]
	\ }
endif

" Nerd Tree
let NERDChristmasTree=0
let NERDTreeWinSize=30
let NERDTreeChDirMode=2
let NERDTreeIgnore=['\~$', '\.pyc$', '\.swp$']
" let NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$',	'\~$']
let NERDTreeShowBookmarks=1
let NERDTreeWinPos = "right"

" nerdcommenter
let NERDSpaceDelims=1
" nmap <D-/> :NERDComToggleComment<cr>
let NERDCompactSexyComs=1

" ZenCoding
let g:user_zen_expandabbr_key='<C-j>'

" powerline
"let g:Powerline_symbols = 'fancy'

" NeoComplCache
let g:neocomplcache_enable_at_startup=1
let g:neoComplcache_disableautocomplete=1
"let g:neocomplcache_enable_underbar_completion = 1
"let g:neocomplcache_enable_camel_case_completion = 1
let g:neocomplcache_enable_smart_case=1
let g:neocomplcache_min_syntax_length = 3
let g:neocomplcache_lock_buffer_name_pattern = '\*ku\*'
set completeopt-=preview

imap <C-k> <Plug>(neocomplcache_snippets_force_expand)
smap <C-k> <Plug>(neocomplcache_snippets_force_expand)
imap <C-l> <Plug>(neocomplcache_snippets_force_jump)
smap <C-l> <Plug>(neocomplcache_snippets_force_jump)

" Enable omni completion.
autocmd FileType css setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
autocmd FileType c setlocal omnifunc=ccomplete#Complete

" SuperTab
"let g:SuperTabDefultCompletionType='context'
let g:SuperTabDefaultCompletionType = '<C-X><C-U>'
let g:SuperTabRetainCompletionType=2

" ctrlp
set wildignore+=*/tmp/*,*.so,*.o,*.a,*.obj,*.swp,*.zip,*.pyc,*.pyo,*.class,.DS_Store  " MacOSX/Linux
let g:ctrlp_custom_ignore = '\.git$\|\.hg$\|\.svn$'

" Keybindings for plugin toggle
nmap <F2> :nohlsearch<cr>
nmap <F5> :TagbarToggle<cr>
nmap <F6> :NERDTreeToggle<cr>
nmap <F4> :IndentGuidesToggle<cr>
nmap  <D-/> :
nnoremap <leader>a :Ack
nnoremap <leader>v V`]

"------------------
" Useful Functions
"------------------
" easier navigation between split windows
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-h> <c-w>h
nnoremap <c-l> <c-w>l

" When editing a file, always jump to the last cursor position
" autocmd BufReadPost *
" if  exists("g:leave_my_cursor_position_alone") \
" 	if line("'\"") > 0 && line ("'\"") <= line("$") \
" 		exe "normal g'\""
" 	endif |
" endif

" w!! to sudo & write a file
cmap w!! w !sudo tee >/dev/null %

" Quickly edit/reload the vimrc file
nmap <silent> <leader>ev :e $MYVIMRC<CR>
nmap <silent> <leader>sv :so $MYVIMRC<CR>

" eggcache vim
nnoremap ; :
:command W w
:command WQ wq
:command Wq wq
:command Q q
:command Qa qa
:command QA qa

" for macvim
if has("gui_running")
	set go=aAce  " remove toolbar
	"set transparency=30
	set guifont=Monaco:h13
	set showtabline=2
	set columns=140
	set lines=40
	noremap <D-M-Left> :tabprevious<cr>
	noremap <D-M-Right> :tabnext<cr>
	map <D-1> 1gt
	map <D-2> 2gt
	map <D-3> 3gt
	map <D-4> 4gt
	map <D-5> 5gt
	map <D-6> 6gt
	map <D-7> 7gt
	map <D-8> 8gt
	map <D-9> 9gt
	map <D-0> :tablast<CR>
endif

" added by tib
" TxtBrowser		  高亮TXT文本文件
au BufRead,BufNewFile *.txt setlocal ft=txt
set nowrapscan				 " 搜索到文件两端时不重新搜索
set writebackup				 " 设置无备份文件
set nobackup
set hidden					 " 允许在有未保存的修改时切换缓冲区
set list					 " 显示Tab符，使用一高亮竖线代替
set listchars=tab:\|\ ,
" Ctrl + H			  将光标移到当前行的行首
imap <c-n> <ESC>I

" Ctrl + J			  将光标移到下一行的行首
imap <c-j> <ESC>jI

" Ctrl + K			  将光标移到上一行的末尾
imap <c-k> <ESC>kA

" Ctrl + L			  将光标移到当前行的行尾
imap <c-l> <ESC>A

" ======= 编译 && 运行 ======= "

" 编译源文件
func! CompileCode()
	exec "w"
	if &filetype == "c"
		exec "!gcc -Wall -std=c99 %<.c -o %<"
	elseif &filetype == "cpp"
		exec "!g++ -Wall -std=c++98 %<.cpp -o %<"
	elseif &filetype == "java"
		exec "!javac %<.java"
	elseif &filetype == "haskell"
		exec "!ghc --make %<.hs -o %<"
	elseif &filetype == "lua"
		exec "!lua %<.lua"
	elseif &filetype == "perl"
		exec "!perl %<.pl"
	elseif &filetype == "python"
		exec "!python %<.py"
	elseif &filetype == "ruby"
		exec "!ruby %<.rb"
	endif
endfunc

" 运行可执行文件
func! RunCode()
	exec "w"
	if &filetype == "c" || &filetype == "cpp" || &filetype == "haskell"
		exec "! ./%<"
	elseif &filetype == "java"
		exec "!java %<"
	elseif &filetype == "lua"
		exec "!lua %<.lua"
	elseif &filetype == "perl"
		exec "!perl %<.pl"
	elseif &filetype == "python"
		exec "!python %<.py"
	elseif &filetype == "ruby"
		exec "!ruby %<.rb"
	endif
endfunc

" Ctrl + C 一键保存、编译
map <c-c> :call CompileCode()<CR>
imap <c-c> <ESC>:call CompileCode()<CR>
vmap <c-c> <ESC>:call CompileCode()<CR>

" Ctrl + R 一键保存、运行
map <c-y> :call RunCode()<CR>
imap <c-y> <ESC>:call RunCode()<CR>
vmap <c-y> <ESC>:call RunCode()<CR>

" added by tib for python support for VIM
let g:pydiction_location = '/Users/tib/.vim/bundle/pydiction/complete-dict'
let g:pydiction_menu_height = 20

"set term=dtterm
"
"

" ####################### added by tib 2014-11-10 ###################################3
" Only do this when not done yet for this buffer
if exists("b:did_ftplugin")
	finish
endif
let b:did_ftplugin = 1

map <buffer> <S-e> :w<CR>:!/usr/bin/env python % <CR>
map <buffer> gd /def <C-R><C-W><CR> 

set foldmethod=expr
set foldexpr=PythonFoldExpr(v:lnum)
set foldtext=PythonFoldText()

map <buffer> f za
map <buffer> F :call ToggleFold()<CR>
let b:folded = 1

function! ToggleFold()
	if( b:folded == 0 )
		exec "normal! zM"
		let b:folded = 1
	else
		exec "normal! zR"
		let b:folded = 0
	endif
endfunction

function! PythonFoldText()

	let size = 1 + v:foldend - v:foldstart
	if size < 10
		let size = " " . size
	endif
	if size < 100
		let size = " " . size
	endif
	if size < 1000
		let size = " " . size
	endif

	if match(getline(v:foldstart), '"""') >= 0
		let text = substitute(getline(v:foldstart), '"""', '', 'g' ) . ' '
	elseif match(getline(v:foldstart), "'''") >= 0
		let text = substitute(getline(v:foldstart), "'''", '', 'g' ) . ' '
	else
		let text = getline(v:foldstart)
	endif

	return size . ' lines:'. text . ' '

endfunction

function! PythonFoldExpr(lnum)

	if indent( nextnonblank(a:lnum) ) == 0
		return 0
	endif

	if getline(a:lnum-1) =~ '^\(class\|def\)\s'
		return 1
	endif

	if getline(a:lnum) =~ '^\s*$'
		return "="
	endif

	if indent(a:lnum) == 0
		return 0
	endif

	return '='

endfunction

" In case folding breaks down
function! ReFold()
	set foldmethod=expr
	set foldexpr=0
	set foldnestmax=1
	set foldmethod=expr
	set foldexpr=PythonFoldExpr(v:lnum)
	set foldtext=PythonFoldText()
	echo
endfunction
"#######################################################################
"
"added 2014-11-10
map <F8> :set expandtab<cr>
map <F9> :%ret!<cr>
map <F10> :set noexpandtab<cr>

map <F7> :set paste<cr>
map <F3> :set nopaste<cr>

if has("autocmd")
	au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

set t_ti= t_te=
