package DbSessionChemistry;

use strict;
use DBI;

use constant DATABASE => "dbi:mysql:dbname=chemistry;host=10.11.8.29";
use constant USERNAME => "asf";
use constant PASSWORD => "asf";

my $DBH;

sub GetConnection {
    unless (ref $DBH eq 'DBI::db') {
	$DBH = DBI->connect(DATABASE, USERNAME, PASSWORD);
    }
    $DBH;
}

1;
