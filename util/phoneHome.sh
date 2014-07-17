#!/bin/sh

ssh -o "StrictHostKeyChecking no" -i /home/pi/.ssh/id_rsa -N -R 2222:localhost:22 tsuck@tsukolsky.dyndns.org -p 31670 &
