package DbDrugbankCidSid;

##########################################
##
## Document   : DbDrugbankCidSid.pm
## Created on : June 20th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionChemistry;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM drugbank_cid_sid WHERE drugbank_id=?";



sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{drugbank_id} = '';
    $this->{name} = '';
    $this->{synonym} = '';
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
		$this->{drugbank_id} = shift @attr;
		$this->{name} = shift @attr;
		$this->{synonym} = shift @attr;
		$this->{cid} = shift @attr;
		$this->{sid} = shift @attr;
	} else {
	    carp "Initializing drugbank_cid_sid : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
