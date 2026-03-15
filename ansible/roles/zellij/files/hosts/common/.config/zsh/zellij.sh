ze() {
	if [ -z "$ZELLIJ" ]; then
    local session_name=${1:-${PWD:t}}
    command zellij attach "$session_name" || command zellij -s "$session_name"
  else 
		command zellij --session "$ZELLIJ_SESSION_NAME" action new-tab
  fi
}
