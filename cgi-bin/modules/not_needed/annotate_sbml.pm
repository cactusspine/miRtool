package annotate_sbml;	

sub get_sbml_annotation {
	my ($in_file, $output_file) = @_;
#	my $in_file = "/Users/satagopam/Documents/Projects/LCSB/PD_Map/test.xml"; #shift;
#	my $output_file = "/Users/satagopam/Documents/Projects/LCSB/PD_Map/test_anno.xml";

use synonym_db2_api;
#print STDERR "in_file : $in_file, output_file : $output_file\n";
#	close(RFH);
	open(RFH, ">$output_file");
	
	close(FH);
	if (open(FH, $in_file)||die "not able to open file : $in_file !!!") {
		my @all = <FH>;
		my @all_copy = @all;
		close(FH);
		my $i=0;
		while(@all) {
			my $line = shift @all;
#<species metaid="s1" id="s1" name="SNCA" compartment="default" initialAmount="0">
			if ($line =~ /<species metaid="s\d+" id="s\d+" name="(.+)"\s.+>/ ) {
				print RFH $line; #adding the "<species metaid= ....>" tag to the new xml file
#print "line : $line";
				my @fields = split('" ', $1);
				my $name = $fields[0];
#print "name : $name\n";
				my $annotation = &synonym_db2_api::get_annotations($name);
				if ($annotation) {
#print "annotation : $annotation\n";
					my $date = `date +%Y/%m/%d`;
					chomp($date);
					my $tag = "[updated by PD map annotation service $date]\n";
					$annotation = $tag . $annotation . $tag;
					$annotation=~s/"//g;

					$line = shift @all; ## may be <annotation> or <notes>

					if ($line=~'<annotation>') {
						my $notes_tag = &get_notes_tag($annotation);	
#print "notes_tag : $notes_tag\n";
						print RFH $notes_tag;
						print RFH $line; ### after adding the notes tag, add back annotation tag as well
					}
					elsif($line=~'<notes>'){
#print "line : $line\n";
						my @tmp = ();
						push @tmp, $line; #<notes> tag added
						do {
							$line = shift @all; 
							push @tmp, $line} until($line=~'</body>');
							pop @tmp; # remove </body> tag
							my $new_notes_tag = join("", @tmp) . $annotation . "</body>\n"; 
#print "new_notes_tag : $new_notes_tag\n";
							print RFH $new_notes_tag;
					}
				} # f ($annotation) 
			} # if ($line =~ /<species metaid="s\d+" id="s\d+" name="(.+)"\s.+>/ )
			else {
				print RFH $line;
			}
		} # while(<FH>) {
	} # if (open(FH, $in_file)) {
	close(RFH);
} # sub get_sbml_annotation {

sub get_notes_tag {
	my $annotation = shift;

	my $notes_tag = "";
$notes_tag .= "<notes>\n";
$notes_tag .= "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
$notes_tag .= "<head>\n";
$notes_tag .= "<title/>\n";
$notes_tag .= "</head>\n";
$notes_tag .= "<body>\n";
$notes_tag .= "$annotation";
$notes_tag .= "</body>\n";
$notes_tag .= "</html>\n";
$notes_tag .= "</notes>\n";
	return $notes_tag;	
}

1;
