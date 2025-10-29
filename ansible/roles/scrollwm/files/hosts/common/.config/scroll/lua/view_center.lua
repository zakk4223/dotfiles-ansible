local args, state = ...

local scroll = require("scroll")

local width = tonumber(args[1])
if not width then
  width = 0.5
end

local function on_focus(view, _)
  local workspace = scroll.focused_workspace()
  local container = scroll.view_get_container(view)
  local parent = scroll.container_get_parent(container)
  if parent then
    container = parent
  end
  if scroll.container_get_width_fraction(container) <= width then
    scroll.workspace_set_mode(workspace, { center_horizontal = false })
  else
    scroll.workspace_set_mode(workspace, { center_horizontal = true })
  end
end

scroll.add_callback("view_focus", on_focus, nil)
