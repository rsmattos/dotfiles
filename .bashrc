# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
#*MCTDH*A***********************************************************************
# Following lines written by install_mctdh.  Thu Nov 10 11:05:21 AM CET 2022
export MCTDH_DIR=/home/rafael/Softwares/MCTDH/85.10
. $MCTDH_DIR/install/mctdh.profile
if [ -f ~/.mctdhrc ] && [ -t 0 ] ; then . ~/.mctdhrc ; fi
#*MCTDH*B***********************************************************************
