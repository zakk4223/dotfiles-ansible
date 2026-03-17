tmx() {
    local session_name=${1:-${PWD:t}}
	  if [ -z "$TMUX" ]; then
		  command tmux new-session -A -s "$session_name"
	  else
		  command tmux new-session -Ad -s "$session_name"; command tmux switch-client -t "$session_name"
    fi
}
