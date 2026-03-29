


zmodload zsh/complist
autoload -U compinit && compinit
autoload -U colors && colors
autoload -U history-search-end

source /usr/share/zsh/plugins/fzf-tab-git/fzf-tab.plugin.zsh

zle -N history-beginning-search-backward-end history-search-end
zle -N history-beginning-search-forward-end history-search-end

bindkey -v

setopt menucomplete 



setopt append_history inc_append_history share_history
setopt auto_param_slash
setopt interactive_comments
stty stop undef


autoload -U promptinit && promptinit
prompt pure

HISTSIZE=1000000
SAVEHIST=1000000
HISTFILE="$XDG_CACHE_HOME/zsh_history"
HISTCONTROL=ignoreboth

source <(fzf --zsh)

alias ls="ls --color=auto"
alias grep="grep --color=auto"
alias mkdir="mkdir -pv"

# disable sort when completing `git checkout`
zstyle ':completion:*:git-checkout:*' sort false
# set descriptions format to enable group support
# NOTE: don't use escape sequences (like '%F{red}%d%f') here, fzf-tab will ignore them
zstyle ':completion:*:descriptions' format '[%d]'
# set list-colors to enable filename colorizing
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# force zsh not to show completion menu, which allows fzf-tab to capture the unambiguous prefix
zstyle ':completion:*' menu no
# preview directory's content with eza when completing cd
# zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
# custom fzf flags
# NOTE: fzf-tab does not follow FZF_DEFAULT_OPTS by default
zstyle ':fzf-tab:*' fzf-flags --color=fg:1,fg+:2 --bind=tab:accept
# To make fzf-tab follow FZF_DEFAULT_OPTS.
# NOTE: This may lead to unexpected behavior since some flags break this plugin. See Aloxaf/fzf-tab#455.
zstyle ':fzf-tab:*' use-fzf-default-opts yes
# switch group using `<` and `>`
zstyle ':fzf-tab:*' switch-group '<' '>'


source ~/.zsh/catppuccin_mocha-zsh-syntax-highlighting.zsh

for config_file in ~/.config/shell_aliases/*(N); do
	[ -f "$config_file" ] && source "$config_file"
done

for config_file in ~/.config/zsh/*(N); do
	[ -f "$config_file" ] && source "$config_file"
done

vim() {
	if command -v lazyvim >/dev/null 2>&1; then
		lazyvim "$@"
	elif command -v nvim >/dev/null 2>&1; then
		nvim "$@"
	elif command -v vim >/dev/null 2>&1; then
		command vim "$@"
	else 
		vi "$@"
	fi
}

vi() {
	if command -v lazyvim >/dev/null 2>&1; then
		lazyvim "$@"
	elif command -v nvim >/dev/null 2>&1; then
		nvim "$@"
	elif command -v vim >/dev/null 2>&1; then
		vim "$@"
	else
		command vi "$@"
	fi
}

if command -v zoxide &> /dev/null; then
	eval "$(zoxide init zsh --cmd cd)"
fi


bindkey "^a" beginning-of-line
bindkey "^e" end-of-line

bindkey "^[[A" history-beginning-search-backward-end
bindkey "^[[B" history-beginning-search-forward-end
