package DbDomain;

use DbSession;
use Carp;

use base DeepPrintable;


use constant SMART_ID_LOAD_STATEMENT => "SELECT id, protein_id, protein, dbname, description, start, end FROM smart_domains WHERE id=?";

use constant PFAM_ID_LOAD_STATEMENT => "SELECT id, protein_id, protein, dbname, description, start, end FROM pfam_domains WHERE id=?";


sub GetDomainIdsForPIDandDBName {
	my ($protein_id, $dbname) = @_;
	my @domainsIds = ();
	if ($protein_id) {
		my $databaseHandle = DbSession::GetConnection();
		my $statement = "";
		if ($dbname eq "Smart") {
			$statement = "SELECT id FROM smart_domains WHERE protein_id=? ORDER BY start";
		}	
		else {
			$statement = "SELECT id FROM pfam_domains WHERE protein_id=? ORDER BY start";
		}
		my $select = $databaseHandle->prepare($statement);
		$select->execute($protein_id);
		my $nr = $select->rows();
	        while ($nr--) {
			push @domainsIds, $select->fetchrow_array();
		} # while ($nr--) {
	} # if ($protein_id) {
	@domainsIds;
} # sub GetDomainIdsForPIDandDBName {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{ProteinID} = '';
    $this->{Protein} = '';
    $this->{DBName} = '';
    $this->{Description} = '';
    $this->{Start} = 0;
    $this->{End} = 0;

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $dbname = shift;
    my $loadStatement = '';
    if ($dbname eq 'Smart') {
	$loadStatement = SMART_ID_LOAD_STATEMENT;
    }
    else {
	$loadStatement = PFAM_ID_LOAD_STATEMENT;
    }	
    if ($criteria) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{ProteinID} = shift @attr;	
            $this->{Protein} = shift @attr;
            $this->{DBName} = shift @attr;
            $this->{Description} = shift @attr;
            $this->{Start} = shift @attr;
            $this->{End} = shift @attr;
	} else {
	    carp "Initializing TAMAHUD DOMAINS : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
