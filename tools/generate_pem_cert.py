#!/usr/bin/python
#
# Copyright (c) 2018 Lenovo, Inc.
# All Rights Reserved.
#
# Authors:
#     Yingfu Zhou <zhouyf6@lenovo.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


str1="""

Actually you need to execute below commands manually:
1) openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout server.key
-out server.crt
$ openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out
cert.pem

The sample input looks like:

-------------------------------------------------------------------------------
Generating a 2048 bit RSA private key
......+++
..............................................+++
unable to write 'random state'
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:China
string is too long, it needs to be less than  2 bytes long
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:Beijing
Locality Name (eg, city) []:Beijing
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Lenovo
Organizational Unit Name (eg, section) []:LR
Common Name (e.g. server FQDN or YOUR name) []:10.100.3.183
Email Address []:zhouyf6@lenovo.com
-------------------------------------------------------------------------------

2) cat server.key server.crt > server.pem
3) cp server.pem etc/server.pem
4) then you can use curl cmd:
   #curl --cacert server.pem https://127.0.0.1:9131/
"""

print str1
