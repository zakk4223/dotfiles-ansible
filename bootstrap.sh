#!/bin/sh


GIT_URL="https://github.com/zakk4223/dotfiles-ansible.git"

#Archlinux only for now.


sudo pacman -S ansible git


mkdir -p "$HOME/proj"
cd "$HOME/proj"
git clone $GIT_URL
cd dotfiles-ansible/ansible
ansible-galaxy collection install -r requirements.yml
ansible-playbook --ask-become-pass ./dotfiles.yml $@




