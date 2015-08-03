package DbSession;

use strict;
use DBI;

use constant DATABASE => "dbi:mysql:dbname=biocompendium;host=10.1.1.155";
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
