#!/bin/bash

# Kill any process using port 5000 (commonly used for network servers)
# Usage: ./network_server_kill.sh

lsof -ti tcp:5000 | xargs kill
