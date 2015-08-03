package DbEffPathwayReactome;

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM eff_pathway_reactome WHERE id=?";


sub GetAllPathwayReactomeIds {

    my @reactome_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM eff_pathway_reactome");
        $select->execute();
	my $nr = $select->rows();
        while ($nr--) {
            push @reactome_ids, $select->fetchrow_array();
        }
   @reactome_ids;	
} # sub GetMatadorIdForProtein {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{EnsemblGene} = '';
    $this->{ReactomeID} = '';
    $this->{PathwayName} = '';
    $this->{ReactomeDBID} = '';

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
		$this->{ReactomeID} = shift @attr;
		$this->{PathwayName} = shift @attr;
		$this->{ReactomeDBID} = shift @attr;
	} else {
	    carp "Initializing eff_pathway_reactome : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
