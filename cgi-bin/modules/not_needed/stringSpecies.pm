package stringSpecies;

sub getStringSpecies {
	my $input = shift;
	my $species_name_file = "/g/projects_rs/biocompendium/modules/species_taxon_name.txt";
	close(SPECIES_NAME_FILE);

	my %taxon2name_hash = ();
	my %name2taxon_hash = ();

	if (open(SPECIES_NAME_FILE,$species_name_file)||die "can't open species_name_file : $species_name_file for reading!!!") {
		while (<SPECIES_NAME_FILE>) {
			my $line = $_;
			chop($line);
			my ($taxon_id, $name) = split("\t", $line);
			$taxon2name_hash{$taxon_id} = $name;
			$name2taxon_hash{$name} = $taxon_id;
		} # while (<SPECIES_NAME_FILE>) {
	} # if (open(SPECIES_NAME_FILE,$species_name_file)||die "can't open species_name_file : $species_name_file for reading!!!") {

	my $output = "";
	if ($input =~ /^\d+$/) {
		$output = $taxon2name_hash{$input};	
	}
	else {
		 $output = $name2taxon_hash{$input};
	}
	return $output;
} # sub getStringSpecies {

1;
