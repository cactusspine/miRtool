package DbMouseGeneNameDes;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM mouse_gene_name_des WHERE id=?";

use constant GENE_LOAD_STATEMENT => "SELECT * FROM mouse_gene_name_des WHERE gene=?";


sub GetTableViewInfo {
	my ($field_name, $asse_or_desc, $tmp_database, $tmp_table) = @_;
        my %result_hash = ();
	my $statement = "";
	if ($field_name eq "description") {
#		$statement = "SELECT b.id, b.gene, b.name, bhgp.description FROM biocompendium.mouse_gene_name b, biocompendium.mouse_gene_protein bhgp, $tmp_database.$tmp_table t WHERE t.gene = b.gene AND t.gene = bhgp.gene ORDER BY bhgp.$field_name $asse_or_desc";
		$statement = "SELECT b.id, b.gene, b.name, b.description FROM biocompendium.mouse_gene_name_des b, $tmp_database.$tmp_table t WHERE t.gene = b.gene ORDER BY b.$field_name $asse_or_desc";
	}
	else {
#		$statement = "SELECT b.id, b.gene, b.name, bhgp.description FROM biocompendium.mouse_gene_name b, biocompendium.mouse_gene_protein bhgp, $tmp_database.$tmp_table t WHERE t.gene = b.gene AND t.gene = bhgp.gene ORDER BY b.$field_name $asse_or_desc";
		$statement = "SELECT b.id, b.gene, b.name, b.description FROM biocompendium.mouse_gene_name_des b, $tmp_database.$tmp_table t WHERE t.gene = b.gene ORDER BY b.$field_name $asse_or_desc";
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
		my $description = $data[3];
		$result_hash{$i}{id} = $id; 
		$result_hash{$i}{gene} = $gene; 
		$result_hash{$i}{name} = $name; 
		$result_hash{$i}{description} = $description; 
        }
	\%result_hash;
} # sub GetTableViewInfo {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{gene} = '';
    $this->{name} = '';
    $this->{description} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $loadStatement = '';
    if ($criteria =~ /^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
    } else {
        $loadStatement = GENE_LOAD_STATEMENT;
    }


    if ($criteria) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
	    $this->{gene} = shift @attr;
      $this->{name} = shift @attr;
      $this->{description} = shift @attr;
	}
	elsif($select->rows > 1) {
#print "loadStatement : $loadStatement\n";
#print "criteria : $criteria \n";
	    carp "Initializing mouse_gene_name : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
