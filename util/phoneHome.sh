#!/bin/sh

ssh -N -R 2222:localhost:22 tsuck@tsukolsky.dyndns.org -p 31670 &
