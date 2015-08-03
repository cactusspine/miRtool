package DbPubchemCidSid;

use DbSessionChemistry;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM pubchem_cid_sid WHERE id=?";

sub GetPubchemCidForSid {
    my $sid = shift;

    my @cid = ();
    if ($sid) { 
        my $databaseHandle = DbSessionChemistry::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(cid) FROM pubchem_cid_sid WHERE sid=?");
        $select->execute($sid);
        my $nr = $select->rows();
        while ($nr--) {
            push @cid, $select->fetchrow_array();
        }
    }
   @cid;
} # sub GetPubchemCidForSid {


sub GetPubchemCidNameForSid {
    my $sid = shift;

    my @cid_name = ();
    if ($sid) {
        my $databaseHandle = DbSessionChemistry::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(m.cid), s.synonym FROM pubchem_cid_sid m, pubchem_cid_synonym s WHERE sid=? AND m.cid=s.cid");
        $select->execute($sid);
        my $nr = $select->rows();
        while ($nr--) {
#            push @cid, $select->fetchrow_array();
	     my ($cid, $name) = $select->fetchrow_array();
	     my $cid_name = $cid . "__" . $name;
	     push @cid_name, $cid_name; 			
        }
    }
   @cid_name;
} # sub GetPubchemCidNameForSid {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id}  = 0;
    $this->{cid} = 0;
    $this->{sid} = 0;
    $this->{type} = '';

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
		$this->{id} = shift @attr;
		$this->{cid} = shift @attr;
		$this->{sid} = shift @attr;
		$this->{type} = shift @attr;
	} else {
	    carp "Initializing pubchem_cid_sid : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
