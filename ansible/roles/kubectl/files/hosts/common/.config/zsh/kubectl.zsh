kctx() {
	local ctx=$(kubectl config get-contexts -o name | fzf)
	if [[ -n "$ctx" ]]; then
		kubectl config use-context "$ctx"
	fi
}
