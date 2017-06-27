
# Usage: perl make_field_ipdata.pl 'exdata_file'

# modified by J Fernandez 29/11/2011

use Math::Trig;  

${host_name} = $ARGV[0];


open (EXDATA, "${host_name}.opnode") || die ("NO ${host_name}.exdata EXISTS");


@hdata=<EXDATA>;                               #print "@data";

${total_lines} = $#hdata;                    

#print "${total_lines}\n";

$node=0;

for ($line = 0 ; $line < ${total_lines} + 1 ; $line = $line + 1)
  { 
   chomp $hdata[$line];
   $_ = $hdata[$line];  

   if (m/nj= 1/)
      {                          
       chomp $hdata[$line];       
       @x = split(/\s+/,$hdata[$line]);
       print "Node ".$x[2]."\n";    
       print "$x[4]\n";  
       print "$x[11]\n";
       $force[$x[2]][$x[4]]=$x[11];
  
      }

   if (m/nj= 2/)
      {                          
       chomp $hdata[$line];       
       @y = split(/\s+/,$hdata[$line]);    
       print "$y[2]\n";  
       print "$y[9]\n";  
       $force[$x[2]][$y[2]]=$y[9];
      }

   if (m/nj= 3/)
      {                          
       chomp $hdata[$line];       
       @z = split(/\s+/,$hdata[$line]);    
       print "$z[2]\n";  
       print "$z[9]\n";
       $force[$x[2]][$z[2]]=$z[9];  
      }

  }

#print 'X force at node 75 is ',$force[75][1]."\n";
#print 'Y force at node 75 is ',$force[75][2]."\n";
#print 'Z force at node 75 is ',$force[75][3]."\n";

$xf=0.0;
$yf=0.0;
$zf=0.0;

for ($i = 1 ; $i < 97; $i++)
  { 
      $xf=$xf+$force[$i][1];
      $yf=$yf+$force[$i][2];
      $zf=$zf+$force[$i][3];
  }

print "total x force is ",$xf."\n"; 
print "total y force is ",$yf."\n"; 
print "total z force is ",$zf."\n";

$net=($xf*$xf)+($yf*$yf)+($zf*$zf);
$net=sqrt($net);
print "net force is ",$net."\n";

close (EXDATA);


