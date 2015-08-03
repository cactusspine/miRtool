package DbMouseOrthology;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ORTHOLOGY_SELECT_STATEMENT => "SELECT id FROM mouse_orthology WHERE protein_family_id=?";
use constant LOAD_STATEMENT => "SELECT * FROM mouse_orthology WHERE id=?";

sub GetOrthologyIdsForFamilyId {
    my $familyId = shift;
    
    my @mouse_orthologyIds = ();
    if ($familyId) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare(ORTHOLOGY_SELECT_STATEMENT);
	$select->execute($familyId);
	my $nr = $select->rows();
	while ($nr--) {
	    push @mouse_orthologyIds, $select->fetchrow_array();
	}
    }
    @mouse_orthologyIds;
}

sub GetOrthologyIdForProtein {
    my $protein = shift;

    my $mouse_orthologyId = ();
    if ($protein) {
        my $databaseHandle = DbSession::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM mouse_orthology WHERE protein=?");
        $select->execute($protein);
        $mouse_orthologyId = $select->fetchrow_array();
    }
    $mouse_orthologyId;
} # sub GetOrthologyIdForProtein {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{PFID} = 0;
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
    my $mouse_orthologyId = shift;

    if ($mouse_orthologyId) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($mouse_orthologyId);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
	    $this->{PFID} = shift @attr;
            $this->{GeneDBID} = shift @attr;
	    $this->{Protein} = shift @attr;
            $this->{GenomeDBID} = shift @attr;
            $this->{Orthologs} = shift @attr;
            $this->{OrthologsDetails} = shift @attr;
	} else {
	    carp "Initializing mouse_orthology : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
