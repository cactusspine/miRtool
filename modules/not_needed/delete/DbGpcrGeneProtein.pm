package DbGpcrGeneProtein;

##########################################
##
## Document   : DbGpcrGeneProtein.pm
## Created on : May 20th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM gpcr_gene_protein WHERE id=?";

use constant GENE_LOAD_STATEMENT => "SELECT * FROM gpcr_gene_protein WHERE gene=?";

#sub GetGeneProteinIdsForHugoName {
#	my $hugo_name = shift;
#	 my @ids = ();
#	if ($hugo_name) {
#		my $statement =  "SELECT id FROM gene_protein WHERE hugo_name = ?";
#		my $databaseHandle = DbSessionGpdb::GetConnection();
#	        my $select = $databaseHandle->prepare($statement);
#        	$select->execute($hugo_name);
#	        my $nr = $select->rows();
#        	while ($nr--) {
#                	push @ids, $select->fetchrow_array();
#	        }	
#	} # if ($hugo_name) {
#	@ids;
#} # sub GetGeneProteinIdsForHugoName {

sub GetGeneProteinIdsForSearchTerm {
	my $search_term = shift;
	 my @ids = ();
	if ($search_term) {
		my $statement =  "SELECT id FROM gpcr_gene_protein WHERE gene LIKE '%$search_term%' OR description LIKE '%$search_term%' OR all_proteins LIKE '%$search_term%'";
		my $databaseHandle = DbSessionGpdb::GetConnection();
	        my $select = $databaseHandle->prepare($statement);
        	$select->execute();
	        my $nr = $select->rows();
        	while ($nr--) {
                	push @ids, $select->fetchrow_array();
	        }	
	} # if ($search_term) {
	@ids;
} # sub GetGeneProteinIdsForSearchTerm {

sub GetAllGeneProteinsIds {
	my ($field_name, $asse_or_desc) = @_;
        my @ids = ();
        my $statement =  "";
		$statement = "SELECT DISTINCT gp.id FROM gpcr_gene_protein gp, gpcr_validation pv WHERE gp.gene = pv.ensembl_gene ORDER BY pv.$field_name $asse_or_desc";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare($statement);
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
		push @ids, $select->fetchrow_array();
        }
        @ids;
} # sub GetAllGeneProteinsIds {


sub GetAllGenes {
        my @genes = ();
        my $statement =  "SELECT gene FROM gpcr_gene_protein";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare($statement);
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
                push @genes, $select->fetchrow_array();
        }
        @genes;
} # sub GetAllGenes {

sub GetGeneDes {
	my $gene = shift;
        my $des = "";
        my $statement =  "SELECT description FROM gpcr_gene_protein where gene=?";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare($statement);
        $select->execute($gene);
                $des= $select->fetchrow_array();
        $des;
} # sub GetGeneDes {


sub GetGeneForProtein {
        my $protein = shift;
        my $gene = "";
        my $statement =  "SELECT gene FROM gpcr_gene_protein where longest_protein=?";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare($statement);
        $select->execute($protein);
                $gene= $select->fetchrow_array();
        $gene;
} # sub GetGeneForProtein {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{GeneGID} = '';
    $this->{Gene} = '';
    $this->{GID} = 0;
    $this->{Description} = '';
    $this->{LongestProtein} = '';
    $this->{AllProteins} = '';
    $this->{DBlinks} = '';

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
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
#	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{GeneGID} = shift @attr;
	    $this->{Gene} = shift @attr;
            $this->{GID} = shift @attr;
            $this->{Description} = shift @attr;
            $this->{LongestProtein} = shift @attr;
            $this->{AllProteins} = shift @attr;
            $this->{DBlinks} = shift @attr;
#	}
#	elsif($select->rows > 1) {
#print "loadStatement : $loadStatement\n";
#print "criteria : $criteria \n";
#	    carp "Initializing Gene_Protein : unexpected number of records = ",$select->rows,"\n";
#	}
    }
}


1;
