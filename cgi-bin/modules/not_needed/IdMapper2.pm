package IdMapper2;

##########################################
##
## Document   : HumanIdMapper.pm
## Created on : August 29th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
## Description: It mapps/ converts different ids to ensembl gene ids ..it is file based
##
##########################################

my $map_dir = "/g/projects_rs/biocompendium/data/";

sub get_ensembl_genes {
	my ($org, $list, $id_doc_type, $primary_org) = @_;
	my @list = @$list;
#print "list : @list<br>";	
	my @ensembl_genes = ();
#	if ($id_doc_type ne 'ensembl_gene_id') {
		my $file = $map_dir . $org . "/biomart/" . $id_doc_type;
#print "from IdMapper<br>org : $org<br>primary_org:$primary_org<br>";
#print STDERR "file : $file<br>";
		my %map_hash = ();
		my $line = "";
		close(FH);
		if (open(FH, "$file")) {
			while(<FH>) {
				$line = $_;
				chomp($line);
				my ($ensg, $second_id) = split("\t", $line);
				$map_hash{$second_id} = $ensg;			
			} # while(<FH>) {
		} # if (open(FH, "$file")) {
		close(FH);
#my @keys = keys %map_hash;
#my $keys_size = @keys;
#print "keys_size : $keys_size<br>";
		foreach my $e (@list) {
#		chomp($e);
#print "protein : $e<br>";
			if ($map_hash{$e}) {
				my $id = $map_hash{$e};
#print "gene : $id<br>";
				push @ensembl_genes, $id;
			} # if ($map_hash{$e}) {
		} # foreach my $e (@list) {
		
		@ensembl_genes = &nonRedundantList(\@ensembl_genes);
#	} # if ($id_doc_type ne 'ensembl_gene_id') {
#	else {
#		@ensembl_genes = @list;
#	}

# the following part get the orthogs ....if necessary ...
	if ($org eq $primary_org) {
#print "org and primary org same<br>";
		return @ensembl_genes;
	} # if ($org eq $primary_org) {
	else {
		my $ortho_file =  $map_dir . $org . "/biomart/" . $org . "2" . $primary_org . "_orthologs";
		my %ortho_hash = ();
		close(ORTHO);
		if (open(ORTHO, "$ortho_file")) {
			while(<ORTHO>) {
				$line = $_;
				chomp($line);
				my ($gene1, $gene2) = split("\t", $line);
				$ortho_hash{$gene1} = $gene2;			
			} # while(<ORTHO>) {
		} # if (open(ORTHO, "$ortho_file")) {
		close(ORTHO);

		my @ortho_ensembl_genes = ();
		foreach my $e (@ensembl_genes) {
#print "e:$e:-->";		
			if ($ortho_hash{$e}) {
#print "$ortho_hash{$e}<br>";			
				push @ortho_ensembl_genes, $ortho_hash{$e};
			} # if ($ortho_hash{$e}) {
		} # foreach my $e (@ensembl_genes) {
		
		@ortho_ensembl_genes = &nonRedundantList(\@ortho_ensembl_genes);
		return @ortho_ensembl_genes;	
	} # else {
} # sub get_ensembl_genes {


sub get_ensg2uniprot {
	my ($org, $list) = @_;
	my $id_doc_type = "uniprot_swissprot_accession";
	my @list = @$list;
#print "list : @list<br>";	
	my @uniprot_acc = ();
		my $file = $map_dir . $org . "/biomart/" . $id_doc_type;
		my %map_hash = ();
		my $line = "";
		close(FH);
		if (open(FH, "$file")) {
			while(<FH>) {
				$line = $_;
				chomp($line);
				my ($ensg, $second_id) = split("\t", $line);
				push @{$map_hash{$ensg}},$second_id;			
			} # while(<FH>) {
		} # if (open(FH, "$file")) {
		close(FH);
		foreach my $e (@list) {
		chomp($e);
#print "protein : $e<br>";
			if ($map_hash{$e}) {
				my $ids = $map_hash{$e};
				my @ids = @$ids;
				push @uniprot_acc, @ids;
			} # if ($map_hash{$e}) {
		} # foreach my $e (@list) {
		
		@uniprot_acc = &nonRedundantList(\@uniprot_acc);
#print "gene : $id<br>";
	return @uniprot_acc;
}# sub get_ensg2uniprot {

sub nonRedundantList{
  my $val = shift;
  my @val=@$val;                                                
  my %cpt;
  foreach (@val){                                               
    $cpt{$_}++;                                                 
  }                                                             
  return keys %cpt;
} # sub redundantList{
