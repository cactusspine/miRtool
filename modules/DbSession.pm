package DbSession;

use strict;
use DBI;

use constant DATABASE => "dbi:mysql:dbname=gist";
#$dsn database source name my $dsn="DBI:$driver:database= $databasename";
#my $driver = "mysql";
#my $database
#use constant DATABASE => "dbi:mysql:dbname=systec;host=10.79.2.1";
#use constant DATABASE => "dbi:mysql:dbname=systec;host=10.79.5.221";

#use constant USERNAME => "sudo_all";
#use constant PASSWORD => "m1SRKmug";
use constant USERNAME => "srk";
use constant PASSWORD => "srk";

my $DBH;#data base handle object 

sub GetConnection {
    unless (ref $DBH eq 'DBI::db') {
	$DBH = DBI->connect(DATABASE, USERNAME, PASSWORD);#connect ($data_source,"","",\%attr) retrun a handling object
	#$dbh->do($sql); prepare and excute a simple SQL sentence. retrurn the lines which are affected
	#$sth->prepare($sql);$sth->execute() prepare and retrun a sentance handle obj and execute,if success, return true
	#$sth->fetchrow_array() rutrun next line
    }
    $DBH;
}

1;
