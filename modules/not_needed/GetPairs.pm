package GetPairs;

# This sub-routine generates the pairs for a given list, for example if the list contains A B C D,
# it generates A____B, A____C, A____D, B____C, B____D, C____D and it follows the order.
sub getPairsInOrder {
        my $L = shift;
        my @L = @$L;
        @L = sort @L;
        my $size = @L;

        my @pairs = ();
        for (my $i=0; $i<$size; $i++) {
                my $p='';
                for(my $j=$i+1; $j<$size; $j++) {
#                        $pair = $L[$i]."____".$L[$j];
                        $pair = $L[$i]."\t".$L[$j];
                        push @pairs, $pair;
                }
        }
        return \@pairs;
} # sub getPairsInOrder {
1;
