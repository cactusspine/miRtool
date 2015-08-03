#!/usr/bin/perl -w

#################################################################
##                                                             ##       
## Developed by Venkata P. Satagopam as part of his PhD thesis ##
##                       July 2009                             ##
##                 venkata.satagopam@embl.de                   ##
##                                                             ##
## Disclaimer: Copy rights reserved by EMBL, please contact    ## 
##             Venkata Satagopam  prior to reuse any part      ##
##             of this code                                    ##
##                                                             ##
#################################################################

use strict;
use CGI qw(:standard);      # or any other CGI:: form handler/decoder
use lib "/home/database/projects/gist/systec/modules";
use DbSearchLookup;


sub suggest {
	my ($input) = @_;
	my $output = "";
	my @names = &DbSearchLookup::auto_detect($input);	
	if (@names) {
		$output = "<ul>";
		foreach my $name (@names) {
			$output.="<li>$name</li>";	
		} # foreach my $name (@names) {
	} # if (@names) {
	return ("$output</ul>");
}


print header;
my $input = param('search'); # unless $input = param('contact_name');
#$input = "$input";
#print "input : $input, org : $org\n";

my $output = &suggest($input);
print "$output";

