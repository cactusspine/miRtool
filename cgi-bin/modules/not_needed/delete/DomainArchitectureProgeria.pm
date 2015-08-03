package DomainArchitectureProgeria;

use DbSessionProgeria;
use DbProgeriaDomain;
use DbProgeriaSmartDomain;
use DbProgeriaPfamDomain;
use DbSmartDomainFrequency;
use DbPfamDomainFrequency; 
use Carp;
	
	
sub getDomainArchitectureIndex {
	my ($pair, $dbname) = @_;
	my $a = 0.36; # a, b, c are domain architecture constans
	my $b = 0.01;
	my $c = 0.63; 
	my $jaccardIndex = 0;
	my $goodman_KruskarIndex = 0;
	my $domain_Duplication_Similarty = 0;
	my $distance = 0.000000;
	my %result = ();
	
#print "pair : $pair\n";
	my @pair = split("_", $pair);
	my $domains_1 = &getDomains($pair[0], $dbname );
	my $domains_2 = &getDomains($pair[1], $dbname);
	my @domains_1 = @$domains_1;
	my @domains_2 = @$domains_2;
#@domains_1 = qw(d1 d1 d1 d2 d2 d3 d4);
#@domains_2 = qw(d1 d2 d3 d3 d4 d4 d5);
#print "domains_1 : ";
#print join(", ", @domains_1), "\n";

#print "domains_2 : ";
#print join(", ", @domains_2), "\n";
	my $Npq = 0;
	if (@domains_1 && @domains_2) {
		my $nr_domains_1 = &getNonRedundantList(\@domains_1);
		my $nr_domains_2 = &getNonRedundantList(\@domains_2);
		my @nr_domains_1 = @$nr_domains_1;
		my @nr_domains_2 = @$nr_domains_2;
		$Npq = &getCommonElementSize(\@nr_domains_1, \@nr_domains_2);
		my $nr_domains_1_size = @nr_domains_1;
		my $nr_domains_2_size = @nr_domains_2;

#print "nr_domains_1 : ";
#print join(", ", @nr_domains_1), "\n";

#print "nr_domains_2 : ";
#print join(", ", @nr_domains_2), "\n";

#print "nr_domains_1_size : $nr_domains_1_size \n";
#print "nr_domains_2_size : $nr_domains_2_size \n";
		$jaccardIndex = &getJaccardIndex(\@nr_domains_1, \@nr_domains_2, $nr_domains_1_size, $nr_domains_2_size, $Npq);
#print "jaccardIndex : $jaccardIndex\n";
		if ("@domains_1" eq "@domains_2") {
                        $goodman_KruskarIndex = 1.000000;
                        $goodman_KruskarIndex = sprintf("%.6f", $goodman_KruskarIndex);
                } # if ("@domains_1" eq "@domains_2") {
                else {
			$goodman_KruskarIndex = &getGoodman_KruskarIndex(\@nr_domains_1, \@nr_domains_2, $nr_domains_1_size, $nr_domains_2_size, $Npq);
		} # else {
#print "goodman_KruskarIndex : $goodman_KruskarIndex\n";
		$domain_Duplication_Similarty = &getDomain_Duplication_Similarty(\@domains_1, \@domains_2, \@nr_domains_1, \@nr_domains_2, $Npq);
	
#print "domain_Duplication_Similarty : $domain_Duplication_Similarty\n";
		$distance = $a * $jaccardIndex + $b * $goodman_KruskarIndex + $c * $domain_Duplication_Similarty;  # Spq = aJpq+ bGKpq + cDpq;
	
		$distance = sprintf("%.6f", $distance);
#print "distance : $distance \n";
	} # if (@domains_1 && @domains_2) {
	%result = (jaccardIndex=>$jaccardIndex, goodman_KruskarIndex=>$goodman_KruskarIndex, domain_Duplication_Similarty=>$domain_Duplication_Similarty, distance=>$distance);
	\%result;
} # sub getDomainArchitectureIndex {


# this sub-routine calculates the Domain_Duplication_Similarty, here it take four value
# as input, list of domains in protein p, list of domains in protein q, list of unique
# domains in protein p and q. see the paper "An initial strategy for comparing proteins
# at the domain architecture level. Bioinformatics 22(17) 2006 pages 2081-2086" for more
# details.
sub getDomain_Duplication_Similarty {
	my ($p, $q, $nr_p, $nr_q, $Npq) = @_;
	my @p = @$p;
	my @q = @$q;
	my @nr_p = @$nr_p;
	my @nr_q = @$nr_q;
	my $Dpq = 0.000000;
	my %dup = ();
	my $dp = 0;
	my $dq = 0;
	my $diff = 0;
	my $max = 0;
	my $sum_diff = 0;
	my $sum_max = 0;
	if($Npq != 0) {
#print "Npq : $Npq \n";
#print "sum_diff : $sum_diff, sum_max : $sum_max \n";

#		my %dup = ();
#		my ($dp, $dq, $diff, $max, $sum_diff, $sum_max) = 0;
		foreach my $np (@nr_p) {
#print "np : $np\n";	
			$dp = grep(/$np/, @p);
			$dq = grep(/$np/, @q);
			if ($dq != 0) {
				if ($dp > 0) { $dp--;}
                                if ($dq > 0) { $dq--;}
				$diff = abs($dp - $dq);
				$max = &max($dp, $dq);
#print "dp : $dp, dq : $dq, diff : $diff, max : $max \n";
				$sum_diff += $diff;
				$sum_max += $max; 
			} # if ($dq != 0) {
		} # foreach my $np (@nr_p) {

#print "sum_diff : $sum_diff, sum_max : $sum_max \n";
	 	foreach my $nq (@nr_q) {
#print "nq : $nq\n";
                	$dp = grep(/$nq/, @p);
                	$dq = grep(/$nq/, @q);
			if ($dp != 0) {
				if ($dp > 0) { $dp--;}
                                if ($dq > 0) { $dq--;}
                		$diff = abs($dp - $dq);
                		$max = &max($dp, $dq);
#print "dp : $dp, dq : $dq, diff : $diff, max : $max \n";
                		$sum_diff += $diff;
                		$sum_max += $max;
			} # if ($dp != 0) {
        	} # foreach my $np (@nr_p) { 
#print "sum_diff : $sum_diff, sum_max : $sum_max \n";
		if ($sum_max == 0) {
			$sum_max = 1;
		}
		$Dpq = exp(-1 * $sum_diff / $sum_max);
	 } # if($Npq != 0) {
	$Dpq = sprintf("%.6f", $Dpq);
	return $Dpq;
	
} # sub getDomain_Duplication_Similarty {



# Goodman Kruskar index GKpq = (1+GAMApq) / 2
# GAMApq = ($Ns - $Nr) / ($Ns + $Nr);
# where Ns is the total no. of occurrence of same order pair in all distinct pairs,
#       Nr is the total no. of occurrence of reverse order pair in all distinct pairs 
#of domains in proteins p and q
# this sub-routine calculate the Goodman Kruskar index and returns its value.
sub getGoodman_KruskarIndex {
	my ($p, $q, $Np, $Nq, $Npq) = @_;
	my $GKpq = 0.000000;
	my $GAMApq = 0.000000;
	if ($Npq != 0) {
		if ($Np > 1 && $Nq > 1) {
			my @p = @$p;
	        	my @q = @$q;
			my $p_pairs = &getPairsInOrder(\@p);
			my $q_pairs = &getPairsInOrder(\@q);
			my @p_pairs = @$p_pairs;
			my @q_pairs = @$q_pairs;
#print "\np_pairs : ", join(", ", @p_pairs), "\n";
#print "\nq_pairs : ", join(", ", @q_pairs), "\n";
			my @pq_pairs = (@p_pairs,  @q_pairs);
#print "\npq_pairs : ", join(", ", @pq_pairs), "\n";
			my $unique_pairs = &getNonRedundantList(\@pq_pairs);
			my @unique_pairs = @$unique_pairs;
#print "\nunique_pairs : ", join(", ", @unique_pairs), "\n";

			my $s = 0;
                        my $r = 0;
                        my $Ns = 0;
                        my $Nr = 0;
			foreach my $unique_pair (@unique_pairs) {
#print "\nunique_pair : $unique_pair\n";
				$s = $r = 0;
				my @pair = split("____", $unique_pair);
				my $reverse_pair = $pair[1]."____".$pair[0];
				$s = grep(/$unique_pair/, @pq_pairs);
				$s--;
				$Ns += $s;
#print "s : $s\n";	
				$r = grep(/$reverse_pair/, @pq_pairs);
#print "r : $r\n";	
				$Nr += $r;	
			} # foreach my $unique_pair (@unique_pairs) {
#print "Ns : $Ns \n";
#print "Nr : $Nr \n";
			if (($Ns + $Nr) != 0) {	
				$GAMApq = ($Ns - $Nr) / ($Ns + $Nr);
			} # if ($Ns && $Nr) {
		} # if ($Np > 1 && $Nq > 1) {

#print "GAMApq : $GAMApq \n";
		$GKpq = (1+$GAMApq) / 2;
	 } # if ($Npq != 0) {
#print "GKpq : $GKpq\n"; 
	$GKpq = sprintf("%.6f", $GKpq);
	return $GKpq;
	
} # sub getGoodman_KruskarIndex {


# Jaccard index Jpq = (Npq)/((Np+Nq) - Npq)
# where N'p is the number of distinct domains in protein p
#       N'q is the number of distinct domains in protein q
#       N'pq is the number of common distinct domains in both protein p and q.
# this sub-routine calcute the jaccard index and return its value.
sub getJaccardIndex {
	my ($p, $q, $Np, $Nq, $Npq) = @_;
	my $Jpq = 0.000000;
	my @p = @$p;
	my @q = @$q;
#	my $Npq = &getCommonElementSize(\@p, \@q);
	$Jpq = $Npq / (($Np+$Nq) - $Npq);	
	$Jpq = sprintf("%.6f", $Jpq);
	return $Jpq;	
} # sub getJaccardIndex {


# This sub-routine takes protein_id (eg:49994), dbname (eg: 'Pfam'), 
# and returs the domains present in the protein associted to protein_id. 
sub getDomains {
        my ($protein_id, $dbname) = @_;
        my @domainsIds = ();
        @domainsIds = DbProgeriaDomain::GetDomainIdsForPIDandDBName($protein_id, $dbname);
#print "clopDomainsIds", join(", ", @clopDomainsIds), "\n";
        my @domains = ();
        foreach my $d (@domainsIds) {
                my $domain;
                $domain = new DbProgeriaDomain($d, $dbname);
		if ($domain->{Description}) {
                	push @domains, $domain->{Description};
		}
        } # foreach my $d (@clopDomainsIds) {
#print "domains from getDomains sub routine", join(", ", @domains), "\n";
	return \@domains

} # sub getDomains {

# This sub-routine returns the Pfam_Domains  object for given cluster_details_id.
sub getPfamDomainInfo {
        my ($protein_id) = @_;
        my @clusterDomainsIds = ();
        @clusterDomainsIds = DbProgeriaPfamDomain::GetDomainIdsForPIDandDBName($protein_id);
        my @domains = ();
        foreach my $d (@clusterDomainsIds) {
                my $domain;
                $domain = new DbProgeriaPfamDomain($d);
                if ($domain->{Description}) {
                        push @domains, $domain;
                }
        } # foreach my $d (@clusterDomainsIds) {
        return \@domains
} # sub getPfamDomainInfo {

# This sub-routine returns the MP_Domains  object for given cluster_details_id.
sub getSmartDomainInfo {
        my ($protein_id) = @_;
        my @clusterDomainsIds = ();
        @clusterDomainsIds = DbProgeriaSmartDomain::GetDomainIdsForPIDandDBName($protein_id);
        my @domains = ();
        foreach my $d (@clusterDomainsIds) {
                my $domain;
                $domain = new DbProgeriaSmartDomain($d);
                if ($domain->{Description}) {
                        push @domains, $domain;
                }
        } # foreach my $d (@clusterDomainsIds) {
        return \@domains
} # sub getPfamDomainInfo {


#sub getSmartDomainInfoForProtein {
#        my ($protein) = @_;
#        my @domainsIds = ();
#        @domainsIds = &DbProgeriaSmartDomain::GetDomainIdsForProtein($protein);
#        my @domains = ();
#        foreach my $d (@domainsIds) {
#                my $domain;
#                $domain = new DbProgeriaSmartDomain($d);
#                if ($domain->{Description}) {
#                        push @domains, $domain;
#                }
#        } # foreach my $d (@clusterDomainsIds) {
#        return \@domains
#} # sub getSmartDomainInfoForProtein {


# This sub-routine generates the pairs for a given list, for example if the list contains A B C D,
# it generates A____B, A____C, A____D, B____C, B____D, C____D and it follows the order.
sub getPairsInOrder {
	my $L = shift;
	my @L = @$L;
	my $size = @L;

	my @pairs = ();
	for (my $i=0; $i<$size; $i++) {
		my $p='';
		for(my $j=$i+1; $j<$size; $j++) {
			$pair = $L[$i]."____".$L[$j];
			push @pairs, $pair;
		}
	}
	return \@pairs;
} # sub getPairsInOrder {


# This sub-routine generates the pairs for a given list, for example if the list contains A B C D,
# it generates A_B, A_C, A_D, B_C, B_D, C_D.
#sub getPairs {
#	my $clopIds = shift;
#	my @clopIds = @$clopIds;
#	
#        my @allComboKeys = ();
#        my $combinat = Math::Combinatorics->new(  count => 2,
#                                                  data => [@clopIds],
#                                                );
#
#	while(my @combo = $combinat->next_combination){
#        	@combo = sort @combo;
#                my $keyStr = '';
#                foreach my $m (@combo) {$keyStr = $keyStr .+ $m .+ '_';}
#                chop($keyStr);
#                push @allComboKeys, $keyStr;
#        } # while(my @combo = $combinat->next_combination){
#
#	return \@allComboKeys;
#} # sub getPairs {
	

# it returns the unique or non redundant list and it maintains the order of elements.
# For example if the input is @in = (1, 1, 1, 2, 3, a, 5, 5, b, 6, 7, 8, 9, 9, 10, 11, 11, c, 12, 12, 1, 2, 3, 1, 1, 1);
# the out put is @out = (1, 2, 3, a, 5, b, 6, 7, 8, 9, 10, 11, c, 12);
sub getNonRedundantList {
	my $in = shift;
	my @in = @$in;
        my %seen = ();
        my @out = ();
 	foreach my $i (@in) {
   		push(@out, $i) unless $seen{$i}++;
 	} # foreach my $i (@in) {

	return \@out;
} # sub getNonRedundantList { 



# subroutine name: max
# Input: number1, number2
# returns greater of 2 numbers
sub max {
	if ($_[0]<$_[1]) {return $_[1]} else {return $_[0]};
} # sub max {

sub getCommonElementSize {
        my ($L1, $L2) = @_;
        my $size = 0;
        my @L1 = @$L1;
        my @L2 = @$L2;
        my $sizeL1 = @L1;
        my $sizeL2 = @L2;
        for (my $i=0; $i<$sizeL1; $i++) {
                for (my $j=0; $j<$sizeL2; $j++){
                        if ($L1[$i] eq $L2[$j]) {$size++;}
                } # for (my $j=0; $j<$sizeL2; $j++){
        } # for (my $i=0; $i<$sizeL1; $i++) {

        return $size;
} # sub getCommonElementSize {

1;
