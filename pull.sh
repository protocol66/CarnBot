#!/usr/bin/expect -f
spawn git pull
expect "name"
send "jjsuperpower\r"

expect "ass"
send "e1ebb62626a1425216db8f8f7a2fdface50c9853\r"
interact
