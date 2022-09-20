#!/bin/bash

gh ssh-key add $1 --title $2

rm $1
echo "Successfully added new key with title " $2
