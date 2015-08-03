package DbMousePathwayKegg;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM mouse_pathway_kegg WHERE id=?";

use constant GENE_LOAD_STATEMENT => "SELECT id FROM mouse_pathway_kegg WHERE gene=?";


sub new {
	my $class = shift;
	my $this = $class->SUPER::new();

	$this->{DBID} = 0;
	$this->{gene} = '';
	$this->{kegg_id} = '';
	$this->{pathway_description} = '';
	$this->{kegg_gene} = '';

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
	  	$this->{kegg_id} = shift @attr;
	  	$this->{pathway_description} = shift @attr;
	  	$this->{kegg_gene} = shift @attr;
		}
		elsif($select->rows > 1) {
#print "loadStatement : $loadStatement\n";
#print "criteria : $criteria \n";
	    carp "Initializing mouse_pathway_kegg : unexpected number of records = ",$select->rows,"\n";
		}
	}
}


1;
