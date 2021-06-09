import sys
if sys.version_info < (3, 6):
    raise Exception("Python 3.6 or above is required")

import subprocess
import datetime
import re
import datetime

# object wrappers                                                                                                                                                                                                      
class wrapper:
    def __init__(self, **kw):
        vars(self).update(kw)


class Distribution(wrapper):
    pass


def os_popen(list):
    return subprocess.Popen(list, stdout=subprocess.PIPE, universal_newlines=True)

def relase_distributions(project, src, sort_revision):

    # current date information will help process svn ls results
    gatherDate = datetime.datetime.utcnow()
    gatherDateString = datetime.datetime.utcnow().ctime()
    gatherYear = gatherDate.year

    signatures = {}
    checksums = {}
    fsizes = {}
    dtms = {}
    versions = {}
    revisions = {}

    with os_popen(['svn', 'ls', '-Rv', f'https://dist.apache.org/repos/dist/release/{project}']) as s:
        for line in s.stdout:
            line = line.strip()
            listing = line.split(' ')
            if line[-1:] == '/':
                # skip directories
                continue
            if sort_revision:
                revision = int(listing[0])
            else:
                revision = 0
            user = listing[1]
            if listing[-6] == '':
                dtm1 = datetime.datetime.strptime(" ".join(listing[-4:-2])+" "+str(gatherYear),"%b %d %Y")
                if dtm1 > gatherDate:
                    dtm1 = datetime.datetime.strptime(" ".join(listing[-4:-2])+" "+str(gatherYear-1),"%b %d %Y")
                fsize = listing[-5]
            else:
                dtm1 = datetime.datetime.strptime(" ".join(listing[-5:-1]),"%b %d %Y")
                fsize = listing[-6]
            dtm = dtm1.strftime("%m/%d/%Y")
            line = listing[-1]
            fields = line.split('/')
            filename = fields[-1]
            parts = line.split('.')
            release = line
            if filename:
                if re.search('KEYS(\.txt)?$', filename):
                    keys = f'https://dist.apache.org/repos/dist/release/{project}/{line}'
                elif re.search('\.(asc|sig)$', filename, flags=re.IGNORECASE):
                    release = '.'.join(parts[:-1]) 
                    signatures[release] = filename
                    versions[release] = '/'.join(fields[:-1])
                    revisions[release] = revision
                    if re.search(src, filename):
                        # put source distributions in the front.
                        revisions[release] = revision+100000
                elif re.search('\.(sha512|sha1|sha256|sha|md5)$', filename, flags=re.IGNORECASE):
                    part0 = ".".join(line.split('.')[-2:-1])
                    if part0 == "asc":
                        continue
                    release = '.'.join(parts[:-1]) 
                    checksums[release] = filename
                else:
                    fsizes[release] = fsize
                    dtms[release] = dtm
    distributions = [ Distribution(release=rel[len(versions[rel]) + 1:],
                                   revision=revisions[rel],
                                   version=versions[rel],
                                   signature=signatures[rel],
                                   checksum=checksums[rel],
                                   dtm=dtms[rel],
                                   fsize=fsizes[rel])
                      for rel in signatures]
    distributions.sort(key=lambda x: (-x.revision, x.version, x.release))
    return keys, distributions

print("Gather PGP keys data and releases ...")

sort_revision = True
project = 'pulsar'
src = 'src'
keys, distributions = relase_distributions(project, src, sort_revision)

print("===================================================================")
print("Version     | Release        | Signature         | Hash   ")
print("------------|----------------|-------------------|--------")
for distro in distributions:
    print(f"{distro.version} | {distro.release} | {distro.signature} | {distro.checksum}")
print("===================================================================")
print(f"{keys}")

sort_revision = False
project = 'openoffice'
src = 'src'

keys, distributions = relase_distributions(project, src, sort_revision)

print("===================================================================")
print("Version     | Release        | Signature         | Hash   ")
print("------------|----------------|-------------------|--------")
for distro in distributions:
    print(f"{distro.version} | {distro.release} | {distro.signature} | {distro.checksum}")
print("===================================================================")
print(f"{keys}")
