package DbPdbLigand;

use DbSessionChemistry;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM pdb_ligand WHERE id=?";


sub GetPdbLigandIdsForPdb {
    my $pdb_id = shift;

    my @pdb_ligand_ids = ();
    if ($pdb_id) {
        my $databaseHandle = DbSessionChemistry::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM pdb_ligand WHERE pdb_id=?");
        $select->execute($pdb_id);
	my $nr = $select->rows();
        while ($nr--) {
            push @pdb_ligand_ids, $select->fetchrow_array();
        }
    }
   @pdb_ligand_ids;	
} # sub GetPdbLigandIdForPdb {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{category} = '';
    $this->{pdb_id} = '';
    $this->{chain} = '';
    $this->{pubchem_cid} = '';
    $this->{name} = '';

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
		$this->{category} = shift @attr;
		$this->{pdb_id} = shift @attr;
		$this->{chain} = shift @attr;
		$this->{pubchem_cid} = shift @attr;
		$this->{name} = shift @attr;
	} else {
	    carp "Initializing pdb_ligand : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
