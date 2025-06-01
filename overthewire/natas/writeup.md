#Level 0:
Web exploitation, it's been a moment for me.
Let's dive in!

###Chellenge Prompt:
You can find the password for the next level on this page.

Looking at the first page, I opened devtools (F12) and looked around. 

Under the line of "You can find the password for the next level on this page.You can find the password for the next level on this page.", I've found this HTML comment:

`<!--The password for natas1 is 0nzCigAq7t2iALyvU9xcHlYN4MlkIwlq -->`


#Level 1:
###Chellenge Prompt:
You can find the password for the next level on this page, but rightclicking has been blocked!

Right clicking has been blocked, good thing we don't need it.
Dev tools again would allow us to see the password:

`<!--The password for natas2 is TguMNxKo1DSa1tujBLuZJnDUlCcUAPlI -->`


#Level 2:
###Chellenge Prompt:
There is nothing on this page

Let's see if there truly is nothing on this page.

It seems there is an <img> tag, with a link to 'files/pixel.png', let's see what that file contains.
After seeing it's simply an image of a single pixel, I've downloaded the file and tried reading it, only to see it is a simple png, nothing hidden.

The png file is inside the 'files' folder, let's see if we can see what's in it:

`http://natas2.natas.labs.overthewire.org/files/`

It seems we can view the directory, and in it there's a text file users.txt containing the natas3 password.

natas3:3gqisGdR0pjm6tpkDKdIWO2hSvchLeYH


#Level 3:
###Chellenge Prompt:
There is nothing on this page

Looking at the page's HTML code, we can see a comment:

`<!-- No more information leaks!! Not even Google will find it this time... -->`

I think this is hinting at 'google dorking', a use of google searches with arguments to view content that would be otherwise hard to find.

`site:*.natas.labs.overthewire.org`

This seems to give us nothing. Oh well.
Reading the comment, "NOT even google will find this", I can assume that google crawling was disabled, and the most common way to do so is with robots.txt, a file that lists endpoints that crawlers are not allowed to crawl.

`http://natas3.natas.labs.overthewire.org/robots.txt`

There's an interesting endpoint listing:
`Disallow: /s3cr3t/`

`http://natas3.natas.labs.overthewire.org/s3cr3t/`

Inside this endpoint we see a users.txt file, in which the password for natas4 resides:

natas4:QryZXc2e0zahULdHrtHxzyYkj59kUxLQ


#Level 4:
###Chellenge Prompt:
Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"

Taking a look at the prompt, it seems to refer to where we came from, "" being the root of the website "/". This is tracked in HTTP via the "refferer" header. Let's add it to our call and try again.

I've tried doing stuff with curl, but that felt less intiutive than I can make it.
So I've set up Burp Suite Community, alongisde FoxyProxy on Chrome, to intercept the HTTP/S calls.
Let's change the 'Referrer' header to be exatctly the text specified in the prompt.

Access granted. The password for natas5 is 0n35PkggAPm2zbEpOU802c0x0Msn1ToK


#Level 5:
###Chellenge Prompt:
Access disallowed. You are not logged in

Interesting. Given the fact that the login form is successfully out of the screen, and I don't get a 401 error, I can say I am logged in as natas5.
So what's up?

Taking a look at the HTTPS request using Burp, it seems there is a cookie named 'loggedin', that is set to '0'.

`Cookie: loggedin=0`

Let's change that to 1.

Access granted. The password for natas6 is 0RoJwHdSKWFTYR5WuiAewauSuNaBXned


#Level 6:
###Chellenge Prompt:
Input secret: *Input Field*
*Submit Button*
*View sourcecode link* 

Clicking the 'View sourcecode' button leads us to '/index-source.html', which shows the source code for the button.
It seems to be PHP code by the '<?' and '?>' opening and closing tags.

'array_key_exists' is a function that checks if a given key or index exists in an array:
`array_key_exists(key,array): bool`

It looks to check if the string 'submit' exists within the POST parameters.
Then the script checks the POST parameter 'secret' to be equal to the variable '$secret', which is probably imported from 'includes/secret.inc'.

If both conditions are met, we get the password for natas7.

as the button is coded within it's HTML with type="submit", the POST request will send this as a parameter.
Adding a secret field is simple, but how can I get the value for the '$secret' variable?
Let's see if we can view the 'includes/secret.inc' file.

`http://natas6.natas.labs.overthewire.org/includes/secret.inc`

This shows us the variable decleration for '$secret'.

$secret = "FOEIUWGHFEEUHOFUOIU";

Let's paste this into the input field and press 'submit'.

Access granted. The password for natas7 is bmg8SvU1LizuWjx3y7xkNERkHxGre0GS


#Level 7:
###Chellenge Prompt:
*Home link* *About link*

Let's see what's on these pages.
When clicking on the home link, we are brought to '/index.php?page=home', using a query string, instead of an actual path.
Within a comment in said page, we see:

`<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->`

Same hint exists within the 'about' page as well.

`http://natas7.natas.labs.overthewire.org/etc/natas_webpass/natas8`

This page gives us an error 'Not Found'.
Maybe we need to use the query string for the 'page' variable?

`http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8`

xcoXLmzMkoIP9D7hlgPlh9XD7OgLAe5Qo

#Level 8:
###Chellenge Prompt:
Input secret: *Input Field*
*Submit Button*
*View sourcecode link* 

Okay, let's see the sourcecode again.

The checking mechanism is the same, except the secret we insert is going through a process of data manipulation, and only then is checked against the secret.
The secret we need to match is given to us at the head of the code, and the data manipulation process as well.
It seems every part of the data manipulation is symmetric, meaning that we can reverse it by understanding what it does, and doing the reversing operation.
So let's break each down:

base64_encode(strings $str): string - encodes the string into base64.

strrev(string $str): string - reverses the string.

bin2hex(string $str): string - Converts binary data contained within a string into hexadecimal. This is intersting, it seems to take binary data as a string, which is the way it's done within PHP. *Today I learned*.

So the process we need to do, in order, is:
Covnert the secret given to bianry format.
Reverse the string.
Base64 decode the string.

That should bring us the input we need to insert.
Using an online PHP sandbox, just to make sure I reverse it with the least chance for stuff to be different than intended, I've used the following code:

`PHP
$p = '3d3d516343746d4d6d6c315669563362';
$b = base64_decode(strrev(hex2bin($p)));
echo $b;
`

This brought me 'oubWYf2kBq'.
When I submit it, we get the password:

Access granted. The password for natas9 is ZE1ck82lmdGIoErlhQgWND6j2Wzz6b6t


#Level 8:
###Chellenge Prompt:
Find words containing: *Input Field* *Search Button*

Output:
*View sourcecode link*

Taking a look at the code, it checks if the string 'needle' exists within the $_REQUEST array.
The $_REQUEST array contains the contents of $_GET $_POST and $_COOKIE, so we can insert 'needle' into any of this to trigger the first 'if' clause.
It will then search the file dictionary.txt for whatever was the value of the param 'needle'.

Let's try testing the form.

`GET /index.php?needle=a&submit=Search HTTP/1.1`

My input is being inserted into the 'needle' request parameter, which should be included inside $_REQUEST.

Inserting 'a', gave us tons of words. dictionary.txt might actually be all the english words. What are we to find in it?
Maybe we aren't to search in it, but rather to manipulate the 'passthru' call in order to do more than the intended 'grep'.

Inserting the input 'a a; ls -la', gives us the following output:

`-rw-r----- 1 natas9 natas9 460878 Apr 10 14:18 dictionary.txt`

The first two a's are for completing the 'grep' command, searching 'a' inside the file 'a', which doesn't exist, i presume, then the ';' to indicate I am trying to run a new command, then 'ls -la' to test if we can run commands after the first.
We indeed can. This gives us command execution for the server.

From the Bandit challegnes, we've learned there is a *challenge_name*_pass folder inside of '/etc', containing all the passwords for the users.
It seems the permissions for that folder is none:

`d---------   2 root root       4096 Apr 10 14:18 natas_pass`

Oh well, where else the password can be?

It turns out I made a big goof, when inserting 'a a; ls -la', it became: 'grep -i *a a; ls -a*dictionary.txt', which made the 'ls' ignore the flags.
When I insert 'a a;ls -la; echo ', it becomes: 'grep -i *a a; ls -la; echo *dictionary.txt', which allows the '-la' part of the 'ls' to run successfully.
This allows me to see some hidden files I've missed in the directory:

`-rw-r-----  1 natas9 natas9    117 Apr 10 14:18 .htaccess
-rw-r-----  1 natas9 natas9     45 Apr 10 14:18 .htpasswd
-rw-r-----  1 natas9 natas9 460878 Apr 10 14:18 dictionary.txt
-rw-r--r--  1 root   root     2924 Apr 10 14:18 index-source.html
-rw-r-----  1 natas9 natas9   1185 Apr 10 14:18 index.php`

Using 'a a; sudo -l 2>&1; echo ' gave me the following error:

`sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`

I've tried looking around but to no avail, even with redirecting the stderr to stdout to see the errors of commands, seems like this will take a lot more to escalate then I believe is intended in a web exploitation focused CTF.
Let's check the writeup.

Of coures, I've gone for '/etc/natas_pass', where there is another folder, '/etc/natas_webpass'.
Let's see if we can read it.

`a a; ls -la /etc/natas_webpass/natas10;`
`-r--r-----   1 natas10 natas9     33 Apr 10 14:18 natas10`

Looks like we can. Here is our password.

`a a; cat /etc/natas_webpass/natas10;`
t7I5VHvpa14sJTUGV0cbEsbYfFP2dmOu



#Level 10:
###Chellenge Prompt:
For security reasons, we now filter on certain characters

Find words containing: *Input Field* *Search Button*


Output:
Input contains an illegal character!
*View sourcecode link*

Okay, let's test which characters are filtered.

';' and '&' are filtered.

I can't seem to be able to use the 'urldecode' PHP function to insert ';' where needed to reproduce the last exploit.
I've gone to the writeups and the first line ends with "... let's use the grep command.".

Using a regex to look for any english character (as -i is on, for case insensitivity) to look in the password file.

`[a-z] /etc/natas_webpass/natas11`
`/etc/natas_webpass/natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk`

