import subprocess
from optparse import OptionParser
import time


parser = OptionParser()

parser.add_option('-r', '--runscript', metavar='FILE', type='string', action='store',
                default   =   '',
                dest      =   'runscript',
                help      =   'Run template to use')
parser.add_option('-i', '--inputs', metavar='FILE', type='string', action='store',
                default   =   '',
                dest      =   'inputs',
                help      =   'Inputs to send along')
parser.add_option('-a', '--args', metavar='FILE', type='string', action='store',
                default   =   '',
                dest      =   'args',
                help      =   'Text file with python arguments')


(options, args) = parser.parse_args()

commands = []

print(options.args)

# Tar stuff
if options.inputs != '':
    commands.append("tar czvf tarball.tgz "+options.inputs)

commands.append('mkdir -p condor/logs/')
commands.append('mkdir -p logs/')

# Make JDL from template
timestr = time.strftime("%Y%m%d-%H%M%S")
out_jdl = 'temp_'+timestr+'_jdl'
commands.append("sed 's$TEMPSCRIPT$"+options.runscript+"$g' $CMSSW_BASE/src/BstarToTW_CMSDAS2023/condor/jdl_template > "+out_jdl)
commands.append("sed -i 's$TEMPARGS$"+options.args+"$g' "+out_jdl)
commands.append("condor_submit "+out_jdl)
commands.append("mv "+out_jdl+" condor/logs/")

for s in commands:
    print(s)
    subprocess.call([s],shell=True)
