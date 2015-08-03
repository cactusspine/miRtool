package blast_result_parser;

##########################################
##
## Document   : blast_result_parser.pm
## Created on : August 5th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use Bio::SearchIO;

sub parse_blast_results {
	my $file = shift; 
	my %result = ();
	my %gpcr_result = ();
	my %gprot_result = ();
	my %eff_result = ();

	my @homolog_pairs = ();

	my $in = new Bio::SearchIO( -format => 'blast', -file => $file);

	while( my $next_result = $in->next_result ) {
		my $id = $next_result->query_name();
           	my $desc = $next_result->query_description();
	        my $dbname = $next_result->database_name();
		$gpcr_result{$id}{qdesc } = $desc;
		$gprot_result{$id}{qdesc } = $desc;
		$eff_result{$id}{qdesc } = $desc;
		my %gpcr_hit_result = ();
		my %gprot_hit_result = ();
		my %eff_hit_result = ();
		while (my $h = $next_result->next_hit ) {
			my $hit_ID = $h->name;
			my $significance = $h->significance;
			my $hsps = $h->hsps;
			my $description = $h->description;
			my $accession = $h->accession;
			my $length = $h->length;
			my $score = $h->raw_score;
			my $rank = $h->rank;
			my $algorithm = $h->algorithm;
			my $frac_identical = $h->frac_identical;
			my ($category, $hid) = split("_", $hit_ID);
			if ($category eq 'gpcr') {
	                       	$gpcr_hit_result{$hid}{hdes} = $description;
		                $gpcr_hit_result{$hid}{significance} = $significance;
        		        $gpcr_hit_result{$hid}{length} = $length;
                	 	$gpcr_hit_result{$hid}{score} = $score;
	                        $gpcr_hit_result{$hid}{frac_identi} = $frac_identical;
			} # if ($category eq 'gpcr') {
			elsif ($category eq 'gprotein') {
        	               	$gprot_hit_result{$hid}{hdes} = $description;
	        	        $gprot_hit_result{$hid}{significance} = $significance;
        	                $gprot_hit_result{$hid}{length} = $length;
                	       	$gprot_hit_result{$hid}{score} = $score;
                		$gprot_hit_result{$hid}{frac_identi} = $frac_identical;
			} # elsif ($category eq 'gprotein') {
			elsif ($category eq 'effector') {
        	                $eff_hit_result{$hid}{hdes} = $description;
	        	        $eff_hit_result{$hid}{significance} = $significance;
        	        	$eff_hit_result{$hid}{length} = $length;
                	        $eff_hit_result{$hid}{score} = $score;
        	         	$eff_hit_result{$hid}{frac_identi} = $frac_identical;
			} # elsif ($category eq 'effector') {
		} # while (my $h = $next_result->next_hit ) {
		$gpcr_result{$id}{hits} = \%gpcr_hit_result;
		$gprot_result{$id}{hits} = \%gprot_hit_result;
		$eff_result{$id}{hits} = \%eff_hit_result;
	} # while( my $next_result = $in->next_result ) {
	%result = (gpcr_result=>\%gpcr_result, gprot_result=>\%gprot_result, eff_result=>\%eff_result);
	return \%result;
} # sub parse_blast_results {

sub parse_blast_results_for_paralog {
        my $file = shift;
        my %result = ();
        my @paralog_pairs = ();

        my $in = new Bio::SearchIO( -format => 'blast', -file => $file);

        while( my $next_result = $in->next_result ) {
                my $id = $next_result->query_name();
                my $desc = $next_result->query_description();
                my $dbname = $next_result->database_name();
                while (my $h = $next_result->next_hit ) {
                        my $hit_ID = $h->name;
                        my $significance = $h->significance;
                        my $hsps = $h->hsps;
                        my $description = $h->description;
                        my $accession = $h->accession;
                        my $length = $h->length;
                        my $score = $h->raw_score;
                        my $rank = $h->rank;
                        my $algorithm = $h->algorithm;
                        my $frac_identical = $h->frac_identical;
                        my @temp = ();
                        my $pair = "";
                        if (($id ne $hit_ID) && ($rank == 1)) {
                                my @id = split('\|', $id);
                                my $id_size = @id;
                                my @hit_ID = split('\|', $hit_ID);
                                my $hitid_size = @hit_ID;
                                my $qid = "";
                                my $qname = "";
                                my $hid = "";
                                my $hname = "";
                                if ($id_size > 1 ) {
                                        $qid = $id[0];
                                        $qname = $id[1];
                                } # if ($id_size > 1 ) {
                                else {
                                        $qid = $id[0];
                                        $qname = "";
                                } # else {
                                if ($hitid_size > 1) {
                                        $hid = $hit_ID[0];
                                        $hname = $hit_ID[1];
                                } # if ($hitid_size > 1) {
                                else {
                                        $hid = $hit_ID[0];
                                        $hname = "";
                                } # else {
                                $result{$qid}{qname } = $qname;
                                $result{$qid}{hid} = $hid;
                                $result{$qid}{hname} = $hname;
                                $result{$qid}{qdes} = $desc;
                                $result{$qid}{hdes} = $description;
                                $result{$qid}{signif} = $significance;
                                $result{$qid}{score} = $score;
                                $result{$qid}{frac_identi} = $frac_identical;
                        } # if (($id ne $hit_ID) && ($rank == 1)) {
                } # while (my $h = $next_result->next_hit ) {
        } # while( my $next_result = $in->next_result ) {
        return \%result;
} # sub parse_blast_results_for_paralog {

# get common elements method forexample @array1 = ( '0', '1', '2', '3', '5' ) and  @array2 = ( '0', '1', '2', '3', '4', '6' )
# the following method return @common_array = ( '0', '1', '2', '3' )

sub get_common_elements_using_foreach {
	my ($array1, $array2) = @_;
	my @array1 = @$array1;
	my @array2 = @$array2;	
	my @common = ();
	
	foreach my $element1 (@array1) {
                foreach my $element2 (@array2) {
                    if ($element1 eq $element2) {
                        push @common, $element1 unless grep { $element1 eq $_ } @common;
                    }
                }
            }
	
	return \@common;	
} # sub get_common_elements_using_foreach {


sub get_common_elements_using_grep {
        my ($array1, $array2) = @_;
        my @array1 = @$array1;
        my @array2 = @$array2;
        my @common = ();
        
	@common =
                grep {
                    my $element1 = $_;
                    ! grep { $element1 == $_ } @array2
                } @array2; 
         
        return \@common; 
} # sub get_common_elements_using_foreach { 
1;
