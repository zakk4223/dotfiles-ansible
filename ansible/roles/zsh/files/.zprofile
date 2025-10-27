export PATH=$PATH:~/bin:~/.local/bin:~/.cargo/bin


alias ls="ls --color=auto"
alias mtc="f(){ docker run -it --rm -v "$(pwd)":/mister misterkun/toolchain "$@"; unset -f f; }; f"
alias vim="lazyvim"
alias vi="lazyvim"


export EDITOR=lazyvim
export VISUAL=lazyvim

export QSYS_ROOTDIR="/home/zakk/intelFPGA_lite/22.1std/quartus/sopc_builder/bin"
export FREETYPE_PROPERTIES="cff:no-stem-darkening=0 autofitter:no-stem-darkening=0"
#export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json:/usr/share/vulkan/icd.d/radeon_icd.i686.json
