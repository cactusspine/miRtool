package DbGprotChemicalDetails;

##########################################
##
## Document   : DbGprotChemicalDetails.pm
## Created on : June 20th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM gprot_chemical_details WHERE id=?";


sub GetChemicalDetailsForBioentityId {
	my $bioentity_id = shift;
	 my @ids = ();
	if ($bioentity_id) {
		my $statement =  "SELECT id FROM gprot_chemical_details WHERE bioentity_id = ?";
		my $databaseHandle = DbSessionGpdb::GetConnection();
	        my $select = $databaseHandle->prepare($statement);
        	$select->execute($bioentity_id);
	        my $nr = $select->rows();
        	while ($nr--) {
                	push @ids, $select->fetchrow_array();
	        }	
	} # if ($bioentity_id) {
	@ids;
} # sub GetChemicalDetailsForBioentityId {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{category} = '';
    $this->{bioentity_id} = 0;
    $this->{biological_db_id} = 0;
    $this->{bio_element_name} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $id = shift;
    my $loadStatement = ID_LOAD_STATEMENT;

    if ($id) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($id);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{id} = shift @attr;
            $this->{category} = shift @attr;
            $this->{bioentity_id} = shift @attr;
            $this->{biological_db_id} = shift @attr;
            $this->{bio_element_name} = shift @attr;
	}
	else{
#print "loadStatement : $loadStatement\n";
	    carp "Initializing gprot_chemical_details : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
