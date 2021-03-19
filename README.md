# lucidworks-fusion-config
Lucidworks Fusion configuration as code utility

## Introduction
Configuration as code is a standard practice in software development 
circles nowadays, and the configuration of Lucidworks Fusion is no
exception.  This utility facilitates segmentation of a Lucidworks
Fusion app into its component objects to facilitate change tracking
in version control.

## System requirements
* Bash
* Python 3
* Lucidworks Fusion 4+

This software has been used with Lucidworks Fusion 4.1.0 and 4.2.6.
Please let me know if you use it with another version of Fusion.

## Getting started
Assuming you're using git, create a new repo for storing your
application(s):

```bash
mkdir my_app
cd my_app
git init
```

Then in that repo, create a clusters.ini file which names
each cluster and sets any variables you'll want to replace.

N.B. when a config is downloaded from a source, variables 
in these definitions will be substituted for the values
found within those variables, so short variables like the
number of clusters aren't suitable.

```
[prod]
fusion=http://fusion.example.com/
myvar=The quick brown fox jumps over the lazy dog.

[local]
fusion=http://localhost:8764
myvar=The five boxing wizards jump quickly.
```

Assuming you have a fusion application already set up,
download it:

```bash
/path/to/config get prod my_app
```

this will create the directory apps/my_app in your project. The "apps" 
directory is to support multiple applications, and it is important
to the script to identify where to find its clusters.ini.  Don't mess
with it.

Inside the apps/my_app directory, you will find index.json, which 
retains the order of the objects that were included in the download,
and an exploded_objects folder which contains a folder for every 
type of object downloaded, and each of those folders contains
a file for each object.

Make any changes, keeping index.json consistent with the files,
commit and review as per your regular procedures, then upload your 
config like so:

```bash
/path/to/config set prod my_app
```

Changes are applied with the "overwrite" option.  If 
any objects might have been removed from the configuration,
they will not be removed from Fusion.

## More advanced usage
If you need to work with the zip files that Fusion uses,
the `pack` and `unpack` operations transform between the 
exploded and zipped formats. 

The `validate` action sends the change to Fusion without
applying it.

Execute config without any options to get the online help
with more details.

## License
Copyright 2021 by James E. Scarborough and Red Hat, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
