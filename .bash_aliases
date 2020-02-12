alias l='ls -lh'
alias la='ls -lah'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles.git/ --work-tree=$HOME'

source /home/rafael/.bash_secrets

function set_environment
{
    while [[ "$#" -gt 0 ]]
    do
        case $1 in
            -h|--help)
                echo "Program usage:"
                echo "set_environment -p [PROGRAM]"
                echo "set_environment -s or --scripts"
                echo ""
                echo "List of supported programs keywords"
                echo "gromos"
                echo "gaussian"
                echo "orca"
                echo "vmd"
                echo "theodore"
                echo "jmol"
                ;;
            -s|--scripts)
                PATH=$PATH:/home/rafael/.compchem_scripts
                ;;
	    -p|--program)
                case $2 in
		    gromos)
	                export PATH=$PATH:/home/rafael/Programs/gromos/gromospp/bin
                        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/rafael/Programs/gromos/gromospp/lib
		        ;;
	            gaussian)
	                PATH=$PATH:/home/rafael/Programs/gaussian/g09
		        export g09root=/home/rafael/Programs/gaussian
		        source $g09root/g09/bsd/g09.profile
		        ;;
		    orca)
                        # OPENMPI
                        export PATH=/home/rafael/Programs/openmpi/3.1.4/bin:$PATH
                        export LD_LIBRARY_PATH=/home/rafael/Programs/openmpi/3.1.4/lib:$LD_LIBRARY_PATH

		        # ORCA
		        export PATH=/home/rafael/Programs/orca/4.2.1:$PATH
                        export LD_LIBRARY_PATH=/home/rafael/Programs/orca/4.2.1:$LD_LIBRARY_PATH

		        alias orca='/home/rafael/Programs/orca/4.2.1/orca'
                        ;;
                    vmd)
                        export PATH=$PATH:/home/rafael/Programs/vmd/bin
                        ;;
                    theodore)
                        export THEODIR=/home/rafael/Programs/theodore
                        export PATH=$THEODIR/bin:$PATH
                        export PYTHONPATH=$THEODIR:$PYTHONPATH
                        ;;
                    jmol)
                        alias jmol='/home/rafael/Programs/jmol/jmol.sh'
                        ;;
                    *)
                        echo "No program mmaches the pattern $2"
                        echo "Look the list of available programs with set_environment -h"
	      esac
	      ;;
	esac
	shift
    done
}

