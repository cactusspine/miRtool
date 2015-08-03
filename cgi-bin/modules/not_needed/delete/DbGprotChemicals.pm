package DbGprotChemicals;

##########################################
##
## Document   : DbGprotChemicals.pm
## Created on : June 20th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM gprot_chemicals WHERE id=?";


sub GetChemicalIdsForGene {
	my $gene_id = shift;
	 my @ids = ();
	if ($gene_id) {
		my $statement =  "SELECT id FROM gprot_chemicals WHERE gene=? AND relevance>=50";
		my $databaseHandle = DbSessionGpdb::GetConnection();
	        my $select = $databaseHandle->prepare($statement);
        	$select->execute($gene_id);
	        my $nr = $select->rows();
        	while ($nr--) {
                	push @ids, $select->fetchrow_array();
	        }	
	} # if ($gene_id) {
	@ids;
} # sub GetChemicalIdsForGene {

sub GetChemicalDetailsForGene {
        my $gene_id = shift;
 #       my @details = ();
	my %details = ();
        if ($gene_id) {
                my $statement =  "SELECT C.name, C.category, C.relevance, D.bio_element_name FROM gprot_chemicals C, gprot_chemical_details D WHERE C.gene=? AND C.relevance>=50 AND C.bioentity_id=D.bioentity_id AND D.biological_db_id=107 order by C.relevance desc;";
                my $databaseHandle = DbSessionGpdb::GetConnection();
                my $select = $databaseHandle->prepare($statement);
                $select->execute($gene_id);
                my $nr = $select->rows();
                while ($nr--) {
			my @temp =  $select->fetchrow_array();
			my ($name, $category, $relevance, $bio_element_name) = @temp;
#			push (@details, [@temp]);
			$details{$name}{category}  =  $category;
			$details{$name}{relevance} = $relevance;
			push @{$details{$name}{bio_element_name}}, $bio_element_name;
                }
        } # if ($gene_id) {
        %details;
} # sub GetChemicalDetailsForGene {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{category} = '';
    $this->{gene} = '';
    $this->{bioentity_id} = 0;
    $this->{bioentity_name} = '';
    $this->{name} = '';
    $this->{tot_docs} = 0;
    $this->{relevance} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $id = shift;
    my $loadStatement = ID_LOAD_STATEMENT;

    if ($id) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($id);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{id} = shift @attr;
            $this->{category} = shift @attr;
	    $this->{gene} = shift @attr;
            $this->{bioentity_id} = shift @attr;
            $this->{bioentity_name} = shift @attr;
            $this->{name} = shift @attr;
            $this->{tot_docs} = shift @attr;
            $this->{relevance} = shift @attr;
	}
	else{
#print "loadStatement : $loadStatement\n";
	    carp "Initializing gprot_chemicals : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
