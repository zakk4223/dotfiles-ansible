fzf_select() {
	fzf --sync --query ${1:-" "} --bind 'result:transform:
	  if [[ -n $FZF_QUERY ]]; then
	    echo "track-current+clear-query"
	  else
	    echo "untrack-current+offset-middle+unbind(result)"
	  fi
	'
}
