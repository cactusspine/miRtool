package DbGprotOrthology;

##########################################
##
## Document   : DbGprotOrthology.pm
## Created on : May 27th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant ORTHOLOGY_SELECT_STATEMENT => "SELECT id FROM gprot_orthology WHERE protein_family_id=?";
use constant LOAD_STATEMENT => "SELECT id,  protein_dbid, protein, dbid, orthologs, orthologs_details FROM gprot_orthology WHERE id=?";

sub GetOrthologyIdsForFamilyId {
    my $familyId = shift;
    
    my @gprot_orthologyIds = ();
    if ($familyId) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare(ORTHOLOGY_SELECT_STATEMENT);
	$select->execute($familyId);
	my $nr = $select->rows();
	while ($nr--) {
	    push @gprot_orthologyIds, $select->fetchrow_array();
	}
    }
    @gprot_orthologyIds;
}

sub GetOrthologyIdForProtein {
    my $protein = shift;

    my $gprot_orthologyId = ();
    if ($protein) {
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM gprot_orthology WHERE protein=?");
        $select->execute($protein);
        $gprot_orthologyId = $select->fetchrow_array();
    }
    $gprot_orthologyId;
} # sub GetOrthologyIdForProtein {

#sub GetOrthologyIdForHugoName {
#    my $protein = shift;
#
#    my $gprot_orthologyId = ();
#    if ($protein) {
#        my $databaseHandle = DbSessionGpdb::GetConnection();
#        my $select = $databaseHandle->prepare("SELECT id FROM gprot_orthology WHERE hugo_name=?");
#        $select->execute($protein);
#        $gprot_orthologyId = $select->fetchrow_array();
#    }
#    $gprot_orthologyId;
#} # sub GetOrthologyIdForHugoName {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{GeneDBID} = '';
    $this->{Protein} = '';
    $this->{GenomeDBID} = 0;
    $this->{Orthologs} = '';
    $this->{OrthologsDetails} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $gprot_orthologyId = shift;

    if ($gprot_orthologyId) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($gprot_orthologyId);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{GeneDBID} = shift @attr;
	    $this->{Protein} = shift @attr;
            $this->{GenomeDBID} = shift @attr;
            $this->{Orthologs} = shift @attr;
            $this->{OrthologsDetails} = shift @attr;
	} else {
	    carp "Initializing Orthologs : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
