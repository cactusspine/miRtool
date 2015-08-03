package stitchAPI;

use LWP::Simple;

sub getDescription {
	my $id = shift;
	my $url = "http://stitch.embl.de/services/iteminfo?node=" . $id ;
	my $content = get($url);
#print "content : $content";
	my @lines = split('\n', $content);
	my $line;
	do {
		$line = shift @lines;
	}until ($line =~ /^<p><table><tr><td valign='top'>/ or not scalar @lines);
	my $des = shift @lines;
	$des =~ s/<br>//g;
#print "des : $des\n";
	return $des;
} 

1;
