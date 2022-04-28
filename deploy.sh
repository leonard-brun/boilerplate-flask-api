#!/bin/bash
COLOR_GREEN="\033[0;32m"
COLOR_RED="\033[0;31m"
COLOR_BLUE="\033[0;34m"
COLOR_PURPLE="\033[0;35m"
COLOR_CYAN="\033[0;36m"
COLOR_RESET="\033[0m"

APP_NAME="api"
GIT_BRANCH=$1

fail() {
    reason=$1
    echo "${COLOR_RED}Error: ${reason}${COLOR_RESET}"
    echo ""
    echo "${COLOR_RED}+ - - - - - - - - - - - +${COLOR_RESET}"
    echo "${COLOR_RED}|  Deployment failed !  |${COLOR_RESET}"
    echo "${COLOR_RED}+ - - - - - - - - - - - +${COLOR_RESET}"
    echo ""
    exit 1
}

success() {
    echo ""
    echo "${COLOR_GREEN}+ - - - - - - - - - - - - - +${COLOR_RESET}"
    echo "${COLOR_GREEN}|  Deployment succeeded !   |${COLOR_RESET}"
    echo "${COLOR_GREEN}+ - - - - - - - - - - - - - +${COLOR_RESET}"
    echo ""
    exit 0
}

echo "${COLOR_PURPLE}             _${COLOR_RESET}"
echo "${COLOR_PURPLE}            (_)${COLOR_RESET}"
echo "${COLOR_PURPLE}  __ _ _ __  _${COLOR_RESET}"
echo "${COLOR_PURPLE} / _\` | '_ \| |${COLOR_RESET}"
echo "${COLOR_PURPLE}| (_| | |_) | |${COLOR_RESET}"
echo "${COLOR_PURPLE} \__,_| .__/|_|${COLOR_RESET}"
echo "${COLOR_PURPLE}      | |${COLOR_RESET}"
echo "${COLOR_PURPLE}      |_|${COLOR_RESET}"

if [ "$GIT_BRANCH" = "" ]
then echo ""; fail "Missing git branch argument."
fi

echo "\n${COLOR_BLUE}- Stopping application...${COLOR_RESET}"
if ! make stop
then fail "Unable to stop application."
fi
echo "${COLOR_GREEN}Application successfully stopped.${COLOR_RESET}"

echo "\n${COLOR_BLUE}- Pulling code...${COLOR_RESET}"
git remote update
if ! git reset --hard origin/${GIT_BRANCH}
then fail "Unable to pull code."
fi
echo "${COLOR_GREEN}Code successfully pulled.${COLOR_RESET}"

# echo "\n${COLOR_BLUE}- Pulling images...${COLOR_RESET}"
# if ! docker-compose -f docker-compose-prod.yml pull
# then fail "Unable to pull images."
# fi
# echo "${COLOR_GREEN}Images successfully pulled.${COLOR_RESET}"

echo "\n${COLOR_BLUE}- Build image...${COLOR_RESET}"
if ! make build
then fail "Unable to build images."
fi
echo "${COLOR_GREEN}Images successfully built.${COLOR_RESET}"

echo "\n${COLOR_BLUE}- Starting application...${COLOR_RESET}"
if ! make prod
then fail "Unable to start application."
fi
echo "${COLOR_GREEN}Application successfully started.${COLOR_RESET}"

echo "\n${COLOR_BLUE}- Running database upgrade...${COLOR_RESET}"
if ! make db_upgrade
then fail "Unable to upgrade database."
fi
echo "${COLOR_GREEN}Database successfully upgraded.${COLOR_RESET}"

success
