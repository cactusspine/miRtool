package DbGpcrPathwayPanther;

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM gpcr_pathway_panther WHERE id=?";


sub GetAllPathwayPantherIds {

    my @panther_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM gpcr_pathway_panther");
        $select->execute();
	my $nr = $select->rows();
        while ($nr--) {
            push @panther_ids, $select->fetchrow_array();
        }
   @panther_ids;	
} # sub GetMatadorIdForProtein {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{EnsemblGene} = '';
    $this->{PantherID} = '';
    $this->{PathwayName} = '';

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
		$this->{PantherID} = shift @attr;
		$this->{PathwayName} = shift @attr;
	} else {
	    carp "Initializing gpcr_pathway_panther : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
