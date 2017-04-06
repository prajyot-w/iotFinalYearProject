#!/bin/bash

export http_proxy='http://172.16.0.2:3128/';
export https_proxy='http://172.16.0.2:3128/';
export ftp_proxy='http://172.16.0.2:3128/';

cd /
python /execute.py 