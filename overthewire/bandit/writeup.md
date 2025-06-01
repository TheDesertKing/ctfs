Bandit Writeup:

#Level 0:
They tell us to SSH in... aight!

-solution:
`ssh -p 2220 bandit0@bandit.labs.overthewire.org`


#Level 1:
After logging in, we can locate a file in the current directory.

`ls`
`-`

Okay, now we just have to read this file!
Problem is, `cat -` or `vim -` wouldn't work as '-' is used to add flags to commands in Bash.

A way to specify it's a file is to add a path specifier, like `/../../..` or `./`.

-solution:
`cat ./-`


#Level 2:
Same thing as last level.

`ls`
`spaces in this filename`

Now just gotta escape the spaces so Bash will get that it's the same file.

-solution:
`cat spaces\ in\ this\ filename`


#Level 3:
Okay we have a directory, let's cd into it.

`ls`
`inhere`

`cd inhere`

Oh but it's empty, but is it? let's view all files in the directory with a flag.

`ls -a`
`. .. ...Hiding-From-You`

-solution:
`cat ...Hiding-From-You`


#Level 4:
`cd inhere`

`ls`
`-file00  -file01  -file02  -file03  -file04  -file05  -file06  -file07  -file08  -file09`

Okay many files, let's try and read all of them at once.

`cat ./*`
`�ŉOT���S �plS]-EH�t�:-�Z�
                         N$���'���Se��
                                      \�- V�P�jls�����
                                                      o5e�Mz9�#P�ws������Oh||xt��6|ر��Vܒ��q ��*rMӼ^';b\�
x����]C�
        �H`�/�X��OGLV��*��-o��w9�P�RAz�b��␦[��F���_��+J��2X1�M�O�g��Y����d�Ŧj4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw
t)�r�R�C#�ӧ��4��_�\����^�)C`

Okay that's wierd binary, let's try and see of what type.

`file ./-file00`
`./-file00: PGP Secret Sub-key -`

Interesting. PGP is an encryption tool. Let's see how we can add these files together.

Okay, after a lot of googling and reading about PGP, it seems I've fell for a red herring.
In the files, there is a string of text, searching them one by one shows us one of them is fully textual, and it is the password.

-solution:
`cat ./-file07`


#Level 5:
This is a mess... folders in a structure that will require me to do a lot of manual work. Let's try and seive through.

`cat inhere/*/*`
`*tons of data*`

First, I've tried to filter through file type.
There is one of 'ASCII text, with very long lines' is very common, and due to it's name, I assume the password won't be here.
The file type 'data' is not textual, so let's remove it too.

`file inhere/*/* | grep -Ev 'long|data'
inhere/maybehere00/-file3:       OpenPGP Secret Key
inhere/maybehere01/-file2:       ASCII text
inhere/maybehere05/-file3:       OpenPGP Public Key
inhere/maybehere08/spaces file1: ASCII text
inhere/maybehere12/-file2:       ASCII text
inhere/maybehere14/-file3:       OpenPGP Secret Key
inhere/maybehere15/spaces file2: ASCII text
inhere/maybehere18/-file2:       ASCII text`

That's not too many files, let's go one by one.

Okay, I've tried going one by one, but I feel I can do better than that.
The passwords so far have the same length and consist of [A-Za-z], let's use it.
(Editor's note: I've missed the fact the password contains numbers... makes sense it doesn't work...)

`find inhere/* -type f -print0 | xargs -0 grep -E "[A-Za-z]{33}$"`
``
No help either, I got nothing.
After a rest, I've taken to look at the web page for the challenge, and now I see there are extra details there.

We can filter via one of the 3 parameters, but that's easy, let's do all three in one.
It's scrappy, but it does the work.

-solution:
`find inhere/ -type f | while read -r file; do wc -c "$file"; done | grep 1033 | awk '{print $2}' | xargs file | grep text | awk '{print $1}' | cut -d':' -f1 | xargs cat`


#Level 6:
Find a file in the whole system using some information.
Okay let's read the file manual.
So there are flags for searching for owner user and group, all we have to do is ignore the "permission denied" output, which is classified with code 2 for an error, so we can redirct it to /dev/null to ignore it.
I also added a pipe to xagrs cat to print the file's content.

-solution:
`find / -type f -user bandit7 -group bandit6 2>/dev/null | xargs cat`


#Level 7:
Finding text in a file? easy grep job.
I also added awk, to print the second column, meaning the second substring, when seperating the string by a space.

-solution:
`cat data.txt | grep millionth | awk '{print $2}'`


#Level 8:
Searching for unique text in a file? uniq sounds like the tool.
But at first it didn't work, showed me many duplicate lines.
It turns out you need to sort it before it works correctly.

-solution:
`sort data.txt | uniq -u`


#Level 9:
Human readable? strings is the command.
Also the password is 32 characters lonf, made of lower and upper case letters with numbers.

-solution:
`strings data.txt | grep -E "= [a-zA-Z0-9]{32}" | awk '{print $2}'`


#Level 10:
Decoding base64, good thing there's a command for it.

-solution:
`base64 -d data.txt | awk '{print $4}'`


#Level 11:
Rot 13, huh. I wasn't sure how to do this, but turns out it's quite easy using tr.

-solution:
`cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' | awk '{print $4}'`


#Level 12:
The solution is a long list of gzip -d, tar --extract -f, bzip2 -d9.


#Level 13:
We need to SSH into bandit14, let's use SSH with the -i flag to use the sshkey.private file, as an authentication method, instead of typing the password I don't have yet.

-solution:
`ssh -p 2220 -i sshkey.private bandit14@localhost`
`The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?`
`yes`
`*The Bandit banner*`
`cat /etc/bandit_pass/bandit14`


#Level 14:
Communication on port 30000. nc is a tool that allows us to communicate over a port.

-solution:
`nc localhost 30000`
``
`*Current password*`
`Correct!`


#Level 15:
Honestly, I have no Interest in SSL so I just got it from the interwebs.

-solution:
`openssl s_client -connect localhost:30001 -ign_eof`


#Level 16:
Going off the last challenge, now we have to also scan ports, nmap for the job.

`nmap -p31000-32000 localhost`
`Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-05-24 19:29 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0016s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.21 seconds`

From here we've got a few ports, let's manually go one by one and try and see which answers to our TLS/SSL call.

`openssl s_client -connect localhost:31046 -ign_eof`
`CONNECTED(00000003)
4087F0F7FF7F0000:error:0A0000F4:SSL routines:ossl_statem_client_read_transition:unexpected message:../ssl/statem/statem_clnt.c:398:
---
no peer certificate available
---
No client certificate CA names sent
---
SSL handshake has read 293 bytes and written 300 bytes
Verification: OK
---
New, (NONE), Cipher is (NONE)
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 0 (ok)
---`

Wrong answer, let's if one of them does allow us to pass the password.

-solution:
`openssl s_client -connect localhost:31790 -ign_eof`
`*Bunch of TLS data...*
read R BLOCK`
`*Current password*`
`Correct!
*RSA key*
closed`

That's not the password, but maybe we can use it to connect to the next level.

`ssh -p 2220 -i /tmp/amit bandit17@localhost`
`The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?`
`yes`
`*...*
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for '/tmp/amit' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/tmp/amit": bad permissions
bandit17@localhost: Permission denied (publickey).`

It seems to still have an issue... Oh the permissions? The key should be private? Okay, let's make it all mine, by allowing only my user to RW.

`chmod 600 /tmp/amit`

Now the SSH with the key works.


#Level 17:
I've actually just done this at my day-job, comparing files using grep with switches.

F: Interpret input as strings, not regex
x: Full line comparison
v: Reverse the selection, find only lines that don't exist in the input file
f: Get the input from a file

-solution:
`grep -Fxvf passwords.old passwords.new`


#Level 18:
Executing commands using ssh, let's see.
Putting the command at the end seems to do it.

`ssh -p 2220 bandit18@bandit.labs.overthewire.org "ls -la"`
`total 24
drwxr-xr-x  2 root     root     4096 Apr 10 14:23 .
drwxr-xr-x 70 root     root     4096 Apr 10 14:24 ..
-rw-r--r--  1 root     root      220 Mar 31  2024 .bash_logout
-rw-r-----  1 bandit19 bandit18 3794 Apr 10 14:23 .bashrc
-rw-r--r--  1 root     root      807 Mar 31  2024 .profile
-rw-r-----  1 bandit19 bandit18   33 Apr 10 14:23 readme`

-solution:
`ssh -p 2220 bandit18@bandit.labs.overthewire.org "cat readme"`


#Level 19:
SetUID binaries, a cool concept where you can get perms of another user/group.
This binary might allow us to do stuff as bandit20.

-solution:
`./bandit20-do cat /etc/bandit_pass/bandit20`


#Level 20:
So we need to connect into a port and print the password from that port.
A reverse netcat would do the trick.

I opened a new terminal and connected to bandit19, then used nc to listen on port 4567.

`nc -lvp 4567`
`Listening on 0.0.0.0 4567`

Then on the other terminal used the suconnect binary to connect to it.

`./suconnect 4567`

Lastly, I pasted the current password to the terminal listening.

`*Current password*`


#Level 21:
So we need to read the cron.d to see the programs being ran automatically.

`ls /etc/cron.d`
`clean_tmp  cronjob_bandit22  cronjob_bandit23  cronjob_bandit24  e2scrub_all  otw-tmp-dir  sysstat`

Let's take a look at cronjob_bandit22.

`cat /etc/cron.d/cronjob_bandit22`
`* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null`

Let's see if we can read this file.

`ls /usr/bin/cronjob_* -la`
`-rwxr-x--- 1 bandit22 bandit21 130 Apr 10 14:23 /usr/bin/cronjob_bandit22.sh
-rwxr-x--- 1 bandit23 bandit22 211 Apr 10 14:23 /usr/bin/cronjob_bandit23.sh
-rwxr-x--- 1 bandit24 bandit23 384 Apr 10 14:23 /usr/bin/cronjob_bandit24.sh`

It seems that for this and the next two challenges, we can read and execute the file that is being cron'd, this is because the owner group for each file is the bandit user that is a level before itself, and there are read rights for groups for the three files.

Let's read our current challenge's file.

`cat /usr/bin/cronjob_bandit22.sh`
`#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`

It's a small Bash script that gives permissions to a certain file in the /tmp directory, allowing everyone to read it.
Then the content of the file /etc/bandit_pass_bandit22 is pushed to it, overwriting the file's content.
The data pushed is the password for this level, so we just need to run it, then read the relevant file.

-solution:
`/usr/bin/cronjob_bandit22.sh`
``
`cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`


#Level 22:
As I found out on the last level, there is a file we can read and execute relating to this level.

`cat /usr/bin/cronjob_bandit23.sh`
`#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget`

This Bash script that takes the user's name along side some extra text:
I am user Bandit22
Then gets the MD5 hash created by that string (and also parses our extra text from the md5sum command).
Lastly, it copies the password for this level to a file in the /tmp directory, with the name being the MD5 hash.

So all we need to do is run the script, and it would let us know the location of the file.
Seems too easy but let's try.

`/usr/bin/cronjob_bandit23.sh`
`Copying passwordfile /etc/bandit_pass/bandit22 to /tmp/8169b67bd894ddbb4412f91573b38db3`
`cat /tmp/8169b67bd894ddbb4412f91573b38db3`
`*Level 22's password*`

Now it makes sense, if I run this script as bandit22, it would copy the current user's password, it being bandit22, so we need it to run as bandit23.
This is a file being run using cron, so it might be ran by bandit23, let's check.

`cat /etc/cron.d/cronjob_bandit23`
`@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null`

Good, it is being ran by bandit23, so all we have to do is figure out the MD5 hash created from the message "I am user bandit23", and we should find this level's password in it.

-solution:
`echo "I am user bandit23" | md5sum | cut -d ' ' -f1`
`8ca319486bfbbc3663ea0fbe81326349`
`cat /tmp/8ca319486bfbbc3663ea0fbe81326349`


#Level 24:
As with the past 2 levels, we have a file being ran by cron relating to this challenge, so let's read it.

`cat /usr/bin/cronjob_bandit24.sh`
`#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done`

So we are ramping up, I like it.
This script goes into a directory depending on the user running it, looping over all files and if their owner is specifically bandit23, it runs it with a timeout of 60 seconds before it kills the proccess.

So I, logged into bandit23, need to create a script, that will be executed as bandit24.
Let's create an automation that copies this level's password to a file in the /tmp directory.

`#!/bin/bash
cp /etc/bandit_pass/bandit24 /tmp/bandit24amit`

But how would it run? and as bandit24?
Looking at the cron job for this file, we see bandit24 is the user that runs it, and it runs every minute, as indicated by five *.

`cat /etc/cron.d/cronjob_bandit24`
`@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null`

After we created the automation, we just have to wait to the next server rounded mintue.
We can watch it's status of creation using the "watch" command.

`ls -la /tmp/bandit24amit`

Weird, this didn't work. Maybe bandit24 lacks the permissions to run the automation, let's make sure he can.

`chmod 777 /var/spool/bandit24/foo/amit`

Okay, we got something!
The "No such file or directory" error changed to "Permission denied".
That's because the file is being created by bandit24, so as bandit23 I couldn't read it, let's add the following line to our script (which has been deleted, but I used vim with ctrl+z to have it's content in my vim's bufffer)

`chmod 777 /tmp/amit`

Boom, with all the pieces in place, we can cat out the password.

`cat /tmp/amit`


#Level 25:
Interesting, we need to create a script to brute force the password.
I see pwntools is available for python, this is great, let's create a python file using pwntools.

`from pwn import *

code = 0
c = remote('localhost',30002)

while code < 10000:
    if code < 10:
        formatted_code = f"000{str(code)}"
    elif code < 100:
        formatted_code = f"00{str(code)}"
    elif code < 1000:
        formatted_code = f"0{str(code)}"
    else:
        formatted_code = f"{str(code)}"
    print(f"fcode:{formatted_code}")

    c.sendline(f"gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 {formatted_code}")
    resp = c.recvuntil("Wrong!",timeout=10)
    print(f"Response: {resp.decode(errors='ignore')}")
    code += 1`

Now let's run it.

`python3 /tmp/bandit24.py`
`*...*
Response:  Please enter the correct current password and pincode. Try again.
Wrong!
fcode:2217
Response:  Please enter the correct current password and pincode. Try again.
Wrong!
fcode:2218
Response:  Please enter the correct current password and pincode. Try again.
Wrong!
fcode:2219
Traceback (most recent call last):
  File "/tmp/bandit24.py", line 18, in <module>
    resp = c.recvuntil("Wrong!",timeout=10)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/pwnlib/tubes/tube.py", line 341, in recvuntil
    res = self.recv(timeout=self.timeout)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/pwnlib/tubes/tube.py", line 106, in recv
    return self._recv(numb, timeout) or b''
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/pwnlib/tubes/tube.py", line 176, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
                               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/pwnlib/tubes/tube.py", line 155, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/pwnlib/tubes/sock.py", line 56, in recv_raw
    raise EOFError
EOFError
[*] Closed connection to localhost port 30002`

So it broke right after inserting 2219, let's manually try it.

`nc localhost 30002`
`I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
*Current password* 2219
Correct!`


#Level 26:
Interesting, talking about a different default shell.
Trying to SSH using the key we've gotten is useless, as we are immideately logged out.
It turns out that we can see the default shell in the /etc/passwd file.

`cat /etc/passwd | grep bandit26`
`bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext`

It looks like bandit26 can execute it, just making sure.

`ls /usr/bin/showtext -la`
`-rwxr-xr-x 1 root root 58 Apr 10 14:23 /usr/bin/showtext`

Let's see what that script does.

`cat /usr/bin/showtext`
`#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0`

So it reads the text.txt file that inside the bandit26 home directory. Let's take a look at that file.

`ls /home/bandit26/text.txt -la`
`-rw-r----- 1 bandit26 bandit26 258 Apr 10 14:23 /home/bandit26/text.txt`

Can't read it.

So I was a bit stumped by this level, didn't know where more to look. Funny enough it was the 'more' command I needed to better understand.
More will either print out the whole file, or go into interactive mode, depending on the full file's content can be pasted onto one screen.
So by chaning the terminal's size would allow us to go into interactive mode.
From there, we can press 'v' to into vim, and then gain Bash access.

`:set shell=/bin/bash`
`:sh`

-solution:
`cat /etc/bandit_pass/bandit26`



#Level 27:
A repeat of challenge 19.

-solution:
`./bandit27-do cat /etc/bandit_pass/bandit27`


#Level 28:
Git based challenge, yay!
I've never cloned a repo via SSH, so I had to read the manual.

`ssh://[user@]host.xz[:port]/~[user]/path/to/repo.git/`

Using this structure, we can safely git clone into a directory we can write to - /tmp.

`git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo /tmp/amitus`
`Cloning into '/tmp/amitus'...
*SSH fingerprint message*`
`yes`
`*Bandit banner*
bandit27-git@localhost's password:`
`*Current level's password*`
`remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.`

Then we can see what's inside the repo, oh and hey look, a readme file.

-solution:
`cat /tmp/amitus/README`


#Level 28
Again git repo, let's clone it and see what's up.

`git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo /tmp/amitus2`
`Cloning into '/tmp/amitus'...
*SSH fingerprint message*`
`yes`
`*Bandit banner*
bandit28-git@localhost's password:`
`*Current level's password*`
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), 798 bytes | 798.00 KiB/s, done.
Resolving deltas: 100% (2/2), done.`

Reading the readme file this time shows the password is X'd out.
Git is a version control system, so maybe the password was saved previously?

`cd /tmp/amitus2
git log`
`git log
commit 674690a00a0056ab96048f7317b9ec20c057c06b (HEAD -> master, origin/master, origin/HEAD)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    fix info leak

commit fb0df1358b1ff146f581651a84bae622353a71c0
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    add missing data

commit a5fdc97aae2c6f0e6c1e722877a100f24bcaaa46
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    initial commit of README.md`

From this log, it's clear that the data was removed in the latest commit, so we just have to go back one.

-solution:
`git checkout HEAD^
cat README.md`


#Level 29:
Another git, *shit, here we go again*.

After seeing the data we want isn't in the current branch, not even in the first commit, let's check out the other branches.

`git branche -a`
`* (HEAD detached at 8d2ffeb)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev`

Going one by one, we can see it in dev.

-solution:
`git checkout dev
cat README.md`


#Level 30:
Another git, let's clone.

After not figuring this out, I've went to check the solution online.
Turns out there are this things called git tags and they hide information in them? It's a cool mechanism of signing and stuff, but why would it hold data? Honestly, this feels very niche and useless to me.
Nonetheless, let's continue.

-solution:
`git show secret`



#Level 31:
More git huh? I'll give it a go, but probably read a writeup, as there is no productive way to figure these challenges out without going on 10 trails of learning niche and useless things...

Turns out I was just whining. It's a simple challnge topush a file to the remote branch.
To start it, let's create the file with the relevant content.

`echo "May I come in?" > key.txt`

We need to push to branch 'master', which we are already on, as we can see here.

`git branch`
`* master`

So all we have to do now is to commit the changes and push it to the remote repo.

`git add .`

Adding the file to staging.

`git commit -m "pushin!"`
`Your branch is up to date with 'origin/master'. create mode 100644 key.txt`

Commiting the change in staging.

`git push`
`On branch master
Your branch is up to date with 'origin/master'.`

Mmm, up to date? But I've just commited changes.
Let's see if there is a reason my changes were ignored.

`ls -la`
`total 9996
drwxrwxr-x   3 bandit31 bandit31     4096 May 31 14:26 .
drwxrwx-wt 105 root     root     10211328 May 31 14:27 ..
drwxrwxr-x   8 bandit31 bandit31     4096 May 31 14:26 .git
-rw-rw-r--   1 bandit31 bandit31        6 May 31 14:26 .gitignore
-rw-rw-r--   1 bandit31 bandit31       15 May 31 14:26 key.txt
-rw-rw-r--   1 bandit31 bandit31      147 May 31 14:26 README.md`

Ah! a .gitignore file. This file selects what files should be ignored by git.

`cat .gitignore`
`*.txt`

Yep, this affects our key.txt file. Let's remove this .gitignore file.

`rm .gitignore`

And do the commiting process again.

`git add .`

`git commit -m "pushin!"
`[master af07c56] pushin!
 2 files changed, 1 insertion(+), 1 deletion(-)
 delete mode 100644 .gitignore
On branch master`

-solution:

`git push`
`*SSH fingerprint message*`
`yes`
`*Bandit banner*
bandit31-git@localhost's password:`
`*Current Level's password*`


#Level 32:
Wierd shell challnge, I feel equiped from the other challenge that had a wierd shell.

I've logged in as bandit 31 again, to check the shell file for the bandit32 user.

`cat /etc/passwd | grep bandit32`
`bandit32:x:11032:11032:bandit level 32:/home/bandit32:/home/bandit32/uppershell`

The shell file is at /home/bandit32, named 'uppershell'. Let's see what we can do with it.

`ls -la /home/bandit32`
`total 36
drwxr-xr-x  2 root     root      4096 Apr 10 14:23 .
drwxr-xr-x 70 root     root      4096 Apr 10 14:24 ..
-rw-r--r--  1 root     root       220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root     root      3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root     root       807 Mar 31  2024 .profile
-rwsr-x---  1 bandit33 bandit32 15140 Apr 10 14:23 uppershell`

So as bandit31, not being part of the bandit32 group or the bandit33 user, cannot do anything with this file, not even read it.

Okay, so we need to go into this blind.
Let's give it a go.

After trying some stuff and googling, I opened the writeup.
It seems that '$0' evaluates to the current shell's name, so simply calling it, would create a new shell instance.

-solution:
`$0`
`$ `
`whoami`
`bandit33`
`cat /etc/bandit_pass/bandit33`


That's it! finished Bandit!
I had to use writeups quite a lot, but this are some niche topics that there are no other means of learning, but just randomlly coming across, so I give myself the pass.
My attempt is to learn, I've yet to get the tools required to get the answers on my own, so it's okay for me to learn now!


