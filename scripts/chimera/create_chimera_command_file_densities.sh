# current directory
dir=$1
# file with density maps colors
file=$2
# file with density maps level value
levels=$3

nlines=`wc -l ${file} | awk '{print $1}'`

# remove old chimera file
rm chimera_density_command_lines.txt 2>/dev/null

for i in `seq 1 ${nlines}`
do
 # extract i-th line
 riga=`sed -n ${i}p ${file}`
 # get full path to density file
 name=`echo $riga | awk '{printf "%s/%s.dx\n",dir,$1}' dir=$dir`
 # get colors
 r=`echo $riga | awk '{print $2}'`
 g=`echo $riga | awk '{print $3}'`
 b=`echo $riga | awk '{print $4}'`
 # find level value
 prefix=`echo $riga | awk '{print $1}'`
 l=`awk '{if($1==name) print $2}' name=$prefix $levels`
 # add to chimera
 echo "open $name" >> chimera_density_command_lines.txt
 echo "volume #${i} style surface level $l color ${r},${g},${b}" >> chimera_density_command_lines.txt
done

# now add visualization stuff
echo "vol all show" >> chimera_density_command_lines.txt
echo "window" >> chimera_density_command_lines.txt
