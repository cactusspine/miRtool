package DbGprotPathwayKegg;

##########################################
##
## Document   : DbGprotPathwayKegg.pm
## Created on : May 30th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM gprot_pathway_kegg WHERE id=?";


sub GetPathwayNameForKeggId {
	my $kegg_id = shift;
	my $pathway_name = "";
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare("SELECT DISTINCT pathway_description FROM gprot_pathway_kegg WHERE kegg_id=?");
	$select->execute($kegg_id);
        $pathway_name = $select->fetchrow_array();

	$pathway_name;
} # sub GetPathwayNameForKeggId {

sub GetAllPathwayKeggIds {

    my @kegg_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM gprot_pathway_kegg");
        $select->execute();
	my $nr = $select->rows();
        while ($nr--) {
            push @kegg_ids, $select->fetchrow_array();
        }
   @kegg_ids;	
} # sub GetMatadorIdForProtein {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{EnsemblGene} = '';
    $this->{KeggID} = '';
    $this->{PathwayName} = '';
    $this->{KeggGenes} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $id = shift;

    if ($id) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($id);
	if ($select->rows == 1) {
		my @attr = $select->fetchrow_array;
		$this->{DBID} = shift @attr;
		$this->{EnsemblGene} = shift @attr;
		$this->{KeggID} = shift @attr;
		$this->{PathwayName} = shift @attr;
		$this->{KeggGenes} = shift @attr;
	} else {
	    carp "Initializing gprot_pathway_kegg : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
