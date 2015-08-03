package DbHumanClinicalTrails;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM human_clinical_trails WHERE id=?";



sub GetIdsForGene {
	my $gene = shift;
	 my @ids = ();
	if ($search_term) {
		my $statement =  "SELECT id FROM human_clinical_trails WHERE gene = ?";
		my $databaseHandle = DbSession::GetConnection();
	        my $select = $databaseHandle->prepare($statement);
        	$select->execute($gene);
	        my $nr = $select->rows();
        	while ($nr--) {
                	push @ids, $select->fetchrow_array();
	        }	
	} # if ($search_term) {
	@ids;
} # sub GetIdsForGene {


sub GetClinicalTrailInfo {
	my ($field_name, $asse_or_desc, $tmp_database, $tmp_table) = @_;
        my %result_hash = ();
	my $statement = "";
	if ($field_name eq "name") {
		$statement = "SELECT ct.id, ct.gene, b.name, ct.clinical_trail_id, ct.title FROM biocompendium.human_clinical_trails ct, biocompendium.human_gene_name b,  $tmp_database.$tmp_table t WHERE t.gene = b.gene AND ct.gene = b.gene ORDER BY b.$field_name $asse_or_desc";
	}
	else {
		$statement = "SELECT ct.id, ct.gene, b.name, ct.clinical_trail_id, ct.title FROM biocompendium.human_clinical_trails ct, biocompendium.human_gene_name b, $tmp_database.$tmp_table t WHERE t.gene = b.gene AND ct.gene = b.gene ORDER BY ct.$field_name $asse_or_desc";
	}
        my $databaseHandle = DbSession::GetConnection();
        my $select = $databaseHandle->prepare($statement);
        $select->execute();
        my $nr = $select->rows();
	my @data;
	my $i = 0;
        while ($nr--) {
		$i++;
		@data = $select->fetchrow_array();
		my $id = $data[0];
		my $gene = $data[1];
		my $name = $data[2];
		my $clinical_trail_id = $data[3];
		my $title = $data[4];
		$result_hash{$i}{id} = $id; 
		$result_hash{$i}{gene} = $gene; 
		$result_hash{$i}{name} = $name; 
		$result_hash{$i}{clinical_trail_id} = $clinical_trail_id; 
		$result_hash{$i}{title} = $title; 
        }
	\%result_hash;
} # sub GetTableViewInfo {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{gene} = '';
    $this->{longest_protein} = '';
    $this->{clinical_trail_id} = '';
    $this->{title} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $loadStatement = ID_LOAD_STATEMENT;


    if ($criteria) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
	    $this->{gene} = shift @attr;
      $this->{longest_protein} = shift @attr;
      $this->{clinical_trail_id} = shift @attr;
      $this->{title} = shift @attr;
	}
	elsif($select->rows > 1) {
#print "loadStatement : $loadStatement\n";
#print "criteria : $criteria \n";
	    carp "Initializing human_clinical_trails : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
