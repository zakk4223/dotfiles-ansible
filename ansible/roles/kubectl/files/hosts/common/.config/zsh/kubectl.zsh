kctx() {
	local current_ctx=$(kubectl config current-context)
	local ctx=$(kubectl config get-contexts -o name | fzf_select $current_ctx)
	if [[ -n "$ctx" ]]; then
		kubectl config use-context "$ctx"
	fi
}
