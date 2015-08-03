package DbSessionGpdb;

##########################################
##
## Document   : DbSessionGpdb.pm
## Created on : May 10th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################


use strict;
use DBI;

use constant DATABASE => "dbi:mysql:dbname=human_gpdb;host=10.1.1.145";
use constant USERNAME => "srk";
use constant PASSWORD => "srk";

my $DBH;

sub GetConnection {
    unless (ref $DBH eq 'DBI::db') {
	$DBH = DBI->connect(DATABASE, USERNAME, PASSWORD);
    }
    $DBH;
}

1;
