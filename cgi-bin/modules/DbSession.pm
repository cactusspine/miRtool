package DbSession;

use strict;
use DBI;

use constant DATABASE => "dbi:mysql:dbname=systec;host=10.79.5.221";
use constant USERNAME => "sudo_all";
use constant PASSWORD => "m1SRKmug";

my $DBH;

sub GetConnection {
    unless (ref $DBH eq 'DBI::db') {
	$DBH = DBI->connect(DATABASE, USERNAME, PASSWORD);
    }
    $DBH;
}

1;
