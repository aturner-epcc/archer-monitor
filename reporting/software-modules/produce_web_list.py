#!/usr/bin/env python
#
# Produce list of software modules for website
#

from datetime import datetime, timedelta
import sys
import os

###############################################################
# Configuration section
###############################################################
indir = os.environ['ARCHER_MON_LOGDIR'] + '/modules'
outdir = os.environ['ARCHER_MON_OUTDIR'] + '/modules'

###############################################################
# End Configuration section
###############################################################

# Get the filename for yesterday's defaults
now = datetime.today()
logdate = now - timedelta(days=1)
filename = "{0}/{1}.avail".format(indir, logdate.strftime("%Y-%m-%d"))
print filename

if os.path.isfile(filename):
   datafile = open(filename, 'r')
else:
   sys.stderr.write("File does not exist: {1}".format(filename))
   sys.exit(1)

# Loop over lines in the file
modname = []
modversions = {}
moddefault = {}
for line in datafile:
    if line.startswith('#'):
       continue
    line = line.rstrip()
    tokens = line.split('/')
    if len(tokens) == 1:
        if tokens[0] not in modname:
            modname.append(tokens[0])
            modversions[tokens[0]] = ''
            moddefault[tokens[0]] = ''
    else:
        if tokens[0] not in modname:
            modname.append(tokens[0])
            if "(default)" in tokens[1]:
                version = tokens[1].replace("(default)", "")
                modversions[tokens[0]] = [version]
                moddefault[tokens[0]] = version
            else:
                modversions[tokens[0]] = [tokens[1]]
                moddefault[tokens[0]] = ""
        else:
            if "(default)" in tokens[1]:
                version = tokens[1].replace("(default)", "")
                moddefault[tokens[0]] = version
                if version not in modversions[tokens[0]]:
                    modversions[tokens[0]].append(version)
            else:
                if tokens[1] not in modversions[tokens[0]]:
                    modversions[tokens[0]].append(tokens[1])

outfile = "{0}/{1}".format(outdir ,"modulelist.html")
htmlout = open(outfile, "w")
htmlout.write("<p>Last Updated: {0}</p>\n".format(now.strftime("%Y-%m-%d")))
htmlout.write('<table class="cse-table">\n')
htmlout.write("""   <tr>
      <th>Module</th>
      <th>Current Default</th>
      <th>Versions Available</th>
   </th>\n""")
for mod in modname:
    htmlout.write("   <tr>\n")
    ver = ''
    for i, version in enumerate(modversions[mod]):
        if i > 0:
            ver = "{0}, {1}".format(ver, version)
        else:
            ver = version
    htmlout.write("""      <td>{0}</td>
      <td>{1}</td>
      <td>{2}</td>\n""".format(mod, moddefault[mod], ver))
    htmlout.write("   </tr>\n")
htmlout.write("</table>\n")
htmlout.close()

sys.exit(0)

