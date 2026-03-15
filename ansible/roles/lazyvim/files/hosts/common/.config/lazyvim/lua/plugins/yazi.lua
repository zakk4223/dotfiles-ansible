return {
	"mikavilpas/yazi.nvim",
	version = "*",
	event = "VeryLazy",
	dependencies = {
		{ "nvim-lua/plenary.nvim", lazy = true},
	},
	opts = {
		open_for_directories = true,

	},

	keys = {
		{
			"<leader>e",
			mode = {"n", "v"},
			"<cmd>Yazi<cr>",
			desc = "Open yazi at the current file",
		},
		{
			"<leader>E",
			mode = {"n", "v"},
			"<cmd>Yazi cwd<cr>",
			desc = "Open yazi in lazyvims working directory",
		}
	},
	init = function()
		vim.g.loaded_netrwPlugin = 1
	end,
}
