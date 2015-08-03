package DbHmdbCidSid;

use DbSessionChemistry;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM hmdb_cid_sid WHERE hmdb_id=?";



sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{hmdb_id} = '';
    $this->{name} = '';
    $this->{cid} = '';
    $this->{sid} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $Id = shift;

    if ($Id) {
	my $databaseHandle = DbSessionChemistry::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($Id);
	if ($select->rows == 1) {
		my @attr = $select->fetchrow_array;
		$this->{hmdb_id} = shift @attr;
		$this->{name} = shift @attr;
		$this->{cid} = shift @attr;
		$this->{sid} = shift @attr;
	} else {
	    carp "Initializing hmdb_cid_sid : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
