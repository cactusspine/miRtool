package DbMatador;

use DbSessionChemistry;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT id,  chemical_id, chemical_name, atc, protein_id, protein_name, mesh_id, uniprot_id, protein_score, protein_annotation, mesh_score, mesh_annotation, matador_score, matador_annotation FROM matador WHERE id=?";


sub GetMatadorIdsForUniprot {
    my $protein = shift;

    my @matador_ids = ();
    if ($protein) {
        my $databaseHandle = DbSessionChemistry::GetConnection();
        my $query = "SELECT id FROM matador WHERE uniprot_id LIKE?";
        my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
       #$select->execute("%$protein%");
        $select->execute("%$protein%") or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
        while ($nr--) {
            push @matador_ids, $select->fetchrow_array();
        }
    }
   @matador_ids;	
} # sub GetMatadorIdForUniprot {

sub GetPubchemCidNameForProtein {
    my $protein_id = shift;
print STDERR "protein_id : $protein_id\n";
    my @cid_name = ();
    if ($protein_id) {
        my $databaseHandle = DbSessionChemistry::GetConnection();
        my $query = "SELECT DISTINCT(chemical_id), chemical_name FROM matador WHERE protein_id=?";
print STDERR "query : $query\n";				
#        my $select = $databaseHandle->prepare($query);
#        $select->execute($protein_id);
        my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
        $select->execute($protein_id) or die "unable to execute" . $databaseHandle->errstr;
        my $nr = $select->rows();
        while ($nr--) {
#            push @cid, $select->fetchrow_array();
             my ($cid, $name) = $select->fetchrow_array();
             my $cid_name = $cid . "__" . $name;
print STDERR "cid_name : $cid_name\n";						 
             push @cid_name, $cid_name;
        }
    }
   @cid_name;
} # sub GetPubchemCidNameForProtein {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{ChemicalID} = 0;
    $this->{ChemicalName} = '';
    $this->{ATC} = '';
    $this->{ProteinID} = '';
    $this->{ProteinName} = '';
    $this->{MeshID} = '';
    $this->{UniprotID} = '';
    $this->{ProteinScore} = 0;
    $this->{ProteinAnnotation} = '';
    $this->{MeshScore} = 0;
    $this->{MeshAnnotation} = '';
    $this->{MatadorScore} = 0;
    $this->{MatadorAnnotation} = '';

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
		$this->{DBID} = shift @attr;
		$this->{ChemicalID} = shift @attr;
		$this->{ChemicalName} = shift @attr;
		$this->{ATC} = shift @attr;
		$this->{ProteinID} = shift @attr;
		$this->{ProteinName} = shift @attr;
		$this->{MeshID} = shift @attr;
		$this->{UniprotID} = shift @attr;
		$this->{ProteinScore} = shift @attr;
		$this->{ProteinAnnotation} = shift @attr;
		$this->{MeshScore} = shift @attr;
		$this->{MeshAnnotation} = shift @attr;
		$this->{MatadorScore} = shift @attr;
		$this->{MatadorAnnotation} = shift @attr;
	} else {
	    carp "Initializing Matador : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
