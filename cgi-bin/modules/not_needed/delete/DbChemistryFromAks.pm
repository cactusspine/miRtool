package DbChemistryFromAks;

use DbSessionAks;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT BIO_ELEMENT_ID, BIOENTITY_ID, BIO_ELEMENT_NAME, BIOENTITY_TYPE_ID, BIOLOGICAL_DB_ID FROM KDB_USER.KDB_BIO_ELEMENT D WHERE D.BIO_ELEMENT_NAME=?";


sub GetsiRNAIdsForGene {
    my $gene = shift;

    my @sirna_ids = ();
    if ($gene) {
        my $databaseHandle = DbSessionAks::GetConnection();
        my $select = $databaseHandle->prepare("SELECT id FROM sirna WHERE gene=?");
        $select->execute("$gene");
	my $nr = $select->rows();
        while ($nr--) {
            push @sirna_ids, $select->fetchrow_array();
        }
    }
   @sirna_ids;	
} # sub GetsiRNAIdsForGene {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{BIO_ELEMENT_ID} = 0;
    $this->{BIOENTITY_ID} = 0;
    $this->{BIO_ELEMENT_NAME} = '';
    $this->{BIOENTITY_TYPE_ID} = 0;
    $this->{BIOLOGICAL_DB_ID} = 0;

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $id = shift;

    if ($id) {
	my $databaseHandle = DbSessionAks::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($id);
		my @attr = $select->fetchrow_array;
		$this->{BIO_ELEMENT_ID} = shift @attr;
		$this->{BIOENTITY_ID} = shift @attr;
		$this->{BIO_ELEMENT_NAME} = shift @attr;
		$this->{BIOENTITY_TYPE_ID} = shift @attr;
		$this->{BIOLOGICAL_DB_ID} = shift @attr;
    }
}


1;
