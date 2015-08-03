package Synonym_db;

##########################################
##
## Document   : HumanIdMapper.pm
## Created on : August 29th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
## Description: It mapps/ converts different ids to ensembl gene ids ..it is file based
##
##########################################

my $map_dir = "/g/projects_rs/garuda/synonym_db/data/biomart/";

sub get_uniprot_pac {
	my ($org, $list) = @_;
	my @list = @$list;
	my @ensembl_genes = ();
		my $file = $map_dir . $org . "_uniprot2ensp.txt";
#print "from IdMapper<br>org : $org<br>primary_org:$primary_org<br>";
#print "file : $file<br>";
		my %map_hash = ();
		my $line = "";
		close(FH);
		if (open(FH, "$file")) {
			while(<FH>) {
				$line = $_;
				chomp($line);
				my ($uniprot_pac, $ensp) = split("\t", $line);
				push @{$map_hash{$ensp}}, $uniprot_pac;			
			} # while(<FH>) {
		} # if (open(FH, "$file")) {
		close(FH);
		my %result_hash = ();
		foreach my $e (@list) {
			if ($map_hash{$e}) {
				my @ids = @{$map_hash{$e}};
				@ids = &nonRedundantList(\@ids);
				my $uniprot_ids_str = join("__",@ids);
				$result_hash{$e} = $uniprot_ids_str;
			} # if ($map_hash{$e}) {
		} # foreach my $e (@list) {
		return %result_hash;
} # sub get_uniprot_pac {


sub nonRedundantList{
  my $val = shift;
  my @val=@$val;                                                
  my %cpt;
  foreach (@val){                                               
    $cpt{$_}++;                                                 
  }                                                             
  return keys %cpt;
} # sub redundantList{
